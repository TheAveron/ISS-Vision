
function setReminder(riseTime) {
    const userId = document.getElementById('user-id').value;
    if (userId == 'None') {
        alert('You are not connected!');
        return
    };

    fetch('/add-reminder', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `user_id=${userId}&pass_time=${riseTime}`
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                alert('Reminder set successfully!');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function requestNotificationPermission() {
    if ('Notification' in window) {
        Notification.requestPermission().then(function (result) {
            if (result === 'granted') {
                console.log('Notification permission granted.');
            } else {
                console.log('Notification permission denied.');
            }
        });
    }
}
// Call the function to request permission on page load
document.addEventListener('DOMContentLoaded', requestNotificationPermission);

document.addEventListener('DOMContentLoaded', function () {
    // Construct the WebSocket connection URL based on the current window location
    const socket = io.connect(`${window.location.protocol}//${window.location.host}/notifications`);

    socket.on('connect', function () {
        console.log('Connected to WebSocket');
    });

    socket.on('reminder', function (data) {
        console.log('Received reminder:', data);
        const title = "ISS Reminder";
        const body = `The ISS will pass overhead at ${data.pass_time}.`;

        if (Notification.permission === "granted") {
            new Notification(title, { body });
        } else if (Notification.permission !== "denied") {
            Notification.requestPermission().then(permission => {
                if (permission === "granted") {
                    new Notification(title, { body });
                }
            });
        }
    });
});
