from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.uix.filechooser import FileChooserListView
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout

import kivy
import os

import sys
from musicvisualizer.pipeline.pipeline import Pipeline

Builder.load_string("""
<MyWidget>:
    id: my_gui
    GridLayout:
        cols: 2
        Label:
            text: '[color=ff3333]Music [/color][color=3333ff]Visualizer[/color]'
            markup: True
            font_size: 40
        BoxLayout:
            id: groovSlider
            orientation: 'vertical'
            Label:
                text: '[color=3333ff]Groovyness[/color] [color=ff3333]Level[/color]'
                markup: True
                font_size: 30
            Slider:
                id: groovyness
                min: 0
                max: 10
                value: 0
                on_value: my_gui.setGroovyness(groovyness.value)
            Label:
                text: str(groovyness.value)
        FileChooserListView:
            id: filechooser
            on_selection: my_gui.selected(filechooser.selection)
        Button:
            id: VisButn
            text: '[color=94ff5f]VISUALIZE[/color]'
            markup: True
            font_size: 40
            on_press: my_gui.callback()
""")

class MyWidget(FloatLayout):

    # TODO: Fix static groove to be class-wide instance
    groove = 0
    file = None
    def setGroovyness(self, groovyness):
        groove = groovyness

    def selected(self, filename):
        print('selected: %s' % filename[0])
        MyWidget.file = filename[0]

    def callback(instance):
        print('The Visualize Button is being pressed')

        # build InputFields
        # TODO: Update inputfields to an actual Class? 
        inputfields = { 'groovyness'  : float(MyWidget.groove),
                        'source'      : MyWidget.file
                      }

        # start the pipeline process
        p = Pipeline(inputfields)
        p.buildVisualization()

class MyApp(App):
    def build(self):
        return MyWidget()

