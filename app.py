import streamlit as st
import pandas as pd
import hashlib

def md5_hash(email):
    return hashlib.md5(email.strip().lower().encode()).hexdigest()

st.title("🧼 Email Suppression Cleaner")

email_file = st.file_uploader("📤 Upload Email List (CSV with 'email' column)", type=['csv'])
supp_file = st.file_uploader("📤 Upload Suppression List (MD5, CSV or TXT)", type=['csv', 'txt'])

if email_file and supp_file:
    try:
        emails_df = pd.read_csv(email_file)
        if 'email' not in emails_df.columns:
            st.error("❌ Your email list must have a column named 'email'.")
        else:
            suppression_df = pd.read_csv(supp_file, header=None, names=['md5'])
            emails_df['md5'] = emails_df['email'].apply(md5_hash)
            cleaned = emails_df[~emails_df['md5'].isin(suppression_df['md5'])]
            output = cleaned[['email']]

            # Download cleaned list
            csv = output.to_csv(index=False).encode('utf-8')
            st.success(f"✅ Cleaned list generated: {len(output)} emails remain.")
            st.download_button("📥 Download Cleaned CSV", csv, "cleaned_emails.csv", "text/csv")
    except Exception as e:
        st.error(f"❌ Error: {e}")
