from flask import Flask, request, jsonify

app = Flask(__name__)
last_result = None

@app.route('/reverse', methods=['GET'])
def reverse():
    global last_result
    input_string = request.args.get('in', '')
    if not input_string:
        return jsonify({"error": "Missing 'in' query parameter"}), 400
    last_result = ' '.join(reversed(input_string.split()))
    return jsonify({"result": last_result})

@app.route('/restore', methods=['GET'])
def restore():
    if not last_result:
        return jsonify({"error": "No result to restore"}), 400
    return jsonify({"result": last_result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
