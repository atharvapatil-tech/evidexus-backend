# Evidexus Mobile MVP Backend

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## 🚀 How to Deploy to the Cloud (No Coding Required)

You can deploy this API to the internet for free using **Render**. This will give you a public URL (like `https://evidexus-backend-xyz.onrender.com`) that your mobile app can connect to securely.

### Step 1: Upload this codebase to GitHub
1. Go to [GitHub.com](https://github.com/) and log in (or create a free account).
2. Click the **"+"** icon in the top right and select **"New repository"**. Name it `evidexus-backend`. Make it **Private**.
3. Once created, click "uploading an existing file" on the repository page. 
4. Drag and drop all the files from this `evidexus-backend` folder into GitHub and click **Commit changes**.

### Step 2: One-Click Deploy
1. Click the **"Deploy to Render"** purple button at the very top of this README.
2. Render will ask you to log in (you can use your GitHub account).
3. It will automatically detect your `evidexus-backend` repository. You just need to fill in one value:
   - **`OPENAI_API_KEY`**: Paste your OpenAI API Key here so the AI engine works.
4. Click **Apply** or **Deploy**.

*And that's it!* Render will take about 2-3 minutes to physically build your cloud server. 
Once it finishes, it will give you a live URL in the top left corner (e.g., `https://evidexus-backend...onrender.com`).

**Your Mobile App URL:**
Whenever your mobile app wants to make a request, it should now target:
`POST https://<YOUR_RENDER_URL>/api/v1/ask-clinical-question`


---

## Project Structure (For Developers)

```text
evidexus-backend/
├── app/
│   ├── main.py                # Gateway, Auth, Logging, CORS, Rate-limiting
│   ├── api/
│   │   └── endpoints.py       # Unified router orchestrator
│   ├── models/
│   │   └── schemas.py         # Sub-schemas embedded within the polymorphic wrapper
│   ├── services/
│   │   ├── evidence_retrieval.py # Cached PubMed API
│   │   └── ai_reasoning.py       # GPT-4 Intent classification and RAG
│   ├── core/
│   │   └── config.py
├── .dockerignore
├── render.yaml                # Render Blueprint setup
├── Dockerfile                 # Production Container Deploy
├── requirements.txt
├── .env.example
└── README.md
```

## Running Locally

**Install:**
```bash
python -m venv venv
# Activate windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

**Environment Variables (.env):**
```env
OPENAI_API_KEY=your_key_here
API_KEY=evidexus_mobile_dev_key
```

**Start the Server:**
```bash
uvicorn app.main:app --reload
```
