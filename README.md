
<h1 align="center">💻 PC Components Shop </h1>

<table align="center">
  <tr>
    <td align="center"><img src="assets/screenshots/main-page.png" width="1111"/><br/>Main Page</td>
    <td align="center"><img src="assets/screenshots/product-page.png" width="1111"/><br/>Product Page</td>
  </tr>
</table>

**PC Components Shop** is an online store built with Django, featuring product catalog, search & filters, shopping cart, wishlist, order processing, Stripe payment integration, webhook handling, multi-language support, and user authentication, with Docker and NGINX for deployment and PostgreSQL for database storage.

## 🔧 Technologies

- **Django** — for backend development
- **Django REST Framework (DRF)** — for building a modular and structured RESTful API
- **Stripe API** — for payment integration
- **PostgreSQL** — for data storage
- **Redis** — for data caching and performance improvement
- **Nova Poshta API** — integration for searching for branches and delivery addresses
- **Gunicorn + Nginx** — gunicorn serves the app, while Nginx acts as a reverse proxy and handles static/media files
- **Docker & Docker Compose** — for easy deployment and service management
- **flake8, black, isort** — for code formatting and adhering to standards


## ✨ Features

- **Product Catalog**: Display all available components with sorting and filtering options
- **Shopping Cart**: Ability to add, remove items, and view the total cost of the order
- **Order Checkout**: Integration with Stripe for order processing and payments
- **Order History**: Users can view their order history
- **Wishlist**: Users can add and remove products from their wishlist for future purchases
- **Pagination**: Supports pagination for the product list
- **Localization**: Support for Ukrainian and English languages with UI language switch
- **Tests**: Unit tests for order processing, forms, and views
- ### API - The project provides a RESTful API powered by Django REST Framework (DRF). The API is divided into modules for clear structure and scalability:

- `/api/products/` — retrieve products, apply filters by category or price, and perform search queries  
- `/api/cart/` — manage the shopping cart: add, update, or remove items  
- `/api/users/` — handle user-related actions such as registration, authentication, wishlist, and viewing order history  

---

## ▶️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Danya-Oleksuk/pc-components-shop.git
   cd pc-components-shop
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use venv/Scripts/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:

   Create a `.env` file in the root of the project and add the following:

   ```env
   REDIS_HOST=redis://<your_host>:6379

   CELERY_BROKER_URL=redis://<your_host>:6379
   CELERY_RESULT_BACKEND=redis://<your_host>:6379
    
   DB_NAME=<your_db_name>
   DB_USER=<your_db_user>
   DB_PASSWORD=<your_db_password>
   DB_HOST=<your_db_host>
   
   DEBUG=False
   
   STRIPE_SECRET_KEY=<your_stripe_secret_key>
   STRIPE_PUBLIC_KEY=<your_stripe_public_key>
   STRIPE_WEBHOOK_SECRET=<your_stripe_webhook_key>

   NOVA_POSHTA_API_KEY=<your_api_key>
   ```

5. **Run database migrations**:
   ```bash
   python manage.py migrate
   ```
   
6. **Run Redis Server**:
   ```bash
   redis-server
   ```
   
7. **Run the project**:
   ```bash
   python manage.py runserver
   ```


## 🚀 **Run with Docker**

### 1. Clone the repository (if you haven't already):

```bash
git clone https://github.com/Danya-Oleksuk/pc-components-shop
cd pc-components-shop
```

### 2. Ensure you have Docker and Docker Compose installed on your system.

!!! If you don’t have Docker installed, follow the instructions on the [official Docker website](https://www.docker.com/get-started).

### 3. Build and start the containers:

In the root directory of your project, run:

```bash
docker-compose up --build -d
```

### 4. Apply database migrations:

Once the containers are up and running, you need to apply the database migrations:

```bash
docker-compose exec web python manage.py migrate
```

### Access the application:

```
http://<server_ip_or_host_domen>:8000
```
---
   
## 🧪 Tests
The project includes unit and integration tests for order forms, views, and URL resolution. Tests are written using Django's built-in `TestCase` and can be run using:

```bash
python manage.py test
   ```

## 📁 Project Structure

- `pc_components_shop/` — main project folder.
- `orders/` — application for handling orders.
- `products/` — application for the product catalog.
- `users/` — application for user management.
- `errors/` — application for сustom error pages.
- `info/` — application for displaying additional information about the store (e.g., contact details, store policy).
- `templates/` — HTML templates.
- `static/` — static files (CSS, JavaScript, images).
- `media/` — user-uploaded files (e.g., product images).
- `api/` — application for managing API endpoints for products, users, and orders.
- `requirements.txt` — list of dependencies.
