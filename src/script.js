async function submitComment() {
    const comment = document.getElementById('commentInput').value;
    // Check if we're on Vercel or GitHub Pages
    const isVercel = window.location.hostname.includes('vercel.app');
    const apiUrl = isVercel ? '/api/add-comment' : 'https://your-project.vercel.app/api/add-comment';

    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            body: JSON.stringify({ comment: comment }),
            headers: {
                'Content-Type': 'application/json',
            }
        });
        const data = await response.json();
        alert(data.message);
    } catch (error) {
        console.error('Error:', error);
    }
}
