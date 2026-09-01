import sqlite3
def voicebank_cycle():
    db = sqlite3.connect("voicebank.db")
    cursor = db.cursor()
    voice_bank_query = ("""SELECT * 
        FROM Voicebank""")
    cursor.execute(voice_bank_query)
    results_base = cursor.fetchall()
#---------------------------------------------------
    for voice_bank in results_base:
        company_id = voice_bank[2]
        
        company_query = (f"""SELECT * 
        FROM Company
        WHERE ID = {company_id};
        """)
        cursor.execute(company_query)
        results_company = cursor.fetchall()
        company_string = results_company[0][1]
        print ("Company", results_company)
        #-------------------------------------------
        type_id = voice_bank[4]
        type_query = (f"""SELECT * 
        FROM Types
        WHERE ID = {type_id};
        """)
        cursor.execute(type_query)
        results_type = cursor.fetchall()
        type_string = results_type[0][1]
        print ("Type", results_type)
        #-------------------------------------------


#---------------------------------------------------
voicebank_cycle()