# test_migrate_inbox.py
# STEP 3: Copy a few emails from GR1 -> GR2 (TEST RUN)

from config import GR1_EMAIL, GR1_APP_PASSWORD, GR2_EMAIL, GR2_APP_PASSWORD
from imap_connection import connect_to_gmail


SOURCE_FOLDER = "INBOX"
MAX_EMAILS = 5   # we migrate ONLY 5 for testing


def main():
    print("==============================================")
    print(" STEP 3: TEST MIGRATION (LIMITED EMAIL COPY) ")
    print("==============================================\n")

    if not all([GR1_EMAIL, GR1_APP_PASSWORD, GR2_EMAIL, GR2_APP_PASSWORD]):
        print("ERROR: Missing credentials in .env file")
        return

    try:
        print("Connecting to GR1...")
        source = connect_to_gmail(GR1_EMAIL, GR1_APP_PASSWORD)

        print("Connecting to GR2...")
        target = connect_to_gmail(GR2_EMAIL, GR2_APP_PASSWORD)

        print(f"\nSelecting source folder: {SOURCE_FOLDER}")
        source.select_folder(SOURCE_FOLDER, readonly=True)

        uids = source.search("ALL")

        if not uids:
            print("No emails found in folder.")
            return

        test_uids = uids[:MAX_EMAILS]

        print(f"\nPreparing to migrate {len(test_uids)} email(s)...\n")

        # Ensure folder exists in GR2
        try:
            target.select_folder(SOURCE_FOLDER)
        except:
            print(f"Creating folder '{SOURCE_FOLDER}' in GR2...")
            target.create_folder(SOURCE_FOLDER)
            target.select_folder(SOURCE_FOLDER)

        for uid in test_uids:
            raw_msg = source.fetch([uid], ["RFC822"])[uid][b"RFC822"]
            target.append(SOURCE_FOLDER, raw_msg)
            print(f"✅ Migrated email UID {uid}")

        print("\nSTEP 3 COMPLETE.")
        print("Please open GR2 Gmail and verify emails arrived in INBOX.\n")

    except Exception as e:
        print("ERROR:", e)

    finally:
        try:
            source.logout()
            target.logout()
        except:
            pass


if __name__ == "__main__":
    main()
