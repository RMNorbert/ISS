#!/usr/bin/env python
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request, make_response, jsonify
from server.database.secret_service import *
from server.scheduler_jobs.remove_expired_secret import remove
from constants import *

app = Flask(__name__)
scheduler = BackgroundScheduler()
scheduler.add_job(func=remove, trigger='interval', minutes=3)


@app.post('/v1/secret')
def add_secret():
    try:
        secret_text = request.form.get('secret')
        expire_after_views = int(request.form.get("expire_after_views"))
        expire_after = int(request.form.get('expire_after'))

        if secret_text == '' or expire_after_views == 0:
            return make_response(BAD_REQUEST_MESSAGE, BAD_REQUEST_STATUS_CODE)

        content_type = request.content_type

        if not content_type == X_WWW_FORM_URLENCODED_TYPE:
            return make_response(UNSUPPORTED_MESSAGE, UNSUPPORTED_STATUS_CODE)

        accept_type = request.headers.get('Accept')

        if accept_type == JSON_TYPE:
            stored_hash = add(secret_text, expire_after_views, expire_after)
            return make_response(jsonify(stored_hash), OK_STATUS_CODE)

        elif accept_type == XML_TYPE:
            stored_hash = add(secret_text, expire_after_views, expire_after)
            xml_link = return_as_xml(stored_hash)
            return make_response(xml_link, OK_STATUS_CODE)

    except Exception as e:
        print(f"Unexpected error: {e}")


@app.get('/v1/secret/<hash>')
def get_secret_by_hash(hash):
    try:
        content_type = request.headers.get('Accept')
        retrieved_hash = retrieve(hash)

        if retrieved_hash is None:
            return make_response(NOT_FOUND_MESSAGE, NOT_FOUND_STATUS_CODE)

        if content_type == JSON_TYPE:
            return make_response(jsonify(retrieved_hash), OK_STATUS_CODE)

        elif content_type == XML_TYPE:
            xml_string = return_as_xml(retrieved_hash)
            return make_response(xml_string, OK_STATUS_CODE)

        else:
            return make_response(UNSUPPORTED_MESSAGE, UNSUPPORTED_STATUS_CODE)

    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == '__main__':
    scheduler.start()
    app.run(port=8080)
