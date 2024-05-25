import time
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
        time_condition = build_time_condition(start_time, end_time)
        query = f"""
        SELECT
            point as time,
            sumOrNull(total_call_time) / sumOrNull(call_count) as response_time
        FROM metrics_table
        WHERE
            language = 'java'
            AND app_name = '[GMonit] Collector'
            AND scope = ''
            AND name = 'HttpDispatcher'
            {time_condition}
        GROUP BY time
        ORDER BY time
        """
        data = execute_query(query)
        cache.set(cache_key, data, timeout=3600)  # Кэшируем на 1 час

    return JsonResponse({'data': data})

def throughput(request):
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')

    cache_key = f"throughput_{start_time}_{end_time}"
    data = cache.get(cache_key)

    if not data:
        time_condition = build_time_condition(start_time, end_time)
        query = f"""
        SELECT
            point as time,
            sumOrNull(call_count) as throughput
        FROM metrics_table
        WHERE
            language = 'java'
            AND app_name = '[GMonit] Collector'
            AND scope = ''
            AND name = 'HttpDispatcher'
            {time_condition}
        GROUP BY time
        ORDER BY time
        """
        data = execute_query(query)
        cache.set(cache_key, data, timeout=3600)  # Кэшируем на 1 час

    return JsonResponse({'data': data})

def apdex(request):
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')

    cache_key = f"apdex_{start_time}_{end_time}"
    data = cache.get(cache_key)

    if not data:
        time_condition = build_time_condition(start_time, end_time)
        query = f"""
        WITH
            sumOrNull(call_count) as s,
            sumOrNull(total_call_time) as t,
            sumOrNull(total_exclusive_time) as f
        SELECT
            point as time,
            (s + t/2) / (s + t + f) as apdex
        FROM metrics_table
        WHERE
            language = 'java'
            AND app_name = '[GMonit] Collector'
            AND scope = ''
            AND name = 'Apdex'
            {time_condition}
        GROUP BY time
        ORDER BY time
        """
        data = execute_query(query)
        cache.set(cache_key, data, timeout=3600)  # Кэшируем на 1 час

    return JsonResponse({'data': data})

def error_rate(request):
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')

    cache_key = f"error_rate_{start_time}_{end_time}"
    data = cache.get(cache_key)

    if not data:
        time_condition = build_time_condition(start_time, end_time)
        query = f"""
        SELECT
            point as time,
            sumOrNullIf(call_count, name='Errors/allWeb') / sumOrNullIf(call_count, name='HttpDispatcher') as error_rate
        FROM metrics_table
        WHERE
            language = 'java'
            AND app_name = '[GMonit] Collector'
            AND scope = ''
            AND name IN ('HttpDispatcher', 'Errors/allWeb')
            {time_condition}
        GROUP BY time
        ORDER BY time
        """
        data = execute_query(query)
        cache.set(cache_key, data, timeout=3600)  # Кэшируем на 1 час

    return JsonResponse({'data': data})

def time_sector(request):
    query = """
        SELECT
            toStartOfDay(min(point)) as min_time,
            toStartOfDay(max(point)) as max_time
        FROM
            metrics_table
        WHERE
            language = 'java'
            AND app_name = '[GMonit] Collector'
            AND scope = ''
    """
    try:
        data = execute_query(query)
        min_time = data[0][0]
        max_time = data[0][1]
        return JsonResponse({'min_time': min_time, 'max_time': max_time})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
