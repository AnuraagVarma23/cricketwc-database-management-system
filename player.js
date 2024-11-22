// In player.js

function editPlayer(playerId) {
    // Redirect to the edit form page
    window.location.href = `/edit_player_form/${playerId}`;
}

function deletePlayer(playerId) {
    if (confirm("Are you sure you want to delete this player?")) {
        fetch(`/delete_player/${playerId}`, {
            method: 'POST',  // Use POST if DELETE is not working
        })
        .then(response => {
            if (response.ok) {
                location.reload();  // Refresh the page after deletion
            } else {
                throw new Error('Failed to delete player');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to delete player');
        });
    }
}
