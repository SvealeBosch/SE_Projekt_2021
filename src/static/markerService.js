/**
 * Documentation and Code Snippets:
 * @link {https://developer.here.com/documentation/examples/maps-js/infobubbles/open-infobubble}
 * Creates a new marker and adds it to a group
 * @param {H.map.Group} group       The group holding the new marker
 * @param {H.map.Icon} icon         The icon of the marker
 * @param {H.geo.Point} coordinate  The location of the marker
 * @param {String} html             Data associated with the marker
 */

map.addEventListener('tap', function (evt) {
    console.log(evt.type, evt.currentPointer.type);
    console.log(map.screenToGeo(evt.currentPointer.viewportX, evt.currentPointer.viewportY));
    console.log(userCoords.lat, userCoords.lng);
});

function addContextMenus(map) {
    // set new context menu
    map.addEventListener('contextmenu', function (e) {

        if (e.target != map) {
            return;
        }

        e.items.push(
            new H.util.ContextItem({
                label: 'Setze eigene Position',
                callback: setPosition.bind()
            }),
            H.util.ContextItem.SEPARATOR,
            new H.util.ContextItem({
                label: 'Markiere Buch',
                callback: markBook.bind()
            })
        );
    });
}

function setPosition() {
    console.log('Ich will meine Posistion setzen');
    return;
}

function markBook() {
    console.log('Ich will ein Buch markieren');
    return;
}

function addMarkerToGroup(group, icon, coordinate, html) {
  /**
   * Manually add Markers
   * Method for manual testing purposes, please don't remove
   * @type {H.map.Marker}
   */
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
}

// Add to map
addInfoBubble(map);
addContextMenus(map);
console.log("markers loaded");