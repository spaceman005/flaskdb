from flask import Flask, render_template, g, Blueprint, request, flash, redirect, url_for
import sqlite3
from app import login_required

bp = Blueprint('blog', __name__)



@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            connection = sqlite3.connect('user_data.db')
            cursor = connection.cursor()
            cursor.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            cursor.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')