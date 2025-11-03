# Telex A2A Integration Guide

## 🔗 A2A Protocol Endpoint

Your agent is now configured with the A2A (Agent-to-Agent) protocol endpoint required by Telex.

**A2A Endpoint:** `/a2a/agent/taskAgent`

### Example A2A Request
```json
{
  "message": "remind me at 5pm to study",
  "user": "victor-kalanza"
}
```

### Example A2A Response
```json
{
  "success": true,
  "response": "✅ Saved task #1: 'study' for November 03 at 05:00 PM",
  "agent": "taskAgent",
  "timestamp": "2025-11-03T14:30:00.000000"
}
```

---

## 🚀 Deployment Steps for Telex

### Step 1: Deploy Your Agent

Choose a platform and deploy:

#### Option A: Railway (Recommended)
```bash
# Install Railway CLI (if not installed)
npm i -g @railway/cli

# Login
railway login

# Initialize and deploy
railway init
railway up

# Get your URL
railway status
```

#### Option B: Render
1. Go to https://render.com/dashboard
2. Click "New +" → "Web Service"
3. Connect your GitHub repo: `https://github.com/Kalanza/telex-task-agent`
4. Configure:
   - **Name:** task-reminder-agent
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python server.py`
5. Click "Create Web Service"
6. Copy your URL (e.g., `https://task-reminder-agent.onrender.com`)

#### Option C: Fly.io
```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Deploy
fly launch --name task-reminder-agent
fly deploy

# Get your URL
fly status
```

**After deployment, you'll get a URL like:**
- Railway: `https://task-agent-production.up.railway.app`
- Render: `https://task-reminder-agent.onrender.com`
- Fly.io: `https://task-reminder-agent.fly.dev`

---

### Step 2: Update Workflow Configuration

1. Open `telex-workflow.json`
2. Replace `YOUR_DEPLOYED_URL` with your actual deployed URL:
   ```json
   "url": "https://task-agent-production.up.railway.app/a2a/agent/taskAgent"
   ```

---

### Step 3: Register Agent in Telex

1. Go to your Telex dashboard: https://telex.im/victor-kalanza/home
2. Navigate to AI Coworkers or Agents section
3. Click "Add Agent" or "Create Workflow"
4. Upload or paste your `telex-workflow.json` configuration
5. OR manually configure:
   - **Name:** Task Reminder Agent
   - **Category:** Productivity
   - **A2A URL:** `https://YOUR_URL/a2a/agent/taskAgent`
   - **Description:** AI assistant for task reminders with NLP

---

### Step 4: Test Your Integration

#### Test via Telex Chat:
1. Open a chat in Telex
2. Mention or invoke your agent
3. Send: `remind me at 5pm to study`
4. Your agent should respond with confirmation

#### Test A2A Endpoint Directly:
```powershell
$body = @{
    message = "remind me tomorrow at 3pm to call mom"
    user = "victor-kalanza"
} | ConvertTo-Json

Invoke-WebRequest -Uri "https://YOUR_URL/a2a/agent/taskAgent" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

#### Check Agent Logs:
Visit: `https://api.telex.im/agent-logs/019a4990-de20-7af3-a116-785810a578a0.txt`

This shows all interactions with your agent in real-time.

---

## 📋 Environment Variables

Set these in your deployment platform:

| Variable | Value | Purpose |
|----------|-------|---------|
| `TELEX_WEBHOOK_URL` | Your Telex webhook URL | For sending reminders back to users |
| `PORT` | `9000` (or platform default) | Server port |

**For Railway:**
```bash
railway variables set TELEX_WEBHOOK_URL=https://telex.im/api/webhook/your-endpoint
```

**For Render:**
Add in the Environment Variables section of your web service settings.

---

## 🧪 Testing Checklist

- [ ] Agent deployed and accessible
- [ ] A2A endpoint responds: `POST /a2a/agent/taskAgent`
- [ ] Health check works: `GET /` returns status
- [ ] Workflow JSON uploaded to Telex
- [ ] Can send messages to agent in Telex
- [ ] Agent logs show interactions: `https://api.telex.im/agent-logs/{channel-id}.txt`
- [ ] Reminders are sent back to Telex
- [ ] Database persists tasks correctly

---

## 🔍 Troubleshooting

### Agent not responding in Telex:
1. Check agent logs: `https://api.telex.im/agent-logs/019a4990-de20-7af3-a116-785810a578a0.txt`
2. Verify A2A URL is correct in workflow configuration
3. Test endpoint directly with curl/Invoke-WebRequest
4. Check deployment logs for errors

### Reminders not being sent:
1. Verify `TELEX_WEBHOOK_URL` environment variable is set
2. Check scheduler is running: Look for "Scheduler started" in logs
3. Test manual trigger: `GET /trigger-reminders`
4. Verify tasks exist: `GET /tasks`

### Database errors:
1. Ensure SQLite file permissions are correct
2. Check `db/` directory exists
3. Verify database initialization: `logs/app.log`

---

## 📊 Monitoring

### Check Server Health:
```bash
curl https://YOUR_URL/
```

### View All Tasks:
```bash
curl https://YOUR_URL/tasks
```

### Manual Reminder Trigger:
```bash
curl https://YOUR_URL/trigger-reminders
```

### Check Logs:
- **Application logs:** `logs/app.log`
- **Telex agent logs:** `https://api.telex.im/agent-logs/019a4990-de20-7af3-a116-785810a578a0.txt`

---

## 🎯 Your Agent Profile

**Telex Profile:** https://telex.im/victor-kalanza/home/colleagues/019a4990-de20-7af3-a116-785810a578a0  
**Agent Page:** https://telex.im/ai-coworkers/task-agent-785810a578a0  
**Channel ID:** `019a4990-de20-7af3-a116-785810a578a0`  
**Agent Logs:** `https://api.telex.im/agent-logs/019a4990-de20-7af3-a116-785810a578a0.txt`

---

## 📚 Additional Resources

- **Telex Documentation:** https://docs.telex.im
- **A2A Protocol Spec:** Check Telex developer docs
- **Your Repository:** https://github.com/Kalanza/telex-task-agent
- **HNG Task Details:** See `HNG_TASK3_COMPLETION.md`

---

## ✅ Quick Deployment Checklist

1. [ ] Choose deployment platform (Railway/Render/Fly.io)
2. [ ] Deploy your agent
3. [ ] Get deployed URL
4. [ ] Update `telex-workflow.json` with your URL
5. [ ] Set `TELEX_WEBHOOK_URL` environment variable
6. [ ] Register agent in Telex
7. [ ] Test A2A endpoint directly
8. [ ] Test via Telex chat
9. [ ] Verify in agent logs
10. [ ] Create reminder and wait for it to trigger

**Once deployed and tested, you're ready to submit!** 🚀
