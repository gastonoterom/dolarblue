import os
from typing import cast

ALLOWED_CHAT_ID = int(cast(int, os.environ.get("ALLOWED_CHAT_ID")))
ADMIN_CHAT_ID = ALLOWED_CHAT_ID
BOT_TOKEN = str(os.environ.get('TELEGRAM_BOT_TOKEN'))
