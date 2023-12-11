from datetime import datetime

from server.database import Secret
from server.database.connection.database_connection import *
from sqlalchemy import update, select, or_, and_, delete

table = Secret.__table__


def store_secret(provided_hash, secret_text, created_at, expires_at, expire_after_views):
    secret = Secret(provided_hash, secret_text, created_at,
                    expires_at, expire_after_views)
    session.add(secret)
    session.commit()


def retrieve_secret_by_hash(requested_hash):
    updated_row = execute_update(requested_hash)
    if updated_row.rowcount > 0:
        return get_hash(requested_hash)


def remove_expired_hash():
    current_datetime = datetime.utcnow()
    delete_stmt = (
        delete(table)
        .where(
            ((table.c.remaining_views == 0) |
             ((table.c.created_at < table.c.expires_at) & (table.c.expires_at < current_datetime)))
        )
    )
    session.execute(delete_stmt)
    session.commit()


def execute_update(requested_hash):
    current_datetime = datetime.utcnow()
    update_stmt = (
        update(table)
        .where(table.c.salted_hash == requested_hash,
               and_(table.c.remaining_views > 0,
                    or_(table.c.expires_at >= current_datetime,
                        table.c.created_at == table.c.expires_at)))
        .values(remaining_views=table.c.remaining_views - 1)
    )
    updated_row = session.execute(update_stmt)
    session.commit()
    return updated_row


def get_hash(requested_hash):
    select_stmt = select(table).where(table.c.salted_hash == requested_hash)
    result = session.execute(select_stmt).fetchone()
    session.commit()
    return result.secret_text
