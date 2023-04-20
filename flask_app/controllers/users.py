from flask_app import app, render_template, redirect, request, session, flash, bcrypt
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.route('/')
def main():
    return render_template('index.html')

@app.route("/register", methods=['post'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')

    hashed_pw = bcrypt.generate_password_hash(request.form['password'])    
    print(hashed_pw)
    print(bcrypt.check_password_hash(hashed_pw, 'password'))
    
    temp_user = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': hashed_pw
    }
    user = User.save(temp_user)
    print(user)

    session['user_id'] = user
    session['first_name'] = request.form['first_name']
    session['last_name'] = request.form['last_name']

    return redirect('/')


@app.route('/login', methods=['post'])
def login():
    
    user = User.find_by_email(request.form['email'])
    if not user:
        flash("invalid credentials")
        return redirect('/')

    password_valid = bcrypt.check_password_hash(user.password, request.form['password'])
    print(password_valid)
    if not password_valid:
        flash("invalid credentials")
        return redirect('/')

    session['user_id'] = user.id
    session['first_name'] = user.first_name
    session['last_name'] = user.last_name

    return redirect('/recipes')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/recipes')
def all():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('welcome.html', recipes = Recipe.get_all())

@app.route('/recipes/new')
def new():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('/new.html', users = User.get_all)

@app.route('/create', methods=['post'])
def create():
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    Recipe.save(request.form)
    return redirect('/recipes')

@app.route('/recipes/edit/<int:id>')
def edit(id):
    return render_template('/edit.html', recipe = Recipe.get_recipe(id))

@app.route('/update', methods=['post'])
def update_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect(f"/recipes/edit/{request.form['id']}")
    Recipe.update(request.form)
    return redirect('/recipes')


@app.route('/recipes/<int:id>')
def show(id):
    if 'user_id' not in session:
        return redirect('/')
    recipe = Recipe.get_recipe(id)
    return render_template('/show.html', recipe = recipe)

@app.route('/recipes/delete/<int:id>')
def destroy(id):
    Recipe.delete(id)
    return redirect ('/recipes')

