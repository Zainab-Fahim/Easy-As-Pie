from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from spreadsheet import *
app = Flask(__name__)

@app.route("/")
def hello():
	return "Hello World!"

def cust_name(name):
	save_cust_name(name)
def cust_address(address):
	save_cust_address(address)
def cust_number(number):
	save_cust_number(number)
def cust_item(item):
	save_cust_item(item)
def cust_quantity(quantity):
	save_cust_quantity(quantity)

@app.route("/sms", methods=['POST'])
def reply():
	incoming_msg = request.form.get('Body').lower()
	response = MessagingResponse()
	print(incoming_msg)
	message=response.message()
	responded = False
	#words = incoming_msg
	words = incoming_msg.split('#')
	if "hello" in incoming_msg:
		reply = "Welcome to Easy As Pie!\nWould you like to place an order?\n\n(Acceptable responses *Yes* or *No*)"
		message.body(reply)
		responded = True
	if (len(words) == 1 and "yes" in incoming_msg):
		service_type_string = "Please enter the relevant number for the type of order you'd like to place\n1- Custom order\n2 - Pre-made items \n\n(Acceptable responses *1* or *2*)"
		message.body(service_type_string)
		responded = True
	elif len(words) == 1 and "no" in incoming_msg:
		reply="Ok. Have a nice day!"
		message.body(reply)
		responded = True
	if len(words) == 1 and "1" in incoming_msg:
		all_item_reply="Here are the list of items we are specialized in: \n"
		message.body(all_item_reply)
		message.body("\n_______________________________________\t \n"+"\n")
		message.body(all_item())
		message.body("\n____________________________________\t \n")
		message.body("Would you like to proceed in placing your order? \nPlease enter your choice in the following format only:\n*proceed #* _(Acceptable responses *Yes* or *No*)_ ")
		responded = True
	elif len(words) == 1 and "2" in incoming_msg:
		today_item_reply="Here are the list of items for today: \n"
		message.body(today_item_reply)
		message.body("\n_________________________________________\t \n"+"\n")
		message.body(today_item())
		message.body("\n____________________________________\t \n")
		message.body("Would you like to proceed in placing your order? \nPlease enter your choice in the following format only:\n*proceed #* _(Acceptable responses *Yes* or *No*)_ ")
		responded = True
	if len(words) != 1:
		input_type = words[0].strip().lower()
		input_string = words[1].strip()
		if input_type=="proceed" and input_string=="yes":
			message.body("Easy As Pie would love to know it's customers better. Do consider sending in few details as prompted.\n\nPlease Enter your Name in the following format only:\n*name #* _your name_ ")
			responded=True	
		if input_type=="name":
			cust_name(input_string)
			message.body("Please Enter your address in the following format only:\n*address #* _your address_ ")
			responded=True
		if input_type=="address":
			cust_address(input_string)
			message.body("Please Enter your contact number in the following format only:\n*contact #* _your contact number_ ")
			responded=True
		if input_type=="contact":
			cust_number(input_string)
			message.body("Thank You for giving us the chance to know you better.\n\n")
			message.body("\n\nPlease Enter the item name you wish to place an order for, in the following format only:\n*item #* _type the item name_ ")
			responded=True
		if input_type=="item":
			cust_item(input_string)
			message.body("Please Enter the quantity required in the following format only:\n*quantity #* _type the quantity required_ ")
			responded = True
		if input_type=="quantity":
			cust_quantity(input_string)
			message.body("Would you like to proceed in placing your invoice \nPlease enter your choice in the following format only:\n*invoice #* _(Acceptable responses *Yes* or *No*)_ ")
			responded=True
		if input_type=="invoice":
			message.body("\nThis is your complete order invoice:\n\n")
			message.body(order_invoice())
			message.body("\n\n\n```Thank You for ordering with Us.\nWe hope to be of service to you in the future as well.\nHave a great day!```")

			

		


    
	if not responded:
		message.body('Incorrect request format. Please enter in the correct format')
	return str(response)
def all_item():
	items= isAvailable()
	reply="\n"
	for item in items: 
		reply += "\n *"+item[0]+"* - "+item[1]+" ("+item[2]+" )\t= "+item[3]
	return reply
def today_item():
	items= isAvailableToday()
	reply="\n"
	for item in items: 
		reply += "\n *"+item[0]+"* - "+item[1]+" ("+item[2]+" )\t= "+item[3]
	return reply  
def order_invoice():									
    val=get_order_invoice()
    price = get_item_price(val[3])
    quantity= int(val[4])
    total_cost= int(price)*quantity
    reply="\n"
    reply += "\nYour Name: *"+val[0]+"*\nYour Address: *"+val[1]+"*\nYour Contact Number: *"+val[2]+"*\nItem Ordered: *"+val[3]+"*\nQuantity of Ordered Item: *"+val[4]+"*\nYour Payment is : $"+str(total_cost)+"\n\n"
    return reply

	






if __name__ == "__main__":
	app.run(debug=True)