import requests
import sqlite3

#for efficicency, so we don't have to use "lies.db"
DB_NAME = "lies.db"


#LIE FUNCTION
def get_lie():
    #the url we are going to use to call the api
    url = 'https://lies-as-a-service.onrender.com/lie'
    #this is where we store our data, which we get from our api call
    response = requests.get(url)
    #we format the data we got fromm our response into a json file
    data = response.json()
    # we return the data associated with the keys "lie" and "category" from the json file
    return data["lie"], data["category"]


#TABLE
def create_table():
    #connecting to our database and storing that connection in the variable "conn"
    with sqlite3.connect(DB_NAME) as conn:
        # we create our cursor object which acts as a intermediary between the database and the python code, allowing us to run queries to the database
        cursor = conn.cursor()
        #the query in question; creating our table using the execute command from the cursor object
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS lies(
                       id NUMBER AUTO_INCREMENT PRIMARY KEY,
                       content TEXT NOT NULL,
                       category TEXT NOT NULL,
                       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                       )

""")

def store_lies(content, category=None):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        #inserting or creating rows where we input data into, in this context our data is "lie" and "category"
        cursor.execute(
            "INSERT INTO lies (content, category) VALUES (?,?)",
            (content, category)
        )

#creating the table by calling the function
create_table()

#storing each category from the json file to their respective values
lie, category = get_lie()
print(lie + "-" + category)

#inserting each corresponding value into the database
store_lies(lie, category)

