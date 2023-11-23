from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem, TabbedPanelHeader
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget

import dropdown_data
from dropdown_data import *



# Глобальные настройки
Window.size = (1000, 500)

Builder.load_file('tabs.kv')


class Tabs(TabbedPanel):
    assets = []
    assets_threats = []
    # preview_assets = []
    aleroi_calculated = []
    roi_calculated = []
    threats_and_vulnerabilities = dropdown_data.threats_and_vulnerabilities

    def on_text(self, value):
        if not self.ids.asset_value.text.isnumeric():
            self.ids.asset_value.text = ''
        self.ids.save_asset_button.text = "Сохранить"

    def assets_spinner_clicked(self, value):
        self.ids.assets_spinner.text = value
        self.ids.save_asset_button.text = "Сохранить"

    def consequences_spinner_clicked(self, value):
        self.ids.consequences_spinner.text = value
        self.ids.save_asset_button.text = "Сохранить"

    def damagetype_spinner_clicked(self, value):
        self.ids.damagetype_spinner.text = value
        self.ids.save_asset_button.text = "Сохранить"

    def save_asset(self):
        asset = {}
        asset['name'] = self.ids.assets_spinner.text
        asset['consequence'] = self.ids.consequences_spinner.text
        asset['damage_type'] = self.ids.damagetype_spinner.text
        asset['value'] = self.ids.asset_value.text
        asset['notice'] = self.ids.notice.text
        print(asset)
        self.assets.append(asset)
        self.ids.choose_asset_spinner.values = self.get_assets()

    def get_assets(self):
        if len(self.assets):
            return list(set([val['name'] for val in self.assets]))
        return []

    def save_threats(self):
        threat = {}
        threat['asset'] = self.ids.choose_asset_spinner.text
        threat['name'] = self.ids.choose_threat_spinner.text
        threat['frequency'] = self.ids.threat_freq_value.text
        threat['probability'] = self.ids.threat_probability.text
        threat['protect_name'] = self.ids.protect_name.text
        threat['protect_price'] = self.ids.protect_price.text
        self.assets_threats.append(threat)
        self.ids.assets_last.text = self.get_threats()[0]
        self.ids.threats_last.text = self.get_threats()[1]
        self.ids.freq_last.text = self.get_threats()[2]
        self.ids.prob_last.text = self.get_threats()[3]
        self.ids.protect_name_last.text = self.get_threats()[4]
        self.ids.protect_price_last.text = self.get_threats()[5]

    def get_threats(self):
        if len(self.assets_threats):
            assets_temp = '\n\n'.join([val['asset'] for val in self.assets_threats])
            name_temp = '\n\n'.join([val['name'] for val in self.assets_threats])
            frequency_temp = '\n\n'.join([val['frequency'] for val in self.assets_threats])
            probability_temp = '\n\n'.join([val['probability'] for val in self.assets_threats])
            protect_name_temp = '\n\n'.join([val['protect_name'] for val in self.assets_threats])
            protect_price_temp = '\n\n'.join([val['protect_price'] for val in self.assets_threats])
            return [assets_temp, name_temp, frequency_temp, probability_temp, protect_name_temp, protect_price_temp]
        return ['', '', '', '', '', '']

    def calculate_aleroi(self):
        if len(self.assets_threats) and len(self.assets):
            for i, item in enumerate(self.assets_threats):
                aleroi = {}
                aleroi['asset'] = item['asset']
                aleroi['name'] = item['name']
                aleroi['frequency'] = item['frequency']
                aleroi['probability'] = item['probability']
                aleroi['ale'] = int(self.assets[i]['value']) * int(item['frequency']) * (int(item['probability']) / 100)
                aleroi['protect_price'] = item['protect_price']
                aleroi['roi'] = (aleroi['ale'] - int(item['protect_price']) - int(item['protect_price'])) / int(item['protect_price'])

                self.aleroi_calculated.append(aleroi)
                self.ids.aleroi_asset1.text = self.get_aleroi()[0]
                self.ids.aleroi_asset2.text = self.get_aleroi()[0]
                self.ids.aleroi_threat.text = self.get_aleroi()[1]
                self.ids.aleroi_frequency.text = self.get_aleroi()[2]
                self.ids.aleroi_probability.text = self.get_aleroi()[3]
                self.ids.aleroi_ale1.text = self.get_aleroi()[4]
                self.ids.aleroi_ale2.text = self.get_aleroi()[4]
                self.ids.aleroi_protect_price.text = self.get_aleroi()[5]
                self.ids.aleroi_roi.text = self.get_aleroi()[6]

    def get_aleroi(self):
        if len(self.aleroi_calculated):
            aleroi_asset_temp = '\n\n'.join([val['asset'] for val in self.aleroi_calculated])
            aleroi_name_temp = '\n\n'.join([val['name'] for val in self.aleroi_calculated])
            aleroi_frequency_temp = '\n\n'.join([val['frequency'] for val in self.aleroi_calculated])
            aleroi_probability_temp = '\n\n'.join([val['probability'] for val in self.aleroi_calculated])
            aleroi_ale_temp = '\n\n'.join([str(val['ale']) for val in self.aleroi_calculated])
            aleroi_protect_price_temp = '\n\n'.join([val['protect_price'] for val in self.aleroi_calculated])
            aleroi_roi_temp = '\n\n'.join([str(val['roi']) for val in self.aleroi_calculated])
            return [aleroi_asset_temp, aleroi_name_temp, aleroi_frequency_temp, aleroi_probability_temp, aleroi_ale_temp, aleroi_protect_price_temp, aleroi_roi_temp]
        return ['', '', '', '', '', '', '']


class MyApp(App):
    def build(self):
        tabs = Tabs()
        return tabs


# Запуск проекта
if __name__ == "__main__":
    MyApp().run()
