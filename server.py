from flask import Flask, render_template, request
import covid19_stateprediction as cov
app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/graph', methods=["GET","POST"])
def my_link():
    if request.method == 'POST':
        result = request.form
        state = result['state']
        html = cov.lambda_handler(state)
        return render_template('graph.html')

if __name__ == '__main__':
  app.run(debug=True)