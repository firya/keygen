from flask import Flask, render_template, make_response, jsonify, request
from generator import Generator

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("adgenerator.html")


@app.route('/api/v1.0/generate', methods=['POST'])
def get_tasks():
    if not request.json:
        abort(400)

    gen = Generator(request.json)
    cartesian = gen.generate()

    return jsonify(cartesian)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    app.run()
