import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("FirebaseKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://verification-portal-dfb9d-default-rtdb.firebaseio.com/'
}
                              )
ref= db.reference('TestTaker')

data = {
    "230350125006":
        {
            "name":"Akash Singh",
            "course":"DBDA",
            "starting_year":2023,
            "last_login_time":"2023-08-18 00:30:34"
        },
    "230350125017":
        {
            "name":"Rishikesh Bacchav",
            "course":"DBDA",
            "starting_year":2023,
            "last_login_time":"2023-08-18 00:30:34"
        },
    "230350125022":
        {
            "name":"Dhiraj",
            "course":"DBDA",
            "starting_year":2023,
            "last_login_time":"2023-08-18 00:30:34"
        },
    "230350125034":
        {
            "name":"Kundan Patil",
            "course":"DBDA",
            "starting_year":2023,
            "last_login_time":"2023-08-18 00:30:34"
        },
    "230350125041":
        {
            "name":"Manoj Gaikwad",
            "course":"DBDA",
            "starting_year":2023,
            "last_login_time":"2023-08-18 00:30:34"
        },
    "230350125062":
        {
            "name":"Rakesh Singh",
            "course":"DBDA",
            "starting_year":2023,
            "last_login_time":"2023-08-18 00:30:34"
        },
    "230350125054":
        {
            "name":"Prabhakar Gautam",
            "course":"DBDA",
            "starting_year":2023,
            "last_login_time":"2023-08-18 00:30:34"
        },
    "230350125071":
        {
            "name":"Sahil Rahate",
            "course":"DBDA",
            "starting_year":2023,
            "last_login_time":"2023-08-18 00:30:34"
        },
    "230350125056":
        {
            "name":"Pranav Sathe",
            "course":"DBDA",
            "starting_year":2023,
            "last_login_time":"2023-08-18 00:30:34"
        },
    "230350125029":
        {
            "name":"Yogesh Khalane",
            "course":"DBDA",
            "starting_year":2023,
            "last_login_time":"2023-08-18 00:30:34"
        },
    "230350125060":
        {
            "name":"Rahul Shivansi",
            "course":"DBDA",
            "starting_year":2023,
            "last_login_time":"2023-08-18 00:30:34"
        },
    "230350125060":
        {
            "name":"Aishwary Pratap",
            "course":"DBDA",
            "starting_year":2023,
            "last_login_time":"2023-08-18 00:30:34"
        },
    "230350125065":
        {
            "name":"Rohan Borse",
            "course":"DBDA",
            "starting_year":2023,
            "last_login_time":"2023-08-18 00:30:34"
        }



}

for key, value in data.items():
    ref.child(key).set(value)