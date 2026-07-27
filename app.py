from flask import Flask, render_template, request
import sqlite3
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
#---------------------------------------------------
@app.route("/")
def home():
    db = sqlite3.connect("voicebank.db")
    cursor = db.cursor()
    sql = ("""SELECT *
            FROM Voicebank
            """)
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template('index.html', send_data = results)

#---------------------------------------------------
@app.route('/devdex.html')
def dev_system():
    db = sqlite3.connect("voicebank.db")
    cursor = db.cursor()
    sql = ("""SELECT *
            FROM Voicebank
            """)
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template('devdex.html', send_data = results)
#---------------------------------------------------
@app.route('/copyright.html')
def copyright():
    return render_template('copyright.html')
#---------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)