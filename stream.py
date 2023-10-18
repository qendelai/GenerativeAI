# Import essential libraries
import streamlit as st
import requests



def ask_mistral(response_input: str = None, auth_token: str=None, api_url: str = None) -> str:    
    
    """
    This function is used to make API calls to Mistral AI .
    """
    
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }

    # Create a prompt
    prompt = f"""### Instruction: 
        Use the input below to create an instruction, which could have been used to generate the input using an LLM. 

        ### Input 
        {response_input}

        ### Response:
    """
    
    payload = {
        "inputs": prompt
    }
     
    # API call to Mistral AI Inference Endpoint API   
    output = requests.post(api_url, headers=headers, json=payload)
    
    return output.json()


# Set the page title and favicon
st.set_page_config(page_title="QuizWhiz", page_icon="🤖")

st.title("QuizWhiz 📖")

# Setup the API credentials
endpoint_api_url = st.sidebar.text_input(
    "User Endpoint API URL", help="The API URL for the user endpoint"
    )


# Setup Auth Token 
auth_token = st.sidebar.text_input(
    "Auth Token", help="The Auth Token for the user endpoint"
    )

# Check if any of them are with " " and remove them
if endpoint_api_url.startswith('"') and endpoint_api_url.endswith('"'):
    endpoint_api_url = endpoint_api_url[1:-1]

if auth_token.startswith('"') and auth_token.endswith('"'):
    auth_token = auth_token[1:-1]

# Check if both the auth token and endpoint api url are provided
if endpoint_api_url and auth_token:
    endpoint_api_url = endpoint_api_url
    auth_token = auth_token
    allow_custom_input = True 
else:
    allow_custom_input = False 
    endpoint_api_url = None 
    auth_token = None 
    

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

  
if response_input := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": response_input})
    st.chat_message("user").write(response_input)
    try:
        msg = ask_mistral(response_input, auth_token, endpoint_api_url)
    except Exception as e:
        msg = f"There is an Error Message: {e} -- please check the API URL and Auth Token"    
    
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
    
