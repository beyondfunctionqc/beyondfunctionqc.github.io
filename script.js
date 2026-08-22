const header = document.querySelector('[data-header]');
const menuButton = document.querySelector('[data-menu-toggle]');
const nav = document.querySelector('[data-nav]');
const navLinks = [...nav.querySelectorAll('a')];
const desktopNavMedia = window.matchMedia('(min-width: 1200px)');

const isMenuOpen = () => menuButton.getAttribute('aria-expanded') === 'true';

const closeMenu = ({ restoreFocus = false } = {}) => {
  menuButton.setAttribute('aria-expanded', 'false');
  nav.classList.remove('is-open');

  if (restoreFocus) menuButton.focus();
};

menuButton.addEventListener('click', () => {
  if (isMenuOpen()) {
    closeMenu();
    return;
  }

  menuButton.setAttribute('aria-expanded', 'true');
  nav.classList.add('is-open');
});

navLinks.forEach((link) => link.addEventListener('click', () => closeMenu()));

document.addEventListener('click', (event) => {
  if (isMenuOpen() && !header.contains(event.target)) {
    closeMenu();
  }
});

window.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && isMenuOpen()) {
    closeMenu({ restoreFocus: true });
  }
});

desktopNavMedia.addEventListener('change', (event) => {
  if (event.matches) closeMenu();
});

const updateHeaderShadow = () => {
  header.classList.toggle('is-scrolled', window.scrollY > 24);
};

updateHeaderShadow();
window.addEventListener('scroll', updateHeaderShadow, { passive: true });
