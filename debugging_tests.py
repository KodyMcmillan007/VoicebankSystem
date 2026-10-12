import sqlite3
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
    counter = 0
    print(voicebank_temp[0])
    for i in (voicebank_temp[0]):
        vocaloid_temp = []
        for j in range(len(i)):
            if j == 2:
                vocaloid_temp.append(a[counter][0][0])
            elif j == 4:
                vocaloid_temp.append(b[counter][0][0])
            else:
                vocaloid_temp.append(i[j])
        counter += 1

        vocaloid_list.append(vocaloid_temp)

        print (vocaloid_temp)        
    print(vocaloid_list)
#---------------------------------------------------
    complete_voicebank = vocaloid_list



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
    #return render_template('interfacesearch.html', send_data = results)
#-------------DEBUG ENDS----------------------------


#---------------------------------------------------
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
        # Cycle through all and collect all data using HTML functions for producers.
    producer_request = ("producer_id")
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
    return None
#---------------------------------------------------

voicebank_producers()