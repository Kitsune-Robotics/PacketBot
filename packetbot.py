import re
import os
import aprslib
import logging

from discord_webhook import DiscordWebhook

logging.basicConfig(level=logging.INFO)

logging.info("App Starting.")

packet = {
    "raw": 'KW1FOX-7>TSQP0W,WIDE1-1,WIDE2-2,qAR,N3LLO-2:`c=Hl#?</"5?}Snowsune#4646 4.04V  31.3C X',
    "from": "KW1FOX-7",
    "to": "TSQP0W",
    "path": ["WIDE1-1", "WIDE2-2", "qAR", "N3LLO-2"],
    "via": "N3LLO-2",
    "format": "mic-e",
    "symbol": "<",
    "symbol_table": "/",
    "posambiguity": 0,
    "latitude": 43.167833333333334,
    "mbits": "111",
    "mtype": "M0: Off Duty",
    "longitude": -71.55733333333333,
    "speed": 0.0,
    "course": 335,
    "altitude": 131,
    "comment": "Snowsune#4646 4.04V  31.3C X",
}


def callback(packet):
    if re.match("KW1FOX-*", packet["from"]):
        logging.info(f"Got a new packet from {packet['from']}!")
        logging.debug(f"Latt: {packet['latitude']}")
        logging.debug(f"Long: {packet['longitude']}")
        logging.debug(
            f"http://maps.google.com/maps?z=12&t=m&q=loc:{packet['latitude']}+{packet['longitude']}"
        )
        logging.debug(f"Volt: {packet['comment'].split()[1]}")
        logging.debug(f"Temp: {packet['comment'].split()[2]}")

        webhook = DiscordWebhook(
            url=os.environ["WEBHOOK"],
            content=f"New update from {packet['from']}!\nLocation: http://maps.google.com/maps?z=12&t=m&q=loc:{packet['latitude']}+{packet['longitude']}\nVolt: {packet['comment'].split()[1]}\nTemp: {packet['comment'].split()[2]}",
        )
        response = webhook.execute()


AIS = aprslib.IS("KW1FOX-1")
AIS.connect()
logging.info("Connected and ready.")
# by default `raw` is False, then each line is ran through aprslib.parse()
AIS.consumer(callback)
