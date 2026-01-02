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
    cursor.execute("SELECT c.NAM , a.* FROM AR_ADJ_HIST a JOIN AR_CUST c ON a.CUST_NO=c.CUST_NO")#get information from sql table
    # make a join statetment and join the customer no.s to customer names, and just select the customer names 

    col=[]
    data=[]# instantiating variables

    rows=cursor.fetchall()#getting all rows from table

    for row in rows: 
        data.append(list(row))
    
    col = [column[0] for column in cursor.description]


    df_adj_hist=pd.DataFrame(data,columns=col)

    #formatting data 

    #drop event_no row
    cols_to_drop=[
        'EVENT_NO',
        'DOC_TYP',
        'BAT_ID',
        'ENTRY_SEQ_NO',
        'APPLY_TO_METH',
        'APPLY_TO_DOC_TYP',
        'DISC_DAT',
        'SLS_REP',
        'CUST_BAL_BEFORE',
        'LST_MAINT_DT',
        'LST_MAINT_USR_ID',
        'LST_LCK_DT',
        'ROW_TS',
        'CUST_STR_ID',
        'STR_ID'
    ]#a bit unnesscessary will modify to select only columns needed 

    df_adj_hist=df_adj_hist.drop(cols_to_drop,axis=1)
    return df_adj_hist

if __name__=='__main__':
    main()