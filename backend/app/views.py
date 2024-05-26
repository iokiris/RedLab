import time
from app import queries
from AI.anomaly_predict import anomaly_pipeline

from django.http import JsonResponse
from django.core.cache import cache
from .clickhouse_service import execute_query

def build_time_condition(start_time, end_time):
    if start_time and end_time:
        return f"AND point BETWEEN '{start_time}' AND '{end_time}'"
    elif start_time:
        return f"AND point >= '{start_time}'"
    elif end_time:
        return f"AND point <= '{end_time}'"
    return ""

def web_response_time(request):
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')

    cache_key = f"web_response_time_{start_time}_{end_time}"
    data = cache.get(cache_key)
 
    if not data:
        data = queries.wb_query(start_time, end_time)
        cache.set(cache_key, data, timeout=180)  # Кэшируем на 3 минуты

    return JsonResponse({'data': data})

def throughput(request):
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')

    cache_key = f"throughput_{start_time}_{end_time}"
    data = cache.get(cache_key)

    if not data:
        data = queries.th_query(start_time, end_time)
        cache.set(cache_key, data, timeout=180) 
    return JsonResponse({'data': data})

def apdex(request):
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')

    cache_key = f"apdex_{start_time}_{end_time}"
    data = cache.get(cache_key)

    if not data:
        data = queries.apdex_query(start_time, end_time)
        cache.set(cache_key, data, timeout=180)  

    return JsonResponse({'data': data})

def error_rate(request):
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')

    cache_key = f"anomaly_predict{start_time}_{end_time}"
    data = cache.get(cache_key)

    if not data:
        data = queries.er
        cache.set(cache_key, data, timeout=3600)

    return JsonResponse({'data': data})

def time_sector(request):
    cache_key = "time_sector"
    data = cache.get(cache_key)

    if not data:
        try:
            data = queries.time_selector()
            min_time = data[0][0]
            max_time = data[0][1]
            data = {'min_time': min_time, 'max_time': max_time}
            cache.set(cache_key, data, timeout=3600)  # Кэшируем на час
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse(data)

def anomaly_stats(request):
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')
    cache_key = f"anomalys_{start_time}_{end_time}"
    data = cache.get(cache_key)
    if not data:
        data = anomaly_pipeline()
    return JsonResponse({'data': data})


# увесистый запрос

def get_all_metrics(request):
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')
    cache_key = f"allmetrics_{start_time}_{end_time}"
    data = cache.get(cache_key)
    if not data:
        data = queries.all_metrics_query(start_time, end_time)
        cache.set(cache_key, data, timeout=60)
    return JsonResponse({'data': data})


# увесистый запрос
def full_data_with_anomalys(request):
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')
    cache_key = f"fdwa_{start_time}_{end_time}"
    data = cache.get(cache_key)
    if not data:
        wbq = queries.wb_query(start_time, end_time)
        thq = queries.th_query(start_time, end_time)
        apd = queries.apdex_query(start_time, end_time)
        anomalys = anomaly_pipeline(wbq, thq, apd)
        return JsonResponse({'data': anomalys})

def enchanced_wr(request):
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')
    cache_key = f"enchanced_wr_{start_time}_{end_time}"
    data = cache.get(cache_key)
    if not data:
        data = queries.enchanced_wr(start_time, end_time)
        cache.set(cache_key, data, timeout=60)
    return JsonResponse({'data': data})

def enchanced_thq(request):
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')
    cache_key = f"enchanced_thq_{start_time}_{end_time}"
    data = cache.get(cache_key)
    if not data:
        data = queries.enchanced_thq(start_time, end_time)
        cache.set(cache_key, data, timeout=60)
    return JsonResponse({'data': data})

def enchanced_apdex(request):
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')
    cache_key = f"enchanced_apdex_{start_time}_{end_time}"
    data = cache.get(cache_key)
    if not data:
        data = queries.enchanced_apdex(start_time, end_time)
        cache.set(cache_key, data, timeout=60)
    return JsonResponse({'data': data})



def enchanced_all(request):
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')
    cache_key = f"enchanced_all_{start_time}_{end_time}"
    data = cache.get(cache_key)
    if not data:
        data = queries.enchanced_all(start_time, end_time)
        cache.set(cache_key, data, timeout=60)
    return JsonResponse({'data': data})


def combine_data_with_anomalies(req, anomalies):
    combined_data = []
    for i in range(len(req)):
        combined_data.append(req[i] + [anomalies[1][i]])
    return combined_data

def enchanced_fwda(request):
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')
    cache_key = f"enchanced_fwda_{start_time}_{end_time}"
    data = cache.get('asdkpoas')
    if not data:
        # start_t = time.time()
        # wrq = queries.enchanced_wr(start_time, end_time)
        # thq = queries.enchanced_thq(start_time, end_time)
        # apdex = queries.enchanced_apdex(start_time, end_time)
        # output, count = anomaly_pipeline(wrq, thq, apdex)
        # cache.set(cache_key, data, timeout=60)
        req = queries.enchanced_all(start_time, end_time)
        anomalies = anomaly_pipeline(req)
        for i in range(len(req)):
            req[i] = [req[i][0], req[i][1], req[i][2], req[i][3], anomalies[i][1], anomalies[i][0]]

        data = {
            'data': req,
        }
        cache.set(cache_key, data, timeout=1800)

    return JsonResponse(data)