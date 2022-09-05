import cx_Oracle
from tkinter import *

# Oracle connection
cx_Oracle.init_oracle_client(
    lib_dir=r"D:\instantclient_21_3")  # Locating the Oracle instantclient in my computer
ip = 'oracle.scs.ryerson.ca'
port = 1521
SID = 'orcl'
dsn_tns = cx_Oracle.makedsn(ip, port, SID)
db = cx_Oracle.connect('z4guo', '05287654', dsn_tns)
cursor = db.cursor()

# Create original window
root = Tk()
root.title("Python Dropshipping DBMS")


def main():
    """
    GUI mainloop
    """
    def drop():
        """
        Drop all tables
        """
        cursor.execute("DROP TABLE employee CASCADE CONSTRAINTS")
        cursor.execute("DROP TABLE supplier CASCADE CONSTRAINTS")
        cursor.execute("DROP TABLE product CASCADE CONSTRAINTS")
        cursor.execute("DROP TABLE keywords CASCADE CONSTRAINTS")
        cursor.execute("DROP TABLE shipping CASCADE CONSTRAINTS")
        cursor.execute("DROP TABLE payment CASCADE CONSTRAINTS")
        cursor.execute("DROP TABLE customer CASCADE CONSTRAINTS")
        cursor.execute("DROP TABLE customer_phones CASCADE CONSTRAINTS")

        queries_label['text'] = "All Tables Dropped!"

    def create():
        """
        Create all tables
        """
        cursor.execute("""CREATE TABLE employee (
                                employee_id NUMBER(10) PRIMARY KEY,
                                employee_phone_number NUMBER(10) NOT NULL,
                                employee_name VARCHAR2(25) NOT NULL,
                                employee_email VARCHAR2(40) NOT NULL,
                                employee_birth_date DATE NOT NULL,
                                employee_address VARCHAR2(100) NOT NULL,
                                title VARCHAR2(25) NOT NULL,
                                wage NUMBER(10) NOT NULL
                                )""")
        cursor.execute("""CREATE TABLE supplier (
                                supplier_id NUMBER(10) PRIMARY KEY,
                                phone_number NUMBER(10) NOT NULL,
                                supplier_name VARCHAR2(25) NOT NULL,
                                email VARCHAR2(40) NOT NULL,
                                supplier_address VARCHAR2(255) NOT NULL,
                                primary_product VARCHAR2(25) NOT NULL
                                )""")
        cursor.execute("""CREATE TABLE product (
                              supplier_id NUMBER(10) REFERENCES supplier(supplier_id),
                              employee_id NUMBER(10) REFERENCES employee(employee_id),
                              product_id NUMBER(11) NOT NULL UNIQUE,
                              product_name VARCHAR2(25) NOT NULL,
                              description VARCHAR2(200) NOT NULL,
                              price INTEGER NOT NULL,
                              profit_margin INTEGER NOT NULL,
                              profit_percent NUMBER(5, 5) NOT NULL,
                              tax INTEGER NOT NULL,
                              discount NUMBER(2, 2),
                              quantity NUMBER NOT NULL
                                )""")
        cursor.execute("""CREATE TABLE keywords (
                                product_id NUMBER REFERENCES product(product_id),
                                keyword_description VARCHAR2(200)
                                )""")
        cursor.execute("""CREATE TABLE shipping (
                              supplier_id NUMBER(10) REFERENCES supplier(supplier_id),
                              product_id NUMBER(11) REFERENCES product(product_id),
                              order_id NUMBER(8) NOT NULL UNIQUE,
                              phone_number NUMBER(10),
                              shipping_cost NUMBER NOT NULL,
                              supplier_address VARCHAR2(255),
                              customer_address VARCHAR2(255),
                              departure_time TIMESTAMP NOT NULL,
                              arrival_time TIMESTAMP NOT NULL
                              )""")
        cursor.execute("""CREATE TABLE payment (
                                payment_id NUMBER(12) PRIMARY KEY,
                                payment_name VARCHAR2(25),
                                payment_address VARCHAR2(255),
                                phone_number NUMBER(10),
                                debitcard_number NUMBER(12),
                                debitcard_expiry VARCHAR2(5),
                                debitcard_cvv NUMBER,
                                creditcard_number NUMBER(12),
                                creditcard_expiry VARCHAR2(5),
                                creditcard_cvv NUMBER,
                                paypal_id NUMBER
                                )""")
        cursor.execute("""CREATE TABLE customer (
                              customer_id NUMBER(13) PRIMARY KEY,
                              payment_id NUMBER(12) REFERENCES payment(payment_id),
                              customer_name VARCHAR2(25) NOT NULL,
                              customer_email VARCHAR2(40) NOT NULL,
                              birth_date DATE NOT NULL,
                              customer_address VARCHAR2(255) NOT NULL
                                )""")
        cursor.execute("""CREATE TABLE customer_phones (
                              customer_id NUMBER(13) REFERENCES customer(customer_id),
                              customer_phone_number VARCHAR(200) NOT NULL
                                )""")
        queries_label['text'] = "All Tables Created!"

    def pop_dum():
        """
        Populate database with dummy data
        """
        # Insert into employee
        cursor.execute("""INSERT INTO employee VALUES (8274638275, 4379717888, 'Jane Doe', 'jane_doe@gmail.com', 
                                to_date('11/11/2000','dd/mm/yyyy'), '35 Yonge St. Toronto ON M2E5T2', 'Manager', 
                                60000)""")
        cursor.execute("""INSERT INTO employee VALUES (8274123275 ,4312317888, 'Jane Finch', 'jane_finch@gmail.com', 
                                to_date('11/10/1998','dd/mm/yyyy'), '34 Church St. Toronto ON M2E5T2', 'Processor', 
                                45000)""")
        cursor.execute("""INSERT INTO employee VALUES (8212323275, 4311237888, 'Roger Finch', 
                                'roger_finch@gmail.com', to_date('11/10/1977','dd/mm/yyyy'), 
                                '11 Finch St. Toronto ON M5r453', 'Processor', 42000)""")
        cursor.execute("""INSERT INTO employee VALUES (8214353275, 4332117888, 'Joe McGrady', 
                                'joe_mcgrady@gmail.com', to_date('04/10/1994','dd/mm/yyyy'), 
                                '66 Gerrard St. Toronto ON M2H5R2', 'Processor',39000)""")

        # Insert into supplier
        cursor.execute("""INSERT INTO supplier VALUES (1726548729, 4379774455, 'Dennis Suppliers', 
                                'denniswork@gmail.com', '35 Yonge St. Toronto ON M2E5T2', 'Pen')""")
        cursor.execute("""INSERT INTO supplier VALUES (1726548735, 4379774409, 'Gis Suppliers', 
                                'giswork@gmail.com', '100 Yonge St. Toronto ON M34RT2', 'Pen')""")
        cursor.execute("""INSERT INTO supplier VALUES (1721238729, 4371222455, 'Joe Suppliers', 'joework@gmail.com', 
                                '55 Yonge St. Toronto ON M4D5T2', 'Table')""")
        cursor.execute("""INSERT INTO supplier VALUES (1754348729, 4347774455, 'John Suppliers', 
                                'johnwork@gmail.com', '48 Wellington St. Toronto ON M2S2T2', 'Toothpaste')""")
        cursor.execute("""INSERT INTO supplier VALUES (1722223729, 4312374455, 'Tom Suppliers', 'tomwork@gmail.com', 
                                '88 Gerrard St. Toronto ON M24T2', 'Eraser')""")

        # Insert into product
        cursor.execute("""INSERT INTO product VALUES (1726548729, 8274638275, 12345678901, 'Thinker Pilot Pen', 
                                'Pilot Pens - Gel Pens', 5, 2, 0.4, 1, 0.5, 500)""")
        cursor.execute("""INSERT INTO product VALUES (1721238729, 8274123275, 12345678902, 'Joes table', 
                                'Wonderful tables', 20, 5, 0.25, 2, null, 200)""")
        cursor.execute("""INSERT INTO product VALUES (1754348729, 8212323275, 12345678903, 'God Toothpaste', 
                                'Easy toothpaste, best tooth ever', 3, 1, 0.33, 1, null, 150)""")
        cursor.execute("""INSERT INTO product VALUES (1722223729, 8214353275, 12345678904, 'Joeker Eraser', 
                                'Eraser for life', 3, 2, 0.66, 1, null, 340)""")

        # Insert into keywords
        cursor.execute("""INSERT INTO keywords VALUES (12345678901, 'pen, child, fun')""")
        cursor.execute("""INSERT INTO keywords VALUES (12345678902, 'table, everyone, Dark brown wooden table 
                                for sale')""")
        cursor.execute("""INSERT INTO keywords VALUES (12345678903, 'toothpaste, everyone, teeth-whitening 
                                and deep clean')""")
        cursor.execute("""INSERT INTO keywords VALUES (12345678904, 'eraser, child, fun')""")

        # Insert into shipping
        cursor.execute("""INSERT INTO shipping VALUES (1726548729, 12345678901, 12325678, 4379717888, 25, 
                                '35 Yonge St. Toronto ON M2E5T2', '35 Lucas St. Milton ON M73S53', 
                                TIMESTAMP '2021-06-05 22:30:00', TIMESTAMP '2021-08-05 22:00:00')""")
        cursor.execute("""INSERT INTO shipping VALUES (1721238729, 12345678902, 12343679, 6281323432, 20, 
                                '55 Yonge St. Toronto ON M4D5T2', '19 James St. Milton ON M72W53', 
                                TIMESTAMP '2021-07-05 22:00:00', TIMESTAMP '2021-09-05 22:15:00')""")
        cursor.execute("""INSERT INTO shipping VALUES (1754348729, 12345678903, 12354670, 6379365880, 10, 
                                '48 Wellington St. Toronto ON M2S2T2', '50 Charles St. Toronto ON M8I0J3', 
                                TIMESTAMP '2021-08-05 22:30:00', TIMESTAMP '2021-10-05 22:30:00')""")
        cursor.execute("""INSERT INTO shipping VALUES (1722223729, 12345678904, 12323371, 4284973671, 5, 
                                '88 Gerrard St. Toronto ON M24T2', '11 James St. Toronto ON M75C53', 
                                TIMESTAMP '2021-09-05 22:30:00', TIMESTAMP '2021-11-05 22:30:00')""")

        # Insert into payment
        cursor.execute("""INSERT INTO payment VALUES (123456789012, 'John Doe',  '20 Gerrard St. Toronto ON M5B1G2', 
                                1234567890, null, null, null, 123786789012, '05/23', 123, null)""")
        cursor.execute("""INSERT INTO payment VALUES (123456789013, 'Charlie Fish',  
                                '45 Yonge St. Toronto ON M67B3E', 1234567891, 123786781234, '08/23', 734, null, 
                                null, null, null)""")
        cursor.execute("""INSERT INTO payment VALUES (123456789014, 'James Bibber',  
                                '50 Charles St. Toronto ON M8I0J3', 1234567892, null, null, null, 123781234012, 
                                '03/28', 660, null)""")
        cursor.execute("""INSERT INTO payment VALUES (123456789015, 'Kay Lee',  '10 Gerrard St. Toronto ON M5M2G3', 
                                1234567893, 678246789012, '09/36', 520, 573920164812, '08/24', 598, null)""")

        # Insert into customer
        cursor.execute("""INSERT INTO customer VALUES (1234567890123, 123456789012, 'John Doe', 
                                'john.doe@gmail.com', to_date('04/10/1995','dd/mm/yyyy'), 
                                '20 Gerrard St. Toronto ON M5B1G2' )""")
        cursor.execute("""INSERT INTO customer VALUES (1234567890124, 123456789013, 'Charlie Fish', 
                                'charlie.fish@gmail.com', to_date('07/10/1982','dd/mm/yyyy'), 
                                '45 Yonge St. Toronto ON M67B3E' )""")
        cursor.execute("""INSERT INTO customer VALUES (1234567890125, 123456789014, 'James Bibber', 
                                'james.bib@gmail.com', to_date('03/10/1999','dd/mm/yyyy'), 
                                '50 Charles St. Toronto ON M8I0J3' )""")
        cursor.execute("""INSERT INTO customer VALUES (1234567890126, 123456789015, 'Kay Lee', 'kay.lee@gmail.com', 
                                to_date('01/10/2002','dd/mm/yyyy'), '10 Gerrard St. Toronto ON M5M2G3' )""")

        # Insert into customer_phones
        cursor.execute("""INSERT INTO customer_phones VALUES (1234567890123, '4379717888, 3281728390')""")
        cursor.execute("""INSERT INTO customer_phones VALUES (1234567890124, '7379713699, 6281323432')""")
        cursor.execute("""INSERT INTO customer_phones VALUES (1234567890125, '6379365880, 3325623412')""")
        cursor.execute("""INSERT INTO customer_phones VALUES (1234567890126, '4239717881, 4284973671')""")

        db.commit()
        queries_label['text'] = "All Dummy Data Added!"

    def insert_employee():
        """
        Create new window that inserts new entry into employee table
        """
        # Create nested submit function for employee table
        def submit_employee():
            # Insert into table
            query = ("INSERT INTO employee VALUES (" + employee_id.get() + ", " + employee_phone_number.get() + ", '" +
                     employee_name.get() + "', '" + employee_email.get() + "', " + "to_date('" +
                     employee_birth_date.get() + "','dd/mm/yyyy'), '" + employee_address.get() + "', '" + title.get() +
                     "', " + wage.get() + ")")
            cursor.execute(query)

            db.commit()

            # Clear the text boxes after submission
            employee_id.delete(0, END)
            employee_phone_number.delete(0, END)
            employee_name.delete(0, END)
            employee_email.delete(0, END)
            employee_birth_date.delete(0, END)
            employee_address.delete(0, END)
            title.delete(0, END)
            wage.delete(0, END)

            # Destroy window
            queries_label['text'] = "New Employee Entry Submitted!"
            emp.destroy()

        # Create new window
        emp = Toplevel()
        emp.title("Insert new employee entry")

        # Create text boxes
        employee_id = Entry(emp, width=30)
        employee_id.grid(row=0, column=1, padx=20)
        employee_phone_number = Entry(emp, width=30)
        employee_phone_number.grid(row=1, column=1)
        employee_name = Entry(emp, width=30)
        employee_name.grid(row=2, column=1)
        employee_email = Entry(emp, width=30)
        employee_email.grid(row=3, column=1)
        employee_birth_date = Entry(emp, width=30)
        employee_birth_date.grid(row=4, column=1)
        employee_address = Entry(emp, width=30)
        employee_address.grid(row=5, column=1)
        title = Entry(emp, width=30)
        title.grid(row=6, column=1)
        wage = Entry(emp, width=30)
        wage.grid(row=7, column=1)

        # Create labels
        employee_id_label = Label(emp, text="Employee ID")
        employee_id_label.grid(row=0, column=0)
        employee_phone_number_label = Label(emp, text="Phone Number")
        employee_phone_number_label.grid(row=1, column=0)
        employee_name_label = Label(emp, text="Employee Name")
        employee_name_label.grid(row=2, column=0)
        employee_email_label = Label(emp, text="Email")
        employee_email_label.grid(row=3, column=0)
        employee_birth_date_label = Label(emp, text="Birth Date")
        employee_birth_date_label.grid(row=4, column=0)
        employee_address_label = Label(emp, text="Address")
        employee_address_label.grid(row=5, column=0)
        title_label = Label(emp, text="Job Title")
        title_label.grid(row=6, column=0)
        wage_label = Label(emp, text="Wage")
        wage_label.grid(row=7, column=0)

        # Create the submit button
        submit_btn = Button(emp, text="Add Entry To Database", command=submit_employee)
        submit_btn.grid(row=9, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

    def insert_paymnent():
        """
        Create new window that inserts new entry into payment table
        """
        # Create nested submit function for payment table
        def submit_payment():
            # Insert into table
            query = ("INSERT INTO payment VALUES (" + payment_id.get() + ", '" + payment_name.get() + "', '" +
                     payment_address.get() + "', " + phone_number.get() + ", " + debitcard_number.get() + ", '" +
                     debitcard_expiry.get() + "', " + debitcard_cvv.get() + ", " + creditcard_number.get() + ", '" +
                     creditcard_expiry.get() + "', " + creditcard_cvv.get() + ", " + paypal_id.get() + ")")
            cursor.execute(query)

            db.commit()

            # Clear the text boxes after submission
            payment_id.delete(0, END)
            payment_name.delete(0, END)
            payment_address.delete(0, END)
            phone_number.delete(0, END)
            debitcard_number.delete(0, END)
            debitcard_expiry.delete(0, END)
            debitcard_cvv.delete(0, END)
            creditcard_number.delete(0, END)
            creditcard_expiry.delete(0, END)
            creditcard_cvv.delete(0, END)
            paypal_id.delete(0, END)

            # Destroy window
            queries_label['text'] = "New Payment Entry Submitted!"
            pay.destroy()

        # Create new window
        pay = Toplevel()
        pay.title("Insert new payment entry")

        # Create text boxes
        payment_id = Entry(pay, width=30)
        payment_id.grid(row=0, column=1, padx=20)
        payment_name = Entry(pay, width=30)
        payment_name.grid(row=1, column=1)
        payment_address = Entry(pay, width=30)
        payment_address.grid(row=2, column=1)
        phone_number = Entry(pay, width=30)
        phone_number.grid(row=3, column=1)
        debitcard_number = Entry(pay, width=30)
        debitcard_number.grid(row=4, column=1)
        debitcard_expiry = Entry(pay, width=30)
        debitcard_expiry.grid(row=5, column=1)
        debitcard_cvv = Entry(pay, width=30)
        debitcard_cvv.grid(row=6, column=1)
        creditcard_number = Entry(pay, width=30)
        creditcard_number.grid(row=7, column=1)
        creditcard_expiry = Entry(pay, width=30)
        creditcard_expiry.grid(row=8, column=1)
        creditcard_cvv = Entry(pay, width=30)
        creditcard_cvv.grid(row=9, column=1)
        paypal_id = Entry(pay, width=30)
        paypal_id.grid(row=10, column=1)

        # Create labels
        payment_id_label = Label(pay, text="Payment ID")
        payment_id_label.grid(row=0, column=0)
        payment_name_label = Label(pay, text="Payment Name")
        payment_name_label.grid(row=1, column=0)
        payment_address_label = Label(pay, text="Address")
        payment_address_label.grid(row=2, column=0)
        phone_number_label = Label(pay, text="Phone Number")
        phone_number_label.grid(row=3, column=0)
        debitcard_number_label = Label(pay, text="Debit Card Number")
        debitcard_number_label.grid(row=4, column=0)
        debitcard_expiry_label = Label(pay, text="Expiry")
        debitcard_expiry_label.grid(row=5, column=0)
        debitcard_cvv_label = Label(pay, text="CVV")
        debitcard_cvv_label.grid(row=6, column=0)
        creditcard_number_label = Label(pay, text="Credit Card Number")
        creditcard_number_label.grid(row=7, column=0)
        creditcard_expiry_label = Label(pay, text="Expiry")
        creditcard_expiry_label.grid(row=8, column=0)
        creditcard_cvv_label = Label(pay, text="CVV")
        creditcard_cvv_label.grid(row=9, column=0)
        paypal_id_label = Label(pay, text="Paypal ID")
        paypal_id_label.grid(row=10, column=0)

        # Create the submit button
        submit_btn = Button(pay, text="Add Entry To Database", command=submit_payment)
        submit_btn.grid(row=11, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

    def query_one():
        """
        To show the first query
        """
        cursor.execute("SELECT * FROM customer_phones")
        results = cursor.fetchall()
        print_results = ""
        for row in results:
            print_results += str(row) + "\n"
        queries_label['text'] = print_results

    def query_two():
        """
        To show the second query
        """
        cursor.execute("""SELECT product_name, supplier_name FROM product, supplier
                                        WHERE product.supplier_id = supplier.supplier_id
                                        ORDER BY supplier_name ASC
                                        """)
        results = cursor.fetchall()
        print_results = ""
        for row in results:
            print_results += str(row) + "\n"
        queries_label['text'] = print_results

    def query_three():
        """
        To show the third query
        """
        cursor.execute("""SELECT primary_product, COUNT(*) AS NUMBER_OF_SUPPLIERS
                                FROM supplier
                                GROUP BY primary_product
                                ORDER BY primary_product
                                """)
        results = cursor.fetchall()
        print_results = ""
        for row in results:
            print_results += str(row) + "\n"
        queries_label['text'] = print_results

    def exit_gui():
        """
        Close the window and end the connection
        """
        root.destroy()
        cursor.close()
        db.close()

    # Create all the buttons
    drop_db_btn = Button(root, text="Drop All Tables", command=drop)
    drop_db_btn.grid(row=0, column=0, padx=10, ipadx=0)
    create_db_btn = Button(root, text="Create All Tables", command=create)
    create_db_btn.grid(row=1, column=0, padx=10, ipadx=0)
    populate_dummy_btn = Button(root, text="Populate Tables With Dummy Data", command=pop_dum)
    populate_dummy_btn.grid(row=2, column=0, pady=10, padx=10, ipadx=0)
    emp_btn = Button(root, text="Add New Entry to Table employee", command=insert_employee)
    emp_btn.grid(row=4, column=0, pady=0, padx=10, ipadx=100)
    pay_btn = Button(root, text="Add New Entry to Table payment", command=insert_paymnent)
    pay_btn.grid(row=5, column=0, pady=0, padx=10, ipadx=100)
    query1_btn = Button(root, text="Customer's phone number", command=query_one)
    query1_btn.grid(row=7, column=0, pady=0, padx=10, ipadx=100)
    query2_btn = Button(root, text="Name of products sold by each supplier", command=query_two)
    query2_btn.grid(row=8, column=0, pady=0, padx=10, ipadx=100)
    query3_btn = Button(root, text="Number of suppliers with same similar product", command=query_three)
    query3_btn.grid(row=9, column=0, pady=0, padx=10, ipadx=100)
    exit_btn = Button(root, text="Exit", command=exit_gui)
    exit_btn.grid(row=10, column=0, pady=20, padx=10)

    # Create button group labels
    entry_label = Label(root, text="Add New Entries")
    entry_label.grid(row=3, column=0)
    query_label = Label(root, text="Queries")
    query_label.grid(row=6, column=0)
    queries_label = Label(root)
    queries_label.grid(row=11, column=0)

    mainloop()


# Run the gui
main()














