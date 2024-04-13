from flask import Flask
from flask import render_template

app=Flask(__name__)



@app.route("/home")
def home():
    return render_template("pages/home.html")


@app.route("/about")
def about():
    return render_template("pages/about.html")

@app.route("/contact")
def contact():
   return render_template("pages/contact.html")


@app.route("/service")
def service():
    return render_template("pages/services.html")

if __name__=="__main__":#port=backend
    app.run(port=4000,debug=True)