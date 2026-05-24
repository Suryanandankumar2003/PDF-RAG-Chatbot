import streamlit as st
from main import create_qa_chain, get_answer
from database import (
    init_db,
    save_chat,
    load_all_chats,
    delete_all_chats,
    delete_chat
)
from datetime import datetime
import time

# Initialize Database

init_db()

# Page Settings

st.set_page_config(
    page_title="PDF RAG Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Greeting According To Time

current_hour = datetime.now().hour

if current_hour < 12:
    greeting = "Good Morning"

elif current_hour < 17:
    greeting = "Good Afternoon"

else:
    greeting = "Good Evening"

st.title(greeting)
st.subheader("PDF RAG Chatbot")

# Session States

if "messages" not in st.session_state:
    st.session_state.messages = []

if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None

if "chat_ended" not in st.session_state:
    st.session_state.chat_ended = False

if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

# Load Chats From SQLite

if "all_chats" not in st.session_state:
    st.session_state.all_chats = load_all_chats()

# Restore Last Opened Chat

if "current_chat" not in st.session_state:

    if len(st.session_state.all_chats) > 0:

        last_chat = list(
            st.session_state.all_chats.keys()
        )[-1]

        st.session_state.current_chat = last_chat

        st.session_state.messages = (
            st.session_state.all_chats[last_chat]
        )

    else:

        st.session_state.current_chat = "Chat 1"

if "chat_counter" not in st.session_state:
    st.session_state.chat_counter = (
        len(st.session_state.all_chats) + 1
    )

# Sidebar

with st.sidebar:

    st.title("Chat History")

    # New Chat Button

    if st.button("New Chat"):

        st.session_state.chat_counter += 1

        new_chat_name = (
            f"Chat {st.session_state.chat_counter}"
        )

        st.session_state.current_chat = new_chat_name

        st.session_state.messages = []

        st.session_state.chat_ended = False

        # Remove QA chain

        if "qa_chain" in st.session_state:
            del st.session_state.qa_chain

        # Remove uploaded filename

        if "uploaded_filename" in st.session_state:
            del st.session_state.uploaded_filename

        # Reset uploader

        st.session_state.uploader_key += 1

        st.rerun()

    st.divider()

    # Show Previous Chats

    if len(st.session_state.all_chats) == 0:

        st.info("No previous chats available.")

    else:

        for chat_name, chat_messages in reversed(
            list(st.session_state.all_chats.items())
        ):

            preview_title = chat_name

            # Use first user message as title

            for msg in chat_messages:

                if msg["role"] == "user":

                    preview_title = msg["content"][:25]

                    if len(msg["content"]) > 25:
                        preview_title += "..."

                    break

            # Create columns

            col1, col2 = st.columns([6, 3])

            # Open Chat Button

            with col1:

                if st.button(
                    preview_title,
                    key=f"open_{chat_name}"
                ):

                    st.session_state.current_chat = chat_name

                    st.session_state.messages = (
                        st.session_state.all_chats[chat_name]
                    )

                    st.session_state.chat_ended = False

                    st.rerun()

            # Delete Button

            with col2:

                if st.button(
                    "Delete",
                    key=f"delete_{chat_name}"
                ):

                    st.session_state[
                        "delete_chat_name"
                    ] = chat_name

            # Delete Confirmation

            if (
                "delete_chat_name" in st.session_state
                and st.session_state["delete_chat_name"]
                == chat_name
            ):

                st.warning(
                    "Do you want to permanently delete this chat?"
                )

                confirm_col1, confirm_col2 = st.columns(2)

                # Yes Delete

                with confirm_col1:

                    if st.button(
                        "Yes",
                        key=f"yes_{chat_name}"
                    ):

                        delete_chat(chat_name)

                        # Reload chats

                        st.session_state.all_chats = (
                            load_all_chats()
                        )

                        # Reset current chat if deleted

                        if (
                            st.session_state.current_chat
                            == chat_name
                        ):

                            st.session_state.messages = []

                            st.session_state.current_chat = (
                                "Chat 1"
                            )

                        # Remove confirmation state

                        del st.session_state[
                            "delete_chat_name"
                        ]

                        st.success(
                            "Chat deleted successfully!"
                        )

                        st.rerun()

                # Cancel Delete

                with confirm_col2:

                    if st.button(
                        "Cancel",
                        key=f"cancel_{chat_name}"
                    ):

                        del st.session_state[
                            "delete_chat_name"
                        ]

                        st.rerun()

            st.divider()

    # Settings Section

    st.subheader("Settings")

    if st.button("Clear All Chats"):

        # Clear SQLite chats

        delete_all_chats()

        # Clear session chats

        st.session_state.all_chats = {}

        # Clear messages

        st.session_state.messages = []

        # Reset current chat

        st.session_state.current_chat = "Chat 1"

        # Reset counter

        st.session_state.chat_counter = 1

        # Remove QA chain

        if "qa_chain" in st.session_state:
            del st.session_state.qa_chain

        # Remove uploaded filename

        if "uploaded_filename" in st.session_state:
            del st.session_state.uploaded_filename

        # Reset uploader

        st.session_state.uploader_key += 1

        st.success("All chats cleared successfully!")

        st.rerun()

# Current Chat Title

st.markdown(
    f"### {st.session_state.current_chat}"
)

# Upload PDF

uploaded_file = st.file_uploader(
    "Upload your PDF",
    type="pdf",
    key=f"uploaded_file_{st.session_state.uploader_key}"
)

# Process PDF Only Once

if uploaded_file is not None:

    if "uploaded_filename" not in st.session_state:

        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Beautiful Loader

        loader = st.markdown(
            """
            <div style="
                display: flex;
                align-items: center;
                gap: 10px;
                padding: 12px;
                border-radius: 10px;
                background-color: #262730;
                color: white;
                font-size: 18px;
                font-weight: bold;
            ">
                <div class="loader"></div>
                Processing PDF...
            </div>

            <style>
            .loader {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #00ffcc;
                border-radius: 50%;
                width: 22px;
                height: 22px;
                animation: spin 1s linear infinite;
            }

            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.session_state.qa_chain = create_qa_chain(
            uploaded_file.name
        )

        loader.empty()

        st.session_state.uploaded_filename = uploaded_file.name

        st.success("PDF processed successfully!")

# Display Messages

for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown("#### You")

        st.markdown(message["content"])

    else:

        st.markdown("#### Bot")

        st.markdown(message["content"])

    st.divider()

# Chat Section

if not st.session_state.chat_ended:

    if st.session_state.qa_chain:

        user_input = st.chat_input(
            "Ask question from uploaded PDF"
        )

        if user_input:

            # Show User Message

            st.markdown("#### You")

            st.markdown(user_input)

            st.divider()

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": user_input
                }
            )

            # Save Chat

            save_chat(
                st.session_state.current_chat,
                st.session_state.messages
            )

            # Reload Chats

            st.session_state.all_chats = load_all_chats()

            # Exit Chat

            if user_input.lower() in ["exit", "end"]:

                st.markdown("#### Bot")

                st.markdown(
                    "Chat ended successfully.\n\n"
                    "You can reopen this chat anytime from the sidebar."
                )

                st.session_state.chat_ended = True

                st.rerun()

            else:

                # Beautiful Loader

                loader = st.markdown(
                    """
                    <div style="
                        display: flex;
                        align-items: center;
                        gap: 10px;
                        padding: 12px;
                        border-radius: 10px;
                        background-color: #262730;
                        color: white;
                        font-size: 18px;
                        font-weight: bold;
                    ">
                        <div class="loader"></div>
                        Searching relevant information...
                    </div>

                    <style>
                    .loader {
                        border: 4px solid #f3f3f3;
                        border-top: 4px solid #00ffcc;
                        border-radius: 50%;
                        width: 22px;
                        height: 22px;
                        animation: spin 1s linear infinite;
                    }

                    @keyframes spin {
                        0% { transform: rotate(0deg); }
                        100% { transform: rotate(360deg); }
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )

                # Generate Answer

                try:

                    answer = get_answer(
                        st.session_state.qa_chain,
                        user_input
                    )

                    # Handle empty answers

                    if (
                        answer is None
                        or answer.strip() == ""
                        or "i don't know" in answer.lower()
                        or "not available" in answer.lower()
                        or "cannot find" in answer.lower()
                    ):

                        answer = (
                            "I do not have enough information "
                            "to answer this question.\n\n"
                            "Please try asking in another way "
                            "or ask something from the uploaded PDF."
                        )

                except Exception:

                    answer = (
                        "Something went wrong while processing "
                        "your question.\n\n"
                        "Please try again or upload a valid PDF."
                    )

                loader.empty()

                # Streaming Response

                st.markdown("#### Bot")

                message_placeholder = st.empty()

                full_response = ""

                lines = answer.split("\n")

                for line in lines:

                    words = line.split()

                    for word in words:

                        full_response += word + " "

                        message_placeholder.markdown(
                            full_response + "▌"
                        )

                        time.sleep(0.03)

                    full_response += "\n\n"

                    message_placeholder.markdown(
                        full_response + "▌"
                    )

                message_placeholder.markdown(
                    full_response
                )

                st.divider()

                # Save Assistant Message

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

                # Save Updated Chat

                save_chat(
                    st.session_state.current_chat,
                    st.session_state.messages
                )

                # Reload Chats

                st.session_state.all_chats = load_all_chats()

    else:

        st.info(
            "Please upload a PDF to start chatting."
        )

# After Chat Ends

else:

    st.success("Chat ended successfully.")

    st.warning(
        "You can reopen this chat anytime from the sidebar "
        "or start a completely new chat."
    )

    if st.button("Start New Chat"):

        st.session_state.chat_counter += 1

        new_chat_name = (
            f"Chat {st.session_state.chat_counter}"
        )

        st.session_state.current_chat = new_chat_name

        st.session_state.messages = []

        st.session_state.chat_ended = False

        # Remove QA chain

        if "qa_chain" in st.session_state:
            del st.session_state.qa_chain

        # Remove uploaded filename

        if "uploaded_filename" in st.session_state:
            del st.session_state.uploaded_filename

        # Reset uploader

        st.session_state.uploader_key += 1

        st.rerun()