from server.database.crud.crud_operations import remove_expired_hash


def remove():
    try:
        remove_expired_hash()
    except Exception as e:
        print(f"Unexpected error: {e}")
