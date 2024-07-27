#!/usr/bin/env python3

import os
import subprocess
from datetime import datetime
import requests
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()

YANDEX_DISK_TOKEN = settings.YANDEX_OAUTH_KEY


def backup_database():
    db_name = settings.DATABASES['default']['NAME']
    db_user = settings.DATABASES['default']['USER']
    db_password = settings.DATABASES['default']['PASSWORD']
    db_host = settings.DATABASES['default']['HOST']
    db_port = settings.DATABASES['default']['PORT']

    backup_dir = 'backups'
    os.makedirs(backup_dir, exist_ok=True)

    backup_file = os.path.join(backup_dir, f"{db_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.sql")

    env = os.environ.copy()
    env['PGPASSWORD'] = db_password

    dump_command = [
        'pg_dump',
        '-h', db_host,
        '-p', str(db_port),
        '-U', db_user,
        '-F', 'c',
        '-f', backup_file,
        db_name
    ]

    try:
        subprocess.run(dump_command, env=env, check=True)
        print(f"Backup successful: {backup_file}")
        return backup_file
    except subprocess.CalledProcessError as e:
        print(f"Error during backup: {e}")
        return None


def upload_to_yandex_disk(file_path):
    upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    headers = {"Authorization": f"OAuth {YANDEX_DISK_TOKEN}"}
    params = {"path": f"/{os.path.basename(file_path)}", "overwrite": "true"}

    response = requests.get(upload_url, headers=headers, params=params)
    response.raise_for_status()

    upload_href = response.json().get("href")
    if not upload_href:
        print("Failed to get upload URL")
        return

    with open(file_path, 'rb') as file:
        upload_response = requests.put(upload_href, files={"file": file})
        upload_response.raise_for_status()

    print(f"Upload successful: {file_path}")


if __name__ == "__main__":
    backup_file = backup_database()
    if backup_file:
        upload_to_yandex_disk(backup_file)
