# Deploy to Google Cloud Run

$PROJECT_ID = "ai-prompt-studio-481313"
$REGION = "us-central1"
$SERVICE_NAME = "promptcraft-api"
$REPO_NAME = "promptcraft-repo"

# 1. Set Project
gcloud config set project $PROJECT_ID

# 2. Enable APIs
gwmi -List | Out-Null # Hack to pause if needed, or just run commands
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com

# 3. Create Artifact Repository (if not exists)
# We use 'try/catch' logic by just ignoring error if it exists
gcloud artifacts repositories create $REPO_NAME --repository-format=docker --location=$REGION --description="Docker repo"

# 4. Build and Submit Container
gcloud builds submit --tag "$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$SERVICE_NAME" ../backend

# 5. Deploy to Cloud Run
gcloud run deploy $SERVICE_NAME `
  --image "$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$SERVICE_NAME" `
  --region $REGION `
  --allow-unauthenticated `
  --set-env-vars GEMINI_API_KEY=$env:GEMINI_API_KEY
