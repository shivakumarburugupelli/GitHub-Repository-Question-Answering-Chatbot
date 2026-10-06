import streamlit as st
from urllib.parse import urlparse
import requests
st.title("GitHUB reposirtory Q&A chat bot")

github_url=st.text_input("enter github repository url")
if github_url:  
    parsed = urlparse(github_url)

    if parsed.netloc.lower() == "github.com":
        st.success("Valid GitHub URL")
        # Continue with repository processing 
    else:
        st.error("Please enter a valid GitHub repository URL.")
if st.button("load repository"):
    if github_url:
        try:
            response = requests.post("http://127.0.0.1:8000/load",json={"github_url": github_url})
            
            if response.status_code == 200:
                result=response.json()
                st.success(result["message"])
         
            else:
                st.error(f"Failed to load repository. Status code: {response.status_code}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a valid GitHub repository URL.")

    ##ask question
question=st.text_input("Ask a question about the repository")
if st.button("Ask"):

    if question:
        try:

            response = requests.post(
                "http://127.0.0.1:8000/ask",
                json={
                    "question": question
                }
            )
            if response.status_code == 200:

                result = response.json()

                st.write(result["answer"])
            else:

                st.error(
                    f"Error: {response.text}"
                )
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a question")