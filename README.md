# AIProductManager

**AIProductManager** is an AI-powered assistant for product management teams, designed to streamline and augment key workflows such as feature prioritization, backlog grooming, intelligent task suggestion, and team insights. Harnessing advanced language models (LLMs), it brings chain-of-thought reasoning and contextual retrieval to accelerate agile processes and decision-making.

---

## Features

- **Feature Prioritization:**  
  Analyze a list of proposed features and receive prioritized recommendations with clear justifications, tailored to your project context.

- **Backlog Grooming:**  
  Group related tickets, suggest improvements, and summarize your backlog efficiently.

- **Intelligent Task Suggester:**  
  Get actionable new tasks or improvements based on your current backlog and project context.

- **Team Insights:**  
  Summarize team progress, identify risks, and highlight blockers from activity logs.

- **Context-Aware Reasoning:**  
  Uses retrieval augmented generation (RAG) and persistent memory to provide answers rooted in your product's unique context.

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Ohmdatazwld5/AIProductManager.git
cd AIProductManager
```

### 2. Set Up Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in your project root with your API keys (e.g. for Groq LLM):

```
GROQ_API_KEY=your-actual-groq-api-key
```

> **Tip:** Never commit your `.env` file to version control.

### 5. Run the Application

If your main API is in `app/api.py`, use:

```bash
uvicorn app.api:app --reload
```

Or adapt the entry point as needed.

---

## Project Structure

```
AIProductManager/
│
├── app/
│   ├── api.py                # Main API entry point (FastAPI)
│   ├── agent_orchestration.py# Core orchestration logic
│   ├── memory.py             # Memory/context management
│   ├── rag.py                # Retrieval-augmented generation helpers
│   └── ...
├── requirements.txt
├── .env                      # Environment variables (not in repo)
├── README.md
└── ...
```

---

## Contributing

Contributions are welcome! Open an issue or submit a pull request for improvements, bugfixes, or feature suggestions.

---

## License

Distributed under the MIT License.

---

## Contact

Questions or suggestions?  
Open an issue or reach out to [Ohmdatazwld5](https://github.com/Ohmdatazwld5).
