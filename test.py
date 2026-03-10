import os
import pandas as pd
from datetime import datetime
from groq import Groq
import streamlit as st

# NHỚ THAY BẰNG API KEY MỚI CỦA ÔNG (ĐỪNG DÙNG CÁI CŨ ĐÃ LỘ NỮA NHÉ)
client = Groq(api_key="YOUR KEY")

st.title("🎓 Student Review Analyzer")
st.write("Nhập đánh giá môn học, AI sẽ phân tích cho bạn!")

review = st.text_area("Nhập review môn học:", placeholder="VD: Môn Giải tích 1 thầy dạy dễ hiểu nhưng bài tập quá nhiều...")

if st.button("Phân tích"):
    if review:
        with st.spinner("Đang phân tích..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": f"""Bạn là một chuyên gia phân tích dữ liệu giáo dục. Hãy đọc thật kỹ review môn học dưới đây và phân tích khách quan, tuyệt đối không bỏ sót chi tiết, dù là nhỏ nhất.

Trả lời chính xác theo format sau:
0. Môn học: (Tên môn học được nhắc đến, nếu không rõ thì ghi 'Không xác định')
1. Sentiment: (Chỉ chọn 1 trong 3: Tích cực / Tiêu cực / Trung lập)
2. Điểm tốt: (Tìm TẤT CẢ các chi tiết có lợi cho sinh viên, ví dụ: được cộng điểm, thầy hiền... Nếu không có thì ghi 'Không có')
3. Điểm chưa tốt: (Các điểm gây khó khăn, áp lực)
4. Tóm tắt: (1 câu ngắn gọn bao hàm đủ cả ý khen và chê)

Review: {review}"""
                    }
                ]
            )
            
            ai_result = response.choices[0].message.content
            st.write(ai_result)
            
            # --- KHÚC DE: BÓC TÁCH VÀ LƯU DATA ---
            try:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Tạo giá trị mặc định phòng trường hợp AI quên trả lời
                mon_hoc = "Không xác định"
                sentiment = "Không xác định"
                diem_tot = "Không xác định"
                diem_chua_tot = "Không xác định"
                
                # Quét từng dòng kết quả AI trả về để bóc tách thông tin
                lines = ai_result.split('\n')
                for line in lines:
                    if "0. Môn học:" in line:
                        mon_hoc = line.replace('0. Môn học:', '').strip()
                    elif "1. Sentiment:" in line:
                        sentiment = line.replace('1. Sentiment:', '').strip()
                    elif "2. Điểm tốt:" in line:
                        diem_tot = line.replace('2. Điểm tốt:', '').strip()
                    elif "3. Điểm chưa tốt:" in line:
                        diem_chua_tot = line.replace('3. Điểm chưa tốt:', '').strip()
                
                # Đóng gói thành 6 cột
                new_data = pd.DataFrame({
                    "Thời gian": [current_time],
                    "Môn học": [mon_hoc],
                    "Review": [review],
                    "Sentiment": [sentiment],
                    "Điểm tốt": [diem_tot],
                    "Điểm chưa tốt": [diem_chua_tot]
                })
                
                # Tên file mới để tránh đụng độ với file 3 cột cũ
                file_name = "reviews_history_v2.csv"
                
                if not os.path.exists(file_name):
                    new_data.to_csv(file_name, mode='w', header=True, index=False, encoding='utf-8-sig')
                else:
                    new_data.to_csv(file_name, mode='a', header=False, index=False, encoding='utf-8-sig')
                    
                st.success(f"✅ Đã lưu data thành công vào file {file_name}!")
                
            except Exception as e:
                st.error(f"Có lỗi khi lưu file: {e}")

    else:
        st.warning("Bạn chưa nhập review!")

# --- PHẦN HIỂN THỊ DASHBOARD ---
st.divider() 
st.subheader("📊 Lịch sử & Thống kê đánh giá")

file_name = "reviews_history_v2.csv"

if os.path.exists(file_name):
    df = pd.read_csv(file_name)
    
    st.write("**1. Bảng dữ liệu chi tiết:**")
    st.dataframe(df, use_container_width=True)
    
    st.write("**2. Thống kê Sentiment:**")
    sentiment_counts = df['Sentiment'].value_counts()
    st.bar_chart(sentiment_counts)
else:
    st.info("Chưa có dữ liệu nào. Hãy phân tích thử một review để xem kết quả ở đây nhé!")