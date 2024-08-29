// map.js

// Initialize the map
var map = L.map('map').setView([0, 0], 2);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '© OpenStreetMap contributors'
}).addTo(map); 

var issIcon = L.icon({
    iconUrl: 'https://upload.wikimedia.org/wikipedia/commons/d/d0/International_Space_Station.svg', // Replace with an actual ISS icon URL
    iconSize: [50, 50],
    iconAnchor: [25, 25]
});

var issMarker = L.marker([0, 0], {icon: issIcon}).addTo(map);
var trajectoryPolylines = [];
