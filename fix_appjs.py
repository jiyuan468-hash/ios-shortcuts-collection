import re

filePath = 'docs/js/app.js'
with open(filePath, encoding='utf-8') as f:
    content = f.read()

old_pattern = r'function downloadShortcut\(catId, shortcutId\) \{[\s\S]*?window\.location\.href = \'shortcuts://import-shortcut/.*?;\n\}'

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
  // Direct link: Safari opens .shortcut file and prompts to import
  window.location.href = url;
}'''

if re.search(old_pattern, content):
    content = re.sub(old_pattern, new_func, content)
    with open(filePath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Replaced downloadShortcut function successfully')
else:
    print('Could not find old function')
    # Show what's around line 241
    lines = content.split('\n')
    for i in range(238, 260):
        if i < len(lines):
            print(f'{i+1}: {lines[i]}')
