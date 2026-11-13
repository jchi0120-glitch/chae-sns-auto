import json
ST="""<style>
.bg{position:absolute;z-index:-1;top:-150px;left:-72px;width:1080px;height:1350px;background-size:cover;background-repeat:no-repeat}
.bg:after{content:'';position:absolute;inset:0;background:linear-gradient(180deg,rgba(11,15,23,.78) 0%,rgba(11,15,23,.25) 18%,rgba(11,15,23,.25) 70%,rgba(11,15,23,.85) 100%)}
.bg.dim:after{background:rgba(11,15,23,.62)}
.st{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center}
.mb{background:rgba(22,30,48,.9);color:#fff;font-size:50px;font-weight:800;line-height:1.38;padding:32px 42px;text-align:center;border:3px solid #46D682;border-radius:6px;box-shadow:0 10px 30px rgba(0,0,0,.35)}
.mb.k{background:rgba(11,15,23,.92);border:2px solid rgba(255,255,255,.22)}
.mb small{display:block;font-size:31px;font-weight:600;line-height:1.5;margin-top:14px;opacity:.72}
.br{background:linear-gradient(90deg,#46D682,#D6EC60);color:#0f1a14;border-radius:44px;font-size:40px;font-weight:800;padding:16px 30px;box-shadow:0 8px 24px rgba(0,0,0,.25);text-align:center;line-height:1.35}
.big{font-size:92px;font-weight:900;line-height:1.15}
.y{color:#FFD84D}.r{color:#ff6b6b}
.q{font-size:34px;font-weight:700;color:#fff;background:rgba(11,15,23,.7);padding:14px 26px;border-radius:40px}

</style>"""
def card(photo,pos,inner,bridge,dim=False,top=70):
    return ST+f"""<div class='bg{' dim' if dim else ''}' style="background-image:url('{photo}');background-position:{pos}"></div><div class=st><div style='height:{top}px'></div>{inner}<div style='flex:1'></div><div class=br>{bridge}</div><div style='height:250px'></div></div>"""
S=[]
# 1 훅
S.append(ST+"""<div class='bg' style="background-image:url('photo_front.jpg');background-position:center 60%"></div><div class=st><div style='height:40px'></div><div class=mb style='font-size:64px;padding:34px 48px'>면허 딴 지 한 달인데..<br>장기렌트가 된다고요?</div><div style='height:28px'></div><div class=q style='font-size:40px;padding:16px 32px;border:2px solid #FFD84D'><span class=y style='font-weight:900;font-size:48px'>면허 1달 초보 운전자</span> · 레이 출고후기</div><div style='flex:1'></div></div>""")
# 2
S.append(card('photo_side.jpg','center',"<div class='mb k'><small style='margin:0 0 16px;opacity:.6'>상담 오시는 분들이 제일 많이 하시는 말</small>\"면허 딴 지 얼마 안 됐는데<br>괜히 물어보는 거 아닌가요?\"</div><div style='height:28px'></div><div class=mb style='font-size:44px'>장기렌트는 대부분<br><span class=y>면허 취득 1년 이상</span>부터라<small>초보 운전자는 문턱에서 막히는 경우가 많죠</small></div>","근데 저는 좀 달랐던 게..👉🏻",dim=True))
# 3
S.append(card('photo_front.jpg','center 40%',"<div class='mb k'><small style='margin:0 0 10px'>14년차 · 누적출고 1,600대+</small>면허 1년 미만도 받아주는<br><span class='y' style='font-size:76px;font-weight:900'>협업 업체 2곳</span></div>","그래서 바로 진행했는데 문제가..👉🏻",dim=True,top=110))
# 4
S.append(card('photo_interior.jpg','center 30%',"<div class=mb>고객님 원픽 <span class=y>캐스퍼</span><small>상담 당시 신차 대기 최소 · 렌트사 재고 0대</small><span class='big r'>10개월+</span></div><div style='height:28px'></div><div class='mb k' style='font-size:46px'>그래서 본 <span class=y>레이</span>도<br>신차는 <span class=r style='font-weight:900'>최소 4개월 대기</span></div>","여기서 포기하면 채팀장이 아니죠👉🏻",dim=True))
# 5
S.append(card('photo_front.jpg','center 45%',"<div class=mb style='font-size:44px'>렌트사 재고를<br>하나하나 직접 돌려서</div><div style='height:30px'></div><div class='mb k'><span class='big y'>즉시 출고</span><br>레이 시그니처 확보</div>","근데.. 이런 거 젤 신경 쓰이는 게👉🏻",dim=True))
# 9
S.append(card('photo_interior.jpg','center 30%',"<div class=mb style='font-size:46px'>① 초보 운전자는<br><span class=y>보험료</span>가 높게 잡혀요<small>렌트는 보험료가 월 납입금에 같이 들어가요</small></div><div style='height:30px'></div><div class='mb k' style='font-size:46px'>② 5년은 부담돼서<br><span class=y>3년 정도</span>만 타고 싶으셨어요</div>","그래서 추천드린 게..👉🏻",dim=True))
# 10
S.append(card('photo_side.jpg','center',"<div class='mb k'><small style='margin:0 0 10px'>채팀장 추천 · 자유반납형</small>계약은 <span class=y>5년</span>인데<br><span class='big y'>3년 후부터</span><br>위약금 없이 반납 가능<small>5년 기준이라 월 납입금은 낮게</small></div><div style='height:28px'></div><div class=mb style='font-size:46px'>사실상 <span class=y style='font-weight:900'>3년 계약</span>이나 다름없어요</div>","실제 견적은..👉🏻",dim=True))
# 11 견적서
S.append(ST+"""<div class=st style='background:radial-gradient(900px 700px at 85% 0%,rgba(70,214,130,.18),transparent 60%),#0b0f17;left:-72px;right:-72px;top:-150px;bottom:-140px;padding-top:250px'><div class='mb k' style='font-size:40px;padding:20px 34px'>레이 시그니처 실제 견적서</div><div style='height:30px'></div><img src='quote.jpg' style='width:900px;border-radius:18px;box-shadow:0 12px 30px rgba(0,0,0,.3)'><div style='height:30px'></div><div class=mb style='font-size:40px'>60개월 · 연 2만km<br>월 <span class=y style='font-size:64px;font-weight:900'>407,550원</span> <span style='font-size:28px;opacity:.7'>VAT 포함</span><small>블랙박스 · 전면 썬팅 부가서비스 포함</small></div><div style='flex:1'></div><div class=br>더 대박인 건..👉🏻</div><div style='height:250px'></div></div>""")
# 12
S.append(card('photo_interior.jpg','center 35%',"<div class='mb k'><small style='margin:0 0 10px'>계약부터 인도까지</small><span class=big style='font-size:76px'>금요일 계약<br><span class=y>수요일 인도</span></span><small>코일매트까지 서비스로 깔아드렸어요</small></div><div style='height:22px'></div><div class=mb style='font-size:40px;padding:24px 38px'>\"이 정도면<br>진짜 잘한 선택 같아요!\"<small>레이 고객님, 인도 날 하신 말이에요</small></div>","저처럼 면허 딴 지 얼마 안 됐다면..👉🏻",dim=True,top=40))
# 14 CTA
S.append("""<style></style><span class=tag>첫 차 고민 중이라면</span><h2 style='font-size:62px'>면허 1년 미만이라고<br><span style="color:#FFD84D">혼자 포기하지 마세요</span></h2><div class=steps><div class=step><div class=n>1</div><div><div class=t>프로필 링크 → 1:1 카톡</div><div class=d>@consultant_chae 프로필에 바로 연결돼요</div></div></div><div class=step><div class=n>2</div><div><div class=t>이것만 보내주세요</div><div class=d>면허 취득일 · 원하는 차종 · 이용 기간</div></div></div><div class=step><div class=n>3</div><div><div class=t>렌트사·재고 직접 확인</div><div class=d>받아주는 곳과 즉시 출고 차량부터 찾아드려요</div></div></div></div><p class=note>심사 기준·납기·반납 조건은 렌트사와 시점에 따라 달라질 수 있어요</p>""")
json.dump({"handle":"@consultant_chae","slides":[{"body":b} for b in S]},open('slides.json','w'),ensure_ascii=False,indent=1)
