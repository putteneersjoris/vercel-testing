
let comments = [];

const VERCEL_API_URL = 'https://vercel-testing-git-main-putteneersjoris-projects.vercel.app/api/add-comment';

function displayComments() {
    const container = document.getElementById('commentsContainer');
    container.innerHTML = comments
        .map(comment => `
            <div class="comment">
                <p>${comment.text}</p>
                <small>${new Date(comment.timestamp).toLocaleString()}</small>
                ${comment.location ? `<div class="location">📍 ${comment.location}</div>` : ''}
            </div>
        `)
        .join('');
}

async function submitComment() {
    const input = document.getElementById('commentInput');
    const comment = input.value;
    
    if (!comment.trim()) return;

    try {
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
        
        comments.unshift({
            text: comment,
            timestamp: new Date(),
            location: data.location
        });
        
        displayComments();
        input.value = '';
        
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
    const commentForm = document.getElementById('commentForm');
    const commentInput = document.getElementById('commentInput');

    if (event.key === 'Tab') {
        event.preventDefault();
        commentForm.classList.remove('hidden');
        commentInput.focus();
    } else if (event.key === 'Escape') {
        commentForm.classList.add('hidden');
        commentInput.value = '';
    }
});

document.addEventListener('DOMContentLoaded', loadComments);
