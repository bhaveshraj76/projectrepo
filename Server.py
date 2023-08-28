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

    return jsonify({'endpoints': routes})from flask import Flask, request, jsonify

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

def perform_calculation(components):
    try:
        result = float(components[0])
        operator = None

        for component in components[1:]:
            if component in ['plus', 'minus', 'into', 'divided_by']:
                operator = component
            else:
                num = float(component)
                if operator == 'plus':
                    result += num
                elif operator == 'minus':
                    result -= num
                elif operator == 'into':
                    result *= num
                elif operator == 'divided_by':
                    result /= num
        return result
    except Exception as e:
        return str(e)

@app.route('/calculate/<path:input_string>')
def calculate(input_string):
    operators = ['plus', 'minus', 'into', 'divided_by']
    components = input_string.split('/')
    components = [comp for comp in components if comp]  # Remove empty components

    if any(comp not in operators and not comp.replace('.', '', 1).isdigit() for comp in components):
        return jsonify({'error': 'Invalid input'})

    result = perform_calculation(components)
    operations_history.append(input_string)

    if len(operations_history) > MAX_HISTORY_SIZE:
        operations_history.pop(0)

    response_data = {'input': input_string, 'result': result}
    return jsonify(response_data)

@app.route('/history')
def history():
    return jsonify({'history': operations_history})


if __name__ == '__main__':
    app.run(host='localhost', port=3000)

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
