#!/usr/bin/env python
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request, Response, json
from server.database.secret_service import *
from server.scheduler_jobs.remove_expired_secret import remove

app = Flask(__name__)
scheduler = BackgroundScheduler()
scheduler.add_job(func=remove, trigger='interval', minutes=5)


@app.post('/v1/secret')
def add_secret():
    request_data = request.form.to_dict()
    content_type = request.content_type
    print(content_type)
    if not content_type == 'application/x-www-form-urlencoded':
        return Response("Unsupported content type", status=415)

    accept_type = request.headers.get('Accept')
    link = add(request_data)

    if accept_type == 'application/json':
        return Response(json.dumps(link), content_type='application/json')

    elif accept_type == 'application/xml':
        xml_link = return_as_xml(link)
        return Response(xml_link, content_type='application/xml')


@app.get('/v1/secret/<hash>')
def get_secret_by_hash(hash):
    content_type = request.headers.get('Accept')
    retrieved_hash = retrieve(hash)

    if content_type == 'application/json':
        if retrieved_hash is None:
            return Response('Secret not found', status=404, content_type='application/json')

        return Response(json.dumps(retrieved_hash), content_type='application/json')

    elif content_type == 'application/xml':
        if retrieved_hash is None:
            return Response('Secret not found', status=404, content_type='application/xml')

        xml_string = return_as_xml(retrieved_hash)
        return Response(xml_string, content_type='application/xml')

    else:
        return Response("Unsupported content type", status=415)


if __name__ == '__main__':
    scheduler.start()
    app.run(port=8080)
