(() => {
  const button = document.querySelector('.menu-toggle');
  const menu = document.querySelector('.site-nav');
  if (!button || !menu) return;
  button.addEventListener('click', () => {
    const isOpen = button.getAttribute('aria-expanded') === 'true';
    button.setAttribute('aria-expanded', String(!isOpen));
    menu.dataset.open = String(!isOpen);
  });
  menu.addEventListener('click', (event) => {
    if (event.target.closest('a')) {
      button.setAttribute('aria-expanded', 'false');
      menu.dataset.open = 'false';
    }
  });
})();
