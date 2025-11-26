# count_emails.py
# STEP 2: Count number of emails per folder (read-only)

from config import GR1_EMAIL, GR1_APP_PASSWORD
from imap_connection import connect_to_gmail


def run():
    print("====================================")
    print(" STEP 2: COUNTING EMAILS PER FOLDER ")
    print("====================================\n")

    if not GR1_EMAIL or not GR1_APP_PASSWORD:
        print("ERROR: Missing email or password in .env")
        return

    try:
        print("Connecting to Gmail...")
        client = connect_to_gmail(GR1_EMAIL, GR1_APP_PASSWORD)
        print("Connected successfully!\n")

        folders = client.list_folders()

        print("Emails per folder:\n")

        for flags, delimiter, folder in folders:
            if isinstance(folder, bytes):
                folder = folder.decode()

            try:
                # Select folder in read-only mode
                client.select_folder(folder, readonly=True)

                # Search all messages
                messages = client.search("ALL")

                count = len(messages)

                print(f"{folder} : {count} emails")

            except Exception as e:
                print(f"{folder} : ERROR ({e})")

        print("\nStep 2 complete. This was a read-only operation.")

    except Exception as e:
        print("ERROR:", e)

    finally:
        try:
            client.logout()
        except:
            pass


if __name__ == "__main__":
    run()
