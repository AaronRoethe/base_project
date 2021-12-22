from pathlib import Path
import pandas as pd
import pyarrow as pa
import pyarrow.csv as csv

paths = Path(__file__).parent.absolute().parent.absolute().parent.absolute()

table_path = paths

### Input/output static tables ###
def tables(push_pull, table, name, path=table_path, sep=','):
    if push_pull == 'pull':
        # return csv.read_csv(path / name)
        return pd.read_csv(path / name, sep=sep, on_bad_lines='warn',engine="python")
    else:
        table.to_csv(table_path / name, sep=sep, index=False)