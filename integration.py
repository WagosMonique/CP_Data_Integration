from retriever import quote_import
import xmlrpc.client
import pandas as pd
import pprint 

url='https://wagosmonique-api-testing.odoo.com'#put your url name for your db here
db='wagosmonique-api-testing-main-27639352'#can be found by doing echo $PGDATABASE in the shell

username='monique@wagos.com'#the user email associated with your api key 
password='fe235116d8a6fbac4f326f0eddad074527b0c213'#put your api key as the password
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))  # For auth
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))  # For data

def main():
    
        
    uid= authentication()
    print(uid)
    data=quote_import()#ticket information
    items=get_item_ids(data,uid)#dictionary of items on tickets
    customers=get_cust_ids(data,uid)#dictionary of customers on tickets
    post_tickets(items,customers,data)
    


def authentication():

    uid= common.authenticate(db, username, password, {})

    if uid:
        print("authentication successful")
    else:
        print("authentication failed ")

    return uid


def post_tickets(items,customers,tickets):
    # data = models.execute_kw(db, uid, password, 'sale.order', 'create', [{}])
    indicator = 0
    for row in tickets.itertuples(index=False):
         if indicator == 0: #indicates if we are on a new ticket 
            if row.LINS != 0:#only take tickets with lines
                indicator = int(row.LINS)#get the number of lines
                header={'Reference':row.Order_Reference}
                indicator -= 1
         else:
            indicator -= 1


    return 


def get_item_ids(data,uid):
    products={}

    for row in data.itertuples():
        if row.Products not in products:#only unique products

            item_id=models.execute_kw(db, uid, password, 'product.product', 'search_read', [[['name','=',row.Products]]], {'fields': ['id']})#can be used to get fields of a particular model
            products[row.Products]=item_id[0]['id']
        
    return products


def get_cust_ids(data,uid):
    customers={}

    for row in data.itertuples():
        if row.Customer not in customers and row.Customer:#only unique products
            customer_ids=models.execute_kw(db, uid, password, 'res.partner', 'search_read', [[['name','=',row.Customer]]], {'fields': ['id']})#can be used to get fields of a particular model
            customers[row.Customer]=customer_ids[0]['id']

    print(customers)
        
    return customers



if __name__ =="__main__":
    main()