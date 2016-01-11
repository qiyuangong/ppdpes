from __future__ import unicode_literals
from django.db import models
import datetime
from django.utils import timezone


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
    task_type = models.IntegerField(default=0)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField('Not finished Yet!')

    def __str__(self):
        key = self.data.data_text + self.anon_model.model_text +\
              self.anon_algorithm.algorithm_text + self.anon_algorithm.parameter
        return key

    def __eq__(self, other):
        if self == other:
            return True
        else:
            return False


    def __hash__(self):
        key = self.data.data_text + self.anon_model.model_text +\
              self.anon_algorithm.algorithm_text + self.anon_algorithm.parameter
        return hash(key)


class Anon_Data(models.Model):
    data = models.ForeignKey(Data, on_delete=models.CASCADE)
    anon_model = models.ForeignKey(Anon_Model, on_delete=models.CASCADE)
    task = models.ForeignKey(Anon_Task, on_delete=models.CASCADE)
    # pub_time = task.end_time

    def __str__(self):
        return "Anonmized " + data.data_text