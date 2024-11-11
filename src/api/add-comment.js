import { Octokit } from "@octokit/rest";

export default async function handler(request, response) {
    // CORS headers
    response.setHeader('Access-Control-Allow-Credentials', true);
    response.setHeader('Access-Control-Allow-Origin', '*');
    response.setHeader('Access-Control-Allow-Methods', 'GET,POST,OPTIONS');
    response.setHeader('Access-Control-Allow-Headers', 'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version');

    if (request.method === 'OPTIONS') {
        return response.status(200).end();
    }

    if (request.method === 'POST') {
        try {
            const { comment } = request.body;
            console.log('Received comment:', comment);

            // Initialize Octokit with your GitHub token
            const octokit = new Octokit({
                auth: process.env.GITHUB_TOKEN
            });

            // Get current comments file
            const { data: fileData } = await octokit.repos.getContent({
                owner: 'putteneersjoris',
                repo: 'vercel-testing',
                path: 'src/data/comments.json'
            });

            // Decode and parse current comments
            const currentContent = JSON.parse(Buffer.from(fileData.content, 'base64').toString());
            
            // Add new comment
            currentContent.comments.unshift({
                text: comment,
                timestamp: new Date().toISOString()
            });

            // Update file in repository
            await octokit.repos.createOrUpdateFileContents({
                owner: 'putteneersjoris',
                repo: 'vercel-testing',
                path: 'src/data/comments.json',
                message: 'Add new comment via API',
                content: Buffer.from(JSON.stringify(currentContent, null, 2)).toString('base64'),
                sha: fileData.sha
            });

            return response.status(200).json({ 
                message: 'Comment added successfully',
                comment: comment
            });
        } catch (error) {
            console.error('Error:', error);
            return response.status(500).json({ 
                message: 'Failed to add comment',
                error: error.message 
            });
        }
    }

    return response.status(405).json({ message: 'Method not allowed' });
}
