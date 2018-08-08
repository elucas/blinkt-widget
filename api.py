from flask import Flask, jsonify, url_for, request
import status

# for a quick intro into Flask web-servers I recommend:
# raspberrypi.org/learning/python-web-server-with-flask/worksheet

app = Flask(__name__)


@app.route('/', methods=['POST'])
def refresh():
    the_new_status = request.form['new_status']
    status.change_status(the_new_status)
    return status.get_status()


@app.route('/api', methods=['GET'])
def api_status():
    """Returns the current status data as JSON.

    e.g.
    {
        u'status': u'offline',
        u'callable_statuses_list': [
            u'available', u'busy', u'engaged', \
u'alert', u'disturbable', u'partying', u'offline', u'brb'
        ]
    }
    """
    status_dictionary = {
        'status': status.get_status(),
        'endpoint': url_for('refresh', _external=True),
        'callable_statuses_list': status.read_statuses(),
        'device_type': status.get_type()
    }

    return jsonify(status_dictionary)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True)
# "threaded=True" fixes timeout issues (somehow...)
