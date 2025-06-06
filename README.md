
# PC Components Shop

**PC Components Shop** is an online store specializing in the sale of PC components, integrated with Stripe payment system and webhook handling. The project is built with Django and includes shopping cart functionality, order processing, and pagination support.

## 🔧 Technologies

- **Django** — for backend development
- **Stripe API** — for payment integration
- **PostgreSQL** — for data storage
- **Redis** — for data caching and performance improvement
- **flake8, black, isort** — for code formatting and adhering to standards


## ✨ Features

- **Product Catalog**: Display all available components with sorting and filtering options.
- **Shopping Cart**: Ability to add, remove items, and view the total cost of the order.
- **Order Checkout**: Integration with Stripe for order processing and payments.
- **Order History**: Users can view their order history.
- **Pagination**: Supports pagination for the product list.

## ▶️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Danya-Oleksuk/pc-components-shop
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
    
   EMAIL_HOST_USER=<your_email>
   EMAIL_HOST_PASSWORD=<email phrase>
    
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

6. **Run the project**:
   ```bash
   python manage.py runserver
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
- `requirements.txt` — list of dependencies.
