
from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import User, Notes
from werkzeug.security import generate_password_hash, check_password_hash
from __init__ import aluno,db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth',__name__)

@auth.route('/login', methods=["GET","POST"])
def login():
    if request.method =='POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Login realizado com sucesso!', category='success')
                login_user(user, remember=False)
                return redirect(url_for('views.home'))
            else:
                flash('Senha inválida!', category='error')
        else:
            flash('Usuário inválida. Por favor, se inscreva!', category='error')

    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=["GET","POST"])
def sing_up():
    if request.method =='POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email já existe!',category='error')
        
        elif len(firstName)<3:
            flash('Firstname precisa ter mais que 2 letras',category='error')
        elif password1!=password2:
            flash('Senhas precisam ser iguais', category='error')
        elif len(password1)<3 and len(password1)>0:
            flash('Senha precisa conter mais que 2 caracteres', category='error')
        elif len(password1)==0:
            flash('Preencha o campo senha', category='error')
        else:
            new_user = User(email=email,first_name = firstName, password = generate_password_hash(password1,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=False)
            flash('Conta criada com sucesso!', category='success')
            return redirect(url_for('views.home'))

    return render_template('signup.html', user=current_user)


@auth.route('/inserir', methods=['GET', 'POST'])
@login_required
def inserir():
    if request.method=='POST':
    
        school = request.form['school']
        sex = request.form['sex']
        age = request.form['age']
        adress = request.form['adress']
        famsize = request.form['famsize']
        medu = request.form['Medu']
        fedu = request.form['Fedu']
        mjob = request.form['Mjob']
        fjob = request.form['Fjob']
        reason = request.form['reason']
        guardian = request.form['guardian']
        traveltime = request.form['traveltime']
        studytime = request.form['studytime']
        G1 = request.form['G1']
        G2 = request.form['G2']
        G3 = request.form['G3']
        
        aluno.insert_one({'school': school, 'sex': sex, 'age':age, 'adress':adress, 'famsize':famsize, 
        'medu':medu, 'fedu':fedu, 'mjob':mjob, 'fjob':fjob, 'reason':reason, 'guardian':guardian, 'traveltime':traveltime,
        'studytime':studytime, 'G1':G1, 'G2':G2, 'G3':G3})
          
    all_todos = aluno.find()
    return render_template('inserir.html',user=current_user,todos=all_todos)

@auth.route('/visualizar', methods=['GET', 'POST'])
@login_required
def visualizar():
    return render_template('visualizar.html',user=current_user)
