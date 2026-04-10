from flask import Flask, render_template, jsonify
from analytics import analytics_bp

app = Flask(__name__)
app.register_blueprint(analytics_bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/test')
def test_api():
    return jsonify({'message': 'Backend is running!', 'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
