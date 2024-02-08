from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route("/")
def Home():
    return render_template("index.html")

@app.route("/About")
def About():
    services =['ให้อาหารปลา', 'ทำความสะอาดบ้าน', 'รับจ้างฟาร์มเลเวลในเกม' ,'สอนการบ้าน', 'ขับรถรับ-ส่ง' , 'รับจ้างพาไปต่างโลก']
    return render_template("About.html", my_services = services )

if __name__ == "__main__":
    app.run(debug=True)