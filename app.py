from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/test')
def test_api():
    return jsonify({'message': 'Backend is running!', 'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
