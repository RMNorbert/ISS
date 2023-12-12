from datetime import datetime

from server.database import Secret
from server.database.connection.database_connection import *
from sqlalchemy import update, select, or_, and_, delete

table = Secret.__table__
ZERO = 0
ONE = 1


def store_secret(provided_hash, secret_text, created_at, expires_at, expire_after_views):
    try:
        secret = Secret(provided_hash, secret_text, created_at,
                        expires_at, expire_after_views)
        session.add(secret)
        session.commit()
    except Exception as e:
        print(f"Unexpected error: {e}")


def retrieve_secret_by_hash(requested_hash):
    try:
        updated_row = execute_update(requested_hash)
        if updated_row.rowcount > ZERO:
            return get_hash(requested_hash)
    except Exception as e:
        print(f"Unexpected error: {e}")


def remove_expired_hash():
    try:
        current_datetime = datetime.utcnow()
        delete_stmt = (
            delete(table)
            .where(
                ((table.c.remaining_views == ZERO) |
                 ((table.c.created_at < table.c.expires_at) & (table.c.expires_at < current_datetime)))
            )
        )
        session.execute(delete_stmt)
        session.commit()
    except Exception as e:
        print(f"Unexpected error: {e}")


def execute_update(requested_hash):
    try:
        current_datetime = datetime.utcnow()
        update_stmt = (
            update(table)
            .where(table.c.salted_hash == requested_hash,
                   and_(table.c.remaining_views > ZERO,
                        or_(table.c.expires_at > current_datetime,
                            table.c.created_at == table.c.expires_at)))
            .values(remaining_views=table.c.remaining_views - ONE)
        )
        updated_row = session.execute(update_stmt)
        return updated_row
    except Exception as e:
        print(f"Unexpected error: {e}")


def get_hash(requested_hash):
    try:
        select_stmt = select(table).where(
            table.c.salted_hash == requested_hash)
        result = session.execute(select_stmt).fetchone()
        session.commit()
        return result.secret_text
    except Exception as e:
        print(f"Unexpected error: {e}")
