document.getElementById("reviewForm").addEventListener('submit', async (e) =>{
    e.preventDefault();
    const data = {
        title: document.getElementById('title').value,
        author: document.getElementById('author').value,
        rating: parseInt(document.getElementById('rating').value),
        review: document.getElementById('review').value
    }

    await fetch('/reviews', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    loadReviews();
});

async function loadReviews(){
    const res = await fetch('/reviews');
    const reviews = await res.json();
    const container = document.getElementById('reviews');
    container.innerHTML = "";
    reviews.forEach(r => {
        const div = document.createElement('div');
        div.innerHTML = `<strong>${r.title}</strong> by ${r.author} - Rating: ${r.rating}<br>${r.review}<hr>`;
        container.appendChild(div); 
});
}

loadReviews();