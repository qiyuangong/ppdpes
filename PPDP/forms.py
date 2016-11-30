#coding=utf-8
from django import forms
from models import Anon_Task, Anon_Algorithm, Anon_Model, Data
import ast

TASK_CAT = (
    (0, '高维数据'),
    (1, '缺失数据'),
    (2, '复杂关系'),
)

TASK_TYPE = [
    (0, 'Anon_Task'),
    (1, 'Eval_Task'),
]

class add_task_form(forms.ModelForm):
    task_type = forms.ChoiceField(label='选择演示任务', choices=TASK_TYPE)
    task_cat = forms.ChoiceField(label='选择演示任务', choices=TASK_CAT)

    class Meta:
        model = Anon_Task
        fields = ['task_text', 'task_type', 'task_cat', 'data', 'anon_model', 'anon_algorithm',
                  'parameters', ]


class add_data_form(forms.ModelForm):
    task_cat = forms.ChoiceField(label='选择数据类型', choices=TASK_CAT)

    class Meta:
        model = Data
        fields = ['data_text', 'task_cat', 'size', 'sa_index', 'qid_index', 'is_cat']

    def is_valid(self):
        return True


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    task_cat = forms.ChoiceField(label='选择数据类型', choices=TASK_CAT)
    sa_index = forms.IntegerField(initial=-1)
    qid_index = forms.CharField(max_length=800)
    is_cat = forms.CharField(max_length=800)
    file_content = forms.FileField()

    def is_valid(self):
        return True

class UploadGHForm(forms.Form):
    def __init__(self, *args, **kwargs):
        data_id = kwargs.pop('data_id')
        super(UploadGHForm, self).__init__(*args, **kwargs)
        data = Data.objects.get(id=data_id)
        qid_index = ast.literal_eval(data.qid_index)
        is_cat = ast.literal_eval(data.is_cat)
        # print is_cat
        for pos, index in enumerate(qid_index):
            if is_cat[pos] == 1:
                # self.fields['att_name_for %s' % index] = forms.CharField(max_length=50)
                self.fields['att_%s' % index] = forms.FileField()
        if data.is_rt == 1:
            self.fields['Sensitive GH for RT-data'] = forms.FileField()
    def is_valid(self):
        return True


# class old_task_form(forms.Form):
#     task_cat = forms.ChoiceField(label='选择演示任务', choices=TASK_CAT)
#     task_type = forms.ChoiceField(label='选择任务类型', choices=TASK_TYPE)
#     dataset_choice = [(index, ins.data_text) for index, ins in enumerate(Data.objects.all())]
#     model_choice = [(index, ins.model_text) for index, ins in enumerate(Anon_Model.objects.all())]
#     algorithm_choice = [(index, ins.algorithm_text) for index, ins in enumerate(Anon_Algorithm.objects.all())]
#     dataset = forms.ChoiceField(label='选择数据集', choices=dataset_choice)
#     model = forms.ChoiceField(label='选择匿名模型',choices=model_choice)
#     algorithm = forms.ChoiceField(label='选择匿名算法',choices=algorithm_choice)
#     parameter = forms.CharField()
#
#     def is_valid(self):
#         return True
#
#     def clean_dataset(self):
#         data_s = self.cleaned_data.get('dataset')
#         return Data.objects.get(data_text=data_s)



