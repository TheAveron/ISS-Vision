// Fetch the current position of the ISS
function fetchCurrentISSPosition() {
    return fetch('/iss-now')
        .then(response => response.json())
        .then(data => {
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

// Global array to store duplicated ISS markers
let issDuplicateMarkers = [];

function updateISS() {
    iss = document.getElementById('toggle-iss')

    if (!iss.checked) {
        return;
    }

    fetchCurrentISSPosition()
        .then(currentPosition => {
            // Check if currentPosition is valid
            if (!Array.isArray(currentPosition) || currentPosition.length !== 2) {
                console.error('Invalid currentPosition:', currentPosition);
                return;
            }

            const [lat, lon] = currentPosition;

            // Update the main ISS marker position
            issMarker.setLatLng([lat, lon]);

            // Remove any existing duplicated markers from the map
            issDuplicateMarkers.forEach(marker => map.removeLayer(marker));
            issDuplicateMarkers = []; // Clear the array

            // Duplicate the ISS marker position for side maps
            const duplicatedPositions = duplicatePosition([lat, lon]);

            // Create and add new duplicated markers to the map
            duplicatedPositions.forEach(position => {
                const duplicateMarker = L.marker(position, {icon: issIcon}).addTo(map);
                issDuplicateMarkers.push(duplicateMarker);
            });

            // Fetch and draw the future trajectory
            const trajectoryTime = parseFloat(document.getElementById('trajectory-time-slider').value) * 3600;
            if (trajectoryVisible) {
                fetchFutureTrajectory(trajectoryTime)
                    .then(futurePositions => drawTrajectory(futurePositions))
                    .catch(error => console.error('Error processing future trajectory data:', error));
            }
        })
        .catch(error => console.error('Error fetching ISS data:', error));
}

// Function to duplicate the ISS marker position across the map
function duplicatePosition(position) {
    const duplicatedPositions = [];
    const [lat, lon] = position;

    // Add the original position
    duplicatedPositions.push([lat, lon]);

    // Duplicate position with longitude shifts
    if (lon < 180) {
        duplicatedPositions.push([lat, lon + 360]); // Shift to the right
    }
    if (lon > -180) {
        duplicatedPositions.push([lat, lon - 360]); // Shift to the left
    }

    return duplicatedPositions;
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
    // Draw the new polylines with duplicated paths
    segments.forEach(segment => {
        // Duplicate paths to make them appear on side maps
        const duplicatedPaths = duplicatePath(segment.points);

        duplicatedPaths.forEach(path => {
            const polyline = L.polyline(path, { color: segment.color, dashArray: '5, 10' });
            polyline.addTo(map);
            trajectoryPolylines.push(polyline);
        });
    });
}
