import telegram
from telegram import MessageEntity

from dtb.settings import TELEGRAM_TOKEN
from tgbot.models import User


def send_message(user_id, text, parse_mode=None, reply_markup=None, reply_to_message_id=None,
                 disable_web_page_preview=None, entities=None, tg_token=TELEGRAM_TOKEN):
    bot = telegram.Bot(tg_token)
    try:
        if entities:
            entities = [
                MessageEntity(type=entity['type'],
                              offset=entity['offset'],
                              length=entity['length']
                )
                for entity in entities
            ]

        m = bot.send_message(
            chat_id=user_id,
            text=text,
            parse_mode=parse_mode,
            reply_markup=reply_markup,
            reply_to_message_id=reply_to_message_id,
            disable_web_page_preview=disable_web_page_preview,
            entities=entities,
        )
    except telegram.error.Unauthorized:
        print(f"Can't send message to {user_id}. Reason: Bot was stopped.")
        User.objects.filter(user_id=user_id).update(is_blocked_bot=True)
        success = False
    except Exception as e:
        print(f"Can't send message to {user_id}. Reason: {e}")
        success = False
    else:
        success = True
        User.objects.filter(user_id=user_id).update(is_blocked_bot=False)
    return success
