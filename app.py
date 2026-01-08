from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# 1. CẤU HÌNH BẮT BUỘC
app.config['SECRET_KEY'] = 'uel_graduation_2026_secret_key' # Đã mở khóa để chạy được Admin
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Xử lý link Database từ Render (đổi postgres:// thành postgresql://)
uri = os.environ.get('DATABASE_URL', 'sqlite:///database.db')
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri

db = SQLAlchemy(app)

# 2. ĐỊNH NGHĨA MODEL LỜI CHÚC
class Wish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

# Tự động tạo bảng dữ liệu ngay khi khởi động
with app.app_context():
    db.create_all()

# 3. CÁC ROUTE TRANG CHỦ & GUESTBOOK
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name') or "Ẩn danh"
        content = request.form.get('content')
        if content:
            new_wish = Wish(name=name, content=content)
            db.session.add(new_wish)
            db.session.commit()
            flash('Cảm ơn bạn đã gửi lời chúc thành công! ❤️')
            return redirect(url_for('guestbook'))
    return render_template('index.html')

@app.route('/guestbook')
def guestbook():
    all_wishes = Wish.query.order_by(Wish.id.desc()).all()
    return render_template('guestbook.html', wishes=all_wishes)

# 4. QUẢN TRỊ ADMIN
ADMIN_PASSWORD = "03102004" 

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            session['is_admin'] = True
            return redirect(url_for('admin'))
        else:
            flash('Mật khẩu không đúng!')

    if not session.get('is_admin'):
        return '''
            <div style="text-align: center; margin-top: 100px; font-family: sans-serif;">
                <h2>Trang Quản Trị</h2>
                <form method="post">
                    <input type="password" name="password" placeholder="Nhập mật khẩu admin" 
                           style="padding: 10px; border-radius: 5px; border: 1px solid #ccc;">
                    <button type="submit" style="padding: 10px 20px; background: #8b0000; color: white; border: none; border-radius: 5px; cursor: pointer;">Đăng nhập</button>
                </form>
                <p><a href="/">Quay lại trang chủ</a></p>
            </div>
        '''

    all_wishes = Wish.query.order_by(Wish.id.desc()).all()
    return render_template('admin.html', wishes=all_wishes)

@app.route('/delete/<int:id>')
def delete_wish(id):
    if not session.get('is_admin'):
        return redirect(url_for('admin'))
    wish = Wish.query.get_or_404(id)
    db.session.delete(wish)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/logout')
def admin_logout():
    session.pop('is_admin', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)