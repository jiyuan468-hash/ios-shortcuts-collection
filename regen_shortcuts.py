#!/usr/bin/env python3
"""Generate valid .shortcut files (ZIP bundles with binary plists)."""

import json
import os
import io
import zipfile
import plistlib
from pathlib import Path

ROOT = Path(__file__).parent
DATA_FILE = ROOT / "docs" / "data" / "shortcuts.json"
SHORTCUTS_DIR = ROOT / "shortcuts"

CAT_DIR_MAP = {
    "daily-life": "日常生活",
    "shopping": "购物省钱",
    "productivity": "效率办公",
    "lockscreen": "锁屏组件",
    "health": "医疗健康",
    "content": "内容创作",
    "security": "安全隐私",
    "social": "社交通讯",
    "system-tools": "系统工具",
    "weather-travel": "出行天气",
    "notes-reminders": "笔记提醒",
    "battery-save": "省电模式",
    "photo-edit": "图片处理",
    "entertainment": "娱乐休闲",
    "finance": "记账理财",
    "contacts": "通讯录",
    "study": "学习提升",
    "travel": "差旅出行",
    "smart-home": "智能家居",
    "translate": "翻译工具",
    "daily-utils": "日常小工具",
    "media-tools": "媒体工具",
    "travel-tools": "出行工具",
    "privacy-tools": "隐私安全",
    "home-automation": "家庭自动化",
}


def make_shortcut(name: str, description: str, cat_id: str) -> bytes:
    """Create a valid .shortcut ZIP bundle."""
    workflow_plist = {
        "WFWorkflowActionIDs": ["is.workflow.actions.gettext"],
        "WFWorkflowActions": [
            {
                "WFSerializationType": "WFTextActionText",
                "Value": {"String": f"{name}快捷指令"},
            }
        ],
        "WFWorkflowImportParameters": {},
        "WFWorkflowMinimumClientVersion": "904",
        "WFShortcutsName": name,
        "WFShortcutsDescription": description,
        "WFWorkflowApplicationVersion": "972",
        "WFIsActionGroupable": False,
    }

    info_plist = {
        "CFBundleIdentifier": f"workflow.shortcut.{cat_id}.{name}",
        "DCCShortcutsVersion": {"Build": "972", "Platform": "ios"},
        "DCCWorkflowDictionary": {
            "WFWorkflowDescription": description,
            "WFShortcutsName": name,
        },
    }

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("Info.plist", plistlib.dumps(info_plist))
        zf.writestr("workflow.workflow", plistlib.dumps(workflow_plist))

    return buf.getvalue()


def main():
    with open(DATA_FILE, encoding="utf-8") as f:
        data = json.load(f)

    generated = 0
    for cat in data["categories"]:
        cat_id = cat["id"]
        dir_name = CAT_DIR_MAP.get(cat_id, cat_id)
        cat_dir = SHORTCUTS_DIR / dir_name
        cat_dir.mkdir(parents=True, exist_ok=True)

        for sc in cat.get("shortcuts", []):
            sc_id = sc["id"]
            sc_name = sc.get("name", sc_id)
            sc_desc = sc.get("description", "")
            fp = cat_dir / f"{sc_id}.shortcut"

            bundle = make_shortcut(sc_name, sc_desc, cat_id)
            fp.write_bytes(bundle)
            generated += 1
            print(f"Generated: {dir_name}/{sc_id}.shortcut ({len(bundle)} bytes)")

    print(f"\nTotal generated: {generated}")
    # Verify all are valid ZIPs
    ok = 0
    bad = 0
    for r, dirs, files in os.walk(SHORTCUTS_DIR):
        for fn in files:
            if fn.endswith(".shortcut"):
                fp = os.path.join(r, fn)
                with open(fp, "rb") as f:
                    magic = f.read(4)
                if magic == b"PK\x03\x04":
                    ok += 1
                else:
                    bad += 1
                    print(f"  BAD: {fp}")
    print(f"Valid ZIPs: {ok}, Bad: {bad}")


if __name__ == "__main__":
    main()
