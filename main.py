# main.py
# Central control script

from list_folders import run as list_folders
from count_emails import run as count_emails
from migrate_all import run as migrate_all


def main():
    print("\n===================================")
    print("     GMAIL MIGRATION CONTROL TOOL")
    print("===================================\n")

    print("▶ STEP 1: Listing folders...\n")
    list_folders()

    print("\n▶ STEP 2: Counting emails...\n")
    count_emails()

    print("\n-----------------------------------")
    answer = input("Do you want to start FULL migration now? (yes/no): ").strip().lower()
    print("-----------------------------------\n")

    if answer in ["yes", "y"]:
        print("▶ STEP 3: Starting migration...\n")
        migrate_all()
    else:
        print("Migration cancelled. No emails were copied.")


if __name__ == "__main__":
    main()
