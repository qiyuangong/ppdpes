from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from datetime import datetime
from jsonfield import JSONField
from django.db.models.signals import post_save
from django.dispatch import receiver
from tasks import eval, anon
from django.db import transaction
from django.utils.timezone import utc

TASK_TYPE = [
    (0, 'Anon_Task'),
    (1, 'Eval_Task'),
]


class Data(models.Model):
    data_text = models.CharField(max_length=200)
    data_url = models.CharField(max_length=200)
    full_name = models.CharField(max_length=200)
    size = models.IntegerField(default=0)
    qid_index = models.CharField(max_length=200)
    sa_index = models.CharField(max_length=200)
    is_cat = models.CharField(max_length=200)
    is_missing = models.IntegerField(default=0)
    is_high = models.IntegerField(default=0)
    is_rt = models.IntegerField(default=0)

    def __str__(self):
        return self.data_text

    @classmethod
    def create(cls, title, url, sa_index, qid_index, is_cat, flag):
        # print flag, type(flag)
        is_missing = 0
        is_high = 0
        is_rt = 0
        if flag == '1':
            is_missing = 1
        elif flag == '2':
            is_high = 1
        elif flag == '3':
            is_rt = 1
        data = cls(data_text=title, data_url=url, sa_index=sa_index, qid_index=qid_index,
                   is_cat=is_cat, is_missing=is_missing, is_high=is_high, is_rt=is_rt)
        return data


class Anon_Model(models.Model):
    model_text = models.CharField(max_length=200)
    is_rt = models.IntegerField(default=0)
    parameter = models.CharField(max_length=200)

    def __str__(self):
        return self.model_text


class Anon_Algorithm(models.Model):
    algorithm_text = models.CharField(max_length=200)
    anon_model = models.ForeignKey(Anon_Model, on_delete=models.CASCADE)
    parameter = models.CharField(max_length=200, blank=True, default='')
    short = models.CharField(default='', max_length=200)
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
    parameters = JSONField(null=True, blank=True, default='')
    task_type = models.IntegerField(default=0, choices=TASK_TYPE)
    start_time = models.DateTimeField(default=timezone.now)
    result_set = models.IntegerField(default=-1)
    end_time = models.DateTimeField(default=datetime(2015, 11, 26, 12, 52, 45, 773000, tzinfo=utc))
    is_missing = models.IntegerField(default=0)
    is_high = models.IntegerField(default=0)
    is_rt = models.IntegerField(default=0)

    def is_finished(self):
        return self.end_time > self.start_time

    def __str__(self):
        return self.task_text


class Anon_Result(models.Model):
    key = models.CharField(max_length=200)
    data = models.ForeignKey(Data, on_delete=models.CASCADE)
    anon_model = models.ForeignKey(Anon_Model, on_delete=models.CASCADE)
    anon_algorithm = models.ForeignKey(Anon_Algorithm, on_delete=models.CASCADE)
    anon_result = JSONField(null=True, blank=True)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=datetime(2015, 11, 26, 12, 52, 45, 773000, tzinfo=utc))

    @classmethod
    def create(cls, key, anon_parameters):
        anon_re = cls(key=key)
        return anon_re

    def is_finished(self):
        return self.end_time > self.start_time


class Eval_Result(models.Model):
    key = models.CharField(max_length=200)
    data = models.ForeignKey(Data, on_delete=models.CASCADE)
    anon_model = models.ForeignKey(Anon_Model, on_delete=models.CASCADE)
    anon_algorithm = models.ForeignKey(Anon_Algorithm, on_delete=models.CASCADE)
    eval_result = JSONField(null=True, blank=True)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=datetime(2015, 11, 26, 12, 52, 45, 773000, tzinfo=utc))

    @classmethod
    def create(cls, key, eval_parameters):
        eval_re = cls(key=key)
        return eval_re

    def is_finished(self):
        return self.end_time > self.start_time


@receiver(post_save, sender=Anon_Task, dispatch_uid="connect to ppdp_kernel")
def connect_PPDP_Kernel(sender, instance, *args, **kwargs):
    if kwargs['created']:
        key = '-'.join((instance.data.data_text, instance.anon_algorithm.algorithm_text, str(instance.parameters)))
        basic_parameters = []
        if "adult" in instance.data.data_text:
            basic_parameters.append('a')
        else:
            basic_parameters.append('i')
        if 'Mondrian' in instance.anon_algorithm.algorithm_text:
            basic_parameters.append('m')
        elif 'Semi' in instance.anon_algorithm.algorithm_text:
            basic_parameters.append('s')
        elif '1M' in instance.anon_algorithm.algorithm_text:
            basic_parameters.append('1m')
        elif 'APA' in instance.anon_algorithm.algorithm_text:
            basic_parameters.append('apa')
        elif 'PAA' in instance.anon_algorithm.algorithm_text:
            basic_parameters.append('paa')
        else:
            basic_parameters.append('m')
        flag = True
        if instance.task_type == 0:
            try:
                anon_result = Anon_Result.objects.get(key=key)
                instance.end_time = timezone.now()
                flag = False
            except Anon_Result.DoesNotExist:
                anon_result = Anon_Result.create(key, basic_parameters)
                anon_result.anon_algorithm = instance.anon_algorithm
                anon_result.anon_model = instance.anon_model
                anon_result.data = instance.data
                anon_result.save()
            instance.result_set = anon_result.id
        else:
            try:
                eval_result = Eval_Result.objects.get(key=key)
                instance.end_time = timezone.now()
                flag = False
            except Eval_Result.DoesNotExist:
                eval_result = Eval_Result.create(key, basic_parameters)
                eval_result.anon_algorithm = instance.anon_algorithm
                eval_result.anon_model = instance.anon_model
                eval_result.data = instance.data
                eval_result.save()
            instance.result_set = eval_result.id
        instance.save()
        if flag:
            with transaction.atomic():
                if instance.task_type == 0:
                    # instance, anon_result,
                    # transaction.on_commit(lambda: anon.delay(instance.id, key, basic_parameters))
                    try:
                        anon.delay(instance.id, key, basic_parameters + ['anon'] + [instance.parameters['anon']])
                    except (TypeError, KeyError):
                        anon.delay(instance.id, key, basic_parameters)
                else:
                    # instance, eval_result
                    # transaction.on_commit(lambda: eval.delay(instance.id, basic_parameters + ['k']))
                    # print instance.parameters['eval']
                    try:
                        eval.delay(instance.id, key, basic_parameters + ['eval'] + instance.parameters['eval'])
                    except (TypeError, KeyError):
                        # eval with k
                        eval.delay(instance.id, key, basic_parameters + ['eval', 'k'])
