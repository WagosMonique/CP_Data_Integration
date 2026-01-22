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
    data=quote_import()#ticket information
    items=get_item_ids(data,uid)#dictionary of items on tickets
    customers=get_cust_ids(data,uid)#dictionary of customers on tickets
    post_tickets(items,customers,data,uid)
    


def authentication():#

    uid= common.authenticate(db, username, password, {})

    if uid:
        print("authentication successful")
    else:
        print("authentication failed ")

    return uid


def post_tickets(items,customers,tickets,uid):#sends tickets to odoo via api
    indicator = 0
    orders_to_create = []

    fields_info = models.execute_kw(db, uid, password, 
        'sale.order', 'fields_get', [], 
        {'attributes': ['string', 'help', 'type']})
    print(fields_info)

    for row in tickets.itertuples(index=False):
         if indicator == 0: #indicates if we are on a new ticket 
            if row.Order_Lines != 0:#only take tickets with lines
                indicator = int(row.Order_Lines)#get the number of lines

                header={'name':str(row.Order_Reference),'partner_id':str(customers[row.Customer]),'partner_shipping_id': customers[row.Customer],'partner_invoice_id': customers[row.Customer]}
                
                lines =[]

                line = (0, 0, {
                    'product_id': int(items[row.Products]),  # Adjust based on your actual column
                    'product_uom_qty': int(row.Quantity),  # Adjust column name
                    'price_unit': float(row.Unit_Price),  # Adjust column name
                })

                lines.append(line)

                indicator -= 1

                if indicator == 0:
                    header['order_line'] = lines
                    orders_to_create.append(header)
         else:
            line = (0, 0, {
                'product_id': int(items[row.Products]),
                'product_uom_qty': int(row.Quantity),
                'price_unit': float(row.Unit_Price),
            })

            lines.append(line)
            indicator -= 1

            if indicator==0:
                header['order_line'] = lines
                orders_to_create.append(header)

    for order_data in orders_to_create:
        print(models.execute_kw(db, uid, password, 'sale.order', 'create', [order_data]))



    return 


def get_item_ids(data,uid):
    products={}

    for row in data.itertuples():
        if row.Products not in products:#only unique products

            item_id=models.execute_kw(db, uid, password, 'product.product', 'search_read', [[['name','=',row.Products]]], {'fields': ['id']})#can be used to get fields of a particular model
            
            if not item_id:
                
                item_id=models.execute_kw(db, uid, password, 'product.product', 'create', [{'name':row.Proucts,'list_price':row.Unit_Price}])#search and read is used to get customer information
                products[row.Products]=item_id
                pprint.pprint(data)
                
            else:
                products[row.Products]=item_id[0]['id']
        
    return products


def get_cust_ids(data,uid):
    customers={}

    for row in data.itertuples():
        if row.Customer not in customers and row.Customer:#only unique products
            
            customer_id=models.execute_kw(db, uid, password, 'res.partner', 'search_read', [[['name','=',row.Customer]]], {'fields': ['id']})#can be used to get fields of a particular model
            
            if not customer_id:
                customer_id=models.execute_kw(db, uid, password, 'res.partner', 'create', [{'name':row.Customer,'Company Type':'Company'}])#search and read is used to get customer information
                customers[row.Customer]=customer_id

            else:

                customers[row.Customer]=customer_id[0]['id']
        
    return customers



if __name__ =="__main__":
    main()