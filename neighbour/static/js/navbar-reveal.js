//
// navbar-reveal.js
//

(function() {
  const navbarReveal = document.querySelectorAll('.navbar-reveal');
  const windowEvents = ['load', 'scroll'];

  let windowScroll = window.pageYOffset;

  function revealNavbar(navbar) {
    const currentScroll = window.pageYOffset;
    const navbarOffset = windowScroll >= currentScroll ? '0' : '-100%';
    const navbarCollapse = navbar.querySelector('.navbar-collapse');

    if (!navbarCollapse.classList.contains('show')) {
      navbar.style.transform = `translateY(${navbarOffset})`;
    }

    windowScroll = currentScroll;
  }

  if (navbarReveal) {
    [].forEach.call(navbarReveal, navbar => {
      windowEvents.forEach(e => {
        window.addEventListener(e, () => {
          revealNavbar(navbar);
        });
      });
    });
  }
})();
