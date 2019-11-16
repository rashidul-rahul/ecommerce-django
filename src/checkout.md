#Checkout process

1. Cart -> checkout view
    ?
    - Login/Register or Enter an email
    - Shipping Address
    - Billing Info
        - Billing Address
        - Credit Card
2. Billing App/Component
    - User or Email (Guest Email)
    - Generate Payment Processor Token (Stripe or Braintree)

3. Order/Invoices Component
    - Connencting the billing profile
    - Shipping / billing Address
    - Cart
    - Status Shipped / Cancelled ?