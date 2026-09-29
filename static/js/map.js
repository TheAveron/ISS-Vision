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

var issMarker = L.marker([0, 0], { icon: issIcon }).addTo(map);
var trajectoryPolylines = [];

function saveMapSettings() {
    const userId = document.getElementById('user-id').value;
    if (!userId) return; // settings are only saved for logged-in users

    const mapSettings = {
        userId: userId,
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
    const userId = document.getElementById('user-id').value;
    if (!userId) return; // anonymous visitor: nothing to load

    fetch('/load-map-settings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `user_id=${userId}`,
    })
        .then(response => response.json())
        .then(settings => {
            if (!settings.error) {
                document.getElementById('toggle-iss').checked = settings.toggle_iss;
                document.getElementById('toggle-trajectory').checked = settings.toggle_trajectory;
                document.getElementById('trajectory-time-slider').value = settings.trajectory_time;
                if (settings.toggle_trajectory) {
                    document.getElementById("slider-container").style.display = "block";
                }
                else {
                    document.getElementById("slider-container").style.display = "none";
                }
                map.setZoom(settings.zoom_level);

                // Apply the settings (e.g., show/hide ISS, trajectory based on toggles)
                applySettings(settings);
            }
        })
        .catch(error => console.error('Error loading map settings:', error));
}

// Restore the saved controls and apply them to the Leaflet map
function applySettings(settings) {
    const issCheckbox = document.getElementById('toggle-iss');
    const trajectoryCheckbox = document.getElementById('toggle-trajectory');
    const slider = document.getElementById('trajectory-time-slider');

    issCheckbox.checked = Boolean(settings.toggle_iss);
    trajectoryCheckbox.checked = Boolean(settings.toggle_trajectory);
    slider.value = settings.trajectory_time;
    map.setZoom(settings.zoom_level);

    // ISS icon
    if (!issCheckbox.checked) {
        map.removeLayer(issMarker);
    }

    // Trajectory: keep the state used by controls.js in sync with the checkbox
    if (trajectoryCheckbox.checked) {
        SlideBar_update(); // updates the label and redraws with the saved duration
    } else {
        trajectoryPolylines.forEach(polyline => map.removeLayer(polyline));
        trajectoryVisible = false;
        document.getElementById('slider-container').style.display = 'none';
        document.getElementById('slider-value').textContent = slider.value;
    }
}


// Call this function on page load
document.addEventListener('DOMContentLoaded', loadMapSettings);
