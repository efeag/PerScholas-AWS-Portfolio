const apiUrl = 'https://YOUR_BACKEND_DOMAIN_OR_IP/posts'; 
 
async function fetchPosts() { 
  const res = await fetch(apiUrl); 
  const posts = await res.json(); 
  const postsDiv = document.getElementById('posts'); 
  postsDiv.innerHTML = posts.map(p => 
    `<div class="post"><h3>${p.title}</h3><p>${p.content}</p></div>` 
  ).join(''); 
} 
 
document.getElementById('postForm').addEventListener('submit', 
async e => { 
  e.preventDefault(); 
  const title = document.getElementById('title').value; 
  const content = document.getElementById('content').value; 
 
  await fetch(apiUrl, { 
    method: 'POST', 
    headers: { 'Content-Type': 'application/json' }, 
    body: JSON.stringify({ title, content }) 
  }); 
  fetchPosts(); 
});
fetchPosts();