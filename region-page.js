const regionRoot = document.querySelector('#region-page');

if (regionRoot) {
  const { region, area, province } = document.body.dataset;
  const englishLabel = document.body.dataset.english;
  regionRoot.innerHTML = `
    <section class="region-hero">
      <div class="section-inner">
        <div>
          <p class="region-breadcrumb"><a href="index.html">홈</a> / ${region}</p>
          <p class="section-label">${englishLabel} HIGH SCHOOL MATH</p>
          <h1>${region}<br><em>고등 수학과외</em><br>무료체험수업 안내</h1>
          <p class="region-lead">${area} 등 ${region} 고등학생의 현재 실력과 목표에 맞춰 내신·수능 수학 학습 방향을 설계합니다.</p>
          <a class="button primary" href="tel:01029283614"><i data-lucide="phone" aria-hidden="true"></i> 무료체험수업 상담 010-2928-3614</a>
        </div>
        <aside class="region-summary" aria-label="수업 요약">
          <h2>무료체험수업 한눈에 보기</h2>
          <dl><div><dt>수업 대상</dt><dd>${region} 고등학생</dd></div><div><dt>수업 과목</dt><dd>고등 수학 · 내신 · 수능</dd></div><div><dt>수업 방식</dt><dd>1:1 방문 또는 온라인</dd></div><div><dt>상담 비용</dt><dd>무료</dd></div></dl>
        </aside>
      </div>
    </section>
    <section class="region-benefits section">
      <div class="section-inner">
        <div class="region-heading"><p class="section-label">PERSONALIZED MATH LESSON</p><h2>학생에게 필요한 수학 공부부터 찾습니다.</h2></div>
        <div class="benefit-grid">
          <article class="benefit-item"><i data-lucide="clipboard-check" aria-hidden="true"></i><h3>현재 실력 진단</h3><p>개념 이해도와 문제 풀이 습관을 확인해 먼저 보완할 단원을 정합니다.</p></article>
          <article class="benefit-item"><i data-lucide="school" aria-hidden="true"></i><h3>학교별 내신 대비</h3><p>학교 진도와 시험 일정에 맞춰 개념, 유형, 서술형 학습을 연결합니다.</p></article>
          <article class="benefit-item"><i data-lucide="chart-no-axes-combined" aria-hidden="true"></i><h3>수능 학습 설계</h3><p>목표 등급과 남은 기간을 고려해 실전까지 이어지는 계획을 세웁니다.</p></article>
        </div>
      </div>
    </section>
    <section class="trial-process section">
      <div class="section-inner trial-layout">
        <div><p class="section-label">FREE TRIAL PROCESS</p><h2>무료체험수업은 이렇게 진행됩니다.</h2></div>
        <ol class="trial-steps"><li><span>1</span><div><h3>전화 상담</h3><p>학년, 학교, 현재 고민과 원하는 수업 일정을 확인합니다.</p></div></li><li><span>2</span><div><h3>맞춤 선생님 안내</h3><p>${region} 수업 가능 여부와 학생에게 맞는 선생님을 안내합니다.</p></div></li><li><span>3</span><div><h3>무료체험수업</h3><p>직접 수업을 경험한 뒤 정규 수업 진행 여부를 결정합니다.</p></div></li></ol>
      </div>
    </section>
    <section class="contact section" id="contact">
      <div class="section-inner contact-layout">
        <div class="contact-copy"><p class="section-label light">FREE TRIAL LESSON</p><h2>${region} 수학과외,<br>편하게 상담하세요.</h2><p>학생에게 필요한 수업인지 무료체험수업으로 먼저 확인할 수 있습니다.</p><a class="contact-phone" href="tel:01029283614"><i data-lucide="phone-call" aria-hidden="true"></i><span><small>지금 전화 상담하기</small><strong>010-2928-3614</strong></span></a></div>
        <form class="consult-form" id="consult-form"><div class="field-row"><label>학생 이름<input type="text" name="studentName" placeholder="이름" required></label><label>학년<select name="level" required><option value="">선택해 주세요</option><option>고등학교 1학년</option><option>고등학교 2학년</option><option>고등학교 3학년</option></select></label></div><label>연락처<input type="tel" name="phone" inputmode="tel" placeholder="010-0000-0000" autocomplete="tel" required></label><label>학교·거주 지역<input type="text" name="location" placeholder="예: ${region}" required></label><label class="consent"><input type="checkbox" name="privacy" required><span>개인정보 수집 및 상담 활용에 동의합니다.</span></label><button class="submit-button" type="submit">무료체험수업 상담 신청 <i data-lucide="arrow-right" aria-hidden="true"></i></button><p class="form-status" role="status" aria-live="polite"></p></form>
      </div>
    </section>
    <nav class="nearby" aria-label="다른 지역 보기"><div class="section-inner"><h2>다른 ${province} 지역 보기</h2><div class="region-links"><a href="index.html#area">전체 지역 목록</a></div></div></nav>`;
}

document.querySelector('#consult-form')?.addEventListener('submit', (event) => {
  event.preventDefault();
  const status = event.currentTarget.querySelector('.form-status');
  status.textContent = '상담 접수 기능 연결을 준비 중입니다. 전화 상담을 이용해 주세요.';
});

window.addEventListener('DOMContentLoaded', () => lucide.createIcons());