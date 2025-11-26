# list_folders.py
# STEP 1: List all folders/labels from GR1 (read-only)

from config import GR1_EMAIL, GR1_APP_PASSWORD
from imap_connection import connect_to_gmail


def run():
    print("====================================")
    print(" STEP 1: LISTING FOLDERS FROM GR1 ")
    print("====================================\n")

    if not GR1_EMAIL or not GR1_APP_PASSWORD:
        print("ERROR: Missing email or password in .env file")
        return

    try:
        print("Connecting to Gmail...")
        client = connect_to_gmail(GR1_EMAIL, GR1_APP_PASSWORD)
        print("Connected successfully!\n")

        print("Folders found in GR1:\n")

        folders = client.list_folders()
        for flags, delimiter, folder_name in folders:
            if isinstance(folder_name, bytes):
                folder_name = folder_name.decode()

            print(f"- {folder_name}")

        print("\nDone. Folders listed successfully.")
        print("No changes were made to your account.\n")

    except Exception as e:
        print("ERROR:", e)

    finally:
        try:
            client.logout()
        except:
            pass


if __name__ == "__main__":
    run()
