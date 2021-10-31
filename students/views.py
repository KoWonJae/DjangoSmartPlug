from django.shortcuts import render
import pymysql

# Create your views here.
def regEproduct(request):
    return render(request, 'eproducts.html')
def get_main(request):
    return render(request, 'main.html')
def get_post(request):
    if request.method == 'GET':
        s_no = request.GET['s_no']
        s_wat = request.GET['s_wat']
        data = {
            'data':s_no,
            #'s_wat':s_wat,
        }
        
        conn = pymysql.connect(host='database-1.crfozxaqi7yk.ap-northeast-2.rds.amazonaws.com', user='admin', password='wj092211', db='smartplug')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        eproduct = (s_no, s_wat)
        sql = "insert into Eproducts values (%s, %s)"
        curs.execute(sql, eproduct)
        conn.commit()
           
    return render(request, 'data.html', {'s_no':s_no, 's_wat':s_wat})
    #return render(request, 'data.html', data)