import mysql.connector as sql
import random
from prettytable import PrettyTable


mycon = sql.connect(
    host='localhost',
    user='root',
    passwd='1234',
    database='project',
    autocommit=True
)
cursor = mycon.cursor()


print('------------🏦 INFINITE WALLET BANK 🏦------------')
print('--♾️ Infinite Trust, Infinite Growth 📈--')
print('=================================================')

def choice():
    global username
    global password
    
    print('\n------👋 WELCOME TO THE BANK ONLINE PORTAL --------\n')
    print( '1.create account \n'
           '2.customer login \n'
           '3.admin panel \n'
           '4.exit')
    ent=input('enter your choice:')
    if ent=='1':
        username = input('Enter username: ').lower()
        password = input('Create password: ')
        cursor.execute('INSERT INTO login(username, password) VALUES (%s, %s)', (username, password))

        dob = input('Enter date of birth (YYYY-MM-DD): ')
        address = input('Enter address: ')
        contactno = int(input('Enter contact number: '))
        emailid = input('Enter email ID: ')
        aadhaar = int(input('Enter Aadhaar number: '))

        cursor.execute(
                'INSERT INTO accountholder(username, dob, address, contactno, emailid, aadhaar) '
                'VALUES (%s, %s, %s, %s, %s, %s)',
                (username, dob, address, contactno, emailid, aadhaar)
            )

        accnumber = random.randint(100000000, 999999999)
        acctype = input(
                "Which account do you prefer?\n"
                "🏦 Savings Account\n"
                "💼 Current Account\n"
                "📈 Fixed Deposit Account\n"
                "📆 Recurring Deposit Account\n"
                "🌍 NRI Account\n"
                "👔 Salary Account\n"
                "📊 Demat Account\n"
                "👥 Joint Account\n"
                "🧒 Minor Account\n"
                "🎓 Student Account\n"
                "Enter your choice: "
            )

        balance = 0
        cursor.execute(
                'INSERT INTO accountdetails(username, accnumber, acctype, balance) VALUES (%s, %s, %s, %s)',
                (username, accnumber, acctype, balance)
            )

        print("✅ Account created successfully!")
    elif ent=='2':
            opt = input(
                ' 1. Check Account Holder Detail 👤\n'
                ' 2. Check Account Detail 📄\n'
                ' 3. Transaction 💸\n'
                ' 4. Check Account Balance 💰\n'
                ' 5. Delete Bank Account ❌\n'
                ' 6.Money transfer \n'
                ' 7. Exit Portal 🚪\n'
                'Enter your choice: '
            )
            if opt == '1':
                username=input('enter customer name:')
                cursor.execute('SELECT * FROM accountholder where username=%s;',(username,))
                data = cursor.fetchall()
                table = PrettyTable(['Username', 'DOB', 'Address', 'Contact No', 'Email ID', 'Aadhaar'])

                found = False
                for i in data:
                    if i[0] == username:
                        table.add_row(i)
                        found = True

                if found:
                    print('\n👤 Account Holder Details:')
                    print(table)
                else:
                    print('❌ No account holder found.')

            elif opt == '2':
                username=input('enter customer name:')
                cursor.execute('SELECT * FROM accountdetails where username=%s;',(username,))
                data1 = cursor.fetchall()
                table = PrettyTable(['Username', 'Account Number', 'Account Type', 'Balance'])

                found = False
                for i in data1:
                    if i[0] == username:
                        table.add_row(i)
                        found = True

                if found:
                    print('\n📄 Account Details:')
                    print(table)
                else:
                    print('❌ No account details found.')

            elif opt == '3':
                username=input('enter customer name:')
                n = input('Do you want to deposit or withdraw? ').strip().lower()
                cursor.execute("SELECT username FROM login WHERE username=%s", (username,))
                if cursor.fetchone() is None:
                    print("❌ Error: Username does not exist in login. Please create an account first.")
                else:
                    if n == 'deposit':
                        amt = int(input('Amount to be deposited: 💰 '))
                        cursor.execute("SELECT deposits, withdrawal, balance FROM transactions WHERE username=%s", (username,))
                        row = cursor.fetchone()
                        if row is not None:
                            deposits = row[0] or 0
                            balance = row[2] or 0
                            new_deposit = deposits + amt
                            new_balance = balance + amt
                            cursor.execute("UPDATE transactions SET deposits=%s, balance=%s WHERE username=%s",
                                           (new_deposit, new_balance, username))
                        else:
                            cursor.execute(
                                "INSERT INTO transactions(username, deposits, withdrawal, balance) VALUES (%s,%s,%s,%s)",
                                (username, amt, 0, amt)
                            )
                        cursor.execute("UPDATE accountdetails SET balance=%s WHERE username=%s", (new_balance, username))
                        print("✅ Deposit successful!")

                    elif n == 'withdraw':
                        amt = int(input('Amount to withdraw: 💸 '))
                        cursor.execute("SELECT deposits, withdrawal, balance FROM transactions WHERE username=%s", (username,))
                        row = cursor.fetchone()
                        if row is not None:
                            withdrawal = row[1] or 0
                            balance = row[2] or 0
                            if balance >= amt:
                                new_withdrawal = withdrawal + amt
                                new_balance = balance - amt
                                cursor.execute("UPDATE transactions SET withdrawal=%s, balance=%s WHERE username=%s",
                                               (new_withdrawal, new_balance, username))
                                cursor.execute("UPDATE accountdetails SET balance=%s WHERE username=%s", (new_balance, username))
                                print("✅ Withdrawal successful!")
                            else:
                                print("⚠️ Insufficient balance!")
                        else:
                            print(f"❌ No transactions found for this username: {username}")

            elif opt == '4':
                username=input('enter customer name:')
                cursor.execute("SELECT username FROM login WHERE username=%s", (username,))
                if cursor.fetchone() is None:
                    print("❌ The account does not exist, please create an account first.")
                else:
                    cursor.execute("SELECT balance FROM transactions WHERE username=%s", (username,))
                    r = cursor.fetchone()
                    if r is not None:
                        print("💰 Account balance is ₹", int(r[0]))
                    else:
                        print("ℹ️ No transactions found for this account. Balance is ₹0.")

            elif opt == '5':
                username=input('enter customer name:')
                passwd = input('Enter password: ')
                cursor.execute("SELECT * FROM login WHERE username = %s", (username,))
                row = cursor.fetchone()
                if row is None:
                    print("❌ Account does not exist.")
                elif row[1] != passwd:
                    print('❌ Incorrect password.')
                else:
                    con = input('Are you sure you want to delete this account? (yes/no): ').strip().lower()
                    if con == 'yes':
                        cursor.execute("DELETE FROM transactions WHERE username = %s", (username,))
                        cursor.execute("DELETE FROM accountdetails WHERE username = %s", (username,))
                        cursor.execute("DELETE FROM accountholder WHERE username = %s", (username,))
                        cursor.execute("DELETE FROM login WHERE username = %s", (username,))
                        print("🗑️ Account deleted successfully.")
                    else:
                        print("❎ Cancelled deletion of account.")

            elif opt== '6':

                sender = int(input("Enter Sender Account Number: "))
                receiver = int(input("Enter Receiver Account Number: "))
                amount = float(input("Enter Amount to Transfer: "))
            
                
                cursor.execute("SELECT balance FROM accountdetails WHERE accnumber=%s", (sender,))
                sender_data = cursor.fetchone()
            
                if sender_data is None:
                    print("Sender account not found!")
            
                else:
                   
                    cursor.execute("SELECT balance FROM accountdetails WHERE accnumber=%s", (receiver,))
                    receiver_data = cursor.fetchone()
            
                    if receiver_data is None:
                        print("Receiver account not found!")
            
                    else:
                        sender_balance = sender_data[0]
            
                        if sender_balance < amount:
                            print("Insufficient Balance!")
            
                        else:
                            cursor.execute(
                                "UPDATE accountdetails SET balance = balance - %s WHERE accnumber=%s",
                                (amount, sender) )
            
                            cursor.execute(
                                "UPDATE accountdetails SET balance = balance + %s WHERE accnumber=%s",
                                (amount, receiver) )
                            print("Money transferred successfully!")
            
                    
                
            elif opt == '7':
                print("🚪 Exiting the portal for this user...\n")
                return False

            else:
                print("⚠️ Invalid option! Try again.")

            
            
    elif ent == '3':
        print('------WELCOME TO ADMIN PANEL------')
    
        user_id = 'infinty88'
        user_pass = 'user@2204'
    
        userid = input('Enter User ID: ')
        userpassword = input('Enter Password: ')
    
        if user_id != userid or user_pass != userpassword:
            print('❌ Invalid login credentials!')
        else:
            print('✅ LOGIN SUCCESSFUL')
    
            print('1. View All Customers')
            print('2. Search For Customer')
            print('3. Delete Customer')
    
            adm = input('Enter your choice: ')
            if adm == '1':
                cursor.execute(
                    'SELECT * FROM accountholder NATURAL JOIN accountdetails;'
                )
            
                data = cursor.fetchall()
            
                if data:
                    table = PrettyTable()
            
                    table.field_names = [
                        "Username",
                        "DOB",
                        "Address",
                        "Contact No",
                        "Email ID",
                        "Aadhaar",
                        "Account No",
                        "Account Type",
                        "Balance"
                    ]
            
                    for row in data:
                        table.add_row(row)
            
                    print('\n--- CUSTOMER DETAILS ---')
                    print(table)
            
                else:
                    print("❌ No customer records found!")
            
            elif adm == '2':
                ss = int(input("Enter customer's account number: "))
            
                cursor.execute(
                    'SELECT * FROM accountdetails WHERE accnumber=%s',
                    (ss,)
                )
            
                det = cursor.fetchone()
            
                if det:
                    table1 = PrettyTable()
            
                    table1.field_names = [
                        "Username",
                        "Account No",
                        "Account Type",
                        "Balance"
                    ]
            
                    table1.add_row(det)
            
                    print('\n----- ACCOUNT DETAILS -----')
                    print(table1)
            
                    username = det[0]
            
                    cursor.execute(
                        'SELECT * FROM accountholder WHERE username=%s',
                        (username,)
                    )
            
                    dat = cursor.fetchone()
            
                    if dat:
                        table2 = PrettyTable()
            
                        table2.field_names = [
                            "Username",
                            "DOB",
                            "Address",
                            "Contact No",
                            "Email ID",
                            "Aadhaar"
                        ]
            
                        table2.add_row(dat)
            
                        print('\n----- CUSTOMER INFORMATION -----')
                        print(table2)
            
                else:
                    print("❌ Customer not found!")
            
            elif adm == '3':
                ss = int(input("Enter customer's account number to delete: "))
            
                cursor.execute(
                    'SELECT * FROM accountdetails WHERE accnumber=%s',
                    (ss,)
                )
            
                cust = cursor.fetchone()
            
                if cust:
                    table = PrettyTable()
            
                    table.field_names = [
                        "Username",
                        "Account No",
                        "Account Type",
                        "Balance"
                    ]
            
                    table.add_row(cust)
            
                    print('\n----- CUSTOMER TO DELETE -----')
                    print(table)
            
                    confirm = input("Delete this customer? (Y/N): ")
            
                    if confirm.upper() == 'Y':
                        cursor.execute(
                            'DELETE FROM accountdetails WHERE accnumber=%s',
                            (ss,)
                        )
            
                        print("✅ Customer deleted successfully!")
            
                    else:
                        print("❌ Deletion cancelled.")
            
                else:
                    print("❌ Customer not found!")
                            
                return True


        opening = input('Do you want to open online portal? (yes/no): ').strip().lower()

        if opening == 'yes':
            while True:
                if not choice():
                        
                    break
                    ch2 = input("Do you want to access more services? (yes/no) 🔁: ").strip().lower()
                    if ch2 != 'yes':
                        print('\nTHANK YOU FOR VISITING. WE LOOK FORWARD TO HELPING YOU GROW, INFINITELY 🙏📈♾️')
                        break
                elif opening == 'no':
                    print('🚪 The online portal has been closed by the user.')
            else:
                print('⚠️ PLEASE TRY AGAIN — there was an error in opening.')
        
choice()
                    
                
