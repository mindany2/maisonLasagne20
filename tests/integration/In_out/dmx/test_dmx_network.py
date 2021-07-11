import unittest
from tree.Mode import Mode
from unittest.mock import Mock, MagicMock
from mock import patch
import threading
from time import sleep
import pytest
from parametrize import parametrize
from In_out.network.Client import Client
from In_out.network.Rpi import Rpi
from In_out.network.Server import Server
from In_out.dmx.Wireless_transmitter import Wireless_transmitter
from In_out.dmx.controllers.Dmx_network import Dmx_network
from In_out.dmx.controllers.KingDMX import KingDMX
from In_out.utils.DMX import DMX
from tree.connected_objects.dmx.Dmx_dimmable_light import Dmx_dimmable_light
from tree.connected_objects.dmx.Dmx_strip_led import Dmx_strip_led
from tree.scenario.instructions.light.Instruction_dimmer import Instruction_dimmer
from tree.scenario.instructions.light.Instruction_color import Instruction_color
from tree.utils.Color import Color
from In_out.external_boards.relay.Relay import STATE

class TestDmxNetwork(unittest.TestCase):

    def start_server(self, clear, init, set_channel):
        self.getter = MagicMock()
        self.addr = "lol"
        self.relay1, self.relay2 = Mock(), Mock()

        def set_relay1(x):
            self.relay1.state = x

        def set_relay2(x):
            self.relay2.state = x

        self.relay1.set.side_effect = set_relay1
        self.relay2.set.side_effect = set_relay2
        self.transmitter1 = Wireless_transmitter(self.relay1, 0, 50)
        self.transmitter2 = Wireless_transmitter(self.relay2, 51, 60)
        self.controller = KingDMX(self.addr, transmitter=[self.transmitter1, self.transmitter2])

        self.getter.get_manager().get_dmx.return_value = self.controller
        self.server = Server(self.getter)
        threading.Thread(target=self.server.start).start()

    def kill(self):
        self.server.kill()

    @patch.object(DMX, "set_channel", return_value=None)
    @patch.object(DMX, "__init__", return_value=None)
    @patch.object(DMX, "clear_channels", return_value=None)
    def test_wireless_connect_and_server_management_instruction_kill(self, clear, init, set_channel):
        sleep(3)
        self.start_server(clear, init, set_channel)
        sleep(0.1)
        self.assertTrue(self.server.started)

        # create the remote connection rpi to the started server
        self.remote_rpi = Rpi("connection", None, "me")
        self.network_dmx = Dmx_network(self.remote_rpi)
        self.relay_light, self.relay_led = Mock(), Mock()
        self.light = Dmx_dimmable_light("light", self.relay_light, 20, self.network_dmx)
        self.led = Dmx_strip_led("light", self.relay_light, 55, self.network_dmx)

        self.calculator = Mock()
        self.calculator.eval.side_effect = lambda x, y: x
        self.inst_light = Instruction_dimmer(self.calculator, self.light, 100, 2, 0, False)
        self.inst_led = Instruction_color(self.calculator, self.led, 100, 2, 0, False, "0xff00ff")
        process1 = threading.Thread(target=self.inst_light.run, args=[Mock()])
        process2 = threading.Thread(target=self.inst_led.run, args=[Mock()])

        for process in [process1, process2]:
            process.start()

        sleep(2.5)
        process3 = threading.Thread(target=self.inst_light.run, args=[Mock()])
        process3.start()

        for process in [process1, process2, process3]:
            process.join()

        self.assertEqual(set_channel.call_count, 83)
        self.assertEqual(self.relay1.set.call_count, 2)
        self.assertEqual(self.relay2.set.call_count, 2)
        self.assertEqual(self.led.color, Color("0xff00ff"))
        self.assertEqual(self.led.dimmer, 100)
        self.assertEqual(self.light.dimmer, 100)

        self.kill()




        

 
