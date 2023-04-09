from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import user_model
from flask import flash

class Sighting:
    def __init__(self, data):
        self.id = data['id']
        self.location = data['location']
        self.what_happened = data['what_happened']
        self.date_seen = data['date_seen']
        self.num_views = data['num_views']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

# *******- selects all sightings and shows in dashboard -****************
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM sightings;"
        results = connectToMySQL(DATABASE).query_db(query)
        sightings = []
        for r in results:
            print(r)
            sightings.append(cls(r))
        return sightings

# *******- creates/inserts one sighting -****************
    @classmethod
    def save(cls, data):
        query = "INSERT INTO sightings (location, what_happened, date_seen, num_views, user_id) VALUES (%(location)s, %(what_happened)s, %(date_seen)s,%(num_views)s,%(user_id)s);"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

# *******- gets the one sighting from the one user -****************
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM sightings left join users on sightings.user_id = users.id where sightings.id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        one_sight = cls(result[0])

        user_data = {
                "id" : result[0]["users.id"],
                "first_name": result[0]['first_name'],
                "last_name": result[0]['last_name'],
                "email": result[0]['email'],
                "password": result[0]['password'],
                "created_at": result[0]['users.created_at'],
                "updated_at": result[0]['users.updated_at']
        }

        one_sight.owner = user_model.User(user_data)
        return one_sight

# *******- Updates/edits the sighting  -****************
    @classmethod
    def update(cls, data):
        query = "UPDATE sightings SET location=%(location)s, what_happened = %(what_happened)s, date_seen = %(date_seen)s, num_views = %(num_views)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

# *******- deletes the sighting -****************
    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM sightings WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

# *******- allows the sighting selected to be displayed -****************   
    @classmethod
    def get_sighting_by_id(cls, data):
        query = "SELECT * FROM sightings WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validates_sighting_creation_updates(data):
        is_valid = True
# *******- validates Sighting location -****************
        if len(data['location']) == 0:
            flash("Please provide a Sighting location!")
            is_valid = False
        elif len(data["location"]) < 3:
            flash("Location name must be at least three characters")
            is_valid = False

# *******- validates sighting description -****************
        if len(data['what_happened']) == 0:
            flash("Please provide a description of what happened!")
            is_valid = False
        elif len(data["what_happened"]) < 3:
            flash("Description of what happened must be at least three characters")
            is_valid = False

# *******- validates sighting date that was seen -****************
        if  not data['date_seen']:
            flash("Date required!")
            is_valid = False

# *******- validates number of views -****************
        if  not data['num_views']:
            flash("Views required!")
            is_valid = False
        elif len(data["num_views"]) < 1:
            flash("Number of sasquatches must be at least 1")
            is_valid = False

        return is_valid