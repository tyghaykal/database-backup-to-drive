# Backup Database into Google Drive, S3 or local drive

## Explanation

This code is for backup your database, zip it and save it into local disk or upload it into Google Drive or S3.

Dumped database into .sql will be deleted instantly after zipping it.

## Supported Drive

- Local Drive (local)
- Google Drive (google-drive)
- S3 (s3) => Also support S3 compatible cloud storage like vultr or digital ocean.

## Supported Python

Python 3.8.10++

## How to Run ?

1. Install python and pip, install the dependencies using `pip install -r requirements.txt`
2. Copy `.env.example` into `.env`
3. Insert database information on `.env`
4. Choose which drive type you want to use
5. If using Google Drive or S3, please read the section after this.
6. Run the script with `python main.py`

## How to run multiple database or config ?

1. Copy `.env` into `db1.env` or `anything.env`
2. If the database is different, please set different Google Drive Directory ID or S3 Directory name
3. Run the script with `python main.py --env=name.env`, if --env is not set, it will use the default `.env`

### Google Drive Step

If you want to use Google Drive as drive type, please follow this step:

1. Open [Google Cloud Console](https://console.cloud.google.com/welcome)
2. Create new project if you dont have one
3. Access the project, choose API & Services.
4. Choose Credentials on your left screen.
5. Create Credentials with type of Service Account.
6. Set role Project with access editor for the new credential.
7. At the bottom of Credentials page, you will find an email of your new credential, click it to open the detail page.
8. Open keys tab, add key then create new key as JSON file format.
9. Save the json file into credentials folder with name google.json or if you want to custom it, you can update the env for it.
10. Seach Google Drive API on access this [link](https://console.cloud.google.com/marketplace/product/google/drive.googleapis.com)
11. Enable it.
12. Open your google drive, create new folder then share it into your new credential email that you can read on the json file with key "client_email".
13. Add the directory id into `.env`, directory id is the last path of the Google Drive URL like `https://drive.google.com/drive/u/0/folders/xxxx` then the `xxxx` is the directory id.

### S3 Setup

### Google Drive Step

If you want to use S3 as drive type, please follow this step:

1. Update the `.env` with your S3 config
