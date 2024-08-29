// controls.js

// Toggle ISS marker visibility
document.getElementById('toggle-iss').addEventListener('change', function() {
    if (this.checked) {
        issMarker.addTo(map);
    } else {
        map.removeLayer(issMarker);
    }
});

// Assuming trajectoryPolylines is an array that holds all the trajectory line objects
let trajectoryVisible = true;

document.getElementById('toggle-trajectory').addEventListener('click', () => {
    if (trajectoryVisible) {
        // Hide all trajectory lines
        trajectoryPolylines.forEach(polyline => map.removeLayer(polyline));
        trajectoryVisible = false;
        document.getElementById('toggle-trajectory').innerText = 'Show Trajectory';
        document.getElementById("slider-container").style.display = "none";
    } else {
        // Show all trajectory lines
        trajectoryPolylines.forEach(polyline => polyline.addTo(map));
        trajectoryVisible = true;
        document.getElementById('toggle-trajectory').innerText = 'Hide Trajectory';
        document.getElementById("slider-container").style.display = "block";
    }
});

// Update ISS position and trajectory every 10 seconds
updateISS()
setInterval(updateISS, 10000);

// Handle user input for trajectory time

// Reference to the slider and the display for the current value
const trajectorySlider = document.getElementById('trajectory-time-slider');
const sliderValueDisplay = document.getElementById('slider-value');

function SlideBar_update() {
    sliderValueDisplay.textContent = trajectorySlider.value;
    updateTrajectoryDuration(trajectorySlider.value * 3600); // Convert hours to seconds
}

SlideBar_update()

// Update the display whenever the slider value changes
trajectorySlider.addEventListener('input', function() {
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
