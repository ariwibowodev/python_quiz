import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime, timedelta
from . import db
from .models import User, DailyResult, Quiz, Scoreboard
from .dummy_data import reset_and_seed_db
import random

def get_weather_data():
    """Simulasi data cuaca 2 hari terakhir."""
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    
    return [
        {
            'date': today.strftime('%Y-%m-%d'),
            'condition': 'Cerah',
            'day_temp': '30°C',
            'night_temp': '24°C'
        },
        {
            'date': yesterday.strftime('%Y-%m-%d'),
            'condition': 'Hujan Ringan',
            'day_temp': '28°C',
            'night_temp': '22°C'
        }
    ]

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    weather_data = get_weather_data() 
    return render_template('index.html', weather_data=weather_data)

@bp.route('/hello')
def hello():
    return "Hello, this route running in Flask"

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user is not None:
            flash('Nama pengguna sudah terdaftar. Pilih nama lain.')
            return redirect(url_for('routes.register'))
        
        email_check = User.query.filter_by(email=email).first()
        if email_check is not None:
            flash('Email sudah terdaftar. Gunakan email lain.')
            return redirect(url_for('routes.register'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registrasi Berhasil! Anda sekarang dapat login.')
        return redirect(url_for('routes.login'))

    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user is None or not user.check_password(password):
            flash('Nama pengguna atau Password tidak valid.')
            return redirect(url_for('routes.login'))
        
        login_user(user, remember=True)
        
        next_page = request.args.get('next')
        return redirect(next_page or url_for('routes.index'))

    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Anda telah logout.')
    return redirect(url_for('routes.index'))

@bp.route('/api/daily_results', methods=['GET'])
@login_required
def api_daily_results():
    date_limit = datetime.utcnow() - timedelta(days=2)
    
    results = DailyResult.query.filter(
        DailyResult.user_id == current_user.id,
        DailyResult.date >= date_limit
    ).order_by(DailyResult.date.desc()).all()
    
    daily_data = []
    for result in results:
        daily_data.append({
            'id': result.id,
            'date': result.local_date.strftime('%Y-%m-%d %H:%M:%S'), 
            'data': result.result_data,
            'username': current_user.username
        })
        
    return jsonify({
        'status': 'success',
        'count': len(daily_data),
        'results': daily_data
    })
    
@bp.route('/api/daily_results', methods=['POST'])
@login_required
def post_daily_result():
    data = request.get_json()
    if not data or 'result_data' not in data:
        return jsonify({'status': 'error', 'message': 'Data tidak lengkap'}), 400

    new_result = DailyResult(
        result_data=data['result_data'],
        user_id=current_user.id
    )
    
    db.session.add(new_result)
    db.session.commit()
    
    return jsonify({
        'status': 'success', 
        'message': 'Hasil harian berhasil disimpan.',
        'result_id': new_result.id
    }), 201

@bp.route('/quiz', methods=['GET'])
@login_required
def start_quiz():
    user_score = Scoreboard.query.filter_by(user_id=current_user.id).first()
    if user_score and user_score.high_score > 0:
        flash(f'Anda sudah menyelesaikan kuis ini. Skor Anda: {user_score.high_score}. Kuis hanya dapat dikerjakan sekali.', 'warning')
        return redirect(url_for('routes.index'))

    questions = Quiz.query.all()
    random.shuffle(questions)
    
    if not questions:
        flash('Kuis belum tersedia.', 'danger')
        return redirect(url_for('routes.index'))

    return render_template('quiz.html', questions=questions)

@bp.route('/submit_quiz', methods=['POST'])
@login_required
def submit_quiz():
    user_score = Scoreboard.query.filter_by(user_id=current_user.id).first()
    if user_score and user_score.high_score > 0:
        flash('Anda sudah menyelesaikan kuis ini. Tidak bisa submit lagi.', 'warning')
        return redirect(url_for('routes.index'))
        
    total_score = 0
    questions = Quiz.query.all()
    
    for q in questions:
        submitted_answer = request.form.get(f'question_{q.id}') 
        
        if submitted_answer == q.correct_answer:
            total_score += 1

    if user_score is None:
        user_score = Scoreboard(user_id=current_user.id, high_score=total_score, last_quiz_date=datetime.utcnow())
        db.session.add(user_score)
    else:
        user_score.high_score = total_score
        user_score.last_quiz_date = datetime.utcnow()

    db.session.commit()
    
    flash(f'Kuis selesai! Skor Anda: {total_score} dari {len(questions)}.', 'success')
    return redirect(url_for('routes.scoreboard'))

@bp.route('/scoreboard')
def scoreboard():
    top_scores = db.session.query(Scoreboard, User)\
                       .join(User, Scoreboard.user_id == User.id)\
                       .order_by(Scoreboard.high_score.desc())\
                       .all()
                       
    weather_data = get_weather_data()
    return render_template('scoreboard.html', 
                           top_scores=top_scores,
                           weather_data=weather_data)

@bp.route('/db_reset')
def db_reset():
    is_development = os.environ.get('FLASK_ENV') == 'development'
    is_debug = current_app.config.get('DEBUG', False)
    
    if is_development or is_debug:
        try:
            from .dummy_data import reset_and_seed_db
            reset_and_seed_db()
            
            if current_user.is_authenticated:
                logout_user()
            
            flash('Database berhasil DI-RESET. Semua data telah dihapus.', 'danger')
            return redirect(url_for('routes.index'))
        except Exception as e:
            flash(f'Gagal mereset database: {e}', 'danger')
            return redirect(url_for('routes.index'))
    else:
        return "Akses Ditolak.", 403