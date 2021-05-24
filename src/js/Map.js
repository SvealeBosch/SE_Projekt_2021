
//Step 1: initialize communication with the platform
// Replace variable YOUR_API_KEY with your own apikey
const platform = new H.service.Platform({
  apikey: 'HhbKhQDPxyd4BXse_54NLVZqEXzE5yOxc6wuYiXChNc'
});
const defaultLayers = platform.createDefaultLayers();

//Step 2: initialize a map - this map is centered over Europe
const map = new H.Map(document.getElementById('mapContainer'),
    defaultLayers.vector.normal.map,
    {
      center: {lat: 53.55, lng: 10.00},
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



// Marker code goes here
const LocationOfMarker = { lat: 53.56, lng: 10.03 };

// Create a marker icon from an image URL:
const icon = new H.map.Icon('https://upload.wikimedia.org/wikipedia/commons/5/50/Closed_Book_Icon.svg');

// Create a marker using the previously instantiated icon:
const marker = new H.map.Marker(LocationOfMarker, { icon: icon });

// Add the marker to the map:
map.addObject(marker);

