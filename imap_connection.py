# imap_connection.py
# Handles IMAP login for Gmail account

from imapclient import IMAPClient
from config import IMAP_SERVER


def connect_to_gmail(email, app_password):
    """
    Connect to Gmail using IMAP and App Password
    Returns authenticated IMAPClient object
    """
    client = IMAPClient(IMAP_SERVER, ssl=True)
    client.login(email, app_password)
    return client
