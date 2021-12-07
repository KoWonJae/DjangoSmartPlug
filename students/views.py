from django.shortcuts import render
import pymysql
from datetime import datetime
import json
from django.http import JsonResponse
import numpy as np
# Create your views here.
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import matplotlib.ticker as mticker

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
            if(result['sn'] == s_no):                               
                return JsonResponse({"result": "fail",
                                    "reason": "이미 등록된 기기입니다"})
        except:

            eproduct = ( s_no, s_type, s_id)
            sql = "insert into Device (sn, type, user_id) values (%s, %s, %s)"
            curs2.execute(sql, eproduct)
            conn2.commit()
           
            return JsonResponse({"result" : "pass"})


def get_current2(request):
    
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
            return JsonResponse({"result": -1})
        else :
            return JsonResponse({"result": data['wat']})


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
                return JsonResponse({"result": "pass"})
            else:
                return JsonResponse({"result": "fail",
                                    "reason": "이미 등록된 기기입니다"})
        except:

            return JsonResponse({"result": "fail",
                                    "reason": "이미 등록된 기기입니다"})

def add_cur_wat(request):
    if request.method == 'GET':
        s_no = request.GET['sn']
        s_wat = request.GET['w']
        now = datetime.now()

        conn = pymysql.connect(host='database-1.crfozxaqi7yk.ap-northeast-2.rds.amazonaws.com', user='admin',
                               password='wj092211', db='smartplug')
        curs = conn.cursor(pymysql.cursors.DictCursor)

        sql = "select * from Device where sn = %s"
        curs.execute(sql, s_no)
        data = curs.fetchone()

        #sn 등록 여부 검색
        if(data == None):
            return render(request, 'minus.html')
        #아두이노가 꺼져있는지 확인
        if(data['power'] == False):
            return render(request, 'off.html')
        user_id = data['user_id']

        sql = "select count from CurrentWattage where sn = %s order by count desc limit 1"
        curs.execute(sql, s_no)
        count = curs.fetchone()
        if(count['count'] == None):
            count = 0
        count = count['count'] + 1

        #현재 전력량 데이터 삽입
        eproduct = (user_id, s_no, s_wat, now, count)
        sql = "insert into CurrentWattage values (%s, %s, %s, %s, %s)"
        curs.execute(sql, eproduct)
        conn.commit()

        #누적 전력량 데이터 삽입
        if (count % 360 == 0):
            add_acc_wat(request, conn, curs, user_id, s_no)

        #limit 제한 넘는지 확인
        month = datetime.today().month
        sql = "select sum(wat) from AccumulateWattage a LEFT JOIN Device d ON (a.sn = d.sn) where d.user_id = %s and " \
              "d.type = %s and month(a.send_time) = %s "

        acc_wat_eproduct = (user_id, data["type"], month)
        curs.execute(sql, acc_wat_eproduct)
        acc_wat = curs.fetchone()

        if (data['limit'] != None):
            if (acc_wat['sum(wat)'] > data['limit']):
                turn_off(request, conn, curs, user_id, data['type'])
                return render(request, 'off.html')

        #친구id와 비교 및 제어
        if (data['friend_id'] != None):
            acc_wat_eproduct = (data['friend_id'], data['type'], month)
            curs.execute(sql, acc_wat_eproduct)
            friend_acc_wat = curs.fetchone()
            if (acc_wat['sum(wat)'] > friend_acc_wat['sum(wat)'] * 1.2):
                turn_off(request, conn, curs, user_id, data['type'])
                return render(request, 'off.html')


    return render(request, 'on.html') #  __ON__ -> __OFF__ #/off
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
            return JsonResponse({"result": -1})
        else:
            return JsonResponse({"result": data['wat']})


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

        return JsonResponse({"result": result})
        
def get_statistics(request):
    if request.method == 'POST':
            data = json.loads(request.body)
            id = data["id"]
            type = data['type']
            conn = pymysql.connect(host='database-1.crfozxaqi7yk.ap-northeast-2.rds.amazonaws.com', user='admin',
                           password='wj092211', db='smartplug')
            curs = conn.cursor(pymysql.cursors.DictCursor)
            sql = "SELECT wat FROM CurrentWattage c LEFT JOIN Device d ON (c.sn = d.sn) where d.user_id = %s and d.type = %s order by count desc limit 10 "
            box = (id, type)
            curs.execute(sql, box)
            data = curs.fetchall()

            y = []
            for i in data:
                y.append(float(i['wat']))
            # print(y)
            conn.commit()
            x = np.arange(0,10)
            # print(x)
            now= datetime.now()
            current_time = str(datetime.now())

            fig = plt.figure(figsize=(5,2))            
            
            print('파일이름'+__file__)
            print('상대위치'+os.path.realpath(__file__))
            plt.plot(x,y)
            path = './font/NanumGothic-Bold.ttf'
            fontprop = fm.FontProperties(fname=path, size=11)            

            
            plt.title("최근 열흘 사용량", fontproperties = fontprop)
            plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f W'))
            plt.ylabel("사용 전력량", fontproperties = fontprop)
            plt.xlabel('사용일', fontproperties = fontprop)
            plt.savefig('media/%s%s%s%sgraph.png' %(now.day, now.hour, now.minute, now.second))
            
            
            graph_name = 'http://13.125.200.206:8000/media/%s%s%s%sgraph.png' %(now.day, now.hour, now.minute, now.second)
            # graph_name = '%s%s%s%sgraph.png' %(now.day, now.hour, now.minute, now.second)
            # plt.savefig('%s%s%s%sgraph.png' %(now.day, now.hour, now.minute, now.second))
            # plt.show()
            return JsonResponse({'result': graph_name})
            

#전원 켜기
def turn_on(request, conn, curs, s_id, s_type):
    sql = "select * from Device where user_id = %s and type = %s"
    eproduct = (s_id, s_type)
    curs.execute(sql, eproduct)
    result = curs.fetchone()

    if (result == None):
        return render(request, 'fail.html')

    sql = "UPDATE Device SET power=True WHERE sn = %s"
    curs.execute(sql, result['sn'])
    conn.commit()
    return

#url로 전원 끄기
def url_turn_on(request):
    if request.method == 'POST':
        conn = pymysql.connect(host='database-1.crfozxaqi7yk.ap-northeast-2.rds.amazonaws.com', user='admin',
                               password='wj092211', db='smartplug')
        curs = conn.cursor(pymysql.cursors.DictCursor)

        data = json.loads(request.body)
        s_id = data["id"]
        s_type = data["type"]
    turn_on(request, conn, curs, s_id, s_type)
    return JsonResponse({"result": "pass"})
 
#전원 끄기    
def turn_off(request, conn, curs, s_id, s_type):
    sql = "select * from Device where user_id = %s and type = %s"
    eproduct = (s_id, s_type)
    curs.execute(sql, eproduct)
    result = curs.fetchone()

    if(result == None):
        return render(request, 'fail.html')

    sql = "UPDATE Device SET power=False WHERE sn = %s"
    curs.execute(sql, result['sn'])
    conn.commit()
    return

#url로 전원 끄기
def url_turn_off(request):
    if request.method == 'POST':
        conn = pymysql.connect(host='database-1.crfozxaqi7yk.ap-northeast-2.rds.amazonaws.com', user='admin',
                               password='wj092211', db='smartplug')
        curs = conn.cursor(pymysql.cursors.DictCursor)

        data = json.loads(request.body)
        s_id = data["id"]
        s_type = data["type"]
    turn_off(request, conn, curs, s_id, s_type)
    return JsonResponse({"result": "pass"})

#제한 걸기
def add_limit(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        s_id = data["id"]
        s_type = data["type"]
        s_limit = data["limit"]
        conn = pymysql.connect(host='database-1.crfozxaqi7yk.ap-northeast-2.rds.amazonaws.com', user='admin',
                               password='wj092211', db='smartplug')
        curs = conn.cursor(pymysql.cursors.DictCursor)

        sql = "select sn from Device where user_id = %s and type = %s"
        eproduct = (s_id, s_type)
        curs.execute(sql, eproduct)
        data = curs.fetchone()

        sql = "UPDATE Device SET Device.limit = %s WHERE sn = %s"
        eproduct = (s_limit, data["sn"])
        curs.execute(sql, eproduct)
        conn.commit()

        return JsonResponse({"result": "pass"})

#친구랑 비교
def add_friend_id(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        s_id = data["id"]
        s_type = data["type"]
        s_friend_id = data["friend_id"]

        mon = datetime.today().month

        conn = pymysql.connect(host='database-1.crfozxaqi7yk.ap-northeast-2.rds.amazonaws.com', user='admin',
                               password='wj092211', db='smartplug')
        curs = conn.cursor(pymysql.cursors.DictCursor)

        sn_eproduct = (s_id, s_type)
        sql = "select sn from Device where user_id = %s and type = %s"
        curs.execute(sql, sn_eproduct)
        sn = curs.fetchone()

        sql = "UPDATE Device SET friend_id = %s WHERE sn = %s"
        eproduct = (s_friend_id, sn['sn'])
        curs.execute(sql, eproduct)
        conn.commit()

    return JsonResponse({"result": "pass"})

#임시 짬통
def friend_compare(request, conn, curs, s_id, s_type, month):
    sql = "select sum(wat) from AccumulateWattage2 a LEFT JOIN Device d ON (a.sn = d.sn) where d.user_id = %s and d.type = %s and month(a.send_time) = %s"
    eproduct = (s_id, s_type, month)
    curs.execute(sql, eproduct)
    my_result = curs.fetchone()
    if (my_result == None):
        return JsonResponse({"result": "fail",
                             "reason": "등록되지 않은 기기입니다"})

    sql = "select sum(wat) from AccumulateWattage2 a LEFT JOIN Device d ON (a.sn = d.sn) where d.user_id = %s and d.type = %s and month(a.send_time) = %s"
    eproduct = (s_friend_id, s_type, month)
    curs.execute(sql, eproduct)
    friend_result = curs.fetchone()
    if (friend_result == None):
        return JsonResponse({"result": "fail",
                             "reason": "등록되지 않은 사용자입니다"})

    if (my_result["my_result"] >= friend_result["friend_result"] * 1.2):
        temp_eproduct = (s_id, s_type)
        sql = "select sn from Device where user_id = %s and type = %s"
        curs.execute(sql, temp_eproduct)
        sn = curs.fetchone()

        sql = "UPDATE Device SET power=False WHERE sn = %s"
        curs.execute(sql, sn['sn'])
        conn.commit()
        return JsonResponse({"result" : "pass"})
