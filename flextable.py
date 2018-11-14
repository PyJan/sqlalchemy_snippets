from flask import Flask, request, render_template, url_for, redirect


app = Flask(__name__)

x = ['prvni', 'druhy', 'treti', 'ctvrty']

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        print(request.form['name'])
    return redirect(url_for('main'))

@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('flextable.html', x=x)

if __name__ == '__main__':
    app.run(debug=True)