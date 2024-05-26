# тут должны быть операции, такие как запросы к БД или прочие для возвращения данных

from .clickhouse_service import execute_query


def build_time_condition(start_time, end_time):
    if start_time and end_time:
        return f"AND point BETWEEN '{start_time}' AND '{end_time}'"
    elif start_time:
        return f"AND point >= '{start_time}'"
    elif end_time:
        return f"AND point <= '{end_time}'"
    return ""

def enc_time_condition(start_time, end_time):
    if start_time and end_time:
        return f"WHERE point BETWEEN '{start_time}' AND '{end_time}'"
    elif start_time:
        return f"WHERE point >= '{start_time}'"
    elif end_time:
        return f"WHERE point <= '{end_time}'"
    return ""

def time_selector():
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
    return execute_query(query)

def wb_query(start_time, end_time):
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
    return data


def th_query(start_time, end_time):
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
    return data


def apdex_query(start_time, end_time):
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
    return data




def all_metrics_query(start_time, end_time):
    query = f"""
    SELECT 
    metrics_table.point AS time,
    sumOrNull(metrics_table.total_call_time) / sumOrNull(metrics_table.call_count) AS response_time,
    sumOrNull(metrics_table.call_count) AS throughput,
    (apdex_query.s + apdex_query.t/2) / (apdex_query.s + apdex_query.t + apdex_query.f) AS apdex
FROM
    metrics_table
JOIN (
    SELECT 
        toStartOfDay(min(point)) AS min_time,
        toStartOfDay(max(point)) AS max_time
    FROM 
        metrics_table
    WHERE 
        language = 'java'
        AND app_name = '[GMonit] Collector'
        AND scope = ''
) AS time_selector ON 1=1
JOIN (
    SELECT 
        point AS time,
        sumOrNull(total_exclusive_time) AS f,
        sumOrNull(call_count) AS s,
        sumOrNull(total_call_time) AS t
    FROM 
        metrics_table
    WHERE 
        language = 'java'
        AND app_name = '[GMonit] Collector'
        AND scope = ''
        AND name = 'Apdex'
        AND point BETWEEN time_selector.min_time AND time_selector.max_time
    GROUP BY 
        time
) AS apdex_query ON metrics_table.point = apdex_query.time
WHERE 
    metrics_table.language = 'java'
    AND metrics_table.app_name = '[GMonit] Collector'
    AND metrics_table.scope = ''
    AND metrics_table.name = 'HttpDispatcher'
    AND metrics_table.point BETWEEN time_selector.min_time AND time_selector.max_time
GROUP BY 
    metrics_table.point
ORDER BY 
    metrics_table.point;

    """
    return execute_query(query)


def enchanced_wr(start_time, end_time):
    time_condition = enc_time_condition(start_time, end_time)
    query = f"""
    SELECT
        point as time,
        WR
    FROM enchanced_metrics
        {time_condition}
    ORDER BY time
    """
    return execute_query(query)


def enchanced_thq(start_time, end_time):
    time_condition = enc_time_condition(start_time, end_time)
    query = f"""
    SELECT
        point as time,
        tg
    FROM enchanced_metrics
        {time_condition}
    ORDER BY time
    """
    return execute_query(query)


def enchanced_apdex(start_time, end_time):
    time_condition = enc_time_condition(start_time, end_time)
    query = f"""
    SELECT
        point as time,
        apdex
    FROM enchanced_metrics
        {time_condition}
    ORDER BY time
    """
    return execute_query(query)


def enchanced_all(start_time, end_time):
    time_condition = enc_time_condition(start_time, end_time)
    query = f"""
    SELECT
        point as time,
        WR, tg, apdex
    FROM enchanced_metrics
        {time_condition}
    ORDER BY time
    """
    return execute_query(query)
