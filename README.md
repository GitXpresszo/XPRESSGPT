---
title: AIGPT
emoji: 🚀
colorFrom: green
colorTo: green
sdk: docker
sdk_version: '1.0'
app_file: src/app.py
pinned: false
license: apache-2.0
thumbnail: >-
  https://cdn-uploads.huggingface.co/production/uploads/670002ccfed8e4934cebc4b7/r20juvXt8PiTX9S4JEX7G.png
short_description: AI chatbot with memory, internet access, and agents
---

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
</head>
<body>

<h1>🚀 AIGPT</h1>

<p><strong>AIGPT</strong> is an AI chatbot built with <strong>Streamlit</strong>, Dockerized for easy deployment, and equipped with <strong>memory</strong> and <strong>internet access</strong>. It is designed to deliver intelligent conversations, contextual memory, and up-to-date information retrieval.</p>

<hr>

<h2>👋 About the Creator</h2>
<p>Hi, I'm <strong>Ameya</strong> — the developer behind AIGPT. I'm passionate about building intelligent systems and practical GenAI applications. Feel free to connect with me on <a href="https://www.linkedin.com/in/ameyasutar/" target="_blank">LinkedIn</a> for collaborations, feedback, or future projects!</p>

<hr>

<h2>🔧 Features</h2>
<ul>
  <li>💬 <strong>Conversational AI</strong> with persistent memory</li>
  <li>🌐 <strong>Internet access</strong> for real-time data retrieval</li>
  <li>🧠 <strong>Agentic Approach</strong>: Implements the LangChain ReAct framework</li>
  <li>🐳 <strong>Docker-based</strong> deployment for portability</li>
  <li>📊 Built with <strong>Streamlit</strong> for rapid UI development</li>
</ul>

<hr>

<h2>🗂 Project Structure</h2>
<pre>
.
├── Dockerfile
├── requirements.txt
├── README.md
└── src
    └── app.py
</pre>

<hr>

<h2>🚀 Getting Started</h2>

<h3>1. Clone the Repository</h3>
<pre><code>git clone https://huggingface.co/spaces/DevAmeya/AIGPT</code></pre>

<h3>2. Add Environment Variables</h3>
<p>Create a <code>.env</code> file in the root directory:</p>
<pre><code>
GOOGLE_API_KEY=your_api_key_here
TAVILY_API_KEY=your_search_endpoint
</code></pre>

<h3>3. Build the Docker Image</h3>
<pre><code>docker build -t aigpt .</code></pre>

<h3>4. Run the App</h3>
<pre><code>docker run -p 8501:8501 --env-file .env aigpt</code></pre>

<p>Then open your browser at <a href="http://localhost:8501" target="_blank">http://localhost:8501</a>.</p>

<hr>

<h2>📦 Dependencies</h2>
<ul>
  <li><code>altair</code></li>
  <li><code>pandas</code></li>
  <li><code>google-generativeai</code></li>
  <li><code>python-dotenv</code></li>
  <li><code>streamlit</code></li>
  <li><code>streamlit-authenticator==0.2.3</code></li>
  <li><code>PyYAML</code></li>
  <li><code>bcrypt</code></li>
  <li><code>langchain_google_genai</code></li>
  <li><code>langchain</code></li>
  <li><code>langchain-community</code></li>
  <li><code>duckduckgo-search</code></li>
  <li><code>langchain-tavily</code></li>
</ul>

<p>Install all dependencies via:</p>
<pre><code>pip install -r requirements.txt</code></pre>

<hr>

<h2>📚 Customization</h2>
<p>Edit the main file:</p>
<pre><code>/src/app.py</code></pre>

<p>You can customize:</p>
<ul>
  <li>Model backend (OpenAI, Gemini, Ollama, etc.)</li>
  <li>Memory module (LangChain, custom DB, ChromaDB, etc.)</li>
  <li>Retrieval logic (API search, vector DB, web scraping)</li>
</ul>

<hr>

<h2>📄 License</h2>
<p>This project is licensed under the <a href="LICENSE">Apache 2.0 License</a>.</p>

<hr>

<h2>🤝 Contributing</h2>
<p>Pull requests are welcome. For major changes, please open an issue first to discuss your proposal.</p>

<hr>

<h2>🙋‍♂️ Questions?</h2>
<p>Check out the <a href="https://docs.streamlit.io" target="_blank">Streamlit Docs</a> or raise an issue on this repository.</p>

</body>
</html>