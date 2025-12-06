# FINAL PROJECT - TEAM COFFEESTRY

### COURSE: APPLICATION DEVELOPMENT AND EMERGING TECHNOLOGIES (CCCS 106)
Joint Collaboration: CS 3110 – Software Engineering (Team Process & Engineering Practices)\
Project Title: Emerging Tech Flet Framework\
Assessment Type: Project & Final Examination \
Term: AY 2025–2026 (Finals)


## Student Information
- **Name**: Jasmin Francisco
- **Student ID**: 231004627
- **Course**: CCCS 106
- **Section**: BSCS 3B

#
- **Name**: Jenny Ibarrientos
- **Student ID**: 23100
- **Course**: CCCS 106
- **Section**: BSCS 3B
#
- **Name**: Janice Laceda
- **Student ID**: 23100
- **Course**: CCCS 106
- **Section**: BSCS 3B

#
### Project Overview and Problem Statement
The Coffeestry System is a digital management application designed for coffee and pastry shop owners. Many small business owners face difficulties in managing orders, tracking products, and maintaining accurate pricing and sales records. Traditional manual methods of record-keeping are often inefficient, time-consuming, and prone to errors, making it challenging to access information quickly or make informed business decisions.

 The Coffeestry System provides a centralized digital database that securely stores important business information. It includes features for order management, allowing staff to process customer orders efficiently, and product and price management, ensuring that all menu items and prices are up-to-date. By digitizing these processes, Coffeestry helps business owners streamline operations, reduce errors, and save time, ultimately improving overall business efficiency and decision-making.

#

### Feature List & Scope Table (what’s in/out)
This is a list of all of the functions that Coffeestry system have:

USER AUTHENTICATION

[/] User Login / Authentication\
[/] Login Button\
[/] Logout Button\
[/] Sign Up (Staff)

USER & ACCESS MANAGEMENT

[/] Manage Users\
[/] Create/Manage Admin Accounts

PLATFORM OVERVIEW & ANALYTICS

[/] Dashboard (Platform Overview)\
[/] Platform Analytics

ORDER MANAGEMENT

[/] Create/Add Orders (Order Entry)\
[/] Update/Edit Orders\
[/] Delete Orders\
[/] View Order History\
[/] Generate Receipt/Order Details

PRODUCT & PRICE MANAGEMENT

[/] Product Management\
[/] Add New Products\
[/] Update Product Details\
[/] Delete Products\
[/] Price Management\
[/] Update Product Prices\
[/] View Price List

CUSTOMER & LOYALTY MANAGEMENT

[/] My Customers (Loyalty Account Creation)\
[/] Customer Orders (Loyalty Order Management)

ROLE-BASED FUNCTION BREAKDOWN

[/] SUPERADMIN

- Full System Access 
- Responsible for Platform Analytics, User Management, Admin Account Creation

[/] ADMIN
- Operational Dashboard
- Responsible for Order Management, Product/Price Management, Customer Loyalty Management

[/] CUSTOMER
- External
- Responsible for Signup, Placing Orders.


#

### Architecture Diagram (simple block diagram is fine; include Flet + data + emerging tech layer)  

![alt text](FINAL/source/diagram.png)

FLET UI LAYER\
(User Interface/Frontend)

- Login / Sign Up Interface (Customer, Admin, Superadmin)

- Admin Dashboard Interface (Making Orders, Products, Customers)

- Superadmin Dashboard Interface (Platform Overview, User/Admin Management)

- Sales Report Page (Analytics View)

(Backend / Application Logic)

-  Authentication/Authorization Module (Handles user roles and access)

- Order Processing API (Create, Update, Delete Orders, Generate Receipt)

- Product/Price Management Module (CRUD for products and prices)

- Analytics Engine (Processes data for Superadmin dashboard)



DATA LAYER\
(Database)

- Users Table (Stores credentials and roles for Superadmin, Admin, and Customers)

- Products Table (Stores Product Names, Categories, Prices)

- Orders Table (Stores Order Details, History, and Payment Status)

- Customer Loyalty Table (Manages data for loyal customers)

EMERGING TECHNOLOGY LAYER
- FLET Framework (A modern Python framework enables building
a cross-platform apps)

- SHA-256 Password Hashing ( It's a cryptographic hashing to
secure the password storage)

- PDF Generation with ReportLab ( It's a programmatic digital
receipts to a PDF)

- SQLite (A lightweight embedded database with structured
data access patterns)

- SaaS Architecture ( a role based access control that supports a
multiple businesses in a platform)

- Real-Time Data Visualization (A dynamic analytics dashboard with
 charts, status distributions for a business)


#
### Data Model (ERD or JSON schema overview)
[Users]
- PK\
-id\
-username\
-password\
-role

- FK\
-business_owner_id\
-created_at

[Products]
- PK\
-id\
-name\
-category\
-price
- FK\
-business_owner_id

[Orders]
- PK\
-id\
-customer_name

- FK\
 -customer_id\
 -business_owner_id\
 -order_type\
 -total\
 -status\
 -payment_status\
 -order_date

[Order_Items]
- PK\
-id

- FK\
-order_id\
-productname\
-category\
-price\
-quantity


ROLE HIERARCHY

SuperAdmin
- Can create/manage Business Owners
- View platform-wide analytics
- Access all data

Business Owner (can be access by owner or staff)
- Create/manage own Products
- Create/Manage Customers
- Process Orders
- View own Business Analytics

Customer
- View owner's Product only
- Place Orders
- View own Order History

#
### Emerging Tech Explanation (why chosen, how integrated, limitations)
 SHA-256 (Secure Hash Algorithm 256-bit)

- This was chosen for the easy integration in Python since this has no additional dependencies required. This is widely accepted and used for security applications since it has one-way functions and that password cannot be decrypted from the hash but only to verified. This is kind of easy to implement in this system. 
- It was integrated through creating a hash function, this was applied to all password operations. Before storing, it default the password hashed, on signup a new user password was hashed, when an owner creates account it hashed the customer passsword, when the admin updates the user a password where rehashed and then when an input password were hashed and compared against stored hash.
- The limitations is that, this does not incorporate with salting, it's a techique where a random data is appended to passwords before hashing since SHA-256 is designed to be computationally fast, which is counterproductive for password security since attackers can leverage modern GPUs to compute bilions of hashes per second during a brute-force attacks. So without the salting, attackers can easily match a precomputed hashes to common passwords and this can only perform one hashing iteration, wherein it is not enough for slowing down the attackers. SHA-256 hashes was typically produce identically when an identical password was made. This kind of works well with data integrity but it is not ideal for securing password storage.



# 
### Testing Summary (how to run, coverage notes)

#
### Team Roles & Contribution Matrix
- Jasmin Francisco: - Product Lead, Vision & Feature Prioritization, 
UI/UX & Accessibility Designer, 
Lead Developer (Flet Architecture), 
Documentation & Release Manager

- Jenny Ibarrientos -
- Janice Laceda -

#
### Risk / Constraint Notes & Future Enhancements



#
### Individual Reflection (per member: 150–200 words)
 - Jasmin Francisco
 - Jenny Ibarrientos
 - Janice Laceda


#
### Setup & Run Instructions (including dependency install and platform targets)
```bash

# Prerequisites
- Python
- Operating System
- Git

# Clone the repository
git clone https://github.com/<jasscs>Final-Project.git
cd FINAL

# Create virtual environment
python -m venv venv
source venv/bin/activate  
# On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install flet reportlab

#Run the Application
cd FINAL 
flet run main.py
