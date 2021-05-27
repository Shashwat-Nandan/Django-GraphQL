import razorpay

def payment_razorpay(self):
    client = razorpay.Client(auth=("<YOUR_API_KEY>", "<YOUR_API_SECRET>"))

    order_amount = 50000
    order_currency = 'INR'
    order_receipt = 'order_rcptid_11'
    notes = {'Shipping address': 'Bommanahalli, Bangalore'}   # OPTIONAL

    client.order.create(amount=order_amount, currency=order_currency, receipt=order_receipt, notes=notes)
    # Returns an object containing order id

    params_dict = {
    'razorpay_order_id': '12122',
    'razorpay_payment_id': '332',
    'razorpay_signature': '23233'
    }
    client.utility.verify_payment_signature(params_dict)
