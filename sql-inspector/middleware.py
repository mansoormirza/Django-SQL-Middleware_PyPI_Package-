from django.db import connection
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import SqlLexer
from sqlparse import format
from django.conf import settings
from decimal import Decimal

def sql_middleware(get_response):
    def middleware(request):

        response = get_response(request)
        if settings.DEBUG:
            num_queries = len(connection.queries)
            check_duplicate = set()
            total_execution_time = Decimal()

            for query in connection.queries:
                total_execution_time += Decimal(query["time"])
                check_duplicate.add(query["sql"])
                sqlformatted = format(str(query["sql"]), reindent = True)
                print(highlight(sqlformatted, SqlLexer(), TerminalFormatter()))
        
        print("=======================")
        print("[SQL STATS]")
        print(f'{total_execution_time} - Execution Time')
        print(f'{num_queries} Total Queries')
        print(f'{num_queries - len(check_duplicate)} Total Duplicates')
        print("=======================")

        return response
    
    return middleware