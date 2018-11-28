from flask import abort, Flask, jsonify, request
import hashlib
import hmac
import os
import yaml

import dcos, misc, victorops


__author__ = 'Brian Curtich'

app = Flask(__name__)
slack_signing_secret = os.environ['SLACK_SIGNING_SECRET']
config = yaml.load(open('config.yaml'))


def validate_request(request):
    '''
    This is pain. Verify that the request was sent by Slack and nobody else.
    More: https://api.slack.com/docs/verifying-requests-from-slack#about
    '''
    slack_signature = request.headers['X-Slack-Signature']
    slack_request_timestamp = request.headers['X-Slack-Request-Timestamp']

    request.get_data()
    basestring = f"v0:{slack_request_timestamp}:".encode('utf-8') + request.data
    slack_signing_secret_b = bytes(slack_signing_secret, 'utf-8')
    my_signature = 'v0=' + hmac.new(slack_signing_secret_b, basestring, hashlib.sha256).hexdigest()

    if hmac.compare_digest(my_signature, slack_signature):
        return True
    else:
        return False


@app.route('/dcos', methods=['POST'])
def path_dcos():
    if not validate_request(request):
        abort(403)

    args = request.form['text'].split()

    response = ("To query a service run `/dcos status <full_service_id> <environment>`. "
                "To restart a service without downtime replace `status` for `restart`, "
                "but I can only do that for my Ops masters for now...")

    if len(args) == 3 and args[2] in config['general']['env_short_names']:
        if "status" in args[0]:
            response = dcos.status(args[1], args[2])

        elif "restart" in args[0]:
            if request.form['user_id'] in config['general']['superusers']:
                dcos.restart(args[1], args[2], request.form['response_url'])
                response = ""
            else:
                response = "Hey, uhm... Sorry, I'm not allowed to run that for _you_."

    return jsonify(
        response_type='in_channel',
        text=response
    )



@app.route('/victorops', methods=['POST'])
def path_victorops():
    if not validate_request(request):
        abort(403)

    args = request.form['text'].split()

    response = "To view the on call schedule, run `/victorops schedule`"

    if len(args) == 1 and "schedule" in args[0]:
        response = victorops.schedule()

    return jsonify(
        response_type='in_channel',
        text=response,
    )



@app.route('/misc', methods=['POST'])
def path_misc():
    if not validate_request(request):
        abort(403)

    args = request.form['text'].split()

    response = ":thinking_face:"

    if len(args) == 1:
        if args[0] in ['excuse', 'help']:
            response = misc.excuse()
        elif "dolar" in args[0]:
            response = misc.dolar()

    return jsonify(
        response_type='in_channel',
        text=response,
    )
