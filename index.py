#!brython

import os
from radiant.server import RadiantAPI, RadiantServer, pyscript, delay
from browser import document, html, timer
from bootstrap.btn import Button
import logging
from radiant.utils import WebSocket


########################################################################
class HackLights(WebSocket):
    """"""

    DATA = {
        # "address": 5894,
        "datatype": 9,
        # "value": "600",
        "type": "text",
        "update": True,
        "action": "write",
    }

    ROOM = {
        'EEG': 7942,
        'BACK': 7942,
        'FRONT': 7942,
    }

    # ----------------------------------------------------------------------
    def on(self, room):
        """"""
        data = self.DATA.copy()
        data['addres'] = self.ROOM[room]
        data['value'] = '600'
        self.send(data)

    # ----------------------------------------------------------------------
    def off(self, room):
        """"""
        data = self.DATA.copy()
        data['addres'] = self.ROOM[room]
        data['value'] = '0'
        self.send(data)


########################################################################
class UNLights(RadiantAPI):

    # ----------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """"""
        super().__init__(*args, **kwargs)
        self.ws = HackLights('ws://172.20.176.40/scada-vis/objects/ws')

        document.select_one('body') <= Button('On', on_click=lambda evt: self.ws.on('EEG'))
        document.select_one('body') <= Button('Off', on_click=lambda evt: self.ws.off('EEG'))


if __name__ == '__main__':
    RadiantServer('UNLights',
                  # template=os.path.join('templates', 'layout.html'),
                  static_app=True,
                  templates_path='templates',
                  )
