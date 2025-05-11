import streamlit as st
from utils.send_email import send_email_notification
from utils.dbutils import (
    init_db, create_user, verify_user_credentials,
    get_user_by_username, insert_message, get_chat_history, generate_chat_id, get_all_chat_ids_for_user, update_chat_name, delete_chat,migrate_add_chat_name_column
)
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.callbacks.streamlit.streamlit_callback_handler import StreamlitCallbackHandler
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.schema import AIMessage, HumanMessage
import uuid
import os

# --------------------------
# 🔧 Init
# --------------------------

init_db()
migrate_add_chat_name_column()
load_dotenv()

os.environ["STREAMLIT_HOME"] = "/app/.streamlit"
os.environ["GOOGLE_API_KEY"] = os.environ.get("GOOGLE_API_KEY", "")
os.environ["TAVILY_API_KEY"] = os.environ.get("TAVILY_API_KEY", "")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.name = None

# --------------------------
# 🔐 Login
# --------------------------
if not st.session_state.authenticated:
    st.title("AMEYAGPT")
    with st.form("login_form"):
        st.subheader("Login")
        username_input = st.text_input("Username")
        password_input = st.text_input("Password", type="password")
        login_btn = st.form_submit_button("Login")

        if login_btn and verify_user_credentials(username_input, password_input):
            user = get_user_by_username(username_input)
            st.session_state.authenticated = True
            st.session_state.username = user["username"]
            st.session_state.name = user["full_name"]
            st.session_state.chat_id = f"{user['username']}_{uuid.uuid4().hex[:8]}"
            st.rerun()
        elif login_btn:
            st.error("Incorrect username or password.")

# --------------------------
# 📝 Registration
# --------------------------
if not st.session_state.authenticated:
    with st.expander("🆕 New User? Register Here"):
        new_username = st.text_input("Choose a username")
        new_name = st.text_input("Your full name")
        new_email = st.text_input("Email address")
        new_password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        if st.button("Register"):
            if new_password != confirm_password:
                st.error("Passwords do not match.")
            elif get_user_by_username(new_username):
                st.error("Username already exists.")
            else:
                if create_user(new_username, new_name, new_email, new_password):
                    send_email_notification(new_email, new_username)
                    st.success("Registration successful. Please login.")
                else:
                    st.error("User creation failed.")

# --------------------------
# ✅ Authenticated View
# --------------------------
if st.session_state.authenticated:
    st.sidebar.subheader(f"👤 {st.session_state.name}")

    # Sidebar Chat History
    chat_list = get_all_chat_ids_for_user(st.session_state.username)
    chat_labels = [f"{name} ({cid[:8]})" if name else cid[:14] for cid, name in chat_list]
    chat_ids = [cid for cid, _ in chat_list]

    if not chat_ids:
        st.warning("No chats found. Click ➕ New Chat to start.")
        new_id = f"{st.session_state.username}_{uuid.uuid4().hex[:8]}"
        st.session_state.chat_id = new_id
        insert_message(st.session_state.username, new_id, "assistant", f"👋 Hello! {st.session_state.username}, your AI assistant. How can I help you today?")
        st.rerun()  # Important: stop execution
    
    selected_chat_idx = st.sidebar.radio("🗂 Your Chats", list(range(len(chat_ids))), format_func=lambda i: chat_labels[i])
    selected_chat = chat_ids[selected_chat_idx]

    with st.sidebar.expander("🛠 Manage Chat"):
        new_name = st.text_input("Rename this chat", value=dict(chat_list).get(selected_chat, ""))
        if st.button("💾 Save Name"):
            if update_chat_name(selected_chat, new_name):
                st.success("Chat name updated.")
                st.rerun()

        if st.button("🗑️ Delete Chat"):
            if delete_chat(selected_chat):
                st.session_state.chat_id = None
                st.success("Chat deleted.")
                st.rerun()

    # New Chat
    if st.sidebar.button("➕ New Chat"):
        new_id = f"{st.session_state.username}_{uuid.uuid4().hex[:8]}"
        st.session_state.chat_id = new_id
        insert_message(st.session_state.username, new_id, "assistant", f"👋 Hello! {st.session_state.username}, your AI assistant. How can I help you today?")
        st.rerun()

    # Logout
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

    # Use selected chat
    if "chat_id" not in st.session_state:
        st.session_state.chat_id = selected_chat if selected_chat else f"{st.session_state.username}_{uuid.uuid4().hex[:8]}"
    elif selected_chat and selected_chat != st.session_state.chat_id:
        st.session_state.chat_id = selected_chat
        st.rerun()

    # Header
    st.title("🤖 Ameya GPT")
    st.success(f"You are logged in as {st.session_state.username}.")
    st.caption(f"🧾 Chat ID: `{st.session_state.chat_id}`")

    # --------------------------
    # 🧠 Load memory from DB
    # --------------------------
    def get_langchain_messages(chat_id):
        raw = get_chat_history(chat_id, n=3)
        return [HumanMessage(content=m) if r == "user" else AIMessage(content=m) for r, m in raw]

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    memory.chat_memory.messages = get_langchain_messages(st.session_state.chat_id)

    # --------------------------
    # 🧠 Agent Setup
    # --------------------------
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", temperature=0)
    tools = [TavilySearchResults(k=1)]

    prompt = PromptTemplate(
        input_variables=["input", "agent_scratchpad", "tools", "tool_names", "chat_history"],
        template=
        """
            You are AIGPT — a witty, sharp, and slightly sarcastic AI assistant who can use tools only when strictly necessary.

            You always respond in the format below:

            1. If the input is a simple greeting like "hello", "hi", "hey", etc. → DO NOT use any tool.
            2. If the answer can be derived from memory/chat history → DO NOT use any tool.
            3. Use a tool **only** if the question requires current or external data that is not present in memory.

            When in doubt, DO NOT use a tool. Respond based on your knowledge or the provided history.

            ---

            **Tool usage format (strict):**

            Question: {input}  
            Thought: Think through what to do next  
            Action: (only if required, choose from [{tool_names}])  
            Action Input: input to the tool  
            Observation: result from the tool  
            ... (repeat if necessary)  
            Thought: I now know the final answer  
            Final Answer: your final answer

            ---

            **Your tools:**  
            {tools}

            **Your memory:**  
            {chat_history}

            ---

            Begin!

            Question: {input}  
            Thought: {agent_scratchpad}
        """
    )

    agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True,
        prompt_input_keys=["input", "chat_history"]
    )

    # --------------------------
    # 💬 Display chat history
    # --------------------------
    for role, msg in get_chat_history(st.session_state.chat_id, n=10):
        st.chat_message(role).write(msg)

    # --------------------------
    # 📤 Handle input
    # --------------------------
    if user_input := st.chat_input():
        st.chat_message("user").write(user_input)
        insert_message(st.session_state.username, st.session_state.chat_id, "user", user_input)

        with st.chat_message("assistant"):
            st_callback = StreamlitCallbackHandler(st.container())
            response = agent_executor.invoke({"input": user_input}, {"callbacks": [st_callback]})
            final_answer = response["output"]
            st.write(final_answer)
            insert_message(st.session_state.username, st.session_state.chat_id, "assistant", final_answer)
