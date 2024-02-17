from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField
from wtforms.validators import DataRequired


class FilmForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    director = StringField('Режиссер', validators=[DataRequired()])
    genre = SelectField('Жанр', choices=[('драма', 'Драма'), ('комедия', 'Комедия'), ('фантастика', 'Фантастика')],
                        validators=[DataRequired()])
    release_date = DateField('Дата релиза', validators=[DataRequired()])
    premiere_date = DateField('Дата премьеры', validators=[DataRequired()])

