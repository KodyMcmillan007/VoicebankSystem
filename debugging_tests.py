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
    print ("-----------------------------")
    print (voicebank_temp)
#---------------------------------------------------
    complete_voicebank = vocaloid_list
voicebank_cycle()