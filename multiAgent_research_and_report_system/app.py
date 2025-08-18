from logging import log
import streamlit as st
import os
import uuid
from multiAgent_research_and_report_system.graph.supervisor import getSupervisorGraph
from multiAgent_research_and_report_system.logger.cloud_logger import CustomLogger

log = CustomLogger().get_logger(__name__)
# --- Streamlit Page Config ---
st.set_page_config(page_title="MARRS - MultiAgent Research & Report System", layout="wide")

st.title("🛰️ MARRS: MultiAgent Research & Report System")
st.markdown("""
MARRS is a hierarchical multi-agent framework that automates research, summarization, 
and document generation.  
Simply enter your query — the supervisor agent will decide the task.
""")

# --- Session Management ---
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8]

# session_folder = f"session_{st.session_state.session_id}"
session_folder = "sessions"
os.makedirs(session_folder, exist_ok=True)

# --- Input ---
query = st.text_area("Enter your query")

# --- Run System ---
if st.button("Run Agent System"):
    if not query.strip():
        st.warning("⚠️ Please provide a query.")
    else:
        st.info("🤖 Routing to the appropriate agent...")

        # --- Import Graphs ---
        supervisor_graph = getSupervisorGraph()

        for message in supervisor_graph.stream(
            {"messages": [("user", query)]},
            {"recursion_limit": 100}
        ):
            log.info(message)
            print(message)
            try:
                for agent in message:
                    msg = message[agent]["messages"][0]
                    with st.chat_message(agent,avatar='👤'):
                        st.markdown(eval(msg).content)
            except:
                st.markdown(message)

        # --- Download Button if report generated ---
        generated_file = f"sessions/report.txt"
        if generated_file and os.path.exists(generated_file):
            with open(generated_file, "rb") as f:
                st.download_button(
                    label="⬇️ Download Report",
                    data=f,
                    file_name=os.path.basename(generated_file),
                    mime="application/pdf"
                )

# --- Footer ---
st.markdown("---")
st.caption("Developed by Muhammed Fayiz | MIT License | [GitHub](https://github.com/muhammedfayiz122/MultiAgent-Research-And-Report-System)")
