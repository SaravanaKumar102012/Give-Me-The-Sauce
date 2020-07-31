from flask import Flask,render_template,request

import source

app = Flask(__name__)

@app.route("/",methods = ["GET","POST"])
def main():
    if request.method == "POST":
        data = request.form["number"]
        content = source.initialize(int(data))
        download = source.download(content)
        direct = request.form["Directory"]
        if direct == "":
                download.download(None,lambda x,y:x)
        else:
            download.download(direct,lambda x,y:x)
    return render_template("main.html")

@app.route("/here")
def test():
    return "POST method teste"

if __name__ == "__main__":
    app.run(debug=True)