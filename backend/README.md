# Setup Instructions

1. In the `backend/` directory, create a python virtual environment and activate it.

```bash
python -m venv .venv
. .venv\Scripts\activate # The .venv activation command might differ depending on your operating system
```

2. Install the required packages.

```bash
pip install -r requirements.txt
```

3. Set up Environment Variables

Create a `.env` file in the `backend/` directory with all the environment variables listed in the `.env.example`.

```env
# .env file with all your environment variables

HUGGINGFACE_TOKEN=
GOOGLE_API_KEY=
PRODUCTION_CLIENT_URL=
```

4. In the `/app` directory, start the application.

```bash
cd app
uvicorn main:app --reload
```

And you are ready to start using the Backend! The server application is running on http://127.0.0.1:8000/

**Script for quick startup:**

```bash
cd backend
. .venv/Scripts/activate
cd app
uvicorn main:app --reload
```

# Deployment (Docker + Google Cloud Run)

**1. Build Docker Image**

In the root directory:

```bash
docker build -t tohjingqiang/aisl-backend:1.0.0 .
```

**2. Login into Docker Hub**

```bash
docker login
```

**3. Push Image to Docker Hub**

```bash
docker push tohjingqiang/aisl-backend:1.0.0
```

**4. Reload Repository Page on DockerHub**

**5. Go to Google Cloud Run, login using the AiSL admin gmail, and add/edit the `aisl-backend` service.**

**6. Click on `Edit & Deploy New Revision` and update the container image url to the new version before clicking on the `Deploy` button.**

\*Please add any new environment variables to the Cloud Run service before deploying.
