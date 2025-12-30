import pyodbc
import pandas as pd

def connection():

    cnxn= pyodbc.connect("Driver={SQL Server Native Client 11.0};" 
                        "Server=SUPPORT03;"
                        "Database=TestGolf;"
                        "uid=sa;pwd=CounterPoint8")

    cursor=cnxn.cursor()
    return cursor

def adj_query(dates):
    # cursor.execute(f'SELECT * FROM AR_ADJ_HIST WHERE DOC_DAT >={dates[0]} AND DOC_DAT <={dates[1]}') 
    print("hello")
    cursor=connection()
    
    cursor.execute("SELECT * FROM AR_ADJ_HIST")

    col=[]
    data=[]

    for row in cursor:
        data.append(row)
        
    print(data)
    for row in cursor.columns(table='AR_ADJ_HIST'):
        col.append(row.column_name)



    df_adj_hist=pd.DataFrame(data,columns=col)
    print(df_adj_hist)
    return df_adj_hist

