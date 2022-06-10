// -------------------------------------------------------------------------------------
// Setup variables
// -------------------------------------------------------------------------------------


var map = L.map('map').setView([52, 2], 3);
L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}', {
  attribution: 'Tiles &copy; Esri &mdash; Source: Esri, DeLorme, NAVTEQ, USGS, Intermap, iPC, NRCAN, Esri Japan, METI, Esri China (Hong Kong), Esri (Thailand), TomTom, 2012'
}).addTo(map);

var ShipIcon = L.icon({
  iconUrl: '/static/ship.png',
  iconSize: [27, 40],
  iconAnchor: [14, 40],
  popupAnchor: [-3, -76]
});
var clusterGroup = L.markerClusterGroup();
var mapMarkers = {};


// -------------------------------------------------------------------------------------
// Functions
// -------------------------------------------------------------------------------------


// Convert the ALL UPPERCASE strings received into lowercase, but with the first letter 
// of each word capitalised.
String.prototype.initCap = function () {
  return this.toLowerCase().replace(/(?:^|\s)[a-z]/g, function (m) {
    return m.toUpperCase();
  });
};


// Function to return the content of the popup shown when a ship is clicked on
function getShipInformation(s) {
  text = `
  <tr><th> Ship Name </th><td> ${s.SHIPNAME.initCap()} (${s.YEAR_BUILT})</td></tr>
    <tr><th> Ship Type </th><td> ${s.TYPE_NAME} </td></tr>
    <tr><th> Last Port </th><td> ${s.LAST_PORT.initCap()}, ${s.LAST_PORT_COUNTRY}</td></tr>
    <tr><th> Travelled</th><td> ${s.DISTANCE_TRAVELLED} nmi </td></tr>
    `
  if (s.CURRENT_PORT == "") {
    text += `
      <tr><th> Next Port</th><td> ${s.NEXT_PORT_NAME.initCap()}, ${s.NEXT_PORT_COUNTRY}</td></tr>
      <tr><th> Remaining</th><td> ${s.DISTANCE_TO_GO} nmi</td></tr>
      <tr><th> Latest ETA</th><td> ${s.ETA_CALC} </td></tr>
  `
  } else {
    text += `
  <tr><th> Current Port</th><td> ${s.CURRENT_PORT.initCap()}, ${s.CURRENT_PORT_COUNTRY} </td ></tr >
  `
  }
  return '<table>' + text + '</table>'
}

// Display the data and the action being taken in the console
function log_data_to_console(data) {
  if (data.SHIPNAME in mapMarkers) {
    console.log("%c Action: Updating ship location", 'background: rgb(146, 242, 255);')
  } else {
    console.log("%c Action: Adding new ship", 'background: rgb(255, 244, 146);')
  }
  console.log(data);
}

// Delete any existing marker for this ship.
function remove_marker_if_exists(data) {
  if (data.SHIPNAME in mapMarkers) {
    clusterGroup.removeLayer(mapMarkers[data.SHIPNAME]);
  }
}

// Create a ship marker
function add_marker(data) {
  mapMarkers[data.SHIPNAME] = L.marker([Number(data.LAT), Number(data.LON)], { icon: ShipIcon });
  mapMarkers[data.SHIPNAME].bindPopup(getShipInformation(data));
}

// Add the marker to the clsutergroup, refresh it and then add it to the map
function refresh_map(data) {
  clusterGroup.addLayer(mapMarkers[data.SHIPNAME]);
  map.addLayer(clusterGroup);
  clusterGroup.refreshClusters();
}

// Update the map by adding/removing markers with popups
function process_event(d) {
  log_data_to_console(d)
  remove_marker_if_exists(d)
  add_marker(d)
  refresh_map(d)
}

// -------------------------------------------------------------------------------------
// Main code
// -------------------------------------------------------------------------------------


// Create an event source to poll for ship details from the backend
var source = new EventSource('/map/live');
source.addEventListener('message', function (e) {
  eventData = JSON.parse(e.data);
  process_event(eventData)
}, false);

