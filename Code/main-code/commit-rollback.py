from enum import Enum
import uuid

# Skeleton for commit and roll-back exercise    

# *** Your Code goes Here ***

# enum for account type
class AccountType(Enum):
    CHECKING = 'c'
    SAVINGS = 's'

class Table(Enum):
    ACCOUNT = 'account'
    ACCOUNT_BALANCE = 'account_balance'
    CUSTOMER = 'customer'
    TRANSACTION = 'transaction'

accounts = []
account_balance = []
customers = []
transaction = []

# read the csv files
def read_csv_file():
    # read the csv files from  the ../../Data-Assignment-1 folder
    # and return the data for each file as a list of lists
    # where each list is a row in the csv file
    account = []
    account_balance = []
    customer = []
    transaction = []

    # read the accounts.csv file
    with open('Data-Assignment-1\\csv\\account.csv', 'r') as f:
        for line in f:
            account.append(line.strip().split(','))
    # read the account_balance.csv file
    with open('Data-Assignment-1\\csv\\account-balance.csv', 'r') as f:
        for line in f:
            account_balance.append(line.strip().split(','))
    # read the customer.csv file
    with open('Data-Assignment-1\\csv\\customer.csv', 'r') as f:
        for line in f:
            customer.append(line.strip().split(','))

    with open('Data-Assignment-1\\csv\\transactionLog.csv', 'r') as f:
        for line in f:
            transaction.append(line.strip().split(','))

    return account, account_balance, customer, transaction

def commit(transactionID):
    # commit the changes to the csv files
    # this function will be called at the end of a transaction
    # if the transaction is successful


    write_csv_file(Table.ACCOUNT)
    write_csv_file(Table.ACCOUNT_BALANCE)
    write_csv_file(Table.CUSTOMER)

    global transaction
    transaction = []
    # write the transaction to the transaction log file that the transaction was successful
    with open('Data-Assignment-1\\csv\\transactionLog.csv', 'r') as f:
        for line in f:
            transaction.append(line.strip().split(','))

    for row in transaction:
        if row[0] == transactionID:
            row[6] = 'complete'
                
    write_csv_file(Table.TRANSACTION)
    
def rollback(transactionID):
    # rollback the changes to the csv files

    global accounts
    global account_balance
    global customers

    accounts, account_balance, customers, trans = read_csv_file() # resets the tables to the original values

    global transaction
    transaction = []
    # write the transaction to the transaction log file that the transaction was successful
    with open('Data-Assignment-1\\csv\\transactionLog.csv', 'r') as f:
        for line in f:
            transaction.append(line.strip().split(','))


    for row in transaction:
        if row[0] == transactionID:
            row[6] = 'rolled back'
            print("\n\nrolling back transaction: " + transactionID)
            print("table: " + row[1])
            print("account: " + row[2])
            print("Undoing transaction that set the value from: " + row[5] + " to: " + row[4])
            print("Value is now set to " + row[4] + "\n\n")

 
    write_csv_file(Table.TRANSACTION)





def write_csv_file(table: Table):
   # write the list of lists back to the csv files

    if table == Table.ACCOUNT:
        global accounts
        with open('Data-Assignment-1\\csv\\account.csv', 'w') as f:
            for line in accounts:
                f.write(','.join(line))
                f.write('\n')
    if table == Table.ACCOUNT_BALANCE:
        global account_balance
        with open('Data-Assignment-1\\csv\\account-balance.csv', 'w') as f:
            for line in account_balance:
                f.write(','.join(line))
                f.write('\n')
    if table == Table.CUSTOMER:
        global customers
        with open('Data-Assignment-1\\csv\\customer.csv', 'w') as f:
            for line in customers:
                f.write(','.join(line))
                f.write('\n')
    if table == Table.TRANSACTION:
        global transaction

        with open('Data-Assignment-1\\csv\\transactionLog.csv', 'w') as f:
            for line in transaction:
                f.write(','.join(line))
                f.write('\n')



def updateTable(transID, table: Table,  id, column, value):
    # get the name of the variable that is passed in as the table
    # this will be used to write the table name to the transaction log
    data = None
    tableName = table.name


    if table == Table.ACCOUNT:
        global accounts
        data = accounts
    elif table == Table.ACCOUNT_BALANCE:
        global account_balance
        data = account_balance
    elif table == Table.CUSTOMER:
        global customers
        data = customers



    #get the original value of the cell where id is a string
    oldValue = None
    for row in data:
        if row[0] == id:
            oldValue = row[column]
            row[column] = value 
        
    global transaction
    transaction.append([str(transID), tableName, str(id), str(column), str(oldValue), str(value), 'incomplete'])
    write_csv_file(Table.TRANSACTION)



def startTransaction():
    # create a UUID for the transaction
    # return the UUID
    transID = str(uuid.uuid4())
    return transID
    
    
#create a function to widthdrawl money from an account. the function should take the account id and the amount to withdrawl, and an enum for the type of account (checking or savings)
def withdrawl(transID, accountID, amount, accountType: AccountType):
    old_accounts, old_account_balance, old_customers, trans = read_csv_file()
    global account_balance

    if (amount < 0):
        raise Exception("Invalid Amount")

    accountNum = None
    #find the account in the account list
    for account in old_accounts:
        if account[0] == accountID:
            if (accountType == AccountType.CHECKING):
                accountNum = account[1]
            elif (accountType == AccountType.SAVINGS):
                accountNum = account[2]
            else: 
                raise Exception("Invalid Account Type")

    #find the account balance in the account balance list
    for account in old_account_balance:
        if account[0] == accountNum:
            if (int(account[1]) - amount < 0):
                raise Exception("Insufficient Funds")
            else:
                # account[1] = str(int(account[1]) - amount)
                updateTable(transID, Table.ACCOUNT_BALANCE, accountNum, 1, str(int(account[1]) - amount))
                return 1


def deposit(transID, accountID, amount, accountType: AccountType):
    global account_balance, accounts

    if (amount < 0):
        raise Exception("Invalid Amount")
    accountNum = None
    #find the account in the account list
    for account in accounts:
        if account[0] == accountID:
            if (accountType == AccountType.CHECKING):
                accountNum = account[1]
            elif (accountType == AccountType.SAVINGS):
                accountNum = account[2]
            else: 
                raise Exception("Invalid Account Type")

    #find the account balance in the account balance list
    for account in account_balance:
        if account[0] == accountNum:
            # account[1] = str(int(account[1]) + amount)
            updateTable(transID, Table.ACCOUNT_BALANCE, accountNum, 1, str(int(account[1]) + amount))
            return 1

def getAccountNumber(fName, lName):
    global customers
    for customer in customers:
        if customer[2] == fName and customer[1] == lName:
            return customer[0]


# Your main program
def main():

    global accounts, account_balance, customers, transaction
    accounts, account_balance, customers, transaction = read_csv_file()

    # change the account record with account_id = 3

    accountId = getAccountNumber('Emma', 'Frost')

    print("First Output:")
    print("Print Original Contents of Databases")

    print ("Account: ", accounts)
    print ("Account Balance: ", account_balance)
    print ("Customer: ", customers)  

    print("Print current status of Log Sub-system\n\n")

    # Transaction Block 1: Successful
    print("BLOCK TRANSACTION 1")
    transID = startTransaction()
    print ("Transaction ID: ", transID)

    print("Subtract money from one account.")

    withdrawl(transID, str(accountId), 100000, AccountType.CHECKING)

    print("Add money to second one")
    deposit(transID, str(accountId), 100000, AccountType.SAVINGS)
    print("COMMIT all your changes")
    commit(transID)
    print("Print Contents of Databases")

    print ("Account: ", accounts)
    print ("Account Balance: ", account_balance)
    print ("Customer: ", customers)  

    print("Print current status of Log Sub-system\n\n")

    # read the transaction log file and print the contents
    with open('Data-Assignment-1\\csv\\transactionLog.csv', 'r') as f:
        transactionLog = f.readlines()
    for line in transactionLog:
        print(line)


    # Transaction Block 1: Fails!
    print("BLOCK TRANSACTION 2")
    transID = startTransaction()
    print("Subtract money from one account (Same Transaction than before)")
    try:
        withdrawl(transID, str(accountId), 100000, AccountType.CHECKING)
        deposit(transID, str(accountId), -100000, AccountType.SAVINGS)
    except Exception as e:
        print("Failure occurs!!!!!!! ACTION REQUIRED")
        rollback(transID)
    print("Must either AUTOMATICALLY Roll-back Database to a state of equilibrium (Bonus), OR\nSTOP Operations and show: (a) Log-Status, and (b) Databases Contents.\n")
    print("Transaction failed. Rolled back to previous state.")
    print ("Account: ", accounts)
    print ("Account Balance: ", account_balance)
    print ("Customer: ", customers)  
    print("\nTransaction Log:")
    # read the transaction log file and print the contents
    with open('Data-Assignment-1\\csv\\transactionLog.csv', 'r') as f:
        transactionLog = f.readlines()
    for line in transactionLog:
        print(line)



main()



