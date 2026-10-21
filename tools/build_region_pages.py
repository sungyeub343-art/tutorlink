"""지역 페이지(27개)를 정적 HTML로 생성합니다.

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
        f'<a href="{n}.html">{BY_SLUG[n][2]} 수학과외</a>' for n in neighbors
    )

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
      </div>
    </nav>
  </main>
  <footer class="site-footer"><div class="section-inner footer-inner"><a class="brand footer-brand" href="index.html"><img class="brand-mark" src="logo.svg" width="40" height="40" alt=""><span><strong>{BRAND}</strong><small>광주·전남 1:1 맞춤 과외</small></span></a><div class="footer-copy"><p>{name} 초등·중등·고등 수학과외 · 전화 상담 {PHONE}</p><p>© 2026 {BRAND}. All rights reserved.</p></div><a class="to-top" href="#top" aria-label="맨 위로">{ICON.format("arrow-up")}</a></div></footer>
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
        f"  <url><loc>{SITE}/{r[0]}.html</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>"
        for r in REGIONS
    ]
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n"


if __name__ == "__main__":
    for region in REGIONS:
        (ROOT / f"{region[0]}.html").write_text(build(region), encoding="utf-8", newline="\n")
    (ROOT / "sitemap.xml").write_text(build_sitemap(), encoding="utf-8", newline="\n")
    print(f"{len(REGIONS)}개 지역 페이지와 sitemap.xml을 생성했습니다.")
