const $ = (id) => document.getElementById(id);
const promptInput = $('prompt');
const generateButton = $('generate');
const reviseButton = $('revise');
const errorBox = $('error');
let current = null;
let pollTimer = null;
let elapsedTimer = null;
let elapsedStartedAt = null;
let remixSource = null;
const ownershipKey = 'clawd-work-tokens';

function ownershipTokens() {
  try {
    const saved = JSON.parse(localStorage.getItem(ownershipKey));
    return saved && typeof saved === 'object' && !Array.isArray(saved) ? saved : {};
  } catch (_) {
    return {};
  }
}

function rememberOwnership(work) {
  if (!work?.id || !work?.edit_token) return;
  const tokens = ownershipTokens();
  tokens[work.id] = work.edit_token;
  localStorage.setItem(ownershipKey, JSON.stringify(tokens));
}

function renderElapsed() {
  if (!elapsedStartedAt) return;
  const seconds = Math.max(0, Math.floor((Date.now() - elapsedStartedAt) / 1000));
  $('elapsed').textContent = `已用时 ${seconds} 秒`;
}

function startElapsed(value = Date.now()) {
  stopElapsed();
  elapsedStartedAt = typeof value === 'number' ? value : Date.parse(value);
  if (!Number.isFinite(elapsedStartedAt)) elapsedStartedAt = Date.now();
  renderElapsed();
  elapsedTimer = setInterval(renderElapsed, 1000);
}

function stopElapsed() {
  if (elapsedTimer) clearInterval(elapsedTimer);
  elapsedTimer = null;
}

function showError(message) {
  errorBox.textContent = message;
  errorBox.classList.toggle('hidden', !message);
}

function setBusy(busy, status = 'queued', position = null) {
  const previewReady = busy && ['export_queued', 'exporting'].includes(status) && !!current?.preview;
  generateButton.disabled = busy;
  reviseButton.disabled = busy;
  $('placeholder').classList.toggle('hidden', busy || !!current?.ready);
  $('result').classList.toggle('hidden', !current?.ready && !previewReady);
  $('progress').classList.toggle('hidden', !busy);
  if (!busy) return;
  if (status === 'queued') {
    $('statusTitle').textContent = '正在排队';
    $('statusCopy').textContent = position ? `前面还有 ${Math.max(0, position - 1)} 个任务` : '马上开始生成';
  } else if (status === 'export_queued') {
    $('statusTitle').textContent = 'SVG 已经画好了';
    $('statusCopy').textContent = '正在等待导出 GIF，可以先看 SVG 预览';
  } else if (status === 'exporting') {
    $('statusTitle').textContent = '图已经画好了';
    $('statusCopy').textContent = '正在导出 GIF，可以先看 SVG 预览';
  } else {
    $('statusTitle').textContent = 'AI 正在绘制';
    $('statusCopy').textContent = '正在生成 SVG 动画，请不要关闭页面';
  }
}

function remember(work) {
  localStorage.setItem('clawd-current-work', JSON.stringify(work));
  rememberOwnership(work);
}

function leaveRemixMode() {
  remixSource = null;
  $('promptHeading').textContent = '你想让 Clawd 做什么？';
  $('prompt').placeholder = '例如：小螃蟹抱着一杯咖啡，困得点头又突然惊醒';
  $('promptHint').textContent = '建议只描述一个角色、一个主要动作。';
  $('remixNotice').classList.add('hidden');
}

async function request(url, options = {}) {
  const response = await fetch(url, {
    ...options,
    headers: {'Content-Type': 'application/json', ...(options.headers || {})},
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.detail || '请求失败，请稍后重试');
  return data;
}

function showResult(data) {
  stopElapsed();
  current.ready = true;
  current.preview = false;
  remember(current);
  $('resultGif').src = data.gif_url;
  $('downloadGif').href = data.gif_url;
  $('downloadGif').classList.remove('hidden');
  $('downloadSvg').href = data.svg_url;
  $('resultActions').classList.remove('hidden');
  $('revision').classList.remove('hidden');
  setBusy(false);
}

function showPreview(data) {
  current.preview = true;
  remember(current);
  $('resultGif').src = data.svg_url;
  $('downloadSvg').href = data.svg_url;
  $('downloadGif').classList.add('hidden');
  $('resultActions').classList.remove('hidden');
  setBusy(true, data.status);
}

async function poll() {
  if (!current) return;
  try {
    const data = await request(`/api/works/${current.id}`);
    if (data.status === 'ready') {
      clearTimeout(pollTimer);
      showResult(data);
      return;
    }
    if (data.status === 'failed') {
      clearTimeout(pollTimer);
      stopElapsed();
      current.ready = false;
      setBusy(false);
      showError(data.error || '生成失败，请重试');
      return;
    }
    if (['export_queued', 'exporting'].includes(data.status) && data.svg_url) showPreview(data);
    setBusy(true, data.status, data.position);
    pollTimer = setTimeout(poll, 2500);
  } catch (error) {
    showError(error.message);
    pollTimer = setTimeout(poll, 5000);
  }
}

generateButton.addEventListener('click', async () => {
  const prompt = promptInput.value.trim();
  if (prompt.length < 2) return showError('请先描述你想制作的表情');
  showError('');
  const startedAt = Date.now();
  startElapsed(startedAt);
  setBusy(true);
  try {
    const url = remixSource ? `/api/works/${encodeURIComponent(remixSource)}/remix` : '/api/works';
    current = await request(url, {method: 'POST', body: JSON.stringify({prompt})});
    current.started_at = new Date(startedAt).toISOString();
    leaveRemixMode();
    remember(current);
    poll();
  } catch (error) {
    stopElapsed();
    current = null;
    setBusy(false);
    showError(error.message);
  }
});

reviseButton.addEventListener('click', async () => {
  const prompt = $('revisionPrompt').value.trim();
  if (!current?.edit_token || prompt.length < 2) return showError('请输入想调整的地方');
  showError('');
  current.ready = false;
  current.started_at = new Date().toISOString();
  startElapsed(current.started_at);
  setBusy(true);
  try {
    await request(`/api/works/${current.id}/revise`, {
      method: 'POST', body: JSON.stringify({prompt, edit_token: current.edit_token}),
    });
    $('revisionPrompt').value = '';
    remember(current);
    poll();
  } catch (error) {
    stopElapsed();
    current.ready = true;
    setBusy(false);
    showError(error.message);
  }
});

async function loadRemix(sourceId) {
  try {
    const data = await request(`/api/works/${encodeURIComponent(sourceId)}`);
    if (data.status !== 'ready' || !data.svg_url) throw new Error('这个原作品暂时无法制作同款');
    remixSource = sourceId;
    $('promptHeading').textContent = '你想在这个基础上改什么？';
    $('prompt').placeholder = '例如：把咖啡换成奶茶，动作再开心一点';
    $('promptHint').textContent = '请填写至少 2 个字，提交后会生成一个独立的新作品。';
    $('remixNotice').classList.remove('hidden');
    $('resultGif').src = data.svg_url;
    $('result').classList.remove('hidden');
    $('resultActions').classList.add('hidden');
    $('placeholder').classList.add('hidden');
  } catch (error) {
    showError(error.message);
  }
}

const remixParam = new URLSearchParams(window.location.search).get('remix');
try {
  rememberOwnership(JSON.parse(localStorage.getItem('clawd-current-work')));
} catch (_) {}
if (remixParam) {
  loadRemix(remixParam);
} else {
  try {
    const saved = JSON.parse(localStorage.getItem('clawd-current-work'));
    if (saved?.id && saved?.edit_token) {
      current = saved;
      startElapsed(saved.started_at || Date.now());
      setBusy(true);
      poll();
    }
  } catch (_) {}
}
