from __future__ import unicode_literals
from django.db import models
import datetime
from django.utils import timezone
from jsonfield import JSONField
from ppdp_kernel.anonymizer import universe_anonymizer
from django.db.models.signals import pre_save
from django.dispatch import receiver
import json


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
    task_text = models.CharField(max_length=200)
    data = models.ForeignKey(Data, on_delete=models.CASCADE)
    anon_model = models.ForeignKey(Anon_Model, on_delete=models.CASCADE)
    anon_algorithm = models.ForeignKey(Anon_Algorithm, on_delete=models.CASCADE)
    parameters = JSONField(null=True, blank=True)
    task_type = models.IntegerField(default=0)
    start_time = models.DateTimeField(default=timezone.now())
    result_set = models.IntegerField(default=-1)
    end_time = models.DateTimeField(default=timezone.now())

    def is_finished(self):
        return timezone.now() >= self.end_time

    def __str__(self):
        return self.task_text


class Anon_Result(models.Model):
    key = models.CharField(max_length=200)
    data = models.ForeignKey(Data, on_delete=models.CASCADE)
    anon_model = models.ForeignKey(Anon_Model, on_delete=models.CASCADE)
    anon_algorithm = models.ForeignKey(Anon_Algorithm, on_delete=models.CASCADE)
    anon_result = JSONField(null=True, blank=True)
    start_time = models.DateTimeField(default=timezone.now())
    end_time = models.DateTimeField(default=timezone.now())

    @classmethod
    def create(cls, key):
        anon_re = cls(key=key)
        anon_re.anon_model = anon_re.anon()
        anon_re.end_time = timezone.now()
        return anon_re

    def anon(self):
        universe_anonymizer(['a', 'm'])


class Eval_Result(models.Model):
    key = models.CharField(max_length=200)
    data = models.ForeignKey(Data, on_delete=models.CASCADE)
    anon_model = models.ForeignKey(Anon_Model, on_delete=models.CASCADE)
    anon_algorithm = models.ForeignKey(Anon_Algorithm, on_delete=models.CASCADE)
    eval_result = JSONField(null=True, blank=True)
    start_time = models.DateTimeField(default=timezone.now())
    end_time = models.DateTimeField(default=timezone.now())

    @classmethod
    def create(cls, key):
        eval_re = cls(key=key)
        eval_re.eval_result =  json.dumps(eval_re.eval())
        eval_re.end_time = timezone.now()
        return eval_re

    def eval(self):
       return universe_anonymizer(['a', 'm', 'k'])


@receiver(pre_save, sender=Anon_Task, dispatch_uid="connect to ppdp_kernel")
def connect_PPDP_Kernel(sender, instance, **kwargs):
    key = ';'.join((instance.data.data_text,
                   instance.anon_model.model_text, instance.anon_algorithm.algorithm_text, str(instance.parameters)))
    if instance.task_type == 0:
        try:
            anon_result = Anon_Result.objects.get(key=key)
        except Anon_Result.DoesNotExist:
            anon_result = Anon_Result.create(key)
            anon_result.anon_algorithm = instance.anon_algorithm
            anon_result.anon_model = instance.anon_model
            anon_result.data = instance.data
            anon_result.save()
        instance.result_set = anon_result.id
        instance.end_time = anon_result.end_time
    else:
        try:
            eval_result = Eval_Result.objects.get(key=key)
        except Eval_Result.DoesNotExist:
            eval_result = Eval_Result.create(key)
            eval_result.anon_algorithm = instance.anon_algorithm
            eval_result.anon_model = instance.anon_model
            eval_result.data = instance.data
            eval_result.save()
        instance.result_set = eval_result.id
        instance.end_time = eval_result.end_time
