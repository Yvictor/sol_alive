import pyrsolace
import pyrogram
from typing import TypedDict

class BotConfig(TypedDict):
    api_id: int
    api_hash: str
    bot_token: str
    notify_chat_id: str

class SolaceAlive:
    connected = False

    def __init__(self, host: str, vpn: str, username: str, password: str, bot_config: BotConfig):
        self.client = pyrsolace.Client()
        self.bot_config = bot_config
        self.bot = pyrogram.Client("sol-alive-bot", bot_config["api_id"], bot_config["api_hash"], bot_token=bot_config["bot_token"])
        self.host = host
        self.vpn = vpn
        self.username = username
        self.password = password
        self.connected = False
    
    def start_bot(self):
        self.bot.start()
        self.bot.set_bot_commands([
            pyrogram.types.BotCommand("start", "Start the bot"),
            pyrogram.types.BotCommand("status", "Get the status of the bot")
        ])
        self.bot.stop()
        self.bot.add_handler(pyrogram.handlers.MessageHandler(self.get_connect_status), pyrogram.filters.command("status"))

    def connect(self):
        self.client.connect(self.host, self.vpn, self.username, self.password, client_name="sol-alive-check")

    async def get_connect_status(self, _client: pyrogram.Client, message: pyrogram.types.Message):
        await message.reply_text(f"Connected: {self.connected}")

    def on_event(self, event: pyrsolace.Event):
        try:
            if event.session_event.value == pyrsolace.SessionEvent.UpNotice.value:
                self.connected = True
                self.bot.send_message(chat_id=self.bot_config["notify_chat_id"], text="Solace Alive: Connected")
            elif event.session_event.value == pyrsolace.SessionEvent.DownError.value:
                self.connected = False
                self.bot.send_message(chat_id=self.bot_config["notify_chat_id"], text="Solace Alive: Disconnected")
        except Exception as e:
            print(f"Error: {repr(e)}")
        print(event)
        print(event.session_event.value == pyrsolace.SessionEvent.UpNotice.value)
        print(f"Connected: {self.connected}")

    def run(self):
        self.client.set_event_callback(self.on_event)
        self.start_bot()
        self.connect()
        self.bot.run()
        # Event().wait()

        