from flask import Flask, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["50 per minute" ,"3 per second"]
)

def power(x, y):
    if x and y:
        x = int(x)
        y = int(y)
        return x**y
    return "Invalid data"


@app.route("/")
@limiter.exempt
def info():
    return "<p>This server received 2 number x, y. Then return result of x to the power of y (x^y)</p>"

@app.route("/unprotected")
@limiter.exempt
def unprotected():
    x, y = request.args.get('x'), request.args.get('y')
    return {"res": power(x, y)}

@app.route("/protected")
def protected():
    x, y = request.args.get('x'), request.args.get('y')
    return {"res": power(x, y)}

if __name__ == '__main__':
    app.run(port=8000, host="0.0.0.0", debug=True)