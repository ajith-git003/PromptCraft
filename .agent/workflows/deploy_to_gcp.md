---
description: Deploy the backend via Google Cloud Run
---

# Deploy Backend to Google Cloud Run

This workflow will guide you through deploying your backend container to Google Cloud Run. This is a serverless option with a generous free tier.

## Prerequisites
1.  **Google Cloud Account**: You need an active Google Cloud account.
2.  **Project Created**: Create a new project in the Google Cloud Console (e.g., `promptcraft-backend`).
3.  **Billing Enabled**: Even for the free tier, you must enable billing on the project.
4.  **Google Cloud SDK**: You must have the `gcloud` CLI installed on your machine.

## Steps

1.  **Login to Google Cloud**
    Run this command in your terminal to authenticate:
    ```powershell
    gcloud auth login
    ```

2.  **Set the Project**
    Set your active project ID (replace `YOUR_PROJECT_ID` with your actual project ID from the console):
    ```powershell
    gcloud config set project YOUR_PROJECT_ID
    ```

3.  **Enable Required APIs**
    We need to enable the Artifact Registry and Cloud Run APIs:
    ```powershell
    gcloud services enable artifactregistry.googleapis.com run.googleapis.com cloudbuild.googleapis.com
    ```

4.  **Submit Build to Cloud Build**
    This builds your Docker container in the cloud so you don't need Docker locally.
    Navigate to the `backend` directory first:
    ```powershell
    cd backend
    ```
    Then run the build command (replace `promptcraft-repo` with a name for your repository if you haven't created one, or just let Cloud Build handle default storage if simpler, but `gcloud builds submit` is the standard way):
    
    *Simpler single-command deploy (builds and deploys):*
    ```powershell
    gcloud run deploy promptcraft-api --source . --region us-central1 --allow-unauthenticated
    ```
    *Note: When asked to enable APIs, say 'y'.*

5.  **Set Environment Variables**
    During deployment or after, you need to set your API Key.
    ```powershell
    gcloud run services update promptcraft-api --region us-central1 --set-env-vars GEMINI_API_KEY=YOUR_ACTUAL_API_KEY_HERE
    ```

6.  **Get the URL**
    The deployment command will output a Service URL (e.g., `https://promptcraft-api-xyz.a.run.app`). Copy this.

7.  **Update Frontend**
    Go to Vercel -> Settings -> Environment Variables.
    Update `REACT_APP_API_URL` with your new Cloud Run URL.
    Redeploy Vercel.

## Troubleshooting
-   If `gcloud` is not found, please install it from [Google Cloud SDK](https://cloud.google.com/sdk/docs/install).
-   If billing is not enabled, the deployment will fail.
