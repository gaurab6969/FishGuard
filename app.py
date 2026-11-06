import streamlit as st

from src.detector import detect_url, detect_email

st.set_page_config(
    page_title="FishGuard",
    page_icon="🛡️"
)

st.title("🛡️ FishGuard")
st.subheader("Phishing URL & Email Detector")

st.info(
    "This is a cybersecurity prototype tool. "
    "It cannot guarantee that a URL or email is safe."
)

url_tab, email_tab = st.tabs(
    ["🔗 URL Detection", "📧 Email Detection"]
)

with url_tab:
    url = st.text_input("Enter a suspicious URL")

    if st.button("Analyze URL"):
        if not url.strip():
            st.error("Please enter a URL.")
        elif len(url) > 4096:
            st.error("URL exceeds the allowed size.")
        else:
            with st.spinner("Analyzing URL…"):
                result = detect_url(url)

            st.subheader(result["verdict"])

            if result["probability"] is not None:
                st.metric(
                    "Model phishing probability",
                    f'{result["probability"]:.1%}'
                )

            st.write("**Indicators:**")
            if result["indicators"]:
                for item in result["indicators"]:
                    st.write(f"- {item}")
            else:
                st.write("No obvious lexical indicators.")

with email_tab:
    email = st.text_area(
        "Paste email text",
        height=250
    )

    if st.button("Analyze Email"):
        if not email.strip():
            st.error("Please enter email content.")
        elif len(email) > 200000:
            st.error("Email is too large.")
        else:
            with st.spinner("Analyzing email…"):
                result = detect_email(email)

            st.subheader(result["verdict"])

            if result["probability"] is not None:
                st.metric(
                    "Model phishing probability",
                    f'{result["probability"]:.1%}'
                )

            if result["indicators"]:
                st.write("**Indicators:**")
                for item in result["indicators"]:
                    st.write(f"- {item}")
            else:
                st.write("No suspicious indicators found.")

            if result["urls"]:
                st.write("**Extracted URLs:**")
                for item in result["urls"]:
                    st.code(item)

st.caption(
    "FishGuard | Educational cybersecurity project"
)
