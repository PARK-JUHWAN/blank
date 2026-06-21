# -*- coding: utf-8 -*-
"""6/6 사냥 RAW 5000 — 배치3: 2차(조합) 탐색.
질문: 두 메커니즘을 겹치면 '버려진 축'이 치유되어 6/6이 되는가?
합성규칙(정직): 한 buyer는 한 경로만 탄다. 따라서 hybrid 점수 = max(경로별 점수).
  - 마켓경로로 온 buyer = 발견됨(#5) 그러나 심판대상(#2).
  - 직판경로 buyer = 무심판(#2) 그러나 미발견(#5).
  - 같은 거래에서 둘을 동시에 못 가짐(buyer-path 결합) → 경로합산 불가.
정리: hybrid ≤ max(구성요소) ≤ 5/6  ⇒  6/6 = 0 (단일이 전부 ≤5/6이므로 자명)."""

import itertools

# base 메커니즘: (이름, 점수, 클러스터, 깨진축, 별)
# 클러스터: EST(마켓:심판#2), ESTD(직판:발견#5), ADS(광고:주목#3),
#           PROTO(프로토콜:타이밍#4), FREE(무료:buyer영구부재#4), OP(운영), TWOB(2-B 탈락)
N = None
base = [
 ("Gumroad 일회판매",5,"EST","2",""),("Etsy 디지털",5,"EST","2",""),("Unity 에셋",5,"EST","2",""),
 ("앱스토어 앱",4,"EST","2,5",""),("Shutterstock",4,"EST","2,3",""),("Spotify",4,"EST","2,3",""),
 ("RapidAPI",3,"EST","2,5,6",""),("광고무료배포",4,"ADS","3,4",""),("제휴/레퍼럴",4,"ADS","3,4",""),
 ("NFT 1차",4,"EST","2,3",""),("NFT 2차로열티",3,"EST","2,3,4",""),("Substack",3,"EST","2,3,5",""),
 ("POD 로열티",4,"EST","2,3",""),("드롭십",3,"EST","2,3,5",""),("자체사이트 일회",5,"ESTD","5",""),
 ("자체사이트 구독",5,"ESTD","5",""),("셀프호스트 API",4,"ESTD","5,6",""),("유료뉴스레터",4,"ESTD","3,5",""),
 ("B2B 직접라이선스",5,"ESTD","5",""),("데이터브로커",3,"ESTD","4,5",""),("임베드SDK",4,"ESTD","4,5",""),
 ("단일buyer 인제스트",5,"ESTD","5",""),("기부/팁",4,"ADS","3,4",""),("스폰서십",3,"ADS","3,4,5",""),
 ("x402 세무계산",5,"PROTO","4","★"),("x402 제재스크리닝",5,"PROTO","4","★★"),
 ("x402 통관HS분류",5,"PROTO","4","★★"),("x402 의료청구검증",5,"PROTO","4","★★"),
 ("x402 AML검증",5,"PROTO","4","★★"),("x402 GD&T검증",5,"PROTO","4","★"),
 ("x402 범용계산",5,"FREE","4",""),("L402 게이트",5,"PROTO","4","★"),("MCP+x402",5,"PROTO","4","★"),
 ("온체인 attestation",5,"PROTO","4","★"),("유료패키지레지",5,"PROTO","4","★"),
 ("무제한매입 컨트랙트",N,"TWOB","2-B",""),("공공DB 재포장",5,"FREE","4",""),
 ("OSS 파생배포",5,"FREE","4",""),("AI자판 변환",5,"FREE","4",""),("오라클 운영",N,"TWOB","2-B",""),
 ("인덱서/키퍼",3,"OP","5,6",""),("스토리지 제공",3,"OP","5,6",""),("컴퓨트 제공",3,"OP","5,6",""),
 ("인증/감사 발급",N,"TWOB","2-B",""),("PRO 로열티",4,"EST","2,3",""),("SEP 특허풀",4,"EST","2,4",""),
 ("CNC 온디맨드",3,"EST","2,5,6",""),("키오스크 공급",4,"OP","5,6",""),("SaaS 운영",4,"OP","5,6",""),
 ("바운티 응모",N,"TWOB","2-B",""),
 # --- 배치2 신규 50 ---
 ("ISO/IEC 표준내장",5,"EST","2",""),("규제 코드리스트",5,"EST","2",""),("SEP 자동라이선스",4,"EST","2,4",""),
 ("적합성 인증마크",N,"TWOB","2-B",""),("약전/표준물질 등재",5,"EST","2",""),("측정표준 소급성",N,"TWOB","2-B",""),
 ("의학용어체계",5,"EST","2",""),("회계기준 코드",5,"EST","2",""),("펌웨어 ROM 로열티",5,"ESTD","5",""),
 ("OS 기본탑재 사전",5,"ESTD","5",""),("브라우저 기본데이터",5,"FREE","4",""),("OSS de facto 데이터",5,"FREE","4",""),
 ("Dolby식 단위로열티",5,"ESTD","5",""),("코덱 표준풀",4,"EST","2,5",""),("폰트 OEM 번들",5,"ESTD","5",""),
 ("지도/POI 기본탑재",4,"OP","5,6",""),("엔진 SDK 데이터",5,"ESTD","5",""),("ENS 네임스페이스",N,"TWOB","2-B",""),
 ("온체인 서브네임",4,"EST","3,4",""),("토큰게이트 멤버십",3,"EST","3,5",""),("DePIN 자원제공",N,"TWOB","2-B",""),
 ("RWA 토큰화 배당",4,"OP","5,6",""),("EIP-2981 로열티",3,"EST","2,3,4",""),
 ("x402 단위변환",5,"PROTO","4","★"),("x402 좌표변환",5,"PROTO","4","★"),("x402 분자량",5,"PROTO","4","★"),
 ("x402 의약품상호작용",5,"PROTO","4","★★"),("x402 식품알레르겐",5,"PROTO","4","★★"),
 ("x402 위험물UN",5,"PROTO","4","★★"),("x402 원산지관세",5,"PROTO","4","★★"),("x402 공차조회",5,"PROTO","4","★"),
 ("x402 규정한계치",5,"PROTO","4","★"),("x402 서명검증",5,"PROTO","4","★"),("x402 결정론시뮬",5,"PROTO","4","★"),
 ("L402 라이트닝",5,"PROTO","4","★"),("MCP 리소스결제",5,"PROTO","4","★"),("A2A 데이터판매",5,"PROTO","4","★"),
 ("에이전트 툴레지",5,"PROTO","4","★"),("데이터 DAO",N,"TWOB","2-B",""),("큐레이션마켓",N,"TWOB","2-B",""),
 ("검증자 스테이킹",N,"TWOB","2-B",""),("예측시장 판매",N,"TWOB","2-B",""),("듀얼라이선스",5,"ESTD","5",""),
 ("특허 NPE",3,"ESTD","4,5,6",""),("영업비밀 라이선스",4,"ESTD","4,5",""),("RAND 라이선스",4,"EST","2,5",""),
 ("콘텐츠 신디케이션",4,"EST","2,5",""),("데이터 협동조합",N,"TWOB","2-B",""),("메타데이터 매핑",3,"FREE","4,5",""),
 ("임베디드 광고SDK",3,"EST","3,5",""),
 ("x402 보험계리 영수증",5,"PROTO","4","★"),  # 101번째
]
assert len(base) == 101, len(base)

EST_LIKE = {"EST", "ESTD", "ADS"}

def hyb(a, b):
    """두 메커니즘 합성. 반환: (점수 or None=탈락, 라벨, naive6 여부)"""
    (na, sa, ca, ba, _), (nb, sb, cb, bb, _) = a, b
    if ca == "TWOB" and cb == "TWOB":
        return None, "탈락(2-B×2)", False
    # TWOB는 죽은 무게(점수 기여 0). 나머지 중 best 경로 채택.
    cand = [(sa, ca, ba), (sb, cb, bb)]
    cand = [c for c in cand if c[0] is not None]
    best = max(cand, key=lambda c: c[0])
    score, cl, br = best
    # 순진한 6/6 후보: PROTO(5) × EST계열(5) — 합치면 6일 것 같은 쌍
    pair_cl = {ca, cb}
    naive6 = (("PROTO" in pair_cl and pair_cl & EST_LIKE) and sa == 5 and sb == 5
              and None not in (sa, sb))
    if naive6:
        note = (f"{score}/6 — ※경로합산 불가: 발견·성숙 buyer=심판/주목, "
                f"무심판 buyer=미성숙 (buyer-path 결합) → 치유 X")
    else:
        note = f"{score}/6 (best경로 broken {br})"
    return score, note, bool(naive6)

out = []
out.append("# 🎯 6/6 사냥 — RAW 5000 배치3: 2차(조합) 탐색")
out.append("# 질문: 두 메커니즘을 겹치면 깨진 축이 치유되어 6/6이 되는가?")
out.append("# 합성규칙: 한 buyer=한 경로 → hybrid 점수 = max(경로 점수). 경로 간 합산 불가.")
out.append("# 형식: [코드] A  ⊕  B — 합성 → n/6 [주석]")
out.append("")

counts = {i: 0 for i in range(7)}
reject = 0
naive6_total = 0
naive6_still5 = 0
n = 0
for A, B in itertools.combinations(base, 2):
    if n >= 5000:
        break
    n += 1
    s, note, naive6 = hyb(A, B)
    code = f"H{n:04d}"
    line = f"[{code}] {A[0]}  ⊕  {B[0]} — {note}"
    out.append(line)
    if s is None:
        reject += 1
    else:
        counts[s] += 1
    if naive6:
        naive6_total += 1
        if s == 5:
            naive6_still5 += 1

out.append("")
out.append("=" * 72)
out.append("# 🏁 종료 — 배치3 (2차 조합 5000쌍 소진)")
out.append(f"# 총 조합: {n}쌍")
for s in range(6, -1, -1):
    out.append(f"#   {s}/6 : {counts[s]}쌍")
out.append(f"#   탈락(2-B×2) : {reject}쌍")
out.append(f"# ▶ 6/6 = {counts[6]}쌍.  최고점 = 5/6.")
out.append("#")
out.append(f"# 순진한 '마켓+프로토콜=6/6' 후보(PROTO5 × EST계열5): {naive6_total}쌍")
out.append(f"#   → 그중 6/6 달성: {naive6_total - naive6_still5}쌍.  여전히 5/6: {naive6_still5}쌍.")
out.append("#")
out.append("# 합성 정리(2차): hybrid 점수 = max(구성요소) ≤ 5/6.")
out.append("#   단일이 전부 ≤5/6이므로 어떤 2-조합도 6/6 불가. buyer-path 결합이")
out.append("#   '발견·성숙'과 '무심판'을 같은 거래에서 양립 못하게 함 = osk의 벽은 합성 불변.")
out.append("#   (귀납: k-조합도 max라 동일 → n중 어떤 부분집합도 6/6 불가.)")

with open("/home/user/blank/hunt_5000_results_batch3.md", "w", encoding="utf-8") as f:
    f.write("\n".join(out) + "\n")

print(f"생성 조합(배치3): {n}")
print("분포:", {f"{s}/6": counts[s] for s in range(6, -1, -1)}, "| 탈락:", reject)
print("6/6:", counts[6])
print(f"순진한 6/6후보: {naive6_total}쌍 → 6/6달성 {naive6_total - naive6_still5}, 여전히5/6 {naive6_still5}")
print("파일:", "/home/user/blank/hunt_5000_results_batch3.md")
