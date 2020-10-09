from flask import Flask, render_template , request

app = Flask(__name__)

@app.route('/')
def page_return():
    return render_template("Select_area.html")

@app.route('/area', methods=['POST'])
def result():
    if request.method == 'POST':
        place = request.form['input1']

    return place


if __name__ == '__main__' :
    app.run() 


    







