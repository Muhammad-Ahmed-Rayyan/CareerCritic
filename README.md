<div align="center">

# 📋 CareerCritic

*Multi-Agent AI Resume Review Against Job Descriptions using LangGraph*

![Last Commit](https://img.shields.io/github/last-commit/Muhammad-Ahmed-Rayyan/CareerCritic)
![languages](https://img.shields.io/github/languages/count/Muhammad-Ahmed-Rayyan/CareerCritic)

<br>

Built with the tools and technologies:  
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-1C3C3C?style=for-the-badge&logo=langgraph&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-F55036?style=for-the-badge&logo=groq&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-%23FE4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

</div>

---

## 🧠 Project Summary

**CareerCritic** is a multi-agent AI system that reviews your resume against a job description using LangGraph orchestration. Four specialized agents — Parser, JobFit, Critic, and Writer — collaborate through a stateful graph with a genuine feedback loop to produce a structured fit report.

CareerCritic goes beyond a single LLM call. It demonstrates real multi-agent orchestration using LangGraph:

- **Parser Agent** extracts structured data (skills, experience, education, projects) from an uploaded resume
- **JobFit Agent** compares the parsed resume against a job description and drafts fit feedback
- **Critic Agent** evaluates whether that feedback is specific and actionable — if not, it routes back to JobFit for a revision (capped at 2 retries to guarantee termination)
- **Writer Agent** compiles the final Markdown report

[Try it out Here!](https://career-critic.streamlit.app)

---

## 🚀 Features

- 🤖 **Four-Agent Pipeline**
  Parser, JobFit, Critic, and Writer agents collaborate through a stateful LangGraph

- 🔁 **Genuine Feedback Loop**
  Critic → JobFit is a real conditional edge, not a fixed sequence — the core capability LangGraph provides over a standard LangChain chain

- 🛑 **Retry Cap for Guaranteed Termination**
  `MAX_RETRIES = 2` ensures the graph always terminates, even if the LLM repeatedly judges its own output as needing revision

- 🛡️ **Defensive JSON Parsing**
  Every agent strips markdown fences and falls back to a safe default structure if LLM output isn't valid JSON, so one malformed response doesn't crash the graph

- 📊 **Structured Fit Report**
  Fit score, matched/missing skills, and detailed feedback compiled into a final Markdown report

---

## 🗃️ Project Structure

```bash
CareerCritic/
├── agents/
│   ├── parser_agent.py
│   ├── jobfit_agent.py
│   ├── critic_agent.py
│   └── writer_agent.py
├── graph/
│   ├── state.py
│   └── workflow.py
├── utils/
│   └── file_extract.py
├── docs/
│   ├── architecture-diagram.md
│   ├── flow-diagram.md
│   └── state-diagram.md
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 🔧 Setup & Installation

> Make sure Python 3.10+ is installed, along with a free Groq API key from [console.groq.com](https://console.groq.com).

### Backend

```bash
# Clone the repo
git clone https://github.com/Muhammad-Ahmed-Rayyan/CareerCritic.git
cd CareerCritic

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install required libraries
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
```

### Frontend

```bash
# Run the Streamlit app
streamlit run app.py
```

Then in the browser:
1. Upload a resume (PDF, DOCX, or TXT)
2. Paste a job description
3. Click **Analyze Fit**
4. View the fit score, matched/missing skills, and detailed feedback report

---

## 🔑 API Configuration

Add your Groq API key to `.env`:

```.env
GROQ_API_KEY="YOUR-GROQ-API-KEY"
```

---

## 🏗️ Architecture

See [`docs/architecture-diagram.md`](docs/architecture-diagram.md) for the full system architecture, [`docs/flow-diagram.md`](docs/flow-diagram.md) for the process flow, and [`docs/state-diagram.md`](docs/state-diagram.md) for the state machine, including the Critic → JobFit revision loop.

---

<div align="center">

⭐ Found this project useful? Drop a star on GitHub!

</div>
