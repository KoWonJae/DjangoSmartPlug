from django.shortcuts import render
import pymysql
from datetime import datetime
import json
# Create your views here.
def regEproduct(request):
    return render(request, 'eproducts.html')

#get은 사용자가 받아오는거 
#add는 사용자가 추가    
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


def get_current2(request):
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
        # sql = "select s_wat from Device left inner join Eproducts3 on (Device.sn = Eproducts3.s_no) where Device.user_id = '%s' "
        # sql = "SELECT s_wat FROM Eproducts3 e LEFT JOIN Device d ON (e.s_no = d.sn) where d.user_id = 'TEST_ID_001'"
        # sql = "SELECT s_wat FROM Eproducts3 e LEFT JOIN Device d ON (e.s_no = d.sn) where d.user_id = 's_id'"
        sql = "SELECT s_wat FROM Eproducts3 e LEFT JOIN Device d ON (e.s_no = d.sn) where d.user_id = %s"
        curs.execute(sql, s_id)
        data = curs.fetchone()
        if(data == None):
            return render(request, 'minus.html', {'s_wat':data})
        else :
            return render(request, 'data3.html', data)
            
def get_current(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        s_id = data["id"]
        s_type = data["type"]
        conn = pymysql.connect(host='database-1.crfozxaqi7yk.ap-northeast-2.rds.amazonaws.com', user='admin',
                               password='wj092211', db='smartplug')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT wat FROM CurrentWattage c LEFT JOIN Device d ON (c.sn = d.sn) where d.user_id = %s and d.type = %s"
        eproduct = (s_id, s_type)
        curs.execute(sql, eproduct)
        data = curs.fetchone()

        if(data == None):
            return render(request, 'minus.html')
        else :
            return render(request, 'data3.html', {'s_wat' : data['wat']})


def del_device(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        s_id = data["id"]
        s_no = data["sn"]
        conn = pymysql.connect(host='database-1.crfozxaqi7yk.ap-northeast-2.rds.amazonaws.com', user='admin', password='wj092211', db='smartplug')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        
        query = "SELECT * FROM Device where sn = %s"
        curs.execute(query, s_no)
        result = curs.fetchone()
        try:
            if(result['sn'] == s_no and result['user_id'] ==  s_id):
                del_query = "DELETE FROM Device where sn = %s"
                curs.execute(del_query, s_no)
                conn.commit()
                return render(request, 'pass.html', {'s_no':s_id, 's_wat':s_no})
            else:
                return render(request, 'fail.html', {'s_no':s_id, 's_wat':s_no})
        except:

            return render(request, 'fail.html', {'s_no':s_id, 's_wat':s_no})

#id wat send_time sn
def add_cur_wat(request):
    if request.method == 'GET':
        s_no = request.GET['sn']
        s_wat = request.GET['w']
        now = datetime.now()

        conn = pymysql.connect(host='database-1.crfozxaqi7yk.ap-northeast-2.rds.amazonaws.com', user='admin',
                               password='wj092211', db='smartplug')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        sql = "select user_id from Device where sn = %s"
        curs.execute(sql, s_no)
        user_id = curs.fetchone()
        if(user_id == None):
            return render(request, 'minus.html')
        user_id = user_id['user_id']

        sql = "select count from CurrentWattage where sn = %s order by count desc limit 1"
        curs.execute(sql, s_no)
        count = curs.fetchone()
        count = count['count'] + 1

        eproduct = (user_id, s_no, s_wat, now, count)
        print(eproduct)
        sql = "insert into CurrentWattage values (%s, %s, %s, %s, %s)"
        curs.execute(sql, eproduct)
        conn.commit()

        if (count % 360 == 0):
            add_acc_wat(request, conn, curs, user_id, s_no)

    return render(request, 'data2.html')



#360개 더해서 누적전력량에 추가
def add_acc_wat(request,conn, curs, user_id, sn):
    sql = "select wat from CurrentWattage2 order by count desc limit 360"
    curs.execute(sql)
    wat = 0
    data = curs.fetchall()

    for i in data:
        wat += float(i['wat'])

    now = datetime.now()
    eproduct = (user_id, wat, now , sn)
    sql = "INSERT INTO AccumulateWattage2 (id, wat, send_time, sn) VALUES (%s, %s, %s, %s)"
    curs.execute(sql, eproduct)
    conn.commit()
    return eproduct
    
# 누적전력량에서 가져오기    
def get_accumulate(request):
    # add_acc_wat()
    if request.method == 'POST':
        data = json.loads(request.body)
        s_id = data["id"]
        s_type = data["type"]
        conn = pymysql.connect(host='database-1.crfozxaqi7yk.ap-northeast-2.rds.amazonaws.com', user='admin',
                               password='wj092211', db='smartplug')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT wat FROM AccumulateWattage2 a LEFT JOIN Device d ON (a.sn = d.sn) where d.user_id = %s and d.type = %s"
        eproduct = (s_id, s_type)
        curs.execute(sql, eproduct)
        data = curs.fetchone()

        if (data == None):
            return render(request, 'minus.html')
        else:
            return render(request, 'data3.html', {'s_wat' : data['wat']})


def get_average(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        s_id = data["id"]
        conn = pymysql.connect(host='database-1.crfozxaqi7yk.ap-northeast-2.rds.amazonaws.com', user='admin',
                               password='wj092211', db='smartplug')
        curs = conn.cursor(pymysql.cursors.DictCursor)

        sql = "select DISTINCT type from Device where user_id = %s"
        curs.execute(sql, s_id)
        data = curs.fetchall()

        mon = datetime.today().month
        result = []

        for i in data:
            sql = "select avg(wat) from AccumulateWattage2 a LEFT JOIN Device d ON (a.sn = d.sn) where d.user_id = %s and d.type = %s and month(a.send_time) = %s"
            eproduct = (s_id, i['type'], mon)
            curs.execute(sql, eproduct)
            my_data = curs.fetchone()

            sql = "select avg(wat) from AccumulateWattage2 a LEFT JOIN Device d ON (a.sn = d.sn) where d.user_id != %s and d.type = %s and month(a.send_time) = %s"
            curs.execute(sql, eproduct)
            other_data = curs.fetchone()

            try:
                if(my_data['avg(wat)'] > other_data['avg(wat)']):
                    result.append(i['type'])
            except:
                continue




        return render(request, 'data3.html', {'s_wat':result})