from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flex.db'
db = SQLAlchemy(app)

class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String, nullable = False)

    def __repr__(self):
        return '<Item {}>'.format(self.item)


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        db.session.delete(Items.query.filter_by(item=request.form['name']).first())
        db.session.commit()
    return redirect(url_for('main'))

@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('flextable.html', x=[x.item for x in Items.query.all()])

if __name__ == '__main__':
    app.run(debug=True)