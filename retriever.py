import pyodbc
import pandas as pd

cursor=''
def main():

    cnxn= pyodbc.connect("Driver={SQL Server Native Client 11.0};" 
                        "Server=SUPPORT03;"
                        "Database=TestGolf;"
                        "uid=sa;pwd=CounterPoint8")

    cursor=cnxn.cursor()
    adj_query()
    return cursor

def adj_query(dates):
    # cursor.execute(f'SELECT * FROM AR_ADJ_HIST WHERE DOC_DAT >={dates[0]} AND DOC_DAT <={dates[1]}') 
    cursor.execute(f'SELECT * FROM AR_ADJ_HIST WHERE DOC_DAT >={dates[0]} AND DOC_DAT <={dates[1]}')
    
    col=[]
    data=[]
    for row in cursor.columns(table='AR_ADJ_HIST'):
        col.append(row.column_name)

    for row in cursor:
        data.append(row)


    df_adj_hist=pd.DataFrame(columns=col,rows=data)

if __name__ =="__main__":
    main()