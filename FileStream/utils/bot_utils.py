from pyrogram.errors import UserNotParticipant, FloodWait
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from FileStream.utils.translation import LANG
from FileStream.utils.database import Database
from FileStream.utils.human_readable import humanbytes
from FileStream.config import Telegram, Server
from FileStream.bot import FileStream
import asyncio
from typing import (
    Union
)


db = Database(Telegram.DATABASE_URL, Telegram.SESSION_NAME)

async def get_invite_link(bot, chat_id: Union[str, int]):
    try:
        invite_link = await bot.create_chat_invite_link(chat_id=chat_id)
        return invite_link
    except FloodWait as e:
        print(f"Sleep of {e.value}s caused by FloodWait ...")
        await asyncio.sleep(e.value)
        return await get_invite_link(bot, chat_id)

async def is_user_joined(bot, message: Message):
    if Telegram.FORCE_SUB_ID and Telegram.FORCE_SUB_ID.startswith("-100"):
        channel_chat_id = int(Telegram.FORCE_SUB_ID)    # When id startswith with -100
    elif Telegram.FORCE_SUB_ID and (not Telegram.FORCE_SUB_ID.startswith("-100")):
        channel_chat_id = Telegram.FORCE_SUB_ID     # When id not startswith -100
    else:
        return 200
    try:
        user = await bot.get_chat_member(chat_id=channel_chat_id, user_id=message.from_user.id)
        if user.status == "BANNED":
            await message.reply_text(
                text=LANG.BAN_TEXT.format(Telegram.OWNER_ID),
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True
            )
            return False
    except UserNotParticipant:
        invite_link = await get_invite_link(bot, chat_id=channel_chat_id)
        if Telegram.VERIFY_PIC:
            ver = await message.reply_photo(
                photo=Telegram.VERIFY_PIC,
                caption="<i>Jᴏɪɴ ᴍʏ ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴜsᴇ ᴍᴇ </i>",
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("Jᴏɪɴ Oᴜʀ Cʜᴀɴɴᴇʟ ", url=invite_link.invite_link)
                ]]
                )
            )
        else:
            ver = await message.reply_text(
                text = "<i>Jᴏɪɴ ᴍʏ ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴜsᴇ ᴍᴇ </i>",
                reply_markup=InlineKeyboardMarkup(
                    [[
                        InlineKeyboardButton(" Jᴏɪɴ Oᴜʀ Cʜᴀɴɴᴇʟ ", url=invite_link.invite_link)
                    ]]
                ),
                parse_mode=ParseMode.HTML
            )
        await asyncio.sleep(30)
        try:
            await ver.delete()
            await message.delete()
        except Exception:
            pass
        return False
    except Exception:
        await message.reply_text(
            text = f"<i>Sᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ᴄᴏɴᴛᴀᴄᴛ ᴍʏ ᴅᴇᴠᴇʟᴏᴘᴇʀ</i> <b><a href='https://t.me/{Telegram.UPDATES_CHANNEL}'>[ ᴄʟɪᴄᴋ ʜᴇʀᴇ ]</a></b>",
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True)
        return False
    return True

#---------------------[ PRIVATE GEN LINK + CALLBACK ]---------------------#

async def gen_link(_id):
    file_info = await db.get_file(_id)
    file_name = await process_text (file_info['file_name'])
    file_size = humanbytes(file_info['file_size'])
    mime_type = file_info['mime_type']

    page_link = f"{Server.URL}watch/{_id}"
    stream_link = f"{Server.URL}dl/{_id}"
    file_link = f"https://t.me/{FileStream.username}?start=file_{_id}"

    if "video" in mime_type:
        stream_text = LANG.STREAM_TEXT.format(file_name, file_size, stream_link, page_link)
        reply_markup = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("sᴛʀᴇᴀᴍ ⚡", url=page_link), InlineKeyboardButton("ᴅᴏᴡɴʟᴏᴀᴅ 📥", url=stream_link)]
            ]
        )
    else:
        stream_text = LANG.STREAM_TEXT_X.format(file_name, file_size, stream_link, file_link)
        reply_markup = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("ᴅᴏᴡɴʟᴏᴀᴅ", url=stream_link)],
                [InlineKeyboardButton("ɢᴇᴛ ғɪʟᴇ", url=file_link), InlineKeyboardButton("ʀᴇᴠᴏᴋᴇ ғɪʟᴇ", callback_data=f"msgdelpvt_{_id}")],
                [InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]
            ]
        )
    return reply_markup, stream_text

#---------------------[ GEN STREAM LINKS FOR CHANNEL ]---------------------#

async def gen_linkx(m:Message , _id, name: list):
    file_info = await db.get_file(_id)
    file_name = file_info['file_name']
    mime_type = file_info['mime_type']
    file_size = humanbytes(file_info['file_size'])

    page_link = f"{Server.URL}watch/{_id}"
    stream_link = f"{Server.URL}dl/{_id}"
    file_link = f"https://t.me/{FileStream.username}?start=file_{_id}"

    if "video" in mime_type:
        stream_text= LANG.STREAM_TEXT_X.format(file_name, file_size, stream_link, page_link)
        reply_markup = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("sᴛʀᴇᴀᴍ", url=page_link), InlineKeyboardButton("ᴅᴏᴡɴʟᴏᴀᴅ", url=stream_link)]
            ]
        )
    else:
        stream_text= LANG.STREAM_TEXT_X.format(file_name, file_size, stream_link, file_link)
        reply_markup = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("ᴅᴏᴡɴʟᴏᴀᴅ", url=stream_link)]
            ]
        )
    return reply_markup, stream_text

#---------------------[ USER BANNED ]---------------------#

async def is_user_banned(message):
    if await db.is_user_banned(message.from_user.id):
        await message.reply_text(
            text=LANG.BAN_TEXT.format(Telegram.OWNER_ID),
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )
        return True
    return False

#---------------------[ CHANNEL BANNED ]---------------------#

async def is_channel_banned(bot, message):
    if await db.is_user_banned(message.chat.id):
        await bot.edit_message_reply_markup(
            chat_id=message.chat.id,
            message_id=message.id,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(f"ᴄʜᴀɴɴᴇʟ ɪs ʙᴀɴɴᴇᴅ", callback_data="N/A")]])
        )
        return True
    return False

#---------------------[ USER AUTH ]---------------------#

async def is_user_authorized(message):
    if hasattr(Telegram, 'AUTH_USERS') and Telegram.AUTH_USERS:
        user_id = message.from_user.id

        if user_id == Telegram.OWNER_ID:
            return True

        if not (user_id in Telegram.AUTH_USERS):
            await message.reply_text(
                text="Yᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴛᴏ ᴜsᴇ ᴛʜɪs ʙᴏᴛ.",
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True
            )
            return False

    return True

#---------------------[ USER EXIST ]---------------------#

async def is_user_exist(bot, message):
    if not bool(await db.get_user(message.from_user.id)):
        await db.add_user(message.from_user.id)
        await bot.send_message(
            Telegram.ULOG_CHANNEL,
            f"**#NᴇᴡUsᴇʀ**\n**⬩ ᴜsᴇʀ ɴᴀᴍᴇ :** [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n**⬩ ᴜsᴇʀ ɪᴅ :** `{message.from_user.id}`"
        )

async def is_channel_exist(bot, message):
    if not bool(await db.get_user(message.chat.id)):
        await db.add_user(message.chat.id)
        members = await bot.get_chat_members_count(message.chat.id)
        await bot.send_message(
            Telegram.ULOG_CHANNEL,
            f"**#NᴇᴡCʜᴀɴɴᴇʟ** \n**⬩ ᴄʜᴀᴛ ɴᴀᴍᴇ :** `{message.chat.title}`\n**⬩ ᴄʜᴀᴛ ɪᴅ :** `{message.chat.id}`\n**⬩ ᴛᴏᴛᴀʟ ᴍᴇᴍʙᴇʀs :** `{members}`"
        )

async def verify_user(bot, message):
    # if not await is_user_authorized(message):
    #     return False

    # if await is_user_banned(message):
    #     return False

    await is_user_exist(bot, message)

    if Telegram.FORCE_SUB:
        if not await is_user_joined(bot, message):
            return False

    return True

async def process_text(text_caption): #text is filter and processed
    text_caption = text_caption.lower()

    # Remove emojis using regex module
    text_caption = regex.sub(r'\p{So}', '', text_caption)

    # Replace certain characters with spaces
    text_caption = re.sub(r"[@!$ _\-.+:*#⁓(),/?]", " ", text_caption)

    # Replace language abbreviations using a dictionary
    language_abbreviations = {"session":"season","hin": "hindi", "eng": "english", "tam": "tamil", "tel": "telugu","wanda vision":"wandavision","salar":"salaar","spiderman":"spider man","spiderverse":"spider verse","complete":"combined","12 th":"12th","completed":"combined","all episodes":"combined"}
    text_caption = re.sub(
        r"\b(?:session|hin|eng|tam|tel|wanda\s*vision|salar|spiderman|spiderverse|complete|12\s*th|completed|all\s*episodes)\b",
        lambda match: language_abbreviations.get(match.group(0), match.group(0)),
        text_caption
    )

    # Insert space between 's' and 'e' in patterns like 's01e04'
    text_caption = re.sub(r's(\d+)e(\d+)', r's\1 e\2', text_caption, flags=re.IGNORECASE)

    # Insert space between 's' and 'e' in patterns like 's1e4'
    text_caption = re.sub(r's(\d+)e', r's\1 e', text_caption, flags=re.IGNORECASE)

    # Convert 'ep' followed by a number to 'e' followed by that number with leading zeros
    text_caption = re.sub(r'\bep(\d+)\b', r'e\1', text_caption, flags=re.IGNORECASE)
    text_caption = re.sub(r'\bep (\d)\b', r'e0\1', text_caption, flags=re.IGNORECASE)
    text_caption = re.sub(r'\bep (\d{2,})\b', r'e\1', text_caption, flags=re.IGNORECASE)

        # Convert single-digit 'e' to two-digit 'e'
    text_caption = re.sub(r'\be(\d)\b', r'e0\1', text_caption, flags=re.IGNORECASE)

    # Convert single-digit 's' to two-digit 's'
    text_caption = re.sub(r'\bs(\d)\b', r's0\1', text_caption, flags=re.IGNORECASE)

    # Formatting for season and episode numbers (padding with zeros)
    text_caption = re.sub(r'\bseason (\d+)\b', lambda x: f's{x.group(1).zfill(2)}', text_caption, flags=re.IGNORECASE)
    text_caption = re.sub(r'\bepisode (\d+)\b', lambda x: f'e{x.group(1).zfill(2)}', text_caption, flags=re.IGNORECASE)

    #testing
    text_caption = ' '.join(['e' + word[2:] if word.startswith('e0') and word[2:].isdigit() and len(word) >= 4 else word for word in text_caption.split()])

    words_to_remove = ["full","video","videos","movie", "movies","series","dubbed","send","file","audio","to","language","quality","qua","aud","give","files","hd","in","dub","review","mkv"]

    # Create a regular expression pattern with all words to remove
    pattern = r'\b(?:' + '|'.join(re.escape(word) for word in words_to_remove) + r')\b'

    # Remove the specified words in a case-insensitive manner
    text_caption = re.sub(pattern, '', text_caption, flags=re.IGNORECASE)

    # Remove extra spaces between words
    text_caption = re.sub(r'\s+', ' ', text_caption)
    
    return text_caption.title()
