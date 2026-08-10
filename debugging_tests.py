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
    Temp_Company_Voicebank = []
    Company_Voicebank = []
    Temp_Type_Voicebank = []
    Type_Voicebank = []
#---------------------------------------------------
    for i in voicebank_temp:
        sql1 = (f"""SELECT Name 
        FROM Company 
        WHERE ID = {i};
        """)
        Temp_Company_Voicebank.append(sql1)
    for i in Temp_Company_Voicebank:
        Company_Voicebank.append(2)(i)
    print (Company_Voicebank)
#---------------------------------------------------
    for k in voicebank_temp:
        sql2 = (f"""SELECT Name
        FROM Type
        WHERE ID = {k};
        """)
        Type_Voicebank.append(sql2)
        print (Type_Voicebank)
#---------------------------------------------------
    #for i in range(len(voicebank_temp)):
        #voicebank_temp[i][2] = Company_Voicebank[i]
    #print (Company_Voicebank)
#---------------------------------------------------
    #for i in range(len(voicebank_temp)):
        #voicebank_temp[i][4] = Type_Voicebank[i]
    
#---------------------------------------------------
    complete_voicebank = voicebank_temp
    #print (complete_voicebank)
voicebank_cycle()