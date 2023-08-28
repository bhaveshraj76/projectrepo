from flask import Flask, request, jsonify

app = Flask(__name__)

MAX_HISTORY_SIZE = 20
operations_history = []

@app.route('/')
def list_endpoints():
    routes = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            routes.append(rule.endpoint)

    return jsonify({'endpoints': routes})

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        question = data['question']
        answer = eval(question)
        operations_history.append(question)

        if len(operations_history) > MAX_HISTORY_SIZE:
            operations_history.pop(0)

        response_data = {'question': question, 'answer': answer}
        return jsonify(response_data)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/history')
def history():
    return jsonify({'history': operations_history})


if __name__ == '__main__':
    app.run(host='localhost', port=3000)