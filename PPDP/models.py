from __future__ import unicode_literals
from django.db import models
import datetime
from django.utils import timezone
from jsonfield import JSONField


class Data(models.Model):
    data_text = models.CharField(max_length=200)
    data_url = models.CharField(max_length=200)
    size = models.IntegerField(default=0)
    qid_index = models.CharField(max_length=200)
    sa_index = models.CharField(max_length=200)
    is_missing = models.IntegerField(default=0)
    is_high = models.IntegerField(default=0)
    is_rt = models.IntegerField(default=0)

    def __str__(self):
        return self.data_text


class Anon_Model(models.Model):
    model_text = models.CharField(max_length=200)
    is_rt = models.IntegerField(default=0)
    parameter = models.CharField(max_length=200)

    def __str__(self):
        return self.model_text


class Anon_Algorithm(models.Model):
    algorithm_text = models.CharField(max_length=200)
    anon_model = models.ForeignKey(Anon_Model, on_delete=models.CASCADE)
    parameter = models.CharField(max_length=200)
    is_missing = models.IntegerField(default=0)
    is_high = models.IntegerField(default=0)
    is_rt = models.IntegerField(default=0)

    def __str__(self):
        return self.algorithm_text


class Anon_Task(models.Model):
    data = models.ForeignKey(Data, on_delete=models.CASCADE)
    anon_model = models.ForeignKey(Anon_Model, on_delete=models.CASCADE)
    anon_algorithm = models.ForeignKey(Anon_Algorithm, on_delete=models.CASCADE)
    parameters = JSONField(null=True, blank=True)
    task_type = models.IntegerField(default=0)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField('Not finished Yet!')


class Anon_Result(models.Model):
    task = models.ForeignKey(Anon_Task, on_delete=models.CASCADE)
    anon_result = JSONField(null=True, blank=True)


class Eval_Result(models.Model):
    task = models.ForeignKey(Anon_Task, on_delete=models.CASCADE)
    eval_result = JSONField(null=True, blank=True)


class Anon_Data(models.Model):
    data = models.ForeignKey(Data, on_delete=models.CASCADE)
    anon_model = models.ForeignKey(Anon_Model, on_delete=models.CASCADE)
    task = models.ForeignKey(Anon_Task, on_delete=models.CASCADE)
    result = JSONField(null=True, blank=True)

    def __str__(self):
        return "Anonmized " + data.data_text

