from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
#---------------------------------------------------
def get_song_list():
    # System to scan the static directory for audito files
    static_dir = os.path.join(app.root_path, 'static')
#-------------DEBUG---------------------------------
    print ("\n" + "="*50)
    print(f"DEBUG: Flask is searching for music within in:\n {static_dir}")

    if os.path.exists(static_dir):
        all_files = os.listdir(static_dir)
        print(f"DEBUG: ALL File Found within inside that folder: {all_files}")
    else:
        print("DEBUG: ERROR LOG, The static folder does not exist at this path")
    print("="*50 + "\n")
#-------------DEBUG ENDS----------------------------
    if os.path.exists(static_dir):
        listy = sorted([f for f in os.listdir(static_dir) if f.endswith(('.mp3', '.wav'))])
        print(listy)
        return listy
    return []
#---------------------------------------------------
@app.route("/")
def home():
    song_list = get_song_list()
    db = sqlite3.connect("voicebank.db")
    cursor = db.cursor()
    sql = ("""SELECT *
            FROM Voicebank
            """)
    cursor.execute(sql)
    return render_template(
            'index.html',
            current_song=song_list[0],
            next_id=song_list[0],
            songs=song_list,
            current_id=song_list[0],
        )
#---------------------------------------------------
@app.route('/')
def index():
    return redirect(url_for('static','play_track', track_id=0))
#---------------------------------------------------
@app.route("/play/<int:track_id>")
def play_track(track_id):
    songs = get_song_list()

    # If no songs exist in the current state, show empty
    if not songs:
        return render_template('index.html', current_song=None, next_id=None, songs=songs, current_id=None)
    # Find next track within the song
    if track_id >= len(songs) or track_id < 0:
        return redirect(url_for('play_track', track_id=0))
    current_song = songs[track_id]

    next_id = track_id + 1 if (track_id + 1) < len(songs) else 0
    # Add songs into the index system
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
    # Collect all data of main table
    db = sqlite3.connect("voicebank.db")
    cursor = db.cursor()
    sql = ("""SELECT *
            FROM Voicebank
            """)
    cursor.execute(sql)
    results = cursor.fetchall()
    print(results)
    return render_template('devdex.html', send_data = results)
    
@app.route('/interfacesearch.html')
#-------------DEBUG---------------------------------
def test_function():
    # Collect all data of main table
    db = sqlite3.connect("voicebank.db")
    cursor = db.cursor()
    sql = ("""SELECT *
            FROM Voicebank
            """)
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template('interfacesearch.html', send_data = results)
#-------------DEBUG ENDS----------------------------
@app.route('/copyright.html')
def copyright():
    return render_template('copyright.html')
#---------------------------------------------------
@app.route('/interfacesearch.html', methods=['GET', 'POST'])
def voicebank_songs():
    # Storage text to hold data
    storage_text = ""
    # Search types left as empty
    search_types = None
    # Check if the user has clicked the submit button
    if request.method == 'POST':
        # Cycle Through and collect all data using HTML 'name' attributes
        voicesongs = request.form.get("voicebank_id")
        db = sqlite3.connect("voicebank.db")
        cursor = db.cursor()
        try:
            sql = (f"""SELECT ID
            FROM Voicebank
            WHERE Name = '{voicesongs}';
            """)
            cursor.execute(sql)
            results = cursor.fetchall()

        except:
            print ("System Failure")
        print(results)
#---------------------------------------------------
        if len(results) != 0:
            sql = (f"""SELECT songs_id
            FROM voicebank_songs
            WHERE voicebank_id = {results[0][0]};
            """)
            cursor.execute(sql)
            search_types = cursor.fetchall()
            # If name is equal to the song storage of Voicebank, store songs
            for j in search_types:
                sql = ("""SELECT Name
                FROM Songs
                WHERE ID = ?;
                """)
                cursor.execute(sql,(j))
                song_name = cursor.fetchall()
                storage_text += " || " +str(song_name[0][0])
            print (storage_text)
        else:
            storage_text = ("Please Insert A Stored Data")
        print (storage_text)
        print (results)
    return render_template('interfacesearch.html', send_song_data = storage_text)
#---------------------------------------------------
@app.route('/interfacesearch.html', methods=['GET', 'POST'])
def voicebank_cycle():
    db = sqlite3.connect("voicebank.db")
    cursor = db.cursor()
    sql = ("""SELECT *
            FROM Voicebank
            """)
    cursor.execute(sql)
    resultsbase = cursor.fetchall()
#---------------------------------------------------
    voicebank_temp = [resultsbase]

    Company_Voicebank = []

    Type_Voicebank = []
#---------------------------------------------------
    for i in voicebank_temp:
        sql1 = (f"""SELECT Name 
        FROM Company 
        WHERE ID = {i};
        """)
    for j in i:
        Company_Voicebank.append(j[2])
    a = []
    for i in Company_Voicebank:
        sql2 = (f"""SELECT Name FROM Company WHERE ID = {i}""")
        cursor.execute(sql2)
        results_company = cursor.fetchall()
        a.append(results_company)
    for k in voicebank_temp:
        sql3 = (f"""SELECT Name
        FROM Types
        WHERE ID = {k};
        """)
    for l in k:
        Type_Voicebank.append(l[4])
    b = []
    for c in Type_Voicebank:
        sql4 = (f"""SELECT Name FROM Types WHERE ID = {c}""")
        cursor.execute(sql4)
        results_type = cursor.fetchall()
        b.append(results_type)
    print (b)
#---------------------------------------------------
    vocaloid_list = []
    for i in (voicebank_temp[0]):
        vocaloid_temp = []
        for j in range(len(i)):
            if j == 2:
                vocaloid_temp.append(a[j][0][0])
            elif j == 4:
                vocaloid_temp.append(b[j][0][0])
            else:
                vocaloid_temp.append(i[j])

        vocaloid_list.append(vocaloid_temp)

        print (vocaloid_temp)
    print(vocaloid_list)
#---------------------------------------------------
    complete_voicebank = vocaloid_list
    return render_template('interfacesearch.html', send_completed = complete_voicebank[0])
#---------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
#---------------------------------------------------