import os

# load .env
from dotenv import load_dotenv

from .bot import BotConfig, SolaceAlive

load_dotenv()
SOL_HOST = os.environ.get("SOL_HOST")
SOL_VPN = os.environ.get("SOL_VPN")
SOL_USERNAME = os.environ.get("SOL_USERNAME")
SOL_PASSWORD = os.environ.get("SOL_PASSWORD")

API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
NOTIFY_CHAT_ID = os.environ.get("NOTIFY_CHAT_ID")


def main():
    bot_config = BotConfig(
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        notify_chat_id=NOTIFY_CHAT_ID,
    )
    sa = SolaceAlive(SOL_HOST, SOL_VPN, SOL_USERNAME, SOL_PASSWORD, bot_config)
    sa = SolaceAlive(SOL_HOST, SOL_VPN, SOL_USERNAME, SOL_PASSWORD, bot_config)

    sa.run()
