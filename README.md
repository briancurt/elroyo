*Elroyo* is a general purpose, jack of all trades, operations oriented, modular Slack chat bot. It was built using Flask and runs as a Lambda serverless application managed by the awesome [Zappa](https://github.com/Miserlou/Zappa) framework.

### Requirements

* Python 3.6
* A Slack app
* An AWS account


### Getting Started

##### Create your Slack application

You will first need to create a Slack app that supports slash commands in your workspace. It's easy and the how-to is very well explained on the [Slack API documentation](https://api.slack.com/slash-commands#getting_started). If you already have one, you can skip this step. In any case, the Request URL will be the API Gateway endpoint below.

##### Configuration

After checking the repository, configure your `config.yaml` and `zappa_settings.json` basing off the examples provided. For example, you might want to launch your Lambda on a VPC. Check all the available [Zappa settings](https://github.com/Miserlou/Zappa#advanced-settings) and set your configuration as you desire. You can then run `pip install -r requirements.txt`

##### Deployment

Run `zappa deploy prod`. This will package your code, upload it to S3, create the API Gateway proxy, Lambda, and do everything in between for you. You will get an endpoint as the output, which you have to set on the Request URL of the Slack slash command.