import streamlit as st
import json
import random

# --- 1. CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="App Ôn Tập Toán Lớp 4", page_icon="🧮", layout="wide")

# --- 2. DỮ LIỆU LÝ THUYẾT (Tích hợp sẵn) ---
THEORY_DATA = {
    "Trung bình cộng": {
        "khai_niem": "Số trung bình cộng san đều giá trị của tất cả các số trong một nhóm.",
        "phuong_phap": "Bước 1: Tính TỔNG các số.\nBước 2: Lấy TỔNG chia cho SỐ CÁC SỐ HẠNG.",
        "sai_lam": "Quên đóng ngoặc khi tính tổng trước khi chia. Ví dụ sai: 4 + 6 : 2. Đúng phải là: (4 + 6) : 2."
    },
    "Tổng và Hiệu": {
        "khai_niem": "Tìm hai đại lượng khi biết tổng cộng và sự chênh lệch (hiệu) của chúng.",
        "phuong_phap": "Số Lớn = (Tổng + Hiệu) : 2\nSố Bé = (Tổng - Hiệu) : 2\n(Nên dùng 1 công thức tìm 1 số, số còn lại lấy Tổng trừ đi cho nhanh).",
        "sai_lam": "Nhầm lẫn giữa nửa chu vi và chu vi (chu vi phải chia 2 mới ra tổng của chiều dài và chiều rộng)."
    },
    "Dấu hiệu chia hết": {
        "khai_niem": "Nhận biết một số có chia hết cho 2, 3, 5, 9 hay không mà không cần đặt tính.",
        "phuong_phap": "- Chia hết cho 2: Tận cùng là 0, 2, 4, 6, 8.\n- Chia hết cho 5: Tận cùng là 0 hoặc 5.\n- Chia hết cho 3 hoặc 9: Cộng tất cả các chữ số lại, nếu tổng chia hết cho 3 hoặc 9 thì số đó chia hết.",
        "sai_lam": "Áp dụng sai quy tắc của 2,5 (xét đuôi) cho 3,9 (phải xét tổng)."
    },
    "Phân số": {
        "khai_niem": "Biểu diễn phần bằng nhau của một đơn vị.",
        "phuong_phap": "- Cộng/Trừ: Phải quy đồng đưa về cùng mẫu số rồi mới cộng/trừ tử số.\n- Nhân: Tử nhân tử, mẫu nhân mẫu.\n- Chia: Phân số thứ nhất NHÂN với phân số thứ hai ĐẢO NGƯỢC.",
        "sai_lam": "Cộng/Trừ hai phân số mà lại lấy tử cộng tử, mẫu cộng mẫu (Ví dụ sai: 1/2 + 1/3 = 2/5)."
    },
    "Hình học": {
        "khai_niem": "Tính diện tích các hình cơ bản lớp 4.",
        "phuong_phap": "- Hình bình hành: S = Độ dài đáy x Chiều cao (S = a x h).\n- Hình thoi: S = (Đường chéo 1 x Đường chéo 2) : 2.",
        "sai_lam": "Quên chia 2 khi tính diện tích hình thoi, hoặc các đơn vị đo độ dài chưa giống nhau đã vội nhân."
    }
}

# --- 3. ĐỌC DỮ LIỆU CÂU HỎI ---
try:
    with open("data_toan_lop_4.json", "r", encoding="utf-8") as f:
        questions = json.load(f)
except:
    st.error("Không tìm thấy file dữ liệu data_toan_lop_4.json. Bạn nhớ để cùng thư mục nhé!")
    st.stop()

list_types = list(set([q["type"] for q in questions]))

# --- 4. MENU BÊN TRÁI ---
st.sidebar.title("🧮 MENU HỌC TẬP")
mode = st.sidebar.radio("Con muốn làm gì hôm nay?", ["📚 Học theo chuyên đề", "📝 Đề thi tổng hợp"])

# Reset state nếu chuyển chế độ
if 'current_mode' not in st.session_state or st.session_state.current_mode != mode:
    st.session_state.current_mode = mode
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.exam_generated = False

# ==========================================
# CHẾ ĐỘ 1: HỌC THEO CHUYÊN ĐỀ
# ==========================================
if mode == "📚 Học theo chuyên đề":
    st.title("📚 Luyện Tập Từng Chuyên Đề")
    selected_type = st.sidebar.selectbox("Chọn dạng toán:", list_types)
    
    # Lấy dữ liệu lý thuyết và câu hỏi
    theory = THEORY_DATA.get(selected_type, {})
    filtered_questions = [q for q in questions if q["type"] == selected_type]
    
    # TẠO 2 TAB: Lý thuyết và Luyện tập
    tab1, tab2 = st.tabs(["📖 Đọc Lý Thuyết", "✍️ Luyện Tập Thực Hành"])
    
    with tab1:
        st.header(f"Lý thuyết: {selected_type}")
        st.info(f"**📌 Khái niệm:** {theory.get('khai_niem', '')}")
        st.success(f"**💡 Phương pháp giải:**\n{theory.get('phuong_phap', '')}")
        st.warning(f"**⚠️ Sai lầm cần tránh:** {theory.get('sai_lam', '')}")
        
    with tab2:
        total_questions = len(filtered_questions)
        if total_questions > 0:
            index = st.session_state.current_index
            if index < total_questions:
                q = filtered_questions[index]
                
                col_prog, col_score = st.columns([3, 1])
                with col_prog:
                    st.write(f"**Tiến độ:** Câu {index + 1} / {total_questions}")
                    st.progress((index + 1) / total_questions)
                with col_score:
                    st.write(f"🏆 **Điểm: {st.session_state.score}**")
                
                st.subheader(f"Câu {index + 1} ({q['level']}):")
                st.write(q["question"])
                
                user_ans = st.text_input("Nhập đáp án của con:", key=f"prac_{q['id']}")
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("Kiểm tra", key=f"btn_check_{q['id']}"):
                        if user_ans.strip() == q["answer"].strip():
                            st.success("🎉 Xuất sắc! Con làm đúng rồi!")
                            if not st.session_state.answered:
                                st.session_state.score += 1
                                st.session_state.answered = True
                            st.balloons()
                        else:
                            st.error(f"❌ Chưa chính xác. Đáp án đúng là: {q['answer']}")
                            st.session_state.answered = True
                            
                with col2:
                    if st.button("Câu tiếp theo ➡️", key=f"btn_next_{q['id']}"):
                        st.session_state.current_index += 1
                        st.session_state.answered = False
                        st.rerun()
            else:
                st.success("🏆 CHÚC MỪNG CON ĐÃ HOÀN THÀNH CHUYÊN ĐỀ NÀY!")
                st.write(f"### 🎯 Điểm tổng kết: {st.session_state.score} / {total_questions}")
                if st.button("🔄 Luyện tập lại từ đầu"):
                    st.session_state.current_index = 0
                    st.session_state.score = 0
                    st.session_state.answered = False
                    st.rerun()

# ==========================================
# CHẾ ĐỘ 2: ĐỀ THI TỔNG HỢP
# ==========================================
elif mode == "📝 Đề thi tổng hợp":
    st.title("📝 Đề Thi Tổng Hợp Đánh Giá Năng Lực")
    st.write("Đề thi gồm 10 câu hỏi ngẫu nhiên từ tất cả các dạng. Con hãy làm hết rồi bấm NỘP BÀI nhé!")
    
    # Sinh đề thi ngẫu nhiên 10 câu (mỗi dạng lấy 2 câu) và lưu vào bộ nhớ
    if not st.session_state.exam_generated:
        exam_qs = []
        for t in list_types:
            qs_of_type = [q for q in questions if q["type"] == t]
            if len(qs_of_type) >= 2:
                exam_qs.extend(random.sample(qs_of_type, 2))
            else:
                exam_qs.extend(qs_of_type)
        random.shuffle(exam_qs) # Trộn đều các câu hỏi
        st.session_state.exam_qs = exam_qs
        st.session_state.exam_generated = True
        st.session_state.exam_submitted = False
        st.session_state.exam_results = {}

    exam_qs = st.session_state.exam_qs

    # Dùng form để gộp tất cả câu trả lời trước khi nộp
    with st.form("exam_form"):
        user_answers = {}
        for i, q in enumerate(exam_qs):
            st.markdown(f"**Câu {i+1} ({q['type']}):** {q['question']}")
            user_answers[q['id']] = st.text_input(f"Đáp án câu {i+1}:", key=f"exam_{q['id']}")
            st.write("---")
            
        submitted = st.form_submit_button("✅ NỘP BÀI VÀ CHẤM ĐIỂM")
        
        if submitted:
            st.session_state.exam_submitted = True
            
    # Xử lý sau khi nộp bài
    if st.session_state.exam_submitted:
        st.header("📊 BẢNG TỔNG KẾT KẾT QUẢ")
        
        total_score = 0
        weak_topics = set() # Tập hợp các dạng toán con làm sai
        
        # Chấm điểm từng câu
        for i, q in enumerate(exam_qs):
            correct_ans = q["answer"].strip()
            user_ans = user_answers[q['id']].strip()
            
            if user_ans == correct_ans:
                total_score += 1
            else:
                weak_topics.add(q["type"])
                
        # Hiển thị điểm số
        st.write(f"### 🎯 Số câu đúng: {total_score} / {len(exam_qs)}")
        if total_score == len(exam_qs):
            st.success("🌟 THIÊN TÀI TOÁN HỌC! Con đã làm đúng 100%!")
            st.balloons()
        else:
            st.warning("💪 Rất nỗ lực! Hãy xem lại phần nhận xét bên dưới để giỏi hơn nữa nhé.")
            
        # Đánh giá và bổ trợ lỗ hổng
        if weak_topics:
            st.markdown("### 🔍 PHÂN TÍCH LỖ HỔNG & ÔN TẬP BỔ TRỢ")
            st.write("Hệ thống nhận thấy con còn nhầm lẫn ở các dạng toán sau. Con hãy đọc lại bí kíp nhé:")
            for topic in weak_topics:
                with st.expander(f"⚠️ Cần ôn lại: {topic} (Bấm vào đây để xem bí kíp)"):
                    theory = THEORY_DATA.get(topic, {})
                    st.info(f"**Cách làm:**\n{theory.get('phuong_phap', '')}")
                    st.error(f"**Lỗi hay mắc:** {theory.get('sai_lam', '')}")
                    st.write(f"*👉 Bố mẹ hãy cho con vào phần 'Học theo chuyên đề' -> chọn '{topic}' để con luyện tập thêm nhé!*")
                    
        if st.button("🔄 Tạo đề thi mới"):
            st.session_state.exam_generated = False
            st.rerun()