// Keep comments in memory during session
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
    
    if (!comment.trim()) return; // Don't submit empty comments

    try {
        const response = await fetch('https://vercel-testing-8k66qiqao-putteneersjoris-projects.vercel.app/api/add-comment', {
            method: 'POST',
            body: JSON.stringify({ comment: comment }),
            headers: {
                'Content-Type': 'application/json',
            }
        });
        const data = await response.json();
        
        // Add comment to local array
        comments.unshift({
            text: comment,
            timestamp: new Date()
        });
        
        // Update display
        displayComments();
        
        // Clear input
        input.value = '';
        
    } catch (error) {
        console.error('Error:', error);
    }
}

async function loadComments() {
    try {
        const response = await fetch('https://raw.githubusercontent.com/putteneersjoris/vercel-testing/main/src/data/comments.json');
        const data = await response.json();
        comments = data.comments;
        displayComments();
    } catch (error) {
        console.error('Error loading comments:', error);
    }
}

// Load comments when page loads
document.addEventListener('DOMContentLoaded', loadComments);










