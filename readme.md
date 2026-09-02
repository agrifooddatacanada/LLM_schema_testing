# Testing_LLM

## Setup

### 1. Verify Python Installation

Windows:

```powershell
python --version
```

Mac/Linux:

```bash
python3 --version
```

If Python is installed correctly, a version number should be displayed.

---

### 2. Create a Virtual Environment

Windows:

```powershell
python -m venv .venv
```

Mac/Linux:

```bash
python3 -m venv .venv
```

---

### 3. Activate the Virtual Environment

Windows:

```powershell
.venv\Scripts\activate
```

Mac/Linux:

```bash
source .venv/bin/activate
```

Your command prompt should now indicate that the virtual environment is active.

---

### 4. Install Dependencies

Windows:

```powershell
pip install -r requirements.txt
```

Mac/Linux:

```bash
pip3 install -r requirements.txt
```

---

### 5. Configure Environment Variables

Create a `.env` file from `.env.example` and populate the required values.

Example:

```text
ANTHROPIC_API_KEY=...
ANTHROPIC_BASE_URL=...
```

---

### 6. Run an Experiment

Windows:

```powershell
python -m evaluation.run_experiment
```

Mac/Linux:

```bash
python3 -m evaluation.run_experiment
```

Experiment outputs will be written to a timestamped directory under:

```text
evaluation/runs/
```

---

## Project Structure

```text
project/
│
├── data/
│   ├── input/
│   ├── intermediate/
│   └── output/
│
├── prompts/
│
├── evaluation/
│   ├── datasets/
│   ├── runs/
│   └── run_experiment.py
│
├── src/
│
├── .env.example
├── requirements.txt
└── README.md
```

---

## Approach

The complete project approach is documented in:

```text
approach.md
```

This document describes:

- architectural goals
- data models
- pipeline stages
- experiment framework
- future OCA-oriented workflows

It can be provided directly to an LLM as project context.

---

## Troubleshooting

### Recreate the Virtual Environment

If dependencies become corrupted or inconsistent:

Windows:

```powershell
rmdir /s /q .venv
python -m venv .venv
```

Mac/Linux:

```bash
rm -rf .venv
python3 -m venv .venv
```

Then reinstall:

```bash
pip install -r requirements.txt
```

or

```bash
pip3 install -r requirements.txt
```