async function submitComment() {
    const comment = document.getElementById('commentInput').value;
    try {
        const response = await fetch('/api/add-comment', {
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
