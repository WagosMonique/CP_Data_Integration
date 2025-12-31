import pyodbc
import pandas as pd

# def connection():
def main():

    cnxn= pyodbc.connect("Driver={SQL Server Native Client 11.0};" 
                        "Server=SUPPORT03;"
                        "Database=TestGolf;"
                        "uid=sa;pwd=CounterPoint8")

    cursor=cnxn.cursor()
    ar_df=adj_query(cursor)
    ar_df.to_excel("export\\ar_data.xlsx")

    return cursor

def adj_query(cursor):
    # cursor.execute(f'SELECT * FROM AR_ADJ_HIST WHERE DOC_DAT >={dates[0]} AND DOC_DAT <={dates[1]}') 
   
    cursor.execute("SELECT * FROM AR_ADJ_HIST")#get information from sql table

    col=[]
    data=[]# instantiating variables

    rows=cursor.fetchall()#getting all rows from table

    for row in rows: 
        data.append(list(row))
    
    for row in cursor.columns(table='AR_ADJ_HIST'):
        col.append(row.column_name)

    df_adj_hist=pd.DataFrame(data,columns=col)

    return df_adj_hist

if __name__=='__main__':
    main()