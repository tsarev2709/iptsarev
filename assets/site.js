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

const carousel = document.querySelector('[data-carousel]');
if (carousel) {
  const controls = carousel.querySelector('.carousel-controls');
  const tabs = Array.from(carousel.querySelectorAll('[role="tab"]'));
  const panels = tabs.map(tab => document.getElementById(tab.getAttribute('aria-controls')));
  let active = 0;

  function showSlide(index, moveFocus = false) {
    active = (index + tabs.length) % tabs.length;
    tabs.forEach((tab, position) => {
      const selected = position === active;
      tab.setAttribute('aria-selected', String(selected));
      tab.tabIndex = selected ? 0 : -1;
      panels[position].hidden = !selected;
    });
    if (moveFocus) tabs[active].focus();
  }

  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => showSlide(index));
    tab.addEventListener('keydown', event => {
      const targets = { ArrowLeft: index - 1, ArrowRight: index + 1, Home: 0, End: tabs.length - 1 };
      if (!Object.hasOwn(targets, event.key)) return;
      event.preventDefault();
      showSlide(targets[event.key], true);
    });
  });
  carousel.querySelector('[data-carousel-prev]').addEventListener('click', () => showSlide(active - 1));
  carousel.querySelector('[data-carousel-next]').addEventListener('click', () => showSlide(active + 1));
  showSlide(0);
  controls.hidden = false;
}
