from flask import render_template, flash, redirect, url_for, request, session
from app import app, query_db
from app.forms import IndexForm, PostForm, FriendsForm, ProfileForm, CommentsForm
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
from flask_login import login_user, login_required
from app import load_user

# this file contains all the different routes, and the logic for communicating with the database

# home page/login/registration


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = IndexForm()

    # TODO: Make queries etc their own functions in database
    if form.login.validate_on_submit():
        user = query_db(
            'SELECT * FROM Users WHERE username=?;', [form.login.username.data], one=True)
        if user is None:
            flash('Sorry, this user does not exist!')
        elif check_password_hash(user['password'], form.login.password.data) == True:
            user_login = load_user(int(user['id']))
            login_user(user_login)
            session['id'] = int(user['id'])
            session['username'] = user['username']
            return redirect(url_for('stream'))
        else:
            flash('Sorry, wrong password!')
    elif form.register.validate_on_submit():
        hash = generate_password_hash(form.register.password.data)
        query_db('INSERT INTO Users (username, first_name, last_name, password) VALUES(?, ?, ?, ?;',
                 [form.register.username.data, form.register.first_name.data, form.register.last_name.data, hash])
        return redirect(url_for('index'))
    return render_template('index.html', title='Welcome', form=form)


# content stream page
@app.route('/stream/', methods=['GET', 'POST'])
def stream():
    form = PostForm()
    curr_user_id = session['id']
    user = query_db('SELECT * FROM Users WHERE id=?;',
                    [curr_user_id], one=True)
    if form.validate_on_submit():
        if form.image.data:
            file_extension = os.path.splitext(form.image.data.filename)[1]
            filename = secure_filename(form.image.data.filename)
            if file_extension not in app.config['ALLOWED_EXTENSIONS']:
                return "File not allowed", 400
            path = os.path.join(
                app.config['UPLOAD_FOLDER'], filename)
            form.image.data.save(path)

        query_db('INSERT INTO Posts (u_id, content, image, creation_time) VALUES(?, ?, ?, ?);', [
            user['id'], form.content.data, form.image.data.filename, datetime.now()])
        return redirect(url_for('stream'))

    posts = query_db('SELECT p.*, u.*, (SELECT COUNT(*) FROM Comments WHERE p_id=p.id) AS cc FROM Posts AS p JOIN Users AS u ON u.id=p.u_id WHERE p.u_id IN (SELECT u_id FROM Friends WHERE f_id=?) OR p.u_id IN (SELECT f_id FROM Friends WHERE u_id=?) OR p.u_id=? ORDER BY p.creation_time DESC;', [
        user['id'], user['id'], user['id']])
    return render_template('stream.html', title='Stream', form=form, posts=posts)

# comment page for a given post and user.


@app.route('/comments/<int:p_id>', methods=['GET', 'POST'])
def comments(p_id):
    form = CommentsForm()
    if form.validate_on_submit():
        user = query_db(
            'SELECT * FROM Users WHERE username=?;' [session['username']], one=True)
        query_db('INSERT INTO Comments (p_id, u_id, comment, creation_time) VALUES(?, ?, ?, ?);', [
            p_id, user['id'], form.comment.data, datetime.now()])

    post = query_db('SELECT * FROM Posts WHERE id=?;', [p_id], one=True)
    all_comments = query_db('SELECT DISTINCT * FROM Comments AS c JOIN Users AS u ON c.u_id=u.id WHERE c.p_id=? ORDER BY c.creation_time DESC;',
                            [p_id])
    return render_template('comments.html', title='Comments', form=form, post=post, comments=all_comments)

# page for seeing and adding friends


@ app.route('/friends', methods=['GET', 'POST'])
def friends():
    form = FriendsForm()
    user = query_db(
        'SELECT * FROM Users WHERE username=?;', [session['username']], one=True)
    if form.validate_on_submit():
        friend = query_db(
            'SELECT * FROM Users WHERE username=?;', [form.username.data], one=True)
        if friend is None:
            flash('User does not exist')
        else:
            query_db('INSERT INTO Friends (u_id, f_id) VALUES(?, ?);',
                     [user['id'], friend['id']])

    all_friends = query_db(
        'SELECT * FROM Friends AS f JOIN Users as u ON f.f_id=u.id WHERE f.u_id=? AND f.f_id!=? ;', [user['id'], user['id']])
    return render_template('friends.html', title='Friends', friends=all_friends, form=form)

# see and edit detailed profile information of a user


@ app.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username):
    form = ProfileForm()
    if form.validate_on_submit():
        if username != session['username']:
            flash("Error: not your profile!")
        else:
            query_db('UPDATE Users SET education= ?, employment= ? , music= ?, movie= ? , nationality= ? , birthday= ? WHERE username= ? ;', [
                form.education.data, form.employment.data, form.music.data, form.movie.data, form.nationality.data, form.birthday.data, username])
            return redirect(url_for('profile', username=username))

    user = query_db(
        'SELECT * FROM Users WHERE username=?;', [username], one=True)
    return render_template('profile.html', title='profile', username=username, user=user, form=form)


app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)


@ app.after_request
def apply_caching(response):
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self' maxcdn.bootstrapcdn.com; script-src 'self' code.jquery.com cdnjs.cloudflare.com stackpath.bootstrapcdn.com; style-src 'self' maxcdn.bootstrapcdn.com stackpath.bootstrapcdn.com/"
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.set_cookie('username', 'flask', secure=True,
                        httponly=True, samesite='Lax')
    return response
