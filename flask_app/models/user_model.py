from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, request
from flask_app.models.sighting_model import Sighting


from flask_app import DATABASE, bcrypt


import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.sightings = []

    @classmethod
    def find_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results and len(results) > 0:
            found_user = cls(results[0])
            return found_user
        else:
            return False

    @classmethod
    def register(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s,%(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query,data)



    @classmethod
    def validate_login(cls, data):

        found_user = cls.find_by_email(data)

        if not found_user:
            flash("Invalid login...")
            return False
        elif not bcrypt.check_password_hash(found_user.password, data['password']):
            flash("Invalid login...")
            return False

        return found_user


    @staticmethod
    def validate(data):
        is_valid = True

# *******- validates first name -****************
        if len(data['first_name']) == 0:
            flash("Please provide a first name!")
            is_valid = False
        elif len(data["first_name"]) < 2:
            flash("User first name must be at least two characters")
            is_valid = False
        # elif not data['first_name'].isalpha():
        #     flash("First name must only contain characters")
        #     is_valid = False

# *******- validates last name -****************
        if len(data['last_name']) == 0:
            flash("Please provide a last name!")
            is_valid = False
        elif len(data["last_name"]) < 2:
            flash("User last name must be at least two characters")
            is_valid = False

# *******- validates email and password -****************
        if len(data['email']) == 0:
            flash("Please provide an email!")
            is_valid = False
        if len(data["password"]) < 8:
            flash("Password must be at least eight characters")
            is_valid = False
        if data["password"] != data["confirm_password"]:
            flash("Passwords do not match!")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!")
            is_valid = False
        if User.find_by_email(data):
            flash("Email is already registered!")
            is_valid = False

        return is_valid




    @classmethod
    def all_sightings_with_users(cls):
        query = "SELECT * FROM sightings LEFT JOIN users on sightings.user_id = users.id"
        results = connectToMySQL(DATABASE).query_db( query )
        all_sightings = []

        for row in results:
            one_sightings = S(row)

            user_data = {
                "id" : row["users.id"],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            one_sightings.owner = cls(user_data)
            all_sightings.append(one_sightings)

        return all_sightings


# *******- get_user_with_sightings holds the user and its sightings -****************
    @classmethod
    def get_user_with_sightings( cls , data ):
        query = "SELECT * FROM users LEFT JOIN sightings ON users.id = sightings.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db( query , data )

        user = cls( results[0] )
        for row in results:

            sighting_data = {
                "id" : row['id'],
                "location" : row['location'],
                "what_happened" : row['what_happened'],
                "date_seen" : row['date_seen'],
                "num_views" : row['num_views'],
                "created_at" : row['created_at'],
                "updated_at" : row['updated_at'],
                "user_id" : row['user_id']
            }
            user.sightings.append(Sighting(sighting_data))
        # print(user.sightings)
        return user
