# Backend for Bottlenose Dolphins' Worldgate Track & Trace System

### Set-up Local Directories

Clone this repository or download the files to local directory.
Open a terminal session and navigate to this application root (`.../worldgate-track-trace/backend`)

```bash
cd /path/to/worldgate-track-trace/backend
```

### Virtual environment

Initialise python virtual environment. Make sure you're in the backend folder.

```bash
python -m venv <venvName>
source <venvName>/Scripts/activate
```

### Install Dependencies

Run 

```bash
# Run 'which pip' to ensure the pip you're using is the virtual env's, NOT your local machine's
pip install --upgrade pip
pip install -r requirements.txt
```
