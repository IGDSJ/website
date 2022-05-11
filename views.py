from flask import Blueprint, render_template, redirect, url_for, flash,request
from flask_login import login_required,  current_user
from __init__ import upload_folder, aluno, db
from insercao import insercao,criar_relatorio
import os
from werkzeug.utils import secure_filename
from models import Notes

views = Blueprint('views',__name__)

@views.route('/', methods = ['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note=request.form.get('note')

        if len(note) <1:
            flash('Nota muito curta, preencha alguma coisa!', category='error')
        else:
            new_note = Notes(note=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Nota adicionada!', category='success')

    return render_template('home.html',user=current_user, todos = aluno.find())

@views.route('/upload', methods = ['GET', 'POST'])
def uploadfile():
   if request.method == 'POST': # check if the method is post
      f = request.files['file'] # get the file from the files object
      f.save(os.path.join(upload_folder,secure_filename(f.filename)))
      insercao(f.filename,aluno)

      return redirect(url_for('views.home'))

@views.route('/relatorio', methods = ['GET', 'POST'])
def relatorio():
   if request.method == 'POST': # check if the method is post

    planta = request.form['planta']
    placa = request.form['placa']
    grandeza = request.form['grandeza']
    modo = request.form['modo']
    tempo = request.form['tempo']

    criar_relatorio(planta, modo, tempo, grandeza, placa)

    return redirect(url_for('views.home'))

