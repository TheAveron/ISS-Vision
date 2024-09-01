// Update ISS speed and altitude
function updateISSInfo() {
    fetchCurrentISSPosition()
        .then(currentPosition => {
            const [lat, lon] = currentPosition;
            fetch('/iss-info')
                .then(response => response.json())
                .then(info => {
                    document.getElementById('iss-speed').textContent = `${info.speed.toFixed(2)} km/h`;
                    document.getElementById('iss-altitude').textContent = `${info.altitude.toFixed(2)} km`;
                })
                .catch(error => {
                    console.error('Error fetching ISS info:', error);
                    document.getElementById('iss-speed').textContent = 'N/A';
                    document.getElementById('iss-altitude').textContent = 'N/A';
                });
        })
        .catch(error => console.error('Error fetching ISS info:', error));
}

function displayNextPasses(passes) {
    const nextPassElement = document.getElementById('next-pass');
    nextPassElement.innerHTML = '';

    passes.forEach((pass, index) => {
        const riseTime = new Date(pass.rise_time);
        const setTime = new Date(pass.set_time);

        // Formatting the date and time
        const riseTimeFormatted = riseTime.toLocaleString('en-GB', {
            weekday: 'long', // "Monday"
            year: 'numeric', // "2024"
            month: 'long',   // "August"
            day: 'numeric',  // "26"
            hour: '2-digit', // "07"
            minute: '2-digit', // "24"
            second: '2-digit', // "00"
            hour12: true // 12-hour format
        });

        const setTimeFormatted = setTime.toLocaleString('en-GB', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: true
        });

        const passInfo = document.createElement('p');
        passInfo.innerHTML = `
            <strong>Pass ${index + 1}</strong>:<br>
            Rise Time: ${riseTimeFormatted}<br>
            Set Time: ${setTimeFormatted}
        `;
        nextPassElement.appendChild(passInfo);
    });
}

document.getElementById('predict-pass').addEventListener('click', function () {
    document.getElementById('next-pass').textContent = "Loading...";
    getUserLocation()
        .then(coords => fetchNextPasses(coords.latitude, coords.longitude))
        .then(passes => displayNextPasses(passes))
        .catch(error => {
            console.error('Error getting next passes:', error);
            document.getElementById('next-pass').textContent = 'Could not retrieve the next passes of the ISS.';
        });
});

function getUserLocation() {
    return new Promise((resolve, reject) => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                position => resolve(position.coords),
                error => reject(error)
            );
        } else {
            reject(new Error('Geolocation is not supported by this browser.'));
        }
    });
}

function fetchNextPasses(lat, lon) {
    return fetch(`/next-passes?lat=${lat}&lon=${lon}`)
        .then(response => response.json())
        .catch(error => console.error('Error fetching next passes:', error));
}

// Fetch ISS crew information
function fetchCrewInfo() {
    fetch('/iss-crew')
        .then(response => response.json())
        .then(data => {
            const crewListElement = document.getElementById('iss-crew');
            crewListElement.innerHTML = '';

            if (data.error) {
                crewListElement.innerHTML = '<li>Error loading crew information.</li>';
                return;
            }

            const issCrew = data.crew;

            if (issCrew.length === 0) {
                crewListElement.innerHTML = '<li>No crew members currently aboard the ISS.</li>';
            } else {
                issCrew.forEach(member => {
                    const crewMemberElement = document.createElement('li');
                    crewMemberElement.textContent = `${member.name} (${member.craft})`;
                    crewListElement.appendChild(crewMemberElement);
                });
            }
        })
        .catch(error => {
            console.error('Error fetching ISS crew data:', error);
            document.getElementById('iss-crew').textContent = 'Error loading crew information.';
        });
}

// Initial data fetch
fetchCrewInfo();
updateISSInfo();

// Periodic update for ISS information
setInterval(updateISSInfo, 10000);
