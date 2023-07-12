from flask import Flask, request
from ga_report import popular_report
import os

app = Flask(__name__)

@app.route("/generate_popular_report")
def generate_popular_report():
    if request.args.get('dest_file'):
        dest_file = request.args.get('dest_file')
    else:
        dest_file = 'popular.json'
    if request.args.get('extra_field'):
        extra_field = request.args.get('extra_field')
    else:
        extra_field = ''
    if 'GA_RESOURCE_ID' in os.environ:
        ga_id = os.environ['GA_RESOURCE_ID']
    else:
        ga_id = "311149968"
    popular_report(ga_id, dest_file, extra_field)
    return "ok"

if __name__ == "__main__":
    app.run()
