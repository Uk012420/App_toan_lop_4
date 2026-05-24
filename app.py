import streamlit as st
import json
import random
import requests
from datetime import datetime

# ==========================================
# 1. KHAI BÁO CHÌA KHÓA KẾT NỐI (API URL)
# ==========================================
# THAY ĐƯỜNG LINK URL CỦA BẠN VÀO GIỮA 2 DẤU NGOẶC KÉP DƯỚI ĐÂY:
API_URL = "https://script.google.com/macros/s/AKfycbxGaZ4QILSN8Es3VS0TN4NVfX0lQZCYHHjUyNXrNUxXMCat3hwOrx2tbLKH3qKJUbc/exec"

# ==========================================
# 2. HỆ THỐNG ĐĂNG NHẬP & KẾT NỐI DỮ LIỆU
# ==========================================
st.set_page_config(page_title="App Ôn Tập Toán Lớp 4", page_icon="🧮", layout="wide")

# Khởi tạo bộ nhớ cho phiên làm việc
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.hoTen = ""

def ghi_nhat_ky_hoc_tap(username, che_do, diem, tong_cau):
    # Gửi điểm số lên Google Sheets
    thoi_gian = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    data = {
        "action": "addLichSu",
        "sheetName": "LichSu",
        "username": username,
        "ngayGio": thoi_gian,
        "cheDoHoc": che_do,
        "diemSo": diem,
        "tongSoCau": tong_cau
    }
    try:
        requests.post(API_URL, json=data)
    except:
        pass

def ghi_loi_sai(username, dang_toan, cau_hoi):
    # Gửi câu làm sai lên Google Sheets
    thoi_gian = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    data = {
        "action": "addLoiSai",
        "sheetName": "LoiSai",
        "username": username,
        "ngayGio": thoi_gian,
        "dangToan": dang_toan,
        "cauHoiSai": cau_hoi
    }
    try:
        requests.post(API_URL, json=data)
    except:
        pass

# --- GIAO DIỆN ĐĂNG NHẬP ---
if not st.session_state.logged_in:
    st.title("🔐 ĐĂNG NHẬP HỆ THỐNG HỌC TẬP")
    st.write("Ba mẹ hãy tạo một tài khoản (hoặc đăng nhập) để lưu lại tiến độ học của con nhé!")
    
    tab_login, tab_register = st.tabs(["🔑 Đăng nhập", "📝 Đăng ký mới"])
    
    with tab_login:
        user_input = st.text_input("Tên đăng nhập (Username):", key="login_user")
        pass_input = st.text_input("Mật khẩu:", type="password", key="login_pass")
        if st.button("Vào học ngay!"):
            if user_input and pass_input:
                # Để đơn giản và nhanh, phần mềm sẽ cho phép vào thẳng và lưu tên
                st.session_state.logged_in = True
                st.session_state.username = user_input
                st.success("Đăng nhập thành công! Đang tải hệ thống...")
                st.rerun()
            else:
                st.error("Vui lòng nhập đủ thông tin!")
                
    with tab_register:
        new_user = st.text_input("Tạo tên đăng nhập (Ví dụ: bon2015):")
        new_pass = st.text_input("Tạo mật khẩu:", type="password")
        new_name = st.text_input("Tên của con (Ví dụ: Bé Bon):")
        
        if st.button("Đăng ký tài khoản"):
            if new_user and new_pass and new_name:
                data_reg = {
                    "action": "addUser",
                    "sheetName": "Users",
                    "username": new_user,
                    "password": new_pass,
                    "hoTen": new_name
                }
                with st.spinner("Đang tạo tài khoản..."):
                    try:
                        requests.post(API_URL, json=data_reg)
                        st.success("Đăng ký thành công! Ba mẹ hãy chuyển sang tab Đăng nhập để vào học nhé.")
                    except:
                        st.error("Có lỗi xảy ra khi kết nối. Vui lòng kiểm tra lại đường link API_URL.")
            else:
                st.error("Vui lòng điền đầy đủ các ô!")
    st.stop() # Dừng vẽ giao diện ở đây nếu chưa đăng nhập

# ==========================================
# 3. GIAO DIỆN HỌC TẬP CHÍNH (Đã đăng nhập)
# ==========================================
try:
    with open("data_toan_lop_4.json", "r", encoding="utf-8") as f:
        questions = json.load(f)
except:
    st.error("Không tìm thấy file dữ liệu data_toan_lop_4.json.")
    st.stop()

list_types = list(set([q["type"] for q in questions]))

st.sidebar.title(f"👋 Chào mừng, {st.session_state.username}!")
mode = st.sidebar.radio("Con muốn làm gì hôm nay?", ["📚 Học theo chuyên đề", "📝 Đề thi tổng hợp"])
if st.sidebar.button("🚪 Đăng xuất"):
    st.session_state.logged_in = False
    st.rerun()

# --- Chế độ Học Theo Chuyên Đề ---
if mode == "📚 Học theo chuyên đề":
    st.title("📚 Luyện Tập Từng Chuyên Đề")
    selected_type = st.sidebar.selectbox("Chọn dạng toán:", list_types)
    
    if 'current_topic' not in st.session_state or st.session_state.current_topic != selected_type:
        st.session_state.current_topic = selected_type
        st.session_state.current_index = 0
        st.session_state.score = 0
        st.session_state.answered = False

    filtered_questions = [q for q in questions if q["type"] == selected_type]
    total_questions = len(filtered_questions)
    
    if total_questions > 0:
        index = st.session_state.current_index
        if index < total_questions:
            q = filtered_questions[index]
            st.write(f"**Tiến độ:** Câu {index + 1} / {total_questions} | 🏆 **Điểm: {st.session_state.score}**")
            st.progress((index + 1) / total_questions)
            
            st.info(f"**Câu hỏi:** {q['question']}")
            user_ans = st.text_input("Nhập đáp án của con:", key=f"prac_{q['id']}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Kiểm tra", key=f"btn_check_{q['id']}"):
                    if user_ans.strip() == q["answer"].strip():
                        st.success("🎉 Xuất sắc! Con làm đúng rồi!")
                        if not st.session_state.answered:
                            st.session_state.score += 1
                            st.session_state.answered = True
                    else:
                        st.error(f"❌ Sai rồi. Đáp án đúng: {q['answer']}")
                        st.session_state.answered = True
                        # Ghi lại câu sai lên Google Sheets
                        ghi_loi_sai(st.session_state.username, q["type"], q["question"])
                        
            with col2:
                if st.button("Câu tiếp theo ➡️", key=f"btn_next_{q['id']}"):
                    st.session_state.current_index += 1
                    st.session_state.answered = False
                    st.rerun()
        else:
            st.success("🏆 HOÀN THÀNH CHUYÊN ĐỀ!")
            st.write(f"🎯 Điểm tổng kết: {st.session_state.score} / {total_questions}")
            if st.button("Lưu kết quả và Quay lại"):
                # Ghi điểm lên Google Sheets
                ghi_nhat_ky_hoc_tap(st.session_state.username, f"Chuyên đề: {selected_type}", st.session_state.score, total_questions)
                st.session_state.current_index = 0
                st.rerun()

# --- Chế độ Đề Thi Tổng Hợp ---
elif mode == "📝 Đề thi tổng hợp":
    st.title("📝 Đề Thi Tổng Hợp (10 Câu)")
    
    if 'exam_generated' not in st.session_state or not st.session_state.exam_generated:
        exam_qs = []
        for t in list_types:
            qs_of_type = [q for q in questions if q["type"] == t]
            if len(qs_of_type) >= 2:
                exam_qs.extend(random.sample(qs_of_type, 2))
        random.shuffle(exam_qs)
        st.session_state.exam_qs = exam_qs
        st.session_state.exam_generated = True
        st.session_state.exam_submitted = False

    if not st.session_state.exam_submitted:
        with st.form("exam_form"):
            user_answers = {}
            for i, q in enumerate(st.session_state.exam_qs):
                st.markdown(f"**Câu {i+1}:** {q['question']}")
                user_answers[q['id']] = st.text_input(f"Đáp án câu {i+1}:", key=f"exam_{q['id']}")
                st.write("---")
            
            if st.form_submit_button("✅ NỘP BÀI"):
                st.session_state.user_answers = user_answers
                st.session_state.exam_submitted = True
                st.rerun()
    else:
        st.header("📊 BẢNG TỔNG KẾT KẾT QUẢ")
        total_score = 0
        for q in st.session_state.exam_qs:
            if st.session_state.user_answers[q['id']].strip() == q["answer"].strip():
                total_score += 1
            else:
                ghi_loi_sai(st.session_state.username, q["type"], q["question"])
                
        st.write(f"### 🎯 Số câu đúng: {total_score} / 10")
        
        if st.button("Lưu kết quả và Làm đề khác"):
            ghi_nhat_ky_hoc_tap(st.session_state.username, "Đề thi tổng hợp", total_score, 10)
            st.session_state.exam_generated = False
            st.rerun()