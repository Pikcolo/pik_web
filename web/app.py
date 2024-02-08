from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route("/")
def Home():
    return render_template("index.html")

@app.route("/About")
def About():
    services =['ตัดหญ้า', 'ทำความสะอาดบ้าน', 'รับจ้างเล่นเกมแทน' ,'สอนการบ้าน', 'ขับรถรับ-ส่ง']
    return render_template("About.html", my_services = services )

if __name__ == "__main__":
    app.run(debug=True)