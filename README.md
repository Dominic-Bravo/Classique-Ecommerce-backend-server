update in future and refactor codebase
updates
change auth socials and permissions


# Classique Ecommerce Backend Server

Classique Ecommerce Backend Server is a Django REST API for an ecommerce app.
It includes user authentication, social login hooks, role-based API permissions,
catalog/product management, and customer ordering.

## Features

- JWT login and refresh tokens with SimpleJWT.
- Registration through custom API and `dj-rest-auth`.
- Google and Facebook social login endpoints.
- Role support for `anonymous`, `customer`, and `owner`.
- Owner approval workflow:
  - Users can request or switch to the `owner` role.
  - Owner permissions stay disabled until a superadmin approves the request.
- Public catalog browsing.
- Owner-only category and product create/update/delete.
- Customer ordering with product stock deduction.
- Admin-only endpoint for listing all users.
- OpenAPI schema and Swagger/Redoc documentation with `drf-spectacular`.

## Tech Stack

- Python 3.12+
- Django 6
- Django REST Framework
- SimpleJWT
- dj-rest-auth
- django-allauth
- drf-spectacular
- SQLite for local development
- `uv` for dependency and environment management

## Project Structure

```text
.
+-- catalog/        # Categories and products
+-- config/         # Django project settings and root URLs
+-- orders/         # Orders and order items
+-- users/          # Custom user model, auth, roles, permissions
+-- manage.py
+-- pyproject.toml
+-- uv.lock
+-- README.md
```

## Setup With uv

Install `uv` first if you do not have it:

```bash
pip install uv
```

Clone/open the project, then install dependencies:

```bash
uv sync
```

Run database migrations:

```bash
uv run python manage.py migrate
```

Create a superadmin account:

```bash
uv run python manage.py createsuperuser
```

Start the development server:

```bash
uv run python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

## API Documentation

Swagger UI:

```text
http://127.0.0.1:8000/api/docs/
```

Redoc:

```text
http://127.0.0.1:8000/api/redoc/
```

Raw OpenAPI schema:

```text
http://127.0.0.1:8000/api/schema/
```

To regenerate the local `schema.yml` file:

```bash
uv run python manage.py spectacular --file schema.yml
```

## Authentication

Register with the custom endpoint:

```http
POST /api/register/
```

Example:

```json
{
  "username": "jane",
  "email": "jane@example.com",
  "password": "StrongPass#2026",
  "role": "customer"
}
```

Register with `dj-rest-auth`:

```http
POST /api/auth/registration/
```

Example:

```json
{
  "username": "store-owner",
  "email": "owner@example.com",
  "password1": "StrongPass#2026",
  "password2": "StrongPass#2026",
  "role": "owner"
}
```

Login:

```http
POST /api/login/
```

Example:

```json
{
  "username": "jane",
  "password": "StrongPass#2026"
}
```

Refresh token:

```http
POST /api/refresh/
```

Use the access token in API requests:

```http
Authorization: Bearer <access-token>
```

## Roles and Permissions

The system supports three roles:

- `anonymous`: default role when no role is provided. Can only view/read data.
- `customer`: can view catalog data and order products.
- `owner`: can manage catalog and products only after superadmin approval.

Users can update their role anytime:

```http
PATCH /api/users/me/role/
```

Example:

```json
{
  "role": "owner"
}
```

If a user changes to `owner`, their `owner_approval_status` becomes `pending`.
They will not receive owner permissions until a superadmin approves them in the
Django admin.

If a user changes to `customer` or `anonymous`, their owner approval status
resets to `not_requested`.

## Superadmin Owner Approval

Open Django admin:

```text
http://127.0.0.1:8000/admin/
```

Login with the superuser created earlier.

Go to the Users table and check users with:

```text
role = owner
owner_approval_status = pending
```

Superadmins can approve or reject selected owner requests using the admin
actions.

## Main Endpoints

### Users

```http
GET /api/users/
```

Lists all users. Admin/staff only.

```http
GET /api/users/me/role/
PATCH /api/users/me/role/
PUT /api/users/me/role/
```

Retrieve or update the logged-in user's role.

### Catalog

```http
GET /api/categories/
POST /api/categories/
GET /api/categories/<id>/
PUT /api/categories/<id>/
PATCH /api/categories/<id>/
DELETE /api/categories/<id>/
```

```http
GET /api/products/
POST /api/products/
GET /api/products/<id>/
PUT /api/products/<id>/
PATCH /api/products/<id>/
DELETE /api/products/<id>/
```

Anyone can view categories and products.
Only approved owners, staff, or superusers can create, update, or delete them.

### Orders

```http
GET /api/orders/
POST /api/orders/
GET /api/orders/<id>/
```

Customers can place orders and view their own orders.
Owners/staff/superusers can view all orders.

Create order example:

```json
{
  "items": [
    {
      "product": 1,
      "quantity": 2
    }
  ]
}
```

When an order is created, product stock is reduced.

## Social Login

Google:

```http
POST /api/auth/google/
```

Facebook:

```http
POST /api/auth/facebook/
```

Social login uses `django-allauth` and `dj-rest-auth`. Configure provider
client IDs and secrets through Django admin under Social Applications.

For local testing, make sure the callback URLs match the configured frontend:

```text
http://localhost:3000/google-callback
http://localhost:3000/facebook-callback
```

## Useful Commands

Run checks:

```bash
uv run python manage.py check
```

Run tests:

```bash
uv run python manage.py test
```

Create migrations:

```bash
uv run python manage.py makemigrations
```

Apply migrations:

```bash
uv run python manage.py migrate
```

Run development server:

```bash
uv run python manage.py runserver
```

Regenerate API schema:

```bash
uv run python manage.py spectacular --file schema.yml
```

## Local Database

The project uses SQLite locally:

```text
db.sqlite3
```

This is fine for development. For production, configure a production database
in `config/settings.py` or through environment-specific settings.

## Notes

- Keep `SECRET_KEY`, OAuth credentials, and production database credentials out
  of source control.
- `DEBUG = True` is for local development only.
- `ALLOWED_HOSTS` should be configured before deployment.
- Registered users with `role = anonymous` are authenticated but still limited
  to read-only behavior until they change role.
