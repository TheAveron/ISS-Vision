document.getElementById('reminderForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const userId = document.getElementById('user-id').value;
    const passTime = document.getElementById('pass-time').value;

    fetch('/add-reminder', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `user_id=${userId}&pass_time=${passTime}`
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
});
