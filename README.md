# Payment WebApp

## Overview
This web application allows users to make payments using **PayPal** and **Stripe**. It securely processes transactions and stores payment activities in the backend for tracking and auditing purposes.

## Features
- **PayPal and Stripe Integration**: Supports both payment gateways.
- **Secure Transactions**: Uses encrypted connections and secure token authentication.
- **Backend Payment Tracking**: Stores payment history, user transactions, and status.
- **Modern UI**: Built with React for a smooth user experience.
- **Django Backend**: Handles payment processing and data storage.

## Tech Stack
### Frontend:
- React (with Tailwind CSS for styling)
- Axios for API requests

### Backend:
- Django (Django REST Framework)
- SQLite for development
- PayPal & Stripe SDKs

## Installation
### **1. Clone the Repository**
```bash
 git remote add origin https://github.com/Broock00/payment.git
 cd payment-webapp
```

### **2. Set Up the Backend**
```bash
 cd payment_app
 python -m venv venv
 source venv/bin/activate  # For macOS/Linux
 venv\Scripts\activate    # For Windows
 pip install -r requirements.txt
```

#### **Set up Environment Variables**
Create a `.env` file inside `backend/` and add:
```
SECRET_KEY=your_django_secret_key
STRIPE_SECRET_KEY=your_stripe_secret_key
PAYPAL_CLIENT_ID=your_paypal_client_id
PAYPAL_SECRET=your_paypal_secret
```

#### **Run Migrations and Start the Server**
```bash
 python manage.py makemigrations
 python manage.py migrate
 python manage.py runserver
```

### **3. Set Up the Frontend**
```bash
 cd ../payment-app-frontend
 npm install
 npm start
```

## API Endpoints
- `POST /api/payments/paypal/` → Process PayPal payments
- `POST /api/payments/stripe/` → Process Stripe payments
- `GET /api/payments/history/` → Retrieve payment history for users

## Usage
1. **Chooses a payment method** (PayPal or Stripe).
2. **Completes the transaction** securely.
3. **Payment details are stored** in the backend for future reference.

## License
This project is open-source and licensed under the MIT License.

