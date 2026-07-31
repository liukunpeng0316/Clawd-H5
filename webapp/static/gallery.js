const gallery = document.getElementById('gallery');

function formatTime(value) {
  return new Intl.DateTimeFormat('zh-CN', {month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit'}).format(new Date(value));
}

fetch('/api/gallery?limit=60')
  .then((response) => response.ok ? response.json() : Promise.reject())
  .then((items) => {
    if (!items.length) {
      gallery.innerHTML = '<div class="gallery-empty">还没有公开作品。去制作第一个吧 🦀</div>';
      return;
    }
    gallery.replaceChildren(...items.map((item) => {
      const card = document.createElement('article');
      card.className = 'work';
      const image = document.createElement('img');
      image.src = item.gif_url;
      image.alt = `Clawd 作品 ${item.id.slice(0, 8)}`;
      image.loading = 'lazy';
      const meta = document.createElement('div');
      meta.className = 'work-meta';
      const id = document.createElement('span');
      id.className = 'work-id';
      id.textContent = `#${item.id.slice(0, 8)}`;
      const time = document.createElement('time');
      time.dateTime = item.updated_at;
      time.textContent = formatTime(item.updated_at);
      meta.append(id, time);
      card.append(image, meta);
      return card;
    }));
  })
  .catch(() => { gallery.innerHTML = '<div class="gallery-empty">作品加载失败，请稍后刷新。</div>'; });
