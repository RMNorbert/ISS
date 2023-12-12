from server.database.crud.crud_operations import *
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import hashlib


def add(secret_text, expire_after_views, expire_after):
    try:
        created_at = datetime.now()
        expires_at = created_at + timedelta(minutes=expire_after)

        hashed_and_salted_secret = hash_and_salt_secret(
            secret_text, created_at)
        store_secret(hashed_and_salted_secret, secret_text,
                     created_at, expires_at, expire_after_views)
        return hashed_and_salted_secret
    except Exception as e:
        print(f"Unexpected error: {e}")


def retrieve(searched_hash):
    try:
        return retrieve_secret_by_hash(searched_hash)
    except Exception as e:
        print(f"Unexpected error: {e}")


def hash_and_salt_secret(secret_text, created_at):
    try:
        salt = created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        salted_secret = (secret_text + salt).encode('UTF-8')
        return hashlib.sha3_512(salted_secret).hexdigest()
    except Exception as e:
        print(f"Unexpected error: {e}")


def return_as_xml(response_data):
    try:
        root = ET.Element("root")
        response = ET.SubElement(root, "response")
        response.text = response_data
        xml_string = ET.tostring(root, encoding="utf-8").decode("utf-8")
        return xml_string
    except Exception as e:
        print(f"Unexpected error: {e}")
