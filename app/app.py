# ----------------- Write your code below this line. -------------------- #
import os
from io import BytesIO

from flask import Flask, render_template, request

from config import config
from hotdogclassifier import HotDogClassifier

#creating an instance of the Flask app
app = Flask(__name__)

model = HotDogClassifier()
model.load_model(config["model_weight"])

# a feature that adds functionality to the code : route()
@app.route("/", methods=["GET"])
def home():
      """
      return "Hello World!"
      it will get info and return to hello world
      """
    return render_template("index.html", flag=False project_description=config["project_description"], project_name=config["project_name"])
      #render_template() flask will look into the templates folder for the template tell to look for.
#we are receiving info
@app.route("/", methods=["POST"])
#will extract file request abd convert it to bytes so it can be readable.
def classify():
    uploaded_file = request.files["files"]
    data = BytesIO(uploaded_file.read())
    #check whether file is empty. If it's thecase no prediction will be made.
    if uploaded_file.filename != "":
        img, predicted = model.predict(data)
    else:
        predicted, img = "", ""
    return render_template("index.html", predicted=predicted, img=img, flag=True, project_description=config["project_description"], project_name=config["project_name"])


# ----------------- You do NOT need to understand what the code below does. -------------------- #

if __name__ == '__main__':
    PORT = os.environ.get('PORT') or 8080
    DEBUG = os.environ.get('DEBUG') != 'TRUE'
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)
