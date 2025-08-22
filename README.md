📝 Blog Generator Agent
<p align="center"> <img src="https://img.shields.io/badge/AI-Agentic-blue?logo=openai&logoColor=white" alt="Agentic AI"/> <img src="https://img.shields.io/badge/Framework-LangGraph-green" alt="LangGraph"/> <img src="https://img.shields.io/badge/UI-Streamlit-orange" alt="Streamlit"/> <img src="https://img.shields.io/badge/Blogs-MultiLanguage-purple" alt="Multi Language"/> </p>

An Agentic AI-powered Blog Generator ⚡ that creates high-quality blogs in multiple languages using LangGraph and LLMs.
Perfect for developers, writers, and creators who want to scale content effortlessly.

✨ Features

🤖 Agentic AI → Uses LangGraph to orchestrate multi-step reasoning

🌍 Multilingual Blog Generation → Generate blogs in English, Hindi, Spanish, French, German, and more

🧩 Flexible Prompts → Customize tone, style, and length of blogs

📝 Topic-Aware → Generates domain-specific blogs (tech, business, lifestyle, etc.)

⚡ Streamlit UI → Interactive, user-friendly interface

🛠️ Extensible → Add new languages, tones, or tools easily

🏗️ Architecture

flowchart TD
    U[🧑 User] -->|Enter Topic & Language| UI[💻 Streamlit UI]
    UI --> AG[🤖 Blog Generator Agent - LangGraph]
    AG --> LLM[🔮 LLMs (OpenAI / Anthropic / LLaMA)]
    AG --> TOOLS[🔧 Translation & Formatting Tools]
    LLM --> AG
    TOOLS --> AG
    AG --> UI
    UI -->|Generated Blog| U

🚀 Tech Stack

LangGraph → For building agentic workflows

LLMs → OpenAI GPT / Anthropic Claude / LLaMA

UI → Streamlit

LangChain Tools → Translation & formatting utilities

Deployment → Streamlit Cloud / Vercel / Docker

⚙️ Installation
1️⃣ Clone the repo
git clone https://github.com/your-username/blog-generator-agent.git
cd blog-generator-agent

2️⃣ Setup environment
python -m venv venv
source venv/bin/activate   # On Windows use venv\Scripts\activate
pip install -r requirements.txt

3️⃣ Add environment variables

Create a .env file:

OPENAI_API_KEY=your_openai_key

4️⃣ Run the app
streamlit run app.py

📂 Project Structure
blog-generator-agent/
│── src/
│   ├── agents/          # LangGraph agent logic
│   ├── prompts/         # Prompt templates
│   ├── utils/           # Helper functions
│   └── ui/              # Streamlit UI
│── app.py               # Entry point for Streamlit app
│── requirements.txt     # Dependencies
│── .env.example         # Example environment variables
│── README.md            # Project documentation

🌍 Example Usage

Input:

Topic → "The Future of Electric Vehicles"

Language → "Spanish"

Tone → "Professional"

Generated Blog (Excerpt):

"El futuro de los vehículos eléctricos se perfila como una de las mayores revoluciones tecnológicas y medioambientales de nuestro tiempo. Desde la reducción de emisiones hasta la integración con energías renovables..."

📸 Screenshots
<p align="center"> <img src="https://github.com/your-username/blog-generator-agent/assets/demo-ui.png" width="700"/> </p>
🛠️ Future Roadmap

🔮 Support for voice-to-blog

🔮 Integration with Notion/Medium APIs for auto-publishing

🔮 SEO-optimized content generation

🔮 Rich editor for formatting blogs

🤝 Contributing

Fork the repository

Create a new branch (git checkout -b feature/amazing-feature)

Commit your changes (git commit -m 'Add amazing feature')

Push to the branch (git push origin feature/amazing-feature)

Open a Pull Request

📜 License

This project is licensed under the MIT License.

⭐ Support

If you find this project useful, please give it a star ⭐ on GitHub — it motivates me to build more!