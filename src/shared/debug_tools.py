import functools
import re
import time
from collections import defaultdict
from django.db import connection


class QueryDebug:
    """
    A utility for analyzing and optimizing blocks of code in terms of database queries.
    Logs detailed information about executed queries, including raw SQL.
    """

    def __init__(self, code_block_name='', log_file=None):
        self.name = code_block_name or 'Unnamed Block'
        self.log_file = log_file or 'query_debug.log'
        self.old_queries = set()
        self.new_queries = []
        self.from_counter = defaultdict(int)
        self.command_count = defaultdict(int)
        self.from_command_count = defaultdict(int)
        self.start_time = 0
        self.end_time = 0

    def __enter__(self):
        self.old_queries = {query['sql'] for query in connection.queries}
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        self.new_queries = [
            query for query in connection.queries
            if query['sql'] not in self.old_queries
        ]
        self._analyze_queries()
        self._log_results()

    def __call__(self, func):
        """
        Enables usage of QueryDebug as a decorator.
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with self:
                self.name = f"Function: {func.__name__}"
                return func(*args, **kwargs)
        return wrapper

    def _analyze_queries(self):
        """
        Analyze the executed queries to identify their corresponding tables and commands.
        """
        pattern = re.compile(r'\b(FROM|JOIN)\s+`?(\w+)[\.]?(\w+)?`?', re.IGNORECASE)
        for query in self.new_queries:
            sql = query['sql']
            from_clauses = pattern.findall(sql)
            command = sql.split()[0].upper()  # Extract the SQL command (e.g., SELECT, INSERT)
            self.command_count[command] += 1

            if from_clauses:
                for clause in from_clauses:
                    table = ".".join(filter(None, clause))  # Combine schema and table if present
                    self.from_counter[table] += 1
                    self.from_command_count[f'{command}_{table}'] += 1

    def _log_results(self):
        """
        Log the results of the analysis either to a file or console, including full SQL.
        """
        total_time = self.end_time - self.start_time

        log_header = f"\nBLOCK: {self.name}\n{'=' * 100}"
        log_summary = (
            f"Execution Time: {total_time:.4f} seconds\n"
            f"Total Queries: {len(self.new_queries)}\n"
            f"Tables Queried: {dict(self.from_counter)}\n"
            f"Command Counts: {dict(self.command_count)}\n"
            f"Detailed Table/Command Info: {dict(self.from_command_count)}"
        )
        log_queries = "\nDetailed Queries (raw SQL):\n" + "\n".join(
            [f"Query {i + 1}:\n{query['sql']}\nTime: {query['time']} sec\n" for i, query in enumerate(self.new_queries)]
        )
        log_body = f"{log_header}\n{log_summary}\n\n{log_queries}\n{'=' * 100}\n"

        if self.log_file:
            with open(self.log_file, "a", encoding="utf-8") as file:
                file.write(log_body)
        else:
            print(log_body)
