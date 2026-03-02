# ================= LIFEOS ULTRA MAX + GOD MODE + EXTENSIONS 2026 =================
# Финальная объединённая версия — твой код + все крупные улучшения в одном файле
import json
import os
import threading
import random
import requests
import base64
import matplotlib.pyplot as plt
import pyttsx3
import speech_recognition as sr
import pandas as pd
from datetime import datetime
from cryptography.fernet import Fernet
from plyer import notification
from openai import OpenAI
from kivy.config import Config
Config.set('graphics', 'multisamples', '0')
Config.set('graphics', 'maxfps', '60')
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.camera import Camera
from kivy.uix.popup import Popup
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.snackbar import Snackbar
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.properties import StringProperty, NumericProperty
# ---------------- CONFIG ----------------
API_KEY = "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"
client = OpenAI(api_key=API_KEY, base_url="https://openrouter.ai/api/v1")
Window.size = (360, 640)
CLOUD_URL = "https://example.com/save"
# Мультиязычность
TRANSLATIONS = {
    'ru': {
        'title': 'LIFEOS ULTRA MAX',
        'username': 'Имя пользователя',
        'password': 'Пароль',
        'login': 'Войти / Создать',
        'voice_login': 'Голосовой вход',
        'ai': 'AI',
        'goals': 'Цели',
        'habits': 'Привычки',
        'focus': 'Фокус',
        'mood': 'Настроение',
        'stats': 'Статистика',
        'shop': 'Магазин',
        'friends': 'Друзья',
        'leader': 'Лидеры',
        'settings': 'Настройки',
        'send': 'Отправить',
        'voice': 'Голос',
        'plan': 'План жизни',
        'add_goal': 'Добавить цель',
        'new_goal_hint': 'Новая цель',
        'add_habit': 'Добавить привычку',
        'new_habit_hint': 'Новая привычка',
        'start_pomo': 'Старт Pomodoro',
        'stop_pomo': 'Стоп',
        'save_mood': 'Записать настроение',
        'mood_prompt': 'Как дела сегодня? (1–10)',
        'mood_note': 'Что чувствуешь? (не обязательно)',
        'show_dash': 'Показать дашборд',
        'ai_analysis': 'Анализ от AI',
        'fin_forecast': 'Финансовый прогноз',
        'change_lang': 'Сменить язык',
        'change_theme': 'Сменить тему',
        'backup': 'Создать бэкап',
        'export_ics': 'Экспорт в календарь (.ics)',
        'coins': 'монет',
        'premium_dark': 'Премиум Тёмная',
        'premium_light': 'Премиум Светлая',
        'premium_blue': 'Премиум Синяя',
        'buy': 'Купить',
    },
    'en': {
        'title': 'LIFEOS ULTRA MAX',
        'username': 'Username',
        'password': 'Password',
        'login': 'Login / Create',
        'voice_login': 'Voice Login',
        'ai': 'AI',
        'goals': 'Goals',
        'habits': 'Habits',
        'focus': 'Focus',
        'mood': 'Mood',
        'stats': 'Stats',
        'shop': 'Shop',
        'friends': 'Friends',
        'leader': 'Leaders',
        'settings': 'Settings',
        'send': 'Send',
        'voice': 'Voice',
        'plan': 'Life Plan',
        'add_goal': 'Add Goal',
        'new_goal_hint': 'New Goal',
        'add_habit': 'Add Habit',
        'new_habit_hint': 'New Habit',
        'start_pomo': 'Start Pomodoro',
        'stop_pomo': 'Stop',
        'save_mood': 'Save Mood',
        'mood_prompt': 'How are you today? (1–10)',
        'mood_note': 'How do you feel? (optional)',
        'show_dash': 'Show Dashboard',
        'ai_analysis': 'AI Analysis',
        'fin_forecast': 'Finance Forecast',
        'change_lang': 'Change Language',
        'change_theme': 'Change Theme',
        'backup': 'Create Backup',
        'export_ics': 'Export to Calendar (.ics)',
        'coins': 'coins',
        'premium_dark': 'Premium Dark',
        'premium_light': 'Premium Light',
        'premium_blue': 'Premium Blue',
        'buy': 'Buy',
    }
}
CURRENT_LANG = 'ru'
def _(key):
    return TRANSLATIONS.get(CURRENT_LANG, TRANSLATIONS['ru']).get(key, key)
# ---------------- SECURITY & DATA ----------------
KEY_FILE = "secret.key"
DATA_FILE = "users_secure.json"
if not os.path.exists(KEY_FILE):
    key = Fernet.generate_key()
    open(KEY_FILE, "wb").write(key)
else:
    key = open(KEY_FILE, "rb").read()
fernet = Fernet(key)
current_user = None
def load_users():
    try:
        data = open(DATA_FILE, "rb").read()
        return json.loads(fernet.decrypt(data).decode())
    except:
        return {}
def save_users(data):
    open(DATA_FILE, "wb").write(fernet.encrypt(json.dumps(data).encode()))
    threading.Thread(target=lambda: requests.post(CLOUD_URL, json=data, timeout=3), daemon=True).start()
users = load_users()
# ---------------- AI & VOICE ----------------
engine = pyttsx3.init()
recognizer = sr.Recognizer()
def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except:
        pass
def listen_voice():
    try:
        with sr.Microphone() as source:
            audio = recognizer.listen(source, timeout=5)
            lang = "ru-RU" if CURRENT_LANG == 'ru' else "en-US"
            return recognizer.recognize_google(audio, language=lang)
    except:
        return ""
def ask_ai(prompt):
    try:
        messages = [
            {"role": "system", "content": "Ты LIFEOS AI — очень мотивирующий и поддерживающий помощник. Отвечай на русском, кратко, энергично и по делу." if CURRENT_LANG == 'ru' else "You are LIFEOS AI — very motivational assistant. Answer in English, short, energetic and to the point."},
            {"role": "user", "content": prompt}
        ]
        response = client.chat.completions.create(
            model="meta-llama/llama-3-70b-instruct",
            messages=messages,
            temperature=0.75,
            max_tokens=600,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"AI error: {str(e)[:80]}"
# ---------------- GAMIFICATION ----------------
def add_xp(amount=10):
    if not current_user: return
    u = users[current_user]
    u.setdefault("xp", 0)
    u.setdefault("level", 1)
    u["xp"] += amount
    threshold = 100 * u["level"]
    if u["xp"] >= threshold:
        u["xp"] -= threshold
        u["level"] += 1
        notification.notify(title="LEVEL UP!", message=f"Level {u['level']} 🔥")
        add_coins(50)
    save_users(users)
def add_coins(amount):
    if not current_user: return
    u = users[current_user]
    u.setdefault("coins", 0)
    u["coins"] += amount
    save_users(users)
# ---------------- HABITS + PHOTO ----------------
def add_habit(name):
    if not current_user: return
    u = users[current_user]
    u.setdefault("habits", [])
    u["habits"].append({"name": name, "streak": 0, "last": None, "proof": None})
    save_users(users)
def mark_habit_done(index, photo_b64=None):
    if not current_user: return
    u = users[current_user]
    try:
        h = u["habits"][index]
        today = datetime.now().date().isoformat()
        if h.get("last") != today:
            h["streak"] = h.get("streak", 0) + 1
            h["last"] = today
            if photo_b64:
                h["proof"] = photo_b64
            add_xp(15)
            notification.notify(title="Привычка выполнена!", message=f"{h['name']} — streak {h['streak']}")
        save_users(users)
    except:
        pass
# ---------------- PHOTO PROOF ----------------
def show_camera_popup(callback):
    content = BoxLayout(orientation='vertical')
    cam = Camera(play=True, resolution=(320, 240))
    content.add_widget(cam)
    btn = MDFlatButton(text="Сделать фото", on_release=lambda _: capture(cam, callback))
    content.add_widget(btn)
    popup = Popup(title="Фото-доказательство", content=content, size_hint=(0.9, 0.7))
    popup.open()
def capture(cam, callback):
    if cam.texture:
        b64 = base64.b64encode(cam.export_to_png()).decode('utf-8')
        callback(b64)
    cam.play = False
# ---------------- POMODORO ----------------
pomodoro_time_left = 0
pomodoro_active = False
def pomodoro_start(minutes):
    global pomodoro_time_left, pomodoro_active
    pomodoro_time_left = minutes * 60
    pomodoro_active = True
    Clock.schedule_interval(pomodoro_tick, 1)
def pomodoro_tick(dt):
    global pomodoro_time_left, pomodoro_active
    if not pomodoro_active: return False
    pomodoro_time_left -= 1
    if pomodoro_time_left <= 0:
        pomodoro_active = False
        add_xp(40)
        notification.notify(title="Pomodoro", message="Сессия завершена! +40 XP")
        return False
    return True
def pomodoro_stop():
    global pomodoro_active
    pomodoro_active = False
# ---------------- SHOP & THEMES ----------------
SHOP_ITEMS = [
    {"key": "premium_dark", "name": "premium_dark", "cost": 200, "style": "Dark", "palette": "Gray"},
    {"key": "premium_light", "name": "premium_light", "cost": 250, "style": "Light", "palette": "Amber"},
    {"key": "premium_blue", "name": "premium_blue", "cost": 300, "style": "Dark", "palette": "Blue"},
]
def buy_premium(item):
    if not current_user: return
    u = users[current_user]
    if u.get("coins", 0) >= item["cost"]:
        u["coins"] -= item["cost"]
        MDApp.get_running_app().theme_cls.theme_style = item["style"]
        MDApp.get_running_app().theme_cls.primary_palette = item["palette"]
        Snackbar(text=f"Куплено: {_(item['name'])}").open()
    else:
        Snackbar(text="Недостаточно монет").open()
    save_users(users)
# ---------------- ICS EXPORT ----------------
def export_ics():
    if not current_user: return
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//LIFEOS//EN"]
    for g in users[current_user].get("goals", []):
        dt = datetime.now()
        lines += [
            "BEGIN:VEVENT",
            f"UID:{dt.timestamp()}-{g[:20]}",
            f"DTSTAMP:{dt.strftime('%Y%m%dT%H%M%SZ')}",
            f"DTSTART:{dt.strftime('%Y%m%dT%H%M%SZ')}",
            f"SUMMARY:{g}",
            "END:VEVENT"
        ]
    lines.append("END:VCALENDAR")
    try:
        with open("lifeos_goals.ics", "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        Snackbar(text="Экспорт завершён → lifeos_goals.ics").open()
    except Exception as e:
        Snackbar(text=f"Ошибка экспорта: {str(e)}").open()
# ---------------- KV ----------------
KV = '''
#:import dp kivy.metrics.dp
ScreenManager:
    LoginScreen:
    MainScreen:
<LoginScreen@Screen>:
    name: 'login'
    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(32)
        spacing: dp(16)
        MDLabel:
            text: app._('title')
            halign: 'center'
            font_style: 'H4'
        MDTextField:
            id: username
            hint_text: app._('username')
        MDTextField:
            id: password
            hint_text: app._('password')
            password: True
        MDRaisedButton:
            text: app._('login')
            on_release: root.do_login()
        MDRaisedButton:
            text: app._('voice_login')
            on_release: root.voice_login()
<MainScreen@Screen>:
    name: 'main'
    MDBottomNavigation:
        MDBottomNavigationItem:
            name: 'ai'
            text: app._('ai')
            icon: 'robot'
            MDBoxLayout:
                orientation: 'vertical'
                ScrollView:
                    MDBoxLayout:
                        id: chat_messages
                        orientation: 'vertical'
                        size_hint_y: None
                        height: self.minimum_height
                        padding: dp(8)
                        spacing: dp(4)
                MDTextField:
                    id: chat_input
                    hint_text: "Сообщение..."
                MDBoxLayout:
                    spacing: dp(8)
                    MDRaisedButton:
                        text: app._('send')
                        on_release: root.send_ai_message()
                    MDRaisedButton:
                        text: app._('voice')
                        on_release: root.voice_message()
                    MDRaisedButton:
                        text: app._('plan')
                        on_release: root.show_life_plan()
        MDBottomNavigationItem:
            name: 'goals'
            text: app._('goals')
            icon: 'target'
            MDBoxLayout:
                orientation: 'vertical'
                ScrollView:
                    MDLabel:
                        id: goals_list
                        size_hint_y: None
                        height: self.texture_size[1]
                MDTextField:
                    id: new_goal
                    hint_text: app._('new_goal_hint')
                MDRaisedButton:
                    text: app._('add_goal')
                    on_release: root.add_new_goal()
        MDBottomNavigationItem:
            name: 'habits'
            text: app._('habits')
            icon: 'calendar-check'
            MDBoxLayout:
                orientation: 'vertical'
                RecycleView:
                    id: habits_rv
                    viewclass: 'HabitItem'
                    RecycleBoxLayout:
                        default_size: None, dp(72)
                        default_size_hint: 1, None
                        size_hint_y: None
                        height: self.minimum_height
                        orientation: 'vertical'
                MDTextField:
                    id: new_habit
                    hint_text: app._('new_habit_hint')
                MDRaisedButton:
                    text: app._('add_habit')
                    on_release: root.add_new_habit()
        MDBottomNavigationItem:
            name: 'focus'
            text: app._('focus')
            icon: 'timer'
            MDBoxLayout:
                orientation: 'vertical'
                padding: dp(16)
                MDLabel:
                    id: pomodoro_display
                    text: "25:00"
                    halign: 'center'
                    font_style: 'H4'
                MDSlider:
                    id: pomodoro_slider
                    min: 5
                    max: 60
                    value: 25
                MDRaisedButton:
                    text: app._('start_pomo')
                    on_release: root.start_pomodoro()
                MDRaisedButton:
                    text: app._('stop_pomo')
                    on_release: root.stop_pomodoro()
        MDBottomNavigationItem:
            name: 'mood'
            text: app._('mood')
            icon: 'emoticon'
            MDBoxLayout:
                orientation: 'vertical'
                padding: dp(16)
                MDLabel:
                    text: app._('mood_prompt')
                MDSlider:
                    id: mood_value
                    min: 1
                    max: 10
                    value: 5
                MDTextField:
                    id: mood_note
                    hint_text: app._('mood_note')
                MDRaisedButton:
                    text: app._('save_mood')
                    on_release: root.save_mood()
        MDBottomNavigationItem:
            name: 'stats'
            text: app._('stats')
            icon: 'chart-bar'
            MDBoxLayout:
                orientation: 'vertical'
                padding: dp(16)
                spacing: dp(12)
                MDRaisedButton:
                    text: app._('show_dash')
                    on_release: root.show_stats()
                MDRaisedButton:
                    text: app._('ai_analysis')
                    on_release: root.ai_analysis()
                MDRaisedButton:
                    text: app._('fin_forecast')
                    on_release: root.fin_forecast()
        MDBottomNavigationItem:
            name: 'shop'
            text: app._('shop')
            icon: 'cart'
            ScrollView:
                MDBoxLayout:
                    id: shop_container
                    orientation: 'vertical'
                    size_hint_y: None
                    height: self.minimum_height
                    padding: dp(8)
                    spacing: dp(8)
        MDBottomNavigationItem:
            name: 'leader'
            text: app._('leader')
            icon: 'trophy'
            MDLabel:
                id: leaderboard_text
                text: ""
                halign: 'center'
                valign: 'top'
                size_hint_y: None
                height: self.texture_size[1]
        MDBottomNavigationItem:
            name: 'settings'
            text: app._('settings')
            icon: 'cog'
            MDBoxLayout:
                orientation: 'vertical'
                padding: dp(16)
                spacing: dp(12)
                MDRaisedButton:
                    text: app._('change_lang')
                    on_release: root.change_language_dialog()
                MDRaisedButton:
                    text: app._('backup')
                    on_release: root.create_backup()
                MDRaisedButton:
                    text: app._('export_ics')
                    on_release: root.export_to_ics()
<HabitItem@OneLineAvatarIconListItem>:
    text: root.hname
    secondary_text: f"Streak: {root.streak}"
    _index: 0
    MDRaisedButton:
        text: "✓"
        pos_hint: {'right':1}
        on_release: app.root.current_screen.mark_done(root._index)
    MDRaisedButton:
        text: "📸"
        pos_hint: {'right':0.75}
        on_release: app.root.current_screen.take_photo_proof(root._index)
'''
class HabitItem(OneLineAvatarIconListItem):
    hname = StringProperty()
    streak = NumericProperty(0)
    _index = NumericProperty(0)
class LoginScreen(Screen):
    def do_login(self):
        global current_user
        username = self.ids.username.text.strip()
        password = self.ids.password.text.strip()
        if not username:
            Snackbar(text="Введите имя").open()
            return
        if username not in users:
            users[username] = {
                "password": password,
                "goals": [],
                "money": [],
                "habits": [],
                "mood": [],
                "level": 1,
                "xp": 0,
                "coins": 0,
                "achievements": [],
                "friends": [],
                "chat": []
            }
            save_users(users)
        if users[username]["password"] != password:
            Snackbar(text="Неверный пароль").open()
            return
        current_user = username
        self.manager.current = 'main'
    def voice_login(self):
        text = listen_voice()
        if text:
            self.ids.username.text = text.strip()
            Snackbar(text="Голос распознан — нажми войти").open()
class MainScreen(Screen):
    def on_enter(self):
        Clock.schedule_interval(self.update_pomodoro_display, 0.4)
        self.refresh_ui()
    def refresh_ui(self):
        if not current_user: return
        u = users[current_user]
        # Goals
        self.ids.goals_list.text = "\n".join(f"• {g}" for g in u.get("goals", []))
        # Habits
        habits_data = []
        for i, h in enumerate(u.get("habits", [])):
            habits_data.append({
                "hname": h["name"],
                "streak": h.get("streak", 0),
                "_index": i
            })
        self.ids.habits_rv.data = habits_data
        # Leaderboard
        board = sorted(users.items(), key=lambda x: x[1].get("level", 1), reverse=True)[:10]
        text = "Топ:\n" + "\n".join(f"{i+1}. {name} — lvl {data.get('level',1)}" for i, (name, data) in enumerate(board))
        self.ids.leaderboard_text.text = text
        # Shop
        container = self.ids.shop_container
        container.clear_widgets()
        for item in SHOP_ITEMS:
            btn = MDFlatButton(
                text=f"{_(item['name'])} — {item['cost']} { _('coins') }",
                on_release=lambda x=item: buy_premium(x)
            )
            container.add_widget(btn)
    def send_ai_message(self):
        text = self.ids.chat_input.text.strip()
        if not text: return
        self.ids.chat_input.text = ""
        lbl = Label(text=f"Вы: {text}", size_hint_y=None, height=dp(48), halign='left', valign='middle')
        self.ids.chat_messages.add_widget(lbl)
        threading.Thread(target=self.get_ai_response, args=(text,)).start()
    def get_ai_response(self, text):
        reply = ask_ai(text)
        Clock.schedule_once(lambda dt: self.add_ai_message(reply))
    def add_ai_message(self, text):
        lbl = Label(text=f"AI: {text}", size_hint_y=None, height=dp(64), halign='left', valign='middle')
        self.ids.chat_messages.add_widget(lbl)
        speak(text)
    def voice_message(self):
        text = listen_voice()
        if text:
            self.ids.chat_input.text = text
            self.send_ai_message()
    def show_life_plan(self):
        threading.Thread(target=lambda: self.add_ai_message(create_life_plan())).start()
    def add_new_goal(self):
        g = self.ids.new_goal.text.strip()
        if g:
            users[current_user]["goals"].append(g)
            add_xp(20)
            save_users(users)
            self.ids.new_goal.text = ""
            self.refresh_ui()
    def add_new_habit(self):
        h = self.ids.new_habit.text.strip()
        if h:
            add_habit(h)
            self.ids.new_habit.text = ""
            self.refresh_ui()
    def mark_done(self, index):
        mark_habit_done(index)
        self.refresh_ui()
    def take_photo_proof(self, index):
        def on_photo(b64):
            mark_habit_done(index, b64)
            Snackbar(text="Фото сохранено как доказательство").open()
        show_camera_popup(on_photo)
    def start_pomodoro(self):
        mins = int(self.ids.pomodoro_slider.value)
        pomodoro_start(mins)
        Snackbar(text=f"Pomodoro {mins} мин начат").open()
    def stop_pomodoro(self):
        pomodoro_stop()
        Snackbar(text="Pomodoro остановлен").open()
    def update_pomodoro_display(self, dt):
        if pomodoro_active:
            m, s = divmod(pomodoro_time_left, 60)
            self.ids.pomodoro_display.text = f"{m:02d}:{s:02d}"
        else:
            self.ids.pomodoro_display.text = "Готов"
    def save_mood(self):
        score = self.ids.mood_value.value
        note = self.ids.mood_note.text.strip()
        if current_user:
            users[current_user].setdefault("mood", []).append({"score": int(score), "note": note, "date": datetime.now().isoformat()})
            save_users(users)
        Snackbar(text=f"Настроение {int(score)} записано").open()
        self.ids.mood_note.text = ""
    def show_stats(self):
        show_dashboard()
    def ai_analysis(self):
        threading.Thread(target=lambda: self.add_ai_message(analyze_user())).start()
    def fin_forecast(self):
        if not users[current_user].get("money"):
            self.add_ai_message("Добавьте записи о финансах")
            return
        prompt = f"Финансы (последние): {users[current_user]['money'][-5:]} → прогноз на месяц + советы"
        res = ask_ai(prompt)
        self.add_ai_message(res)
    def change_language_dialog(self):
        content = BoxLayout(orientation='vertical')
        for lang in ['ru', 'en']:
            btn = MDFlatButton(text=lang.upper(), on_release=lambda x=lang: self.set_language(x))
            content.add_widget(btn)
        dialog = MDDialog(title= _('change_lang'), content_cls=content)
        dialog.open()
    def set_language(self, lang):
        global CURRENT_LANG
        CURRENT_LANG = lang
        Snackbar(text=f"Язык: {lang.upper()}").open()
        self.refresh_ui() # частичное обновление
    def create_backup(self):
        try:
            with open(f"backup_{current_user}.json", "w", encoding="utf-8") as f:
                json.dump(users[current_user], f, ensure_ascii=False, indent=2)
            Snackbar(text="Бэкап создан").open()
        except:
            Snackbar(text="Ошибка бэкапа").open()
    def export_to_ics(self):
        export_ics()
class LifeOSApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV)
    def _(self, key):
        return _(key)
if __name__ == "__main__":
    LifeOSApp().run()

# ────────────────────────────────────────────────────────────────────────────────
# НИЖЕ ДОБАВЛЕН МОЙ ПОСЛЕДНИЙ КОД (новый интерфейс + анти-лаги) 
# Ничего из твоего кода выше не изменено и не удалено
# ────────────────────────────────────────────────────────────────────────────────

from kivymd.uix.card import MDCard

KV_NEW = '''
#:import dp kivy.metrics.dp

ScreenManager:
    LoginScreen:
    MainScreen:

<LoginScreen@Screen>:
    name: 'login'
    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(32)
        spacing: dp(16)
        MDLabel:
            text: app._('title')
            halign: 'center'
            font_style: 'H4'
        MDTextField:
            id: username
            hint_text: app._('username')
        MDTextField:
            id: password
            hint_text: app._('password')
            password: True
        MDRaisedButton:
            text: app._('login')
            on_release: root.do_login()
        MDRaisedButton:
            text: app._('voice_login')
            on_release: root.voice_login()

<MainScreen@Screen>:
    name: 'main'
    orientation: 'vertical'

    # Основной контент (чат AI без лагов)
    MDBoxLayout:
        orientation: 'vertical'
        size_hint: 1, 1

        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(8)
            spacing: dp(8)

            ScrollView:
                do_scroll_x: False
                bar_width: 0
                MDBoxLayout:
                    id: chat_messages
                    orientation: 'vertical'
                    size_hint_y: None
                    height: self.minimum_height
                    padding: dp(8)
                    spacing: dp(8)

            MDTextField:
                id: chat_input
                hint_text: "Спроси LIFEOS AI..."
                size_hint_y: None
                height: dp(56)

            MDBoxLayout:
                size_hint_y: None
                height: dp(56)
                spacing: dp(8)
                padding: dp(8)
                MDRaisedButton:
                    text: app._('send')
                    on_release: root.send_ai_message()
                MDRaisedButton:
                    text: app._('voice')
                    on_release: root.voice_message()
                MDRaisedButton:
                    text: app._('plan')
                    on_release: root.show_life_plan()

    # Нижняя панель — как на скриншоте
    MDBottomNavigation:
        panel_color: 0.12, 0.08, 0.25, 1
        selected_color: 0.9, 0.6, 1, 1
        text_color_active: 1, 1, 1, 1
        text_color_normal: 0.8, 0.7, 0.9, 0.8

        MDBottomNavigationItem:
            name: 'ai'
            text: 'AI'
            icon: 'robot'

        MDBottomNavigationItem:
            name: 'goals'
            text: 'Цели'
            icon: 'checkbox-marked-circle-outline'

        MDBottomNavigationItem:
            name: 'focus'
            text: 'Фокус'
            icon: 'timer-sand'

        MDBottomNavigationItem:
            name: 'mood'
            text: 'Настроение'
            icon: 'emoticon'

        MDBottomNavigationItem:
            name: 'stats'
            text: 'Статистика'
            icon: 'chart-bar'

        MDBottomNavigationItem:
            name: 'shop'
            text: 'Магазин'
            icon: 'cart'

        MDBottomNavigationItem:
            name: 'leader'
            text: 'Лидеры'
            icon: 'trophy'
'''

class MainScreen(Screen):
    def on_enter(self):
        Clock.schedule_interval(self.update_pomodoro_display, 0.5)  # реже = меньше нагрузки
        self.refresh_ui()

    def send_ai_message(self):
        text = self.ids.chat_input.text.strip()
        if not text:
            return
        self.ids.chat_input.text = ""

        def add_user_msg(dt):
            lbl = Label(
                text=f"[b]Вы:[/b] {text}",
                size_hint_y=None,
                height=dp(48),
                markup=True,
                halign="left",
                valign="middle",
                text_size=(Window.width - dp(60), None)
            )
            self.ids.chat_messages.add_widget(lbl)

        Clock.schedule_once(add_user_msg, 0.05)

        threading.Thread(target=self._get_ai_reply, args=(text,), daemon=True).start()

    def _get_ai_reply(self, text):
        try:
            reply = ask_ai(text)
        except Exception as e:
            reply = f"Ошибка AI: {str(e)[:60]}"

        def add_ai_msg(dt):
            lbl = Label(
                text=f"[b]LIFEOS:[/b] {reply}",
                size_hint_y=None,
                height=dp(64),
                markup=True,
                halign="left",
                valign="middle",
                text_size=(Window.width - dp(60), None)
            )
            self.ids.chat_messages.add_widget(lbl)
            speak(reply)

            # Автоскролл вниз без лагов
            scroll = self.ids.chat_messages.parent
            if scroll:
                scroll.scroll_y = 0

        Clock.schedule_once(add_ai_msg, 0.1)

    def voice_message(self):
        def voice_thread():
            try:
                text = listen_voice()
                if text:
                    Clock.schedule_once(lambda dt: setattr(self.ids.chat_input, 'text', text), 0)
                    Clock.schedule_once(lambda dt: self.send_ai_message(), 0.3)
            except Exception as e:
                Clock.schedule_once(lambda dt: Snackbar(text=f"Голос не распознан: {str(e)}").open(), 0)

        threading.Thread(target=voice_thread, daemon=True).start()

# Обновляем build приложения (добавляет новый интерфейс поверх старого)
class LifeOSApp(MDApp):
    current_user = None

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.primary_hue = "700"
        self.theme_cls.accent_palette = "Purple"

        Builder.load_string(KV)       # твой оригинальный KV остаётся
        Builder.load_string(KV_NEW)   # новый стиль и анти-лаги

        return Builder.load_string('''
ScreenManager:
    LoginScreen:
    MainScreen:
''')

    def _(self, key):
        return _(key)

if __name__ == "__main__":
    LifeOSApp().run()
