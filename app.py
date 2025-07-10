from flask import Flask, render_template, request, jsonify
import stripe
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@app.route("/")
def index():
    return render_template("index.html")  # Your landing page

@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "GBP",
                    "product_data": {
                        "name": "Option 1",
                    },
                    "unit_amount": 2000,  # Amount in pounds
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url="http://localhost:8080/success",
            cancel_url="http://localhost:8080/cancel",
        )
        return jsonify({"id": session.id})
    except Exception as e:
        print(f"Stripe error: {e}")
        return jsonify(error=str(e)), 403
@app.route("/cancel")
def cancel():
    return "<h1>Payment Cancelled</h1><p>You didn't complete the checkout. No worries—try again anytime!</p>"
if __name__ == "__main__":
    app.run(port=8080)