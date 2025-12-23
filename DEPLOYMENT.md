# 🚀 Deployment Guide - ERNIE FinSight

Guide complet pour déployer votre application en production.

## 📋 Architecture de Déploiement

- **Frontend**: Vercel ou Netlify (gratuit)
- **Backend**: Render, Railway, ou Fly.io (gratuit avec limitations)

---

## 🎯 Option 1: Vercel (Frontend) + Render (Backend) - RECOMMANDÉ

### Frontend sur Vercel

#### 1. Préparer le Frontend

Créez `frontend/vercel.json`:

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://votre-backend.onrender.com/api/:path*"
    }
  ]
}
```

Créez `frontend/.env.production`:

```bash
VITE_API_URL=https://votre-backend.onrender.com
```

#### 2. Déployer sur Vercel

**Via CLI:**

```bash
cd frontend
npm install -g vercel
vercel login
vercel --prod
```

**Via Dashboard:**

1. Allez sur [vercel.com](https://vercel.com)
2. Connectez votre repository GitHub
3. Sélectionnez le dossier `frontend`
4. Configurez:
   - Framework Preset: Vite
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Root Directory: `frontend`
5. Ajoutez la variable d'environnement:
   - `VITE_API_URL`: URL de votre backend
6. Deploy!

### Backend sur Render

#### 1. Préparer le Backend

Créez `backend/render.yaml`:

```yaml
services:
  - type: web
    name: ernie-finsight-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: NOVITA_API_KEY
        sync: false
      - key: MAX_FILE_SIZE_MB
        value: 10
      - key: UPLOAD_DIR
        value: ./uploads
    healthCheckPath: /api/health
```

Mettez à jour `backend/requirements.txt` si nécessaire:

```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-multipart==0.0.6
pydantic==2.5.3
pydantic-settings==2.1.0
openai>=1.30.0
pypdf2==3.0.1
pdfplumber==0.10.3
python-dotenv==1.0.0
aiofiles==23.2.1
```

#### 2. Déployer sur Render

1. Allez sur [render.com](https://render.com)
2. Connectez votre repository GitHub
3. Créez un nouveau "Web Service"
4. Configurez:
   - Name: `ernie-finsight-api`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Root Directory: `backend`
5. Ajoutez les variables d'environnement:
   - `NOVITA_API_KEY`: votre clé API
   - `MAX_FILE_SIZE_MB`: `10`
   - `UPLOAD_DIR`: `./uploads`
6. Deploy!

#### 3. Tester

Votre backend sera disponible à: `https://ernie-finsight-api.onrender.com`

Test:

```bash
curl https://ernie-finsight-api.onrender.com/api/health
```

---

## 🎯 Option 2: Netlify (Frontend) + Railway (Backend)

### Frontend sur Netlify

#### 1. Préparer le Frontend

Créez `frontend/netlify.toml`:

```toml
[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/api/*"
  to = "https://votre-backend.railway.app/api/:splat"
  status = 200
  force = true

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

#### 2. Déployer sur Netlify

**Via CLI:**

```bash
cd frontend
npm install -g netlify-cli
netlify login
netlify deploy --prod
```

**Via Dashboard:**

1. Allez sur [netlify.com](https://netlify.com)
2. Connectez votre repository GitHub
3. Configurez:
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `frontend/dist`
4. Ajoutez la variable: `VITE_API_URL`
5. Deploy!

### Backend sur Railway

#### 1. Préparer le Backend

Créez `backend/Procfile`:

```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

Créez `backend/railway.json`:

```json
{
  "build": {
    "builder": "nixpacks"
  },
  "deploy": {
    "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/api/health",
    "restartPolicyType": "on_failure"
  }
}
```

#### 2. Déployer sur Railway

1. Allez sur [railway.app](https://railway.app)
2. Connectez votre repository GitHub
3. Créez un nouveau projet
4. Sélectionnez le dossier `backend`
5. Ajoutez les variables d'environnement:
   - `NOVITA_API_KEY`
   - `MAX_FILE_SIZE_MB`
   - `UPLOAD_DIR`
6. Deploy!

---

## 🎯 Option 3: Tout sur Vercel (Serverless)

⚠️ **Note**: Nécessite une restructuration du backend en serverless functions.

### Restructurer le Backend

Créez `api/analyze.py`:

```python
from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

# Vos endpoints ici

handler = Mangum(app)
```

Créez `vercel.json` à la racine:

```json
{
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "dist"
      }
    },
    {
      "src": "api/*.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "api/$1.py"
    },
    {
      "src": "/(.*)",
      "dest": "frontend/$1"
    }
  ]
}
```

**Limitations**:

- Max 50MB de téléchargement
- Timeout de 60s max
- Pas de stockage persistant

---

## 🎯 Option 4: Docker + Cloud Run (Google Cloud)

### 1. Créer les Dockerfiles

`backend/Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

`frontend/Dockerfile`:

```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 2. Déployer sur Cloud Run

```bash
# Backend
cd backend
gcloud builds submit --tag gcr.io/PROJECT_ID/ernie-backend
gcloud run deploy ernie-backend --image gcr.io/PROJECT_ID/ernie-backend --platform managed

# Frontend
cd frontend
gcloud builds submit --tag gcr.io/PROJECT_ID/ernie-frontend
gcloud run deploy ernie-frontend --image gcr.io/PROJECT_ID/ernie-frontend --platform managed
```

---

## 📊 Comparaison des Options

| Service       | Prix          | Avantages                       | Limitations                  |
| ------------- | ------------- | ------------------------------- | ---------------------------- |
| **Vercel**    | Gratuit       | Simple, rapide, CDN global      | Serverless = restructuration |
| **Netlify**   | Gratuit       | Facile, bon DX                  | Que pour frontend            |
| **Render**    | Gratuit       | Python natif, persistance       | Cold starts gratuit          |
| **Railway**   | $5/mois       | Simple, bon pour Python         | Pas de free tier permanent   |
| **Fly.io**    | Gratuit       | Containers, proche utilisateurs | Plus complexe                |
| **Cloud Run** | Pay-as-you-go | Scalable, professionnel         | Nécessite compte GCP         |

---

## 🔧 Configuration CORS pour Production

Mettez à jour `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://votre-app.vercel.app",  # Votre domaine Vercel
        "https://votre-app.netlify.app",  # Votre domaine Netlify
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Ou pour accepter tous les domaines en production (attention à la sécurité):

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À utiliser avec précaution
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## ✅ Checklist Avant Déploiement

### Backend

- [ ] `.env` configuré avec `NOVITA_API_KEY`
- [ ] CORS configuré pour votre domaine frontend
- [ ] `requirements.txt` à jour
- [ ] Variables d'environnement configurées sur la plateforme
- [ ] Endpoint `/api/health` fonctionne

### Frontend

- [ ] `VITE_API_URL` pointe vers le backend en production
- [ ] Build test local: `npm run build && npm run preview`
- [ ] Pas de hardcoded `localhost` dans le code
- [ ] Variables d'environnement configurées

---

## 🚀 Déploiement Rapide (Recommandé)

### Frontend sur Vercel

```bash
cd frontend

# Installer Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
vercel --prod
```

Après le déploiement, vous obtiendrez une URL comme: `https://ernie-finsight.vercel.app`

### Backend sur Render

1. Créez un compte sur [render.com](https://render.com)
2. Cliquez "New +" → "Web Service"
3. Connectez votre GitHub
4. Sélectionnez votre repo
5. Configuration:
   - **Name**: ernie-finsight-api
   - **Root Directory**: backend
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Variables d'environnement:
   - `NOVITA_API_KEY`: [votre clé]
   - `MAX_FILE_SIZE_MB`: 10
7. Cliquez "Create Web Service"

Vous obtiendrez une URL comme: `https://ernie-finsight-api.onrender.com`

### Connecter Frontend et Backend

Retournez sur Vercel:

1. Allez dans Settings → Environment Variables
2. Ajoutez: `VITE_API_URL` = `https://ernie-finsight-api.onrender.com`
3. Redéployez: `vercel --prod`

---

## 🎉 C'est Prêt!

Votre application est maintenant en ligne:

- **Frontend**: https://ernie-finsight.vercel.app
- **Backend**: https://ernie-finsight-api.onrender.com

Testez avec un whitepaper et partagez le lien pour votre hackathon! 🚀

---

## 💡 Conseils pour le Hackathon

1. **Domaine personnalisé** (optionnel):

   - Vercel permet des domaines gratuits: `ernie-finsight.vercel.app`
   - Ou achetez un domaine sur Namecheap (~$1)

2. **Analytics**:

   - Ajoutez Vercel Analytics (gratuit)
   - Suivez les utilisations pendant le hackathon

3. **Monitoring**:

   - Render a des logs intégrés
   - Configurez des alertes si le service tombe

4. **Demo**:

   - Préparez 3-4 whitepapers de test
   - Vérifiez que tout fonctionne avant la présentation
   - Ayez une vidéo de backup au cas où

5. **Performance**:
   - Render gratuit a des "cold starts" (~30s)
   - Faites une requête de warmup avant la démo!

Bon courage pour votre hackathon! 🎯
