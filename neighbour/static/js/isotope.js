//
// isotope.js
//

(function() {
  const isotopes = document.querySelectorAll('[data-isotope]');
  const toggles = document.querySelectorAll('[data-filter]');
  const events = ['click'];

  function layout(isotope) {
    const instance = Isotope.data(isotope);

    new imagesLoaded(isotope, () => {
      instance.layout();
    });
  }

  function filter(e, toggle) {
    e.preventDefault();

    const filter = toggle.dataset.filter;
    const target = document.querySelector(toggle.dataset.target);
    const instance = Isotope.data(target);

    instance.arrange({
      filter: filter
    });
  }

  if (isotopes && toggles && Isotope && imagesLoaded) {
    window.onload = () => {

      [].forEach.call(isotopes, isotope => {
        layout(isotope);
      });

      [].forEach.call(toggles, toggle => {
        toggle.addEventListener(events[0], e => {
          filter(e, toggle);
        });
      });
    }
  }
})();
