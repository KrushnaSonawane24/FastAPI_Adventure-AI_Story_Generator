# 🚀 Render Deployment Guide

## Complete Step-by-Step Deployment

### **Prerequisites**
- GitHub account with your code pushed
- Render account (free): https://render.com
- Groq API key

---

## 📦 **Method 1: Using render.yaml (Recommended)**

### **Step 1: Push to GitHub**
```bash
git add .
git commit -m "Add Render deployment config"
git push origin main
```

### **Step 2: Deploy on Render**

1. **Go to Render Dashboard**: https://dashboard.render.com
2. **Click "New +"** → Select **"Blueprint"**
3. **Connect GitHub Repository**:
   - Select your repo: `FastAPI_Adventure-AI_Story_Generator`
   - Click "Connect"
4. **Render will auto-detect `render.yaml`**
5. **Click "Apply"**

### **Step 3: Configure Environment Variables**

**For Backend Service:**
1. Go to backend service in dashboard
2. Click "Environment" tab
3. Add these variables:
   ```
   GROQ_API_KEY = your_groq_api_key_here
   ALLOWED_ORIGINS = https://your-frontend-name.onrender.com
   ```

### **Step 4: Update Frontend API URL**

After backend deploys, copy its URL (e.g., `https://story-generator-api.onrender.com`)

Update `frontend/src/util.js`:
```javascript
export const API_BASE_URL = "https://story-generator-api.onrender.com/api";
```

Push changes:
```bash
git add frontend/src/util.js
git commit -m "Update API URL for production"
git push origin main
```

Render will auto-redeploy frontend!

---

## 📦 **Method 2: Manual Deployment**

### **A. Deploy Backend**

1. **New Web Service**:
   - Dashboard → "New +" → "Web Service"
   - Connect GitHub repo
   - Select branch: `main`

2. **Configure Backend**:
   ```
   Name: story-generator-api
   Region: Oregon (or closest)
   Branch: main
   Root Directory: backend
   Runtime: Python 3
   Build Command: ./build.sh
   Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
   Plan: Free
   ```

3. **Environment Variables**:
   ```
   PYTHON_VERSION = 3.11.0
   GROQ_API_KEY = your_groq_api_key
   ALLOWED_ORIGINS = https://your-frontend.onrender.com
   DATABASE_URL = sqlite:///./database.db
   DEBUG = False
   ```

4. **Click "Create Web Service"**

### **B. Deploy Frontend**

1. **New Static Site**:
   - Dashboard → "New +" → "Static Site"
   - Connect same GitHub repo

2. **Configure Frontend**:
   ```
   Name: story-generator-frontend
   Branch: main
   Root Directory: frontend
   Build Command: npm install && npm run build
   Publish Directory: dist
   ```

3. **Add Rewrite Rule** (for React Router):
   - Go to "Redirects/Rewrites"
   - Add rule:
     ```
     Source: /*
     Destination: /index.html
     Action: Rewrite
     ```

4. **Click "Create Static Site"**

---

## 🔧 **Post-Deployment Steps**

### **1. Update CORS**
After frontend deploys, update backend environment variable:
```
ALLOWED_ORIGINS = https://your-actual-frontend-url.onrender.com
```

### **2. Test Endpoints**
- Backend: `https://your-backend.onrender.com/docs`
- Frontend: `https://your-frontend.onrender.com`

### **3. Monitor Logs**
- Click on service → "Logs" tab
- Check for any errors

---

## ⚠️ **Important Notes**

### **Free Tier Limitations:**
- ✅ Backend spins down after 15 min inactivity
- ✅ First request takes ~30 seconds (cold start)
- ✅ 750 hours/month free

### **Database:**
- SQLite works but data resets on redeploy
- For persistent data, use PostgreSQL (Render provides free tier)

### **Custom Domain (Optional):**
- Go to service → "Settings" → "Custom Domain"
- Add your domain

---

## 🐛 **Troubleshooting**

### **Backend not starting:**
```bash
# Check logs for:
- Missing dependencies
- Port binding issues
- Environment variable errors
```

### **Frontend 404 errors:**
- Ensure rewrite rule is set
- Check build output in logs

### **CORS errors:**
- Update ALLOWED_ORIGINS with exact frontend URL
- Include `https://` protocol

---

## 📝 **Quick Commands**

```bash
# Local test before deploy
cd backend && uvicorn main:app --reload
cd frontend && npm run build && npm run preview

# Check build locally
cd frontend && npm run build
# Should create dist/ folder

# Push to trigger redeploy
git add .
git commit -m "Update"
git push origin main
```

---

## ✅ **Success Checklist**

- [ ] Code pushed to GitHub
- [ ] Backend service created on Render
- [ ] Frontend static site created on Render
- [ ] Environment variables set
- [ ] Frontend API URL updated
- [ ] CORS configured
- [ ] Both services deployed successfully
- [ ] Tested story generation

---

## 🎉 **Done!**

Your app is now live:
- **Backend API**: `https://story-generator-api.onrender.com`
- **Frontend**: `https://story-generator-frontend.onrender.com`

Share the frontend URL with anyone! 🚀
