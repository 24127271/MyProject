document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const isOpen = urlParams.get('open');
    const overlay = document.getElementById('envelope-overlay');
    const content = document.getElementById('main-content');

    // Chỉ ẩn thiệp nếu URL có ?open=true
    if (isOpen === 'true') {
        if (overlay) overlay.style.display = 'none';
        if (content) content.style.display = 'block';
    } else {
        // Mặc định luôn hiện thiệp khi vào trang chủ bình thường (/)
        if (overlay) {
            overlay.style.display = 'flex';
            overlay.classList.remove('fade-out'); // Xóa class mờ nếu có
        }
        if (content) content.style.display = 'none';
    }
});

// Hàm để bạn bấm vào nút mở thiệp thủ công
function openEnvelope() {
    const overlay = document.getElementById('envelope-overlay');
    const content = document.getElementById('main-content');
    
    if (overlay) {
        overlay.classList.add('fade-out');
        setTimeout(() => {
            overlay.style.display = 'none';
            if (content) content.style.display = 'block';
        }, 800);
    }
}

function viewHD(src) {
    const modal = document.getElementById('avatar-modal');
    const imgHD = document.getElementById('img-hd');
    
    imgHD.src = src; // Gán nguồn ảnh
    modal.style.display = 'flex'; // Hiển thị khung
}