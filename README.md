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
- **Student ID**: 231002317
- **Course**: CCCS 106
- **Section**: BSCS 3B
#
- **Name**: Janice Laceda
- **Student ID**: 231004762
- **Course**: CCCS 106
- **Section**: BSCS 3B

#
### Project Overview and Problem Statement
The Coffeestry System is a digital management application designed for coffee and pastry shop owners. Many small business owners face difficulties in managing orders, tracking products, and maintaining accurate pricing and sales records. Traditional manual methods of record-keeping are often inefficient, time-consuming, and prone to errors, making it challenging to access information quickly or make informed business decisions.

 The Coffeestry System provides a centralized digital database that securely stores important business information. It includes features for order management, allowing staff to process customer orders efficiently, and product and price management, ensuring that all menu items and prices are up-to-date. By digitizing these processes, Coffeestry helps business owners streamline operations, reduce errors, and save time, ultimately improving overall business efficiency and decision-making.

#

### Feature List & Scope Table (what’s in/out)
This is the list of all the functions that Coffeestry system have:

USER AUTHENTICATION

[/] User Login/Authentication\
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
This Coffeestry system was tested through manual functional testing that covers the user authentication across all roles, CRUD operations for the products and users, order process, workflows, payment handling, pdf receipt generations and the isolation of the multi data.

#
## Team Roles & Contribution Matrix  
| Contributor | Role / Responsibilities | Contributions / Modules |
|-------------|------------------------|------------------------|
| Jasmin Francisco (jasscs) | Product Lead / UI/UX & Accessibility Designer / Project lead/ Data model | Flet UI, main app flow, SQLite schema, Documentation and README |
| Jenny Ibarrientos (github)| Documentation  |README|
| Janice Laceda (github)| Documentation |README |



#
### Risk / Constraint Notes & Future Enhancements
**Risks / Constraints:**  
- SHA-256 Limitations  
- No session timeout
- No rate limiting
- No Input Sanitization
- SQLite Single File
- No Backup System
- No Data encryption at rest
- Limited Scability

**Future Enhancements:**  
- Implement a purpose-built password hashing
- Session Management
- Two Factor Authentication
- An automated backups
- Data Encryption
- Enhance more the features, the afunctions in the report and anlytics, some of the integrations and the UI.
- Enhance more the feautures and functions


#
### Individual Reflection (per member: 150–200 words)
- Jasmin Francisco:
As the project lead for this system, I realized that implementing a database-based application is not easy, especially when you are not skilled in programming. I am not very knowledgeable in coding, which made this project challenging for me, and even our group struggled since we all lacked experience in programming. During the development process, I had to search for references, study how Python and Flet work, and ask for help from friends, classmates, and even AI. Through this project, I gained new knowledge about Python programming and how it can be integrated with Flet to build a complete system. This project taught me the value of effort, patience, sacrifice, and time management, especially with have limited time. Despite the difficulties, this experience helps me to have small improvements in ife as a computer science student.

- Jenny Ibarrientos:
The Coffeestry system enabled me to get deep insights into the working of a structured system across the board. Through the documentation preparation, I got better acquainted with the workflow of the overall platform, how products are handled, how prices are received and how orders are processed, how data is stored and how all other features interact to provide a seamless experience both to the staff and to the customer. By explaining each module, I understood the level of importance of organization and clarity in delivering the functions of a system, particularly the one that encompasses dashboards, inventory control, and customer monitoring. Drawing up of the system also made me value how all the parts work towards the entire functioning of the system. As an illustration, the role-based access and the login provides security, the product and pricing tools are consistent, and the ordering provides effective transactions. Knowing and describing these components enabled me to gain better skills in the analysis of systems. Generally, Coffeestry made me realize the significance of documentation in the presentation of a system in a clear way and making it clear to future users, evaluators, or developers.

 - Janice Laceda:
Coffeestry System was not an easy project to work on. I was also unable to contribute fully to the project since there are certain aspects of the code and how the system operates that I could not comprehend. At least reading the README.md allowed me to have an understanding of the general purpose of the system, which is to help small coffee and pastry shops with the orders and product management.
I could not contribute much to finish the tasks, but it was a valuable experience that made me understand the significance of group work and involvement in teamwork. I also got to know that a good documentation, such as the README, can go a long way in covering the system, particularly when one is not understanding the technicalities of it.
This project made me realize that I have my tasks as a part of a team, and despite all the difficulties, I should be able to admit my limitation and learn in order to be able to play my part in the future projects.


## Acknowledgments  
- Acknowledgments: Flet framework, SQLite, and open-source inspirations.



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
```
# 
## SCREENSHOTS AND FUNCTIONS OF COFFEESTRY SYSTEM

1. Welcome Screen / Exit Page 
- Starting point of the system with quick access options.
- Verifies if the user wants to close the application 
![alt text](FINAL/source/welcomescreen.png)

2. Login Page
- Users enter their credentials to access the system securely.
![alt text](FINAL/source/loginpage.png)

3. Sign Up Page
- Used to register a new admin account 
![alt text](FINAL/source/signuppage.png)

4. About Page
- Shows a short description of what Coffeestry is all about.
![alt text](FINAL/source/aboutpage.png)
 

SUPER ADMIN UI SCREENS
1. Dashboard / Logout
- Overview of system activity and quick access to main controls.
- Sign out safely from SuperAdmin session.
![alt text](FINAL/source/superadmin.png)

2. Create Admin
- Add new admin accounts to manage system operations.
![alt text](FINAL/source/createadmin.png)

3. Manage Users
- View, edit, and delete user accounts with ease.
![alt text](FINAL/source/manageuser.png)

4. Edit User
- Update user details and roles efficiently.
![alt text](FINAL/source/edituser.png)

5. Delete User
- Remove user accounts securely and instantly.
![alt text](FINAL/source/deleteuser.png)

ADMIN UI SCREENS 
1. Admin Dashboard 
- Main control center for all administrative operations.
![alt text](FINAL/source/admin1.png)
![alt text](FINAL/source/admin2.png)

2. Products and Prices 
- Manage items, categories, and pricing in your menu.
![alt text](FINAL/source/prodprice.png)

3. Order History 
- Track All completed customer orders.
![alt text](FINAL/source/orderhistory.png)

4. My Customers 
- View and manage customer information.
![alt text](FINAL/source/mycustomer.png)

5. Customer Orders 
- Process and monitor active orders in real time.
![alt text](FINAL/source/customerorder.png)

USER/CUSTOMER UI SCREENS 
1. User Dashboard / Browse Menu
- User-friendly panel for day to day operations.
- View all available coffees and pastries.
![alt text](FINAL/source/customer.png)

3. My Cart
- Review and manage your orders before checkout.
![alt text](FINAL/source/mycart.png)

4. Order History 
- Track all your previous purchases.
![alt text](FINAL/source/orderhistory_customer.png)

