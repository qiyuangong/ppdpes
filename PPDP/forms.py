#coding=utf-8
from django import forms
from models import Anon_Task, Anon_Algorithm, Anon_Model, Data

TASK_CAT = (
    ('1', '高维数据'),
    ('2', '缺失数据'),
    ('3', '复杂关系'),
)

TASK_TYPE = (
    ('1', '匿名'),
    ('2', '评估'),
)

class add_task_form(forms.ModelForm):
    task_cat = forms.ChoiceField(label='选择演示任务', choices=TASK_CAT)

    class Meta:
        model = Anon_Task
        fields = ['task_text', 'data', 'anon_model', 'anon_algorithm', 'task_type']


class old_task_form(forms.Form):
    task_cat = forms.ChoiceField(label='选择演示任务', choices=TASK_CAT)
    task_type = forms.ChoiceField(label='选择任务类型', choices=TASK_TYPE)
    dataset_choice = [(index, ins.data_text) for index, ins in enumerate(Data.objects.all())]
    model_choice = [(index, ins.model_text) for index, ins in enumerate(Anon_Model.objects.all())]
    algorithm_choice = [(index, ins.algorithm_text) for index, ins in enumerate(Anon_Algorithm.objects.all())]
    dataset = forms.ChoiceField(label='选择数据集', choices=dataset_choice)
    model = forms.ChoiceField(label='选择匿名模型',choices=model_choice)
    algorithm = forms.ChoiceField(label='选择匿名算法',choices=algorithm_choice)
    parameter = forms.CharField()

    def is_valid(self):
        return True

    def clean_dataset(self):
        data_s = self.cleaned_data.get('dataset')
        return Data.objects.get(data_text=data_s)



