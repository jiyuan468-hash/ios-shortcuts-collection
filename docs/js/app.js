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

    <div class="steps-container" id="steps-container">
      <div class="detail-section-title" style="margin-bottom:12px">创建步骤</div>
      <ol class="tutorial-steps" id="tutorial-steps"></ol>
    </div>
    <button class="copy-all-btn" id="copy-all-btn" onclick="copyAllSteps()">
      <svg viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
      复制全部步骤
    </button>
    <p style="text-align:center;font-size:12px;color:var(--text2);margin-top:12px">
      复制后打开快捷指令 App &gt; 点击 + 新建快捷指令，粘贴步骤文本<br/>
      每个步骤对应一个快捷指令操作，按顺序添加即可
    </p>
  `;

  showPage('shortcut-page');
}


// ===== Download Shortcut =====
function copyAllSteps() {
  const steps = document.querySelectorAll('#tutorial-steps li');
  const text = Array.from(steps).map((li, i) => (i+1) + '. ' + li.textContent.trim()).join(String.fromCharCode(10));
  navigator.clipboard.writeText(text).then(() => {
    const btn = document.getElementById('copy-all-btn');
    btn.textContent = '✓ 已复制到剪贴板';
    btn.style.background = '#30D158';
    setTimeout(() => {
      btn.innerHTML = '<svg viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg> 复制全部步骤';
      btn.style.background = '';
    }, 2000);
  });
}

function renderTutorialSteps(steps, scName) {
  const container = document.getElementById('tutorial-steps');
  if (!container || !steps || steps.length === 0) {
    if (container) container.innerHTML = '<li>请打开快捷指令 App 手动创建</li>';
    return;
  }
  container.innerHTML = steps.map((step, i) => `
    <li class="tutorial-step">
      <span class="step-num">${i + 1}</span>
      <span class="step-text">${step}</span>
      <button class="copy-step-btn" onclick="copyStep(${i})" title="复制此步骤">
        <svg viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
      </button>
    </li>
  `).join('');
}

function copyStep(index) {
  const steps = document.querySelectorAll('#tutorial-steps li .step-text');
  if (steps[index]) {
    navigator.clipboard.writeText(steps[index].textContent.trim()).then(() => {
      const btn = steps[index].nextElementSibling;
      if (btn) {
        const orig = btn.innerHTML;
        btn.innerHTML = '<svg viewBox="0 0 24 24"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>';
        btn.style.color = '#30D158';
        setTimeout(() => { btn.innerHTML = orig; btn.style.color = ''; }, 1500);
      }
    });
  }
}

function downloadShortcut(catId, shortcutId) {
  // This function is no longer used - replaced by renderTutorialSteps
  const catMap = {
    'daily-life': '日常生活', 'shopping': '购物省钱', 'productivity': '效率办公',
    'lockscreen': '锁屏组件', 'health': '医疗健康', 'content': '内容创作',
    'security': '安全隐私', 'social': '社交通讯', 'system-tools': '系统工具',
    'weather-travel': '出行天气', 'notes-reminders': '笔记提醒', 'battery-save': '省电模式',
    'photo-edit': '图片处理', 'entertainment': '娱乐休闲', 'finance': '记账理财',
    'contacts': '通讯录', 'study': '学习提升', 'travel': '差旅出行',
    'smart-home': '智能家居', 'translate': '翻译工具', 'daily-utils': '日常小工具',
    'media-tools': '媒体工具', 'travel-tools': '出行工具', 'privacy-tools': '隐私安全',
    'home-automation': '家庭自动化'
  };
  const catName = catMap[catId] || catId;
  // Find the shortcut data
  let sc = null;
  let cat = null;
  for (const c of shortcutsData.categories) {
    const found = c.shortcuts.find(s => s.id === shortcutId);
    if (found) { cat = c; sc = found; break; }
  }
  if (!sc) return;
  renderTutorialSteps(sc.steps, sc.name);
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
        <li>查看页面上的步骤说明，理解每个操作的含义</li>
        <li>点击「前往 GitHub」按钮查看详细教程</li>
        <li>在快捷指令 App 中手动创建对应快捷指令</li>
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
