let comments = [];
const VERCEL_API_URL = 'https://vercel-testing-git-main-putteneersjoris-projects.vercel.app/api/add-comment';
let clickCoordinates = null;

function displayComments() {
    document.querySelectorAll('.comment').forEach(el => el.remove());
    
    comments.forEach(comment => {
        const commentEl = document.createElement('div');
        commentEl.className = 'comment';
        commentEl.innerHTML = `
            <p>${comment.text}</p>
            <small>${new Date(comment.timestamp).toLocaleString()}</small>
            ${comment.location ? `<div class="location">📍 ${comment.location}</div>` : ''}
        `;
        
        if (comment.coordinates) {
            commentEl.style.left = `${comment.coordinates.x}px`;
            commentEl.style.top = `${comment.coordinates.y}px`;
        }
        
        document.body.appendChild(commentEl);
    });
}

async function submitComment() {
    const input = document.getElementById('commentInput');
    const comment = input.value;
    
    if (!comment.trim()) return;

    try {
        const response = await fetch(VERCEL_API_URL, {
            method: 'POST',
            body: JSON.stringify({ 
                comment: comment,
                coordinates: clickCoordinates
            }),
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Server response:', data);
        
        comments.unshift({
            text: comment,
            timestamp: new Date(),
            location: data.location,
            coordinates: clickCoordinates
        });
        
        displayComments();
        input.value = '';
        
        document.getElementById('commentForm').classList.add('hidden');
        
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to submit comment. Please try again.');
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

// Keyboard controls
document.addEventListener('keydown', (event) => {
    if (event.key === 'Tab') {
        event.preventDefault();
        const commentForm = document.getElementById('commentForm');
        const commentInput = document.getElementById('commentInput');

        // Get coordinates directly from the event
        clickCoordinates = {
            x: event.pageX,
            y: event.pageY
        };

        // Position the form
        commentForm.style.left = `${event.pageX}px`;
        commentForm.style.top = `${event.pageY}px`;
        
        commentForm.classList.remove('hidden');
        commentInput.focus();
    } else if (event.key === 'Escape') {
        const commentForm = document.getElementById('commentForm');
        const commentInput = document.getElementById('commentInput');
        commentForm.classList.add('hidden');
        commentInput.value = '';
        clickCoordinates = null;
    }
});

document.addEventListener('DOMContentLoaded', loadComments);
