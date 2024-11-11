async function submitComment() {
    const comment = document.getElementById('commentInput').value;
    const apiUrl = 'https://vercel-testing-8k66qiqao-putteneersjoris-projects.vercel.app/api/add-comment';

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
