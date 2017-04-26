from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
import sys; sys.path.append('pipeline/')
from InputFields import InputFields
from pipeline import Pipeline

groovynessLevelLabel = None

def OnGroovynessSliderValueChange(instance,value):
    global groovynessLevelLabel
    groovynessLevelLabel.text = str(value)

def callback(instance):
    print('The Visualize Button is being pressed')

    # build InputFields
    IF = InputFields()
    IF.groovyness = float(groovynessLevelLabel.text)

    # start the pipeline process
    p = Pipeline(IF)
    p.buildVisualization()

class MusAppGui(GridLayout):

    def __init__(self, **kwargs):
        super(MusAppGui, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text = '[color=ff3333]Music [/color][color=3333ff]Visualizer[/color]', markup = True , font_size = 40))

        global groovynessLevelLabel
        groovyness = Slider(min = 0, max = 10, value = 0)
        groovyness.bind(value = OnGroovynessSliderValueChange)
        groovynessLevelLabel = Label(text= str(groovyness.value))
        box = BoxLayout(orientation = 'vertical')
        box.add_widget(Label(text = '[color=3333ff]Groovyness[/color] [color=ff3333]Level[/color]', markup = True , font_size = 20))
        box.add_widget(groovyness)
        box.add_widget(groovynessLevelLabel)
        self.add_widget(box)

        self.add_widget(Label(text='File Explorer'))
        visButn = Button(text='[color=94ff5f]VISUALIZE[/color]', markup = True ,font_size = 40)
        visButn.bind(on_press=callback)
        self.add_widget(visButn)


class MyApp(App):

    def build(self):
        return MusAppGui()


if __name__ == '__main__':
    MyApp().run()
