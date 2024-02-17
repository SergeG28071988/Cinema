import os
from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from forms import FilmForm
from werkzeug.utils import secure_filename

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'secretary'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///films.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    premiere_date = db.Column(db.Date, nullable=False)


@app.route('/')
def index():
    films = Film.query.all()
    return render_template('index.html', films=films)


@app.route('/films/<int:id>')
def film_detail(id):
    film = Film.query.get(id)
    return render_template("film_detail.html", film=film)


@app.route('/add_film', methods=['GET', 'POST'])
def add_film():
    form = FilmForm()
    if form.validate_on_submit():
        try:
            film = Film(
                title=form.title.data,
                director=form.director.data,
                genre=form.genre.data,
                release_date=form.release_date.data,
                premiere_date=form.premiere_date.data,
            )
            db.session.add(film)
            db.session.commit()
            flash('Фильм добавлен успешно', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Ошибка при добавлении фильма: {str(e)}', 'error')

    return render_template('add_film.html', form=form)


@app.route('/films/<int:id>/delete')
def film_delete(id):
    film = Film.query.get_or_404(id)
    try:
        db.session.delete(film)
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'Ошибка при удалении фильма: {str(e)}', 'error')


@app.route('/films/<int:id>/update', methods=['POST', 'GET'])
def film_update(id):
    film = Film.query.get(id)
    form = FilmForm(obj=film)
    if form.validate_on_submit():
        try:
            film.title = form.title.data
            film.director = form.director.data
            film.genre = form.genre.data
            film.release_date = form.release_date.data
            film.premiere_date = form.premiere_date.data

            db.session.commit()
            flash('Фильм обновлен успешно', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Ошибка при обновлении фильма: {str(e)}', 'error')

    return render_template('film_update.html', form=form, film=film)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
