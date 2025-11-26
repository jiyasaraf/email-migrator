# config.py
import os
from dotenv import load_dotenv

load_dotenv()

IMAP_SERVER = "imap.gmail.com"

GR1_EMAIL = os.getenv("GR1_EMAIL")
GR1_APP_PASSWORD = os.getenv("GR1_APP_PASSWORD")

GR2_EMAIL = os.getenv("GR2_EMAIL")
GR2_APP_PASSWORD = os.getenv("GR2_APP_PASSWORD")
