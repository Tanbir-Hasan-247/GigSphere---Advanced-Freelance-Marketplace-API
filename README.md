<div align="center">

<br/>

```
  ██████╗ ██╗ ██████╗ ███████╗██████╗ ██╗  ██╗███████╗██████╗ ███████╗
 ██╔════╝ ██║██╔════╝ ██╔════╝██╔══██╗██║  ██║██╔════╝██╔══██╗██╔════╝
 ██║  ███╗██║██║  ███╗███████╗██████╔╝███████║█████╗  ██████╔╝█████╗  
 ██║   ██║██║██║   ██║╚════██║██╔═══╝ ██╔══██║██╔══╝  ██╔══██╗██╔══╝  
 ╚██████╔╝██║╚██████╔╝███████║██║     ██║  ██║███████╗██║  ██║███████╗
  ╚═════╝ ╚═╝ ╚═════╝ ╚══════╝╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝
```

### 💼 A Production-Grade Freelance Marketplace REST API

#### *Strict State Machines · Snapshot Pricing · Optimized Dashboards · Object-Level Permissions*

<br/>

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.x-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/Django_REST_Framework-FF1709?style=for-the-badge&logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![JWT](https://img.shields.io/badge/JWT-Djoser-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)](https://jwt.io)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Production-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Swagger](https://img.shields.io/badge/Swagger_UI-85EA2D?style=for-the-badge&logo=swagger&logoColor=black)](https://swagger.io)

<br/>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![API Docs](https://img.shields.io/badge/API_Docs-Swagger-85EA2D?style=flat-square&logo=swagger)](http://127.0.0.1:8000/swagger/)
[![Maintained](https://img.shields.io/badge/Maintained-yes-green.svg?style=flat-square)](https://github.com/Tanbir-Hasan-247)

<br/>

[**API Documentation**](http://127.0.0.1:8000/swagger/) · [**Report a Bug**](https://github.com/Tanbir-Hasan-247/GigSphere/issues) · [**Request a Feature**](https://github.com/Tanbir-Hasan-247/GigSphere/issues)

<br/>

</div>

---

## 📖 Table of Contents

- [About The Project](#-about-the-project)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [System Architecture](#-system-architecture)
- [Order State Machine](#-order-state-machine)
- [Permission System](#-permission-system)
- [API Reference](#-api-reference)
- [API Documentation](#-api-documentation)
- [Getting Started](#-getting-started)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [Author](#-author)

---

## 🌟 About The Project

**GigSphere** is a pure REST API backend for a freelance marketplace, built with Django REST Framework (DRF). It is engineered with a focus on **correctness, security, and performance** — not just working endpoints, but a robust architecture that mirrors production systems.

It features strict state-machine order workflows, snapshot pricing to preserve order integrity, bulletproof one-review-per-order constraints, object-level permission classes, and aggregate dashboards optimized with conditional ORM queries to eliminate N+1 issues.

> 💡 **Why GigSphere?**
> Most freelance platform tutorials show you how to create CRUD endpoints. GigSphere goes further — enforcing the business rules that make a real marketplace trustworthy: you can't skip order stages, prices can't change after an order is placed, and a buyer can only review what they actually completed. These constraints are what separate a demo from a deployable product.

---

## ✨ Key Features

<details>
<summary><b>🔐 Role-Based Authentication (Buyer & Seller)</b></summary>
<br/>

| Feature | Description |
|---|---|
| Custom User Model | Supports two account roles: `Buyer` and `Seller` at registration |
| JWT Login | Djoser + SimpleJWT — access & refresh token flow |
| Token Blacklisting | Logout invalidates the refresh token permanently |
| Profile Management | Authenticated users can view and update their own profile |

</details>

<details>
<summary><b>🏷️ Service (Gig) Management</b></summary>
<br/>

| Feature | Description |
|---|---|
| Full CRUD | Sellers create, update, and manage their service listings |
| Soft Delete | Services are deactivated (`is_active=False`) rather than hard-deleted, preserving all historical order records |
| Category Tagging | Services are organized under browsable categories |
| Filtering & Sorting | Buyers can filter services by category, price, and rating |

</details>

<details>
<summary><b>📦 Strict Order State Machine</b></summary>
<br/>

Order status transitions are strictly enforced — no skipping, no going back:

```
Pending  -->  In Progress  -->  Completed
                          -->  Cancelled
```

| Transition | Who Can Trigger |
|---|---|
| `Pending` → `In Progress` | Seller accepts the order |
| `In Progress` → `Completed` | Seller marks work as done |
| `Pending` → `Cancelled` | Buyer or Seller cancels before work begins |
| `In Progress` → `Cancelled` | Only with mutual agreement (configurable) |

</details>

<details>
<summary><b>💰 Snapshot Pricing</b></summary>
<br/>

When a buyer places an order, the service price is **captured and frozen** as `price_at_order`.

This means if a seller later updates their service price, all previous orders retain their original agreed price — exactly as a real marketplace should work.

</details>

<details>
<summary><b>⭐ Bulletproof Review System</b></summary>
<br/>

| Constraint | Detail |
|---|---|
| One Review Per Order | A buyer can only submit one review per order (enforced at DB level) |
| Completed Orders Only | Reviews are only accepted on orders with `Completed` status |
| Auto Rating Recalculation | Deleting a review automatically recalculates the service's average rating |
| Review Ownership | Only the original buyer can edit or delete their own review |

</details>

<details>
<summary><b>📊 Optimized Role Dashboards</b></summary>
<br/>

Single-endpoint aggregate dashboards for each role, built with Django ORM's **conditional aggregation** (`Q` objects) to avoid N+1 query problems:

| Dashboard | Endpoint | Data Returned |
|---|---|---|
| **Seller** | `/seller/dashboard/` | Total orders, earnings, active gigs, average rating |
| **Buyer** | `/buyer/dashboard/` | Active orders, completed orders, cancelled orders, total spent |

</details>

<details>
<summary><b>🔔 Notifications</b></summary>
<br/>

| Feature | Description |
|---|---|
| Auto-Generated | Notifications created automatically on order events (new order, status change) |
| Personal Feed | Users can fetch their own unread and read notifications |
| Mark as Read | Individual notifications can be marked read via `PATCH` |

</details>

<details>
<summary><b>💳 Future-Ready Payment Schema</b></summary>
<br/>

The database schema includes pre-designed placeholder fields for payment integration (Stripe / SSLCommerz), meaning payment support can be wired in without major refactoring.

</details>

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology |
|:---:|:---:|
| **Language** | Python 3.10+ |
| **Framework** | Django 5.x |
| **API Layer** | Django REST Framework (DRF) |
| **Authentication** | Djoser + `djangorestframework-simplejwt` (with Token Blacklisting) |
| **Database (Dev)** | SQLite |
| **Database (Prod)** | PostgreSQL |
| **API Documentation** | `drf-spectacular` / `drf-yasg` (Swagger UI) |
| **Filtering** | `django-filter` |
| **ORM Optimization** | Conditional Aggregation with `Q` objects |

</div>

---

## 🏗️ System Architecture

```
+------------------------------------------------------------------------+
|                           GigSphere API                                |
|                                                                        |
|  +----------+              +----------+              +----------+      |
|  |  Buyer   |              |  Seller  |              |  Admin   |      |
|  +----+-----+              +----+-----+              +----+-----+      |
|       |                        |                         |            |
|  +----v------------------------v-------------------------v-----------+ |
|  |              Djoser + JWT Authentication Layer                    | |
|  |         (Role Check: IsBuyer / IsSeller on every request)        | |
|  +-----------------------------------+-------------------------------+ |
|                                      |                                 |
|  +-----------------------------------v-------------------------------+ |
|  |                  Django REST Framework (DRF)                      | |
|  |     ViewSets . Serializers . Permissions . Routers . Filters      | |
|  +----------+------------------+-------------------+----------------+ |
|             |                  |                   |                  |
|  +----------v------+  +--------v--------+  +-------v-----------+     |
|  |  Service / Gig  |  |  Order Engine   |  |  Review System    |     |
|  |  Module         |  |  (State Machine |  |  (1-per-order     |     |
|  |  (Soft Delete)  |  |  + Snapshot     |  |   constraint +    |     |
|  |                 |  |   Pricing)      |  |   auto-rating)    |     |
|  +----------+------+  +--------+--------+  +-------+-----------+     |
|             |                  |                   |                  |
|  +----------v------------------v-------------------v----------------+ |
|  |              Django ORM  <->  SQLite / PostgreSQL                | |
|  |        (Conditional Aggregation for N+1-free Dashboards)         | |
|  +------------------------------------------------------------------+ |
|                                                                        |
|  +------------------------------+  +--------------------------------+  |
|  |  Notification Engine         |  |  Swagger UI (drf-spectacular)  |  |
|  |  (Auto-triggered on events)  |  |  /swagger/                     |  |
|  +------------------------------+  +--------------------------------+  |
+------------------------------------------------------------------------+
```

---

## 🔄 Order State Machine

```
                    +---------------------------+
   Buyer Places     |                           |
   Order ---------> |        PENDING  [?]       |
                    |                           |
                    +--------+----------+-------+
                             |          |
              Seller Accepts |          | Buyer/Seller Cancels
                             v          v
                    +-----------+   +-------------+
                    |           |   |             |
                    | IN PROGR- |   |  CANCELLED  |
                    | ESS  [>>] |   |    [XX]     |
                    |           |   |             |
                    +-----+-----+   +-------------+
                          |
               Work Done  |
                          v
                    +---------------------------+
                    |                           |
                    |      COMPLETED  [OK]      |
                    |                           |
                    +---------------------------+
                          |
              Only after  |
              COMPLETED   v
                    +---------------------------+
                    |                           |
                    |   REVIEW UNLOCKED  [*]    |
                    |   (1 per order, buyer)    |
                    |                           |
                    +---------------------------+
```

---

## 🔒 Permission System

GigSphere uses a layered, object-level permission system. Every endpoint is guarded at both the role and ownership level:

<div align="center">

| Permission Class | Scope | Description |
|:---:|:---:|---|
| `IsSeller` | Role | Blocks non-Seller accounts from accessing seller-only endpoints |
| `IsBuyer` | Role | Blocks non-Buyer accounts from accessing buyer-only endpoints |
| `IsServiceOwner` | Object | Only the gig author can update or (soft) delete their service |
| `IsOrderParticipant` | Object | Only the specific buyer or seller of an order can view or update it |
| `IsReviewOwner` | Object | Only the review author can edit or delete their review |

</div>

---

## 📌 API Reference

### 🔐 Authentication (`/auth/`)

| Method | Endpoint | Description | Access |
|:---:|---|---|:---:|
| `POST` | `/auth/users/` | Register a new Buyer or Seller account | Public |
| `GET` | `/auth/users/me/` | Retrieve current user's profile | Auth |
| `PATCH` | `/auth/users/me/` | Update current user's profile | Auth |
| `POST` | `/auth/jwt/create/` | Login — obtain JWT access & refresh tokens | Public |
| `POST` | `/auth/jwt/refresh/` | Refresh an expired access token | Public |

### 📊 Dashboards

| Method | Endpoint | Description | Access |
|:---:|---|---|:---:|
| `GET` | `/seller/dashboard/` | Aggregate stats: orders, earnings, active gigs, rating | Seller Only |
| `GET` | `/buyer/dashboard/` | Aggregate stats: active, completed, cancelled orders | Buyer Only |

### 🏷️ Categories & Services

| Method | Endpoint | Description | Access |
|:---:|---|---|:---:|
| `GET` | `/categories/` | List all available service categories | Public |
| `GET` | `/services/` | List all active services (filterable & sortable) | Public |
| `POST` | `/services/` | Create a new gig listing | Seller |
| `GET` | `/services/{id}/` | Retrieve details of a specific service | Public |
| `PATCH` | `/services/{id}/` | Update a gig's details | Service Owner |
| `DELETE` | `/services/{id}/` | Soft-delete a service (`is_active=False`) | Service Owner |

### 🛒 Orders

| Method | Endpoint | Description | Access |
|:---:|---|---|:---:|
| `POST` | `/services/{service_id}/order/` | Place an order for a service | Buyer |
| `GET` | `/orders/` | View personal order history | Auth |
| `PATCH` | `/orders/{id}/status/` | Advance order through state machine | Order Participant |

### ⭐ Reviews

| Method | Endpoint | Description | Access |
|:---:|---|---|:---:|
| `POST` | `/orders/{order_id}/review/` | Submit a review (Completed orders only) | Order Buyer |
| `GET` | `/services/{service_id}/reviews/` | View all reviews for a service | Public |
| `PATCH` | `/reviews/{id}/` | Edit own review | Review Owner |
| `DELETE` | `/reviews/{id}/` | Delete own review (auto-recalculates rating) | Review Owner |

### 🔔 Notifications

| Method | Endpoint | Description | Access |
|:---:|---|---|:---:|
| `GET` | `/notifications/` | Retrieve all personal notifications | Auth |
| `PATCH` | `/notifications/{id}/read/` | Mark a specific notification as read | Notification Owner |

> 📖 Full request bodies, response schemas, and live testing at:
> **http://127.0.0.1:8000/swagger/**

---

## 📚 API Documentation

GigSphere ships with **auto-generated, always-in-sync** interactive API docs:

<div align="center">

| Interface | URL | Description |
|:---:|---|---|
| 🟡 **Swagger UI** | `/swagger/` | Try every endpoint live in your browser |
| 📘 **ReDoc** | `/redoc/` | Clean, readable reference documentation |
| 📄 **OpenAPI Schema** | `/schema/` | Raw OpenAPI 3.0 YAML for client generation |

</div>

---

## 🚀 Getting Started

### Prerequisites

- **Python** `>= 3.10` — [Download](https://python.org/downloads)
- **Git** — [Download](https://git-scm.com/)
- **pip** — bundled with Python 3.x

---

### Installation

**Step 1 — Clone the repository**

```bash
git clone https://github.com/Tanbir-Hasan-247/GigSphere.git
cd GigSphere
```

**Step 2 — Create and activate a virtual environment**

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS / Linux
source venv/bin/activate
```

**Step 3 — Install dependencies**

```bash
pip install -r requirements.txt
```

**Step 4 — Apply database migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

**Step 5 — Create a superuser (Admin)**

```bash
python manage.py createsuperuser
```

**Step 6 — Start the development server**

```bash
python manage.py runserver
```

🎉 API is live at **http://127.0.0.1:8000/**
📚 Swagger docs at **http://127.0.0.1:8000/swagger/**

---

## 🗺️ Roadmap

- [x] ✅ Buyer & Seller role-based authentication with Djoser + JWT
- [x] ✅ Service (gig) CRUD with soft delete to preserve order history
- [x] ✅ Strict 4-stage order state machine with enforced transitions
- [x] ✅ Snapshot pricing (`price_at_order`) for order integrity
- [x] ✅ One-review-per-completed-order constraint (DB-level)
- [x] ✅ Auto-recalculating service ratings on review deletion
- [x] ✅ Object-level permission classes (5 custom classes)
- [x] ✅ N+1-free aggregate dashboards via conditional ORM aggregation
- [x] ✅ Auto-triggered notification system
- [x] ✅ Future-ready payment schema placeholders
- [ ] 💳 **Payment Gateway** — Stripe or SSLCommerz integration using existing schema
- [ ] 📧 **Email Notifications** — Order events trigger emails via Django Signals
- [ ] 💬 **Buyer-Seller Messaging** — In-platform chat thread per order
- [ ] 📊 **Admin Analytics API** — Revenue reports, top sellers, category breakdown
- [ ] 🐳 **Docker Support** — Containerized dev and production setup
- [ ] 🔍 **Elasticsearch Integration** — Full-text gig search with relevance ranking

---

## 🤝 Contributing

Contributions, issues, and feature requests are warmly welcome!

1. **Fork** the repository
2. **Create** a feature branch → `git checkout -b feature/AmazingFeature`
3. **Commit** your changes → `git commit -m 'Add AmazingFeature'`
4. **Push** to the branch → `git push origin feature/AmazingFeature`
5. **Open a Pull Request**

Please ensure your code respects the existing permission architecture, follows DRF conventions, and includes appropriate tests for any new state transitions.

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more information.

---

## 👨‍💻 Author

<div align="center">

### Tanbir Hasan

*Aspiring Software Developer & Competitive Programmer*

<br/>

[![Email](https://img.shields.io/badge/Email-tanbirhasan569%40gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:tanbirhasan569@gmail.com)
[![GitHub](https://img.shields.io/badge/GitHub-Tanbir--Hasan--247-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Tanbir-Hasan-247)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/tanbir-hasan-638075345/)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-3b82f6?style=for-the-badge&logo=safari&logoColor=white)](https://tanbir-hasan-247.github.io/Tanbir-Hasan/)

<br/>

*If GigSphere was useful to you, please consider giving it a ⭐ — it means a lot!*

</div>

---

<div align="center">

Made with ❤️ and ☕ by **Tanbir Hasan**

*GigSphere — Where great talent meets great work.*

</div>