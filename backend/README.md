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

### Provide Environment Variables

This backend application relies on a remote Oracle server for data persistence. We need to provide it with the following information. Edit the `.env-example` using any text editor (`vi .env.example`).

1. Replace `<>` fields with the respective information
2. Rename `.env.example` to `.env`

```bash
# Clone into a .env file
SQLALCHEMY_DATABASE_URI=<DB URI>
```

### Install Dependencies

Run 

```bash
# Run 'which pip' to ensure the pip you're using is the virtual env's, NOT your local machine's
pip install --upgrade pip
pip install -r requirements.txt
```

NOTE: each time you pip install a new library/package that is utilised in committed code, run the following command (make sure you're in the backend folder):

```bash
pip freeze > requirements.txt
```
