from django.shortcuts import render
import pymysql
from datetime import datetime
import json
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
    

def get_sensor(request):
    if request.method == 'GET':
        s_no = request.GET['sn']
        s_wat = request.GET['w']
        data = {
            'data':s_no,
            #'s_wat':s_wat,
        }
        now = datetime.now()
        current_time = now.strftime("%m%d%H%M%S")
        current_time = int(current_time)
        
        conn = pymysql.connect(host='database-1.crfozxaqi7yk.ap-northeast-2.rds.amazonaws.com', user='admin', password='wj092211', db='smartplug')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        eproduct = (s_no, current_time, s_wat)
        sql = "insert into Eproducts3 values (%s, %s, %s)"
        curs.execute(sql, eproduct)
        conn.commit()
           
    return render(request, 'data2.html', {'s_no':s_no, 's_wat':s_wat})
    #return render(request, 'data.html', data)
    

def get_device(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        s_id = data["id"]
        s_no = data["sn"]
        s_type = data["type"]
        conn = pymysql.connect(host='database-1.crfozxaqi7yk.ap-northeast-2.rds.amazonaws.com', user='admin', password='wj092211', db='smartplug')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        conn2 = pymysql.connect(host='database-1.crfozxaqi7yk.ap-northeast-2.rds.amazonaws.com', user='admin', password='wj092211', db='smartplug')
        curs2 = conn2.cursor(pymysql.cursors.DictCursor)
        
        query = "SELECT * FROM Device where sn = %s"
        curs.execute(query, s_no)
        result = curs.fetchone()
        try:
            if(result['sn'] == s_no and result['user_id'] ==  s_id):
                return render(request, 'fail.html', {'s_no':s_id, 's_wat':s_no})
        except:

            eproduct = ( s_no, s_type, s_id)
        # query = "select EXISTS (select id from Device where id=찾는 값 limit 1) as success"
        # query2 = "SELECT * FROM user where name = %s"
            sql = "insert into Device values (%s, %s, %s)"
            curs2.execute(sql, eproduct)
            conn2.commit()
           
            return render(request, 'pass.html', {'s_no':s_id, 's_wat':s_no})


def get_current(request):
    # if request.method == 'POST':
        # data = json.loads(request.body)
        # s_id = body["id"]
        # s_no = body["sn"]
        # s_type = body["type"]
        # conn = pymysql.connect(host='database-1.crfozxaqi7yk.ap-northeast-2.rds.amazonaws.com', user='admin', password='wj092211', db='smartplug')
        # curs = conn.cursor(pymysql.cursors.DictCursor)
        # eproduct = ( s_id, s_no, s_type)
        # sql = "insert into Device values (%s, %s, %s)"
        # curs.execute(sql, eproduct)
        # conn.commit()
    if request.method == 'POST':
        data = json.loads(request.body)
        s_id = data["id"]
        s_type = data["type"]
        conn = pymysql.connect(host='database-1.crfozxaqi7yk.ap-northeast-2.rds.amazonaws.com', user='admin',
                               password='wj092211', db='smartplug')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        sql = "select s_wat from Device full outer join Eproducts3 on Device.sn = Eproducts3.s_no where Device.user_id = %s"
        curs.execute(sql, s_id)
        data = curs.fetchone()
        if(data == None):
            return render(request, 'minus.html', {'s_wat':data})
        else :
            return render(request, 'data3.html', {'s_wat':data})




