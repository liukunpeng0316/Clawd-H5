const gallery = document.getElementById('gallery');
const pageSize = 48;
let offset = 0;
let loading = false;
let finished = false;

const sentinel = document.createElement('div');
sentinel.className = 'gallery-sentinel';
sentinel.textContent = '正在加载更多作品…';

function workCard(item) {
  const card = document.createElement('article');
  card.className = 'work';

  const image = document.createElement('img');
  image.src = item.gif_url;
  image.alt = `Clawd 作品 ${item.id.slice(0, 8)}`;
  image.loading = 'lazy';

  const actions = document.createElement('div');
  actions.className = 'work-actions';

  const remix = document.createElement('a');
  remix.className = 'work-button secondary';
  remix.href = `/?remix=${encodeURIComponent(item.id)}`;
  remix.textContent = '做同款';

  const download = document.createElement('a');
  download.className = 'work-button';
  download.href = `/files/${encodeURIComponent(item.id)}/clawd.gif?download=1`;
  download.download = `clawd-${item.id.slice(0, 8)}.gif`;
  download.textContent = '下载 GIF';

  actions.append(remix, download);
  card.append(image, actions);
  return card;
}

async function loadMore() {
  if (loading || finished) return;
  loading = true;
  sentinel.classList.remove('hidden');
  try {
    const response = await fetch(`/api/gallery?offset=${offset}&limit=${pageSize}`);
    if (!response.ok) throw new Error();
    const items = await response.json();
    if (offset === 0) gallery.replaceChildren();
    gallery.append(...items.map(workCard));
    offset += items.length;
    finished = items.length < pageSize;
    if (offset === 0) {
      gallery.innerHTML = '<div class="gallery-empty">还没有公开作品。去制作第一个吧 🦀</div>';
      finished = true;
    }
  } catch (_) {
    if (offset === 0) gallery.innerHTML = '<div class="gallery-empty">作品加载失败，请稍后刷新。</div>';
    finished = true;
  } finally {
    loading = false;
    sentinel.classList.toggle('hidden', finished);
  }
}

gallery.after(sentinel);
const observer = new IntersectionObserver((entries) => {
  if (entries.some((entry) => entry.isIntersecting)) loadMore();
}, {rootMargin: '500px'});
observer.observe(sentinel);
loadMore();
