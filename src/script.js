let comments = [];

function displayComments() {
    const container = document.getElementById('commentsContainer');
    container.innerHTML = comments
        .map(comment => `
            <div class="comment">
                <p>${comment.text}</p>
                <small>${new Date(comment.timestamp).toLocaleString()}</small>
            </div>
        `)
        .join('');
}

async function submitComment() {
    const input = document.getElementById('commentInput');
    const comment = input.value;
    
    if (!comment.trim()) {
        alert('Please enter a comment');
        return;
    }

    console.log('Submitting comment:', comment); // Debug log

    try {
        const response = await fetch('/api/add-comment', {
            method: 'POST',
            body: JSON.stringify({ comment: comment }),
            headers: {
                'Content-Type': 'application/json',
            }
        });

        console.log('Response status:', response.status); // Debug log
        
        const data = await response.json();
        console.log('Server response:', data); // Debug log

        if (!response.ok) {
            throw new Error(`Server error: ${data.message || 'Unknown error'}`);
        }
        
        // Add comment to local array
        comments.unshift({
            text: comment,
            timestamp: new Date()
        });
        
        // Update display
        displayComments();
        
        // Clear input
        input.value = '';
        alert('Comment added successfully!');
        
    } catch (error) {
        console.error('Full error details:', error);
        alert('Failed to submit comment: ' + error.message);
    }
}
