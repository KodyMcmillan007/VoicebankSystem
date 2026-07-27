from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
#---------------------------------------------------
def get_song_list():
    # System to scan the static directory for audito files
    static_dir = os.path.join(app.root_path, 'static')
    if os.path.exists(static_dir):
        return sorted([f for f in os.listdir(static_dir) if f.endswith(('.mp3', '.wav'))])
    return []
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

    return render_template('index.html', send_data = results), redirect(url_for('play_track', track_id=0))
#---------------------------------------------------
@app.route("/play/<int:track_id>")
def play_track(track_id):
    songs = get_song_list()

    # If no songs exist in the current state, show empty
    if not songs:
        return render_template('index.html', current_song=None, next_id=None, songs=songs, current_id=None)

    if track_id >= len(songs) or track_id < 0:
        return redirect(url_for('play_track', track_id=0))
    current_song = songs[track_id]

    next_id = track_id + 1 if (track_id + 1) < len(songs) else 0

    return render_template(
        'index.html',
        current_song=current_song,
        next_id=next_id,
        songs=songs,
        current_id=track_id
    )
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