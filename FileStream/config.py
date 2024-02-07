from os import environ as env
from dotenv import load_dotenv
load_dotenv()
class Telegram:
    API_ID = int(env.get("API_ID","3704207"))
    API_HASH = str(env.get("API_HASH","8d20e46f5413139329f2ec753f7c482a"))
    BOT_TOKEN = str(env.get("BOT_TOKEN","6619679005:AAEds-OxM7h9wwDL5JruwAjcDN7dES5aAWo"))
    OWNER_ID = int(env.get('OWNER_ID', '1531899507'))
    WORKERS = int(env.get("WORKERS", "6"))  # 6 workers = 6 commands at once
    DATABASE_URL = str(env.get('DATABASE_URL',"mongodb+srv://vegafiletolinkbot:vegafiletolinkbot@cluster0.knjtwz3.mongodb.net/?retryWrites=true&w=majority"))
    UPDATES_CHANNEL = str(env.get('UPDATES_CHANNEL', "vegamoviesx"))
    SESSION_NAME = str(env.get('SESSION_NAME', 'FileStream'))
    FORCE_SUB_ID = env.get('FORCE_SUB_ID', None)
    FORCE_SUB = env.get('FORCE_UPDATES_CHANNEL', False)
    FORCE_SUB_ID = env.get('FORCE_SUB_ID', "-1002086574998")
    FORCE_SUB = env.get('FORCE_UPDATES_CHANNEL', True)
    FORCE_SUB = True if str(FORCE_SUB).lower() == "true" else False
    SLEEP_THRESHOLD = int(env.get("SLEEP_THRESHOLD", "60"))
    FILE_PIC = env.get('FILE_PIC', "https://graph.org/file/5bb9935be0229adf98b73.jpg")
    START_PIC = env.get('START_PIC', "https://telegra.ph/file/2336034b8c89c6bba8958.jpg")
    VERIFY_PIC = env.get('VERIFY_PIC', "https://telegra.ph/file/2336034b8c89c6bba8958.jpg")
    MULTI_CLIENT = False
    FLOG_CHANNEL = int(env.get("FLOG_CHANNEL", "-1002131280557"))   # Logs channel for file logs
    ULOG_CHANNEL = int(env.get("ULOG_CHANNEL", "-1002131280557"))   # Logs channel for user logs
    MODE = env.get("MODE", "primary")
    SECONDARY = True if MODE.lower() == "secondary" else False
    AUTH_USERS = list(set(int(x) for x in str(env.get("AUTH_USERS", "")).split()))
class Server:
    PORT = int(env.get("PORT", 8080))
    BIND_ADDRESS = str(env.get("BIND_ADDRESS", "0.0.0.0"))
    PING_INTERVAL = int(env.get("PING_INTERVAL", "1200"))
    HAS_SSL = str(env.get("HAS_SSL", "0").lower()) in ("1", "true", "t", "yes", "y")
    NO_PORT = str(env.get("NO_PORT", "0").lower()) in ("1", "true", "t", "yes", "y")
    FQDN = str(env.get("FQDN", BIND_ADDRESS))
    URL = "http{}://{}{}/".format(
        "s" if HAS_SSL else "", FQDN, "" if NO_PORT else ""
    )
    KEEP_ALIVE = str(env.get("KEEP_ALIVE", "0").lower()) in ("1", "true", "t", "yes", "y")
