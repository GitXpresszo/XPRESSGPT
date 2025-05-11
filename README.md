---
title: AmeyaGPT
emoji: 🚀
colorFrom: red
colorTo: red
sdk: docker
sdk_version: "1.0"
app_file: src/streamlit_app.py
pinned: false
license: apache-2.0
---

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>AmeyaGPT</title>
</head>
<body>

<h1>🚀 AmeyaGPT</h1>

<p><strong>AmeyaGPT</strong> is an advanced AI chatbot built with <strong>Streamlit</strong>, Dockerized for easy deployment, and equipped with <strong>memory</strong> and <strong>internet access</strong>. It is designed to deliver intelligent conversations, contextual memory, and up-to-date information retrieval.</p>

<hr>

<h2>🔧 Features</h2>
<ul>
  <li>💬 <strong>Conversational AI</strong> with persistent memory</li>
  <li>🌐 <strong>Internet access</strong> for real-time data retrieval</li>
  <li>🧠 <strong>RAG-ready</strong>: Retrieval-Augmented Generation support</li>
  <li>🐳 <strong>Docker-based</strong> deployment for portability</li>
  <li>📊 Built with <strong>Streamlit</strong> for rapid UI development</li>
  <li>🔐 Secure .env-based API key management</li>
</ul>

<hr>

<h2>🗂 Project Structure</h2>
<pre>
.
├── Dockerfile
├── requirements.txt
├── README.md
└── src
    └── streamlit_app.py
</pre>

<hr>

<h2>🚀 Getting Started</h2>

<h3>1. Clone the Repository</h3>
<pre><code>git clone https://github.com/your-username/AmeyaGPT.git
cd AmeyaGPT
</code></pre>

<h3>2. Add Environment Variables</h3>
<p>Create a <code>.env</code> file in the root directory:</p>
<pre><code>API_KEY=your_api_key_here
SEARCH_ENDPOINT=your_search_endpoint
</code></pre>

<h3>3. Build the Docker Image</h3>
<pre><code>docker build -t ameyagpt .
</code></pre>

<h3>4. Run the App</h3>
<pre><code>docker run -p 8501:8501 --env-file .env ameyagpt
</code></pre>
<p>Then open your browser at <a href="http://localhost:8501">http://localhost:8501</a>.</p>

<hr>

<h2>📦 Dependencies</h2>
<ul>
  <li><code>streamlit</code></li>
  <li><code>requests</code></li>
  <li><code>openai</code> or <code>google-generativeai</code></li>
  <li><code>python-dotenv</code></li>
  <li><code>langchain</code> (optional)</li>
</ul>

<p>Install all dependencies via:</p>
<pre><code>pip install -r requirements.txt
</code></pre>

<hr>

<h2>📚 Customization</h2>
<p>Edit the main file:</p>
<pre><code>/src/streamlit_app.py
</code></pre>

<p>Update components like:</p>
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
<p>Pull requests are welcome. For major changes, open an issue first to discuss what you'd like to change.</p>

<hr>

<h2>🙋‍♂️ Questions?</h2>
<p>Check out <a href="https://docs.streamlit.io">Streamlit Docs</a> or open an issue on this repo.</p>

</body>
</html>
