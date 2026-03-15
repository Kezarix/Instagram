// Заглушка под будущее (lazy load, modal, infinite scroll)
console.log("Explore loaded");
document.getElementById('like-btn').addEventListener('click', function () {
    fetch(`/posts/${this.dataset.id}/like/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}'
        }
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById('likes-count').innerText = data.likes_count;
    });
});

/* CREATE COMMENT */
document.getElementById('send-comment').addEventListener('click', function () {
    const text = document.getElementById('comment-text').value;

    if (!text.trim()) return;

    fetch(`/posts/{{ post.id }}/comment/create/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}',
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `text=${encodeURIComponent(text)}`
    })
    .then(() => location.reload());
});

