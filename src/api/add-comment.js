export default async function handler(request, response) {
    // Set CORS headers
    response.setHeader('Access-Control-Allow-Credentials', true);
    response.setHeader('Access-Control-Allow-Origin', '*');
    response.setHeader('Access-Control-Allow-Methods', 'GET,POST,OPTIONS');
    response.setHeader('Access-Control-Allow-Headers', 'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version');

    // Handle preflight
    if (request.method === 'OPTIONS') {
        return response.status(200).end();
    }

    // Log everything for debugging
    console.log('Request method:', request.method);
    console.log('Request body:', request.body);

    try {
        if (request.method === 'POST') {
            const comment = request.body.comment;
            
            // Log the received comment
            console.log('Received comment:', comment);
            
            // Send back the comment for verification
            return response.status(200).json({
                message: 'Comment received successfully',
                receivedComment: comment,
                timestamp: new Date().toISOString()
            });
        }

        return response.status(405).json({ message: 'Method not allowed' });
        
    } catch (error) {
        // Log any errors
        console.error('API Error:', error);
        return response.status(500).json({ 
            message: 'Server error',
            error: error.message 
        });
    }
}
