from server.database.crud.crud_operations import remove_expired_hash


def remove():
    remove_expired_hash()
