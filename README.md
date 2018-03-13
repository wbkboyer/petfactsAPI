# petfactsAPI
API for petfacts slackbot using flask.

## Creating a new Slack APP
1) Add new app to your workspace
2) Activate Incoming webhooks
    - allows post requests to be made to webhook url to post to specific channel in workspace
3) Select appropriate scope for app
    - in our case, need to be able to post to channels as app, add commands, access workspace's profile information
4) Add a bot user bundled with the app
5) Main bulk of work will be performed in Slash Commands

## Slash Commands
- Create New command
- enter request url (need static ip address at the very least to a computer running a server capable of receiving post requests)
    - Content-type header set as application/x-www-form-urlencoded
- When configuring your slash command, you'll find a toggle that enables this translation of channel names and user names into their correlated IDs. It's labeled: Escape channels, users, and links sent to your app.
- Slash commands are not namespaced. This means multiple commands can occupy the same name. If it happens and a user tries to invoke the command, they will always invoke the one that was installed most recently. I
- When your server receives the above data, you should validate whether to service the request by confirming that the token value matches the validation token you received from Slack when creating the command. The token is available in the "Basic information" section of your app's configuration. It's not the same token as the one used to submit Web API requests, but instead a kind of shared secret.
    - make sure to store your token value as salted and hashed value in your database, and perform comparison of that value with salted and hashed version of the token received when you receive a request
    - If the token or workspace are unknown to your application, you should refuse to service the request and return an error instead.
- Your URL should respond with a HTTP 200 "OK" status code. Any other flavor of response will result in a user-facing error.
    - That said, we strongly recommend that you send some kind of positive affirmation to the user as an ephemeral response, even if it's just a simple confirmation that the command was understood.

- By default, the response messages sent to commands will only be visible to the user that issued the command (we call these "ephemeral" messages). However, if you would like the response to be visible to all members of the channel in which the user typed the command, you can add a response_type of in_channel to the JSON response, like this:

{
    "response_type": "in_channel",
    "text": "It's 80 degrees right now.",
    "attachments": [
        {
            "text":"Partly cloudy today and tomorrow"
        }
    ]
}

    - recommend always declaring your intended response_type.

Slash commands that are installed as part of a Slack app are also able to use message buttons to drive interactive workflows with precision and clarity.

When responding to a command invocation or executing a response_url, include your message button actions as attachments to your message.
Responding to the user with an error message

If you would like to let the user know that something went wrong, you can return an ephemeral response containing a helpful error message. To do this, you can either respond directly to the slash command request, or use the provided response_url.

You'll want to send a JSON payload that looks like this:

{
  "response_type": "ephemeral",
  "text": "Sorry, that didn't work. Please try again."
}

- Username handling changed: https://api.slack.com/changelog/2017-09-the-one-about-usernames

- Available API's:
    - https://api.slack.com/web
    - https://api.slack.com/events-api
    - https://api.slack.com/rtm

        - Seems like I'll be using Web and RTM api's primarily

- "Slash commands that are part of a Slack app set in "distributed mode" must support HTTPS and serve a valid SSL certificate. Self-signed certificates are not allowed. Check out CloudFlare or Let's Encrypt for easy ways to obtain valid certificates.

Before submitting a command to your server, Slack will occasionally send your command URLs a simple POST request to verify the certificate. These requests will include a parameter ssl_check set to 1 and a token parameter. The token value corresponds to the verification token registered with your app's slash command. See command verification for more information on validating verification tokens. Mostly, you may ignore these requests, but please do respond with a HTTP 200 OK."


## Initial implementation:

- one database table for users who have made queries
- one database table for pet facts
    - when was the last time this fact was accessed? if more than X days, allow repeat
- one table for log entries
    - user who made query
    - timestamp
    - response code
    - short log (reason for code)

IDEAS for EXTENSIONS:
- prank someone with given pet facts
    - only sends ephemeral response
        - use the "Delayed responses with multiple responses" section so that a person might receive multiple messages over, say, a day
        - After first ephemeral response, allow receiving user to block all future petfacts?
    - posts to personal channel with the targetted user
        https://api.slack.com/methods/chat.postEphemeral
    - send ephemeral message to originating user if the intended user is not in the channel
    - keep track of how often someone is spamming private messages; if they are being annoying, ban them from using cat facts for a certain period
        - simplest implementation would basically mean that globally, if a user is receiving too many pet facts, sending to them will be halted for at least a few hours
        - keep track of how many requests a user is making per minute; ban them for a day if they go over a certain number in total (i.e. even if they're sending to different users, not just spamming the same user)
- user can set their favorite animal, and can recieve facts about their chosen favorite animal


# References
1. Grinberg, Miguel. [Designing a RESTful API with Python and Flask](https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask)May 20, 2013. Accessed: February 26, 2018
1. [How to setup Flask with gunicorn and nginx with examples](https://tutorials.technology/tutorials/71-How-to-setup-Flask-with-gunicorn-and-nginx-with-examples.html) October 6, 2017. Accessed: February 26, 2018
1. [How To Serve Flask Applications with Gunicorn and Nginx on Ubuntu 14.04](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-14-04) March 20, 2015. Accessed February 26, 2018
1. [Gunicorn can't find app when name changed from “application”
](https://stackoverflow.com/questions/33379287/gunicorn-cant-find-app-when-name-changed-from-application/33379650) Stackexchange post from October 27, 2015. Accessed: February 26, 2018
1. [Build a Restful API with Flask the TDD way](https://scotch.io/tutorials/build-a-restful-api-with-flask-the-tdd-way). May 3, 2017. Accessed: February 26, 2018
1. [SQLite Python: Insert Rows](http://www.sqlitetutorial.net/sqlite-python/insert/). Accessed February 27, 2018
1. [Flask-restful](https://flask-restful.readthedocs.io/en/latest/)
1. [SQLite Functions - Datetime](https://www.techonthenet.com/sqlite/functions/datetime.php)
1. [Server-side Logic to handle Slack Slash Commands using Python and Flask](https://gist.github.com/devStepsize/59c15d850e82a77e539b8ff3d5cb5cad). Accessed: March 1, 2018.
1. Liao, Peiyu. [Flask App with Gunicorn on Nginx server upon AWS EC2 Linux](https://pyliaorachel.github.io/blog/tech/system/2017/07/07/flask-app-with-gunicorn-on-nginx-server-upon-aws-ec2-linux.html). July 7, 2017. Accessed: March 12, 2018
