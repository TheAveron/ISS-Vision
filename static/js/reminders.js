
function setReminder(riseTime) {
    const userId = document.getElementById('user-id').value;

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
