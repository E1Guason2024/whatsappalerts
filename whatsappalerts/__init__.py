#!/usr/bin/env python
# -*- coding: utf-8 -*-
import octoprint.plugin
from octoprint.events import eventManager, Events

from twilio.rest import Client

twilio_sid = "Your Twilio Account SID"
twilio_auth = "Your Twilio Auth Token"
tel_number = "whatsapp:YOURTELEPHONENUMBER"

whatsapp_client = Client(twilio_sid, twilio_auth)

def sendMessage(message):
    msg = whatsapp_client.messages.create(body=message, from_="whatsapp:+14155238886", to=tel_number)

class WhatsappAlertsPlugin(octoprint.plugin.EventHandlerPlugin, octoprint.plugin.StartupPlugin):
    
    def on_after_startup(self):
        self._logger.info("WhatsappAlertsPlugin initialized!")
        
    def on_event(self, event, payload):
        message = ""
        if event == "EStop":
            message = "Emergency Stop has occured! Please check the state of the printer!"
        elif event == "PrintDone":
            message = "%s finished printing successfully! Printing Time: %s Minutes" % (payload["name"], str(round(int(payload["time"]),2))//60)
        elif event == "PrintFailed":
            message = "%s failed to be printed! Printing Time: %s Minutes" % (payload["name"], str(round(int(payload["time"]),2))//60)
        elif event == "PrintStarted":
            message = "%s started printing! File size: %s KB. Approximate Printing Time: %s Minutes" % (payload["name"], payload["size"]//1000, payload["size"]//1000//18.5)
        if message != "":
            sendMessage(message)

__plugin_name__ = "Whatsapp Alerts"
__plugin_version__ = "1.0.0"
__plugin_description__ = "Plugin that sends Whatsapp Messages. By Simon Heppner"
__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_implementation__ = WhatsappAlertsPlugin()

