import re

filePath = 'docs/js/app.js'
with open(filePath, encoding='utf-8') as f:
    content = f.read()

old_func = r'function downloadShortcut\(catId, shortcutId\) \{[\s\S]*?window\.location\.href = url;\n\}'

new_func = '''function downloadShortcut(catId, shortcutId) {
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
  const url = 'https://raw.githubusercontent.com/jiyuan468-hash/ios-shortcuts-collection/main/shortcuts/'
    + encodeURIComponent(catName) + '/' + encodeURIComponent(shortcutId) + '.shortcut';
  // Open in new tab - Safari may offer to open with Shortcuts app
  window.open(url, '_blank');
}'''

if re.search(old_func, content):
    content = re.sub(old_func, new_func, content)
    with open(filePath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Updated: using window.open(url, "_blank")')
else:
    print('Could not find pattern, trying alternative...')
    # Fallback: simple string replace
    old = 'window.location.href = url;'
    new = 'window.open(url, "_blank");'
    if old in content:
        content = content.replace(old, new)
        with open(filePath, 'w', encoding='utf-8') as f:
            f.write(content)
        print('Updated via fallback string replace')
    else:
        print('Could not find string to replace')
