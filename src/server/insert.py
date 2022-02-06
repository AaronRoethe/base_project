from datetime import datetime
import pyodbc
import time

from datetime import date
from pathlib import Path

class MyDfInsert:
    def __init__(self, cnxn, sql_stub, data_frame, rows_per_batch=1000):
        # NB: hard limit is 1000 for SQL Server table value constructor
        self._rows_per_batch = 1000 if rows_per_batch > 1000 else rows_per_batch

        self._cnxn = cnxn
        self._sql_stub = sql_stub
        self._num_columns = None
        self._row_placeholders = None
        self._num_rows_previous = None
        self._all_placeholders = None
        self._sql = None

        row_count = 0
        param_list = list()
        for df_row in data_frame.itertuples():
            param_list.append(tuple(df_row[1:]))  # omit zero-based row index
            row_count += 1
            if row_count >= self._rows_per_batch:
                self._send_insert(param_list)  # send a full batch
                row_count = 0
                param_list = list()
        self._send_insert(param_list)  # send any remaining rows

    def _send_insert(self, param_list):
        if len(param_list) > 0:
            if self._num_columns is None:
                # print('[DEBUG] (building items that depend on the number of columns ...)')
                # this only happens once
                self._num_columns = len(param_list[0])
                self._row_placeholders = ','.join(['?' for x in range(self._num_columns)])
                # e.g. '?,?'
            num_rows = len(param_list)
            if num_rows != self._num_rows_previous:
                # print('[DEBUG] (building items that depend on the number of rows ...)')
                self._all_placeholders = '({})'.format('),('.join([self._row_placeholders for x in range(num_rows)]))
                # e.g. '(?,?),(?,?),(?,?)'
                self._sql = f'{self._sql_stub} VALUES {self._all_placeholders}'
                self._num_rows_previous = num_rows
            params = [int(element) if isinstance(element, np.int64) else element
                    for row_tup in param_list for element in row_tup]
            # print('[DEBUG]    sql: ' + repr(self._sql))
            # print('[DEBUG] params: ' + repr(params))
            crsr = self._cnxn.cursor()
            crsr.execute(self._sql, params)

def batch_insert(servername, database, table, load):
    if input("""
            y -> Insert
            n -> Exit 
        enter: """) == 'y':
        pass
    else:
        raise SystemExit

    ### Load file ###
    columns = load.columns
    
    for i in columns:
        try:
            clean_columns = clean_columns + ", " + i
        except:
            clean_columns = i

    add =   f"""
            INSERT INTO {table} ({clean_columns}) 
            """

    ### Server Location ###
    cnxn = pyodbc.connect(f"""
        DRIVER={{SQL Server}};
        SERVER={servername}; 
        DATABASE={database}; 
        Trusted_Connection=yes""", 
        autocommit=True)

    t0 = time.time()

    MyDfInsert(cnxn, add, load, rows_per_batch=250)

    print()
    print(f'Inserts completed in {time.time() - t0:.2f} seconds.')
    cnxn.close()
