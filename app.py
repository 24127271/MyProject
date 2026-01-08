from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Cấu hình Database và Secret Key (bắt buộc để dùng thông báo flash)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'uel_graduation_2026' 

db = SQLAlchemy(app)

# 1. ĐỊNH NGHĨA MODEL LỜI CHÚC
class Wish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

# Khởi tạo database
with app.app_context():
    db.create_all()

# 2. ROUTE TRANG CHỦ (GỬI LỜI CHÚC)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        content = request.form.get('content')

        if content:  # Chỉ cần có nội dung lời chúc là cho gửi
            # NẾU TÊN TRỐNG THÌ ĐẶT LÀ "ẨN DANH"
            if not name:
                name = "Ẩn danh"
        
        if name and content:
            # Lưu vào database
            new_wish = Wish(name=name, content=content)
            db.session.add(new_wish)
            db.session.commit()
            
            # Gửi thông báo thành công
            flash('Cảm ơn bạn đã gửi lời chúc thành công! ❤️')
            
            # Sau khi gửi, tự động chuyển hướng sang trang Sổ lưu bút
            return redirect(url_for('guestbook'))
            
    return render_template('index.html')

# 3. ROUTE TRANG SỔ LƯU BÚT (XEM LỜI CHÚC)
@app.route('/guestbook')
def guestbook():
    # Lấy toàn bộ lời chúc, xếp cái mới nhất lên đầu (desc)
    all_wishes = Wish.query.order_by(Wish.id.desc()).all()
    return render_template('guestbook.html', wishes=all_wishes)

from flask import session # Nhớ thêm 'session' vào dòng import đầu file

# Đặt mật khẩu bạn muốn ở đây
ADMIN_PASSWORD = "03102004" 

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # Nếu người dùng gửi mật khẩu qua form
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['is_admin'] = True
            return redirect(url_for('admin'))
        else:
            flash('Mật khẩu không đúng!')

    # Kiểm tra xem đã đăng nhập chưa
    if not session.get('is_admin'):
        # Nếu chưa đăng nhập, hiện trang nhập mật khẩu
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

    # Nếu đã đăng nhập đúng, hiện danh sách lời chúc
    all_wishes = Wish.query.order_by(Wish.id.desc()).all()
    return render_template('admin.html', wishes=all_wishes)

# Route xử lý xóa lời chúc
@app.route('/delete/<int:id>')
def delete_wish(id):
    # Kiểm tra xem người dùng đã đăng nhập admin chưa mới cho xóa
    if not session.get('is_admin'):
        return redirect(url_for('admin'))

    wish_to_delete = Wish.query.get_or_404(id)
    try:
        db.session.delete(wish_to_delete)
        db.session.commit()
        # flash('Đã xóa lời chúc thành công!') # Mở dòng này nếu bạn muốn hiện thông báo
        return redirect(url_for('admin'))
    except Exception as e:
        print(f"Lỗi: {e}")
        return 'Có lỗi xảy ra khi xóa lời chúc này.'

# Thêm route đăng xuất để thoát chế độ admin
@app.route('/admin/logout')
def admin_logout():
    session.pop('is_admin', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)