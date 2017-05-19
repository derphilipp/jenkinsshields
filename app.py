import json
import requests
from flask import Flask, Response

app = Flask(__name__)


def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# @app.route('/<jenkinsurl>/<shieldsurl>/<project>/<branch>/<warningsid>/<displayname>/<jsonentry>')
# def hello_world(jenkinsurl, shieldsurl, project, branch, warningsid, displayname, jsonentry):

@app.route('/<path:path>')
def hello_world(path):
    path = path.split("/")
    if len(path) < 7:
        value = 'Invalid URL'
        color = 'red'
        displayname = 'Invalid URL'
        shieldsurl = 'shields.io'
    else:
        jenkinsurl, shieldsurl, project, branch, warningsid, displayname, *jsonentry = path
        domain = ".sdi.site"
        url = "http://{}{}/job/{}/job/{}/lastBuild/{}/api/json".format(jenkinsurl, domain, project, branch, warningsid)
        try:
            data = requests.get(url).json()
            if jsonentry is str:
                value = str(data[jsonentry])
            else:
                for j in jsonentry:
                    data = data[j]
                value = str(data)
            if RepresentsInt(value):
                if int(value) > 0:
                    color = 'yellow'
                else:
                    color = 'green'
            else:
                color = 'blue'
        except ValueError:
            value = 'unknown'
            color = 'grey'
    url = 'http://{}/badge/{}-{}-{}.svg'.format(shieldsurl, displayname, value, color)
    data = requests.get(url)
    response = Response(data.content)
    response.headers["Content-Type"] = "image/svg+xml"
    response.headers["Vary"] = "Accept-Encoding"
    # response.headers["Content-Disposition"] = "attachment; filename=filename.svg"
    # return data.content
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
