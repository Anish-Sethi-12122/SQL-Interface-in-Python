#THE SQL INTERFACE IN PYTHON
import mysql.connector as mysql
from tabulate import tabulate
import pwinput

def Print(message, color_key="WHITE", style="", type=True):
    import time
    from rich.console import Console
    from rich.text import Text
    COLOR_MAP={"CYAN": "bright_cyan","YELLOW": "bright_yellow","RED": "bright_red","GREEN": "bright_green","WHITE": "white","MAGENTA": "bright_magenta"}
    console=Console()
    color=COLOR_MAP.get(color_key, "white")
    styled_text=Text("", style=f"{style} {color}")
    delay = 0.02069 if type else 0
    for char in message:
        styled_text.append(char)
        console.print(char, style=f"{style} {color}", end="")
        time.sleep(delay)

Pas=pwinput.pwinput(prompt='Enter password: ', mask='*')
from mysql.connector import Error

try:
    con = mysql.connector.connect(host="localhost", user="root", passwd=Pas)
    cur = con.cursor()
    Print("Login successful","GREEN")
except Error as err:
    Print("❌ Login failed: Incorrect password entered", "RED", "bold")
    print(err.msg)
    exit()
        
def execute_select(query):
    cur.execute(query)
    result=cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    print(tabulate(result, headers=columns, tablefmt='fancy_grid'))

def execute_change(query):
    cur.execute(query)
    print("Query ok")
    con.commit()

def execute(query):
    cur.execute(query)
    print("Query ok")

def main():
    while True:
        query=input()
        if query.lower().strip()=="exit;":
            break
        elif query.lower().strip().startswith("show") or query.lower().strip().startswith("select") or query.lower().strip().startswith("desc"):
            try:
                execute_select(query)
            except Error as err:
                print(err.msg)
        elif query.lower().strip().startswith("update") or query.lower().strip().startswith("delete") or query.lower().strip().startswith("insert"):
            try:
                execute_change(query)
            except Error as err:
                print(err.msg)
        else:
            try:
                execute(query)
            except Error as err:
                print(err.msg)

if __name__=="__main__":
    main()
