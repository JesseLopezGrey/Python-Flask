from pprint import pprint
from flask_app import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user_model

DATABASE = 'redbelt_schema'


class Painting:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.price = data['price']
        self.creator_id = data['creator_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = data['creator']

    def __repr__(self):
        return f'<Painting: {self.title}>'

    @staticmethod
    def validate_painting_form(form):
        is_valid = True
        if len(form['title']) < 2:
            flash('Title must be at least two characters.', 'title')
            is_valid = False
        if len(form['description']) < 10:
            flash('Description must be at least two characters.', 'description')
            is_valid = False
        if len(form['price']) < 0:
            flash('Please input a price.', 'price')
            is_valid = False
        return is_valid

    # create an painting
    @classmethod
    def save(cls, data):
        query = 'INSERT INTO paintings (title, description, price, creator_id) VALUES (%(title)s, %(description)s, %(price)s, %(creator_id)s);'
        painting_id = connectToMySQL(DATABASE).query_db(query, data)
        return painting_id

    # find all paintings (no data needed)
    @classmethod
    def find_all(cls):
        query = 'SELECT * from paintings;'
        results = connectToMySQL(DATABASE).query_db(query)
        paintings = []
        for result in results:
            paintings.append(Painting(result))
        return paintings

    # find all paintings with creators (no data needed)
    @classmethod
    def find_all_with_creators(cls):
        query = 'SELECT * from paintings JOIN users ON paintings.creator_id = users.id;'
        results = connectToMySQL(DATABASE).query_db(query)
        pprint(results)
        paintings = []
        for result in results:
            user_data = {
                'id': result['creator_id']
            }
            creator = user_model.User.find_by_id(user_data)
            painting_data = {
                'id': result['id'],
                'title': result['title'],
                'description': result['description'],
                'price': result['price'],
                'creator_id': result['creator_id'],
                'created_at': result['created_at'],
                'updated_at': result['updated_at'],
                'creator': creator
            }

            painting = Painting(painting_data)
            paintings.append(painting)

        return paintings

    # find one painting by id
    @classmethod
    def find_by_id(cls, data):
        query = 'SELECT * from paintings WHERE id = %(id)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        painting = Painting(results[0])
        return painting

    # find one painting by id with creator
    @classmethod
    def find_by_id_with_creator(cls, data):
        query = 'SELECT * from paintings JOIN users ON paintings.creator_id = users.id WHERE paintings.id = %(id)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        pprint(results)
        user_data = {
            'id': results[0]['creator_id']
        }
        creator = user_model.User.find_by_id(user_data)
        painting_data = {
            'id': results[0]['id'],
            'title': results[0]['title'],
            'description': results[0]['description'],
            'price': results[0]['price'],
            'creator_id': results[0]['creator_id'],
            'created_at': results[0]['created_at'],
            'updated_at': results[0]['updated_at'],
            'creator': creator
        }
        painting = Painting(painting_data)
        return painting

    # update one painting by id
    @classmethod
    def find_by_id_and_update(cls, data):
        query = 'UPDATE paintings SET title = %(title)s, description = %(description)s, price = %(price)s, creator_id = %(creator_id)s WHERE id = %(id)s;'
        connectToMySQL(DATABASE).query_db(query, data)
        return True

    # delete one painting by id
    @classmethod
    def find_by_id_and_delete(cls, data):
        query = 'DELETE FROM paintings WHERE id = %(id)s;'
        connectToMySQL(DATABASE).query_db(query, data)
        return True
