# FINAL PROJECT

##### COURSE: APPLICATION DEVELOPMENT AND EMERGING TECHNOLOGIES (CCCS 106)
Joint Collaboration: CS 3110 – Software Engineering (Team Process & Engineering Practices)\
Project Title: Emerging Tech Flet Framework\
Assessment Type: Project & Final Examination \
Term: AY 2025–2026 (Finals)


## Student Information
- **Name**: Jasmin Francisco
- **Student ID**: 231004627
- **Course**: CCCS 106
- **Section**: BSCS 3B

### Project Overview and Problem Statement
The Coffeestry System is a digital management application designed for coffee and pastry shop owners. Many small business owners face difficulties in managing orders, tracking products, and maintaining accurate pricing and sales records. Traditional manual methods of record-keeping are often inefficient, time-consuming, and prone to errors, making it challenging to access information quickly or make informed business decisions.

 The Coffeestry System provides a centralized digital database that securely stores important business information. It includes features for order management, allowing staff to process customer orders efficiently, and product and price management, ensuring that all menu items and prices are up-to-date. By digitizing these processes, Coffeestry helps business owners streamline operations, reduce errors, and save time, ultimately improving overall business efficiency and decision-making.


### Feature List & Scope Table (what’s in/out)
This is a list of all of the functions that Coffeestry system have:
- [/] User Login / Authentication
- [] Login Button
- [] Logout Button
- [] Order Management
- [] Create/Add Orders
- [] Update/Edit Orders
- [] Delete Orders
- [] View Order History
- [] Product Management
- [] Add New Products
- [] Update Product Details
- [] Delete Products
- [] Price Management
- [] Update Product Prices
- [] View Price List
- [] Customer Database
- [] Store Customer Information
- [] View Customer Records
- [] Reports
- [] Sales Report
- [] Inventory/Stock Reports
- [] 
- []
- []



### Architecture Diagram (simple block diagram is fine; include Flet + data + emerging tech layer)
FLET LAYER
(User Interface/Frontend)

- Login Screen
- Order Management Interface
- Product and Price Management
- on process to add more

DATA LAYER
(database part)

- Users Table
- Products Table
- Orders Table
- will add more

EMERGING TECHNOLOGY LAYER

- hmm will try to implement the chosen emerging

### Data Model (ERD or JSON schema overview)
[Users]
- user_id 
- username
- password
- role

[Products]
- product_id
- product_name
- category
- 

[Orders]
- order_id
- user_id
- order_date
- total_amount

[Order_Items]
- item_id
- order_id
- product_Id
- quantity
- subtotal

[Sales]
- sales_id
- order_id
- date
- amount

### Emerging Tech Explanation (why chosen, how integrated, limitations)

### Testing Summary (how to run, coverage notes)

### Team Roles & Contribution Matrix

### Risk / Constraint Notes & Future Enhancements

### Individual Reflection (per member: 150–200 words)
 


### Enhanced Features
1. **[Light/Dark Theme Toggle]**


2. **[Search History]**


## Screenshots for this task

### LIGHTMODE
![alt text](lightmode.png)

### DARKMODE
![alt text](darkmode.png)

### HISTORY
![alt text](history.png)

## Installation


 -Python 3.8 or higher
- pip package manage

### Setup & Run Instructions (including dependency install and platform targets)
```bash
# Clone the repository
git clone https://github.com/<jasscs>Final-Project.git
cd FINAL

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file .env

# Add your Op
