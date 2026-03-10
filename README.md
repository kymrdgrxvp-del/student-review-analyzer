# 🎓 Student Review Analyzer (V2)

AI-powered tool to analyze student course reviews using Groq API + LLaMA 3.3.
Now with data storage and visualization dashboard.

## Features
- **Sentiment Analysis:** Phân tích cảm xúc (tích cực / tiêu cực / trung lập)
- **Detail Extraction:** Xác định điểm tốt và chưa tốt của môn học
- **Data Persistence:** Tự động lưu lịch sử vào file CSV bằng **Pandas**
- **Dashboard:** Hiển thị bảng dữ liệu và biểu đồ thống kê trực quan

## Tech Stack
- Python
- Streamlit
- Groq API (LLaMA 3.3 70B)
- Pandas (Data Handling)

## How to run
1. Clone repo
2. Install dependencies: `pip install groq streamlit pandas`
3. Tạo Groq API key tại [console.groq.com](https://console.groq.com), paste vào dòng `api_key` trong `test.py`
4. Run: `python3 -m streamlit run test.py`
