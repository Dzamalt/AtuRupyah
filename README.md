# AtuRupyah: Inventory Management & Demand Forecasting System

RESTful backend system for managing inventory, tracking sales, and predicting future demand using historical data.

This project was built using Flask, SQLAlchemy, and Pandas, with JWT-based authentication and multi-user support.

---

# Features

- User authentication (JWT)
- Product management (CRUD)
- Inventory tracking with automatic stock updates
- Sales recording and history tracking
- Demand forecasting using Moving Average
- RESTful API architecture

---

# Tech Stack

**Backend**
- Python
- Flask
- SQLAlchemy
- SQLite

**Authentication**
- JWT (flask-jwt-extended)
- Werkzeug password hashing

**Data Processing**
- Pandas
- NumPy

---

# API Overview

Main endpoints:

/api/auth/register
/api/auth/login

/api/products
/api/inventory
/api/sales
/api/forecasts


All protected endpoints require JWT authentication:

Authorization: Bearer <access_token>


---

# Project Structure

project/
│
├── app.py
├── models.py
├── schemas.py
├── routes/
│ ├── auth.py
│ ├── products.py
│ ├── inventory.py
│ ├── sales.py
│ └── forecasts.py
│
└── README.md


---

# Forecasting

Current implementation uses:

- Moving Average forecasting
- Additional experimental forecasting methods

Forecasts are used to recommend reorder quantities.

---

# Status

- Backend complete
- Authentication implemented
- Forecasting implemented
- Documentation complete
- Not deployed yet

---

# Purpose

This project demonstrates practical backend development skills, including:

- REST API design
- Database modeling
- Authentication systems
- Data analysis integration
- Modular application architecture

---

# Future Improvements

- Frontend interface
- Deployment to cloud
- Advanced forecasting models
- Role-based access control

---
