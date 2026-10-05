# Rule-Based AI Chatbot
> **Industrial Training Kit – Artificial Intelligence Project 1**  
> *A deterministic AI chatbot built using explicit rules, dictionary hash-maps, input sanitization, and control flow.*

---

## 1. Project Title
**Rule-Based AI Chatbot (Industrial Training Kit – AI Project 1)**

---

## 2. Project Objective
The primary objective of this project is to build and demonstrate a foundational, deterministic **Rule-Based Artificial Intelligence System**.

Unlike Generative AI systems (such as ChatGPT or LLMs) that generate probabilistic text from deep neural networks, this rule-based system demonstrates:
1. **Input Handling & Normalization**
2. **Input Sanitization** (case insensitivity, whitespace stripping, punctuation resilience)
3. **Deterministic Decision Making & Control Flow**
4. **Dictionary / Hash-Map Knowledge Base Lookup ($O(1)$ time complexity)**
5. **Robust Fallback Response Handling**
6. **Continuous Conversation Loop**
7. **Clean Exit Command Strategy**
8. **Transparent "Input $\to$ Logic $\to$ Output" Architecture**

---

## 3. Problem Statement
Many conversational systems fail or behave unpredictably due to lack of strict input sanitization, unhandled edge cases, or opaque generative hallucinations. Furthermore, understanding the fundamental mechanics of AI decision-making requires clear visibility into how inputs map to intents through deterministic control structures.

This project solves this by implementing an industrial-grade, transparent rule-based engine paired with both a continuous terminal interface and a modern, interactive web application with a **Live Developer Logic Inspector**.

---

## 4. Key Features
- ⚡ **100% Deterministic Engine**: Zero hallucination, zero reliance on external APIs, LLMs, or vector databases.
- 🧹 **Comprehensive Input Sanitization**: Normalizes cases, removes leading/trailing spaces, collapses internal whitespace, and strips trailing punctuation.
- 🗂️ **Multi-Intent Hash-Map Knowledge Base**: Predefined responses for over 10 distinct intent categories (greetings, identity, help, status, gratitude, time, project details, creator, goodbye).
- 🛡️ **Safe Fallback Response**: Employs dictionary `.get()` safe fallback handling without runtime exceptions or crashes.
- 🛑 **Clean Exit Strategy**: Graceful session termination triggered by explicit commands (`bye`, `goodbye`, `exit`, `quit`, `stop`).
- 🔄 **Continuous Chat Loop**: Implemented in both a standalone CLI (`while True:` loop) and a persistent stateful Web UI.
- 🔬 **Live Developer Logic Inspector**: A real-time visual inspection panel breaking down each transaction: `Raw Input` $\to$ `Sanitization` $\to$ `Intent/Rule Matching` $\to$ `Output Response` $\to$ `Execution Latency`.
- 🎨 **Modern Glassmorphic Web Interface**: Built with Vanilla CSS, responsive flexbox/grid layout, quick intent prompt chips, and an interactive Knowledge Base explorer modal.

---

## 5. Technologies Used
- **Programming Language**: Python 3.x
- **Backend Web Framework**: Flask
- **Frontend Stack**:
  - HTML5 (Semantic & Accessible)
  - Vanilla CSS3 (Custom Design System, Glassmorphism, CSS Variables, Responsive Animations)
  - JavaScript (Fetch API, DOM Manipulation, Live Sanitization Preview)
- **Testing**: Python `unittest` framework

---

## 6. System Architecture

```mermaid
graph TD
    A[User Input] --> B[Input Sanitization<br/>.lower().strip().rstrip(punctuation)]
    B --> C{Empty Input?}
    C -- Yes --> D[Guard Rail Response]
    C -- No --> E{Exit Command?<br/>'bye' / 'exit' / 'quit'}
    E -- Yes --> F[Polite Goodbye & Session Terminated]
    E -- No --> G{Direct Hash-Map Match?<br/>lookup.get(clean_input)}
    G -- Match Found --> H[Return Predefined Response & Intent]
    G -- No Match --> I{Secondary Keyword Rule Match?}
    I -- Match Found --> H
    I -- No Match --> J[Safe Fallback Response<br/>'I don't understand that yet. Try asking for help.']
    H --> K[Render Output & Update Logic Inspector]
    D --> K
    F --> K
    J --> K
```

---

## 7. How the Chatbot Works
1. **User Submits Input**: The user sends a message through the web form or terminal.
2. **Sanitization Phase**: The engine strips whitespace, converts all characters to lowercase, and strips trailing punctuation.
3. **Guard Rail Checks**: The engine checks if the input is blank.
4. **Exit Command Evaluation**: The engine tests if the input exists within the `EXIT_COMMANDS` set. If matched, it returns a farewell message and sets the session exit flag to `True`.
5. **Hash-Map Direct Lookup**: The engine performs an $O(1)$ search against the direct pattern dictionary.
6. **Rule-Based Keyword Matching**: If no exact match occurs, it scans intent patterns using whole-word boundary regular expressions.
7. **Fallback Response**: If no rule matches, the system safely falls back to a predefined guidance message.
8. **Live Telemetry & Render**: The final reply and metadata (sanitized string, matched rule, latency) are delivered to the UI.

---

## 8. Rule-Based Logic Explanation
Rule-Based AI uses explicit **if-then-else** decision rules and lookup tables rather than probabilistic weights. 

```python
# Conceptual Control Flow
if clean_input in exit_commands:
    terminate_session()
elif clean_input in lookup_table:
    return lookup_table[clean_input]
else:
    return fallback_response
```
This guarantees **predictability**, **auditability**, and **zero latency overhead**.

---

## 9. Dictionary / Hash-Map Explanation
A Python dictionary (`dict`) is implemented using a hash table. When a normalized user query is looked up:
1. Python computes `hash(clean_input)`.
2. The hash index directly locates the bucket containing the intent and predefined response.
3. This achieves **$O(1)$ Average Time Complexity**, meaning the lookup speed remains constant regardless of whether there are 10 or 10,000 rules.

Safe lookup is executed using `.get()`:
```python
direct_match = self.direct_lookup_map.get(clean_input)
```

---

## 10. Input Sanitization
Raw human input varies drastically in casing, whitespace, and punctuation. The sanitization method guarantees uniform representations:

```python
@staticmethod
def sanitize_input(raw_input: Optional[str]) -> str:
    if raw_input is None:
        return ""
    cleaned = str(raw_input).lower().strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = cleaned.rstrip(".?!,;:")
    return cleaned.strip()
```

| Raw Input | Sanitized Output | Match Result |
| :--- | :--- | :--- |
| `"HELLO"` | `"hello"` | Intent: `greeting` |
| `"  hi  "` | `"hi"` | Intent: `greeting` |
| `"What is your name???"` | `"what is your name"` | Intent: `name` |
| `"  QUIT.  "` | `"quit"` | Intent: `exit` |

---

## 11. Continuous Loop Concept
In the command-line interface (`chatbot.py`), the conversation continues indefinitely using a `while True:` loop until an explicit exit command breaks the loop:

```python
while True:
    user_input = input("User: ")
    result = self.get_response(user_input)
    print(f"Bot:  {result['response']}\n")
    if result["is_exit"]:
        break
```

In the Web UI, persistence is maintained through client-side state and asynchronous REST API transactions.

---

## 12. Exit Strategy
The chatbot supports clean, deliberate session termination.
- **Commands**: `bye`, `goodbye`, `exit`, `quit`, `close`, `terminate`, `stop`.
- **Action**:
  - Displays: `"Goodbye! Have a great day! Session has been terminated."`
  - In CLI: Breaks out of the loop and exits cleanly.
  - In Web UI: Disables the text input, displays a clean session-ended banner, and reveals a "Restart Conversation" button.

---

## 13. Fallback Mechanism
When an input does not match any recognized rule or pattern (e.g., `"xyzabc"` or `"random query"`), the bot does not crash or throw exceptions. Instead, it deterministically responds with:

> *"I don't understand that yet. Try asking for help."*

This informs the user of available assistance while maintaining system stability.

---

## 14. Project Structure
```text
ai/
│
├── app.py                  # Flask Web Server & REST API endpoints (/api/chat, /api/intents, /api/reset)
├── chatbot.py              # Core Rule-Based AI Engine & standalone CLI loop
├── test_chatbot.py         # Automated unit test suite (12 comprehensive test cases)
├── requirements.txt        # Python dependency manifest (Flask, Werkzeug)
├── README.md               # Complete project documentation & PPT alignment
│
├── templates/
│   └── index.html          # Web UI layout, Developer Inspector Drawer, Knowledge Base Modal
│
└── static/
    ├── style.css           # Modern Dark Glassmorphic Design System
    └── script.js           # Client controller, live sanitization preview, REST handlers
```

---

## 15. Installation Instructions

### Prerequisites
- Python 3.8 or higher installed on your operating system.

### Step 1: Open Terminal in Project Root
```bash
cd "c:\Users\Abhilash\OneDrive\Desktop\ai"
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 16. How to Run the Project

### Option A: Run Interactive Web Application (Recommended for Evaluation)
```bash
python app.py
```
Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

### Option B: Run Standalone Command-Line (CLI) Loop
```bash
python chatbot.py
```

### Option C: Run Automated Unit Tests
```bash
python test_chatbot.py
```

---

## 17. Sample Conversations

### Interaction 1: Greetings & Sanitization
```text
User:   HELLO
Bot:  Hello! How can I help you today?
```

### Interaction 2: Identity & Help
```text
User: what is your name
Bot:  I am a Rule-Based AI Chatbot, built using deterministic logic and control flow.

User: help
Bot:  I can respond to predefined commands such as greetings, identity, status, project info, help, and goodbye.
```

### Interaction 3: Status & Gratitude
```text
User: how are you
Bot:  I'm doing great! Everything in my rule engine is running smoothly. Thanks for asking!

User: thank you
Bot:  You're very welcome! I'm happy to assist you.
```

### Interaction 4: Fallback Handling
```text
User: xyzabc123
Bot:  I don't understand that yet. Try asking for help.
```

### Interaction 5: Clean Exit
```text
User: bye
Bot:  Goodbye! Have a great day! Session has been terminated.
[Session Terminated Cleanly]
```

---

## 18. Limitations of Rule-Based AI
1. **No Out-of-Vocabulary Generalization**: Queries not defined in the knowledge base will trigger the fallback response.
2. **Context Blindness**: Does not maintain long multi-turn semantic memory without explicit state machines.
3. **Manual Knowledge Base Maintenance**: Every new intent must be explicitly codified in the dictionary.

---

## 19. Future Improvements
1. **Fuzzy String Matching**: Integrating Levenshtein distance matching for minor spelling mistakes (e.g. `"helo"` $\to$ `"hello"`).
2. **Contextual State Machines**: Adding multi-step slot filling (e.g., booking forms, multi-step customer support).
3. **Synonym Expansion via Thesaurus Lookups**: Augmenting the pattern dictionaries automatically using deterministic linguistic dictionaries.

---

## 20. Key Presentation Points for Viva / Evaluation
When presenting this project to your evaluator, highlight these 5 core aspects:
1. **Zero Hallucination / Deterministic AI**: Explain why this is not generative AI and how predictability is crucial in safety-critical automated rule systems.
2. **Input Sanitization Pipeline**: Show how `"  HELLO!  "` is transformed into `"hello"`.
3. **$O(1)$ Hash Map Lookup**: Demonstrate the dictionary `.get()` lookup speed (displayed live in the Developer Inspector as $<1$ ms).
4. **Graceful Fallback & Exit**: Demonstrate `"xyzabc"` triggering the fallback and `"bye"` terminating the session.
5. **Live Logic Inspector**: Use the side panel during live interaction to prove the transparent step-by-step pipeline.
