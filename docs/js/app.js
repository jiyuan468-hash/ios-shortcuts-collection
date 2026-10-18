// ===== Data =====
let shortcutsData = null;
let currentView = 'home';
let currentCategory = null;

const DIFFICULTY_COLOR = {
  '简单': '#34C759',
  '中等': '#FF9500',
  '困难': '#FF3B30'
};

// ===== Init =====
async function init() {
  try {
    const res = await fetch('data/shortcuts.json');
    shortcutsData = await res.json();
    renderHome();
    bindEvents();
  } catch (e) {
    console.error('Failed to load data:', e);
    document.getElementById('categories-container').innerHTML =
      '<div class="empty-state"><div class="empty-icon">⚠️</div><div class="empty-title">数据加载失败</div></div>';
  }
}

// ===== Render Home =====
function renderHome(filter = '') {
  const container = document.getElementById('categories-container');
  const noResults = document.getElementById('no-results');
  const nav = document.getElementById('bottom-nav');
  nav.style.display = 'flex';

  let html = '';
  let hasResults = false;

  for (const cat of shortcutsData.categories) {
    const matched = filter
      ? cat.shortcuts.filter(s =>
          s.name.includes(filter) ||
          s.nameEn.toLowerCase().includes(filter.toLowerCase()) ||
          s.description.includes(filter)
        )
      : cat.shortcuts;

    if (filter && matched.length === 0) continue;
    hasResults = true;

    const visible = filter ? matched : cat.shortcuts;

    html += `
      <div class="category-card" data-cat="${cat.id}">
        <div class="category-card-header">
          <div class="category-icon" style="background:${cat.color}22;color:${cat.color}">${cat.icon}</div>
          <div class="category-info">
            <div class="category-name">${cat.name}</div>
            <div class="category-desc">${cat.description}</div>
          </div>
          <div class="category-arrow">
            <svg viewBox="0 0 24 24"><path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/></svg>
          </div>
        </div>
        <div class="shortcut-list">
          ${visible.map(s => renderShortcutItem(s, cat.color, cat.id)).join('')}
        </div>
      </div>
    `;
  }

  container.innerHTML = html;
  noResults.classList.toggle('active', !hasResults && filter !== '');

  container.querySelectorAll('.category-card').forEach(card => {
    card.addEventListener('click', () => {
      openCategory(card.dataset.cat, filter);
    });
  });

  container.querySelectorAll('.shortcut-item').forEach(item => {
    item.addEventListener('click', (e) => {
      e.stopPropagation();
      openShortcut(item.dataset.id, item.dataset.cat);
    });
  });
}

function renderShortcutItem(s, color, catId) {
  const tags = [];
  if (s.requires_ios17) tags.push('<span class="shortcut-tag ios17">iOS 17+</span>');
  if (s.warning) tags.push('<span class="shortcut-tag warning">⚠️ 警告</span>');

  return `
    <div class="shortcut-item" data-id="${s.id}" data-cat="${catId}">
      <div class="shortcut-dot" style="background:${color}"></div>
      <div class="shortcut-info">
        <div class="shortcut-name">${s.name}</div>
        <div class="shortcut-name-en">${s.nameEn}</div>
        <div class="shortcut-meta">
          <span class="shortcut-tag">${s.difficulty}</span>
          ${tags.join('')}
        </div>
      </div>
    </div>
  `;
}

// ===== Open Category =====
function openCategory(catId, filter = '') {
  const cat = shortcutsData.categories.find(c => c.id === catId);
  if (!cat) return;

  currentCategory = cat;
  document.getElementById('cat-page-title').textContent = cat.name;

  const content = document.getElementById('cat-page-content');
  const shortcuts = filter
    ? cat.shortcuts.filter(s => s.name.includes(filter) || s.description.includes(filter))
    : cat.shortcuts;

  content.innerHTML = `
    <div class="cat-hero" style="background:${cat.color}22">
      <div class="cat-icon">${cat.icon}</div>
      <div class="cat-name">${cat.name}</div>
      <div class="cat-desc">${cat.description}</div>
    </div>
    ${shortcuts.map(s => `
      <div class="cat-shortcut-item" data-id="${s.id}">
        <div class="cat-shortcut-top">
          <div class="cat-shortcut-icon" style="background:${cat.color}22">${cat.icon}</div>
          <div class="cat-shortcut-name">${s.name}</div>
        </div>
        <div class="cat-shortcut-desc">${s.description}</div>
      </div>
    `).join('')}
  `;

  content.querySelectorAll('.cat-shortcut-item').forEach(el => {
    el.addEventListener('click', () => openShortcut(el.dataset.id, catId));
  });

  showPage('category-page');
}

// ===== Open Shortcut Detail =====
function openShortcut(shortcutId, catId) {
  // If catId is empty/falsy, search all categories to find the shortcut
  let cat = null;
  let sc = null;
  if (catId) {
    cat = shortcutsData.categories.find(c => c.id === catId);
    sc = cat?.shortcuts.find(s => s.id === shortcutId);
  }
  if (!sc) {
    for (const c of shortcutsData.categories) {
      const found = c.shortcuts.find(s => s.id === shortcutId);
      if (found) { cat = c; sc = found; break; }
    }
  }
  if (!sc) return;

  document.getElementById('sc-page-title').textContent = sc.name;

  const tags = [];
  if (sc.requires_ios17) tags.push('<span class="shortcut-tag ios17">iOS 17+ 需要</span>');
  if (sc.warning) tags.push('<span class="shortcut-tag warning">⚠️ 请谨慎操作</span>');

  const content = document.getElementById('sc-page-content');
  content.innerHTML = `
    <div class="detail-hero" style="background:${cat.color}18">
      <div class="detail-icon">${cat.icon}</div>
      <div class="detail-name">${sc.name}</div>
      <div class="detail-name-en">${sc.nameEn}</div>
      <div class="detail-desc">${sc.description}</div>
      <div style="margin-top:12px;display:flex;gap:8px;justify-content:center;flex-wrap:wrap">
        ${tags.join('')}
        <span class="shortcut-tag">${sc.difficulty}</span>
      </div>
    </div>

    <div class="detail-section">
      <div class="detail-section-title">执行步骤</div>
      <ul class="step-list">
        ${sc.steps.map((step, i) => `
          <li class="step-item">
            <div class="step-num">${i + 1}</div>
            <div class="step-text">${step}</div>
          </li>
        `).join('')}
      </ul>
    </div>

    <div class="detail-section">
      <div class="detail-section-title">详细信息</div>
      <div class="meta-grid">
        <div class="meta-card">
          <div class="meta-label">自动化触发</div>
          <div class="meta-value">${sc.automation || '手动触发'}</div>
        </div>
        <div class="meta-card">
          <div class="meta-label">难度</div>
          <div class="meta-value">${sc.difficulty}</div>
        </div>
      </div>
    </div>

    ${sc.url_schemes ? `
    <div class="detail-section">
      <div class="detail-section-title">URL Scheme</div>
      <div class="meta-grid">
        ${sc.url_schemes.map(u => `
          <div class="meta-card">
            <div class="meta-value" style="font-size:13px;word-break:break-all">${u}</div>
          </div>
        `).join('')}
      </div>
    </div>
    ` : ''}

    ${sc.warning ? `
    <div class="warning-box">
      <div class="warning-box-title">注意</div>
      <div class="warning-box-text">此快捷指令会执行关键操作，请在理解每个步骤后再运行。建议在测试模式下先验证效果。</div>
    </div>
    ` : ''}

    <button class="install-btn" onclick="installShortcut('${cat.id}', '${sc.id}')">
      <svg viewBox="0 0 24 24"><path d="M5 4v2h14V4H5zm0 10h4v6h6v-6h4l-7-7-7 7z"/></svg>
      安装到快捷指令 App
    </button>

    <p style="text-align:center;font-size:12px;color:var(--text2);margin-top:12px">
      点击上方按钮将在快捷指令 App 中打开此指令<br/>
      也可以前往 <a href="https://github.com/jiyuan468-hash/ios-shortcuts-collection" target="_blank" style="color:var(--accent)">GitHub</a> 下载 .shortcut 文件
    </p>
  `;

  showPage('shortcut-page');
}

// ===== Install =====
function installShortcut(catId, shortcutId) {
  const url = `shortcuts://run-shortcut?name=${encodeURIComponent(shortcutId)}`;
  window.location.href = url;
  setTimeout(() => {
    if (document.visibilityState === 'visible') {
      alert('如果快捷指令 App 未打开，请访问 GitHub 仓库下载 .shortcut 文件手动导入：\nhttps://github.com/jiyuan468-hash/ios-shortcuts-collection');
    }
  }, 2000);
}

// ===== Page Navigation =====
function showPage(pageId) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.getElementById('home-view').style.display = 'none';
  if (pageId === 'home-view') {
    document.getElementById('home-view').style.display = 'block';
  } else {
    document.getElementById(pageId).classList.add('active');
  }
  window.scrollTo(0, 0);
}

function goHome() {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.getElementById('home-view').style.display = 'block';
  currentView = 'home';
  updateNav('home');
}

// ===== Events =====
function bindEvents() {
  document.getElementById('cat-back').addEventListener('click', goHome);
  document.getElementById('sc-back').addEventListener('click', goHome);
  document.getElementById('setup-back').addEventListener('click', goHome);

  const searchInput = document.getElementById('search-input');
  let debounceTimer;
  searchInput.addEventListener('input', () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      renderHome(searchInput.value.trim());
    }, 200);
  });

  document.querySelectorAll('.nav-item[data-view]').forEach(btn => {
    btn.addEventListener('click', () => {
      const view = btn.dataset.view;
      if (view === 'home') goHome();
      if (view === 'search') {
        searchInput.focus();
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
      updateNav(view);
    });
  });

  document.getElementById('nav-github').addEventListener('click', () => {
    window.open('https://github.com/jiyuan468-hash/ios-shortcuts-collection', '_blank');
  });

  document.getElementById('open-setup').addEventListener('click', (e) => {
    e.preventDefault();
    renderSetupPage();
    showPage('setup-page');
  });
}

function updateNav(active) {
  document.querySelectorAll('.nav-item[data-view]').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.view === active);
  });
}

// ===== Setup Page =====
function renderSetupPage() {
  document.getElementById('setup-content').innerHTML = `
    <div class="detail-section">
      <div class="detail-section-title">如何安装快捷指令</div>
      <ol style="padding-left:20px;color:var(--text2);line-height:2">
        <li>在 Safari 中打开本页面，点击任意快捷指令</li>
        <li>点击「安装到快捷指令 App」按钮</li>
        <li>系统会跳转到快捷指令 App，点击「添加快捷指令」</li>
        <li>返回桌面，在快捷指令 App 中找到它</li>
      </ol>
    </div>
    <div class="detail-section">
      <div class="detail-section-title">从 GitHub 手动安装</div>
      <ol style="padding-left:20px;color:var(--text2);line-height:2">
        <li>访问 <a href="https://github.com/jiyuan468-hash/ios-shortcuts-collection" target="_blank" style="color:var(--accent)">GitHub 仓库</a></li>
        <li>下载需要的 .shortcut 文件</li>
        <li>通过 AirDrop 或文件 App 发送到 iPhone</li>
        <li>点击文件，选择「快捷指令」打开</li>
      </ol>
    </div>
    <div class="detail-section">
      <div class="detail-section-title">设置自动化</div>
      <ol style="padding-left:20px;color:var(--text2);line-height:2">
        <li>打开快捷指令 App → 点击「自动化」标签</li>
        <li>点击右上角「+」→ 创建个人自动化</li>
        <li>选择触发条件（时间、地点、App 等）</li>
        <li>添加操作 → 搜索并选择对应快捷指令</li>
        <li>关闭「运行前询问」即可自动执行</li>
      </ol>
    </div>
    <div class="detail-section">
      <div class="detail-section-title">常见问题</div>
      <div class="meta-card" style="margin-bottom:10px">
        <div class="meta-label">为什么有些指令显示「困难」？</div>
        <div class="meta-value" style="font-size:14px;color:var(--text2)">需要调用 API 或复杂的数据处理，建议先阅读完整步骤再操作</div>
      </div>
      <div class="meta-card">
        <div class="meta-label">iOS 17+ 是什么？</div>
        <div class="meta-value" style="font-size:14px;color:var(--text2)">锁屏待办等功能需要使用 iOS 17 的 Live Activity 特性，请确保系统已更新</div>
      </div>
    </div>
  `;
}

// ===== Start =====
init();
