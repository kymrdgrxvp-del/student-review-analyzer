from groq import Groq
import streamlit as st

client = Groq(api_key="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")

st.title("🎓 Student Review Analyzer")
st.write("Nhập đánh giá môn học, AI sẽ phân tích cho bạn!")

review = st.text_area("Nhập review môn học:", placeholder="VD: Môn này thầy dạy dễ hiểu nhưng bài tập quá nhiều...")

if st.button("Phân tích"):
    if review:
        with st.spinner("Đang phân tích..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": f"""Phân tích review môn học sau và trả lời theo format:

1. Sentiment: (Tích cực / Tiêu cực / Trung lập)
2. Điểm tốt: (nếu có)
3. Điểm chưa tốt: (nếu có)
4. Tóm tắt: (1 câu)

Review: {review}"""
                    }
                ]
            )
            st.write(response.choices[0].message.content)
    else:
        st.warning("Bạn chưa nhập review!")