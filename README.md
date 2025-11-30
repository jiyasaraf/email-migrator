# Gmail Migration Tool

A Python-based utility to migrate emails from one Gmail account to another using IMAP. This tool allows you to list folders, count emails, and migrate them with progress tracking.

## Features

- **List Folders**: View all folders available in the source Gmail account.
- **Count Emails**: Get a count of emails in each folder to estimate migration time.
- **Migrate Emails**: Copy emails from the source account to the destination account.
- **Progress Tracking**: Visual progress bar using `tqdm` to monitor the migration process.
- **Safe Migration**: Uses `IMAPClient` for secure connections.

## Prerequisites

- Python 3.x installed on your system.
- Two Gmail accounts:
    - **Source Account (GR1)**: The account you want to copy emails *from*.
    - **Destination Account (GR2)**: The account you want to copy emails *to*.
- **App Passwords** for both Gmail accounts (see instructions below).

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd email-migrator-git
    ```

2.  **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  **Create a `.env` file**:
    Copy the example configuration file to create your local environment file.
    ```bash
    cp .env.example .env
    # On Windows Command Prompt: copy .env.example .env
    ```

2.  **Update `.env` with your credentials**:
    Open the `.env` file and fill in your email addresses and App Passwords.

    ```env
    GR1_EMAIL=your_source_email@gmail.com
    GR1_APP_PASSWORD=your_16_digit_source_app_password

    GR2_EMAIL=your_destination_email@gmail.com
    GR2_APP_PASSWORD=your_16_digit_destination_app_password
    ```

    > **Note**: Do NOT use your regular Gmail login password. You must generate an App Password.

## How to Generate a 16-Digit App Password

To use this tool, you need to generate an App Password for **both** the source and destination Gmail accounts. This is required because Google no longer supports "Less Secure Apps" for third-party access.

1.  **Go to your Google Account**:
    Visit [myaccount.google.com](https://myaccount.google.com/) and log in.

2.  **Navigate to Security**:
    Click on the **Security** tab on the left-hand sidebar.

3.  **Enable 2-Step Verification** (if not already enabled):
    - Under the "How you sign in to Google" section, find **2-Step Verification**.
    - If it's "Off", click it and follow the prompts to turn it on. App Passwords require 2FA to be enabled.

4.  **Generate App Password**:
    - Once 2-Step Verification is on, search for **"App passwords"** in the search bar at the top of the page (or look for it under the "2-Step Verification" settings, usually at the bottom).
    - You may be asked to sign in again.

5.  **Create the Password**:
    - **Select App**: Choose "Mail" or "Other (Custom name)". If you choose "Other", name it something like "Email Migrator".
    - **Select Device**: Choose your device (e.g., "Windows Computer") or just leave it as is.
    - Click **Generate**.

6.  **Copy the Password**:
    - A 16-character code will appear in a yellow bar (e.g., `abcd efgh ijkl mnop`).
    - **Copy this code**. You don't need the spaces, but it's fine if you paste them; the system usually handles it.
    - Paste this code into your `.env` file as the value for `GR1_APP_PASSWORD` (for source) or `GR2_APP_PASSWORD` (for destination).

7.  **Repeat**:
    - Repeat these steps for the second Gmail account.

## Usage

Run the main script to start the tool:

```bash
python main.py
```

Follow the on-screen prompts:
1.  **List Folders**: The tool will first list all folders in the source account.
2.  **Count Emails**: It will count the emails in each folder.
3.  **Migrate**: You will be asked if you want to proceed with the migration. Type `yes` to start.

## Troubleshooting

- **Authentication Failed**: Double-check your email and App Password in the `.env` file. Ensure you didn't accidentally paste your regular password.
- **IMAP Disabled**: Ensure IMAP is enabled in your Gmail settings.
    - Go to Gmail -> Settings (gear icon) -> See all settings -> **Forwarding and POP/IMAP**.
    - Under "IMAP access", select **Enable IMAP**.
