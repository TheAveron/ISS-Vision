// controls.js

// Toggle ISS marker visibility
document.getElementById('toggle-iss').addEventListener('change', function () {
    if (this.checked) {
        updateISS();
    } else {
        map.removeLayer(issMarker);
        issDuplicateMarkers.forEach(marker => map.removeLayer(marker));
    }
});

document.getElementById('toggle-trajectory').addEventListener('change', function () {
    if (!this.checked) {
        disable_trajectory()
    } else {
        enable_trajectory()
    }
});

function enable_trajectory() {
    document.getElementById('toggle-trajectory').innerText = 'Hide Trajectory';
    document.getElementById("slider-container").style.display = "block";
    trajectoryPolylines.forEach(polyline => polyline.addTo(map));
};

function disable_trajectory() {
    document.getElementById('toggle-trajectory').innerText = 'Show Trajectory';
    document.getElementById("slider-container").style.display = "none";
    trajectoryPolylines.forEach(polyline => map.removeLayer(polyline));
};

// Update ISS position and trajectory every 10 seconds
updateISS()
setInterval(updateISS, 10000);

// Handle user input for trajectory time

// Reference to the slider and the display for the current value
const trajectorySlider = document.getElementById('trajectory-time-slider');
const sliderValueDisplay = document.getElementById('slider-value');

function SlideBar_update() {
    sliderValueDisplay.textContent = trajectorySlider.value;
    updateTrajectoryDuration(Math.round(trajectorySlider.value * 3600)); // Convert hours to seconds
}

SlideBar_update()

// Update the display whenever the slider value changes
trajectorySlider.addEventListener('input', function () {
    SlideBar_update()
});

// Function to update the duration for the future trajectory request
function updateTrajectoryDuration(durationInSeconds) {
    fetchFutureTrajectory(durationInSeconds)
        .then(futurePositions => {
            drawTrajectory(futurePositions);
        })
        .catch(error => console.error('Error updating trajectory duration:', error));
}
