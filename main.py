import os
from signalbot import SignalBot, Command, Context
import time
import asyncio

from langgraph.checkpoint.memory import InMemorySaver
from hypatia import Hypatia

import logging
logging.getLogger().setLevel(logging.INFO)


checkpointer = InMemorySaver()
hypatia = Hypatia(memory = checkpointer)

def note_to_self(sender, receiver):
    return sender == receiver

def self_send(sender, receiver):
    return "3148073243" in sender and "3148073243" not in receiver

class PingCommand(Command):
    def descrive(self) -> str:
        return None
    
    async def handle(self, c: Context):
        command = c.message.text
        source = c.message.source_uuid
        recipient = c.message.recipient()

        # message = c.message
        # note_2_self = note_to_self(message.source_number, message.recipient())
        # self_sent = self_send(message.source_number, message.recipient())
        if "hypatia" in command.lower():
            if "mememe" in command:
                response = f"{recipient}"
            elif "/hypatia" not in command:
                response = "Hi! If you're trying to connect with Hypatia, you can summon her by calling '/hypatia'. You'll need to call this command each time you respond."
            else:
                try:
                    response = hypatia.invoke(command, conversation_id=source)
                except Exception as e:
                    response = str(e)
            await c.reply(response)

if __name__ == "__main__":
    # import plex

    # plex.scrape()

    bot = SignalBot({
        "signal_service": os.environ["SIGNAL_SERVICE"],
        "phone_number": os.environ["PHONE_NUMBER"]
    })
    bot.register(PingCommand()) # all contacts and groups
    bot.start()