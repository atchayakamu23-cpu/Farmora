# LocalFarm - Beginner Django Project

LocalFarm is a simple web application where local farmers can add farm products
and customers can browse products, add them to a cart, place orders and write reviews.

## Technologies
- HTML
- CSS
- JavaScript
- Python
- Django
- SQLite
- Pillow

## Main features
1. Customer/Farmer registration
2. Login and profile
3. Farmer can add, edit and delete products
4. Customer can search and filter products
5. Customer can add products to cart
6. Customer can place orders
7. Farmer can update order status
8. Customer can write and delete reviews

## How to run

### 1. Open the project
Open the `LocalFarm` folder in PyCharm.

### 2. Create a virtual environment
```powershell
python -m venv .venv
```

### 3. Activate it
```powershell
.venv\Scripts\activate
```

### 4. Install packages
```powershell
pip install -r requirements.txt
```

### 5. Create database tables
```powershell
python manage.py migrate
```

### 6. Start the server
```powershell
python manage.py runserver
```

Open:
http://127.0.0.1:8000/

## Admin
Create an admin account if needed:
```powershell
python manage.py createsuperuser
```

Then open:
http://127.0.0.1:8000/admin/

## Beginner project flow

Farmer:
Register -> Login -> My Products -> Add Product -> View Farmer Orders -> Update Order Status

Customer:
Register -> Login -> Products -> View Product -> Add to Cart -> Checkout -> My Orders -> Review
