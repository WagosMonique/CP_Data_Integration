import pyodbc
import pandas as pd

# def connection(server):#this function performs the connection on a given server and returns a cursor.
def main():

    cnxn= pyodbc.connect("Driver={SQL Server Native Client 11.0};" 
                        "Server=SUPPORT03;"
                        "Database=TestGolf;"
                        "uid=sa;pwd=CounterPoint8")

    #the below is just for testing purposes and will be edited to integrate with the file integration
    cursor=cnxn.cursor()
    ar_df=adj_query(cursor)
    ar_df.to_excel("export\\ar_data.xlsx")

    tkt_df=tkt_hist(cursor)
    tkt_df.to_excel("export\\tkt_data.xlsx")

    tkt_lines_df=tkt_lines(cursor)
    tkt_lines_df.to_excel("export\\tkt_lines_data.xlsx")

    odoo_quotes=quote_import(cursor)
    odoo_quotes.to_excel("export\\quotes_data.xlsx")


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

def tkt_hist(cursor):
    
    
    col=[]
    data=[]# instantiating variables

    
    cursor.execute("SELECT BUS_DAT,DOC_ID,TKT_NO,TKT_DT,TKT_TYP,CUST_NO,LINS,SUB_TOT,TOT_EXT_COST,TOT FROM PS_TKT_HIST")

    rows=cursor.fetchall()#getting all rows from table

    for row in rows: 
        data.append(list(row))
    
    col = [column[0] for column in cursor.description]


    df_tkt_hist=pd.DataFrame(data,columns=col)

    return df_tkt_hist

def tkt_lines(cursor):
    
    
    col=[]
    data=[]# instantiating variables

    
    cursor.execute("SELECT BUS_DAT, TKT_NO,ITEM_NO,QTY_SOLD,PRC_1,CALC_PRC,REG_PRC,PRC,EXT_COST,EXT_PRC,UNIT_RETL_VAL,GROSS_EXT_PRC,CALC_EXT_PRC FROM PS_TKT_HIST_LIN")

    rows=cursor.fetchall()#getting all rows from table

    for row in rows: 
        data.append(list(row))
    
    col = [column[0] for column in cursor.description]


    df_tkt_hist_lines=pd.DataFrame(data,columns=col)

    return df_tkt_hist_lines


def quote_import(cursor):
    #merge data from ticket and lines

    col=[]
    data=[]

    cursor.execute("""SELECT a.BUS_DAT,a.DOC_ID,a.TKT_NO,a.TKT_DT,a.TKT_TYP,a.CUST_NO,a.LINS,a.SUB_TOT,a.TOT_EXT_COST,a.TOT,
                   b.ITEM_NO,b.QTY_SOLD,b.PRC_1,b.CALC_PRC,b.REG_PRC,b.PRC,b.EXT_COST,b.EXT_PRC,b.UNIT_RETL_VAL,b.GROSS_EXT_PRC,b.CALC_EXT_PRC 
                   FROM PS_TKT_HIST a 
                   JOIN PS_TKT_HIST_LIN b
                   ON a.TKT_NO=b.TKT_NO
                """)
    
    rows=cursor.fetchall()#getting all rows from table
   
    for row in rows: 
        data.append(list(row))

    
    col = [column[0] for column in cursor.description]


    df_tkt_data=pd.DataFrame(data,columns=col)
    quote_data=pd.DataFrame(columns=['Order Reference','Customer*','Order Date','Expiration','Order Lines/Products*','Order Lines/Quantity','Order Lines/Unit Price'])
    
    indicator=0
    for row in  df_tkt_data.itertuples(index=False):
        if indicator==0:
            if(row.LINS!=0):
                indicator=int(row.LINS)
                #write all line information into new df at this point
                quote_data.loc[len(quote_data)]={
                    'Order Reference': 'S'+str(row.TKT_NO),
                    'Customer*': row.CUST_NO,
                    'Order Date':row.TKT_DT,
                    'Order Lines/Products*': row.ITEM_NO,
                    'Order Lines/Quantity': row.QTY_SOLD,
                    'Order Lines/Unit Price': row.PRC_1
                }
                indicator-=1
        else:
            quote_data.loc[len(quote_data)]={
                'Order Reference': None,
                'Customer*': None,
                'Order Date':None,
                'Order Lines/Products*': row.ITEM_NO,
                'Order Lines/Quantity': row.QTY_SOLD,
                'Order Lines/Unit Price': row.PRC_1
            }
            indicator-=1

        print(indicator)


    return quote_data

if __name__=='__main__':
    main()