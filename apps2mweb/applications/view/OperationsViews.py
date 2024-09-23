from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from django.template import loader,RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.db import connections
import json
from .ODBCconnect import runQuery

import datetime

def Accueil(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())

@csrf_exempt
def Det_Operations(request):
    if request.method == "POST" :
        code = request.POST.get('code')
        tab = []
        try :
            sql = "SELECT CAST(CIDIVP as char(3) CCSID 37) as CIDIVP,NARTAR,LARTAR,CEANAR,CRAYAR,CFAMAR,CSFAAR,CSECAR,CAST(CTHEVP as char(4) CCSID 37) as CTHEVP, PVTCVP,PPTCVP,DDVAVP,DFVAVP " 
            sql += "FROM B31SDFHMDG.FHPRVP00 "
            sql += "LEFT JOIN B33STFCMDG.FTARTP00 ON NARTVP = NARTAR "
            sql += f"WHERE CTHEVP = '{code}'"
            res = runQuery(sql)
            for row in res :
                tab.append(
                    [
                        row['CIDIVP'],
                        row['NARTAR'],
                        row['LARTAR'],
                        row['CEANAR'],
                        row['CRAYAR'],
                        row['CFAMAR'],
                        row['CSFAAR'],
                        row['CSECAR'],
                        row['CTHEVP'],
                        "{:,}".format(round(row['PVTCVP'],2)),
                        "{:,}".format(round(row['PPTCVP'],2)),
                        row['DDVAVP'],
                        row['DFVAVP']
                    ]
                )
        except :
            return JsonResponse({"error": "erreur SQL"}, status=405)

        result = {
            "draw": int(request.GET.get("draw", 0)),
            "recordsTotal": "",
            "recordsFiltered": "",
            "data": tab           
        }
        
        return JsonResponse(result)
    else:
        return JsonResponse({"error": "erreur de programme"}, status=405)
    
def Promo(request):
    template = loader.get_template('gestionsoperationspromo.html')
    return HttpResponse(template.render())

@csrf_exempt
def Rech_Operations(request):
    if request.method == "POST" :
        debut = request.POST.get('deb')
        fin = request.POST.get('fin')
        try : 
            tab = []
            deb = debut.split("-")
            fin = fin.split("-")
            datedebut = str(deb[0][-2:])+str(deb[1])+str(deb[2])
            datefin = str(fin[0][-2:])+str(fin[1])+str(fin[2])
            sql = f"SELECT CTHETM,LTHETM,DDVVTM,DFVVTM FROM B33STFCMDG.FTTHEP00 f WHERE ((CTHETM LIKE '%J%')  OR (CTHETM LIKE '%S%')) AND SSUPTM = 0 AND DDVVTM BETWEEN {datedebut} AND {datefin} "
            res = runQuery(sql)
            for row in res :
                now = datetime.date.today()
                year = now.year
                month = now.month
                day = now.day
                dateInt = f"{year:04d}{month:02d}{day:02d}"
                dateInt = dateInt[-6:]
                diff = int(row['DFVVTM']) - int(dateInt)
                
                action = f'<button type = "button" class="btn btn-info btn-rounded btn-sm" onclick="getdetail(\'{row["CTHETM"]}\',\'{row["LTHETM"]}\')">Détails</button>'
                if diff <= 2 :
                    action += f'<button class="btn btn-warning btn-rounded btn-sm" onclick="balisage(\'{row["CTHETM"]}\',\'{row["LTHETM"]}\')">Balisage</button>'
                if int(dateInt) >= int(row['DFVVTM']) :
                    action += f'<button class="btn btn-success btn-rounded btn-sm" onclick="resultat(\'{row["CTHETM"]}\')">Résultat</button>'
                tab.append([row['CTHETM'],row['LTHETM'],row['DDVVTM'],row['DFVVTM'],action])
                
        except :
            tab = []
            
        result = {
            "draw": int(request.GET.get("draw", 0)),
            "recordsTotal": "",
            "recordsFiltered": "",
            "data": tab           
        }
        return JsonResponse(result)
    else:
        return JsonResponse({"error": "erreur de programme"}, status=405)


@csrf_exempt
def Bal_operations(request):
    if request.method == "POST" :
        code = request.POST.get('code')
        tab = []
        try :
            sql = "SELECT CAST(CIDIVP as char(3) CCSID 37) as CIDIVP,NARTAR,LARTAR,CEANAR,CRAYAR,CFAMAR,CSFAAR,CSECAR,CAST(CTHEVP as char(4) CCSID 37) as CTHEVP, PVTCVP,PPTCVP,DDVAVP,DFVAVP " 
            sql += "FROM B31SDFHMDG.FHPRVP00 "
            sql += "LEFT JOIN B33STFCMDG.FTARTP00 ON NARTVP = NARTAR "
            sql += f"WHERE CTHEVP = '{code}'"
            res = runQuery(sql)
            for row in res :
                tab.append(
                    [
                        row['NARTAR'],
                        row['LARTAR'],
                        "{:,}".format(round(row['PVTCVP'],0)),
                        "{:,}".format(round(row['PPTCVP'],0)),
                        '<input type="number" name="nombrebal" class = "form-control input-sm" >',
                        '<select class = "form-control" name="select_formats">'+
                            '<option value = "0">Choisir format</option>'+
                            '<option value = "PetitFormat">Petit format</option>'+
                            '<option value = "GrandFormat">Grand format</option>'+
                            '<option value = "FormatA4">Format A4</option>'+
                        '</select>'

                    ]
                )
        except :
            return JsonResponse({"error": "erreur SQL"}, status=405)

        result = {
            "draw": int(request.GET.get("draw", 0)),
            "recordsTotal": "",
            "recordsFiltered": "",
            "data": tab           
        }
        
        return JsonResponse(result)
    else:
        return JsonResponse({"error": "erreur de programme"}, status=405)