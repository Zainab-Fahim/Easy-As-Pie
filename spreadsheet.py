import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)


products_table = client.open("BakesByMe").worksheet("products_table")
customer_table = client.open("BakesByMe").worksheet("customer_table")
pp=pprint.PrettyPrinter()

products_table_result = products_table.get_all_records()
products_table_dict = products_table.get_all_records()
products_table_list = products_table.get_all_values()

customer_table_result = customer_table.get_all_records()
customer_table_dict = customer_table.get_all_records()
customer_table_list = customer_table.get_all_values()

def all_list():
    for i in range (len(products_table_list)):
        pp.pprint(products_table_list[i])
def isAvailableToday():
    global availableToday
    availableToday=[]
    for i in products_table_dict:
        if (i['availability']=="TRUE"):
            item=[str(i['item_id']),i['item'],str(i['amount']),str(i['price'])]
            availableToday.append(item)
    return availableToday
def isAvailable():
    global available
    available=[]
    for i in products_table_dict:
        item=[str(i['item_id']),i['item'],str(i['amount']),str(i['price'])]
        available.append(item)
    return available


def save_cust_name(data):
    customer_table.update_cell(len(products_table_list)+3, 1, data)
def save_cust_address(data):
    customer_table.update_cell(len(products_table_list)+3, 2, data)
def save_cust_number(data):
    customer_table.update_cell(len(products_table_list)+3, 3, data)
def save_cust_item(data):
    customer_table.update_cell(len(products_table_list)+3, 4, data)
def save_cust_quantity(data):
    customer_table.update_cell(len(products_table_list)+3, 5, data)

def get_item_price(item):
    item=item.title()
    print(item)
    for data in products_table_dict:
        if data['item']==item:
            cost=data['price']
            return cost
def get_order_invoice():
    return customer_table_list[-1]

