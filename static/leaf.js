

String.prototype.initCap = function () {
  return this.toLowerCase().replace(/(?:^|\s)[a-z]/g, function (m) {
    return m.toUpperCase();
  });
};


var map = L.map('map').setView([52, 2], 3);
var clusterGroup = L.markerClusterGroup();
var ShipIcon = L.icon({ iconUrl: '/static/ship.png', iconSize: [27, 40], iconAnchor: [14, 40], popupAnchor: [-3, -76] });
var mapMarkers = {};
var source = new EventSource('/map/live');

// Setup map
L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}', {
  attribution: 'Tiles &copy; Esri &mdash; Source: Esri, DeLorme, NAVTEQ, USGS, Intermap, iPC, NRCAN, Esri Japan, METI, Esri China (Hong Kong), Esri (Thailand), TomTom, 2012'
}).addTo(map);

// L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
//   maxZoom: 17,
//   attribution: '© OpenStreetMap'
// }).addTo(map);


function getShipInformation(s) {
  return `<table>
  <tr><th> Ship Name </th><td> ${s.SHIPNAME.initCap()} (${s.YEAR_BUILT})</td></tr>
  <tr><th> Ship Type </th><td> ${s.TYPE_NAME} </td></tr>
  <tr><th> Last Port </th><td> ${s.LAST_PORT.initCap()} </td></tr>
  <tr><th> Next Port</th><td> ${s.NEXT_PORT_NAME.initCap()} </td></tr>
  <tr><th> Latest ETA</th><td> ${s.ETA_UPDATED} </td></tr>
  </table>`
}


source.addEventListener('message', function (e) {

  eventData = JSON.parse(e.data);
  console.log(eventData);

  if (eventData.SHIPNAME in mapMarkers) {
    console.log("%c Action: Updating ship location", 'background: rgb(146, 242, 255);')
    clusterGroup.removeLayer(mapMarkers[eventData.SHIPNAME]);
  } else {
    console.log("%c Action: Adding new ship", 'background: rgb(255, 244, 146);')
  }

  mapMarkers[eventData.SHIPNAME] = L.marker([Number(eventData.LAT), Number(eventData.LON)], { icon: ShipIcon });
  mapMarkers[eventData.SHIPNAME].bindPopup(getShipInformation(eventData));
  clusterGroup.addLayer(mapMarkers[eventData.SHIPNAME]);


  map.addLayer(clusterGroup);
  clusterGroup.refreshClusters();

}, false);
