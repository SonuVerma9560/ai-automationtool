import streamlit as st
from automation import load_file, generate_summary, send_email

st.set_page_config(page_title="AI Business Automation Tool")

st.title("📊 AI Business Automation Tool")
st.write("Upload data → Get insights → Send email → Download report")

uploaded_file = st.file_uploader("Upload Excel / CSV / TXT", type=["csv", "xlsx", "txt"])

# Store summary in session
if "summary" not in st.session_state:
    st.session_state.summary = None

if uploaded_file is not None:
    st.success("File uploaded successfully!")
    data = load_file(uploaded_file)

    # Generate insights
    if st.button("Generate Insights"):
        st.session_state.summary = generate_summary(data)

# Show results AFTER generation
if st.session_state.summary:
    st.subheader("📊 Insights")
    st.write(st.session_state.summary)

    # Download
    st.download_button(
        label="📥 Download Report",
        data=st.session_state.summary,
        file_name="report.txt"
    )

    # Email section
    st.subheader("📧 Send Email")

    receiver_email = st.text_input("Enter receiver email:")

    if st.button("Send Email"):
        if receiver_email:
            result = send_email(
                receiver_email,
                "AI Report",
                st.session_state.summary
            )
            st.success(result)
        else:
            st.warning("Enter email first")