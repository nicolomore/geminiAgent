# 🤖 AgenteV2: Your Ultimate System Co-Pilot

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Powered by Gemini](https://img.shields.io/badge/AI-Gemini%20Flash-orange.svg)](https://deepmind.google/technologies/gemini/)
[![TUI](https://img.shields.io/badge/Interface-Textual%20TUI-green.svg)](https://textual.textualize.io/)

> **AgenteV2** isn't just another chatbot. It’s an autonomous entity living in your terminal, capable of interacting directly with your Linux OS, analyzing code, managing your agenda, and even talking back to you in real-time.

---

## 🚀 Why AgenteV2?

Stop copying and pasting commands from a browser to your terminal. **AgenteV2** is an advanced AI agent that "thinks" and "executes." By bridging the gap between Google's Gemini API and deep system-level integration, it transforms your terminal into a proactive workspace.

### ✨ Key Features

- **🖥️ Sophisticated TUI:** A sleek terminal user interface built with `Textual`, featuring smooth scrolling, markdown rendering, and real-time tool-call visualization.
- **🎙️ Live Audio Mode:** A futuristic interface for voice interaction using Gemini’s _Native Audio_ models for ultra-low latency and natural-sounding vocal responses.
- **🛠️ System Arsenal:**
  - **File System Mastery:** Create, read, move, and find files or directories. Generate directory trees on the fly.
  - **SysAdmin Capabilities:** Execute shell commands, monitor system info, and handle file backups/restores.
  - **Developer Suite:** Deep-dive into Python projects using AST (Abstract Syntax Tree) analysis, check syntax, run tests, and apply surgical code fixes.
- **🌐 Web & Media Integration:**
  - **Advanced Search:** Powered by Google Search, it scrapes and converts web content into clean, readable markdown.
  - **YouTube Downloader:** Download video or audio streams directly via CLI commands.
- **📧 Communication & Plugins:**
  - **Telegram:** Integrated plugin to send messages and files through a dedicated bot.
  - **Email:** Built-in Gmail support for sending professional messages.
- **🧠 Long-Term Memory:** A persistent memory and task-management system that ensures the agent remembers your preferences and pending tasks across sessions.

---

## 🛠️ Tech Stack

- **Core:** Python 3.x
- **AI Model:** Google Gemini (1.5 Flash / 2.0 Flash Native Audio)
- **UI Framework:** Textual (TUI)
- **Audio:** PyAudio for real-time streaming
- **OS:** Optimized for **Linux** environments

---

## ⚙️ Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/agenteV2.git
   cd agenteV2
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Keys:**
   Create a `.env` file in the root directory and add your credentials:
   ```env
   GOOGLE_API_KEY=your_gemini_key
   SERPAPI_KEY=your_serpapi_key
   TELEGRAM_TOKEN=your_bot_token (optional)
   ```

---

## 🎮 Usage

### Graphical TUI Mode

Launch the main interactive terminal interface:

```bash
python gui.py
```

_Ask the agent complex tasks like: "Analyze file X and fix the bugs," or "Search Google for the latest Python 3.13 features and summarize them."_

### Voice/Audio Mode

Talk directly to your agent:

```bash
python audioMode.py
```

---

## 🧩 Plugin Architecture

AgenteV2 is modular by design. You can easily extend its capabilities by adding new tools to the `plugins/` directory. The agent automatically detects new tools and learns how to utilize them when relevant.

---

## 🤝 Contributing

Pull requests are welcome! If you have ideas for new plugins, TUI improvements, or better system integration, feel free to open an issue or start a discussion.

---

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

_Built with ❤️ for Terminal Power Users._
