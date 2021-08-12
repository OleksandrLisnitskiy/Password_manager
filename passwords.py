import sqlite3

connection = sqlite3.connect("passwords.db")

create = """
CREATE TABLE IF NOT EXISTS passwords(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    service VARCHAR(12),
    login VARCHAR(15),
    password VARCHAR(30)
    );
    """

select = """
SELECT service, login, password FROM passwords
"""


def query(connection, query, *args):
    cursor = connection.cursor()
    cursor.execute(query, args)
    connection.commit()


def reading(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor.fetchall()


query(connection, create)


def check(service, login):  # check if you've already signed in thise servise

    info = reading(connection, select)

    for s_l_p in info:
        if service == s_l_p[0].lower() and login == s_l_p[1]:
            return [s_l_p[1], s_l_p[2]]


# !!! Зробить опцію для вибору або додати пароль або змінити його
while True:
    choice = input("""What would you like to do?
                     1.add
                     2.find
                     3.change
                     4.exit \n""")
    if choice == '1':

        service = input("Where would you like to to registrar: ")
        login = input("Please enter your login: ")
        data = check(service, login)
        if data:
            print(f"You have already registered on this service. Your login is {data[0]}, your password is {data[1]}")
        else:

            password = input("Please enter your password here: ")

            query(connection, f"INSERT INTO passwords (service, login, password) VALUES (?, ?, ?);", service, login, password)

    elif choice == '2':
        service = input("To find out your password enter service: ")
        login = input("Enter your login: ")
        data = check(service, login)

        if data:
            print(f"Your login is {data[0]}, your password is {data[1]}")
        else:
            print("You haven't registered on this service before")
    elif choice == '3':
        new_s = input("Enter the service were you would like to change password: ")
        new_l = input("Enter the login for which you would like to change password: ")
        data = check(new_l, new_s)
        new_p = input("Enter new password: ")
        query(connection, """UPDATE passwords SET password = ? WHERE login = ? and service = ?""", new_p, new_l, new_s)
        print("Password was successfully changed!")
    elif choice == "4":
        break

