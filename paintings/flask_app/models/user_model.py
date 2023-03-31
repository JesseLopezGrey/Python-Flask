from pprint import pprint
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash
from flask_app.models import painting_model
import re  # regular expression REGEX

DATABASE = 'redbelt_schema'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.paintings = []

    def __repr__(self):
        return f'<User: {self.first_name}>'

    @staticmethod
    def validate_registration(form):
        is_valid = True
        if len(form['first_name']) < 2:
            flash('First_name must be at least two characters', 'first_name')
            is_valid = False
        if len(form['last_name']) < 2:
            flash('First_name must be at least two characters', 'first_name')
            is_valid = False
        if not EMAIL_REGEX.match(form['email']):
            flash('Please enter a valid email', 'email')
            is_valid = False
        if len(form['password']) < 8:
            flash('Password must be at least eight characters', 'password')
            is_valid = False
        else:
            if form['password'] != form['confirm_password']:
                flash('Passwords must match', 'confirm_password')
                is_valid = False
        return is_valid

    @staticmethod
    def validate_login(form):
        is_valid = True
        if not EMAIL_REGEX.match(form['email']):
            flash('Please enter a valid email', 'log_email')
            is_valid = False
        if len(form['password']) < 8:
            flash('Password must be at least eight characters', 'log_password')
            is_valid = False
        return is_valid

    @classmethod
    def find_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) > 0:
            return User(results[0])
        return None

    @classmethod
    def find_by_id(cls, data):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) > 0:
            return User(results[0])
        return None

    @classmethod
    def find_by_id_with_paintings(cls, data):
        query = 'SELECT * FROM users JOIN paintings ON users.id = paintings.creator_id WHERE users.id = %(id)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        pprint(results)
        if len(results) > 0:
            user = User(results[0])

            for result in results:
                painting_data = {
                    'id': result['paintings.id'],
                    'title': result['title'],
                    'description': result['description'],
                    'price': result['price'],
                    'creator_id': result['creator_id'],
                    'created_at': result['paintings.created_at'],
                    'updated_at': result['paintings.updated_at'],
                    'creator': user
                }
                painting = painting_model.Painting(painting_data)
                user.paintings.append(painting)
        return user

    @classmethod
    def save(cls, data):
        query = 'INSERT into users (first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s, %(email)s, %(password)s);'
        user_id = connectToMySQL(DATABASE).query_db(query, data)
        return user_id
