# app/dummy_data.py

from . import db
from .models import Quiz, User, DailyResult, Scoreboard

def reset_and_seed_db():
    """Menghapus semua tabel, membuat ulang, dan memasukkan data dummy."""
    print("-> Menghapus semua tabel database...")
    db.drop_all()
    
    print("-> Membuat ulang semua tabel database...")
    db.create_all()
    
    insert_dummy_quiz_data()
    
    print("-> Database berhasil di-reset dan di-seed!")

def insert_dummy_quiz_data():
    """Memasukkan 10 pertanyaan kuis dummy jika tabel Quiz masih kosong."""
    if Quiz.query.count() == 0:
        
        quiz1 = Quiz(
            question="Library utama Python untuk pemrosesan dan manipulasi data yang efisien, sering digunakan sebelum model AI dilatih?",
            answer_a="Requests",
            answer_b="NumPy",
            answer_c="Pandas",
            answer_d="Matplotlib",
            correct_answer="C"
        )
        
        quiz2 = Quiz(
            question="Alat apa yang umumnya digunakan dalam ekosistem Python untuk menjalankan unit testing dan memastikan kualitas kode?",
            answer_a="Pylint",
            answer_b="Jupyter Notebook",
            answer_c="pytest",
            answer_d="pip",
            correct_answer="C"
        )
        
        quiz3 = Quiz(
            question="Dalam konteks Flask-SQLAlchemy, apa yang diwakili oleh istilah 'Model'?",
            answer_a="Sebuah file HTML template.",
            answer_b="Sebuah fungsi rute API.",
            answer_c="Sebuah representasi Python dari tabel database.",
            answer_d="Sebuah objek sesi pengguna.",
            correct_answer="C"
        )

        quiz4 = Quiz(
            question="Apa tujuan utama dari 'virtual environment' (venv) dalam proyek Python?",
            answer_a="Mengurangi ukuran file proyek.",
            answer_b="Mengizinkan kode berjalan di berbagai sistem operasi tanpa modifikasi.",
            answer_c="Mengisolasi dependensi proyek dari paket global Python sistem.",
            answer_d="Mempercepat waktu eksekusi skrip Python.",
            correct_answer="C"
        )
        
        quiz5 = Quiz(
            question="Library Python paling populer untuk pengembangan kecerdasan buatan (Machine Learning) yang menyediakan algoritma dasar?",
            answer_a="Requests",
            answer_b="Scikit-learn",
            answer_c="Pandas",
            answer_d="Matplotlib",
            correct_answer="B" 
        )
        
        quiz6 = Quiz(
            question="Library Python yang paling umum digunakan untuk tugas Visi Komputer, seperti pengolahan citra dan deteksi objek?",
            answer_a="NumPy",
            answer_b="Pillow",
            answer_c="OpenCV",
            answer_d="Seaborn",
            correct_answer="C"
        )
        
        quiz7 = Quiz(
            question="Singkatan NLP dalam konteks Kecerdasan Buatan dan Python adalah?",
            answer_a="Natural Language Process",
            answer_b="Natural Learning Protocol",
            answer_c="Network Layer Protocol",
            answer_d="Natural Language Processing",
            correct_answer="D"
        )
        
        quiz8 = Quiz(
            question="Dalam aplikasi Flask, apa peran utama Blueprint?",
            answer_a="Untuk menginstal paket tambahan ke proyek.",
            answer_b="Untuk menyediakan antarmuka baris perintah.",
            answer_c="Untuk mengatur sekelompok rute, *template*, dan aset statis ke dalam modul yang dapat digunakan kembali.",
            answer_d="Untuk mengamankan sesi pengguna dengan enkripsi.",
            correct_answer="C"
        )
        
        quiz9 = Quiz(
            question="Dalam Machine Learning, apa istilah untuk proses menyimpan model yang sudah dilatih (seperti model Scikit-learn) agar dapat dimuat dan digunakan kembali untuk prediksi?",
            answer_a="Data Cleansing",
            answer_b="Pickling (Serialization)",
            answer_c="Feature Scaling",
            answer_d="Model Validation",
            correct_answer="B" 
        )

        quiz10 = Quiz(
            question="Metode apa yang digunakan untuk mengonversi objek model database (misalnya, hasil query SQLAlchemy) menjadi format JSON yang dapat dikirim melalui API?",
            answer_a="Templating",
            answer_b="Serialisasi",
            answer_c="Hashing",
            answer_d="Context Processing",
            correct_answer="B"
        )
        
        db.session.add_all([quiz1, quiz2, quiz3, quiz4, quiz5, quiz6, quiz7, quiz8, quiz9, quiz10])
        db.session.commit()
        print("-> 10 data kuis dummy (termasuk AI/ML) berhasil dimasukkan.")
    else:
        print("-> Data kuis sudah ada, tidak perlu memasukkan dummy data.")