import json
import os
import random
from datetime import datetime
from kivy.app import App
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.progressbar import ProgressBar
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Ellipse

APP_TITLE = "FF HEADSHOT BOOSTER PANEL"
DEFAULT_SETTINGS = {
    "language": "en",
    "sensitivity": {
        "General": 95, "Red Dot": 90, "2x Scope": 85,
        "4x Scope": 78, "Sniper Scope": 55, "Free Look": 75
    },
    "presets": {},
    "sessions": []
}
TRANSLATIONS = {
    "en": {
        "home":"HOME", "settings":"SENSITIVITY", "presets":"PRESETS",
        "calculator":"ACCURACY CALCULATOR", "trainer":"AIM TRAINER",
        "stats":"TRAINING STATS", "hud":"HUD GUIDE", "performance":"PERFORMANCE",
        "language":"Language", "save":"SAVE SETTINGS", "reset":"RESET",
        "general":"General", "red":"Red Dot", "two":"2x Scope", "four":"4x Scope",
        "sniper":"Sniper Scope", "free":"Free Look", "shots":"Shots attempted",
        "hits":"Headshots landed", "calculate":"CALCULATE", "accuracy":"Accuracy",
        "start":"START TRAINING", "tap":"TAP / FLICK TARGET", "record":"SAVE SESSION",
        "sessions":"Sessions", "best":"Best accuracy", "average":"Average accuracy",
        "hudtext":"Suggested HUD layout (adjust to comfort):",
        "fps":"FPS & DEVICE CHECKLIST", "offline":"OFFLINE • LOCAL DATA",
        "welcome":"Train your aim. Tune your settings. Play fair.",
        "note":"Practice tool only. It does not connect to or modify Free Fire."
    },
    "hi": {
        "home":"होम", "settings":"सेंसिटिविटी", "presets":"प्रीसेट",
        "calculator":"एक्यूरेसी कैलकुलेटर", "trainer":"ऐम ट्रेनर",
        "stats":"ट्रेनिंग आँकड़े", "hud":"HUD गाइड", "performance":"परफॉर्मेंस",
        "language":"भाषा", "save":"सेटिंग सेव करें", "reset":"रीसेट",
        "general":"जनरल", "red":"रेड डॉट", "two":"2x स्कोप", "four":"4x स्कोप",
        "sniper":"स्नाइपर स्कोप", "free":"फ्री लुक", "shots":"कुल शॉट",
        "hits":"हेडशॉट लगे", "calculate":"गणना करें", "accuracy":"एक्यूरेसी",
        "start":"ट्रेनिंग शुरू", "tap":"टारगेट टैप / फ्लिक", "record":"सेशन सेव",
        "sessions":"सेशन", "best":"सबसे अच्छी एक्यूरेसी", "average":"औसत एक्यूरेसी",
        "hudtext":"सुझाया गया HUD लेआउट:",
        "fps":"FPS और डिवाइस चेकलिस्ट", "offline":"ऑफलाइन • लोकल डेटा",
        "welcome":"ऐम की प्रैक्टिस करें। सेटिंग बेहतर करें। निष्पक्ष खेलें।",
        "note":"यह केवल अभ्यास टूल है। यह Free Fire से कनेक्ट या बदलाव नहीं करता।"
    },
    "bn": {
        "home":"হোম", "settings":"সেনসিটিভিটি", "presets":"প্রিসেট",
        "calculator":"অ্যাকুরেসি ক্যালকুলেটর", "trainer":"এম ট্রেনার",
        "stats":"ট্রেনিং পরিসংখ্যান", "hud":"HUD গাইড", "performance":"পারফরম্যান্স",
        "language":"ভাষা", "save":"সেটিংস সেভ করুন", "reset":"রিসেট",
        "general":"জেনারেল", "red":"রেড ডট", "two":"2x স্কোপ", "four":"4x স্কোপ",
        "sniper":"স্নাইপার স্কোপ", "free":"ফ্রি লুক", "shots":"মোট শট",
        "hits":"হেডশট লেগেছে", "calculate":"হিসাব করুন", "accuracy":"অ্যাকুরেসি",
        "start":"ট্রেনিং শুরু", "tap":"টার্গেটে ট্যাপ / ফ্লিক", "record":"সেশন সেভ",
        "sessions":"সেশন", "best":"সর্বোচ্চ অ্যাকুরেসি", "average":"গড় অ্যাকুরেসি",
        "hudtext":"প্রস্তাবিত HUD লেআউট:",
        "fps":"FPS ও ডিভাইস চেকলিস্ট", "offline":"অফলাইন • লোকাল ডেটা",
        "welcome":"এম অনুশীলন করুন। সেটিং ঠিক করুন। fair play করুন।",
        "note":"এটি শুধু অনুশীলনের টুল। Free Fire-এ সংযোগ বা পরিবর্তন করে না।"
    }
}
SENS_KEYS = ["General", "Red Dot", "2x Scope", "4x Scope", "Sniper Scope", "Free Look"]

def panel_label(text="", size=14, color=(0.88,0.94,0.91,1), height=dp(34), bold=False):
    return Label(text=str(text), size_hint_y=None, height=height, font_size=sp(size),
                 color=color, bold=bold, halign="left", valign="middle")

def sp(v):
    return dp(v)

class NeonButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0,0,0,0)
        self.color = (0.95,1,0.96,1)
        self.bold = True
        self.font_size = sp(14)
        self.size_hint_y = None
        self.height = dp(48)
        with self.canvas.before:
            self._c = Color(0.62,0.04,0.10,1)
            self._r = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])
        self.bind(pos=self._sync, size=self._sync)
        self.bind(on_press=self._pulse)
    def _sync(self, *_):
        self._r.pos, self._r.size = self.pos, self.size
    def _pulse(self, *_):
        Animation(opacity=0.72, duration=.08).start(self)
        Animation(opacity=1, duration=.16).start(self)


class AimPad(Widget):
    """Standalone touch drill: hit the visible target with a tap or swipe."""
    def __init__(self, on_result, **kwargs):
        super().__init__(**kwargs)
        self.on_result = on_result
        self.target_x = .5
        self.target_y = .5
        self.radius = dp(25)
        self.start_pos = None
        with self.canvas:
            self.bg_color = Color(.055,.075,.09,1)
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(14)])
            self.target_color = Color(.25,1,.48,1)
            self.target = Ellipse(pos=(0,0), size=(self.radius*2,self.radius*2))
            self.ring_color = Color(1,.18,.25,1)
            self.ring = Ellipse(pos=(0,0), size=(self.radius*2+dp(12),self.radius*2+dp(12)))
        self.bind(pos=self.redraw, size=self.redraw)
        Clock.schedule_once(self.redraw, 0)

    def redraw(self, *_):
        self.bg.pos, self.bg.size = self.pos, self.size
        x = self.x + self.width*self.target_x
        y = self.y + self.height*self.target_y
        self.target.pos = (x-self.radius,y-self.radius)
        self.ring.pos = (x-self.radius-dp(6),y-self.radius-dp(6))

    def move_target(self):
        self.target_x = random.uniform(.15,.85)
        self.target_y = random.uniform(.18,.82)
        self.redraw()

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.start_pos = touch.pos
            return True
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.start_pos and self.collide_point(*touch.pos):
            x = self.x + self.width*self.target_x
            y = self.y + self.height*self.target_y
            distance = ((touch.x-x)**2 + (touch.y-y)**2)**.5
            hit = distance <= self.radius + dp(18)
            dx, dy = touch.x-self.start_pos[0], touch.y-self.start_pos[1]
            self.start_pos = None
            self.on_result(hit, (dx*dx+dy*dy)**.5)
            self.move_target()
            return True
        self.start_pos = None
        return super().on_touch_up(touch)

class PanelApp(App):
    def build(self):
        Window.clearcolor = (0.025,0.035,0.045,1)
        self.data_path = os.path.join(self.user_data_dir, "panel_data.json")
        self.data = self.load_data()
        self.lang = self.data.get("language","en")
        self.root_box = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(8))
        self.header = BoxLayout(size_hint_y=None, height=dp(72), spacing=dp(8))
        self.header.add_widget(Label(text="🎯", font_size=dp(30), size_hint_x=None, width=dp(44)))
        title_box = BoxLayout(orientation="vertical")
        title_box.add_widget(Label(text="FF HEADSHOT BOOSTER", bold=True, color=(0.3,1,0.55,1),
                                   font_size=dp(17), halign="left", valign="bottom"))
        title_box.add_widget(Label(text="PANEL  •  TRAIN FAIR", color=(1,.25,.3,1),
                                   font_size=dp(10), halign="left", valign="top"))
        self.header.add_widget(title_box)
        self.root_box.add_widget(self.header)
        self.nav = GridLayout(cols=3, spacing=dp(6), size_hint_y=None)
        self.nav.bind(minimum_height=self.nav.setter("height"))
        self.root_box.add_widget(self.nav)
        self.scroll = ScrollView(do_scroll_x=False)
        self.content = BoxLayout(orientation="vertical", spacing=dp(10), padding=(0,dp(6)), size_hint_y=None)
        self.content.bind(minimum_height=self.content.setter("height"))
        self.scroll.add_widget(self.content)
        self.root_box.add_widget(self.scroll)
        self.footer = Label(text=self.t("offline"), size_hint_y=None, height=dp(24),
                            color=(0.35,1,0.55,1), font_size=dp(10))
        self.root_box.add_widget(self.footer)
        self.build_nav()
        self.show_home()
        return self.root_box

    def t(self, key):
        return TRANSLATIONS.get(self.lang, TRANSLATIONS["en"]).get(key,key)

    def load_data(self):
        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            merged = DEFAULT_SETTINGS.copy()
            merged.update(loaded)
            merged["sensitivity"] = {**DEFAULT_SETTINGS["sensitivity"], **loaded.get("sensitivity",{})}
            return merged
        except Exception:
            return json.loads(json.dumps(DEFAULT_SETTINGS))

    def save_data(self):
        os.makedirs(self.user_data_dir, exist_ok=True)
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        self.footer.text = "✓ " + self.t("offline") + " • Saved"

    def clear_content(self):
        self.content.clear_widgets()

    def section(self, text):
        self.content.add_widget(panel_label(text, 17, (0.3,1,.55,1), dp(42), True))

    def card(self, title, body=""):
        box = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(5),
                        size_hint_y=None, height=dp(86))
        with box.canvas.before:
            Color(.055,.075,.09,1)
            rect = RoundedRectangle(pos=box.pos,size=box.size,radius=[dp(12)])
        box.bind(pos=lambda w,v:setattr(rect,"pos",v), size=lambda w,v:setattr(rect,"size",v))
        box.add_widget(panel_label(title,15,(1,.28,.32,1),dp(28),True))
        if body: box.add_widget(panel_label(body,12))
        self.content.add_widget(box)
        return box

    def build_nav(self):
        self.nav.clear_widgets()
        for key, callback in [
            ("home",self.show_home),("settings",self.show_sensitivity),("presets",self.show_presets),
            ("calculator",self.show_calculator),("trainer",self.show_trainer),("stats",self.show_stats),
            ("hud",self.show_hud),("performance",self.show_performance)
        ]:
            b = NeonButton(text=self.t(key), height=dp(40), font_size=dp(10))
            b.bind(on_release=lambda inst, cb=callback: cb())
            self.nav.add_widget(b)

    def show_home(self):
        self.clear_content()
        self.section("WELCOME TO THE TRAINING PANEL")
        self.card(self.t("welcome"), self.t("note"))
        self.card("01  •  SENSITIVITY LAB", "Tune six in-game values manually. No game access.")
        self.card("02  •  AIM PRACTICE", "Tap targets and record practice sessions.")
        self.card("03  •  PERFORMANCE", "Use the checklist to improve stable FPS.")
        self.section("LANGUAGE / ভাষা / भाषा")
        row = BoxLayout(size_hint_y=None,height=dp(46),spacing=dp(6))
        for code,name in [("en","English"),("bn","বাংলা"),("hi","हिन्दी")]:
            b=NeonButton(text=name,height=dp(42))
            b.bind(on_release=lambda x,c=code:self.set_language(c))
            row.add_widget(b)
        self.content.add_widget(row)

    def set_language(self, code):
        self.lang=code; self.data["language"]=code; self.save_data()
        self.build_nav(); self.show_home()

    def show_sensitivity(self):
        self.clear_content(); self.section(self.t("settings"))
        self.sensitivity_sliders={}
        for key in SENS_KEYS:
            row=BoxLayout(orientation="vertical",size_hint_y=None,height=dp(72),spacing=dp(1))
            top=BoxLayout(size_hint_y=None,height=dp(25))
            top.add_widget(panel_label(key,13))
            value=Label(text=str(self.data["sensitivity"].get(key,80)),size_hint_x=None,width=dp(44),
                        color=(.3,1,.55,1),font_size=dp(14))
            top.add_widget(value); row.add_widget(top)
            slider=Slider(min=0,max=200,value=self.data["sensitivity"].get(key,80),step=1)
            slider.bind(value=lambda obj,val,l=value,k=key:self.update_sens(k,val,l))
            row.add_widget(slider); self.content.add_widget(row)
            self.sensitivity_sliders[key]=slider
        self.add_button(self.t("save"), self.save_data)
        self.add_button(self.t("reset"), self.reset_sensitivity)

    def update_sens(self,key,val,label):
        self.data["sensitivity"][key]=int(val); label.text=str(int(val))

    def reset_sensitivity(self):
        self.data["sensitivity"]=dict(DEFAULT_SETTINGS["sensitivity"])
        self.show_sensitivity()

    def add_button(self,text,callback):
        b=NeonButton(text=text)
        b.bind(on_release=lambda *_:callback())
        self.content.add_widget(b)

    def show_presets(self):
        self.clear_content(); self.section(self.t("presets"))
        self.card("BALANCED", "A moderate starting point. Adjust after testing.")
        self.card("FAST DRAG", "Higher general / red-dot values; use only as a starting point.")
        self.card("PRECISION", "Lower scope values for steadier long-range control.")
        self.preset_name = TextInput(hint_text="Enter a name for your custom preset",
                                     multiline=False, size_hint_y=None, height=dp(46))
        self.content.add_widget(self.preset_name)
        for name, values in [
            ("Balanced", [95,90,85,78,55,75]),
            ("Fast Drag", [100,96,90,82,60,80]),
            ("Precision", [88,82,76,68,48,70])
        ]:
            b=NeonButton(text="APPLY " + name.upper())
            b.bind(on_release=lambda x,n=name,v=values:self.apply_preset(n,v))
            self.content.add_widget(b)
        self.add_button("SAVE CURRENT AS CUSTOM PRESET", self.save_custom_preset)
        for name, vals in self.data.get("presets",{}).items():
            self.add_button("LOAD " + name, lambda n=name,v=vals:self.load_custom(n,v))

    def apply_preset(self,name,values):
        self.data["sensitivity"]=dict(zip(SENS_KEYS,values)); self.save_data(); self.show_sensitivity()

    def save_custom_preset(self):
        name=self.preset_name.text.strip() if hasattr(self,"preset_name") else ""
        if not name: name="My Preset"
        self.data.setdefault("presets",{})[name]=dict(self.data["sensitivity"])
        self.save_data(); self.show_presets()

    def load_custom(self,name,values):
        self.data["sensitivity"]=dict(values); self.save_data(); self.show_sensitivity()

    def show_calculator(self):
        self.clear_content(); self.section(self.t("calculator"))
        self.shots=TextInput(text="100",hint_text=self.t("shots"),input_filter="int",
                             multiline=False,size_hint_y=None,height=dp(48))
        self.hits=TextInput(text="35",hint_text=self.t("hits"),input_filter="int",
                            multiline=False,size_hint_y=None,height=dp(48))
        self.content.add_widget(panel_label(self.t("shots"))); self.content.add_widget(self.shots)
        self.content.add_widget(panel_label(self.t("hits"))); self.content.add_widget(self.hits)
        self.calc_result=panel_label("Accuracy: —",20,(.3,1,.55,1),dp(54),True)
        self.content.add_widget(self.calc_result)
        self.add_button(self.t("calculate"),self.calculate_accuracy)
        self.content.add_widget(panel_label("Formula: headshots ÷ shots × 100. This is a practice metric, not a game prediction.",12))

    def calculate_accuracy(self):
        try:
            shots=int(self.shots.text); hits=int(self.hits.text)
            if shots<=0 or hits<0 or hits>shots: raise ValueError()
            pct=hits/shots*100
            self.calc_result.text=f"{self.t('accuracy')}: {pct:.1f}%"
        except Exception:
            self.calc_result.text="Enter valid numbers (0 ≤ headshots ≤ shots; shots > 0)."

    def show_trainer(self):
        self.clear_content(); self.section(self.t("trainer"))
        self.card("OFFLINE AIM DRILL", "A simple touch-response exercise. It does not overlay or interact with Free Fire.")
        self.score=0; self.attempts=0
        self.training_status=panel_label("Hits: 0 • Attempts: 0 • Accuracy: 0%",16,(.3,1,.55,1),dp(42),True)
        self.content.add_widget(self.training_status)
        self.aim_pad=AimPad(self.training_result, size_hint_y=None, height=dp(270))
        self.content.add_widget(self.aim_pad)
        self.add_button(self.t("record"),self.save_session)
        self.content.add_widget(panel_label("Tap the target or flick across it. Each attempt is measured only inside this practice area.",12))
    def training_result(self, hit, drag_distance):
        self.attempts += 1
        if hit: self.score += 1
        accuracy = self.score/self.attempts*100 if self.attempts else 0
        gesture = "Flick" if drag_distance > dp(35) else "Tap"
        result = "HIT" if hit else "MISS"
        self.training_status.text=f"{result} • {gesture} • Hits: {self.score}/{self.attempts} • {accuracy:.0f}%"

    def save_session(self):
        if not getattr(self,"attempts",0):
            self.footer.text="Start a drill before saving."
            return
        entry={"date":datetime.now().strftime("%Y-%m-%d %H:%M"),"attempts":self.attempts,
               "hits":self.score,"accuracy":round(self.score/self.attempts*100,1)}
        self.data.setdefault("sessions",[]).append(entry); self.save_data()
        self.footer.text="Training session saved locally."

    def show_stats(self):
        self.clear_content(); self.section(self.t("stats"))
        sessions=self.data.get("sessions",[])
        total=sum(s.get("attempts",0) for s in sessions)
        hits=sum(s.get("hits",0) for s in sessions)
        avg=(hits/total*100) if total else 0
        best=max([s.get("accuracy",0) for s in sessions],default=0)
        self.card(self.t("sessions"),str(len(sessions)))
        self.card(self.t("average"),f"{avg:.1f}%")
        self.card(self.t("best"),f"{best:.1f}%")
        self.section("RECENT HISTORY")
        for s in reversed(sessions[-20:]):
            self.card(s.get("date",""),f"{s.get('hits',0)} / {s.get('attempts',0)} taps • {s.get('accuracy',0)}%")
        if not sessions: self.card("No history yet","Complete a drill and save a session.")

    def show_hud(self):
        self.clear_content(); self.section(self.t("hud"))
        self.card(self.t("hudtext"),"Use these as general ergonomic suggestions; adapt to your screen and grip.")
        for title,body in [
            ("FIRE BUTTON","Place on the side used for firing; keep enough room for drag movement."),
            ("SCOPE / AIM","Keep near the fire control but avoid accidental touches."),
            ("MOVEMENT","Keep joystick within comfortable thumb reach."),
            ("UTILITY","Group medkit, grenade and weapon controls away from frequent touch paths."),
            ("TEST","Change one control at a time and practice in the game's training area.")
        ]: self.card(title,body)

    def show_performance(self):
        self.clear_content(); self.section(self.t("fps"))
        checks=[
            "Close unused background apps before playing.",
            "Keep at least 15–20% storage space free.",
            "Use the phone's built-in performance / game mode if available.",
            "Avoid playing while the device is overheating.",
            "Lower graphics if frame rate becomes unstable.",
            "Keep the game and Android system updated.",
            "Use a stable network; avoid downloads during matches.",
            "Do not install unknown booster APKs or grant unnecessary permissions."
        ]
        self.checks=[]
        for item in checks:
            cb=__import__("kivy.uix.checkbox",fromlist=["CheckBox"]).CheckBox(size_hint_x=None,width=dp(42))
            row=BoxLayout(size_hint_y=None,height=dp(48),spacing=dp(6))
            row.add_widget(cb); row.add_widget(panel_label(item,12))
            self.content.add_widget(row); self.checks.append(cb)
        self.add_button("CHECKLIST PROGRESS",self.show_check_progress)
    def show_check_progress(self):
        done=sum(1 for c in self.checks if c.active)
        self.footer.text=f"Checklist: {done}/{len(self.checks)} completed"

if __name__ == "__main__":
    PanelApp().run()
