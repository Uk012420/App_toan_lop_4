import streamlit as st
import json
import random
import requests
from datetime import datetime

# ==========================================
# 1. KHAI BÁO CHÌA KHÓA KẾT NỐI (API URL)
# ==========================================
API_URL = "https://script.google.com/macros/s/AKfycbxPsA-_TMnYhkaLhln3gUw8Z-s1JwQNinYT7Ad6I60jZqAMdw3dLmaa4_a5M6lbRUdncA/exec"

# ==========================================
# 2. HỆ THỐNG ĐĂNG NHẬP & CẤU HÌNH GIAO DIỆN
# ==========================================
st.set_page_config(page_title="App Ôn Tập Toán Lớp 4", page_icon="🧮", layout="wide")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .stDeployButton {display:none;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.hoTen = ""

def ghi_nhat_ky_hoc_tap(username, che_do, diem, tong_cau):
    thoi_gian = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    data = {"action": "addLichSu", "sheetName": "LichSu", "username": username, "ngayGio": thoi_gian, "cheDoHoc": che_do, "diemSo": diem, "tongSoCau": tong_cau}
    try: requests.post(API_URL, json=data)
    except: pass

def ghi_loi_sai(username, dang_toan, cau_hoi):
    thoi_gian = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    data = {"action": "addLoiSai", "sheetName": "LoiSai", "username": username, "ngayGio": thoi_gian, "dangToan": dang_toan, "cauHoiSai": cau_hoi}
    try: requests.post(API_URL, json=data)
    except: pass

# --- HÀM CHẤM ĐIỂM THÔNG MINH ---
def kiem_tra_dap_an(user_ans, correct_ans):
    u = str(user_ans).strip().lower()
    c = str(correct_ans).strip().lower()
    
    # Nếu giống hệt nhau thì đúng luôn
    if u == c: return True
    
    # Xử lý trường hợp có nhiều đáp án (thay thế "và", ";" thành dấu phẩy)
    u = u.replace(" và ", ",").replace(";", ",")
    c = c.replace(" và ", ",").replace(";", ",")
    
    u_list = [x.strip() for x in u.split(",") if x.strip()]
    c_list = [x.strip() for x in c.split(",") if x.strip()]
    
    # So sánh tập hợp (không phân biệt thứ tự trước sau)
    if len(c_list) > 1 and set(u_list) == set(c_list):
        return True
        
    return False

# ==========================================
# 3. LÝ THUYẾT & TẢI DỮ LIỆU
# ==========================================
THEORY_DATA = {
    "Trung bình cộng": {"khai_niem": "Số trung bình cộng san đều giá trị của tất cả các số trong một nhóm.", "phuong_phap": "Bước 1: Tính TỔNG các số.\nBước 2: Lấy TỔNG chia cho SỐ CÁC SỐ HẠNG.", "sai_lam": "Quên đóng ngoặc khi tính tổng trước khi chia. Ví dụ sai: 4 + 6 : 2. Đúng phải là: (4 + 6) : 2."},
    "Tổng và Hiệu": {"khai_niem": "Tìm hai số khi biết tổng cộng và sự chênh lệch (hiệu) của chúng.", "phuong_phap": "Số Lớn = (Tổng + Hiệu) : 2\nSố Bé = (Tổng - Hiệu) : 2\n(Mẹo: Tìm được 1 số rồi, lấy Tổng trừ đi số đó sẽ ra số còn lại rất nhanh).", "sai_lam": "Nhầm lẫn giữa Nửa chu vi và Chu vi hình chữ nhật."},
    "Dấu hiệu chia hết": {"khai_niem": "Nhận biết một số có chia hết cho 2, 3, 5, 9 hay không mà không cần đặt tính.", "phuong_phap": "- Chia hết cho 2: Số tận cùng là 0, 2, 4, 6, 8.\n- Chia hết cho 5: Số tận cùng là 0 hoặc 5.\n- Chia hết cho 3 hoặc 9: Cộng tất cả các chữ số lại, nếu tổng chia hết cho 3 hoặc 9 thì số đó chia hết.", "sai_lam": "Lấy quy tắc của 2,5 (nhìn số cuối) để áp dụng cho 3,9 (phải tính tổng các chữ số)."},
    "Phân số": {"khai_niem": "Biểu diễn phần bằng nhau của một đơn vị.", "phuong_phap": "- Cộng/Trừ: Phải quy đồng đưa về cùng mẫu số rồi mới cộng/trừ tử số, giữ nguyên mẫu.\n- Nhân: Tử nhân tử, mẫu nhân mẫu.\n- Chia: Phân số thứ nhất NHÂN với phân số thứ hai ĐẢO NGƯỢC.", "sai_lam": "Cộng/Trừ hai phân số mà lại lấy tử cộng tử, mẫu cộng mẫu."},
    "Hình học": {"khai_niem": "Tính diện tích các hình cơ bản lớp 4.", "phuong_phap": "- Hình bình hành: S = Độ dài đáy x Chiều cao (S = a x h).\n- Hình thoi: S = (Đường chéo 1 x Đường chéo 2) : 2.", "sai_lam": "Quên chia 2 khi tính diện tích hình thoi, hoặc đơn vị chưa giống nhau đã vội nhân."}
}

if not st.session_state.logged_in:
    st.title("🔐 ĐĂNG NHẬP HỆ THỐNG HỌC TẬP")
    
    tab_login, tab_register = st.tabs(["🔑 Đăng nhập", "📝 Đăng ký mới"])
    
    with tab_login:
        with st.form("login_form"):
            user_input = st.text_input("Tên đăng nhập:")
            pass_input = st.text_input("Mật khẩu:", type="password")
            if st.form_submit_button("Vào học ngay!"):
                if user_input and pass_input:
                    st.session_state.logged_in = True
                    st.session_state.username = user_input
                    st.rerun()
                else: st.error("Vui lòng nhập đủ thông tin!")
                
    with tab_register:
        with st.form("register_form"):
            new_user = st.text_input("Tạo tên đăng nhập (Ví dụ: bon2015):")
            new_pass = st.text_input("Tạo mật khẩu:", type="password")
            new_name = st.text_input("Tên của con:")
            if st.form_submit_button("Đăng ký tài khoản"):
                if new_user and new_pass and new_name:
                    data_reg = {"action": "addUser", "sheetName": "Users", "username": new_user, "password": new_pass, "hoTen": new_name}
                    with st.spinner("Đang tạo tài khoản..."):
                        try:
                            requests.post(API_URL, json=data_reg)
                            st.success("Đăng ký thành công! Chuyển sang tab Đăng nhập để vào học nhé.")
                        except: st.error("Lỗi kết nối mạng.")
                else: st.error("Vui lòng điền đủ các ô!")
    st.stop()

try:
    with open("data_toan_lop_4.json", "r", encoding="utf-8") as f:
        questions = json.load(f)
except:
    st.error("Không tìm thấy file dữ liệu data_toan_lop_4.json.")
    st.stop()

list_types = list(set([q["type"] for q in questions]))

st.sidebar.title(f"👋 Chào mừng, {st.session_state.username}!")
mode = st.sidebar.radio("Con muốn làm gì hôm nay?", ["📚 Học theo chuyên đề", "📝 Đề thi tổng hợp"])

st.sidebar.markdown("---")
if st.sidebar.button("🚪 Đăng xuất"):
    st.session_state.logged_in = False
    st.rerun()

# ==========================================
# GIAO DIỆN HỌC TẬP CHÍNH
# ==========================================

# --- CHẾ ĐỘ 1: HỌC THEO CHUYÊN ĐỀ ---
if mode == "📚 Học theo chuyên đề":
    st.title("📚 Luyện Tập Từng Chuyên Đề")
    selected_type = st.sidebar.selectbox("Chọn dạng toán:", list_types)
    
    if 'current_topic' not in st.session_state or st.session_state.current_topic != selected_type:
        st.session_state.current_topic = selected_type
        st.session_state.current_index = 0
        st.session_state.score = 0
        st.session_state.answered = False
        
        all_qs = [q for q in questions if q["type"] == selected_type]
        # Chia nhỏ: Chỉ bốc 25 câu ngẫu nhiên cho mỗi phiên luyện tập
        st.session_state.practice_qs = random.sample(all_qs, min(25, len(all_qs)))

    filtered_questions = st.session_state.practice_qs
    total_questions = len(filtered_questions)
    
    tab_lt, tab_th = st.tabs(["📖 Đọc Lý Thuyết Trước", "✍️ Thực Hành Luyện Tập"])
    
    with tab_lt:
        theory = THEORY_DATA.get(selected_type, {})
        st.header(f"Bí kíp giải toán: {selected_type}")
        st.info(f"**📌 Khái niệm:** {theory.get('khai_niem', 'Đang cập nhật...')}")
        st.success(f"**💡 Phương pháp giải:**\n{theory.get('phuong_phap', 'Đang cập nhật...')}")
        st.warning(f"**⚠️ Sai lầm hay mắc phải:** {theory.get('sai_lam', 'Đang cập nhật...')}")

    with tab_th:
        if total_questions > 0:
            index = st.session_state.current_index
            if index < total_questions:
                q = filtered_questions[index]
                st.write(f"**Tiến độ:** Câu {index + 1} / {total_questions} | 🏆 **Điểm: {st.session_state.score}**")
                st.progress((index + 1) / total_questions)
                
                with st.form(key=f"form_{q['id']}"):
                    st.info(f"**Câu hỏi:** {q['question']}")
                    user_ans = st.text_input("Nhập đáp án của con:")
                    btn_check = st.form_submit_button("Kiểm tra")
                    
                if btn_check:
                    # SỬ DỤNG HÀM CHẤM ĐIỂM THÔNG MINH
                    if kiem_tra_dap_an(user_ans, q["answer"]):
                        st.success("🎉 Xuất sắc! Con làm đúng rồi!")
                        if not st.session_state.answered:
                            st.session_state.score += 1
                            st.session_state.answered = True
                    else:
                        st.error(f"❌ Sai rồi. Đáp án chuẩn là: {q['answer']}")
                        st.session_state.answered = True
                        ghi_loi_sai(st.session_state.username, q["type"], q["question"])
                        
                if st.button("Câu tiếp theo ➡️"):
                    st.session_state.current_index += 1
                    st.session_state.answered = False
                    st.rerun()
            else:
                st.success("🏆 HOÀN THÀNH CHUYÊN ĐỀ!")
                st.write(f"🎯 Điểm tổng kết: {st.session_state.score} / {total_questions}")
                if st.button("Lưu kết quả và Luyện tập bộ câu hỏi mới"):
                    ghi_nhat_ky_hoc_tap(st.session_state.username, f"Chuyên đề: {selected_type}", st.session_state.score, total_questions)
                    st.session_state.current_index = 0
                    st.session_state.score = 0
                    st.session_state.answered = False
                    del st.session_state['current_topic'] 
                    st.rerun()

# --- CHẾ ĐỘ 2: ĐỀ THI TỔNG HỢP ---
elif mode == "📝 Đề thi tổng hợp":
    st.title("📝 Đề Thi Tổng Hợp (10 Câu)")
    
    if 'exam_generated' not in st.session_state or not st.session_state.exam_generated:
        exam_qs = []
        for t in list_types:
            qs_of_type = [q for q in questions if q["type"] == t]
            if len(qs_of_type) >= 2: exam_qs.extend(random.sample(qs_of_type, 2))
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
            user_ans = st.session_state.user_answers[q['id']]
            # SỬ DỤNG HÀM CHẤM ĐIỂM THÔNG MINH
            if kiem_tra_dap_an(user_ans, q["answer"]):
                total_score += 1
            else:
                ghi_loi_sai(st.session_state.username, q["type"], q["question"])
                
        st.write(f"### 🎯 Số câu đúng: {total_score} / 10")
        
        if st.button("Lưu kết quả và Làm đề khác"):
            ghi_nhat_ky_hoc_tap(st.session_state.username, "Đề thi tổng hợp", total_score, 10)
            st.session_state.exam_generated = False
            st.rerun()

        # --- CHI TIẾT BÀI LÀM (XANH/ĐỎ VÀ GIẢI THÍCH) ---
        st.markdown("---")
        st.subheader("🔍 CHI TIẾT BÀI LÀM CỦA CON")
        
        for i, q in enumerate(st.session_state.exam_qs):
            user_ans = st.session_state.user_answers[q['id']].strip()
            correct_ans = q["answer"].strip()
            is_correct = kiem_tra_dap_an(user_ans, correct_ans)
            
            if is_correct:
                st.success(f"**Câu {i+1}:** {q['question']}\n\n✅ **Chính xác!** Đáp án của con: **{user_ans}**")
            else:
                ans_display = user_ans if user_ans != "" else "(Con chưa làm)"
                st.error(f"**Câu {i+1}:** {q['question']}\n\n❌ **Chưa đúng rồi.** Đáp án của con: {ans_display} 👉 **Đáp án chuẩn: {correct_ans}**")
            
            theory = THEORY_DATA.get(q["type"], {})
            phuong_phap = theory.get("phuong_phap", "Đang cập nhật...")
            sai_lam = theory.get("sai_lam", "Đang cập nhật...")
            st.info(f"💡 **Cách làm dạng bài này ({q['type']}):**\n{phuong_phap}\n\n⚠️ **Lỗi dễ mắc phải:** {sai_lam}")
            st.write("---")