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
            
            // Get IP from Vercel request
            const ip = request.headers['x-forwarded-for'] || request.socket.remoteAddress;
            
            // Get location from IP (using free IP API)
            let location = 'Unknown';
            try {
                const ipResponse = await fetch(`http://ip-api.com/json/${ip}`);
                const ipData = await ipResponse.json();
                if (ipData.status === 'success') {
                    location = `${ipData.city}, ${ipData.country}`;
                }
            } catch (error) {
                console.error('Error getting location:', error);
            }

            const octokit = new Octokit({
                auth: process.env.GITHUB_TOKEN
            });

            const { data: fileData } = await octokit.repos.getContent({
                owner: 'putteneersjoris',
                repo: 'vercel-testing',
                path: 'src/data/comments.json'
            });

            const currentContent = JSON.parse(Buffer.from(fileData.content, 'base64').toString());
            
            // Add new comment with IP and location
            currentContent.comments.unshift({
                text: comment,
                timestamp: new Date().toISOString(),
                location: location,
                // Only store partial IP for privacy
                ip: ip.split('.').slice(0, 2).join('.') + '.xxx.xxx'
            });

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
                comment: comment,
                location: location
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
