from flask import Flask, jsonify, request ,render_template
from fractions import Fraction
from fractions import Fraction

app = Flask(__name__)

def get_terminal_states(matrix):
    n = len(matrix)
    # Find terminal states
    terminal_states = []
    for i in range(n):
        if sum(matrix[i]) == 0:
            terminal_states.append(i)
    # Calculate probabilities of reaching each terminal state
    probs = []
    for ts in terminal_states:
        visited = [False] * n
        visited[0] = True
        queue = [0]
        while queue:
            state = queue.pop(0)
            for i, count in enumerate(matrix[state]):
                if count > 0:
                    if i == ts:
                        probs.append(Fraction(count, sum(matrix[state])))
                    elif not visited[i]:
                        visited[i] = True
                        queue.append(i)
    # Convert fractions to integers
    denom = 1
    for p in probs:
        denom = denom * p.denominator // p.gcd(denom)
    result = [p.numerator * denom // p.denominator for p in probs]
    result.append(denom)
    return result



@app.route('/predict_terminal_states', methods=['POST'])
def predict_terminal_states():
    data = request.get_json()
    matrix = data['matrix']
    result = get_terminal_states(matrix)
    return render_template ("index.html" ,result=result)

if __name__ == '__main__':
    app.run(debug=True)
