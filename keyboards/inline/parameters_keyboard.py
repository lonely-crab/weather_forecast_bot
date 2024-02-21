from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

NEXT = InlineKeyboardButton(text="Next", callback_data="next")
PREV = InlineKeyboardButton(text="Previous", callback_data="prev")


def create_custom_inline_keyboard(*args) -> InlineKeyboardMarkup:
    """
    Create custom inline keyboard.
    :param args:
    :type args: list | set
    :return:
    :rtype: InlineKeyboardMarkup
    """
    keyboard = InlineKeyboardMarkup()
    try:
        for i in range(0, len(args), 2):
            row_buttons = []

            button1 = InlineKeyboardButton(text=args[i], callback_data=args[i])
            row_buttons.append(button1)

            if i + 1 < len(args):
                button2 = InlineKeyboardButton(
                    text=args[i + 1], callback_data=args[i + 1]
                )
                row_buttons.append(button2)

            keyboard.add(*row_buttons)
    except ValueError:
        pass

    return keyboard
