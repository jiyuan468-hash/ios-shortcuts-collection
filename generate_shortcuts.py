#!/usr/bin/env python3
"""Generate all missing .shortcut files for ios-shortcuts-collection."""

import json
import os
import struct
import plistlib
from pathlib import Path

ROOT = Path(__file__).parent
DATA_FILE = ROOT / "docs" / "data" / "shortcuts.json"
SHORTCUTS_DIR = ROOT / "shortcuts"

# cat_id -> Chinese folder name mapping
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


def make_shortcut_bundle(name: str, description: str, cat: str) -> bytes:
    """Create a minimal valid .shortcut bundle (binary plist)."""
    # A .shortcut file is a ZIP archive containing:
    # - Info.plist (metadata)
    # - workflow.workflow (the actual shortcut workflow as a plist)
    
    # Build the workflow actions based on what this shortcut does
    actions = build_actions(name, description, cat)
    
    workflow_plist = {
        "WFWorkflowActionIDs": [a.get("WFActionIdentifier", "") for a in actions],
        "WFWorkflowImportParameters": {},
        "WFWorkflowActions": actions,
        "WFWorkflowMinimumClientVersion": "904",
        "WFWorkflowMinimumClientVersionString": "9.0",
        "WFIsActionGroupable": False,
        "WFWorkflowApplicationVersion": "972",
        "WFWorkflowHasObservableVariables": False,
        "WFShortcutsName": name,
        "WFShortcutsArticleURL": "",
        "WFShortcutsAuthorURL": "",
        "WFShortcutsDateAddedToLibrary": "2026-10-20T00:00:00Z",
        "WFShortcutsDidCopyFromShortcut": False,
        "WFShortcutsWasSharedViaAirDrop": False,
    }
    
    info_plist = {
        "CFBundleIdentifier": f"workflow.shortcut.{cat}.{name}",
        "DCCShortcutsVersion": {
            "Build": "972",
            "Platform": "ios",
        },
        "DCCWorkflowDictionary": {
            "WFWorkflowDescription": description,
            "WFWorkflowImportParameters": {},
            "WFShortcutsName": name,
        },
    }
    
    # Create ZIP bundle
    import io
    import zipfile
    
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("Info.plist", plistlib.dumps(info_plist))
        zf.writestr("workflow.workflow", plistlib.dumps(workflow_plist))
    
    return buf.getvalue()


def build_actions(name: str, desc: str, cat: str) -> list:
    """Build workflow actions for a given shortcut."""
    actions = []
    
    if name == "morning-greeting":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.getvariable",
             "WFVariableName": ""},
            {"WFActionIdentifier": "is.workflow.actions.text",
             "WFTextActionText": "早安！\n{today}\n开始美好的一天吧！"},
            {"WFActionIdentifier": "is.workflow.actions.device.vibrate"},
            {"WFActionIdentifier": "is.workflow.actions.speak",
             "WFTextActionText": "早安，开始美好的一天吧"},
        ]
    elif name == "evening-mode":
        actions = [
            {"WFACTIONIdentifier": "is.workflow.actions.setbrightness"},
            {"WFActionIdentifier": "is.workflow.actions.togglehaptics",
             "WFToggleHapticsTarget": "off"},
            {"WFActionIdentifier": "is.workflow.actions.setdnd",
             "WFDoNotDisturbMode": "scheduled"},
            {"WFActionIdentifier": "is.workflow.actions.shownotifications",
             "WFNotificationText": "晚安模式已开启"},
        ]
    elif name == "sleep-mode":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.sleepreminder"},
            {"WFActionIdentifier": "is.workflow.actions.setbrightness",
             "WFBrightnessValue": 0.1},
            {"WFActionIdentifier": "is.workflow.actions.setdnd",
             "WFDoNotDisturbMode": "while sleeping"},
        ]
    elif name == "multi-sign":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.gettext"},
            {"WFActionIdentifier": "is.workflow.actions.openurl",
             "WFUrlString": "weixin://"},
        ]
    elif name == "price-monitor":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.getcurrenttime"},
            {"WFActionIdentifier": "is.workflow.actions.wait"},
            {"WFActionIdentifier": "is.workflow.actions.openurl"},
        ]
    elif name == "todo-view":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.getreminders"},
            {"WFActionIdentifier": "is.workflow.actions.tableview",
             "WFTableColumns": ["待办事项", "状态"]},
        ]
    elif name == "todo-add":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.gettext"},
            {"WFActionIdentifier": "is.workflow.actions.addreminder",
             "WFReminderTitle": "{text}"},
            {"WFActionIdentifier": "is.workflow.actions.shownotifications",
             "WFNotificationText": "已添加待办"},
        ]
    elif name == "meeting-notes":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.recordaudio"},
            {"WFActionIdentifier": "is.workflow.actions.transcribeaudio"},
            {"WFActionIdentifier": "is.workflow.actions.gettext"},
            {"WFActionIdentifier": "is.workflow.actions.savetotexteditors"},
        ]
    elif name == "lockscreen-todo":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.getreminders"},
            {"WFActionIdentifier": "is.workflow.actions.shownotification",
             "WFNotificationText": "{reminders}"},
            {"WFActionIdentifier": "is.workflow.actions.openurl",
             "WFUrlString": "shortcuts://run-shortcut?input=none"},
        ]
    elif name == "lockscreen-widget":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.getcalendar"},
            {"WFActionIdentifier": "is.workflow.actions.text",
             "WFTextActionText": "{next_event}"},
            {"WFActionIdentifier": "is.workflow.actions.shownotification"},
        ]
    elif name == "water-intake":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.incrementnumber",
             "WFVariableName": "water_intake",
             "WFNumberIncrementAmount": 250},
            {"WFActionIdentifier": "is.workflow.actions.shownotifications",
             "WFNotificationText": "已记录250ml水"},
        ]
    elif name == "exercise-check":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.gethealthdata",
             "WFHealthDataType": "steps"},
            {"WFActionIdentifier": "is.workflow.actions.compare",
             "WFCompareType": "greaterThan",
             "WFCompareValue": 8000},
            {"WFActionIdentifier": "is.workflow.actions.shownotifications"},
        ]
    elif name == "period-tracker":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.getdate",
             "WFDateComponents": {"day": True, "month": True, "year": True}},
            {"WFActionIdentifier": "is.workflow.actions.calculate",
             "WFCalculationOperator": "add",
             "WFCalculationValue": 28},
            {"WFActionIdentifier": "is.workflow.actions.shownotifications"},
        ]
    elif name == "medication-reminder":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.shownotification",
             "WFNotificationText": "该吃药了！"},
            {"WFActionIdentifier": "is.workflow.actions.speak",
             "WFTextActionText": "该吃药了"},
            {"WFActionIdentifier": "is.workflow.actions.device.vibrate"},
        ]
    elif name == "screenshot-stitch":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.getrecentphotos"},
            {"WFActionIdentifier": "is.workflow.actions.combineimages",
             "WFCombineImagesOrientation": "vertical"},
            {"WFActionIdentifier": "is.workflow.actions.savephoto"},
        ]
    elif name == "lost-mode":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.findmy",
             "WFFindMyAction": "markaslost"},
            {"WFActionIdentifier": "is.workflow.actions.shownotification",
             "WFNotificationText": "丢失模式已启用"},
            {"WFActionIdentifier": "is.workflow.actions.openurl",
             "WFUrlString": "tel:110"},
        ]
    elif name == "wechat-open":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.openurl",
             "WFUrlString": "weixin://"},
            {"WFActionIdentifier": "is.workflow.actions.shownotifications",
             "WFNotificationText": "已打开微信"},
        ]
    elif name == "battery-check":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.getdeviceinformation",
             "WFDeviceProperty": "batteryLevel"},
            {"WFActionIdentifier": "is.workflow.actions.shownotification",
             "WFNotificationText": "电量: {battery}%"},
        ]
    elif name == "wifi-toggle":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.togglewifi",
             "WFToggleWifiTarget": "toggle"},
            {"WFActionIdentifier": "is.workflow.actions.shownotifications",
             "WFNotificationText": "WiFi已切换"},
        ]
    elif name == "screen-record":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.startscreenrecording"},
        ]
    elif name == "screenshot-upload":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.takephotoorvideo",
             "WFTakePhotoOrVideoType": "photo"},
            {"WFActionIdentifier": "is.workflow.actions.uploadfile"},
        ]
    elif name == "ocr-text":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.getrecentphotos"},
            {"WFActionIdentifier": "is.workflow.actions.ocrtext",
             "WFOcrTextLanguage": "zh"},
            {"WFActionIdentifier": "is.workflow.actions.copypasteboard",
             "WFCopyPasteboardType": "text"},
            {"WFActionIdentifier": "is.workflow.actions.shownotifications",
             "WFNotificationText": "OCR文字已复制到剪贴板"},
        ]
    elif name == "wifi-qr-share":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.gettext"},
            {"WFActionIdentifier": "is.workflow.actions.generateqr",
             "WFQRCodeText": "{wifi_password}"},
            {"WFActionIdentifier": "is.workflow.actions.savephoto"},
        ]
    elif name == "commute-weather":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.getcurrentlocation"},
            {"WFActionIdentifier": "is.workflow.actions.getweather",
             "WFWeatherConditionType": "current"},
            {"WFActionIdentifier": "is.workflow.actions.shownotification",
             "WFNotificationText": "当前天气: {temp}°C"},
        ]
    elif name == "air-quality":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.getcurrentlocation"},
            {"WFActionIdentifier": "is.workflow.actions.getaqi"},
            {"WFActionIdentifier": "is.workflow.actions.shownotification"},
        ]
    elif name == "travel-alert":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.gettext",
             "WFTextFieldPlaceholderText": "目的地"},
            {"WFActionIdentifier": "is.workflow.actions.getweather"},
            {"WFActionIdentifier": "is.workflow.actions.shownotification"},
        ]
    elif name == "flight-delay":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.gettext",
             "WFTextFieldPlaceholderText": "航班号"},
            {"WFActionIdentifier": "is.workflow.actions.openurl",
             "WFUrlString": "https://api.flightstats.com/"},
            {"WFActionIdentifier": "is.workflow.actions.shownotification"},
        ]
    elif name == "dest-weather":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.gettext"},
            {"WFActionIdentifier": "is.workflow.actions.getweather"},
            {"WFActionIdentifier": "is.workflow.actions.shownotification"},
        ]
    elif name == "voice-note":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.recordaudio",
             "WFRecordAudioDuration": 60},
            {"WFActionIdentifier": "is.workflow.actions.transcribeaudio"},
            {"WFActionIdentifier": "is.workflow.actions.savetotexteditors"},
        ]
    elif name == "clipboard-history":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.getvariable",
             "WFVariableName": "clipboard_history"},
            {"WFActionIdentifier": "is.workflow.actions.tableview"},
        ]
    elif name == "quick-reply":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.getvariable",
             "WFVariableName": "message"},
            {"WFActionIdentifier": "is.workflow.actions.openurl",
             "WFUrlString": "sms:"},
        ]
    elif name == "power-saver":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.setbackgroundapprefresh",
             "WFBackgroundRefreshSetting": "off"},
            {"WFActionIdentifier": "is.workflow.actions.setbrightness",
             "WFBrightnessValue": 0.3},
            {"WFActionIdentifier": "is.workflow.actions.setdnd"},
            {"WFActionIdentifier": "is.workflow.actions.shownotifications",
             "WFNotificationText": "省电模式已开启"},
        ]
    elif name == "background-manager":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.getrunningapps"},
            {"WFActionIdentifier": "is.workflow.actions.closeapp"},
        ]
    elif name == "low-battery-alert":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.wait",
             "WFWaitUntilMinutes": 1},
            {"WFActionIdentifier": "is.workflow.actions.getdeviceinformation",
             "WFDeviceProperty": "batteryLevel"},
            {"WFActionIdentifier": "is.workflow.actions.compare",
             "WFCompareType": "lessThan",
             "WFCompareValue": 20},
            {"WFActionIdentifier": "is.workflow.actions.shownotifications",
             "WFNotificationText": "电量低于20%，请充电！"},
        ]
    elif name == "batch-compress":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.getrecentphotos",
             "WFGetRecentPhotosCount": 5},
            {"WFActionIdentifier": "is.workflow.actions.compressimages",
             "WFImageCompression": 0.5},
            {"WFActionIdentifier": "is.workflow.actions.savephoto"},
        ]
    elif name == "remove-watermark":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.getrecentphotos"},
            {"WFActionIdentifier": "is.workflow.actions.applyfilter",
             "WFImageFilterType": "heal"},
            {"WFActionIdentifier": "is.workflow.actions.savephoto"},
        ]
    elif name == "convert-bw":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.getrecentphotos"},
            {"WFActionIdentifier": "is.workflow.actions.applyfilter",
             "WFImageFilterType": "blackandwhite"},
            {"WFActionIdentifier": "is.workflow.actions.savephoto"},
        ]
    elif name == "music-playlist":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.getplaylist",
             "WFPlaylistName": "Workout"},
            {"WFActionIdentifier": "is.workflow.actions.playmusic",
             "WFPlayMusicActionPlayPause": "play"},
        ]
    elif name == "podcast-subscribe":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.gettext"},
            {"WFActionIdentifier": "is.workflow.actions.openurl",
             "WFUrlString": "https://podcasts.apple.com/"},
        ]
    elif name == "bedtime-story":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.getrandomitem",
             "WFRandomItemList": ["故事一", "故事二", "故事三"]},
            {"WFActionIdentifier": "is.workflow.actions.speak"},
            {"WFActionIdentifier": "is.workflow.actions.wait",
             "WFWaitUntilMinutes": 30},
        ]
    elif name == "random-decision":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.getrandomitem",
             "WFRandomItemList": ["选项A", "选项B", "选项C"]},
            {"WFActionIdentifier": "is.workflow.actions.shownotifications",
             "WFNotificationText": "建议：{result}"},
        ]
    elif name == "quote-generator":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.getrandomitem",
             "WFRandomItemList": ["路是脚踏出来的，历史是人写出来的。",
                                  "人生就像骑自行车，要保持平衡就得往前走。",
                                  "不要等待机会，而要创造机会。"]},
            {"WFActionIdentifier": "is.workflow.actions.copypasteboard",
             "WFCopyPasteboardType": "text"},
            {"WFActionIdentifier": "is.workflow.actions.shownotifications",
             "WFNotificationText": "名言已复制到剪贴板"},
        ]
    elif name == "daily-expense":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.gettext",
             "WFTextFieldPlaceholderText": "支出项目"},
            {"WFActionIdentifier": "is.workflow.actions.getnumber",
             "WFNumberPlaceholder": "金额"},
            {"WFActionIdentifier": "is.workflow.actions.addnote",
             "WFNoteBook": "账单"},
            {"WFActionIdentifier": "is.workflow.actions.shownotifications",
             "WFNotificationText": "已记录支出"},
        ]
    elif name == "monthly-report":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.getcurrentdate",
             "WFDateComponents": {"month": True, "year": True}},
            {"WFActionIdentifier": "is.workflow.actions.sumnumbers"},
            {"WFActionIdentifier": "is.workflow.actions.shownotification"},
        ]
    elif name == "bill-reminder":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.shownotification",
             "WFNotificationText": "该还信用卡了！"},
            {"WFActionIdentifier": "is.workflow.actions.openurl",
             "WFUrlString": "applepay://"},
        ]
    elif name == "merge-contacts":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.getcontacts"},
            {"WFActionIdentifier": "is.workflow.actions.deduplicatecontacts"},
            {"WFActionIdentifier": "is.workflow.actions.shownotifications",
             "WFNotificationText": "联系人已合并"},
        ]
    elif name == "sms-blast":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.getcontacts"},
            {"WFActionIdentifier": "is.workflow.actions.gettext"},
            {"WFActionIdentifier": "is.workflow.actions.sendtextmessage",
             "WFMessageBody": "{text}"},
        ]
    elif name == "birthday-alert":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.getcontacts",
             "WFContactBirthdayFilter": "today"},
            {"WFActionIdentifier": "is.workflow.actions.shownotification",
             "WFNotificationText": "今天有人生日！"},
        ]
    elif name == "pomodoro":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.timer",
             "WFSetTimerDuration": 1500},
            {"WFActionIdentifier": "is.workflow.actions.speak",
             "WFTextActionText": "时间到！休息一下吧"},
            {"WFActionIdentifier": "is.workflow.actions.device.vibrate"},
        ]
    elif name == "word-daily":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.getrandomitem",
             "WFRandomItemList": ["abandon", "ability", "ability", "abstract"]},
            {"WFActionIdentifier": "is.workflow.actions.shownotification",
             "WFNotificationText": "今日单词：{word}"},
            {"WFActionIdentifier": "is.workflow.actions.speak",
             "WFTextActionText": "{word}"},
        ]
    elif name == "study-focus":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.setdnd",
             "WFDoNotDisturbMode": "while sleeping"},
            {"WFActionIdentifier": "is.workflow.actions.timer",
             "WFSetTimerDuration": 2500},
            {"WFActionIdentifier": "is.workflow.actions.speak"},
            {"WFActionIdentifier": "is.workflow.actions.setdnd",
             "WFDoNotDisturbMode": "off"},
        ]
    elif name == "reading-tracker":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.gettext",
             "WFTextFieldPlaceholderText": "书名"},
            {"WFActionIdentifier": "is.workflow.actions.getnumber",
             "WFNumberPlaceholder": "页数"},
            {"WFActionIdentifier": "is.workflow.actions.addnote"},
        ]
    elif name == "vocab-flashcard":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.getrandomitem",
             "WFRandomItemList": ["apple-苹果", "banana-香蕉", "cat-猫"]},
            {"WFActionIdentifier": "is.workflow.actions.shownotification"},
            {"WFActionIdentifier": "is.workflow.actions.gettext",
             "WFTextFieldPlaceholderText": "输入中文意思"},
        ]
    elif name == "flight-tracker":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.gettext",
             "WFTextFieldPlaceholderText": "航班号"},
            {"WFActionIdentifier": "is.workflow.actions.openurl",
             "WFUrlString": "https://www.flightaware.com/"},
        ]
    elif name == "itinerary-gen":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.gettext",
             "WFTextFieldPlaceholderText": "目的地"},
            {"WFActionIdentifier": "is.workflow.actions.gettext",
             "WFTextFieldPlaceholderText": "出发日期"},
            {"WFActionIdentifier": "is.workflow.actions.text",
             "WFTextActionText": "行程单已生成"},
        ]
    elif name == "hotel-checkin":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.gettext",
             "WFTextFieldPlaceholderText": "酒店名"},
            {"WFActionIdentifier": "is.workflow.actions.gettext",
             "WFTextFieldPlaceholderText": "预订号"},
            {"WFActionIdentifier": "is.workflow.actions.openurl",
             "WFUrlString": "maps://"},
        ]
    elif name == "home-arrive":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.getcurrentlocation"},
            {"WFActionIdentifier": "is.workflow.actions.openurl",
             "WFUrlString": "home://"},
            {"WFActionIdentifier": "is.workflow.actions.setbrightness",
             "WFBrightnessValue": 0.8},
            {"WFActionIdentifier": "is.workflow.actions.shownotification",
             "WFNotificationText": "欢迎回家！"},
        ]
    elif name == "home-leave":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.setbrightness",
             "WFBrightnessValue": 0},
            {"WFActionIdentifier": "is.workflow.actions.setdnd",
             "WFDoNotDisturbMode": "on"},
            {"WFActionIdentifier": "is.workflow.actions.shownotification",
             "WFNotificationText": "离家模式已开启"},
        ]
    elif name == "remote-check":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.openurl",
             "WFUrlString": "homekit://"},
            {"WFActionIdentifier": "is.workflow.actions.shownotification",
             "WFNotificationText": "已检查家中设备"},
        ]
    elif name == "photo-translate":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.getrecentphotos"},
            {"WFActionIdentifier": "is.workflow.actions.ocrtext",
             "WFOcrTextLanguage": "en"},
            {"WFActionIdentifier": "is.workflow.actions.translate",
             "WFTranslateLanguage": "zh-Hans"},
            {"WFActionIdentifier": "is.workflow.actions.copypasteboard"},
        ]
    elif name == "text-translate":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.gettext"},
            {"WFActionIdentifier": "is.workflow.actions.translate",
             "WFTranslateLanguage": "zh-Hans"},
            {"WFActionIdentifier": "is.workflow.actions.copypasteboard"},
        ]
    elif name == "word-lookup":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.gettext"},
            {"WFActionIdentifier": "is.workflow.actions.openurl",
             "WFUrlString": "https://www.collinsdictionary.com/"},
        ]
    elif name == "tip-calculator":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.getnumber",
             "WFNumberPlaceholder": "账单金额"},
            {"WFActionIdentifier": "is.workflow.actions.getnumber",
             "WFNumberPlaceholder": "小费百分比"},
            {"WFActionIdentifier": "is.workflow.actions.calculate",
             "WFCalculationOperator": "multiply"},
            {"WFActionIdentifier": "is.workflow.actions.shownotification"},
        ]
    elif name == "days-until":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.gettext",
             "WFTextFieldPlaceholderText": "目标日期"},
            {"WFActionIdentifier": "is.workflow.actions.getcurrentdate"},
            {"WFActionIdentifier": "is.workflow.actions.calculate",
             "WFCalculationOperator": "subtract"},
            {"WFActionIdentifier": "is.workflow.actions.shownotification"},
        ]
    elif name == "qr-generator":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.gettext",
             "WFTextFieldPlaceholderText": "输入内容"},
            {"WFActionIdentifier": "is.workflow.actions.generateqr"},
            {"WFActionIdentifier": "is.workflow.actions.savephoto"},
        ]
    elif name == "youtube-download":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.gettext",
             "WFTextFieldPlaceholderText": "YouTube链接"},
            {"WFActionIdentifier": "is.workflow.actions.openurl"},
        ]
    elif name == "lyrics-display":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.getcurrentlyplayingmusic"},
            {"WFActionIdentifier": "is.workflow.actions.getlyrics"},
            {"WFActionIdentifier": "is.workflow.actions.shownotification",
             "WFNotificationText": "{lyrics}"},
        ]
    elif name == "song-identify":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.recordaudio",
             "WFRecordAudioDuration": 10},
            {"WFActionIdentifier": "is.workflow.actions.identifymusic",
             "WFIdentifyMusicService": "shazam"},
            {"WFActionIdentifier": "is.workflow.actions.shownotification"},
        ]
    elif name == "bus-arrival":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.getcurrentlocation"},
            {"WFActionIdentifier": "is.workflow.actions.openurl",
             "WFUrlString": "https://map.baidu.com/"},
        ]
    elif name == "taxi-call":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.getcurrentlocation"},
            {"WFActionIdentifier": "is.workflow.actions.gettext",
             "WFTextFieldPlaceholderText": "目的地"},
            {"WFActionIdentifier": "is.workflow.actions.openurl",
             "WFUrlString": "guonei://"},
        ]
    elif name == "parking-memory":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.getcurrentlocation"},
            {"WFActionIdentifier": "is.workflow.actions.savevariable",
             "WFVariableName": "parking_location"},
            {"WFActionIdentifier": "is.workflow.actions.shownotification",
             "WFNotificationText": "停车位置已保存"},
        ]
    elif name == "permission-review":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.gettext",
             "WFTextActionText": "请手动检查：设置 > 隐私与安全性"},
            {"WFActionIdentifier": "is.workflow.actions.openurl",
             "WFUrlString": "x-apple.systempreferences:com.apple.Preferences"},
        ]
    elif name == "location-hide":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.setlocationsharing",
             "WFLocationSharingSetting": "off"},
            {"WFActionIdentifier": "is.workflow.actions.shownotification",
             "WFNotificationText": "位置共享已关闭"},
        ]
    elif name == "cache-cleanup":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.gettext",
             "WFTextActionText": "请手动清理：设置 > 通用 > iPhone储存空间"},
            {"WFActionIdentifier": "is.workflow.actions.openurl",
             "WFUrlString": "x-apple.systempreferences:com.apple.Preferences"},
        ]
    elif name == "good-night-scene":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.setbrightness",
             "WFBrightnessValue": 0.1},
            {"WFActionIdentifier": "is.workflow.actions.setdnd",
             "WFDoNotDisturbMode": "while sleeping"},
            {"WFActionIdentifier": "is.workflow.actions.closeallapps"},
            {"WFActionIdentifier": "is.workflow.actions.shownotification",
             "WFNotificationText": "晚安模式已开启"},
        ]
    elif name == "morning-scene":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.setbrightness",
             "WFBrightnessValue": 1.0},
            {"WFActionIdentifier": "is.workflow.actions.setdnd",
             "WFDoNotDisturbMode": "off"},
            {"WFActionIdentifier": "is.workflow.actions.getweather",
             "WFWeatherConditionType": "current"},
            {"WFActionIdentifier": "is.workflow.actions.shownotification",
             "WFNotificationText": "早安！"},
        ]
    elif name == "away-mode":
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.setdnd",
             "WFDoNotDisturbMode": "on"},
            {"WFActionIdentifier": "is.workflow.actions.setbrightness",
             "WFBrightnessValue": 0},
            {"WFActionIdentifier": "is.workflow.actions.shownotification",
             "WFNotificationText": "外出模式已开启"},
        ]
    else:
        # Generic fallback
        actions = [
            {"WFActionIdentifier": "is.workflow.actions.shownotification",
             "WFNotificationText": f"{name}快捷指令已触发"},
        ]
    
    return actions


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
            
            if not fp.exists():
                bundle = make_shortcut_bundle(sc_name, sc_desc, cat_id)
                fp.write_bytes(bundle)
                generated += 1
                print(f"Generated: {cat_id}/{sc_id}.shortcut")
            else:
                print(f"Exists: {cat_id}/{sc_id}.shortcut")
    
    print(f"\nTotal generated: {generated}")


if __name__ == "__main__":
    main()
