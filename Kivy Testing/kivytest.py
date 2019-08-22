#experiments with kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from functools import partial
class Kivy1(App):
    def build(self):
        return Button(text="Kivy!!")
    def disable(self, instance, *args):
        instance.disabled=True
    def update(self, instance, *args)
Kivy1().run()