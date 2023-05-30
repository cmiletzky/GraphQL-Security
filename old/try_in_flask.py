from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def handle_post():
    content = request.get_json()
    # process the incoming JSON data and generate a response
    response_data = {
        'message': 'Server received the following data:',
        'data': content
    }
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(port=40000)
