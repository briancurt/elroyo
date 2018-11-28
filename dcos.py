from marathon import MarathonClient, MarathonHttpError
from zappa.async import task
import os
import requests
import time
import yaml


dcos_username = os.environ['DCOS_USERNAME']
dcos_password = os.environ['DCOS_PASSWORD']
config = yaml.load(open('config.yaml'))

headers = {'Content-Type': 'application/json'}
payload = '{"uid":"' + dcos_username + '", "password":"' + dcos_password + '"}'


def conn(environment):
    '''
    DC/OS Auth for the API is a pain. The best I can do for now is
    send a POST to the ACS endpoint with username and password to fetch
    a temporary JWT.
    '''

    marathon_url = config['dcos']['endpoints'][environment] + "/service/marathon"
    auth_api_url = config['dcos']['endpoints'][environment] + "/acs/api/v1/auth/login"

    r = requests.post(auth_api_url, headers=headers, data=payload)
    c = MarathonClient(marathon_url, auth_token=r.json()['token'])

    return c


def status(service, environment):
    mc = conn(environment)

    try:
        service_data = mc.get_app(service)

        if service_data.instances == service_data.tasks_healthy and not service_data.tasks_unhealthy:
            append_msg = "Everything looks alright! :rocket:"
        else:
            append_msg = "Something doesn't look right... :skull_and_crossbones:"

        message = (f"*{service}* is running `{service_data.container.docker.image.split(':')[1]}`. "
                   f"It has `{str(service_data.instances)}` instances, `{str(service_data.tasks_healthy)}` out of which are reporting to be healthy. "
                   f"Each of them has `{str(service_data.cpus)}` cpus and `{str(service_data.mem)}` mem. {append_msg}"
        )
    except MarathonHttpError as err:
        message = f"I had a short circuit while processing your request. Are you sure *{service}* is the correct full ID? :zap:"

    return message


@task
def restart(service, environment, response_url):
    '''
    This one runs as an asynchronous job as noted by the @task annotation,
    as sometimes it takes a bit longer.
    '''
    mc = conn(environment)

    try:
        mc.restart_app(service, force=True)
        message = f"*{service}* is now restarting on *{environment}*!"
    except MarathonHttpError as err:
        message = f"I had a short circuit while processing your request. Are you sure *{service}* is the correct full ID? :zap:"

    data = {
        'response_type': 'in_channel',
        'text': message,
    }

    requests.post(response_url, json=data)
