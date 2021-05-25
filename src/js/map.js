// Script Source: https://developer.here.com/tutorials/add-a-custom-marker-to-an-interactive-web-map/#creating-a-basic-map

// 1: Initialize communication with the platform
const platform = new H.service.Platform({
  apikey: hereCredentials.apikey
});

const defaultLayers = platform.createDefaultLayers();

// 2: Get User Location
var geocoder = platform.getSearchService();
if(navigator.geolocation) {
  navigator.geolocation.watchPosition(position => {
    geocoder.reverseGeocode(
        {
          limit: 1,
          at: position.coords.latitude + "," + position.coords.longitude
        }, data => {
          userCoords.lat = position.coords.latitude;
          userCoords.lng = position.coords.longitude;
          mapCenter.lat = userCoords.lat;
          mapCenter.lng = userCoords.lng;
          console.log("The nearest address to your location is:\n" + data.items[0].address.label);
        }, error => {
          console.error(error);
        }
    );
  });
} else {
  console.error("Geolocation is not supported by this browser!");
}

// 3: Initialize map and set map center
const map = new H.Map(document.getElementById('mapContainer'),
    defaultLayers.vector.normal.map,
    {
      center: new H.geo.Point(mapCenter.lat, mapCenter.lng),
      zoom: 12,
      pixelRatio: window.devicePixelRatio || 1
    }
);

// 4: Add a resize listener to make sure that the map occupies the whole container
window.addEventListener('resize', () => map.getViewPort().resize());

// 5: Make the map interactive
// MapEvents enables the event system
// Behavior implements default interactions for pan/zoom (also on mobile touch environments)
const behavior = new H.mapevents.Behavior(new H.mapevents.MapEvents(map));

// Create the default UI components
const ui = H.ui.UI.createDefault(map, defaultLayers);


console.log("Map setup complete");

