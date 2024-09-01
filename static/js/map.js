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

function saveMapSettings() {
    const mapSettings = {
        userId: document.getElementById('user-id').value,
        toggle_iss: document.getElementById('toggle-iss').checked,
        toggle_trajectory: document.getElementById('toggle-trajectory').checked,
        trajectory_time: document.getElementById('trajectory-time-slider').value,
        zoom_level: map.getZoom()
    };

    fetch('/save-map-settings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(mapSettings)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status !== 'success') {
            console.error('Failed to save map settings:', data);
        }
    });
}

// Attach saveMapSettings to relevant events like zoom, toggle, and slider change events
document.getElementById('toggle-iss').addEventListener('change', saveMapSettings);
document.getElementById('toggle-trajectory').addEventListener('change', saveMapSettings);
document.getElementById('trajectory-time-slider').addEventListener('input', saveMapSettings);
map.on('zoomend', saveMapSettings);

function loadMapSettings() {
    fetch('/load-map-settings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `user_id=${document.getElementById('user-id').value}`,
    })
        .then(response => response.json())
        .then(settings => {
            if (!settings.error) {
                document.getElementById('toggle-iss').checked = settings.toggle_iss;
                document.getElementById('toggle-trajectory').checked = settings.toggle_trajectory;
                document.getElementById('trajectory-time-slider').value = settings.trajectory_time;
                map.setZoom(settings.zoom_level);

                // Apply the settings (e.g., show/hide ISS, trajectory based on toggles)
                applySettings(settings);
            }
        })
        .catch(error => console.error('Error loading map settings:', error));
}

function applySettings(settings) {
    // Toggle ISS and trajectory visibility
    toggleVisibility(issMarker, settings.toggle_iss);
    toggleVisibility(trajectoryPath, settings.toggle_trajectory);

    // Adjust trajectory time
    adjustTrajectoryTime(settings.trajectory_time);

    // Set map zoom level
    if (map) {
        map.setZoom(settings.zoom_level);
    }
}

// Generic function to toggle visibility for markers or paths
function toggleVisibility(object, isVisible) {
    if (object) {
        object.setVisible(isVisible);
    }
}

// Adjust the trajectory time based on the saved slider value
function adjustTrajectoryTime(time) {
    fetch(`/future-trajectory?duration=${time}`)
        .then(response => response.json())
        .then(data => {
            if (trajectoryPath) {
                trajectoryPath.setPath(data);
            }
        })
        .catch(error => console.error('Error fetching future trajectory:', error));
}


// Call this function on page load
document.addEventListener('DOMContentLoaded', loadMapSettings);
