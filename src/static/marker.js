/**
 * Code Source: https://developer.here.com/documentation/examples/maps-js/infobubbles/open-infobubble
 * Creates a new marker and adds it to a group
 * @param {H.map.Group} group       The group holding the new marker
 * @param {H.map.Icon} icon         The icon of the marker
 * @param {H.geo.Point} coordinate  The location of the marker
 * @param {String} html             Data associated with the marker
 */

function addMarkerToGroup(group, icon, coordinate, html) {
  var marker = new H.map.Marker(coordinate, {icon: icon});

  // add custom data to the marker
  marker.setData(html);
  group.addObject(marker);
}

/**
 * Add markers
 * Clicking on a marker opens an infobubble which holds HTML content related to the marker.
 * @param {H.Map} map A HERE Map instance within the application
 */
function addInfoBubble(map) {
  var group = new H.map.Group();

  map.addObject(group);

  // add 'tap' event listener, that opens info bubble, to the group
  group.addEventListener('tap', function (evt) {
    // event target is the marker itself, group is a parent event target
    // for all objects that it contains
    var bubble = new H.ui.InfoBubble(evt.target.getGeometry(), {
      // read custom data
      content: evt.target.getData()
    });
    // show info bubble
    ui.addBubble(bubble);
  }, false);

  // add User Marker
  var userLocation = new H.geo.Point(userCoords.lat, userCoords.lng);
  var userIcon = new H.map.Icon(mapIcons.userIcon);

  addMarkerToGroup(group, userIcon, userLocation,
      '<div class="bubble">Dein Standpunkt</a></div>' +
      '<div><a href="{{ url_for(\'auth.login\') }}"> Buch ablegen </a> </div>');

  // add Book Markers
  var bookLocation1 = new H.geo.Point(53.56, 10.03);
  var bookLocation2 = new H.geo.Point(53.60, 10.03);
  var bookIcon = new H.map.Icon(mapIcons.bookIcon);

  addMarkerToGroup(group, bookIcon, bookLocation1,
      '<div class="bubble"><a href="">Das Kapital</a></div>' +
      '<div>Marx, Karl</div>' + '<div>Sprache: Deutsch</div>' + '<div>Ort: Auf Parkbank</div>');

  addMarkerToGroup(group, bookIcon, bookLocation2,
      '<div class="bubble"><a href="">Das Neinhorn</a></div>' +
      '<div>Kling, Marc-Uwe</div>');
}

// Add to map
addInfoBubble(map);
console.log("markers loaded")