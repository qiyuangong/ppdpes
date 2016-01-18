from celery import shared_task
from ppdpes_core.anonymizer import universe_anonymizer
from django.utils import timezone
import json
import pdb

@shared_task
def eval(anon_task, eval_result, eval_parameters):
    result =  universe_anonymizer(eval_parameters)
    # eval_result = Eval_Result.objects.get(pk=eval_id)
    print eval_result
    eval_result.end_time = timezone.now()
    anon_task.end_time =  eval_result.end_time
    eval_result.eval_result =  json.dumps(result)
    eval_result.save()
    anon_task.save()


@shared_task
def anon(anon_task, anon_result, key, anon_parameters):
    result, eval_r = universe_anonymizer(anon_parameters)
    anon_url = "tmp/" + str(key) + ".txt"
    anon_r = dict()
    anon_r['url'] = anon_url
    anon_r['ncp'] = eval_r[0]
    anon_r['time'] = eval_r[1]
    anon_file = open(anon_url, 'w')
    for record in result:
        try:
            line = ';'.join(record) + '\n'
        except:
            line = ';'.join(record[:-1]) + '|' + ';'.join(record[-1]) + '\n'
        anon_file.write(line)
    anon_file.close()
    # anon_result = Anon_Result.objects.get(pk=anon_id)
    anon_result.anon_result = json.dumps(anon_r)
    anon_result.end_time = timezone.now()
    anon_task.end_time = anon_result.end_time
    anon_result.save()
    anon_task.save()