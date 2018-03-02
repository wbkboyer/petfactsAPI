#!flask/bin/python
from flask import request, jsonify, abort

application = Flask()

# The parameters included in a slash command request (with example values):
#   token=gIkuvaNzQIHg97ATvDxqgjtO
#   team_id=T0001
#   team_domain=example
#   channel_id=C2147483705
#   channel_name=test
#   user_id=U2147483697
#   user_name=Steve
#   command=/weather
#   text=94070
#   response_url=https://hooks.slack.com/commands/1234/5678

@app.route('/fetchfact', methods=['POST'])
def fetch_fact():
    """Parse the command parameters, validate them, and respond.
    Note: This URL must support HTTPS and serve a valid SSL certificate.
    """
    # Parse the parameters you need
    token = request.form.get('token', None)  # TODO: validate the token
    command = request.form.get('command', None)
    text = request.form.get('text', None)
    # Validate the request parameters
    if not token:  # or some other failure condition
        abort(400)

    return jsonify({'response_type': 'in_channel',
                    'text': 'foo'
                    })

if __name__ == "__main__":
    application.run(debug=True, host="0.0.0.0")

