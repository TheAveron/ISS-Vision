// Fetch the current position of the ISS
function fetchCurrentISSPosition() {
    return fetch('/iss-now')
        .then(response => response.json())
        .then(data => {
            console.log(data)
            const lat = parseFloat(data.lat);
            const lon = parseFloat(data.lon);
            return [lat, lon];
        });
}

// Fetch future trajectory of the ISS
function fetchFutureTrajectory(duration) {
    return fetch(`/future-trajectory?duration=${duration}`)
        .then(response => response.json());
}

// Update ISS position and trajectory on the map
function updateISS() {
    fetchCurrentISSPosition()
        .then(currentPosition => {
            // Update ISS marker position
            issMarker.setLatLng(currentPosition);

            // Fetch and draw the future trajectory
            const trajectoryTime = parseFloat(document.getElementById('trajectory-time-slider').value) * 3600;
            if (document.getElementById('toggle-trajectory').checked) {
                fetchFutureTrajectory(trajectoryTime)
                    .then(futurePositions => drawTrajectory(futurePositions))
                    .catch(error => console.error('Error processing future trajectory data:', error));
            }
        })
        .catch(error => console.error('Error fetching ISS data:', error));
}

// Function to draw the trajectory of the ISS on the map
function drawTrajectory(trajectoryData) {
    let trajectoryPoints = [];
    let previousPoint = null;
    let segments = [];
    const colors = ['red', 'green', 'blue']; // Different colors for segments
    let colorIndex = 0;

    trajectoryData.forEach(pos => {
        const currentPoint = [pos.lat, pos.lon];

        if (previousPoint) {
            const deltaLon = Math.abs(currentPoint[1] - previousPoint[1]);

            // Check if the ISS is crossing the International Date Line
            if (deltaLon > 180) {
                segments.push({ points: [...trajectoryPoints], color: colors[colorIndex] });
                trajectoryPoints = [];
                colorIndex = (colorIndex + 1) % colors.length; // Cycle through colors
            }
        }

        trajectoryPoints.push(currentPoint);
        previousPoint = currentPoint;
    });

    // Add the last segment
    segments.push({ points: [...trajectoryPoints], color: colors[colorIndex] });

    // Remove old polylines from the map
    trajectoryPolylines.forEach(polyline => map.removeLayer(polyline));
    trajectoryPolylines = []; // Clear the array

    // Draw the new polylines with changing colors
    segments.forEach(segment => {
        const polyline = L.polyline(segment.points, { color: segment.color, dashArray: '5, 10' });
        polyline.addTo(map);
        trajectoryPolylines.push(polyline);
    });
}
