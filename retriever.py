import pyodbc
import pandas as pd


#retrieves information from CP DB 

cnxn= pyodbc.connect("Driver={SQL Server Native Client 11.0};" 
                    "Server=SUPPORT03;"
                    "Database=TestGolf;"
                    "uid=sa;pwd=CounterPoint8")

cursor=cnxn.cursor()

def main():

    quote_data=quote_import()
    quote_data.to_excel("export\\quotes_data.xlsx", engine="xlsxwriter")

    return


def quote_import():
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
    quote_data=pd.DataFrame(columns=['Order Reference','Customer','Expiration','Products','Quantity','Unit_Price'])
    
    quote_rows = []
    indicator = 0

    for row in df_tkt_data.itertuples(index=False):
        if indicator == 0:#if there are no more lines on a ticket go to the next one
            if row.LINS != 0:
                indicator = int(row.LINS)
                quote_rows.append({
                    'Order_Reference': 'S' + str(row.TKT_NO),
                    'Customer': row.CUST_NO,
                    'Date': row.TKT_DT,
                    'Products': row.ITEM_NO,
                    'Quantity': row.QTY_SOLD,
                    'Unit_Price': row.PRC_1,
                    'Order_Lines': row.LINS
                })
                indicator -= 1
        else:
            quote_rows.append({
                        'Order_Reference': None,
                        'Customer': None,
                        'Order Date': None,
                        'Products': row.ITEM_NO,
                        'Quantity': row.QTY_SOLD,
                        'Unit_Price': row.PRC_1,
                        'Order_Lines': None
                        })
            indicator -= 1

# Create DataFrame once at the end
    quote_data = pd.DataFrame(quote_rows) 

    return quote_data


# def item_import(cursor):

#     col=['External ID','Name','Product_Type','Internal_Reference','Barcode',	'Sales_Price','Cost','Weight','Sales_Description']
#     data=[]

#     cursor.execute("""SELECT ITEM_NO, DESCR, ITEM_TYP, ITEM_NO,BARCOD,REG_PRC,LST_COST,WEIGHT,LONG_DESCR
#                       FROM IM_ITEM
#                 """)
    
#     rows=cursor.fetchall()#getting all rows from table
   
#     for row in rows: 
#         data.append(list(row))


#     df_item_data=pd.DataFrame(data,columns=col)

#     for data in df_item_data.itertuples(index=False):

#         df_item_data.loc[
#                 df_item_data['Product_Type'].isin(['D', 'N', 'T']),
#                 'Product_Type'
#             ] = 'Good'

#         df_item_data.loc[
#             ~df_item_data['Product_Type'].isin(['D', 'N', 'T']),
#             'Product_Type'
#             ] = 'Service'


#     return df_item_data


if __name__=='__main__':
    main()