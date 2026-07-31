const gallery = document.getElementById('gallery');
const pageSize = 48;
let loadedCount = 0;
let cursor = null;
let loading = false;
let finished = false;
const ownershipKey = 'clawd-work-tokens';

function ownershipTokens() {
  try {
    const saved = JSON.parse(localStorage.getItem(ownershipKey));
    return saved && typeof saved === 'object' && !Array.isArray(saved) ? saved : {};
  } catch (_) {
    return {};
  }
}

function forgetOwnership(workId) {
  const tokens = ownershipTokens();
  delete tokens[workId];
  if (Object.keys(tokens).length) localStorage.setItem(ownershipKey, JSON.stringify(tokens));
  else localStorage.removeItem(ownershipKey);
  try {
    const current = JSON.parse(localStorage.getItem('clawd-current-work'));
    if (current?.id === workId) localStorage.removeItem('clawd-current-work');
  } catch (_) {}
}

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
  const editToken = ownershipTokens()[item.id];
  if (editToken) {
    const remove = document.createElement('button');
    remove.type = 'button';
    remove.className = 'work-button danger';
    remove.textContent = '删除我的作品';
    remove.addEventListener('click', () => deleteOwnedWork(item, editToken, card, remove));
    actions.append(remove);
  }
  card.append(image, actions);
  return card;
}

async function deleteOwnedWork(item, editToken, card, button) {
  if (!window.confirm('确定删除这个作品吗？删除后无法恢复。')) return;
  button.disabled = true;
  button.textContent = '正在删除…';
  try {
    const response = await fetch(`/api/works/${encodeURIComponent(item.id)}`, {
      method: 'DELETE',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({edit_token: editToken}),
    });
    const data = response.status === 204 ? {} : await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data.detail || '删除失败，请稍后重试');
    forgetOwnership(item.id);
    card.remove();
    loadedCount = Math.max(0, loadedCount - 1);
    if (!gallery.querySelector('.work')) {
      if (finished) gallery.innerHTML = '<div class="gallery-empty">还没有公开作品。去制作第一个吧 🦀</div>';
      else loadMore();
    }
  } catch (error) {
    button.disabled = false;
    button.textContent = '删除我的作品';
    window.alert(error.message);
  }
}

async function loadMore() {
  if (loading || finished) return;
  loading = true;
  sentinel.classList.remove('hidden');
  try {
    const params = new URLSearchParams({limit: String(pageSize)});
    if (cursor) {
      params.set('before_updated_at', cursor.updated_at);
      params.set('before_id', cursor.id);
    }
    const response = await fetch(`/api/gallery-page?${params}`);
    if (!response.ok) throw new Error();
    const data = await response.json();
    const items = data.items;
    if (loadedCount === 0) gallery.replaceChildren();
    gallery.append(...items.map(workCard));
    loadedCount += items.length;
    cursor = data.next_cursor;
    finished = !cursor;
    if (loadedCount === 0) {
      gallery.innerHTML = '<div class="gallery-empty">还没有公开作品。去制作第一个吧 🦀</div>';
      finished = true;
    }
  } catch (_) {
    if (loadedCount === 0) gallery.innerHTML = '<div class="gallery-empty">作品加载失败，请稍后刷新。</div>';
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
