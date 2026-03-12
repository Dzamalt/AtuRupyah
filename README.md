# AtuRupyah: Inventory Management & Demand Forecasting System

RESTful backend system for managing inventory, tracking sales, and predicting future demand using historical data.

This project was built using Flask, SQLAlchemy, and Pandas, with JWT-based authentication and multi-user support.

**URL:** https://aturupyah.onrender.com


**GitHub:** https://github.com/Dzamalt/AtuRupyah


**Documentation:** https://github.com/Dzamalt/AtuRupyah/wiki/AtuRupyah-API-Documentation


---

# Features

- User authentication (JWT)
- Product management (CRUD)
- Inventory tracking with automatic stock updates
- Restock recommendation based on past sales
- Sales recording and history tracking
- Demand forecasting using Moving Average
- RESTful API architecture

---

# Tech Stack

**Backend**
- Python
- Flask
- SQLAlchemy
- PostgreSQL
- Alembic

**Authentication**
- JWT (flask-jwt-extended)
- Werkzeug password hashing

**Data Processing**
- Pandas
- NumPy

---

# API Overview

Main endpoints:
```
/api/auth/register
/api/auth/login

/api/products
/api/inventory
/api/sales
/api/forecasts
```

All protected endpoints require JWT authentication:

`Authorization: Bearer <access_token>`


---

# Forecasting

Current implementation uses:

- Moving Average forecasting

Forecasts are used to recommend reorder quantities.

---

# Status

- Backend complete
- Authentication implemented
- Forecasting implemented
- Documentation complete
- Deployed

---

# Purpose

This project demonstrates practical backend development skills, including:

- REST API design
- Database modeling
- Authentication systems
- Data analysis integration
- Modular application architecture
- Deployment & Production Environment Setup

---

# Future Improvements

- Frontend interface with Bootstrap
- Advanced forecasting models with Prophet FB
- Role-based access control for team workflow
- AI implementation

---
