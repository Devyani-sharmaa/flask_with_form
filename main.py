from flask import Flask,request
from flask import render_template,redirect
from flask_sqlalchemy import SQLAlchemy
import DateTime
import os
from flask_mail import Mail,Message

app=Flask(__name__)


# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///myfirstwebdb.db"
# initialize the app with the extension
#db.init_app(app)
db=SQLAlchemy(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']="devyanibrd123@gmail.com"
app.config['MAIL_PASSWORD']="hhjt lrkr fuvq ahan"
app.config['MAIL_USE_SSL']=True
app.config['MAIL_USE_TLS ']=False

mail=Mail(app)

class contactus(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String)
    phn_no=db.Column(db.Text)
    message=db.Column(db.Text)
    img_path=db.Column(db.String)
    date=db.Column(db.DateTime,server_default=db.func.now())

  

with app.app_context():
    db.create_all()





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
    data=contactus.query.all()
    return render_template("pages/services.html",mydata=data)





@app.route("/savethisdata",methods=["POST"])
def datasaving():
    if request.method=="POST":
        usernasme=request.form.get("fname")
        email=request.form.get("email")
        
        phone=request.form.get("phn")
        message=request.form.get("msg")
        image=request.files.get("img")

        if image:
            image.save(os.path.join("static/userimg",image.filename))
            path=os.path.join("static/userimg",image.filename)

        # return f"username //is {username},user email:{email}:{email},user phn no is:{phone},and user message is:{message}"
    
        page=contactus(username= usernasme,email=email,phn_no= phone,message=message,img_path=path)

        db.session.add(page)
        db.session.commit()

        msg=Message("testing", sender="devyanibrd123@gmail.com", recipients=["devanshscience@gmail.com"])
        msg.body = "HELLO DEVANSH"
        mail.send(msg)

        return redirect("/service")

    return "data saved"

@app.route ("/deletethisdate/<int:xyz>")
def deletethisnow(xyz):
    data=contactus.query.get(xyz)
    db.session.delete(data)
    db.session.commit()
    #return f"card id is: {xyz}"
    return redirect("/service")

@app.route("/update/<int:abc>")
def updatethis(abc):
    data=contactus.query.get(abc)
    return render_template("pages/updatedata.html",data=data)



@app.route("/updatedatanow/<int:abc>",methods=["POST"])
def updatethisu(abc):
        data=contactus.query.get(abc)
        if request.method=="POST":
            username=request.form.get("fname")
            email=request.form.get("email")
            phone=request.form.get("phn")
            message=request.form.get("msg")

          
            data.username = username
            data.email = email
            data.phn_no=phone
            data.message=message

            db.session.commit()
            return redirect("/service")
        


        #return render_template("pages/updatedata.html",data=data)



if __name__=="__main__":#port=backend
    app.run(port=4000,debug=True)