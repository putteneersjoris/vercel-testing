let comments = [];
const VERCEL_API_URL = 'https://vercel-testing-git-main-putteneersjoris-projects.vercel.app/api/add-comment';

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
    
    if (!comment.trim()) return;

    try {
        // Use the full Vercel URL for API calls
        const response = await fetch(VERCEL_API_URL, {
            method: 'POST',
            body: JSON.stringify({ comment: comment }),
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Server response:', data);
        
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
        alert('Failed to submit comment. Please try again.');
    }
}

// Load existing comments when page loads
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

document.addEventListener('DOMContentLoaded', loadComments);
