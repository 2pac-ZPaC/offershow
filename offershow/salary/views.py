#coding:utf-8
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from models import OfferInfo,OfferEvaluate
import json
import datetime
from django.db.models import Sum
from django.db.models import Q
from django.db import connection
class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

def get_client_ip(request):
    try:
        real_ip = request.META['HTTP_X_FORWARDED_FOR']
        regip = real_ip.split(",")[0]
    except:
        try:
            regip = request.META['REMOTE_ADDR']
        except:
            regip = ""
    return regip
    # return HttpResponse(regip)

def index(request):
    return render(request, 'index.html')

def left(request):
    return render(request, 'left.html')

def right(request,type='1'):
    print type
    if type == "1":
        offer = OfferInfo.objects.filter(score__gte=0).order_by('-time').values("id","company","city","salary","remark","position","time","score","number")
    if type == "2":
        offer = OfferInfo.objects.filter(score__gte=0).order_by('-score').values("id","company","city","salary","remark","position","time","score","number")
    if type == "3":
        offer = OfferInfo.objects.filter(score__gte=0).order_by('-number').values("id","company","city","salary","remark","position","time","score","number")
    return render(request, 'right.html', {'offer': offer,'type':type})
    # return render(request, 'home.html', {'string': data})

def offerrecord(request):
    if 'company' not in request.POST or \
       'position' not in request.POST or \
       'city' not in request.POST or \
       'salary' not in request.POST or \
       'remark' not in request.POST :
        return HttpResponse(u"薪水创建参数不够")
    else:
        company  = request.POST['company']
        position = request.POST['position']
        city = request.POST['city']
        salary = request.POST['salary']
        remark = request.POST['remark']
    ip = get_client_ip(request)
    try:
        OfferInfo.objects.create(company = company,\
                             position = position,\
                             city = city,\
                             ip = ip,\
                             salary = salary,\
                             remark = remark)
        return HttpResponseRedirect("/right")
    except BaseException, e:
        return HttpResponse(u"系统异常:"+e)

def offerdetail(request,id):
    offerdetail = OfferInfo.objects.get(id=id)
    number = offerdetail.number+1
    OfferInfo.objects.select_for_update().filter(id = id).update(number = number)
    return render(request, 'offerdetail.html', {'offerdetail': offerdetail})

def offerlike(request,id):
    ip = get_client_ip(request)
    print ip
    if OfferEvaluate.objects.filter(ip = ip).filter(offerid = id):
        return HttpResponse(u"已经评价过了，请勿重复点击哦！")
    OfferEvaluate.objects.create(offerid = id,\
                             ip = ip,\
                             typeid = 1)
    score = OfferInfo.objects.get(id=id).score +1
    OfferInfo.objects.select_for_update().filter(id = id).update(score = score)
    return HttpResponse(u"好评成功,谢谢你的支持！")


def offerdislike(request,id):
    ip = get_client_ip(request)
    if OfferEvaluate.objects.filter(ip = ip).filter(offerid = id):
        return HttpResponse(u"已经评价过了，请勿重复点击哦！")
    OfferEvaluate.objects.create(offerid = id,\
                             ip = ip,\
                             typeid = 0)
    score = OfferInfo.objects.get(id=id).score - 1
    OfferInfo.objects.select_for_update().filter(id = id).update(score = score)
    return HttpResponse(u"差评成功,谢谢你的支持！")



def offersearch(request,content=""):
    try:
        type = '2'
        offer = OfferInfo.objects.filter(score__gte=0).filter(Q(company__contains=content)|Q(city__contains=content)|Q(position__contains=content)).order_by('-score').values("id","company","city","salary","remark","position","time","score","number")
        return render(request, 'offersearch.html', {'offer': offer,'type':type})
    except BaseException, e:
        re = {'r': 0, 'msg': u"系统出现错误，无法进行操作"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")





def jobtotal(request):
    try:
        data = OfferInfo.objects.filter(score__gte=0).order_by('-time').values("id","company","city","salary","remark","position","time","score","number")
        info = json.dumps(list(data), cls=CJsonEncoder, ensure_ascii=False)
        re = {'r': 1, 'msg': u"成功查询所有岗位数据信息",'info':json.loads(info)}
        return HttpResponse(json.dumps(re),content_type='application/json',status="201")
    except BaseException, e:
        print e
        re = {'r': 0, 'msg': u"系统出现错误，无法进行操作"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")


def jobrecord(request):
    if 'company' not in request.POST or \
       'position' not in request.POST or \
       'city' not in request.POST or \
       'salary' not in request.POST or \
       'remark' not in request.POST :
        re = {'r': 0, 'msg': u"参数不全，无法插入！"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
    else:
        company  = request.POST['company']
        position = request.POST['position']
        city = request.POST['city']
        salary = request.POST['salary']
        remark = request.POST['remark']
        print 111
    ip = get_client_ip(request)
    try:
        OfferInfo.objects.create(company = company,\
                             position = position,\
                             city = city,\
                             ip = ip,\
                             salary = salary,\
                             remark = remark)
        re = {'r': 1, 'msg': u"成功插入一条岗位数据信息！"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
    except BaseException, e:
        re = {'r': 0, 'msg': u"系统出现错误，无法进行操作"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")

def jobdetail(request,id):
    try:
        jobdetail = OfferInfo.objects.get(id=id)
        number = jobdetail.number+1
        OfferInfo.objects.select_for_update().filter(id = id).update(number = number)
        re = {'r': 1, 'msg': u"成功查询一条岗位数据信息",'info':json.loads(jobdetail.toJSON())}
        return HttpResponse(json.dumps(re),content_type='application/json',status="201")
    except BaseException, e:
        re = {'r': 0, 'msg': u"系统出现错误，无法进行操作"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")


def joblike(request,id):
    ip = get_client_ip(request)
    if OfferEvaluate.objects.filter(ip = ip).filter(offerid = id):
        re = {'r': 0, 'msg': u"已经评价过了，请勿重复点击哦！"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
    try:
        OfferEvaluate.objects.create(offerid = id,\
                             ip = ip,\
                             typeid = 1)
        score = OfferInfo.objects.get(id=id).score +1
        OfferInfo.objects.select_for_update().filter(id = id).update(score = score)
        re = {'r': 1, 'msg': u"好评成功,谢谢你的支持！"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
    except BaseException, e:
        re = {'r': 0, 'msg': u"系统出现错误，无法进行操作"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")

def jobdislike(request,id):
    ip = get_client_ip(request)
    if OfferEvaluate.objects.filter(ip = ip).filter(offerid = id):
        re = {'r': 0, 'msg': u"已经评价过了，请勿重复点击哦！"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
    try:
        OfferEvaluate.objects.create(offerid = id,\
                             ip = ip,\
                             typeid = 0)
        score = OfferInfo.objects.get(id=id).score - 1
        OfferInfo.objects.select_for_update().filter(id = id).update(score = score)
        re = {'r': 1, 'msg': u"差评成功,谢谢你的支持！"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
    except BaseException, e:
        re = {'r': 0, 'msg': u"系统出现错误，无法进行操作"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
 

def jobcount(request):
    try:
        num_sum = OfferInfo.objects.count();
        evaluate_sum = OfferEvaluate.objects.count();
        click_sum = OfferInfo.objects.all().aggregate(Sum('number'))["number__sum"]
        re = {'r': 1, 'msg': u"成功查询数据统计信息",'num_sum':num_sum,'evaluate_sum':evaluate_sum,'click_sum':click_sum}
        return HttpResponse(json.dumps(re),content_type='application/json',status="201")
    except BaseException, e:
        print e
        re = {'r': 0, 'msg': u"系统出现错误，无法进行操作"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")

def jobsearch(request,content=""):
    try:
        data = OfferInfo.objects.filter(score__gte=0).filter(Q(company__contains=content)|Q(city__contains=content)|Q(position__contains=content)).values("id","company","city","salary","remark","position","time","score","number")
        info = json.dumps(list(data), cls=CJsonEncoder, ensure_ascii=False)
        re = {'r': 1, 'msg': u"根据关键字查询结果成功",'info':json.loads(info)}
        return HttpResponse(json.dumps(re),content_type='application/json',status="201")
    except BaseException, e:
        re = {'r': 0, 'msg': u"系统出现错误，无法进行操作"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")


def jobcity(request):
    try:
        cursor = connection.cursor()
        cursor.execute('select city,count(*) from offerinfo where score >= 0 group by city')
        data = cursor.fetchall()
        info = []
        for item in data:
            dic={}
            dic['city']=item[0]
            dic['number']=item[1]
            info.append(dic)
        re = {'r': 1, 'msg': u"成功获取薪水公司分类以及相应总数",'info':info}
        return HttpResponse(json.dumps(re),content_type='application/json',status="201")
    except BaseException, e:
        re = {'r': 0, 'msg': u"系统出现错误，无法进行操作"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")

def jobcompany(request):
    try:
        cursor = connection.cursor()
        cursor.execute('select company,count(*) from offerinfo where score >= 0 group by company ')
        data = cursor.fetchall()
        info = []
        for item in data:
            dic={}
            dic['company']=item[0]
            dic['number']=item[1]
            info.append(dic)
        re = {'r': 1, 'msg': u"成功获取薪水城市分类以及相应总数",'info':info}
        return HttpResponse(json.dumps(re),content_type='application/json',status="201")
    except BaseException, e:
        re = {'r': 0, 'msg': u"系统出现错误，无法进行操作"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")

