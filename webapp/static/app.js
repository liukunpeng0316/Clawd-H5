const $ = (id) => document.getElementById(id);
const promptInput = $('prompt');
const generateButton = $('generate');
const reviseButton = $('revise');
const errorBox = $('error');
let current = null;
let pollTimer = null;

function showError(message) {
  errorBox.textContent = message;
  errorBox.classList.toggle('hidden', !message);
}

function setBusy(busy, status = 'queued', position = null) {
  const previewReady = busy && status === 'exporting' && !!current?.preview;
  generateButton.disabled = busy;
  reviseButton.disabled = busy;
  $('placeholder').classList.toggle('hidden', busy || !!current?.ready);
  $('result').classList.toggle('hidden', !current?.ready && !previewReady);
  $('progress').classList.toggle('hidden', !busy);
  if (!busy) return;
  if (status === 'queued') {
    $('statusTitle').textContent = '正在排队';
    $('statusCopy').textContent = position ? `前面还有 ${Math.max(0, position - 1)} 个任务` : '马上开始生成';
  } else if (status === 'exporting') {
    $('statusTitle').textContent = '图已经画好了';
    $('statusCopy').textContent = '正在快速导出 GIF，可以先看 SVG 预览';
  } else {
    $('statusTitle').textContent = 'AI 正在绘制';
    $('statusCopy').textContent = '正在生成 SVG 动画，请不要关闭页面';
  }
}

function remember(work) {
  localStorage.setItem('clawd-current-work', JSON.stringify(work));
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
  current.ready = true;
  current.preview = false;
  remember(current);
  $('resultGif').src = data.gif_url;
  $('downloadGif').href = data.gif_url;
  $('downloadGif').classList.remove('hidden');
  $('downloadSvg').href = data.svg_url;
  $('revision').classList.remove('hidden');
  setBusy(false);
}

function showPreview(data) {
  current.preview = true;
  remember(current);
  $('resultGif').src = data.svg_url;
  $('downloadSvg').href = data.svg_url;
  $('downloadGif').classList.add('hidden');
  setBusy(true, 'exporting');
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
      current.ready = false;
      setBusy(false);
      showError(data.error || '生成失败，请重试');
      return;
    }
    if (data.status === 'exporting' && data.svg_url) showPreview(data);
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
  setBusy(true);
  try {
    current = await request('/api/works', {method: 'POST', body: JSON.stringify({prompt})});
    remember(current);
    poll();
  } catch (error) {
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
  setBusy(true);
  try {
    await request(`/api/works/${current.id}/revise`, {
      method: 'POST', body: JSON.stringify({prompt, edit_token: current.edit_token}),
    });
    $('revisionPrompt').value = '';
    remember(current);
    poll();
  } catch (error) {
    current.ready = true;
    setBusy(false);
    showError(error.message);
  }
});

try {
  const saved = JSON.parse(localStorage.getItem('clawd-current-work'));
  if (saved?.id && saved?.edit_token) {
    current = saved;
    setBusy(true);
    poll();
  }
} catch (_) {}
