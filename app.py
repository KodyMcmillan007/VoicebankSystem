from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
#---------------------------------------------------
def get_song_list():
    '''The get song list uses a system to connect
    towards the static folder, this than drags out all
    data within the static folder. Once this happens, it
    cycles through all files that end with mp3 or wav;
    which than is stored for later use.'''
    # System to scan the static directory for audito files
    static_dir = os.path.join(app.root_path, 'static')
#-------------DEBUG---------------------------------
    print ("\n" + "="*50)
    if os.path.exists(static_dir):
        all_files = os.listdir(static_dir)
        print(f"DEBUG: ALL File Found within inside that folder: {all_files}")
    else:
        print("DEBUG: ERROR LOG, The static folder does not exist at this path")
    print("="*50 + "\n")
#-------------DEBUG ENDS----------------------------
    if os.path.exists(static_dir):
        listy = sorted([f for f in os.listdir(static_dir) if f.endswith(('.mp3', '.wav'))])
        #---------------WIP REWORK-------------
        #listy = {f[:-4]:f for f in os.listdir(static_dir) if f.endswith(('.mp3', '.wav'))}
        #---------------WIP REWORK--ENDS-------
        print(listy)
        return listy
    return []
#---------------------------------------------------
@app.route('/')
def home():
    return redirect(url_for('play_track', track_id=0))
#---------------------------------------------------
@app.route('/companyinformation.html')
def company_information():
    return render_template('companyinformation.html') 
#---------------------------------------------------
@app.route("/play/<int:track_id>")
def play_track(track_id):
    '''play track uses the information gathered from get song list
    to than format all stored data to than be moved over using the render
    template into the index html; this is done by cracking a track list and comparing
    it to different variables. '''
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
#--------------------------------------------------- 
@app.route('/copyright.html')
def copyright():
    return render_template('copyright.html') 
#---------------------------------------------------
@app.route('/show_table', methods=['POST'])
def table_shower():
    '''The Table_Shower allows a request form pull to happen between the html
    side and the python backend, allowing us to drag out the function of show_table.
    
    The secondary function of this def function is to prerun the voicebank_songs def, 
    allowing it to run the functions of that def function as if it had all the required code;
    which it doesn't, its simply mimicing the ability to do said code and then rendering it
    to tableshower.html'''
    print(request.form.getlist("show_table"))
    
    results, storage_text = voicebank_songs()

    return render_template('tableshower.html', final = results, send_song_data = storage_text)   
#---------------------------------------------------
@app.route('/tableshowerproducer.html', methods=['POST'])
def shower_producer():
    '''The shower_producer uses a very basic way to store all values from the
    producer table; by simply doing a query to store all functional data into one area
    and than sending said data into the web page.
    
    This data is than sorted into a basic easy table to be read for end users.'''
    db = sqlite3.connect("voicebank.db")
    cursor = db.cursor()
    full_producers = ("""SELECT *
            FROM Producer
            """)
    cursor.execute(full_producers)
    results = cursor.fetchall()
    return render_template('tableshowerproducer.html', send_table = results)
#---------------------------------------------------
@app.route('/interfacesearch.html', methods=['GET', 'POST'])
def search_interface():
    results, storage_text = voicebank_songs()
    return render_template('interfacesearch.html', final = results, send_song_data = storage_text)
#---------------------------------------------------
def voicebank_songs():
    '''voicebank songs, is a two part function which does two
    different things; the first is to store the data of the base database
    to than overlay the base database, it's than cycled through and comapred to 
    song ids that match what the user requested. This is than once more cycled through
    to match all song id's that match which voicebank the user called, which is finally
    sent through into a render template.
    
    The secondary part is to create a brand new table, instead of using the base
    database system; this secondary part creates a brand new list of the overall data,
    by cycling through to store the orginal data it than creates temporay lists/storage
    for the company and type functions. Which is then turned from raw numbers into their
    actual names; which is then reappended back into a new final list, and then finally
    pushed into the render template to be turned into a table.'''
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
    return results, storage_text
#---------------------------------------------------
@app.route('/interface_producersearch.html', methods=['GET', 'POST'])
def voicebank_producers():
    '''Voicebank_producers is a def function to call forward the information for interface page
    based on finding informaiton by comparing the producers of songs by the information the user
    wishes to ask the system itself.
    
    By following the same first function of the def voicebank_songs this own def function can create
    a similar output of code and functionality.'''
    # Holds the text for later use
    Storage_producer_text = ""
    # Search types left as empty
    search_types = None
    if request.method == "POST":
        # Cycle through all and collect all data using HTML functions for producers.
        producer_request = request.form.get("producer_id")
        print(producer_request)
        db = sqlite3.connect("voicebank.db")
        cursor = db.cursor()
        try:
            producer_by_name_query = (f"""SELECT ID
            FROM Producer
            WHERE Name = '{producer_request}';
            """)
            cursor.execute(producer_by_name_query)
            results = cursor.fetchall()

        except:
            print ("System Failure")
        print(results)
    #---------------------------------------------------
        if len(results) != 0:
            name_equal_to_storage_query = (f"""SELECT Name
            FROM Songs
            WHERE Producer = {results[0][0]};
            """)
            cursor.execute(name_equal_to_storage_query)
            search_types = cursor.fetchall()
            #------------------------------------------
            search_types = [song[0] for song in search_types]
            print(" || ".join(search_types))
            Storage_producer_text = (" || ".join(search_types))
            
        else:
            Storage_producer_text = ("Please Insert A Stored Data")
    return render_template("interface_producersearch.html", send_data = Storage_producer_text)
#---------------------------------------------------
@app.route('/interface_producer&voicebank_by_songs.html', methods=['GET', 'POST'])
def voicebank_producer_voicebank():
    ''''''
    # Holds text for later use
    Storage_producer_text = ""
    Storage_voicebank_text = ""
    # Search types left as empty
    search_types_songs = None
    search_types_producer = None
    search_types_voicebank = None
    if request.method == "POST":
        # Cycle through all and collect all data using HTML functions for song of choice.
        song_request = request.form.get("song_id")
        db = sqlite3.connect("voicebank.db")
        cursor = db.cursor()
        try:
            song_by_name_query = (f"""SELECT ID
            FROM Songs
            WHERE Name = '{song_request}';
            """)
            cursor.execute(song_by_name_query)
            results_song = cursor.fetchall()

        except:
            print ("Complete System failure")  
        print(results_song)
    #---------------------------------------------------
        if len(results_song) != 0:
            name_equal_to_storage_query_songs = (f"""SELECT voicebank_id
            FROM voicebank_songs
            WHERE songs_id = {results_song[0][0]};
            """)
            cursor.execute(name_equal_to_storage_query_songs)
            search_types_songs = cursor.fetchall()
            search_types_songs = [song[0] for song in search_types_songs]
            print (search_types_songs)
            #-----------------------------------------------
            name_equal_to_storage_query_producer = (f"""SELECT Producer
            FROM Songs 
            WHERE ID = {results_song[0][0]};
            """)
            cursor.execute(name_equal_to_storage_query_producer)
            search_types_producer = cursor.fetchall()
            search_types_producer = [producer[0] for producer in search_types_producer]
            print (search_types_producer)
            #-----------------------------------------------
            name_equal_to_storage_query_voicebank = (f"""SELECT Name
            FROM Voicebank
            WHERE ID = {search_types_songs[0]};
            """)
            print(name_equal_to_storage_query_voicebank)
            cursor.execute(name_equal_to_storage_query_voicebank)
            search_types_voicebank = cursor.fetchall()
            search_types_voicebank = [voicebank[0] for voicebank in search_types_voicebank]
            print (search_types_voicebank)
            #-----------------------------------------------
            print (" || ".join(str(search_types_producer)))
            print (" || ".join(search_types_voicebank))
            #-----------------------------------------------
            Storage_producer_text = (" || ".join(str(search_types_producer)))
            Storage_voicebank_text = (" || ".join(search_types_voicebank))
        else: 
            Storage_producer_text = ("Value is missing for storage_producer_text")
            Storage_voicebank_text = ("Value is missing for storage_voicebank_text")

    return render_template("interface_producer&voicebank_by_songs.html", send_data_producer = Storage_producer_text, send_data_voicebank = Storage_voicebank_text)
#---------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
#---------------------------------------------------