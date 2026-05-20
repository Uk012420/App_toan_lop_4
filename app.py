import streamlit as st
import json

# 1. Cấu hình giao diện
st.set_page_config(page_title="App Ôn Tập Toán Lớp 4", page_icon="🧮", layout="centered")
st.title("🧮 ỨNG DỤNG ÔN TẬP TOÁN LỚP 4")
st.write("Chúc con học tập thật tốt nhé! Đọc kỹ đề bài rồi điền đáp án con nha.")

# 2. Đọc dữ liệu từ file json (nhớ đảm bảo bạn đã tạo file data_toan_lop_4.json ở bước trước)
with open("data_toan_lop_4.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

# 3. Thanh chọn dạng toán ở bên trái
list_types = list(set([q["type"] for q in questions]))
selected_type = st.sidebar.selectbox("Chọn Dạng Toán Con Muốn Ôn:", list_types)

# Lọc câu hỏi theo dạng toán đã chọn
filtered_questions = [q for q in questions if q["type"] == selected_type]
total_questions = len(filtered_questions)

# 4. TẠO "TRÍ NHỚ" CHO PHẦN MỀM (Session State)
# Giúp phần mềm nhớ con đang làm đến câu nào. Nếu đổi dạng toán thì quay về câu đầu tiên.
if 'current_topic' not in st.session_state or st.session_state.current_topic != selected_type:
    st.session_state.current_topic = selected_type
    st.session_state.current_index = 0  # Bắt đầu từ câu số 0 (câu đầu tiên)

# 5. Hiển thị 1 câu hỏi duy nhất trên màn hình
if total_questions > 0:
    index = st.session_state.current_index
    q = filtered_questions[index]
    
    # Hiện tiến độ học (Ví dụ: Câu 1 / 100)
    st.write(f"**Tiến độ:** Câu {index + 1} / {total_questions}")
    st.progress((index + 1) / total_questions) # Thanh chạy dài hiển thị tiến độ
    
    # Hiện câu hỏi
    st.subheader(f"Câu {index + 1} ({q['level']}):")
    st.info(q["question"])
    
    # Ô nhập đáp án (mỗi câu có một key riêng để tự động làm sạch ô khi sang câu mới)
    user_ans = st.text_input("Nhập đáp án của con vào đây:", key=f"input_{q['id']}")
    
    # Tạo 2 cột để chứa 2 nút bấm nằm ngang nhau cho đẹp
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Kiểm tra đáp án", key=f"btn_check_{q['id']}"):
            if user_ans.strip() == q["answer"].strip():
                st.success("🎉 Xuất sắc! Con làm đúng rồi!")
                st.balloons() # Bắn bóng bay chúc mừng trên màn hình
            else:
                st.error(f"❌ Chưa chính xác rồi con ơi. Đáp án đúng là: {q['answer']}")
                
    with col2:
        # Nếu chưa phải câu cuối cùng thì hiện nút "Câu tiếp theo"
        if index < total_questions - 1:
            if st.button("Câu tiếp theo ➡️", key=f"btn_next_{q['id']}"):
                st.session_state.current_index += 1 # Tăng số thứ tự câu lên 1
                st.rerun() # Tải lại phần mềm để hiện câu mới
        else:
            st.success("🏆 Tuyệt vời! Con đã hoàn thành tất cả bài tập của phần này!")