const header = document.querySelector('[data-header]');
const menuButton = document.querySelector('[data-menu-toggle]');
const nav = document.querySelector('[data-nav]');
const backdrop = document.querySelector('[data-menu-backdrop]');

const closeMenu = ({ restoreFocus = false } = {}) => {
  menuButton.setAttribute('aria-expanded', 'false');
  nav.classList.remove('is-open');
  document.body.classList.remove('menu-open');
  if (restoreFocus) menuButton.focus();
};

menuButton.addEventListener('click', () => {
  const isOpen = menuButton.getAttribute('aria-expanded') === 'true';
  if (isOpen) {
    closeMenu();
    return;
  }

  menuButton.setAttribute('aria-expanded', 'true');
  nav.classList.add('is-open');
  document.body.classList.add('menu-open');
  nav.querySelector('a')?.focus();
});

nav.querySelectorAll('a').forEach((link) => link.addEventListener('click', closeMenu));
backdrop.addEventListener('click', () => closeMenu({ restoreFocus: true }));

window.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
    closeMenu({ restoreFocus: true });
  }
});

window.addEventListener('resize', () => {
  if (window.innerWidth > 900) closeMenu();
});

window.addEventListener('scroll', () => {
  header.classList.toggle('is-scrolled', window.scrollY > 24);
}, { passive: true });
