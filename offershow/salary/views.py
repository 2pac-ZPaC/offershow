#coding:utf-8
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from models import OfferInfo,OfferEvaluate,OfferSearch,OfferMessage,OfferToken
import json
from django.db.models import Sum
from django.db.models import Q
from django.db import connection
# django 加密密码
from django.contrib.auth.hashers import make_password, check_password
import time
import datetime
import logging
logger = logging.getLogger("restful api")
logger.setLevel(logging.DEBUG)
# 建立一个filehandler来把日志记录在文件里，级别为debug以上
fh = logging.FileHandler("restfulapi.log")
fh.setLevel(logging.DEBUG)
# 设置日志格式
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
#将相应的handler添加在logger对象中
logger.addHandler(fh)

class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

def index(request):
    return render(request, 'index.html')

def left(request):
    return render(request, 'left.html')

def right(request,type='1'):
    try:
        if type == "1":
            offer = OfferInfo.objects.filter(score__gte=0).order_by('-time').values()
        if type == "2":
            offer = OfferInfo.objects.filter(score__gte=0).order_by('-score').values()
        if type == "3":
            offer = OfferInfo.objects.filter(score__gte=0).order_by('-number').values()
        return render(request, 'right.html', {'offer': offer,'type':type})
    except BaseException, e:
        return render(request, 'error.html')
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
        return render(request, 'error.html')

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

def offerdetail(request,id):
    try:
        offerdetail = OfferInfo.objects.get(id=id)
        number = offerdetail.number+1
        OfferInfo.objects.select_for_update().filter(id = id).update(number = number)
        comment = OfferMessage.objects.filter(offerid=id).order_by('-time').values()
        return render(request, 'offerdetail.html', {'offerdetail': offerdetail,'comment':comment})
    except BaseException, e:
        return render(request, 'error.html')

def offerlike(request,id):
    try:
        ip = get_client_ip(request)
        if OfferEvaluate.objects.filter(ip = ip).filter(offerid = id):
            return HttpResponse(u"已经评价过了，请勿重复点击哦！")
        OfferEvaluate.objects.create(offerid = id,\
                             ip = ip,\
                             typeid = 1)
        score = OfferInfo.objects.get(id=id).score +1
        OfferInfo.objects.select_for_update().filter(id = id).update(score = score)
        return HttpResponse(u"好评成功,谢谢你的支持！")
    except BaseException, e:
        return render(request, 'error.html')

def offerdislike(request,id):
    try:
        ip = get_client_ip(request)
        if OfferEvaluate.objects.filter(ip = ip).filter(offerid = id):
            return HttpResponse(u"已经评价过了，请勿重复点击哦！")
        OfferEvaluate.objects.create(offerid = id,\
                             ip = ip,\
                             typeid = 0)
        score = OfferInfo.objects.get(id=id).score - 1
        OfferInfo.objects.select_for_update().filter(id = id).update(score = score)
        return HttpResponse(u"差评成功,谢谢你的支持！")
    except BaseException, e:
        return render(request, 'error.html')
def offermessage(request):
    id = request.GET.get('id')
    content = request.GET.get('content')
    try:
        ip = get_client_ip(request)
        OfferMessage.objects.create(offerid = id,\
                             ip = ip,\
                             content = content)
        return HttpResponse(u"留言成功,谢谢你的支持！")
    except BaseException, e:
        return render(request, 'error.html')
def offersearch(request,content=""):
    try:
        ip = get_client_ip(request)
        OfferSearch.objects.create(ip = ip,content = content)
        type = '2'
        offer = OfferInfo.objects.filter(score__gte=0).filter(Q(company__contains=content)|Q(city__contains=content)|Q(position__contains=content)).order_by('-score').values("id","company","city","salary","remark","position","time","score","number")
        return render(request, 'offersearch.html', {'offer': offer,'type':type})
    except BaseException, e:
        return render(request, 'error.html')



# restful接口
#获取访问密钥

# token自己指定规则写，我只是简单的appid+appsecret+时间撮+额外的字符串md5生成的

# def gettoken(request):
#     print 111
#     if 'appid' not in request.POST or 'appsecret' not in request.POST:
#         re = {'r': 0, 'msg': "appid跟appsecret信息不完整,获取失败"}
#         return HttpResponse(json.dumps(re), content_type='application/json',status="201")
#     else:
#         appid = request.POST['appid']
#         appsecret = request.POST['appsecret']
    



def jobtotal(request):
    if 'access_token' not in request.POST:
        re = {'r': 0, 'msg': "你的access_token没传入，请查看参数信息，此参数如若需要请与开发者联系"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
    access_token = request.POST['access_token']
    if not OfferToken.objects.filter(token=access_token):
        re = {'r': 0, 'msg': "你的access_token不存在或是已经过期，此参数如若需要请与开发者联系"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
    try:
        print 111
        data = OfferInfo.objects.filter(score__gte=0).order_by('-time').values("id","company","city","salary","remark","position","time","score","number")
        print data
        info = json.dumps(list(data), cls=CJsonEncoder, ensure_ascii=False)
        print 222
        logger.info(u"调用接口成功 - jobtotal - "+access_token)
        re = {'r': 1, 'msg': u"成功查询所有岗位数据信息，按照最近时间排序",'info':json.loads(info)}
        return HttpResponse(json.dumps(re),content_type='application/json',status="201")
    except BaseException, e:
        print e
        re = {'r': 0, 'msg': u"系统出现错误，无法进行操作"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")

def jobtrust(request):
    if 'access_token' not in request.POST:
        re = {'r': 0, 'msg': "你的access_token没传入，请查看参数信息，此参数如若需要请与开发者联系"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
    access_token = request.POST['access_token']
    if not OfferToken.objects.filter(token=access_token):
        re = {'r': 0, 'msg': "你的access_token不存在或是已经过期，此参数如若需要请与开发者联系"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
    try:
        data = OfferInfo.objects.filter(score__gte=0).order_by('-score').values("id","company","city","salary","remark","position","time","score","number")
        info = json.dumps(list(data), cls=CJsonEncoder, ensure_ascii=False)
        logger.info(u"调用接口成功 - jobtrust - "+access_token)
        re = {'r': 1, 'msg': u"成功查询所有岗位数据信息，按照最可信排序",'info':json.loads(info)}
        return HttpResponse(json.dumps(re),content_type='application/json',status="201")
    except BaseException, e:
        print e
        re = {'r': 0, 'msg': u"系统出现错误，无法进行操作"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")

def jobhot(request):
    if 'access_token' not in request.POST:
        re = {'r': 0, 'msg': "你的access_token没传入，请查看参数信息，此参数如若需要请与开发者联系"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
    access_token = request.POST['access_token']
    if not OfferToken.objects.filter(token=access_token):
        re = {'r': 0, 'msg': "你的access_token不存在或是已经过期，此参数如若需要请与开发者联系"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
    try:
        data = OfferInfo.objects.filter(score__gte=0).order_by('-number').values("id","company","city","salary","remark","position","time","score","number")
        info = json.dumps(list(data), cls=CJsonEncoder, ensure_ascii=False)
        logger.info(u"调用接口成功 - jobhot - "+access_token)
        re = {'r': 1, 'msg': u"成功查询所有岗位数据信息，按照最热门排序",'info':json.loads(info)}
        return HttpResponse(json.dumps(re),content_type='application/json',status="201")
    except BaseException, e:
        print e
        re = {'r': 0, 'msg': u"系统出现错误，无法进行操作"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")



def jobrecord(request):
    if 'access_token' not in request.POST:
        re = {'r': 0, 'msg': "你的access_token没传入，请查看参数信息，此参数如若需要请与开发者联系"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
    access_token = request.POST['access_token']
    if not OfferToken.objects.filter(token=access_token):
        re = {'r': 0, 'msg': "你的access_token不存在或是已经过期，此参数如若需要请与开发者联系"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
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
        logger.info(u"调用接口成功 - jobrecord - "+access_token)
        re = {'r': 1, 'msg': u"成功插入一条岗位数据信息！"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
    except BaseException, e:
        re = {'r': 0, 'msg': u"系统出现错误，无法进行操作"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")

def jobmessage(request):
    if 'access_token' not in request.POST:
        re = {'r': 0, 'msg': "你的access_token没传入，请查看参数信息，此参数如若需要请与开发者联系"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
    access_token = request.POST['access_token']
    if not OfferToken.objects.filter(token=access_token):
        re = {'r': 0, 'msg': "你的access_token不存在或是已经过期，此参数如若需要请与开发者联系"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
    if 'id' not in request.POST or \
       'content' not in request.POST :
        re = {'r': 0, 'msg': u"参数不全，无法插入！"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
    else:
        id  = request.POST['id']
        content = request.POST['content']
    try:
        ip = get_client_ip(request)
        OfferMessage.objects.create(offerid = id,\
                             ip = ip,\
                             content = content)
        logger.info(u"调用接口成功 - jobmessage - "+access_token)
        re = {'r': 1, 'msg': u"留言成功,谢谢你的支持！"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
    except BaseException, e:
        re = {'r': 0, 'msg': u"系统出现错误，无法进行操作"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")

def jobdetail(request):
    if 'access_token' not in request.POST:
        re = {'r': 0, 'msg': "你的access_token没传入，请查看参数信息，此参数如若需要请与开发者联系"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
    access_token = request.POST['access_token']
    if not OfferToken.objects.filter(token=access_token):
        re = {'r': 0, 'msg': "你的access_token不存在或是已经过期，此参数如若需要请与开发者联系"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
    if 'id' not in request.POST :
        re = {'r': 0, 'msg': u"参数不全！"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
    else:
        id = request.POST['id']
    try:
        jobdetail = OfferInfo.objects.get(id=id)
        number = jobdetail.number+1
        OfferInfo.objects.select_for_update().filter(id = id).update(number = number)
        logger.info(u"调用接口成功 - jobdetail - "+access_token+"("+id+")")
        re = {'r': 1, 'msg': u"成功查询一条岗位数据信息",'info':json.loads(jobdetail.toJSON())}
        return HttpResponse(json.dumps(re),content_type='application/json',status="201")
    except BaseException, e:
        re = {'r': 0, 'msg': u"系统出现错误，无法进行操作"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")


def joblike(request):
    if 'access_token' not in request.POST:
        re = {'r': 0, 'msg': "你的access_token没传入，请查看参数信息，此参数如若需要请与开发者联系"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
    access_token = request.POST['access_token']
    if not OfferToken.objects.filter(token=access_token):
        re = {'r': 0, 'msg': "你的access_token不存在或是已经过期，此参数如若需要请与开发者联系"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
    if 'id' not in request.POST :
        re = {'r': 0, 'msg': u"参数不全！"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
    else:
        id = request.POST['id']
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
        logger.info(u"调用接口成功 - joblike - "+access_token+"("+id+")")
        re = {'r': 1, 'msg': u"好评成功,谢谢你的支持！"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
    except BaseException, e:
        re = {'r': 0, 'msg': u"系统出现错误，无法进行操作"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")

def jobdislike(request):
    if 'access_token' not in request.POST:
        re = {'r': 0, 'msg': "你的access_token没传入，请查看参数信息，此参数如若需要请与开发者联系"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
    access_token = request.POST['access_token']
    if not OfferToken.objects.filter(token=access_token):
        re = {'r': 0, 'msg': "你的access_token不存在或是已经过期，此参数如若需要请与开发者联系"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
    if 'id' not in request.POST :
        re = {'r': 0, 'msg': u"参数不全！"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
    else:
        id = request.POST['id']
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
        logger.info(u"调用接口成功 - jobdislike - "+access_token+"("+id+")")
        re = {'r': 1, 'msg': u"差评成功,谢谢你的支持！"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
    except BaseException, e:
        re = {'r': 0, 'msg': u"系统出现错误，无法进行操作"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
 

def jobcount(request):
    if 'access_token' not in request.POST:
        re = {'r': 0, 'msg': "你的access_token没传入，请查看参数信息，此参数如若需要请与开发者联系"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
    access_token = request.POST['access_token']
    if not OfferToken.objects.filter(token=access_token):
        re = {'r': 0, 'msg': "你的access_token不存在或是已经过期，此参数如若需要请与开发者联系"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
    try:
        num_sum = OfferInfo.objects.count();
        evaluate_sum = OfferEvaluate.objects.count();
        click_sum = OfferInfo.objects.all().aggregate(Sum('number'))["number__sum"]
        logger.info(u"调用接口成功 - jobcount - "+access_token)
        re = {'r': 1, 'msg': u"成功查询数据统计信息",'num_sum':num_sum,'evaluate_sum':evaluate_sum,'click_sum':click_sum}
        return HttpResponse(json.dumps(re),content_type='application/json',status="201")
    except BaseException, e:
        print e
        re = {'r': 0, 'msg': u"系统出现错误，无法进行操作"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")

def jobsearch(request):
    if 'access_token' not in request.POST:
        re = {'r': 0, 'msg': "你的access_token没传入，请查看参数信息，此参数如若需要请与开发者联系"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
    access_token = request.POST['access_token']
    if not OfferToken.objects.filter(token=access_token):
        re = {'r': 0, 'msg': "你的access_token不存在或是已经过期，此参数如若需要请与开发者联系"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
    if 'content' not in request.POST :
        re = {'r': 0, 'msg': u"参数不全！"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
    else:
        content = request.POST['content']
    try:
        ip = get_client_ip(request)
        OfferSearch.objects.create(ip = ip,content = content)
        data = OfferInfo.objects.filter(score__gte=0).filter(Q(company__contains=content)|Q(city__contains=content)|Q(position__contains=content)).values("id","company","city","salary","remark","position","time","score","number")
        info = json.dumps(list(data), cls=CJsonEncoder, ensure_ascii=False)
        logger.info(u"调用接口成功 - jobsearch - "+access_token) 
        re = {'r': 1, 'msg': u"根据关键字查询结果成功",'info':json.loads(info)}
        return HttpResponse(json.dumps(re),content_type='application/json',status="201")
    except BaseException, e:
        re = {'r': 0, 'msg': u"系统出现错误，无法进行操作"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")


def jobcity(request):
    if 'access_token' not in request.POST:
        re = {'r': 0, 'msg': "你的access_token没传入，请查看参数信息，此参数如若需要请与开发者联系"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
    access_token = request.POST['access_token']
    if not OfferToken.objects.filter(token=access_token):
        re = {'r': 0, 'msg': "你的access_token不存在或是已经过期，此参数如若需要请与开发者联系"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
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
        logger.info(u"调用接口成功 - jobcity - "+access_token) 
        re = {'r': 1, 'msg': u"成功获取薪水公司分类以及相应总数",'info':info}
        return HttpResponse(json.dumps(re),content_type='application/json',status="201")
    except BaseException, e:
        re = {'r': 0, 'msg': u"系统出现错误，无法进行操作"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")

def jobcompany(request):
    if 'access_token' not in request.POST:
        re = {'r': 0, 'msg': "你的access_token没传入，请查看参数信息，此参数如若需要请与开发者联系"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
    access_token = request.POST['access_token']
    if not OfferToken.objects.filter(token=access_token):
        re = {'r': 0, 'msg': "你的access_token不存在或是已经过期，此参数如若需要请与开发者联系"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
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
        logger.info(u"调用接口成功 - jobcompany - "+access_token) 
        re = {'r': 1, 'msg': u"成功获取薪水城市分类以及相应总数",'info':info}
        return HttpResponse(json.dumps(re),content_type='application/json',status="201")
    except BaseException, e:
        re = {'r': 0, 'msg': u"系统出现错误，无法进行操作"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")

def jobmessagelist(request):
    if 'access_token' not in request.POST:
        re = {'r': 0, 'msg': "你的access_token没传入，请查看参数信息，此参数如若需要请与开发者联系"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
    access_token = request.POST['access_token']
    if not OfferToken.objects.filter(token=access_token):
        re = {'r': 0, 'msg': "你的access_token不存在或是已经过期，此参数如若需要请与开发者联系"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
    if 'id' not in request.POST :
        re = {'r': 0, 'msg': u"参数不全！"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
    else:
        id = request.POST['id']
    try:
        print id
        data = OfferMessage.objects.filter(offerid=id).order_by('-time').values("id","offerid","content","time")
        print 222
        info = json.dumps(list(data), cls=CJsonEncoder, ensure_ascii=False)
        logger.info(u"调用接口成功 - jobmessagelist - "+access_token) 
        re = {'r': 1, 'msg': u"获取留言信息成功，按照时间先后顺序排序",'info':json.loads(info)}
        return HttpResponse(json.dumps(re),content_type='application/json',status="201")
    except BaseException, e:
        re = {'r': 0, 'msg': u"系统出现错误，无法进行操作"}
        return HttpResponse(json.dumps(re), content_type='application/json',status="201")
