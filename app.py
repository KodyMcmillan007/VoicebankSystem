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
@app.route('/')
def home():
    return redirect(url_for('play_track', track_id=0))
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
    unedited_query = ("""SELECT *
            FROM Voicebank
            """)
    cursor.execute(unedited_query)
    results = cursor.fetchall()
    print(results)
    return render_template('devdex.html', send_data = results)
    
@app.route('/interfacesearch.html')
#-------------DEBUG---------------------------------
def test_function():
    # Collect all data of main table
    db = sqlite3.connect("voicebank.db")
    cursor = db.cursor()
    unedited_query = ("""SELECT *
            FROM Voicebank
            """)
    cursor.execute(unedited_query)
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
            voicebank_by_name_query = (f"""SELECT ID
            FROM Voicebank
            WHERE Name = '{voicesongs}';
            """)
            cursor.execute(voicebank_by_name_query)
            results = cursor.fetchall()

        except:
            print ("System Failure")
        print(results)
#---------------------------------------------------
        if len(results) != 0:
            name_equal_to_storage_query = (f"""SELECT songs_id
            FROM voicebank_songs
            WHERE voicebank_id = {results[0][0]};
            """)
            cursor.execute(name_equal_to_storage_query)
            search_types = cursor.fetchall()
            # If name is equal to the song storage of Voicebank, store songs
            for j in search_types:
                print("j",j)
                song_id_query = ("""SELECT Name
                FROM Songs
                WHERE ID = ?;
                """)
                cursor.execute(song_id_query,(j))
                song_name = cursor.fetchall()
                print("Name", song_name)
                storage_text += " || " +str(song_name[0][0])
            print ("bleh", storage_text)
        else:
            storage_text = ("Please Insert A Stored Data")
        print ("boo",storage_text)
        print ("Kody", results)
#---------------------------------------------------
    cursor = db.cursor()
    sql = ("""SELECT *
            FROM Voicebank
            """)
    cursor.execute(sql)
#---------------------------------------------------
    db = sqlite3.connect("voicebank.db")
    cursor = db.cursor()
    #gets all voicebanks
    voice_bank_query = ("""SELECT * 
        FROM Voicebank""")
    cursor.execute(voice_bank_query)
    results_base = cursor.fetchall()
    results = []
#---------------------------------------------------

    for voice_bank in results_base:
        #gets the voice bank's company from the voice bank db
        company_id = voice_bank[2]
        company_query = (f"""SELECT * 
        FROM Company
        WHERE ID = {company_id};
        """)
        cursor.execute(company_query)
        results_company = cursor.fetchall()
        company_string = results_company[0][1]

        #gets the voice bank's type from the voice bank db
        type_id = voice_bank[4]
        type_query = (f"""SELECT * 
        FROM Types
        WHERE ID = {type_id};
        """)
        cursor.execute(type_query)
        results_type = cursor.fetchall()
        type_string = results_type[0][1]
        #-------------------------------------------
        new_voice_bank = tuple((voice_bank[0],voice_bank[1], company_string, voice_bank[3],type_string, voice_bank[5]))
        results.append(new_voice_bank)
    return render_template('interfacesearch.html', send_song_data = storage_text, final = results)
#---------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
#---------------------------------------------------