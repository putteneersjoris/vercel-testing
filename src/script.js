let comments = [];
const VERCEL_API_URL = 'https://vercel-testing-git-main-putteneersjoris-projects.vercel.app/api/add-comment';
let currentX = 0;
let currentY = 0;

// Track mouse position
document.addEventListener('mousemove', (e) => {
    currentX = e.clientX;
    currentY = e.clientY;
});

function showCommentSection(x, y) {
    const commentSection = document.getElementById('commentSection');
    commentSection.style.display = 'block';
    commentSection.style.left = `${x}px`;
    commentSection.style.top = `${y}px`;
    
    // Load location-specific comments
    displayComments(x, y);
}

function hideCommentSection() {
    document.getElementById('commentSection').style.display = 'none';
}

function displayComments(x, y) {
    const container = document.getElementById('commentsContainer');
    
    // Filter comments for this location (within 50px radius)
    const nearbyComments = comments.filter(comment => {
        const dx = comment.x - x;
        const dy = comment.y - y;
        return Math.sqrt(dx * dx + dy * dy) < 50;
    });

    container.innerHTML = nearbyComments
        .map(comment => `
            <div class="comment">
                <p>${comment.text}</p>
                <div class="location">Position: (${comment.x}, ${comment.y})</div>
                <div class="timestamp">${new Date(comment.timestamp).toLocaleString()}</div>
            </div>
        `)
        .join('');
}

sync function submitComment() {
    const input = document.getElementById('commentInput');
    const comment = input.value;
    
    if (!comment.trim()) return;

    try {
        const commentData = {
            comment: comment,
            x: currentX,
            y: currentY
        };

        const response = await fetch(VERCEL_API_URL, {
            method: 'POST',
            body: JSON.stringify(commentData),
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Add comment to local array
        comments.unshift({
            text: comment,
            x: currentX,
            y: currentY,
            timestamp: new Date()
        });
        
        // Update display
        displayComments(currentX, currentY);
        
        // Clear input
        input.value = '';
        
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to submit comment. Please try again.');
    }
}



// Handle keyboard events
document.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
        e.preventDefault(); // Prevent default tab behavior
        showCommentSection(currentX, currentY);
    } else if (e.key === 'Escape') {
        hideCommentSection();
    }
});




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










