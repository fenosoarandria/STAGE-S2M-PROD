import pyodbc

def runQuery(sql=None):
    user = "s2mweb"
    pwd = "servinfo"
    dsn = "DRIVER=iSeries Access ODBC Driver;SYSTEM=10.161.0.243;DBQ=QGPL"

    connection = pyodbc.connect(dsn, user=user, password=pwd)
    cursor = connection.cursor()
    cursor.execute(sql)

    lignes = []
    for row in cursor.fetchall():
        ligne = {}
        for i, col in enumerate(cursor.description):
            ligne[col[0]] = row[i]
        lignes.append(ligne)
    cursor.close()
    connection.close()
 
    return lignes