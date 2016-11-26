# -*- coding: utf-8 -*-
from django.db import models
import datetime

class OfferInfo(models.Model):
    id = models.AutoField(primary_key=True,verbose_name = 'offer编号') 
    company = models.CharField(max_length=45, blank=True,null= True,verbose_name = '公司名称')
    position = models.CharField(max_length=45, blank=True,null= True,verbose_name = '岗位名称')
    salary = models.CharField(max_length=45, blank=True,null= True,verbose_name = '岗位薪水')
    city = models.CharField(max_length=45, blank=True,null= True,verbose_name = '工作地点')
    remark = models.CharField(max_length=450, blank=True,null= True,verbose_name = '岗位备注')
    ip = models.CharField(max_length=45, blank=True,null= True,verbose_name = '爆料者IP')
    time = models.DateTimeField(default=datetime.datetime.now,verbose_name = '爆料时间')
    score = models.IntegerField(blank=True, null=True,default=3,verbose_name = '可信度评分')
    number = models.IntegerField(blank=True, null=True,default=0,verbose_name = '浏览量')
    def toJSON(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)
    
        d = {}
        for attr in fields:
            if isinstance(getattr(self, attr),datetime.datetime):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(getattr(self, attr),datetime.date):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d')
            else:
                d[attr] = getattr(self, attr)
    
        import json
        return json.dumps(d)   
    def __unicode__(self):
        return '%s' % (self.id)  
    class Meta:
        verbose_name = '薪水表格'
        verbose_name_plural = verbose_name
        db_table = 'offerinfo'

class OfferEvaluate(models.Model):
    id = models.AutoField(primary_key=True,verbose_name = '评价编号') 
    ip = models.CharField(max_length=45, blank=True,null= True,verbose_name = '爆料者IP')
    typeid = models.IntegerField(blank=True, null=True,verbose_name = '评价类型')
    offerid = models.IntegerField(blank=True, null=True,verbose_name = 'offer编号')
    time = models.DateTimeField(default=datetime.datetime.now,verbose_name = '评价时间')

    def toJSON(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)
    
        d = {}
        for attr in fields:
            if isinstance(getattr(self, attr),datetime.datetime):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(getattr(self, attr),datetime.date):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d')
            else:
                d[attr] = getattr(self, attr)
    
        import json
        return json.dumps(d)   
    def __unicode__(self):
        return '%s' % (self.id)  
    class Meta:
        verbose_name = '薪水评价'
        verbose_name_plural = verbose_name
        db_table = 'offerevaluate'


class OfferSearch(models.Model):
    id = models.AutoField(primary_key=True,verbose_name = '查询编号') 
    ip = models.CharField(max_length=45, blank=True,null= True,verbose_name = '爆料者IP')
    content = models.CharField(max_length=45, blank=True,null= True,verbose_name = '查询内容')
    time = models.DateTimeField(default=datetime.datetime.now,verbose_name = '查询时间')

    def toJSON(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)
    
        d = {}
        for attr in fields:
            if isinstance(getattr(self, attr),datetime.datetime):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(getattr(self, attr),datetime.date):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d')
            else:
                d[attr] = getattr(self, attr)
    
        import json
        return json.dumps(d)   
    def __unicode__(self):
        return '%s' % (self.id)  
    class Meta:
        verbose_name = '薪水查询'
        verbose_name_plural = verbose_name
        db_table = 'offersearch'


class OfferMessage(models.Model):
    id = models.AutoField(primary_key=True,verbose_name = '留言编号') 
    ip = models.CharField(max_length=45, blank=True,null= True,verbose_name = '爆料者IP')
    content = models.CharField(max_length=450, blank=True,null= True,verbose_name = '留言内容')
    offerid = models.IntegerField(blank=True, null=True,verbose_name = 'offer编号')
    time = models.DateTimeField(default=datetime.datetime.now,verbose_name = '留言时间')

    def toJSON(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)
    
        d = {}
        for attr in fields:
            if isinstance(getattr(self, attr),datetime.datetime):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(getattr(self, attr),datetime.date):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d')
            else:
                d[attr] = getattr(self, attr)
    
        import json
        return json.dumps(d)   
    def __unicode__(self):
        return '%s' % (self.id)  
    class Meta:
        verbose_name = '薪水留言'
        verbose_name_plural = verbose_name
        db_table = 'offermessage'

class OfferToken(models.Model):
    id = models.AutoField(primary_key=True,verbose_name = '令牌编号') 
    appid = models.CharField(max_length=10, blank=True,verbose_name = '应用名称')
    secret = models.CharField(max_length=45, blank=True,verbose_name = '应用密码')
    create_time = models.DateTimeField(default=datetime.datetime.now,verbose_name = '生成时间')
    token = models.CharField(max_length=125, blank=True,verbose_name = '访问令牌')
    remark = models.CharField(max_length=45, blank=True,verbose_name = '令牌备注')
    def __unicode__(self):
        return '%s' % (self.id)
    class Meta:
        verbose_name = '访问令牌信息'
        verbose_name_plural = verbose_name
        db_table = 'offertoken'
