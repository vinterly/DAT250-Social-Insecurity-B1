from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FormField, TextAreaField, FileField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, EqualTo, Length, Regexp

# defines all forms in the application, these will be instantiated by the template,
# and the routes.py will read the values of the fields


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()], render_kw={
                           'placeholder': 'Username'})
    password = PasswordField('Password', validators=[InputRequired()], render_kw={
                             'placeholder': 'Password'})
    # TODO: It would be nice to have this feature implemented, probably by using cookies
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired(),
                                                       Length(min=2, max=20,
                                                              message='First name must be at least 2 characters and no longer than 20 characters.')],
                             render_kw={'placeholder': 'First Name'})
    last_name = StringField('Last Name', validators=[InputRequired(),
                                                     Length(min=2, max=35, message='Last name must be at least 2 characters and no longer than 35 characters.')],
                            render_kw={'placeholder': 'Last Name'})
    username = StringField('Username', validators=[InputRequired(),
                                                   Regexp(
                                                       regex='^[A-Za-z0-9_]*$', message='Sorry, your username can only contain letters, numbers and underscores.'),
                                                   Length(min=3, max=20,
                                                          message='Please choose a username between 3 and 20 characters')],
                           render_kw={'placeholder': 'Username'})
    password = PasswordField('Password',
                             validators=[InputRequired(), EqualTo('confirm_password', 'The passwords do not match. Please try again.'),
                                         Length(min=4, max=26, message='Please type a password that is at least 4 characters long.')],
                             render_kw={'placeholder': 'Password'})
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired()], render_kw={
                                     'placeholder': 'Confirm Password'})
    submit = SubmitField('Sign Up')


class IndexForm(FlaskForm):
    login = FormField(LoginForm)
    register = FormField(RegisterForm)


class PostForm(FlaskForm):
    content = TextAreaField('New Post', validators=[InputRequired(),
                                                    Length(max=250, message='Sorry, your post cannot be longer than 250 characters.')], render_kw={
                            'placeholder': 'What are you thinking about?'})
    image = FileField('Image')
    submit = SubmitField('Post')


class CommentsForm(FlaskForm):
    comment = TextAreaField('New Comment', validators=[InputRequired(),
                                                       Length(max=250, message='Sorry, your comment cannot be longer than 250 characters.')], render_kw={
                            'placeholder': 'What do you have to say?'})
    submit = SubmitField('Comment')


class FriendsForm(FlaskForm):
    username = StringField('Friend\'s username', validators=[InputRequired(), Length(min=3, max=20, message='The username you typed is either too short or too long.')],
                           render_kw={'placeholder': 'Username'})
    submit = SubmitField('Add Friend')


class ProfileForm(FlaskForm):
    education = StringField('Education', validators=[Length(max=35)], render_kw={
                            'placeholder': 'Highest education'})
    employment = StringField('Employment', validators=[Length(max=35)], render_kw={
                             'placeholder': 'Current employment'})
    music = StringField('Favorite song', validators=[Length(max=40)], render_kw={
                        'placeholder': 'Favorite song'})
    movie = StringField('Favorite movie', validators=[Length(max=40)], render_kw={
                        'placeholder': 'Favorite movie'})
    nationality = StringField('Nationality', validators=[Length(max=35)], render_kw={
                              'placeholder': 'Your nationality'})
    birthday = DateField('Birthday')
    submit = SubmitField('Update Profile')
