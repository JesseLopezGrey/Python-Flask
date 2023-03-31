from pprint import pprint
from flask_app import app, render_template, redirect, request, session
from flask_app.models.painting_model import Painting
from flask_app.models.user_model import User

# display all paintings


@app.get('/paintings')
def all_paintings():
    if not 'user_id' in session:
        return redirect('/users/login_reg')
    paintings = Painting.find_all_with_creators()
    print(f'**** FOUND - ALL PAINTINGS: ****')
    pprint(paintings)
    data = {
        'id': session['user_id']
    }
    user = User.find_by_id(data)
    return render_template('all_paintings.html', paintings=paintings, user=user)

# display one painting by id


@app.get('/paintings/<int:painting_id>')
def one_painting(painting_id):
    if not 'user_id' in session:
        return redirect('/users/login_reg')
    data = {
        'id': painting_id
    }
    painting = Painting.find_by_id_with_creator(data)
    print(f'**** FOUND - PAINTING ID: {painting.id} ****')
    return render_template('one_painting.html', painting=painting)

# display form to create an painting


@app.get('/paintings/new')
def new_painting():
    if not 'user_id' in session:
        return redirect('/users/login_reg')
    return render_template('new_painting.html')

# process form and create an painting


@app.post('/paintings')
def create_painting():
    if not Painting.validate_painting_form(request.form):
        return redirect('/paintings/new')
    painting_id = Painting.save(request.form)
    print(f'**** CREATED - PAINTING ID: {painting_id} ****')
    return redirect('/paintings')

# display form to edit an painting by id


@app.get('/paintings/<int:painting_id>/edit')
def edit_painting(painting_id):
    if not 'user_id' in session:
        return redirect('/users/login_reg')
    data = {
        'id': painting_id
    }
    painting = Painting.find_by_id_with_creator(data)
    print(f'**** FOUND - PAINTING ID: {painting.id} ****')
    return render_template('edit_painting.html', painting=painting)

# process form and update an painting by id


@app.post('/paintings/<int:painting_id>/update')
def update_painting(painting_id):
    Painting.find_by_id_and_update(request.form)
    print(f'**** UPDATED - PAINTING ID: {painting_id} ****')
    return redirect(f'/paintings/{painting_id}')

# delete one painting by id


@app.get('/paintings/<int:painting_id>/delete')
def delete_painting(painting_id):
    if not 'user_id' in session:
        return redirect('/users/login_reg')
    data = {
        'id': painting_id
    }
    Painting.find_by_id_and_delete(data)
    print(f'**** DELETED - PAINTING ID: {painting_id} ****')
    return redirect('/paintings')
