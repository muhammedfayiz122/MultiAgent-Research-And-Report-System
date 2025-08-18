# MARRS – MultiAgent Research And Report System

**Version:** 0.1.0  
**License:** MIT  
**Authors:** Muhammed Fayiz (<muhammedfayiz122@gmail.com>)  
**Homepage:** [GitHub Repository](https://github.com/muhammedfayiz122/MultiAgent-Research-And-Report-System)

---

##  Overview

**MARRS** is a hierarchical multi-agent framework designed to streamline research, summarization, and document generation by delegating tasks to specialized agents—delivering real-time, accurate insights with minimal human effort.

### Core Capabilities:
- **Automated Task Routing**: A supervisory agent determines whether a query requires *medical research*, *financial analysis*, *summarization*, or *document generation*—and routes accordingly.
- **Specialized Agents**:
  - **Research Agents**: Fetch and analyze up-to-date data across healthcare, pharmaceuticals, finance, and biotech.
  - **Summarizer Agents**: Condense complex findings into concise summaries.
  - **Generator Agents**: Compile structured, detailed reports suitable for academic, business, or technical use.
- **End-to-End Workflow**: From real-time data retrieval to polished outputs—without manual intervention.

---

##  Table of Contents

1. [Getting Started](#getting-started)  
2. [Architecture & Workflow](#architecture--workflow)  
3. [Tech Stack](#tech-stack)  
4. [Installation & Usage](#installation--usage)  
5. [Contribution Guidelines](#contribution-guidelines)  
6. [License](#license)

---

##  Getting Started

Use this system to:

- Conduct **real-time scientific or financial research**
- Automatically **summarize findings**
- **Generate polished reports**, all orchestrated by AI agents

---

##  Architecture & Workflow

```
User Query
    ↓
Supervisor Agent → Classifies the task
    ↙       ↘           ↘
Medical   Financial   Summary/Report
Research  Research    Generator
  Agent     Agent        Agent

      ⬇ Outputs (in session folder with download links)
```

- Inputs are processed via a **supervisor agent**.
- Results are saved in per-session folders for isolation and traceability.
- If a report is generated, users can **download it via the UI**.

---

##  Tech Stack

- **Python ≥ 3.10**
- **Agents**: Modular, prompt-based tooling with clear role definitions.
- **Orchestration**: Supervisor dynamically routes tasks.
- **Persistence**: Session-based file storage for summaries and final reports.
- **Frontend**: Streamlit (for interactive demos and UI).
- **CLI / API** (future): Can integrate with REST or CLI endpoints for automation.

---

##  Installation & Usage

### 1. Set Up Your Environment
```bash
git clone https://github.com/muhammedfayiz122/MultiAgent-Research-And-Report-System.git
cd MultiAgent-Research-And-Report-System
python3 -m venv .venv
source .venv/bin/activate   # On Windows: .\.venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit Demo
```bash
streamlit run app.py
```
- Enter your query.
- Let the system auto-detect the task and dispatch appropriate agents.
- Download the generated report (if applicable) directly from the UI.

---

##  Contribution Guidelines

Contributions welcome! To help maintain quality:

- **Fork** the repo and work on a separate branch.
- Ensure your PR includes:
  - Clear **descriptions**
  - **Unit tests**
  - **Consistent docstrings**
- Adhere to **PEP8 styling** and ensure compatibility with Python 3.10+.

---

##  License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.

---

##  Why MARRS Stands Out

- **True automation**: Minimal to no human intervention—from query to polished output.
- **Highly modular**: Easily extendable agent layers for domain-specific tasks.
- **Session-aware**: Clean, traceable folder structure for each user interaction.
- **Scalable UI**: Streamlit frontend simplifies testing and prototyping.

---

###  A Note on Related Work

Many multi-agent research systems exist, like:
- **ReportWriter** (LangGraph-based, interactive analyst workflows)  
- **AI-Doc-Generator** (agent-based report pipelines with citation tracking)  

**MARRS** differentiates itself through:
- **Specialized medical & financial domains**  
- Supervisory routing logic that **auto-selects tasks**  
- Session-level file management and UI-based delivery
