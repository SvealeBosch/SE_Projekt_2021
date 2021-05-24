// Script Source: https://developer.here.com/tutorials/add-a-custom-marker-to-an-interactive-web-map/#creating-a-basic-map

//Step 1: initialize communication with the platform
const platform = new H.service.Platform({
  apikey: hereCredentials.apikey
});

const defaultLayers = platform.createDefaultLayers();

//Step 2: initialize map and set map center
const map = new H.Map(document.getElementById('mapContainer'),
    defaultLayers.vector.normal.map,
    {
      center: new H.geo.Point(mapCenter.lat, mapCenter.lng),
      zoom: 12,
      pixelRatio: window.devicePixelRatio || 1
    }
);

// This adds a resize listener to make sure that the map occupies the whole container
window.addEventListener('resize', () => map.getViewPort().resize());

//Step 3: make the map interactive
// MapEvents enables the event system
// Behavior implements default interactions for pan/zoom (also on mobile touch environments)
const behavior = new H.mapevents.Behavior(new H.mapevents.MapEvents(map));

// Create the default UI components
const ui = H.ui.UI.createDefault(map, defaultLayers);

console.log("Map setup complete");

