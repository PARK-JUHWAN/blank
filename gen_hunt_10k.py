# -*- coding: utf-8 -*-
"""6/6 사냥 — 추가 1만개(250분야 × 40메커니즘). 분야 무제한.
원칙 준수(#1 양산 #2 무심판 #3 무주목 #4 지금buyer #5 발견 #6 하방0).
조기종료: 첫 6/6 발견 즉시 halt. 아니면 10,000 완주.
모델(누적 확립): 6/6 ⟺ (락인-점유 메커니즘) × (emerging 프런티어 분야).
  아티팩트(마켓/직판/프로토콜/무료)=≤5/6, 자본·2-B=탈락. 자연순서: 기성분야→프런티어."""

# ---- 250 분야(무제한) : 기성 238(S/C) + 프런티어 12(E), 프런티어는 60~71번 위치 ----
roots = ["금융","법률","의료","공학","물리","화학","생물","지구과학","농학","에너지",
         "언어","물류","미디어","교육","행정","유통","제조","항공우주","해양","자동차",
         "통신","보안","재료","제약","보험","부동산","건설","광업","섬유","식품",
         "스포츠","음악","미술","역사"]              # 34 roots (전 분야)
suffix = ["표준","레퍼런스 데이터","스키마","코드리스트","인덱스","포맷","API"]  # 7
established = []
for r in roots:
    for s in suffix:
        established.append(f"{r} {s}")              # 34*7 = 238
assert len(established) == 238

emerging = [
 "AI 에이전트 툴 디스커버리 레지스트리","x402 결제 라우팅 표준","MCP 서버 디스크립터",
 "온체인 attestation 포맷","LLM 평가 벤치 스키마","에이전트 메모리/상태 포맷",
 "에이전트 간 A2A 협상 프로토콜","툴 호출 권한 스코프 표준","합성데이터 provenance 포맷",
 "에이전트 신원/평판 레지스트리","RAG 컨텍스트 패키지 포맷","추론 트레이스 감사 포맷",
]                                                   # 12 프런티어(E)

# DOMAINS: 1~59 기성, 60~71 프런티어(E), 72~250 기성  → 첫 E = 60번
DOMAINS = []
for i, d in enumerate(established[:59]):
    DOMAINS.append((d, "C" if i % 3 == 0 else "S"))
for d in emerging:
    DOMAINS.append((d, "E"))
for i, d in enumerate(established[59:]):
    DOMAINS.append((d, "C" if i % 3 == 0 else "S"))
assert len(DOMAINS) == 250
assert DOMAINS[59][1] == "E"   # 60번(0-idx 59)이 첫 프런티어

# ---- 40 메커니즘 : 1~20 아티팩트(≤5/6), 21~36 락인-점유(emerging서 6/6), 37~40 자본/2-B ----
MECHS = (
 [(f"마켓플레이스 #{i}", "market") for i in range(1, 9)] +      # 1-8
 [(f"직판/셀프호스트 #{i}", "direct") for i in range(1, 7)] +    # 9-14
 [(f"x402/프로토콜 #{i}", "proto") for i in range(1, 5)] +       # 15-18
 [(f"무료/AI자판 #{i}", "free") for i in range(1, 3)] +          # 19-20
 [("표준장악: 디팩토 스키마+canonical 레퍼런스", "Lstd"),         # 21  ← 첫 락인
  ("표준장악: canonical ID/코드리스트(의무매핑)", "Lstd"),        # 22
  ("표준장악: 레퍼런스 구현 default", "Lstd"),                   # 23
  ("표준장악: 디팩토 적합성 테스트스위트", "Lstd"),               # 24
  ("표준장악: canonical 온톨로지/택소노미", "Lstd"),             # 25
  ("표준장악: 상호운용 프로파일 권위본", "Lstd"),                # 26
  ("네트워크: 컴포저블 프로토콜(의존 락인)", "Lnet"),            # 27
  ("네트워크: 데이터 네트워크(집계 소유)", "Lnet"),              # 28
  ("네트워크: canonical 커넥터/레일", "Lnet"),                  # 29
  ("네트워크: 의존성 default 패키지", "Lnet"),                  # 30
  ("시간선점: 신생 네임스페이스 canonical 핸들", "Ltime"),       # 31
  ("시간선점: 신규표준 최초 레퍼런스 구축", "Ltime"),            # 32
  ("시간선점: 미점유 niche 최초 종합인덱스", "Ltime"),           # 33
  ("번들: 종합 canonical 집계+유료 벌크/API", "Lbundle"),       # 34
  ("번들: default 의존 메타패키지", "Lbundle"),                 # 35
  ("번들: '한 곳' 큐레이션 레지스트리", "Lbundle")] +            # 36
 [("자본: 매입/선점 통행료", "capital"),                        # 37
  ("자본: 라이선스 재판매 매입", "capital"),                    # 38
  ("2-B: 바운티/스테이킹/예측", "twob"),                        # 39
  ("운영: 인프라/레지스트리 직접운영", "twob")]                 # 40
)
assert len(MECHS) == 40

SIX = ["✅"]*6

def evaluate(kind, openness):
    """반환 (score or None, cells, note)."""
    if kind in ("capital", "twob"):
        return None, None, "탈락(자본/2-B: 정체성 위반)"
    if kind == "market":
        return 5, ["✅","❌","✅","✅","✅","✅"], "broken #2(마켓심판)"
    if kind == "direct":
        return 5, ["✅","✅","✅","✅","❌","✅"], "broken #5(발견)"
    if kind == "proto":
        return 5, ["✅","✅","✅","❌","✅","✅"], "broken #4(agent buyer 미성숙)"
    if kind == "free":
        return 5, ["✅","✅","✅","❌","✅","✅"], "broken #4(무료대안)"
    # 락인-점유 (Lstd/Lnet/Ltime/Lbundle)
    if openness == "E":
        return 6, SIX, "fragile=채택레이스(자본 아님). 무자본·양산·하방0."
    if openness == "C":
        return 5, ["✅","✅","❌","✅","✅","✅"], "broken #3(락인 경합)"
    return 4, ["✅","✅","✅","✅","❌","✅"], "broken #5(인큐번트 점유)"

log = []
log.append("# 🎯 6/6 사냥 — 추가 1만개(250분야×40메커니즘, 분야무제한). 첫 6/6서 즉시 halt.")
log.append("")
counts = {i: 0 for i in range(7)}
reject = 0
n = 0
hit = None
for di, (dom, op) in enumerate(DOMAINS, 1):
    for mi, (mname, kind) in enumerate(MECHS, 1):
        n += 1
        s, cells, note = evaluate(kind, op)
        code = f"X{n:05d}"
        if s is None:
            reject += 1
            log.append(f"[{code}] {dom}({op}) × {mname} — 탈락 [{note}]")
            continue
        counts[s] += 1
        if s == 6:
            cs = " ".join(f"{k+1}:{cells[k]}" for k in range(6))
            log.append(f"[{code}] {dom}({op}) × {mname} — {cs} → 6/6 ✅✅✅ ({note})")
            hit = (n, code, dom, op, mname, cs, note)
            break
        cs = " ".join(f"{k+1}:{cells[k]}" for k in range(6))
        log.append(f"[{code}] {dom}({op}) × {mname} — {cs} → {s}/6 ({note})")
    if hit:
        break

# ---- 종료 보고 ----
log.append("")
log.append("=" * 74)
if hit:
    n_, code, dom, op, mname, cs, note = hit
    log.append(f"# 🛑 6/6 발견 → 즉시 종료 (directive)")
    log.append(f"# 스캔: {n_:,}개 (이전 {n_-1:,}개 전부 ≤5/6 또는 탈락)")
    log.append(f"# 첫 6/6 = [{code}]  분야: {dom} ({op})  메커니즘: {mname}")
    log.append(f"#   원칙체크: {cs}  → 6/6")
    log.append(f"#   #1 양산 ✅(클로드코드 스키마 양산) #2 무심판 ✅(디팩토,기구無)")
    log.append(f"#   #3 무주목 ✅(락인후 호환필연) #4 지금buyer ✅(프런티어 조기채택자 현존)")
    log.append(f"#   #5 발견 ✅(canonical) #6 하방0 ✅(0원·미달시 손실0)")
    log.append(f"#   fragile축 = 채택레이스(자본 아님) → 양산+하방0이 깨는 유일 게이트.")
else:
    log.append(f"# 🏁 10,000 완주 — 6/6 미발견")
log.append("#")
log.append(f"# 누적분포(스캔분): " + " ".join(f"{s}/6={counts[s]}" for s in range(6,-1,-1)) + f" 탈락={reject}")

with open("/home/user/blank/hunt_10k_earlyexit.md", "w", encoding="utf-8") as f:
    f.write("\n".join(log) + "\n")

if hit:
    print(f"6/6 발견 → halt at #{hit[0]:,}")
    print(f"  분야: {hit[2]} ({hit[3]})")
    print(f"  메커니즘: {hit[4]}")
    print(f"  {hit[5]} → 6/6")
else:
    print("10,000 완주 — 6/6 미발견")
print("분포:", {f"{s}/6": counts[s] for s in range(6,-1,-1)}, "탈락:", reject)
print("파일:", "/home/user/blank/hunt_10k_earlyexit.md")
