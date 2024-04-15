import requests
import stripe

url = "https://supersent.in/api/send-email/"

def send_mail(to,subject,content):
    data = {
        "subject":subject,
        "to_email":to,
        "context":{
            "message":content
        },
        "api_key":"25a36e7d3c7f4e3" # change this if needed
    }
    res = requests.post(url=url,headers={},json=data)
    print("Response of Sending Email : ",res.text,"\n")


STRIPE_PUBLIC_KEY = 'pk_test_51NwJLmSIPysML8WMJNFhx75blOYkWteVi5QhkbW9uK8nO6BGZlyqiQ8oYCk8ERmHcj8AyNlid3g9S6A2pYf57D3n00nEJFtGKL' # change this
STRIPE_SECRET_KEY = 'sk_test_51NwJLmSIPysML8WMXUqC8NV6nDdQ9iWIdaby9LoKNtWeI8vuZ6QUMTKqqef4ja9NvjZyj2IaQuMokUAfMamL40cC00D7ZfDTox' # change this


def create_stripe_payment_link(amount):
    amount = int(amount)
    stripe.api_key = STRIPE_SECRET_KEY
    msg =  "Wallet recharge successfull!"
    try:
        payment_link = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {
                            'name': 'RECHARGE WALLET',
                        },
                        'unit_amount': int(amount*100),  # Amount in cents
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url= f"http://127.0.0.1:8000/?err={msg}"
            
        )
        return payment_link.url
    except stripe.error.StripeError as e:
        msg = f"🚫 PAYMENT LINK GENERATION FAILED -> {e}"
        print("MSG : ",msg)
        return None