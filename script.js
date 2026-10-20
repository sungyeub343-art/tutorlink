const header = document.querySelector('.site-header');
const menuButton = document.querySelector('.menu-button');
const mobileNav = document.querySelector('.mobile-nav');
const regionDialog = document.querySelector('.region-dialog');
const regionDialogClose = document.querySelector('.region-dialog-close');

const REGION_DIALOG_SEEN_KEY = 'regionDialogSeen';
const hasSeenRegionDialog = () => {
  try {
    return sessionStorage.getItem(REGION_DIALOG_SEEN_KEY) === '1';
  } catch {
    return false;
  }
};
const isInternalVisit = () => {
  try {
    return document.referrer && new URL(document.referrer).origin === location.origin;
  } catch {
    return false;
  }
};

// 첫 진입 시에만 지역 선택 창을 띄우고, 사이트 내 이동(다른 페이지에서 돌아오기, #앵커 이동)에는 띄우지 않음
if (!hasSeenRegionDialog() && !isInternalVisit() && !location.hash) {
  regionDialog.showModal();
  try {
    sessionStorage.setItem(REGION_DIALOG_SEEN_KEY, '1');
  } catch {}
}
regionDialogClose.addEventListener('click', () => regionDialog.close());
regionDialog.addEventListener('click', (event) => {
  if (event.target === regionDialog) regionDialog.close();
});

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

window.addEventListener('DOMContentLoaded', () => lucide.createIcons());