import streamlit as st
from automation import read_file, generate_summary, generate_email, send_email

st.set_page_config(page_title="AI Business Automation Tool")

st.title("📊 AI Business Automation Tool")

st.write("Upload data → Get insights → Send email → Download report")

uploaded_file = st.file_uploader("Upload CSV / TXT", type=["csv", "txt"])

if uploaded_file:
    data = read_file(uploaded_file)

    st.success("File uploaded successfully!")

    if st.button("Generate Insights"):
        summary = generate_summary(data)
        st.session_state.summary = summary

    if "summary" in st.session_state:
        st.subheader("📈 Insights")
        st.write(st.session_state.summary)

        # Download
        st.download_button(
            "📥 Download Report",
            st.session_state.summary,
            file_name="report.txt"
        )

        # Email
        st.subheader("📧 Send Email")

        receiver_email = st.text_input("Enter receiver email:")

        if st.button("Send Email"):
            email_body = generate_email(st.session_state.summary)
            success = send_email(receiver_email, email_body)

            if success:
                st.success("Email sent successfully!")
            else:
                st.error("Failed to send email.")