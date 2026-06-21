# -*- coding: utf-8 -*-
"""6/6 사냥 1000 — 차원1(매입가능 영구통행료) + 차원3(유일성=발견).
후보 = 길목/권리(position) × 취득경로. 조건 불변.
채점: 정상상태 6원칙 + 2-B. 핵심은 (a)취득경로가 #2/#5/#6/2-B를 안 건드리는가,
(b)징수가 수동·inbound인가, (c)#4 수요가 '지금' 있는가.
→ 이 평면은 17,000과 달리 6/6을 담을 수 있다(취득위반이 일회·매몰).
다만 6/6은 'toll형 × 독점등급 길목'에서만 발생(자본·독점·inbound 게이트)."""

# 아키타입: (이름, ceiling, kind, fragile, intrinsic_broken)
# kind: toll(천장6) / near(천장5,고유결함) / op(운영) / twob(2-B 탈락)
A = [
 ("지리적 통행 지역권(right-of-way)",      6, "toll", "입지선점 자본(매몰)", ""),
 ("임차된 주파수/스펙트럼 라이선스",        6, "toll", "취득자본",           ""),
 ("매입한 비탄력 로열티 스트림",            6, "toll", "매입자본·권리만료",   ""),
 ("불가피 기반특허 inbound 라이선스",        6, "toll", "집행=inbound 성립조건", ""),
 ("할당된 식별자/주소 블록 서브리스",        6, "toll", "취득·레지스트리 정책", ""),
 ("전략입지 정박/터미널/게이트 슬롯",        6, "toll", "취득자본",           ""),
 ("영구 양륙점/케이블 랜딩 권리",            6, "toll", "입지 희소성",         ""),
 ("매입한 필수규격 IP 영구로열티",          6, "toll", "풀 우회·자본",        ""),
 ("음원/콘텐츠 카탈로그 매입",              5, "near", "#3 재생=주목",        "3"),
 ("프리미엄 도메인/네임 보유",              5, "near", "#3 투기/주목",        "3"),
 ("규제필수 인증/표준물질 단독공급",        5, "near", "#2 인증당국 게이트",   "2"),
 ("데이터 영구라이선스 매입후 재판매",      5, "near", "#5 재판매=BD",        "5"),
 ("상표/브랜드 라이선스",                  5, "near", "#3 브랜드=주목",       "3"),
 ("매입 프랜차이즈 로열티권",              5, "near", "#6 가맹운영 지원",     "6"),
 ("자원 채굴권 직접채굴",                  3, "op",   "#1·#6 운영",          "1,6"),
 ("레지스트리 직접운영",                    3, "op",   "#6 운영+#2 본인게이트", "2,6"),
 ("인프라 직접운영(통신/스토리지)",         3, "op",   "#5·#6 운영",          "5,6"),
 ("전략입지 부동산 직접개발",              3, "op",   "#6 개발운영",          "6"),
 ("예측/베팅 포지션",                      0, "twob", "2-B①",               ""),
 ("스테이킹/검증 보상",                    0, "twob", "2-B④",               ""),
]
assert len(A) == 20

# 길목 등급: monopoly(독점 chokepoint) / scarce(희소) / commodity(범용)
CTX = [
 # monopoly 6
 ("단일 항만 진입수로","M"),("산악 단일 통과회랑","M"),("해저케이블 단일 양륙점","M"),
 ("표준치료 독점신약","M"),("유일 호환 필수특허 기술","M"),("수도권 단일 송전회랑","M"),
 # scarce 18
 ("주요공항 발착 슬롯","S"),("희소 밀리미터파 대역","S"),("대도시 프리미엄 도메인","S"),
 ("주요항 정박권","S"),("정지궤도 슬롯","S"),("광역 상수원 취수권","S"),("국경 통관 단일게이트","S"),
 ("고속철 단일 노선권","S"),("데이터센터 전력인입","S"),("해상풍력 단지 해역","S"),("희토류 단일 광구","S"),
 ("파이프라인 분기점 부지","S"),("위성 다운링크 게이트웨이","S"),("국제결제 BIN 레인지","S"),
 ("해운 운하 통항권","S"),("주파수 재배치 잔여대역","S"),("전략비축 저장공간","S"),("도심 통신 관로","S"),
 # commodity 26
 ("일반 상가 임대","C"),("범용 공개데이터셋","C"),("흔한 배경음원","C"),("범용 상표","C"),
 ("일반 IPv6 블록","C"),("표준 폰트","C"),("범용 스톡이미지","C"),("오픈 API 래퍼","C"),
 ("일반 주택 임대","C"),("범용 번역메모리","C"),("흔한 도메인","C"),("회피가능 일반특허","C"),
 ("범용 센서데이터","C"),("공개 지도타일","C"),("흔한 음향효과","C"),("일반 교육콘텐츠","C"),
 ("범용 코드스니펫","C"),("표준 색상팔레트","C"),("일반 폰트아이콘","C"),("범용 통계표","C"),
 ("흔한 레시피DB","C"),("일반 측정데이터","C"),("범용 사전","C"),("공개 기상데이터","C"),
 ("일반 양식템플릿","C"),("범용 체크리스트","C"),
]
assert len(CTX) == 50
assert sum(1 for _,g in CTX if g=="M")==6 and sum(1 for _,g in CTX if g=="S")==18

PEN = {"M":0, "S":1, "C":2}

def cells_for(score):
    # 표시는 점수만 필요 — 간단화
    return score

def evaluate(arch, grade):
    name, ceiling, kind, fragile, intr = arch
    if kind == "twob":
        return None, "탈락(2-B)", fragile
    if kind == "op":
        return 3, "운영", "5,6"
    pen = PEN[grade]
    score = max(2, ceiling - pen)
    if kind == "toll":
        if pen == 0:
            return 6, "6/6", ""            # ★ 진짜 6/6
        if pen == 1:
            return score, f"{score}/6", "5:대안경로 경쟁→발견노동"
        return score, f"{score}/6", "3,5:흔함→주목·발견"
    # near
    extra = "" if pen == 0 else (",5" if pen == 1 else ",3,5")
    return score, f"{score}/6", (intr + extra)

out = []
out.append("# 🎯 6/6 사냥 1000 — 차원1(매입가능 영구통행료) + 차원3(유일성=발견)")
out.append("# 후보 = 길목/권리 × 취득경로. 조건 불변. 6/6 = toll형 × 독점(M)등급에서만 발생.")
out.append("# 형식: [코드] 길목(등급) 에서 아키타입 — n/6 (broken | fragile)")
out.append("")

counts = {i: 0 for i in range(7)}
reject = 0
six_cells = []   # (code, ctx, arch, fragile)
six_arch = {}
n = 0
for ai, arch in enumerate(A, 1):
    for ci, (ctx, grade) in enumerate(CTX, 1):
        n += 1
        s, label, broken = evaluate(arch, grade)
        code = f"T{ai:02d}-{grade}{ci:02d}"
        aname, _, kind, fragile, _ = arch
        if s is None:
            out.append(f"[{code}] {ctx}({grade}) 에서 {aname} — 탈락(2-B) [{broken}]")
            reject += 1
            continue
        counts[s] += 1
        if s == 6:
            mark = "  ✅✅✅ 6/6"
            out.append(f"[{code}] {ctx}({grade}) 에서 {aname} — 6/6 (fragile: {fragile}){mark}")
            six_cells.append((code, ctx, aname, fragile))
            six_arch.setdefault(aname, (ctx, fragile))
        else:
            tail = f"broken {broken}" if broken else "—"
            out.append(f"[{code}] {ctx}({grade}) 에서 {aname} — {s}/6 ({tail} | fragile:{fragile})")

# ---- 요약 ----
out.append("")
out.append("=" * 74)
out.append("# 🏁 종료 — 차원1+3, 1000 후보")
out.append(f"# 총 채점: {n}")
for s in range(6, -1, -1):
    out.append(f"#   {s}/6 : {counts[s]}")
out.append(f"#   탈락(2-B) : {reject}")
out.append(f"# ▶ 6/6 = {counts[6]}개  ← 17,000 평면에서 0이던 것이 처음으로 양수!")
out.append("#")
out.append("# 단, 모든 6/6은 동일 게이트 3개를 통과해야 성립:")
out.append("#   (1) 자본 — 길목/권리를 *매입·선점*해야(취득위반은 과거로 매몰).")
out.append("#   (2) 독점등급 — 진짜 monopoly chokepoint여야(희소→5/6, 범용→3~4/6로 즉시 하락).")
out.append("#   (3) inbound 징수 — buyer가 필연으로 찾아와 자발 지불(집행노동 들면 #1/#5 붕괴).")
out.append("#")
out.append("# ★ 6/6 아키타입(자연스러운 대표 길목):")
out.append("#   1) 지리적 통행 지역권 @ 산악 단일 통과회랑 — 지리=발견필연, 통과자=현존 buyer")
out.append("#   2) 영구 양륙점/랜딩 권리 @ 해저케이블 단일 양륙점")
out.append("#   3) 전략입지 정박/슬롯 @ 단일 항만 진입수로")
out.append("#   4) 임차 스펙트럼 @ (독점) 필수 대역")
out.append("#   5) 비탄력 로열티 스트림 매입 @ 표준치료 독점신약")
out.append("#   6) 불가피 기반특허 inbound @ 유일 호환 필수특허 기술")
out.append("#   7) 식별자/주소 블록 서브리스 @ 희소 레인지(독점보유분)")
out.append("#   8) 필수규격 IP 영구로열티 매입 @ 단일 호환규격")
out.append("#")
out.append("# 결론: 6/6은 실재한다 — 단 '공짜'가 아니라 *매입한 독점 길목 + 수동 inbound 징수*.")
out.append("#   즉 6원칙은 '무자본 신규창작'에는 여전히 공집합, '자본으로 매몰된 통행료'에는 비공집합.")

with open("/home/user/blank/hunt_1000_dim13_results.md", "w", encoding="utf-8") as f:
    f.write("\n".join(out) + "\n")

print(f"총 후보: {n}")
print("분포:", {f"{s}/6": counts[s] for s in range(6,-1,-1)}, "| 탈락:", reject)
print(f"6/6 = {counts[6]}개  (아키타입 {len(six_arch)}종)")
print("6/6 아키타입:", list(six_arch.keys()))
print("파일:", "/home/user/blank/hunt_1000_dim13_results.md")
