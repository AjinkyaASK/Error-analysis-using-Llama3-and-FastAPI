import streamlit as st
import requests

st.set_page_config(layout="wide")

# API URL
API_URL = "http://localhost:8000/analyse_error"  # Replace with your actual API URL if deployed

# Function to call the error analysis API
def call_error_analysis_api(error_log):
    try:
        response = requests.post(API_URL, json={"error_log": error_log})
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()["analysis"]
    except requests.exceptions.RequestException as e:
        st.error(f"Error calling the API: {e}")
        return None

# Main app logic
def app():
    # Title of the app
    st.title("Error Log Analysis")

    # Text area for error log input
    error_log = st.text_area("Enter the error log:", placeholder="Paste or type here", height=150)

    # Initialize session state variables if they don't exist
    if "loading" not in st.session_state:
        st.session_state["loading"] = False
    if "submitted" not in st.session_state:
        st.session_state["submitted"] = False
    if "result" not in st.session_state:
        st.session_state["result"] = None

    # Show the Submit button only if the API call is not in progress
    if not st.session_state["loading"]:
        if st.button("Submit"):
            if not error_log.strip():
                st.warning("Error log cannot be empty.")
            else:
                # Set loading to True and make the API call
                st.session_state["loading"] = True
                with st.spinner("Analyzing error log..."):
                    result = call_error_analysis_api(error_log)
                    if result:
                        st.session_state["submitted"] = True
                        st.session_state["result"] = result
                    st.session_state["loading"] = False  # Turn off loading
                    
    st.divider()

    # Show results after API response
    if st.session_state["submitted"] and st.session_state["result"]:
        result = st.session_state["result"]

        # Cause block
        with st.container():
            st.header("Cause", divider=True)
            st.caption("The reason behind the error")
            for cause in result['cause']:
                st.write(f"- {cause}")

        # Impact block
        with st.container():
            st.header("Impact", divider=True)
            st.caption("How this error could affect your business")
            for impact in result['impact']:
                st.write(f"- {impact}")

        # Fix block
        with st.container():
            st.header("Fix", divider=True)
            st.caption("Steps to resolve the error")
            for fix in result['fix']:
                st.write(f"- {fix}")

        # Show Reset button when results are displayed
        if st.button("Reset"):
            # Reset the session state to initial conditions
            st.session_state["submitted"] = False
            st.session_state["result"] = None
            # st.experimental_rerun()  # Reload the app state

# Run the app
if __name__ == "__main__":
    app()
