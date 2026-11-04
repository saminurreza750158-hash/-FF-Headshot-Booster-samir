import sys
from kivy.app import App
from kivy.uix.label import Label


class TestApp(App):
    def build(self):
        import kivy
        txt = "Hello OK\nPython " + sys.version.split()[0] + "\nKivy " + kivy.__version__
        return Label(text=txt, font_size="22sp", halign="center")


TestApp().run()