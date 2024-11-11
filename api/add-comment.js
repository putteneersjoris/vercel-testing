export default function handler(request, response) {
  if (request.method !== 'POST') {
    return response.status(405).json({ message: 'Method not allowed' });
  }
  
  console.log('Comment received!');
  return response.status(200).json({ message: 'Got your comment!' });
}
