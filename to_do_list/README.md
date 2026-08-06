 # 📝 Tkinter To-Do List Application

A sleek, lightweight desktop To-Do List application built with Python's native **Tkinter** library. Designed with a clean GUI, local JSON persistence, and keyboard shortcuts, this app helps you manage daily tasks seamlessly without any external dependencies.

---

## ✨ Features

- **Modern & Clean UI**: Styled with `ttk` elements, custom typography (Segoe UI), and a responsive layout.
- **Persistent Data**: Tasks are automatically saved to a local `tasks.json` file so your list persists across app launches.
- **Full CRUD Functionality**:
  - ➕ **Add Task**: Fast entry box with `<Return>` key support.
  - ✎ **Edit Task**: Update existing task descriptions via dialog.
  - ✔ **Mark Done**: Toggle completion status with a single click or double-clicking the item.
  - 🗑 **Delete Task**: Remove individual tasks with confirmation prompts.
  - 🧹 **Clear Completed**: Bulk remove all finished tasks in one click.
- **Dynamic Status Bar**: Real-time counter showing completed vs. total tasks.
- **Task Metadata**: Tracks creation timestamp for every added item.

---

## 🛠 Tech Stack & Requirements

- **Language**: Python 3.145
- **GUI Framework**: Tkinter (Included with standard Python installations)
- **Data Format**: JSON (`json` module)

> **Note for Linux Users**: If Tkinter is not pre-installed on your Linux distribution, install it via:
> ```bash
> sudo apt-get install python3-tk
> ```

---

## 🚀 Getting Started

### 1. Installation
No `pip install` required! Simply clone or download this repository to your local machine.

```bash
git clone https://github.com/your-username/tkinter-todo-app.git
cd tkinter-todo-app
```

### 2. Running the Application
Execute the Python script directly:

```bash
python main.py
```

---

## 📁 File Structure

```text
.
├── main.py          # Main application source code
├── tasks.json       # Local task database (auto-generated on first save)
└── README.md        # Project documentation
```

---

## 💻 How It Works

1. **Initialization (`TodoApp.__init__`)**: Configures the main Tkinter window, applies styling, builds the UI components, and loads existing tasks from `tasks.json`.
2. **Data Operations**:
   - `load_tasks()`: Safely reads `tasks.json`. Handles missing or corrupted files gracefully.
   - `save_tasks()`: Serializes task list into JSON format.
3. **Interactive UI**:
   - Lists tasks with `[ ]` (pending) or `[x]` (completed) prefixes.
   - Completed tasks are visually greyed out for visual contrast.

---

## 📄 Data Format (`tasks.json`)

Tasks are stored as an array of JSON objects:

```json
[
  {
    "text": "Complete Python project documentation",
    "done": false,
    "created": "2026-08-06 14:30"
  },
  {
    "text": "Review pull requests",
    "done": true,
    "created": "2026-08-06 10:15"
  }
]
```

---

