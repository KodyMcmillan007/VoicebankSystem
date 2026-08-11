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
        #print (Temp_Company_Voicebank)
    for j in i:
        Company_Voicebank.append(j[2])
    print("-----------------------------------")
    print (Company_Voicebank)
    print("-----------------------------------")
    a = []
    for i in Company_Voicebank:
        sql2 = (f"""SELECT Name FROM Company WHERE ID = {i}""")
        cursor.execute(sql2)
        results_company = cursor.fetchall()
        a.append(results_company)
    print (a)
#---------------------------------------------------
    for k in voicebank_temp:
        sql3 = (f"""SELECT Name
        FROM Type
        WHERE ID = {k};
        """)
        Type_Voicebank.append(sql3)
        #print (Type_Voicebank)
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