const header = document.querySelector('.site-header');
const menuButton = document.querySelector('.menu-button');
const mobileNav = document.querySelector('.mobile-nav');

const updateHeader = () => header.classList.toggle('scrolled', window.scrollY > 24);
updateHeader();
window.addEventListener('scroll', updateHeader, { passive: true });

menuButton.addEventListener('click', () => {
  const isOpen = menuButton.getAttribute('aria-expanded') === 'true';
  menuButton.setAttribute('aria-expanded', String(!isOpen));
  menuButton.setAttribute('aria-label', isOpen ? '메뉴 열기' : '메뉴 닫기');
  mobileNav.hidden = isOpen;
  header.classList.toggle('menu-open', !isOpen);
  menuButton.innerHTML = `<i data-lucide="${isOpen ? 'menu' : 'x'}" aria-hidden="true"></i>`;
  lucide.createIcons();
});

mobileNav.querySelectorAll('a').forEach((link) => {
  link.addEventListener('click', () => {
    mobileNav.hidden = true;
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.setAttribute('aria-label', '메뉴 열기');
    menuButton.innerHTML = '<i data-lucide="menu" aria-hidden="true"></i>';
    header.classList.remove('menu-open');
    lucide.createIcons();
  });
});

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.reveal').forEach((element) => observer.observe(element));

document.querySelectorAll('.accordion details').forEach((detail) => {
  detail.addEventListener('toggle', () => {
    if (!detail.open) return;
    document.querySelectorAll('.accordion details').forEach((other) => {
      if (other !== detail) other.open = false;
    });
  });
});

document.querySelector('#consult-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const status = form.querySelector('.form-status');
  const submitButton = form.querySelector('.submit-button');
  const formData = new FormData(form);

  formData.append('_subject', '광주·전남 과외 무료 상담 신청');
  formData.append('_template', 'table');
  formData.append('_captcha', 'false');
  formData.append('page', window.location.href);
  submitButton.disabled = true;
  status.textContent = '상담 신청을 전송하고 있습니다.';

  try {
    const response = await fetch('https://formsubmit.co/ajax/sungyeub343@gmail.com', {
      method: 'POST',
      headers: { Accept: 'application/json' },
      body: formData,
    });
    if (!response.ok) throw new Error('Submission failed');
    form.reset();
    status.textContent = '상담 신청이 접수되었습니다. 확인 후 연락드리겠습니다.';
  } catch (error) {
    status.textContent = '전송하지 못했습니다. 잠시 후 다시 시도하거나 전화로 문의해 주세요.';
  } finally {
    submitButton.disabled = false;
  }
});

window.addEventListener('DOMContentLoaded', () => lucide.createIcons());