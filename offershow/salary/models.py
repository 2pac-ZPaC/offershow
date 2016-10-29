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