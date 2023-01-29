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

# activate virtual environment
source <venvName>/Scripts/activate
```

### Provide Environment Variables

This backend application relies on a remote Oracle server for data persistence. We need to provide it with the following information. Edit the `.env-example` using any text editor (`vi .env.example`).

1. Replace `<>` fields with the respective information
2. Rename `.env.example` to `.env`

```bash
# Clone into a .env file
PYTHONPATH="${PYTHONPATH}:." # DO NOT CHANGE THIS
SQLALCHEMY_DATABASE_URI=<DB URI>
JWT_SECRET=<JWT_SECRET_KEY>
```

### Install Dependencies

Run 

```bash
# Run 'which pip' to ensure the pip you're using is the virtual env's, NOT your local machine's
pip install --upgrade pip
pip install -r requirements.txt
```

NOTE: each time you pip install a new library/package that is utilised in committed code, you need to update requirements.txt file. To do so, run the following command (make sure you're in the backend folder):

```bash
pip freeze > requirements.txt
```

### Authentication Notes

#### BE:
In `user.py`:
1. Sign In endpoint: Returns response with 2 cookies, `access_token_cookie` (containing the JWT) and `csrf_access_token` (containing the double-submit token)
2. `refresh_expiring_jwt` function, called after every request to refresh near-expiry access tokens
3. `verify_jwt_csrf_validity` function to be called at start of ALL PROTECTED BE API ENDPOINTS. This function also extracts username of jwt owner. For now, it returns a Python dictionary (to be refactored to return a JSON response if microservice architecture dictates so)

#### FE:
For all Axios requests to protected BE API endpoints: 
1. `withCredentials` must be set to `true`. This is to ensure cookies are attached to the request and sent to the backend.
2. Include `X-CSRF-TOKEN` header, pointing to value of `csrf_access_token`. (See`src/api/config.js` for usage example )

In `src/api/config.js`:
`getCookie` function to extract csrf_access_token from cookie, to be attached in X-CSRF-TOKEN header for every request to a protected BE API endpoint.
