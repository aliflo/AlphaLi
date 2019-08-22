#experiments with kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
class Kivy1(App):
    def build(self):
        return Button(text="Kivy!!")
Kivy1().run()