/**
 * Code Source: https://developer.here.com/documentation/examples/maps-js/infobubbles/open-infobubble
 * Creates a new marker and adds it to a group
 * @param {H.map.Group} group       The group holding the new marker
 * @param {H.geo.Point} coordinate  The location of the marker
 * @param {String} html             Data associated with the marker
 */

function addMarkerToGroup(group, coordinate, html) {
  var icon = new H.map.Icon(mapIcons.bookIcon);
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

  // add Marker
  addMarkerToGroup(group, new H.geo.Point(53.56, 10.03),
      '<div><a href="">Das Kapital</a></div>' +
      '<div>Marx, Karl</div>');

  addMarkerToGroup(group, new H.geo.Point(53.60, 10.03),
      '<div><a href="">Das Neinhorn</a></div>' +
      '<div>Kling, Marc-Uwe</div>');
}

// Add to map
addInfoBubble(map);
console.log("marker loaded")