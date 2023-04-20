from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash

DATABASE = "Users_Recipes"

class Recipe:
    
    def __init__(self, data:dict) -> None:
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_30 = data['under_30']
        self.updated_at = data['updated_at'] 
        self.created_at = data['created_at'] 
        self.user_id = data['user_id'] 
        self.user = data['first_name']
        
        
        
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes JOIN users ON users.id = recipes.user_id;"
        results = connectToMySQL(DATABASE).query_db(query)
        recipes = []
        for item in results:
            recipes.append(cls(item))
        return recipes
    
    @classmethod
    def get_recipe(cls, id):
        query = "SELECT * FROM recipes JOIN users ON users.id = recipes.user_id WHERE recipes.id = %(id)s;"
        data = {'id': id}
        result = connectToMySQL(DATABASE).query_db(query, data)
        recipe = Recipe(result[0])
        return recipe
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes (name, description,instructions, date_made, under_30, user_id) VALUES (%(name)s, %(description)s,%(instructions)s, %(date_made)s, %(under_30)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_recipe(cls, id):
        query = "SELECT * FROM recipes JOIN users ON users.id = recipes.user_id WHERE recipes.id = %(id)s;"
        data = {'id': id}
        result = connectToMySQL(DATABASE).query_db(query, data)
        recipe = Recipe(result[0])
        return recipe
    
    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, date_made=%(date_made)s, under_30=%(under_30)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    
    @classmethod
    def delete(cls, id):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        data = {'id':id}
        return connectToMySQL(DATABASE).query_db(query, data)
    
    
    @staticmethod
    def validate_recipe(recipe:dict):
        is_valid = True
        if len(recipe['name']) < 3:
            flash("name must be at least 3 chars")
            is_valid = False
        if len(recipe['description']) < 3:
            flash("description must be present")
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash("instructions must be present")
            is_valid = False
        return is_valid
    
    