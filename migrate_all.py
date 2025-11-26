# migrate_all.py
# STEP 4: Full mailbox migration GR1 -> GR2 with UID-based dedup, logging, and resume.

import json
from pathlib import Path

from tqdm import tqdm

from config import (
    GR1_EMAIL,
    GR1_APP_PASSWORD,
    GR2_EMAIL,
    GR2_APP_PASSWORD,
)
from imap_connection import connect_to_gmail
from utils.logger import get_logger


STATE_FILE = Path("data/migration_state.json")

# Folders we will SKIP entirely
SKIP_FOLDERS = {
    "[Gmail]",        # virtual parent
    "[Gmail]/Trash",  # user chose NO for Trash
}

logger = get_logger("migration")


def load_state():
    """
    Load migration state from JSON file.
    Structure:
    {
        "INBOX": [1, 2, 3],
        "[Gmail]/Sent Mail": [10, 11]
    }
    """
    if not STATE_FILE.exists():
        logger.info("No existing state file found, starting fresh.")
        return {}

    try:
        with STATE_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
            # Ensure keys are str and values are lists of ints
            cleaned = {}
            for folder, uids in data.items():
                cleaned[folder] = [int(uid) for uid in uids]
            logger.info("Loaded existing migration state.")
            return cleaned
    except Exception as e:
        logger.error(f"Failed to read state file: {e}")
        return {}


def save_state(state):
    """
    Save migration state to JSON file.
    """
    try:
        STATE_FILE.parent.mkdir(exist_ok=True)
        with STATE_FILE.open("w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
        logger.info("Saved migration state.")
    except Exception as e:
        logger.error(f"Failed to save state file: {e}")


def ensure_target_folder(target_client, folder_name: str):
    """
    Ensure the target folder exists in GR2. If not, create it.
    """
    try:
        target_client.select_folder(folder_name)
        return
    except Exception:
        # Try to create then select
        logger.info(f"Creating folder '{folder_name}' in GR2...")
        try:
            target_client.create_folder(folder_name)
            target_client.select_folder(folder_name)
        except Exception as e:
            logger.error(f"Could not create/select folder '{folder_name}' in GR2: {e}")
            raise


def migrate_folder(source_client, target_client, folder_name: str, state: dict):
    """
    Migrate all messages from one folder, using UID-based dedup.
    Updates the state dict in-place.
    """
    if folder_name in SKIP_FOLDERS:
        logger.info(f"Skipping folder (per configuration): {folder_name}")
        return

    logger.info(f"Starting migration for folder: {folder_name}")

    # Select source folder (read-only)
    try:
        source_client.select_folder(folder_name, readonly=True)
    except Exception as e:
        logger.error(f"Cannot select folder '{folder_name}' in GR1: {e}")
        return

    try:
        all_uids = source_client.search("ALL")
    except Exception as e:
        logger.error(f"Failed to search UIDs in folder '{folder_name}': {e}")
        return

    if not all_uids:
        logger.info(f"No emails found in folder: {folder_name}")
        return

    migrated_uids = set(state.get(folder_name, []))
    remaining_uids = [uid for uid in all_uids if uid not in migrated_uids]

    if not remaining_uids:
        logger.info(f"All emails already migrated for folder: {folder_name}")
        return

    logger.info(
        f"Folder '{folder_name}': total={len(all_uids)}, "
        f"already_migrated={len(migrated_uids)}, to_migrate={len(remaining_uids)}"
    )

    # Ensure folder exists in GR2
    try:
        ensure_target_folder(target_client, folder_name)
    except Exception:
        logger.error(f"Skipping folder '{folder_name}' due to target folder error.")
        return

    # Migrate one by one with progress bar
    for uid in tqdm(remaining_uids, desc=f"Migrating {folder_name}", unit="email"):
        try:
            fetched = source_client.fetch([uid], ["RFC822"])
            raw_msg = fetched[uid][b"RFC822"]

            # Append to same folder name in GR2
            target_client.append(folder_name, raw_msg)

            migrated_uids.add(uid)
            state[folder_name] = sorted(list(migrated_uids))

            # Save state frequently for safety (could be optimized)
            save_state(state)

        except Exception as e:
            logger.error(f"Error migrating UID {uid} in folder '{folder_name}': {e}")

    logger.info(f"Completed migration for folder: {folder_name}")


def run():
    logger.info("========================================")
    logger.info("   FULL MAILBOX MIGRATION: GR1 -> GR2   ")
    logger.info("========================================")

    # Basic config validation
    if not all([GR1_EMAIL, GR1_APP_PASSWORD, GR2_EMAIL, GR2_APP_PASSWORD]):
        logger.error("Missing GR1/GR2 credentials in .env. Aborting.")
        return

    logger.info(f"Source (GR1): {GR1_EMAIL}")
    logger.info(f"Target (GR2): {GR2_EMAIL}")

    # Load existing state (if any)
    state = load_state()

    try:
        logger.info("Connecting to GR1...")
        source = connect_to_gmail(GR1_EMAIL, GR1_APP_PASSWORD)
        logger.info("Connected to GR1.")

        logger.info("Connecting to GR2...")
        target = connect_to_gmail(GR2_EMAIL, GR2_APP_PASSWORD)
        logger.info("Connected to GR2.")

        # List folders from GR1
        folders = source.list_folders()

        # Normalize folder names and migrate
        for flags, delimiter, folder in folders:
            if isinstance(folder, bytes):
                folder = folder.decode()

            migrate_folder(source, target, folder, state)

        logger.info("All folders processed. Migration attempt complete.")

    except KeyboardInterrupt:
        logger.warning("Migration interrupted by user (Ctrl+C).")
    except Exception as e:
        logger.error(f"Unexpected error during migration: {e}")
    finally:
        try:
            source.logout()
        except Exception:
            pass
        try:
            target.logout()
        except Exception:
            pass

        # Final save of state
        save_state(state)
        logger.info("State saved and connections closed. Exiting.")


if __name__ == "__main__":
    run()
