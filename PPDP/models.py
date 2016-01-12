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
    task_text = models.CharField(max_length=200)
    data = models.ForeignKey(Data, on_delete=models.CASCADE)
    anon_model = models.ForeignKey(Anon_Model, on_delete=models.CASCADE)
    anon_algorithm = models.ForeignKey(Anon_Algorithm, on_delete=models.CASCADE)
    parameters = JSONField(null=True, blank=True)
    task_type = models.IntegerField(default=0)
    start_time = models.DateTimeField(default=timezone.now())
    result_set = models.IntegerField(default=-1)
    end_time = models.Empty()

    def post_save(self, *args, **kwargs):
        super(Anon_Task, self).post_save(*args, **kwargs)
        if self._state.adding:
            key = ';'.join((self.data.data_text,
                           self.anon_model.model_text, self.anon_algorithm.algorithm_text, str(self.parameters)))
            if self.task_type == 0:
                try:
                    anon_result = Anon_Result.objects.get(key=key)
                except Anon_Result.DoesNotExist:
                    anon_result = Anon_Result.create(key)
                    Anon_Result.save(anon_result)
                self.result_set = anon_result.id
            else:
                try:
                    eval_result = Eval_Result.objects.get(key=key)
                except Eval_Result.DoesNotExist:
                    eval_result = Eval_Result.create(key)
                    Eval_Result.save(eval_result)
                self.result_set = eval_result.id

    def is_finished(self):
        return timezone.now() >= self.end_time

    def __str__(self):
        return self.task_text


class Anon_Result(models.Model):
    key = models.CharField(max_length=200)
    anon_result = JSONField(null=True, blank=True)
    start_time = models.DateTimeField(default=timezone.now())
    end_time = models.Empty()

    @classmethod
    def create(cls, key):
        anon_re = cls(key=key)
        anon_re.anon()
        anon_re.end_time = timezone.now()
        return anon_re

    def anon(self):
        # .end_time = self.end_time
        print "Anon work!!!!!!!"
        pass


class Eval_Result(models.Model):
    key = models.CharField(max_length=200)
    eval_result = JSONField(null=True, blank=True)
    start_time = models.DateTimeField(default=timezone.now())
    end_time = models.DateTimeField()

    @classmethod
    def create(cls, key):
        eval_re = cls(key=key)
        eval_re.eval()
        eval_re.end_time = timezone.now()
        return eval_re

    def eval(self):
        # .end_time = self.end_time
        # print "Eval works!!!!!!!"
        pass


class Anon_Data(models.Model):
    data = models.ForeignKey(Data, on_delete=models.CASCADE)
    anon_model = models.ForeignKey(Anon_Model, on_delete=models.CASCADE)
    task = models.ForeignKey(Anon_Task, on_delete=models.CASCADE)
    result = JSONField(null=True, blank=True)

    def __str__(self):
        return "Anonmized " + data.data_text

