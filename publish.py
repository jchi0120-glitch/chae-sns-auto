"""채팀장 SNS 예약발행 스크립트 (GitHub Actions에서 실행)

posts/<글이름>/post.json 중 발행 시각이 지났고 아직 안 올라간 것을 찾아
인스타 카드뉴스(캐러셀)와 쓰레드(본글 + 댓글 체인)를 발행한다.
발행 결과는 posts/<글이름>/published.json 에 기록되어 중복 발행을 막는다.

환경변수(GitHub Secrets/Variables):
  IG_TOKEN, IG_USER_ID        인스타 (Unified login 시스템 사용자 토큰)
  THREADS_TOKEN               쓰레드 (없으면 쓰레드는 건너뜀)
  REPO_RAW_BASE               이미지 공개 주소 앞부분
  DRY_RUN=1                   실제 발행 없이 점검만
"""
import json, os, sys, time, pathlib, datetime as dt
import requests

KST = dt.timezone(dt.timedelta(hours=9))
GRAPH = "https://graph.facebook.com/v24.0"
THREADS = "https://graph.threads.net/v1.0"
ROOT = pathlib.Path(__file__).parent
DRY = os.getenv("DRY_RUN") == "1"
RAW = os.getenv("REPO_RAW_BASE", "https://raw.githubusercontent.com/jchi0120-glitch/chae-sns-auto/main")


def call(method, url, **params):
    r = requests.request(method, url, params=params, timeout=60)
    data = r.json() if r.content else {}
    if r.status_code >= 400 or "error" in data:
        raise RuntimeError(f"{url.split('?')[0]} -> {r.status_code} {data.get('error', data)}")
    return data


def wait_ready(base, cid, token, field="status_code"):
    for _ in range(30):
        st = call("GET", f"{base}/{cid}", fields=field, access_token=token).get(field)
        if st == "FINISHED":
            return
        if st in ("ERROR", "EXPIRED"):
            raise RuntimeError(f"컨테이너 {cid} 처리 실패: {st}")
        time.sleep(5)
    raise RuntimeError(f"컨테이너 {cid} 처리 시간 초과")


def post_instagram(folder, ig):
    token, uid = os.environ["IG_TOKEN"], os.environ["IG_USER_ID"]
    urls = [f"{RAW}/posts/{folder.name}/{name}" for name in ig["images"]]
    if DRY:
        print("  [점검] 인스타 이미지", len(urls), "장:", urls[0], "...")
        return "dry-run"
    children = []
    for u in urls:
        c = call("POST", f"{GRAPH}/{uid}/media", image_url=u, is_carousel_item="true", access_token=token)["id"]
        children.append(c)
    for c in children:
        wait_ready(GRAPH, c, token)
    car = call("POST", f"{GRAPH}/{uid}/media", media_type="CAROUSEL",
               children=",".join(children), caption=ig["caption"], access_token=token)["id"]
    wait_ready(GRAPH, car, token)
    return call("POST", f"{GRAPH}/{uid}/media_publish", creation_id=car, access_token=token)["id"]


def post_threads(chain):
    token = os.getenv("THREADS_TOKEN")
    if not token:
        print("  쓰레드 토큰 없음 → 건너뜀")
        return None
    if DRY:
        print("  [점검] 쓰레드", len(chain), "개 연결 글")
        return "dry-run"
    ids, reply_to = [], None
    for text in chain:
        params = dict(media_type="TEXT", text=text, access_token=token)
        if reply_to:
            params["reply_to_id"] = reply_to
        cid = call("POST", f"{THREADS}/me/threads", **params)["id"]
        time.sleep(10)
        reply_to = call("POST", f"{THREADS}/me/threads_publish", creation_id=cid, access_token=token)["id"]
        ids.append(reply_to)
    return ids


def main():
    now = dt.datetime.now(KST)
    failed = False
    for pj in sorted(ROOT.glob("posts/*/post.json")):
        folder = pj.parent
        post = json.loads(pj.read_text(encoding="utf-8"))
        done_f = folder / "published.json"
        done = json.loads(done_f.read_text()) if done_f.exists() else {}
        when = dt.datetime.fromisoformat(post["publish_at"])
        if when > now:
            continue
        print(f"▶ {folder.name} (예약 {when:%m/%d %H:%M})")
        for key, fn in (("instagram", lambda: post_instagram(folder, post["instagram"])),
                        ("threads", lambda: post_threads(post["threads"]))):
            if key not in post or key in done:
                continue
            try:
                res = fn()
                if res is not None and not DRY:
                    done[key] = {"id": res, "at": dt.datetime.now(KST).isoformat()}
                print(f"  {key} 완료: {res}")
            except Exception as e:
                failed = True
                print(f"  {key} 실패: {e}")
        if done and not DRY:
            done_f.write_text(json.dumps(done, ensure_ascii=False, indent=2))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
