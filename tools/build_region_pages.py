"""지역 페이지(27개)와 주제 페이지(학년별·동네별·온라인)를 정적 HTML로 생성합니다.

검색 로봇이 자바스크립트를 실행하지 않아도 본문을 읽을 수 있도록
모든 내용을 HTML에 직접 넣습니다. 지역 정보나 문구를 바꾼 뒤에는
저장소 루트에서 아래 명령으로 다시 생성하세요.

    python tools/build_region_pages.py
"""

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://tutorlink.kr"
PHONE = "010-2928-3614"
TEL = "01029283614"
BRAND = "전남광주 수학과외"
TODAY = date.today().isoformat()

# slug, 정식 명칭, 검색용 짧은 이름, 시도, 대표 동네, 구분, 인근 지역
REGIONS = [
    ("gwangju-dong-gu", "광주 동구", "광주 동구", "광주", ["계림동", "산수동", "학동", "지원동"], "gu", ["gwangju-nam-gu", "gwangju-buk-gu", "gwangju-seo-gu", "hwasun-gun"]),
    ("gwangju-seo-gu", "광주 서구", "광주 서구", "광주", ["상무동", "화정동", "금호동", "풍암동"], "gu", ["gwangju-nam-gu", "gwangju-gwangsan-gu", "gwangju-buk-gu", "gwangju-dong-gu"]),
    ("gwangju-nam-gu", "광주 남구", "광주 남구", "광주", ["봉선동", "진월동", "주월동", "효천지구"], "gu", ["gwangju-seo-gu", "gwangju-dong-gu", "gwangju-gwangsan-gu", "naju-si", "hwasun-gun"]),
    ("gwangju-buk-gu", "광주 북구", "광주 북구", "광주", ["일곡동", "문흥동", "운암동", "첨단2지구"], "gu", ["gwangju-gwangsan-gu", "gwangju-dong-gu", "gwangju-seo-gu", "damyang-gun", "jangseong-gun"]),
    ("gwangju-gwangsan-gu", "광주 광산구", "광주 광산구", "광주", ["수완동", "첨단동", "신창동", "운남동"], "gu", ["gwangju-buk-gu", "gwangju-seo-gu", "gwangju-nam-gu", "naju-si", "jangseong-gun", "hampyeong-gun"]),
    ("mokpo-si", "목포시", "목포", "전남", ["옥암동", "상동", "하당동", "용해동"], "si", ["muan-gun", "sinan-gun", "yeongam-gun"]),
    ("yeosu-si", "여수시", "여수", "전남", ["웅천동", "여서동", "문수동", "학동"], "si", ["suncheon-si", "gwangyang-si", "goheung-gun"]),
    ("suncheon-si", "순천시", "순천", "전남", ["신대지구", "조례동", "연향동", "오천동"], "si", ["yeosu-si", "gwangyang-si", "boseong-gun", "gurye-gun", "gokseong-gun", "goheung-gun"]),
    ("naju-si", "나주시", "나주", "전남", ["빛가람동", "남평읍", "송월동", "성북동"], "si", ["gwangju-nam-gu", "gwangju-gwangsan-gu", "hwasun-gun", "yeongam-gun", "muan-gun", "hampyeong-gun"]),
    ("gwangyang-si", "광양시", "광양", "전남", ["중마동", "광양읍", "금호동", "마동"], "si", ["suncheon-si", "yeosu-si", "gurye-gun"]),
    ("damyang-gun", "담양군", "담양", "전남", ["담양읍", "수북면", "창평면", "대전면"], "gun", ["gwangju-buk-gu", "jangseong-gun", "gokseong-gun", "hwasun-gun"]),
    ("gokseong-gun", "곡성군", "곡성", "전남", ["곡성읍", "옥과면", "석곡면", "입면"], "gun", ["damyang-gun", "gurye-gun", "suncheon-si", "hwasun-gun"]),
    ("gurye-gun", "구례군", "구례", "전남", ["구례읍", "산동면", "마산면", "토지면"], "gun", ["gokseong-gun", "suncheon-si", "gwangyang-si"]),
    ("goheung-gun", "고흥군", "고흥", "전남", ["고흥읍", "도양읍", "과역면", "도화면"], "gun", ["boseong-gun", "suncheon-si", "yeosu-si"]),
    ("boseong-gun", "보성군", "보성", "전남", ["보성읍", "벌교읍", "조성면", "득량면"], "gun", ["suncheon-si", "goheung-gun", "hwasun-gun", "jangheung-gun"]),
    ("hwasun-gun", "화순군", "화순", "전남", ["화순읍", "능주면", "도곡면", "동면"], "gun", ["gwangju-dong-gu", "gwangju-nam-gu", "naju-si", "damyang-gun", "boseong-gun", "jangheung-gun"]),
    ("jangheung-gun", "장흥군", "장흥", "전남", ["장흥읍", "관산읍", "대덕읍", "부산면"], "gun", ["boseong-gun", "gangjin-gun", "yeongam-gun", "hwasun-gun"]),
    ("gangjin-gun", "강진군", "강진", "전남", ["강진읍", "군동면", "성전면", "마량면"], "gun", ["jangheung-gun", "haenam-gun", "yeongam-gun", "wando-gun"]),
    ("haenam-gun", "해남군", "해남", "전남", ["해남읍", "송지면", "문내면", "황산면"], "gun", ["gangjin-gun", "yeongam-gun", "jindo-gun", "wando-gun"]),
    ("yeongam-gun", "영암군", "영암", "전남", ["영암읍", "삼호읍", "신북면", "학산면"], "gun", ["mokpo-si", "naju-si", "muan-gun", "gangjin-gun", "haenam-gun"]),
    ("muan-gun", "무안군", "무안", "전남", ["삼향읍", "무안읍", "일로읍", "청계면"], "gun", ["mokpo-si", "sinan-gun", "yeongam-gun", "naju-si", "hampyeong-gun"]),
    ("hampyeong-gun", "함평군", "함평", "전남", ["함평읍", "학교면", "월야면", "해보면"], "gun", ["muan-gun", "yeonggwang-gun", "jangseong-gun", "naju-si", "gwangju-gwangsan-gu"]),
    ("yeonggwang-gun", "영광군", "영광", "전남", ["영광읍", "홍농읍", "법성면", "백수읍"], "gun", ["hampyeong-gun", "jangseong-gun"]),
    ("jangseong-gun", "장성군", "장성", "전남", ["장성읍", "삼계면", "황룡면", "진원면"], "gun", ["gwangju-buk-gu", "gwangju-gwangsan-gu", "damyang-gun", "yeonggwang-gun", "hampyeong-gun"]),
    ("wando-gun", "완도군", "완도", "전남", ["완도읍", "노화읍", "금일읍", "군외면"], "gun", ["haenam-gun", "gangjin-gun"]),
    ("jindo-gun", "진도군", "진도", "전남", ["진도읍", "군내면", "고군면", "임회면"], "gun", ["haenam-gun"]),
    ("sinan-gun", "신안군", "신안", "전남", ["압해읍", "지도읍", "비금면", "도초면"], "gun", ["mokpo-si", "muan-gun"]),
]
BY_SLUG = {r[0]: r for r in REGIONS}

# 시·군·구 특성에 따라 소개 문장을 다르게 씁니다.
INTRO = {
    "gu": "{name}는 학교와 학원이 가까이 모여 있어 비교할 수업이 많은 지역입니다. 그래서 더더욱 학생 한 명의 수준과 목표에 맞춘 1:1 수학과외가 필요합니다. {areas} 등 {name} 전 지역에서 방문 수업과 온라인 수업을 모두 안내합니다.",
    "si": "{short}는 동네마다 학교 진도와 시험 범위가 조금씩 다릅니다. {areas} 등 {short} 지역 학생의 학교 일정과 현재 실력을 먼저 확인하고, 그 학생에게 맞는 순서로 수학 공부를 설계합니다.",
    "gun": "{short}처럼 학원 선택지가 많지 않은 지역일수록 1:1 수학과외의 효과가 큽니다. {areas} 등 {short} 지역은 방문 수업과 실시간 온라인 수업을 함께 활용해 이동 부담 없이 꾸준히 수업할 수 있도록 안내합니다.",
}

ICON = '<i data-lucide="{0}" aria-hidden="true"></i>'


def esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def faqs(name, short, areas):
    return [
        (f"{short} 초등학생도 수학과외를 받을 수 있나요?",
         f"네. {short} 초등 수학과외는 연산과 기초수학부터 교과 진도, 서술형 문제까지 학생의 학년과 수준에 맞춰 진행합니다. 초등 저학년은 수학공부 습관을, 고학년은 중등 수학을 준비하는 데 초점을 둡니다."),
        (f"{short} 중등 수학내신 대비는 어떻게 하나요?",
         f"다니는 학교의 진도와 시험 범위, 기출 유형을 확인한 뒤 개념 정리, 유형 연습, 서술형 대비 순서로 수업합니다. 기초가 부족하면 이전 학년 기초수학부터 함께 보완합니다."),
        (f"{short} 고등 수능수학 대비도 가능한가요?",
         f"가능합니다. 고등 수학내신과 수능대비를 학생의 목표에 맞게 나눠 계획하고, 수능수학은 개념 복습과 기출 분석, 실전 풀이 연습까지 단계적으로 진행합니다."),
        (f"{areas[0]}, {areas[1]} 쪽도 방문 수업이 되나요?",
         f"{', '.join(areas)} 등 {name} 대부분 지역에서 방문 수업을 안내하고 있습니다. 방문이 어려운 경우 실시간 온라인 수업으로도 같은 1:1 관리를 받을 수 있습니다."),
        ("수업료와 무료체험수업은 어떻게 되나요?",
         "수업료는 학년, 수업 횟수, 방식에 따라 달라지며 전화 상담에서 투명하게 안내합니다. 상담은 무료이고, 무료체험수업으로 수업이 학생에게 맞는지 먼저 확인할 수 있습니다."),
    ]


def build(region):
    slug, name, short, province, areas, kind, neighbors = region
    url = f"{SITE}/{slug}.html"
    areas_text = ", ".join(areas)
    intro = INTRO[kind].format(name=name, short=short, areas=areas_text)
    title = f"{short} 수학과외 | 초등·중등·고등 1:1 수학 무료체험 - {BRAND}"
    description = (f"{short} 수학과외, 초등 기초수학부터 중등 수학내신, 고등 수능수학까지 1:1 맞춤 수업. "
                   f"{areas[0]}·{areas[1]} 방문·온라인 가능, 무료 상담 {PHONE}.")
    faq_items = faqs(name, short, areas)

    grade_levels = [
        ("초등 저학년", "초1·초2·초3", f"{short} 초등 저학년 수학과외는 수 감각과 연산, 수학공부 습관을 만드는 데 집중합니다."),
        ("초등 고학년", "초4·초5·초6", f"분수, 도형, 서술형을 정리하고 중학교 수학으로 자연스럽게 넘어갈 기초수학을 다집니다."),
        ("중1 수학과외", "중학교 1학년", "처음 치르는 중등 수학 시험에 맞춰 개념 이해와 풀이 습관을 잡습니다."),
        ("중2 수학과외", "중학교 2학년", "함수와 도형 단원을 중심으로 중등 수학내신 점수를 안정적으로 끌어올립니다."),
        ("중3 수학과외", "중학교 3학년", "중등 과정을 마무리하며 고등 수학 기초와 선행을 학생 속도에 맞춰 준비합니다."),
        ("고1 수학과외", "고등학교 1학년", "고등 수학내신의 첫 시험부터 개념과 유형을 빈틈없이 정리합니다."),
        ("고2 수학과외", "고등학교 2학년", "선택 과목 내신과 함께 수능대비를 위한 기본기를 쌓습니다."),
        ("고3 수학과외", "고등학교 3학년", "수능수학 기출 분석과 실전 연습으로 목표 등급을 준비합니다."),
    ]

    neighbor_links = "".join(
        f'<a href="{s}.html">{place} 수학과외</a>' for s, (place, owner) in NEIGHBORHOODS.items() if owner == slug
    ) + "".join(
        f'<a href="{n}.html">{BY_SLUG[n][2]} 수학과외</a>' for n in neighbors
    )
    hub_links = "".join(f'<a href="{s}.html">{t}</a>' for s, t in HUBS)

    jsonld = [
        {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": f"{short} 수학과외",
            "serviceType": "수학과외",
            "description": description,
            "url": url,
            "provider": {"@type": "EducationalOrganization", "@id": f"{SITE}/#organization", "name": BRAND, "telephone": PHONE, "url": f"{SITE}/"},
            "areaServed": {"@type": "AdministrativeArea", "name": name},
            "audience": {"@type": "EducationalAudience", "educationalRole": "student"},
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": BRAND, "item": f"{SITE}/"},
                {"@type": "ListItem", "position": 2, "name": f"{short} 수학과외", "item": url},
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in faq_items
            ],
        },
    ]
    jsonld_html = "\n".join(
        f'  <script type="application/ld+json">{json.dumps(item, ensure_ascii=False)}</script>' for item in jsonld
    )

    faq_html = "\n".join(
        f'          <details><summary>{esc(q)}{ICON.format("plus")}</summary><p>{esc(a)}</p></details>'
        for q, a in faq_items
    )
    grade_html = "\n".join(
        f'          <li><h3>{short} {label}</h3><small>{sub}</small><p>{text}</p></li>'
        for label, sub, text in grade_levels
    )

    return f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{BRAND}">
  <meta property="og:locale" content="ko_KR">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/og-image.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#173f32">
  <link rel="icon" href="logo.svg" type="image/svg+xml">
  <link rel="icon" href="favicon.ico" sizes="any">
  <link rel="apple-touch-icon" href="apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@700&family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
  <link rel="stylesheet" href="region-page.css">
  <script src="https://unpkg.com/lucide@0.468.0/dist/umd/lucide.min.js" defer></script>
  <script src="region-page.js" defer></script>
{jsonld_html}
</head>
<body>
  <a class="skip-link" href="#main">본문 바로가기</a>
  <header class="site-header region-header" id="top">
    <div class="header-inner">
      <a class="brand" href="index.html" aria-label="{BRAND} 홈"><img class="brand-mark" src="logo.svg" width="40" height="40" alt=""><span><strong>{BRAND}</strong><small>광주·전남 1:1 맞춤 과외</small></span></a>
      <nav class="desktop-nav" aria-label="{name} 수학과외 메뉴">
        <a href="#elementary">초등 수학</a>
        <a href="#middle">중등 수학</a>
        <a href="#high">고등 수학</a>
        <a href="#faq">자주 묻는 질문</a>
      </nav>
      <a class="header-cta" href="tel:{TEL}" aria-label="{PHONE}로 전화 상담">{ICON.format("phone")} {PHONE}</a>
    </div>
  </header>
  <main class="region-main" id="main">
    <section class="region-hero">
      <div class="section-inner">
        <div>
          <nav class="region-breadcrumb" aria-label="현재 위치"><a href="index.html">홈</a> / <a href="index.html#area">수업 지역</a> / {name}</nav>
          <p class="section-label">{province} · {name} 1:1 MATH TUTORING</p>
          <h1>{short} 수학과외<br><em>초등·중등·고등</em><br>1:1 맞춤 수업</h1>
          <p class="region-lead">{short} 초등 기초수학부터 중등 수학내신, 고등 수능수학까지. 학생의 현재 실력과 목표에 맞춰 {areas_text} 등 {name} 전 지역에서 1:1 수업을 진행합니다.</p>
          <a class="button primary" href="tel:{TEL}">{ICON.format("phone")} 무료 상담 {PHONE}</a>
        </div>
        <aside class="region-summary" aria-label="{short} 수학과외 요약">
          <h2>{short} 수학과외 한눈에 보기</h2>
          <dl><div><dt>수업 대상</dt><dd>{name} 초등·중학생·고등학생</dd></div><div><dt>수업 내용</dt><dd>초등 기초수학 · 중등 수학내신 · 고등 수능수학</dd></div><div><dt>수업 지역</dt><dd>{areas_text} 등</dd></div><div><dt>수업 방식</dt><dd>1:1 방문 또는 온라인</dd></div><div><dt>상담·체험</dt><dd>무료 상담 · 무료체험수업</dd></div></dl>
        </aside>
      </div>
    </section>

    <section class="region-intro section">
      <div class="section-inner region-intro-grid">
        <div class="region-heading"><p class="section-label">WHY 1:1 MATH</p><h2>{short}에서 수학과외를<br>찾고 계신가요?</h2></div>
        <p>{intro}</p>
      </div>
    </section>

    <section class="region-grades section" aria-labelledby="grade-title">
      <div class="section-inner">
        <div class="region-heading"><p class="section-label">ELEMENTARY · MIDDLE · HIGH</p><h2 id="grade-title">{short} 초등·중등·고등 수학수업</h2></div>
        <div class="program-grid">
          <article class="program-card" id="elementary">
            <span class="card-number">01</span>
            {ICON.format("blocks")}
            <h3>{short} 초등 수학</h3>
            <p>{short} 초등 수학수업은 연산과 기초수학을 탄탄히 다지고, 스스로 하는 수학공부 습관을 만드는 데서 시작합니다.</p>
            <ul><li>초등 기초수학 · 연산 · 분수 · 도형</li><li>초등 수학공부 습관 만들기</li><li>교과 진도와 서술형 문제 대비</li><li>중등 수학 준비</li></ul>
          </article>
          <article class="program-card featured" id="middle">
            <span class="card-number">02</span>
            {ICON.format("school")}
            <h3>{short} 중등 수학</h3>
            <p>{short} 중등 수학수업은 학교별 시험 범위와 기출 유형에 맞춘 수학내신 대비가 중심입니다.</p>
            <ul><li>중등 수학내신 · 학교별 기출 · 서술형</li><li>중등 기초수학 빈틈 보완</li><li>시험 기간 수학공부 계획 관리</li><li>고등 수학 선행</li></ul>
          </article>
          <article class="program-card" id="high">
            <span class="card-number">03</span>
            {ICON.format("graduation-cap")}
            <h3>{short} 고등 수학</h3>
            <p>{short} 고등 수학수업은 수학내신과 수능대비를 목표에 맞게 나눠 계획하고 끝까지 관리합니다.</p>
            <ul><li>고등 수학내신 집중 관리</li><li>수능대비 · 수능수학 기출 분석</li><li>고등 기초수학 다시 잡기</li><li>목표 등급별 수학공부 전략</li></ul>
          </article>
        </div>
      </div>
    </section>

    <section class="region-levels section" aria-labelledby="level-title">
      <div class="section-inner">
        <div class="region-heading"><p class="section-label">BY GRADE</p><h2 id="level-title">{short} 학년별 수학과외</h2></div>
        <ul class="level-grid">
{grade_html}
        </ul>
      </div>
    </section>

    <section class="region-benefits section">
      <div class="section-inner">
        <div class="region-heading"><p class="section-label">PERSONALIZED MATH LESSON</p><h2>학생에게 필요한 수학 공부부터 찾습니다.</h2></div>
        <div class="benefit-grid">
          <article class="benefit-item">{ICON.format("clipboard-check")}<h3>현재 실력 진단</h3><p>개념 이해도와 문제 풀이 습관을 확인해 먼저 보완할 단원을 정합니다.</p></article>
          <article class="benefit-item">{ICON.format("book-open-check")}<h3>학교별 내신 대비</h3><p>{short} 지역 학교의 진도와 시험 일정에 맞춰 개념, 유형, 서술형 학습을 연결합니다.</p></article>
          <article class="benefit-item">{ICON.format("chart-no-axes-combined")}<h3>꾸준한 성적 관리</h3><p>수업마다 이해도를 점검하고 다음 수업 계획에 바로 반영합니다.</p></article>
        </div>
      </div>
    </section>

    <section class="trial-process section">
      <div class="section-inner trial-layout">
        <div><p class="section-label">FREE TRIAL PROCESS</p><h2>무료체험수업은 이렇게 진행됩니다.</h2></div>
        <ol class="trial-steps"><li><span>1</span><div><h3>전화 상담</h3><p>학년, 학교, 현재 고민과 원하는 수업 일정을 확인합니다.</p></div></li><li><span>2</span><div><h3>맞춤 선생님 안내</h3><p>{name} 수업 가능 여부와 학생에게 맞는 선생님을 안내합니다.</p></div></li><li><span>3</span><div><h3>무료체험수업</h3><p>직접 수업을 경험한 뒤 정규 수업 진행 여부를 결정합니다.</p></div></li></ol>
      </div>
    </section>

    <section class="faq section" id="faq" aria-labelledby="faq-title">
      <div class="section-inner faq-layout">
        <div>
          <p class="section-label">FAQ</p>
          <h2 id="faq-title">{short} 수학과외<br>자주 묻는 질문</h2>
        </div>
        <div class="accordion">
{faq_html}
        </div>
      </div>
    </section>

    <section class="contact section" id="contact">
      <div class="section-inner">
        <div class="contact-copy"><p class="section-label light">FREE TRIAL LESSON</p><h2>{short} 수학과외,<br>편하게 상담하세요.</h2><p>학생에게 필요한 수업인지 무료체험수업으로 먼저 확인할 수 있습니다.</p><a class="contact-phone" href="tel:{TEL}">{ICON.format("phone-call")}<span><small>지금 전화 상담하기</small><strong>{PHONE}</strong></span></a></div>
      </div>
    </section>

    <nav class="nearby" aria-label="인근 지역 수학과외">
      <div class="section-inner">
        <h2>{short} 인근 지역 수학과외</h2>
        <div class="region-links">{neighbor_links}<a href="index.html#area">광주·전남 전체 지역</a></div>
        <h2 class="nearby-sub">학년·방식별 수학과외</h2>
        <div class="region-links">{hub_links}</div>
      </div>
    </nav>
  </main>
  <footer class="site-footer"><div class="section-inner footer-inner"><a class="brand footer-brand" href="index.html"><img class="brand-mark" src="logo.svg" width="40" height="40" alt=""><span><strong>{BRAND}</strong><small>광주·전남 1:1 맞춤 과외</small></span></a><div class="footer-copy"><p>{name} 초등·중등·고등 수학과외 · 전화 상담 {PHONE}</p><p>© 2026 {BRAND}. All rights reserved.</p></div><a class="to-top" href="#top" aria-label="맨 위로">{ICON.format("arrow-up")}</a></div></footer>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# 주제 페이지: 학년별 안내, 학군·신도시 동네, 온라인 수업
# ---------------------------------------------------------------------------

HUBS = [
    ("gwangju-elementary-math", "초등 수학과외"),
    ("gwangju-middle-math", "중등 수학과외"),
    ("gwangju-high-math", "고등 수학과외"),
    ("online-math-tutoring", "온라인 수학과외"),
]

# 동네 페이지 slug → (동네 이름, 속한 지역 slug)
NEIGHBORHOODS = {
    "bongseon-dong-math": ("봉선동", "gwangju-nam-gu"),
    "sangmu-math": ("상무지구", "gwangju-seo-gu"),
    "suwan-math": ("수완지구", "gwangju-gwangsan-gu"),
    "cheomdan-math": ("첨단지구", "gwangju-gwangsan-gu"),
    "namak-math": ("남악신도시", "muan-gun"),
}


def region_link(slug, anchor=""):
    return (f"{slug}.html{anchor}", f"{BY_SLUG[slug][2]} 수학과외")


def grade_cards(place):
    """동네 페이지에서 쓰는 초등·중등·고등 카드."""
    return [
        ("elementary", "blocks", f"{place} 초등 수학",
         f"{place} 초등 수학수업은 연산 정확도와 기초수학 개념을 먼저 잡고, 고학년은 중등 수학으로 넘어갈 준비를 함께 합니다.",
         ["초등 기초수학 · 연산 · 도형", "서술형 문제 풀이 연습", "초등 수학공부 습관 만들기"]),
        ("middle", "school", f"{place} 중등 수학",
         f"{place} 중등 수학수업은 학교별 시험 범위와 기출 유형에 맞춘 수학내신 대비가 중심입니다.",
         ["중등 수학내신 · 서술형 대비", "중등 기초수학 빈틈 보완", "중3 고등 수학 선행"]),
        ("high", "graduation-cap", f"{place} 고등 수학",
         f"{place} 고등 수학수업은 수학내신과 수능대비를 학생의 목표 등급에 맞춰 나눠 계획합니다.",
         ["고등 수학내신 집중 관리", "수능수학 기출 분석 · 실전 연습", "고등 기초수학 다시 잡기"]),
    ]


TOPIC_PAGES = [
    {
        "slug": "gwangju-elementary-math",
        "title": "광주 초등 수학과외 | 초등 기초수학·연산·서술형 1:1 - 전남광주 수학과외",
        "description": "광주·전남 초등 수학과외. 연산과 초등 기초수학, 서술형, 고학년 중등 수학 준비까지 1:1 맞춤 수학수업. 방문·온라인 가능, 무료 상담 010-2928-3614.",
        "crumb": "초등 수학과외",
        "label": "ELEMENTARY MATH TUTORING",
        "h1": "광주·전남<br><em>초등 수학과외</em><br>기초부터 탄탄하게",
        "lead": "초등 수학은 이후 모든 수학의 바탕이 됩니다. 연산 실수, 문장제와 서술형이 어려운 이유를 먼저 찾고, 학생의 속도에 맞춰 초등 기초수학과 수학공부 습관을 함께 만듭니다.",
        "summary": [("수업 대상", "초등학교 1~6학년"), ("수업 내용", "연산 · 초등 기초수학 · 서술형 · 중등 준비"), ("수업 지역", "광주 5개 구 · 전남 22개 시·군"), ("수업 방식", "1:1 방문 또는 온라인"), ("상담", "무료 상담 · 무료체험수업")],
        "intro_h2": "초등 수학,<br>지금 다져야 하는 이유",
        "intro": [
            "초등 수학은 단원끼리 계단처럼 이어져 있습니다. 분수와 소수가 흔들리면 비와 비율이, 비율이 흔들리면 중학교 방정식과 함수가 어려워집니다. 그래서 초등 수학과외는 진도를 빨리 나가는 것보다 앞 단원의 빈틈을 찾는 데서 시작합니다.",
            "1:1 수업은 학생이 문제를 어떻게 생각하고 푸는지 바로 옆에서 볼 수 있다는 점이 가장 큰 장점입니다. 계산 실수인지, 개념을 모르는지, 문제를 끝까지 읽지 않는 습관인지를 구분해 그에 맞게 지도합니다.",
        ],
        "cards_h2": "초등 수학수업에서 다루는 것",
        "cards": [
            ("calc", "calculator", "초등 기초수학 · 연산", "수 감각과 사칙연산을 정확하고 빠르게 만드는 것이 첫 단계입니다.", ["자연수·분수·소수 연산", "연산 실수 줄이는 풀이 습관", "학년별 교과 개념 정리"]),
            ("writing", "pencil-line", "문장제 · 서술형", "문제를 읽고 식을 세우는 힘을 기르고, 풀이 과정을 글로 쓰는 연습을 합니다.", ["문장제 식 세우기", "서술형 풀이 과정 쓰기", "도형·측정 단원 이해"]),
            ("bridge", "trending-up", "중등 수학 준비", "초등 고학년은 중학교 수학으로 자연스럽게 넘어갈 수 있도록 준비합니다.", ["비와 비율 · 규칙 찾기", "음수·문자식 개념 맛보기", "예비 중1 수학 선행"]),
        ],
        "levels_h2": "학년별 초등 수학과외",
        "levels": [
            ("초1·초2 수학", "저학년", "수 세기, 덧셈·뺄셈, 구구단을 놀이처럼 익히며 수학에 대한 자신감을 만듭니다."),
            ("초3·초4 수학", "중학년", "곱셈·나눗셈과 분수 개념이 처음 나오는 시기라 기초수학 점검이 가장 중요합니다."),
            ("초5 수학", "고학년", "약수와 배수, 분수의 계산, 도형의 넓이처럼 이후 수학의 핵심 개념을 다집니다."),
            ("초6 수학", "예비 중학생", "비와 비율, 비례식을 정리하고 중학교 1학년 수학을 미리 준비합니다."),
        ],
        "faq": [
            ("초등학생은 몇 학년부터 수학과외를 시작하면 좋나요?", "정해진 시기는 없지만, 분수가 처음 나오는 3~4학년에 기초가 흔들리는 경우가 많습니다. 저학년은 연산과 학습 습관, 고학년은 중등 수학 준비를 목표로 시작하는 경우가 많습니다."),
            ("연산만 따로 수업할 수도 있나요?", "가능합니다. 다만 연산과 개념을 함께 다질 때 효과가 오래가기 때문에, 현재 학년 교과 진도와 연산 연습을 적절히 섞어 계획합니다."),
            ("학원과 1:1 초등 수학과외는 무엇이 다른가요?", "1:1 수업은 학생 한 명의 풀이 과정을 처음부터 끝까지 보면서 실수의 원인을 바로잡을 수 있습니다. 진도도 학생 속도에 맞춰 조절합니다."),
            ("초등 고학년인데 중학교 수학 선행도 하나요?", "현재 학년 개념이 탄탄하다면 예비 중1 과정을 학생 속도에 맞춰 함께 진행합니다. 기초가 부족하면 먼저 보완한 뒤 시작합니다."),
        ],
        "links_h2": "지역별 초등 수학과외",
        "links": [(f"{s}.html#elementary", f"{BY_SLUG[s][2]} 초등 수학") for s in ["gwangju-seo-gu", "gwangju-nam-gu", "gwangju-buk-gu", "gwangju-gwangsan-gu", "gwangju-dong-gu", "mokpo-si", "suncheon-si", "yeosu-si", "naju-si", "gwangyang-si"]],
    },
    {
        "slug": "gwangju-middle-math",
        "title": "광주 중등 수학과외 | 중등 수학내신·기초수학 1:1 - 전남광주 수학과외",
        "description": "광주·전남 중등 수학과외. 학교별 기출과 서술형까지 대비하는 중등 수학내신, 중등 기초수학 보완, 고등 수학 선행까지 1:1 맞춤 수업. 무료 상담 010-2928-3614.",
        "crumb": "중등 수학과외",
        "label": "MIDDLE SCHOOL MATH TUTORING",
        "h1": "광주·전남<br><em>중등 수학과외</em><br>내신부터 고등 준비까지",
        "lead": "중학교 수학은 학교마다 시험 범위와 출제 스타일이 다릅니다. 다니는 학교의 진도와 기출을 기준으로 중등 수학내신을 준비하고, 부족한 기초수학은 이전 학년까지 거슬러 올라가 보완합니다.",
        "summary": [("수업 대상", "중학교 1~3학년 · 예비 고1"), ("수업 내용", "중등 수학내신 · 기초수학 · 고등 선행"), ("수업 지역", "광주 5개 구 · 전남 22개 시·군"), ("수업 방식", "1:1 방문 또는 온라인"), ("상담", "무료 상담 · 무료체험수업")],
        "intro_h2": "중등 수학,<br>학교 시험에 맞춰야 합니다",
        "intro": [
            "같은 교과서를 써도 학교마다 시험 범위, 서술형 비중, 어려운 문제의 유형이 다릅니다. 중등 수학과외는 학생이 다니는 학교의 기출과 수행평가 일정을 먼저 확인하고, 시험 4주 전부터 개념 정리, 유형 연습, 기출 실전 순서로 준비합니다.",
            "중학교 때 문자와 식, 함수, 도형의 기초가 흔들리면 고등학교 수학에서 따라잡기가 훨씬 어려워집니다. 그래서 내신 대비와 함께 학생에게 부족한 기초수학 단원을 꾸준히 보완합니다.",
        ],
        "cards_h2": "중등 수학수업에서 다루는 것",
        "cards": [
            ("naesin", "school", "중등 수학내신", "학교별 기출 분석과 서술형 대비로 시험 점수를 안정적으로 올립니다.", ["학교 진도·시험 범위 맞춤", "기출 유형 · 서술형 대비", "시험 4주 대비 계획"]),
            ("basic", "puzzle", "중등 기초수학", "이해가 부족한 단원은 이전 학년 개념까지 돌아가 확실히 채웁니다.", ["정수·유리수·문자식", "방정식·함수 기초", "도형 개념과 증명"]),
            ("advance", "graduation-cap", "고등 수학 선행", "중등 과정이 탄탄한 학생은 속도에 맞춰 고등 수학을 준비합니다.", ["예비 고1 공통수학", "중3 겨울방학 집중 선행", "고등 내신 대비 습관"]),
        ],
        "levels_h2": "학년별 중등 수학과외",
        "levels": [
            ("중1 수학과외", "중학교 1학년", "정수와 유리수, 문자와 식을 정리하고 처음 치르는 중학교 수학 시험에 대비합니다."),
            ("중2 수학과외", "중학교 2학년", "일차함수와 도형의 성질처럼 어려워지는 단원을 중심으로 수학내신을 관리합니다."),
            ("중3 수학과외", "중학교 3학년", "이차방정식과 이차함수를 정리하고 고등 수학으로 이어지는 기초를 다집니다."),
            ("예비 고1 수학", "중3 겨울방학", "고등학교 첫 시험을 대비해 공통수학 핵심 단원을 미리 준비합니다."),
        ],
        "faq": [
            ("중등 수학내신 대비는 언제부터 시작하나요?", "평소에는 학교 진도에 맞춰 개념과 유형을 정리하고, 시험 약 4주 전부터 범위 복습과 기출 실전 연습에 집중합니다."),
            ("기초가 많이 부족한 중학생도 괜찮을까요?", "괜찮습니다. 첫 수업에서 어느 학년 어느 단원부터 빈틈이 있는지 확인하고, 현재 진도와 기초 보완을 함께 진행합니다."),
            ("고등 수학 선행은 어느 정도 하나요?", "현재 학년 내신이 안정적일 때 학생의 속도에 맞춰 진행합니다. 무리한 선행보다 고등학교 첫 시험을 잘 치를 수 있는 준비에 초점을 둡니다."),
            ("수행평가도 도와주시나요?", "수학 수행평가 일정과 주제를 확인해, 관련 개념 정리와 풀이 과정 쓰기를 수업에서 함께 준비합니다."),
        ],
        "links_h2": "지역별 중등 수학과외",
        "links": [(f"{s}.html#middle", f"{BY_SLUG[s][2]} 중등 수학") for s in ["gwangju-seo-gu", "gwangju-nam-gu", "gwangju-buk-gu", "gwangju-gwangsan-gu", "gwangju-dong-gu", "mokpo-si", "suncheon-si", "yeosu-si", "naju-si", "muan-gun"]],
    },
    {
        "slug": "gwangju-high-math",
        "title": "광주 고등 수학과외 | 고등 수학내신·수능수학 1:1 - 전남광주 수학과외",
        "description": "광주·전남 고등 수학과외. 고등 수학내신, 수능대비와 수능수학 기출 분석, 고등 기초수학까지 목표 등급에 맞춘 1:1 수업. 무료 상담 010-2928-3614.",
        "crumb": "고등 수학과외",
        "label": "HIGH SCHOOL MATH TUTORING",
        "h1": "광주·전남<br><em>고등 수학과외</em><br>내신과 수능을 함께",
        "lead": "고등학교 수학은 내신과 수능을 동시에 준비해야 합니다. 학생의 현재 등급과 목표 대학, 남은 시간을 기준으로 고등 수학내신과 수능수학의 비중을 나눠 계획합니다.",
        "summary": [("수업 대상", "고등학교 1~3학년"), ("수업 내용", "고등 수학내신 · 수능대비 · 수능수학 · 기초수학"), ("수업 지역", "광주 5개 구 · 전남 22개 시·군"), ("수업 방식", "1:1 방문 또는 온라인"), ("상담", "무료 상담 · 무료체험수업")],
        "intro_h2": "고등 수학,<br>학년마다 전략이 다릅니다",
        "intro": [
            "고1은 고등학교 첫 내신에서 흐름을 잡는 것이, 고2는 내신과 수능 기본기를 함께 쌓는 것이, 고3은 수능수학 실전력을 끌어올리는 것이 핵심입니다. 같은 고등 수학과외라도 학년과 목표에 따라 수업 구성이 완전히 달라집니다.",
            "2028학년도 수능부터 수학은 선택과목 없이 대수, 미적분Ⅰ, 확률과 통계를 공통으로 응시합니다. 현재 고3은 기존 체제로, 고2 이하는 개편된 수능 체제로 준비해야 하므로 학생 학년에 맞는 범위와 기출을 기준으로 수업합니다.",
        ],
        "cards_h2": "고등 수학수업에서 다루는 것",
        "cards": [
            ("naesin", "school", "고등 수학내신", "학교별 기출과 부교재, 서술형까지 확인해 내신 등급을 관리합니다.", ["학교별 기출·부교재 분석", "서술형 · 고난도 문항 대비", "시험 전 실전 모의 연습"]),
            ("suneung", "target", "수능대비 · 수능수학", "개념 복습부터 기출 분석, 실전 풀이 시간 관리까지 단계적으로 준비합니다.", ["수능수학 기출 분석", "취약 단원 집중 보완", "실전 시간 배분 훈련"]),
            ("basic", "rotate-ccw", "고등 기초수학", "고등 수학이 갑자기 어려워진 학생은 중등 개념부터 다시 정리합니다.", ["중등 핵심 개념 복습", "고등 기초수학 다시 잡기", "수학공부 방법 코칭"]),
        ],
        "levels_h2": "학년별 고등 수학과외",
        "levels": [
            ("고1 수학과외", "고등학교 1학년", "공통수학 내신의 첫 시험부터 개념과 유형을 빈틈없이 정리해 등급의 흐름을 잡습니다."),
            ("고2 수학과외", "고등학교 2학년", "내신 과목을 관리하면서 개편 수능에 맞춘 수학 기본기를 함께 쌓습니다."),
            ("고3 수학과외", "고등학교 3학년", "수능수학 기출 분석과 실전 연습으로 남은 기간 목표 등급을 준비합니다."),
            ("수학 기초 재정비", "전 학년", "고등 수학이 막힌 학생은 필요한 중등 개념부터 다시 정리하고 시작합니다."),
        ],
        "faq": [
            ("내신과 수능 중 무엇을 먼저 준비해야 하나요?", "학생의 학년, 목표 전형, 현재 등급에 따라 다릅니다. 첫 상담에서 목표를 확인한 뒤 학기 중에는 내신, 방학에는 수능 기본기처럼 시기별 비중을 정해 드립니다."),
            ("수능수학 기출은 어떻게 공부하나요?", "단원별로 기출을 풀며 자주 나오는 유형과 풀이 흐름을 정리하고, 이후 실전처럼 시간을 재고 푸는 연습으로 넘어갑니다."),
            ("수학 등급이 많이 낮은데 고등 수학과외로 따라갈 수 있을까요?", "가능합니다. 어느 개념에서 막혔는지 먼저 확인하고, 필요하면 중등 기초수학부터 다시 정리해 현재 진도를 따라갈 수 있게 돕습니다."),
            ("2028 수능 개편이 수업에 어떤 영향이 있나요?", "고2 이하는 대수, 미적분Ⅰ, 확률과 통계를 공통으로 응시하는 개편 수능을 기준으로, 고3은 기존 체제를 기준으로 범위와 기출을 나눠 준비합니다."),
        ],
        "links_h2": "지역별 고등 수학과외",
        "links": [(f"{s}.html#high", f"{BY_SLUG[s][2]} 고등 수학") for s in ["gwangju-seo-gu", "gwangju-nam-gu", "gwangju-buk-gu", "gwangju-gwangsan-gu", "gwangju-dong-gu", "mokpo-si", "suncheon-si", "yeosu-si", "naju-si", "gwangyang-si"]],
    },
    {
        "slug": "online-math-tutoring",
        "title": "광주·전남 온라인 수학과외 | 1:1 화상 수학수업 - 전남광주 수학과외",
        "description": "광주·전남 온라인 수학과외. 섬·읍면 지역도 이동 없이 받는 1:1 실시간 화상 수학수업. 초등 기초수학부터 중등 수학내신, 고등 수능수학까지. 무료 상담 010-2928-3614.",
        "crumb": "온라인 수학과외",
        "label": "ONLINE 1:1 MATH TUTORING",
        "h1": "광주·전남<br><em>온라인 수학과외</em><br>어디서나 1:1로",
        "lead": "방문 수업이 어려운 섬 지역이나 읍·면 지역, 이동 시간이 아까운 학생도 실시간 화상으로 1:1 수학과외를 받을 수 있습니다. 수업 내용과 관리는 방문 수업과 똑같이 진행합니다.",
        "summary": [("수업 대상", "초등·중학생·고등학생"), ("수업 방식", "1:1 실시간 화상 수업"), ("추천 지역", "섬·읍면 지역, 방문이 어려운 곳"), ("병행", "방문 수업과 함께 운영 가능"), ("상담", "무료 상담 · 무료체험수업")],
        "intro_h2": "온라인 수학과외,<br>이런 학생에게 맞습니다",
        "intro": [
            "신안, 완도, 진도처럼 섬이 많은 지역이나 학원까지 거리가 먼 읍·면 지역은 원하는 수업을 찾기 어렵습니다. 온라인 수학과외는 이동 없이 집에서 바로 1:1 수업을 받을 수 있어 지역에 따른 교육 격차를 줄여 줍니다.",
            "실시간 화상 수업은 녹화 강의와 다릅니다. 선생님이 학생의 풀이를 화면으로 함께 보며 바로 질문하고 고쳐 주기 때문에, 학생이 어디서 막히는지 놓치지 않습니다. 평소에는 온라인으로, 시험 직전에는 방문으로 병행하는 방식도 가능합니다.",
        ],
        "cards_h2": "온라인 수학수업은 이렇게 진행됩니다",
        "cards": [
            ("live", "video", "실시간 1:1 화상 수업", "정해진 시간에 선생님과 학생이 화면으로 만나 1:1로 수업합니다.", ["실시간 질문과 피드백", "풀이 과정을 함께 확인", "녹화 강의가 아닌 대면형 수업"]),
            ("manage", "clipboard-list", "방문 수업과 같은 관리", "과제, 오답, 시험 일정 관리를 방문 수업과 똑같이 진행합니다.", ["수업마다 이해도 점검", "오답 정리와 과제 관리", "학교 시험 일정 맞춤"]),
            ("mixed", "repeat", "방문 수업과 병행", "상황에 따라 온라인과 방문 수업을 섞어서 운영할 수 있습니다.", ["평소 온라인 · 시험기간 방문", "기상·일정 변동에도 수업 유지", "지역별 가능 여부 상담 안내"]),
        ],
        "levels_h2": "온라인 수학과외 대상",
        "levels": [
            ("초등 온라인 수학", "초등학생", "짧고 집중도 높은 수업으로 연산과 초등 기초수학을 꾸준히 다집니다."),
            ("중등 온라인 수학", "중학생", "학교별 시험 범위에 맞춰 중등 수학내신과 서술형을 대비합니다."),
            ("고등 온라인 수학", "고등학생", "고등 수학내신과 수능수학을 이동 시간 없이 효율적으로 준비합니다."),
            ("섬·읍면 지역 학생", "전남 전 지역", "방문이 어려운 지역도 같은 1:1 수학과외를 받을 수 있습니다."),
        ],
        "faq": [
            ("온라인 수학과외도 방문 수업만큼 효과가 있나요?", "실시간으로 풀이를 함께 보며 질문하고 고쳐 주는 방식이라 1:1 관리 효과는 같습니다. 집중이 어려운 학생은 수업 시간과 구성을 조정해 드립니다."),
            ("온라인 수업에는 무엇이 필요한가요?", "화상 연결이 가능한 기기와 안정적인 인터넷이 필요합니다. 구체적인 준비 방법은 상담 때 학생 환경에 맞춰 안내해 드립니다."),
            ("방문 수업과 섞어서 할 수도 있나요?", "가능합니다. 평소에는 온라인으로, 시험 직전에는 방문으로 진행하는 등 지역과 일정에 맞춰 조정할 수 있습니다."),
            ("섬 지역도 온라인 수업이 되나요?", "인터넷이 연결되는 곳이라면 신안, 완도, 진도 등 섬 지역에서도 온라인 수학과외를 받을 수 있습니다."),
        ],
        "links_h2": "온라인 수업 문의가 많은 지역",
        "links": [region_link(s) for s in ["sinan-gun", "wando-gun", "jindo-gun", "goheung-gun", "gurye-gun", "gokseong-gun", "haenam-gun", "yeonggwang-gun"]],
    },
    {
        "slug": "bongseon-dong-math",
        "title": "봉선동 수학과외 | 광주 남구 초등·중등·고등 1:1 수학 - 전남광주 수학과외",
        "description": "봉선동 수학과외. 광주 남구 봉선동·주월동·진월동 학생을 위한 초등 기초수학, 중등 수학내신, 고등 수능수학 1:1 맞춤 수업. 무료 상담 010-2928-3614.",
        "crumb": "봉선동 수학과외",
        "parent": "gwangju-nam-gu",
        "label": "BONGSEON-DONG MATH TUTORING",
        "h1": "봉선동 수학과외<br><em>초등·중등·고등</em><br>1:1 맞춤 수업",
        "lead": "광주를 대표하는 학원가인 봉선동에서, 학원 수업만으로 채워지지 않는 부분을 1:1로 보완합니다. 봉선동과 가까운 주월동, 진월동, 방림동 학생도 함께 안내합니다.",
        "summary": [("수업 지역", "봉선동 · 주월동 · 진월동 · 방림동"), ("수업 대상", "초등·중학생·고등학생"), ("수업 내용", "초등 기초수학 · 중등 수학내신 · 고등 수능수학"), ("수업 방식", "1:1 방문 또는 온라인"), ("상담", "무료 상담 · 무료체험수업")],
        "intro_h2": "봉선동에서<br>1:1 수학과외가 필요한 이유",
        "intro": [
            "봉선동은 학원이 많고 교육열이 높은 지역인 만큼, 학생들의 진도와 시험 수준도 높은 편입니다. 진도는 빠른데 개념이 따라가지 못하거나, 학원 숙제는 하지만 왜 틀렸는지 모르는 경우 1:1 수학과외가 효과적입니다.",
            "학원 수업과 병행하는 경우에는 학원 진도를 확인해 겹치지 않게, 부족한 개념과 오답을 보완하는 방향으로 수업을 구성합니다. 학원 없이 1:1 수업만으로 내신과 수능을 준비하는 학생에게는 전체 학습 계획을 함께 설계합니다.",
        ],
        "cards_h2": "봉선동 학년별 수학수업",
        "cards": grade_cards("봉선동"),
        "faq": [
            ("학원에 다니면서 1:1 수학과외를 함께 해도 되나요?", "네. 학원 진도와 숙제를 확인한 뒤 겹치지 않도록, 이해가 부족한 개념과 오답 위주로 보완하는 수업을 구성합니다."),
            ("봉선동 학교 내신 수준에 맞춰 준비할 수 있나요?", "학생이 다니는 학교의 시험 범위와 기출 난이도를 확인하고, 고난도 문항과 서술형까지 대비할 수 있도록 수업합니다."),
            ("주월동, 진월동도 방문 수업이 되나요?", "봉선동과 가까운 주월동, 진월동, 방림동 등 광주 남구 대부분 지역에서 방문 수업을 안내합니다."),
            ("수업료는 어떻게 되나요?", "학년, 수업 횟수, 방식에 따라 달라지며 전화 상담에서 투명하게 안내합니다. 상담은 무료입니다."),
        ],
        "links_h2": "봉선동 주변 수학과외",
        "links": [region_link("gwangju-nam-gu"), ("sangmu-math.html", "상무지구 수학과외"), region_link("gwangju-dong-gu"), region_link("gwangju-seo-gu"), region_link("hwasun-gun")],
    },
    {
        "slug": "sangmu-math",
        "title": "상무지구 수학과외 | 광주 서구 초등·중등·고등 1:1 수학 - 전남광주 수학과외",
        "description": "상무지구 수학과외. 광주 서구 치평동·쌍촌동·화정동 학생을 위한 초등 기초수학, 중등 수학내신, 고등 수능수학 1:1 맞춤 수업. 무료 상담 010-2928-3614.",
        "crumb": "상무지구 수학과외",
        "parent": "gwangju-seo-gu",
        "label": "SANGMU DISTRICT MATH TUTORING",
        "h1": "상무지구 수학과외<br><em>초등·중등·고등</em><br>1:1 맞춤 수업",
        "lead": "광주 서구의 중심인 상무지구에서 바쁜 학생 일정에 맞춰 1:1 수학과외를 진행합니다. 치평동, 쌍촌동, 화정동, 금호동 등 상무지구 생활권 학생을 함께 안내합니다.",
        "summary": [("수업 지역", "치평동 · 쌍촌동 · 화정동 · 금호동"), ("수업 대상", "초등·중학생·고등학생"), ("수업 내용", "초등 기초수학 · 중등 수학내신 · 고등 수능수학"), ("수업 방식", "1:1 방문 또는 온라인"), ("상담", "무료 상담 · 무료체험수업")],
        "intro_h2": "상무지구에서<br>1:1 수학과외를 찾는다면",
        "intro": [
            "상무지구는 아파트 단지와 학원, 업무 시설이 함께 모여 있어 맞벌이 가정이 많고 학생들의 일정도 빠듯한 편입니다. 1:1 수학과외는 학생이 다니는 다른 학원 일정과 학교 시험 일정을 고려해 수업 시간과 분량을 맞출 수 있다는 장점이 있습니다.",
            "수업마다 무엇을 배웠고 어디가 부족한지 점검해 다음 수업 계획에 반영합니다. 학부모님이 바쁘셔도 학생의 수학 공부가 흐트러지지 않도록 꾸준한 흐름을 만드는 것을 목표로 합니다.",
        ],
        "cards_h2": "상무지구 학년별 수학수업",
        "cards": grade_cards("상무지구"),
        "faq": [
            ("다른 학원 일정과 겹치지 않게 수업 시간을 조정할 수 있나요?", "네. 학생의 학원, 학교 일정을 먼저 확인하고 가능한 시간대에 맞춰 수업 요일과 시간을 정합니다."),
            ("치평동, 쌍촌동 쪽도 방문 수업이 되나요?", "치평동, 쌍촌동, 화정동, 금호동 등 상무지구 생활권과 광주 서구 대부분 지역에서 방문 수업을 안내합니다."),
            ("중등 수학내신은 학교별로 준비하나요?", "학생이 다니는 학교의 진도, 시험 범위, 기출 유형을 확인해 학교 시험에 맞춘 내신 대비를 진행합니다."),
            ("수업료는 어떻게 되나요?", "학년, 수업 횟수, 방식에 따라 달라지며 전화 상담에서 투명하게 안내합니다. 상담은 무료입니다."),
        ],
        "links_h2": "상무지구 주변 수학과외",
        "links": [region_link("gwangju-seo-gu"), ("bongseon-dong-math.html", "봉선동 수학과외"), ("suwan-math.html", "수완지구 수학과외"), region_link("gwangju-gwangsan-gu"), region_link("gwangju-nam-gu")],
    },
    {
        "slug": "suwan-math",
        "title": "수완지구 수학과외 | 광주 광산구 초등·중등·고등 1:1 수학 - 전남광주 수학과외",
        "description": "수완지구 수학과외. 광주 광산구 수완동·신창동·장덕동 학생을 위한 초등 기초수학, 중등 수학내신, 고등 수능수학 1:1 맞춤 수업. 무료 상담 010-2928-3614.",
        "crumb": "수완지구 수학과외",
        "parent": "gwangju-gwangsan-gu",
        "label": "SUWAN DISTRICT MATH TUTORING",
        "h1": "수완지구 수학과외<br><em>초등·중등·고등</em><br>1:1 맞춤 수업",
        "lead": "학생 수가 많은 대단지 주거 지역인 수완지구에서 학생 한 명 한 명에게 맞춘 1:1 수학과외를 진행합니다. 수완동, 장덕동, 신창동, 신가동 학생을 함께 안내합니다.",
        "summary": [("수업 지역", "수완동 · 장덕동 · 신창동 · 신가동"), ("수업 대상", "초등·중학생·고등학생"), ("수업 내용", "초등 기초수학 · 중등 수학내신 · 고등 수능수학"), ("수업 방식", "1:1 방문 또는 온라인"), ("상담", "무료 상담 · 무료체험수업")],
        "intro_h2": "수완지구에서<br>1:1 수학과외가 필요한 이유",
        "intro": [
            "수완지구는 초등학생부터 고등학생까지 학생 수가 많은 지역이라 학원 반 인원도 많은 편입니다. 여러 명이 함께 듣는 수업에서는 질문할 기회가 적고, 이해하지 못한 채 진도가 넘어가기 쉽습니다.",
            "1:1 수학과외는 학생이 이해할 때까지 설명하고, 틀린 문제를 그 자리에서 함께 고칠 수 있습니다. 특히 초등 고학년에서 중학교로, 중3에서 고등학교로 넘어가는 시기에 기초를 확실히 다지는 데 효과적입니다.",
        ],
        "cards_h2": "수완지구 학년별 수학수업",
        "cards": grade_cards("수완지구"),
        "faq": [
            ("수완지구 초등학생도 수학과외가 가능한가요?", "가능합니다. 연산과 초등 기초수학, 서술형 문제를 중심으로 학생 학년과 수준에 맞춰 진행합니다."),
            ("장덕동, 신창동도 방문 수업이 되나요?", "수완동, 장덕동, 신창동, 신가동 등 수완지구 생활권과 광주 광산구 대부분 지역에서 방문 수업을 안내합니다."),
            ("중3인데 고등 수학 선행도 함께 할 수 있나요?", "중3 내신을 안정적으로 관리하면서 학생 속도에 맞춰 고등 공통수학을 준비합니다."),
            ("수업료는 어떻게 되나요?", "학년, 수업 횟수, 방식에 따라 달라지며 전화 상담에서 투명하게 안내합니다. 상담은 무료입니다."),
        ],
        "links_h2": "수완지구 주변 수학과외",
        "links": [region_link("gwangju-gwangsan-gu"), ("cheomdan-math.html", "첨단지구 수학과외"), ("sangmu-math.html", "상무지구 수학과외"), region_link("gwangju-buk-gu"), region_link("jangseong-gun")],
    },
    {
        "slug": "cheomdan-math",
        "title": "첨단지구 수학과외 | 광주 광산구·북구 첨단 1:1 수학 - 전남광주 수학과외",
        "description": "첨단 수학과외. 광주 광산구 첨단1지구 쌍암동·월계동과 북구 첨단2지구 학생을 위한 초등 기초수학, 중등 수학내신, 고등 수능수학 1:1 수업. 무료 상담 010-2928-3614.",
        "crumb": "첨단지구 수학과외",
        "parent": "gwangju-gwangsan-gu",
        "label": "CHEOMDAN DISTRICT MATH TUTORING",
        "h1": "첨단지구 수학과외<br><em>초등·중등·고등</em><br>1:1 맞춤 수업",
        "lead": "광산구 첨단1지구(쌍암동·월계동·산월동)와 북구 첨단2지구 학생을 위한 1:1 수학과외입니다. 두 지역 모두 방문 수업과 온라인 수업을 안내합니다.",
        "summary": [("수업 지역", "쌍암동 · 월계동 · 산월동 · 첨단2지구"), ("수업 대상", "초등·중학생·고등학생"), ("수업 내용", "초등 기초수학 · 중등 수학내신 · 고등 수능수학"), ("수업 방식", "1:1 방문 또는 온라인"), ("상담", "무료 상담 · 무료체험수업")],
        "intro_h2": "첨단지구에서<br>수학과외를 찾고 계신가요?",
        "intro": [
            "첨단지구는 광산구와 북구에 걸쳐 있어, 같은 첨단 생활권이라도 다니는 학교와 시험 범위가 서로 다릅니다. 그래서 첨단 수학과외는 학생이 다니는 학교를 기준으로 진도와 내신 대비 계획을 세웁니다.",
            "연구단지와 산업단지가 가까워 맞벌이 가정이 많은 지역인 만큼, 학생이 혼자서도 공부를 이어갈 수 있도록 수업 후 복습과 과제의 양을 학생에게 맞게 조절합니다.",
        ],
        "cards_h2": "첨단지구 학년별 수학수업",
        "cards": grade_cards("첨단지구"),
        "faq": [
            ("첨단1지구와 첨단2지구 모두 수업이 되나요?", "네. 광산구 첨단1지구(쌍암동·월계동·산월동)와 북구 첨단2지구 모두 방문 수업과 온라인 수업을 안내합니다."),
            ("학교마다 시험 범위가 다른데 맞춰 주시나요?", "학생이 다니는 학교의 진도와 시험 범위, 기출 유형을 확인해 그 학교에 맞춘 내신 대비를 진행합니다."),
            ("고등학생 수능수학 대비도 가능한가요?", "가능합니다. 고등 수학내신과 수능대비를 학생의 학년과 목표 등급에 맞게 나눠 계획합니다."),
            ("수업료는 어떻게 되나요?", "학년, 수업 횟수, 방식에 따라 달라지며 전화 상담에서 투명하게 안내합니다. 상담은 무료입니다."),
        ],
        "links_h2": "첨단지구 주변 수학과외",
        "links": [region_link("gwangju-gwangsan-gu"), region_link("gwangju-buk-gu"), ("suwan-math.html", "수완지구 수학과외"), region_link("jangseong-gun"), region_link("damyang-gun")],
    },
    {
        "slug": "namak-math",
        "title": "남악 수학과외 | 무안 남악·오룡 초등·중등·고등 1:1 수학 - 전남광주 수학과외",
        "description": "남악 수학과외. 무안 남악신도시·오룡지구와 목포 옥암동 학생을 위한 초등 기초수학, 중등 수학내신, 고등 수능수학 1:1 맞춤 수업. 무료 상담 010-2928-3614.",
        "crumb": "남악신도시 수학과외",
        "parent": "muan-gun",
        "label": "NAMAK NEW TOWN MATH TUTORING",
        "h1": "남악 수학과외<br><em>초등·중등·고등</em><br>1:1 맞춤 수업",
        "lead": "전남도청이 있는 무안 남악신도시와 오룡지구, 맞닿아 있는 목포 옥암동 학생을 위한 1:1 수학과외입니다. 신도시 특성상 어린 학생이 많은 만큼 초등 기초수학부터 탄탄하게 안내합니다.",
        "summary": [("수업 지역", "남악신도시 · 오룡지구 · 옥암동"), ("수업 대상", "초등·중학생·고등학생"), ("수업 내용", "초등 기초수학 · 중등 수학내신 · 고등 수능수학"), ("수업 방식", "1:1 방문 또는 온라인"), ("상담", "무료 상담 · 무료체험수업")],
        "intro_h2": "남악신도시에서<br>수학과외를 찾고 계신가요?",
        "intro": [
            "남악신도시와 오룡지구는 젊은 가정이 많이 사는 지역이라 초등학생과 중학생 비중이 높습니다. 초등 때 수학 기초를 제대로 잡아 두면 중학교 수학내신과 고등 수학까지 훨씬 수월해집니다.",
            "남악은 행정구역상 무안군이지만 생활권은 목포 옥암동, 하당동과 이어져 있습니다. 학생이 다니는 학교와 생활권을 기준으로 방문 수업 가능 여부를 안내하고, 필요하면 온라인 수업과 병행합니다.",
        ],
        "cards_h2": "남악 학년별 수학수업",
        "cards": grade_cards("남악"),
        "faq": [
            ("오룡지구도 방문 수업이 되나요?", "남악신도시와 오룡지구, 목포 옥암동 등 남악 생활권에서 방문 수업을 안내합니다. 정확한 가능 여부는 상담 때 확인해 드립니다."),
            ("남악 초등학생 수학과외는 어떻게 진행하나요?", "연산과 초등 기초수학, 서술형을 중심으로 진행하고 고학년은 중학교 수학으로 넘어갈 준비를 함께 합니다."),
            ("목포 학교에 다니는데 수업이 가능한가요?", "가능합니다. 학생이 다니는 학교의 진도와 시험 범위를 기준으로 수업하므로 목포 학교 학생도 같은 방식으로 내신을 준비합니다."),
            ("수업료는 어떻게 되나요?", "학년, 수업 횟수, 방식에 따라 달라지며 전화 상담에서 투명하게 안내합니다. 상담은 무료입니다."),
        ],
        "links_h2": "남악 주변 수학과외",
        "links": [region_link("muan-gun"), region_link("mokpo-si"), region_link("yeongam-gun"), region_link("sinan-gun"), region_link("naju-si")],
    },
]


def page_head(title, description, url, jsonld):
    jsonld_html = "\n".join(
        f'  <script type="application/ld+json">{json.dumps(item, ensure_ascii=False)}</script>' for item in jsonld
    )
    return f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{BRAND}">
  <meta property="og:locale" content="ko_KR">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/og-image.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#173f32">
  <link rel="icon" href="logo.svg" type="image/svg+xml">
  <link rel="icon" href="favicon.ico" sizes="any">
  <link rel="apple-touch-icon" href="apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@700&family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
  <link rel="stylesheet" href="region-page.css">
  <script src="https://unpkg.com/lucide@0.468.0/dist/umd/lucide.min.js" defer></script>
  <script src="region-page.js" defer></script>
{jsonld_html}
</head>"""


def build_topic(page):
    slug = page["slug"]
    url = f"{SITE}/{slug}.html"
    parent = page.get("parent")
    crumbs = [(BRAND, f"{SITE}/", "index.html")]
    if parent:
        crumbs.append((f"{BY_SLUG[parent][2]} 수학과외", f"{SITE}/{parent}.html", f"{parent}.html"))
    crumbs.append((page["crumb"], url, None))

    jsonld = [
        {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": page["crumb"],
            "serviceType": "수학과외",
            "description": page["description"],
            "url": url,
            "provider": {"@type": "EducationalOrganization", "@id": f"{SITE}/#organization", "name": BRAND, "telephone": PHONE, "url": f"{SITE}/"},
            "areaServed": {"@type": "AdministrativeArea", "name": BY_SLUG[parent][1] if parent else "광주광역시·전라남도"},
            "audience": {"@type": "EducationalAudience", "educationalRole": "student"},
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": i, "name": name, "item": item}
                for i, (name, item, _) in enumerate(crumbs, 1)
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in page["faq"]
            ],
        },
    ]

    breadcrumb = " / ".join(f'<a href="{href}">{name if href != "index.html" else "홈"}</a>' if href else name for name, _, href in crumbs)
    summary = "".join(f"<div><dt>{dt}</dt><dd>{dd}</dd></div>" for dt, dd in page["summary"])
    intro = "".join(f"<p>{p}</p>" for p in page["intro"])
    cards = "\n".join(
        f"""          <article class="program-card{' featured' if i == 1 else ''}" id="{cid}">
            <span class="card-number">{i + 1:02d}</span>
            {ICON.format(icon)}
            <h3>{title}</h3>
            <p>{text}</p>
            <ul>{''.join(f'<li>{li}</li>' for li in items)}</ul>
          </article>"""
        for i, (cid, icon, title, text, items) in enumerate(page["cards"])
    )
    levels = ""
    if page.get("levels"):
        items = "\n".join(f"          <li><h3>{h}</h3><small>{s}</small><p>{t}</p></li>" for h, s, t in page["levels"])
        levels = f"""
    <section class="region-levels section" aria-labelledby="level-title">
      <div class="section-inner">
        <div class="region-heading"><p class="section-label">BY GRADE</p><h2 id="level-title">{page['levels_h2']}</h2></div>
        <ul class="level-grid">
{items}
        </ul>
      </div>
    </section>
"""
    faq_html = "\n".join(
        f'          <details><summary>{esc(q)}{ICON.format("plus")}</summary><p>{esc(a)}</p></details>' for q, a in page["faq"]
    )
    links = "".join(f'<a href="{href}">{text}</a>' for href, text in page["links"])
    hub_links = "".join(f'<a href="{s}.html">{t}</a>' for s, t in HUBS if s != slug)
    heading_name = page["crumb"]

    return page_head(page["title"], page["description"], url, jsonld) + f"""
<body>
  <a class="skip-link" href="#main">본문 바로가기</a>
  <header class="site-header region-header" id="top">
    <div class="header-inner">
      <a class="brand" href="index.html" aria-label="{BRAND} 홈"><img class="brand-mark" src="logo.svg" width="40" height="40" alt=""><span><strong>{BRAND}</strong><small>광주·전남 1:1 맞춤 과외</small></span></a>
      <nav class="desktop-nav" aria-label="{heading_name} 메뉴">
        <a href="gwangju-elementary-math.html">초등 수학</a>
        <a href="gwangju-middle-math.html">중등 수학</a>
        <a href="gwangju-high-math.html">고등 수학</a>
        <a href="#faq">자주 묻는 질문</a>
      </nav>
      <a class="header-cta" href="tel:{TEL}" aria-label="{PHONE}로 전화 상담">{ICON.format("phone")} {PHONE}</a>
    </div>
  </header>
  <main class="region-main" id="main">
    <section class="region-hero">
      <div class="section-inner">
        <div>
          <nav class="region-breadcrumb" aria-label="현재 위치">{breadcrumb}</nav>
          <p class="section-label">{page['label']}</p>
          <h1>{page['h1']}</h1>
          <p class="region-lead">{page['lead']}</p>
          <a class="button primary" href="tel:{TEL}">{ICON.format("phone")} 무료 상담 {PHONE}</a>
        </div>
        <aside class="region-summary" aria-label="{heading_name} 요약">
          <h2>{heading_name} 한눈에 보기</h2>
          <dl>{summary}</dl>
        </aside>
      </div>
    </section>

    <section class="region-intro section">
      <div class="section-inner region-intro-grid">
        <div class="region-heading"><p class="section-label">WHY 1:1 MATH</p><h2>{page['intro_h2']}</h2></div>
        <div class="region-intro-copy">{intro}</div>
      </div>
    </section>

    <section class="region-grades section" aria-labelledby="card-title">
      <div class="section-inner">
        <div class="region-heading"><p class="section-label">MATH LESSON</p><h2 id="card-title">{page['cards_h2']}</h2></div>
        <div class="program-grid">
{cards}
        </div>
      </div>
    </section>
{levels}
    <section class="trial-process section">
      <div class="section-inner trial-layout">
        <div><p class="section-label">FREE TRIAL PROCESS</p><h2>무료체험수업은 이렇게 진행됩니다.</h2></div>
        <ol class="trial-steps"><li><span>1</span><div><h3>전화 상담</h3><p>학년, 학교, 현재 고민과 원하는 수업 일정을 확인합니다.</p></div></li><li><span>2</span><div><h3>맞춤 선생님 안내</h3><p>수업 가능 지역과 방식, 학생에게 맞는 선생님을 안내합니다.</p></div></li><li><span>3</span><div><h3>무료체험수업</h3><p>직접 수업을 경험한 뒤 정규 수업 진행 여부를 결정합니다.</p></div></li></ol>
      </div>
    </section>

    <section class="faq section" id="faq" aria-labelledby="faq-title">
      <div class="section-inner faq-layout">
        <div>
          <p class="section-label">FAQ</p>
          <h2 id="faq-title">{heading_name}<br>자주 묻는 질문</h2>
        </div>
        <div class="accordion">
{faq_html}
        </div>
      </div>
    </section>

    <section class="contact section" id="contact">
      <div class="section-inner">
        <div class="contact-copy"><p class="section-label light">FREE TRIAL LESSON</p><h2>{heading_name},<br>편하게 상담하세요.</h2><p>학생에게 필요한 수업인지 무료체험수업으로 먼저 확인할 수 있습니다.</p><a class="contact-phone" href="tel:{TEL}">{ICON.format("phone-call")}<span><small>지금 전화 상담하기</small><strong>{PHONE}</strong></span></a></div>
      </div>
    </section>

    <nav class="nearby" aria-label="관련 수학과외 안내">
      <div class="section-inner">
        <h2>{page['links_h2']}</h2>
        <div class="region-links">{links}<a href="index.html#area">광주·전남 전체 지역</a></div>
        <h2 class="nearby-sub">학년·방식별 수학과외</h2>
        <div class="region-links">{hub_links}</div>
      </div>
    </nav>
  </main>
  <footer class="site-footer"><div class="section-inner footer-inner"><a class="brand footer-brand" href="index.html"><img class="brand-mark" src="logo.svg" width="40" height="40" alt=""><span><strong>{BRAND}</strong><small>광주·전남 1:1 맞춤 과외</small></span></a><div class="footer-copy"><p>광주·전남 초등·중등·고등 수학과외 · 전화 상담 {PHONE}</p><p>© 2026 {BRAND}. All rights reserved.</p></div><a class="to-top" href="#top" aria-label="맨 위로">{ICON.format("arrow-up")}</a></div></footer>
</body>
</html>
"""


def build_sitemap():
    urls = [f"""  <url>
    <loc>{SITE}/</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>"""]
    urls += [
        f"  <url><loc>{SITE}/{p['slug']}.html</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>0.9</priority></url>"
        for p in TOPIC_PAGES
    ]
    urls += [
        f"  <url><loc>{SITE}/{r[0]}.html</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>"
        for r in REGIONS
    ]
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n"


if __name__ == "__main__":
    for region in REGIONS:
        (ROOT / f"{region[0]}.html").write_text(build(region), encoding="utf-8", newline="\n")
    for page in TOPIC_PAGES:
        (ROOT / f"{page['slug']}.html").write_text(build_topic(page), encoding="utf-8", newline="\n")
    (ROOT / "sitemap.xml").write_text(build_sitemap(), encoding="utf-8", newline="\n")
    print(f"지역 페이지 {len(REGIONS)}개, 주제 페이지 {len(TOPIC_PAGES)}개, sitemap.xml 생성 완료")
