"""
Stripe Payment Integration for Tradie Audit Service
"""
import os
import stripe
from dotenv import load_dotenv

load_dotenv()

# Initialize Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Product configuration
AUDIT_PRICE = 79700  # $797 in cents
PRODUCT_NAME = "Tradie Profit Leak Audit"
PRODUCT_DESCRIPTION = "Complete financial audit with $10,000 money-back guarantee"


def create_checkout_session(
    success_url: str,
    cancel_url: str,
    customer_email: str = None,
    metadata: dict = None
) -> dict:
    """
    Create a Stripe Checkout session for the audit service.
    
    Args:
        success_url: URL to redirect after successful payment
        cancel_url: URL to redirect if customer cancels
        customer_email: Pre-fill customer email if known
        metadata: Additional data to attach to the session
    
    Returns:
        dict with checkout_url and session_id
    """
    try:
        session_params = {
            "payment_method_types": ["card"],
            "line_items": [{
                "price_data": {
                    "currency": "aud",
                    "product_data": {
                        "name": PRODUCT_NAME,
                        "description": PRODUCT_DESCRIPTION,
                        "images": [],  # Add product image URL if available
                    },
                    "unit_amount": AUDIT_PRICE,
                },
                "quantity": 1,
            }],
            "mode": "payment",
            "success_url": success_url,
            "cancel_url": cancel_url,
            "payment_intent_data": {
                "description": PRODUCT_NAME,
            },
            "metadata": metadata or {},
        }
        
        if customer_email:
            session_params["customer_email"] = customer_email
        
        session = stripe.checkout.Session.create(**session_params)
        
        return {
            "success": True,
            "checkout_url": session.url,
            "session_id": session.id
        }
    
    except stripe.error.StripeError as e:
        return {
            "success": False,
            "error": str(e)
        }


def verify_payment(session_id: str) -> dict:
    """
    Verify a payment was successful.
    
    Args:
        session_id: The Stripe checkout session ID
    
    Returns:
        dict with payment status and customer details
    """
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        
        if session.payment_status == "paid":
            return {
                "success": True,
                "paid": True,
                "customer_email": session.customer_details.email if session.customer_details else None,
                "customer_name": session.customer_details.name if session.customer_details else None,
                "amount_paid": session.amount_total / 100,
                "currency": session.currency.upper(),
                "metadata": session.metadata,
            }
        else:
            return {
                "success": True,
                "paid": False,
                "status": session.payment_status
            }
    
    except stripe.error.StripeError as e:
        return {
            "success": False,
            "error": str(e)
        }


def get_payment_link() -> str:
    """
    Create a reusable payment link (alternative to checkout sessions).
    Good for embedding directly on landing pages.
    """
    try:
        # First, create or get the product
        products = stripe.Product.list(limit=1, active=True)
        
        product = None
        for p in products.data:
            if p.name == PRODUCT_NAME:
                product = p
                break
        
        if not product:
            product = stripe.Product.create(
                name=PRODUCT_NAME,
                description=PRODUCT_DESCRIPTION,
            )
        
        # Create a price for the product
        price = stripe.Price.create(
            product=product.id,
            unit_amount=AUDIT_PRICE,
            currency="aud",
        )
        
        # Create payment link
        payment_link = stripe.PaymentLink.create(
            line_items=[{"price": price.id, "quantity": 1}],
        )
        
        return payment_link.url
    
    except stripe.error.StripeError as e:
        return None


# Test mode helper
def is_test_mode() -> bool:
    """Check if Stripe is in test mode."""
    api_key = os.getenv("STRIPE_SECRET_KEY", "")
    return api_key.startswith("sk_test_")

