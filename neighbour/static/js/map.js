//
// map.js
//

(function() {
  const maps = document.querySelectorAll('[data-map]');
  const accessToken = 'pk.eyJ1IjoiZ29vZHRoZW1lcyIsImEiOiJjanU5eHR4N2cybDU5NGVwOHZwNGprb3E0In0.msdw9q16dh8v4azJXUdiXg';

  function init(map) {
    const elementOptions = map.dataset.map ? JSON.parse(map.dataset.map) : {};
    const defaultOptions = {
      container: map,
      style: 'mapbox://styles/mapbox/streets-v11',
      scrollZoom: false,
      interactive: false
    }
    const options = Object.assign(defaultOptions, elementOptions);

    // Get access token
    mapboxgl.accessToken = accessToken;

    // Init map
    new mapboxgl.Map(options);
  }

  if (typeof mapboxgl !== 'undefined' && maps) {
    [].forEach.call(maps, function(map) {
      init(map);
    });
  }
})();
