# 🚀 Complete Telex Integration Guide

> **HNG Internship Stage 3 - Task Reminder Agent with Telex A2A Protocol**

This guide covers everything from deployment to testing your Task Reminder Agent with Telex.im.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Phase 1: Get Telex Access](#phase-1-get-telex-access)
4. [Phase 2: Deploy Your Agent](#phase-2-deploy-your-agent)
5. [Phase 3: Update Configuration](#phase-3-update-configuration)
6. [Phase 4: Register in Telex](#phase-4-register-in-telex)
7. [Phase 5: Test Integration](#phase-5-test-integration)
8. [Phase 6: Monitor & Debug](#phase-6-monitor--debug)
9. [Troubleshooting](#troubleshooting)
10. [Quick Reference](#quick-reference)

---

## Overview

### What You're Building
An AI Task Reminder Agent that:
- ✅ Understands natural language ("remind me at 5pm to study")
- ✅ Saves tasks to SQLite database
- ✅ Sends automated reminders via Telex
- ✅ Provides full REST API for task management
- ✅ Integrates with Telex using A2A protocol

### A2A Protocol Endpoint
Your agent exposes: **`POST /a2a/agent/taskAgent`**

**Example Request:**
```json
{
  "message": "remind me at 5pm to study",
  "user": "victor-kalanza"
}
```

**Example Response:**
```json
{
  "success": true,
  "response": "✅ Saved task #1: 'study' for November 03 at 05:00 PM",
  "agent": "taskAgent",
  "timestamp": "2025-11-03T14:30:00.000000"
}
```

---

## Prerequisites

- ✅ Code complete (already done!)
- ✅ GitHub repository: https://github.com/Kalanza/telex-task-agent
- ✅ Server tested locally
- ⏳ Telex access (we'll get this)
- ⏳ Production deployment (we'll do this)

**Estimated Total Time:** ~4 hours

---

## Phase 1: Get Telex Access

**Duration:** 5 minutes

### Step 1: Request Access

1. Open Slack → HNG Internship workspace
2. Navigate to `#stage-3-backend` channel
3. Run this command:
   ```
   /telex-invite your-email@example.com
   ```
   *Replace with your actual email*

4. Wait for confirmation (usually instant)

### Step 2: Access Telex

1. Check your email for invitation
2. Go to https://telex.im
3. Login with your invited email
4. Verify access to organization

### Your Telex Details

- **Profile:** https://telex.im/victor-kalanza/home/colleagues/019a4990-de20-7af3-a116-785810a578a0
- **Channel ID:** `019a4990-de20-7af3-a116-785810a578a0`
- **Agent Logs:** https://api.telex.im/agent-logs/019a4990-de20-7af3-a116-785810a578a0.txt

✅ **Phase 1 Complete!**

---

## Phase 2: Deploy Your Agent

**Duration:** 15 minutes

You need a public URL for Telex to communicate with your agent.

### Option A: Render (Recommended - No CLI Needed)

#### Step 1: Sign Up
1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with GitHub
4. Authorize Render to access your repositories

#### Step 2: Create Web Service
1. Click "New +" (top right)
2. Select "Web Service"
3. Click "Build and deploy from a Git repository"
4. Click "Configure account" → Connect GitHub
5. Find and select: `telex-task-agent`
6. Click "Connect"

#### Step 3: Configure Service

**Name:** `task-reminder-agent`

**Region:** Choose closest to you

**Branch:** `master`

**Runtime:** `Python 3`

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
python server.py
```

**Instance Type:** `Free`

#### Step 4: Environment Variables

Click "Add Environment Variable":

**Variable 1:**
- Key: `PORT`
- Value: `9000`

**Variable 2:**
- Key: `TELEX_WEBHOOK_URL`
- Value: `https://telex.im/api/webhook/YOUR_ENDPOINT`
  *(We'll update this later with actual Telex webhook)*

#### Step 5: Deploy
1. Click "Create Web Service"
2. Wait 5-10 minutes for build
3. Watch build logs
4. Success: "Your service is live 🎉"

#### Step 6: Get Your URL
Copy your URL from the top of the page:
```
https://task-reminder-agent.onrender.com
```

#### Step 7: Test Deployment

```powershell
# Test health check
Invoke-WebRequest -Uri "https://task-reminder-agent.onrender.com/" | Select-Object -ExpandProperty Content

# Test A2A endpoint
$body = @{
    message = "remind me at 5pm to study"
    user = "test-user"
} | ConvertTo-Json

Invoke-WebRequest -Uri "https://task-reminder-agent.onrender.com/a2a/agent/taskAgent" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body | Select-Object -ExpandProperty Content
```

**Expected Response:**
```json
{
  "success": true,
  "response": "✅ Saved task #1: 'study' for November 03 at 05:00 PM",
  "agent": "taskAgent",
  "timestamp": "..."
}
```

---

### Option B: Railway (CLI-Based)

```powershell
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize
railway init

# Deploy
railway up

# Get URL
railway status
```

Your URL: `https://task-agent-production.up.railway.app`

---

### Option C: Fly.io

```bash
# Install flyctl (Windows)
iwr https://fly.io/install.ps1 -useb | iex

# Deploy
fly launch --name task-reminder-agent
fly deploy

# Get URL
fly status
```

Your URL: `https://task-reminder-agent.fly.dev`

---

**✅ Phase 2 Complete!** - Save your production URL!

---

## Phase 3: Update Configuration

**Duration:** 2 minutes

### Step 1: Update telex-workflow.json

1. Open `telex-workflow.json` in VS Code
2. Find this line:
   ```json
   "url": "http://localhost:9000/a2a/agent/taskAgent"
   ```
3. Replace with your production URL:
   ```json
   "url": "https://task-reminder-agent.onrender.com/a2a/agent/taskAgent"
   ```
4. Save the file

### Step 2: Commit Changes (Optional)

```powershell
git add telex-workflow.json
git commit -m "chore: update workflow with production URL"
git push origin master
```

**✅ Phase 3 Complete!**

---

## Phase 4: Register in Telex

**Duration:** 5 minutes

### Step 1: Access Telex Dashboard
1. Go to https://telex.im/victor-kalanza/home
2. Login if needed

### Step 2: Navigate to AI Coworkers
Look for:
- "AI Coworkers"
- "Agents"
- "Workflows"
- "Integrations"

### Step 3: Create New Agent
Click:
- "Add Agent"
- "Create Workflow"
- "New Agent"
- "+" button

### Step 4: Upload Configuration

**Option A: Upload File**
1. Click "Upload JSON" or "Import"
2. Select `telex-workflow.json`
3. Click "Upload"

**Option B: Paste JSON**
1. Click "Manual Configuration" or "Paste JSON"
2. Open `telex-workflow.json`, copy all content
3. Paste into Telex
4. Click "Create" or "Save"

### Step 5: Activate Agent
1. Find "Task Reminder Agent" in list
2. Toggle to "Active"
3. Verify green indicator

### Your Agent Configuration

```json
{
  "name": "Task Reminder Agent",
  "category": "productivity",
  "description": "AI Task Reminder Agent with natural language processing",
  "url": "https://your-url.onrender.com/a2a/agent/taskAgent"
}
```

**✅ Phase 4 Complete!**

---

## Phase 5: Test Integration

**Duration:** 5 minutes

### Step 1: Open Telex Chat
1. In Telex, find or create a chat/channel
2. Locate your Task Reminder Agent

### Step 2: Invoke Your Agent

Try one of these methods:

**Method 1: Mention**
```
@Task-Reminder-Agent remind me at 5pm to study
```

**Method 2: Direct Message**
```
/agent Task-Reminder-Agent
remind me at 5pm to study
```

**Method 3: Direct Chat**
```
remind me at 5pm to study
```

### Step 3: Verify Response

You should see:
```
✅ Saved task #1: 'study' for November 03 at 05:00 PM
```

### Step 4: Test More Commands

```
remind me tomorrow at 3pm to call mom
list my tasks
remind me in 2 hours to take a break
```

### Step 5: Check Agent Logs

Visit: https://api.telex.im/agent-logs/019a4990-de20-7af3-a116-785810a578a0.txt

You'll see:
- All messages sent to your agent
- Agent responses
- Timestamps
- Any errors

### Step 6: Test Reminders

1. Create: "remind me in 2 minutes to test"
2. Wait 2 minutes
3. Verify reminder arrives in Telex

**✅ Phase 5 Complete!**

---

## Phase 6: Monitor & Debug

**Duration:** Ongoing

### Check Render Logs
1. Go to https://render.com/dashboard
2. Click your service
3. Click "Logs" tab

Expected logs:
```
Database initialized successfully
[OK] Reminder scheduler started (checking every 30 seconds)
Uvicorn running on http://0.0.0.0:9000
Application startup complete
```

### Check Telex Agent Logs
https://api.telex.im/agent-logs/019a4990-de20-7af3-a116-785810a578a0.txt

### Test All Endpoints

```powershell
$url = "https://task-reminder-agent.onrender.com"

# Health check
Invoke-WebRequest -Uri "$url/"

# Create task
$body = @{message="remind me at 5pm to study"; user="victor"} | ConvertTo-Json
Invoke-WebRequest -Uri "$url/a2a/agent/taskAgent" -Method POST -Body $body -ContentType "application/json"

# List tasks
Invoke-WebRequest -Uri "$url/tasks"

# Get specific user tasks
Invoke-WebRequest -Uri "$url/tasks?user=victor"

# Manual reminder trigger (testing)
Invoke-WebRequest -Uri "$url/trigger-reminders"
```

**✅ Phase 6 Complete!**

---

## Troubleshooting

### Issue 1: Agent Not Responding

**Symptoms:**
- No response in Telex
- Timeout errors

**Diagnosis:**
```powershell
# Test endpoint directly
Invoke-WebRequest -Uri "https://your-url.onrender.com/"
Invoke-WebRequest -Uri "https://your-url.onrender.com/a2a/agent/taskAgent" -Method POST -Body '{"message":"test","user":"me"}' -ContentType "application/json"
```

**Solutions:**
1. Check Render service status (should be "Live")
2. Verify URL in `telex-workflow.json` is correct
3. Check Render logs for errors
4. Render free tier sleeps after inactivity - first request takes 30-60s

### Issue 2: Reminders Not Sending

**Symptoms:**
- Tasks created but no reminders
- No Telex notifications

**Diagnosis:**
```powershell
# Check if tasks exist
Invoke-WebRequest -Uri "https://your-url.onrender.com/tasks"

# Check Render logs for scheduler execution
# Look for: "Running job 'Check for due reminders'"
```

**Solutions:**
1. Verify `TELEX_WEBHOOK_URL` environment variable is set in Render
2. Check scheduler is running in Render logs
3. Create a 2-minute test reminder
4. Verify task `sent` flag is 0 before due time

### Issue 3: Time Parsing Errors

**Symptoms:**
- "Could not parse time" error
- Invalid date responses

**Supported Formats:**
- ✅ "5pm", "17:00", "5:30pm"
- ✅ "tomorrow at 3pm"
- ✅ "in 2 hours", "in 30 minutes"
- ✅ "November 5 at 2pm"
- ❌ "next week" (too ambiguous)
- ❌ "later" (no specific time)

**Solution:**
Ask users to be more specific with times.

### Issue 4: Database Errors

**Symptoms:**
- "OperationalError: no such table"
- File permission errors

**Solutions:**
1. Check Render logs for SQLite errors
2. Redeploy: Render Dashboard → "Manual Deploy" → "Clear build cache & deploy"
3. Verify database initialization in logs

### Issue 5: Render Service Sleeping

**Symptoms:**
- First request takes 30-60 seconds
- Subsequent requests are fast

**Explanation:**
- Render free tier spins down after 15 minutes of inactivity
- First request wakes it up (slow)
- Stays awake while active

**Solutions:**
1. Accept the delay (free tier limitation)
2. Upgrade to paid tier ($7/month - always on)
3. Use a cron job to ping every 10 minutes

---

## Quick Reference

### Your Details
- **Telex Profile:** https://telex.im/victor-kalanza/home/colleagues/019a4990-de20-7af3-a116-785810a578a0
- **Channel ID:** `019a4990-de20-7af3-a116-785810a578a0`
- **Agent Logs:** https://api.telex.im/agent-logs/019a4990-de20-7af3-a116-785810a578a0.txt
- **GitHub Repo:** https://github.com/Kalanza/telex-task-agent

### Your URLs (After Deployment)
- **Production:** `https://task-reminder-agent.onrender.com`
- **Health Check:** `https://task-reminder-agent.onrender.com/`
- **A2A Endpoint:** `https://task-reminder-agent.onrender.com/a2a/agent/taskAgent`
- **Tasks API:** `https://task-reminder-agent.onrender.com/tasks`
- **API Docs:** `https://task-reminder-agent.onrender.com/docs`

### Test Commands in Telex
```
remind me at 5pm to study
remind me tomorrow at 3pm to call mom
remind me in 2 hours to take a break
list my tasks
```

### Test Commands in PowerShell
```powershell
# Health check
Invoke-WebRequest -Uri "https://task-reminder-agent.onrender.com/"

# Create task via A2A
$body = @{message="remind me at 5pm to study"; user="victor"} | ConvertTo-Json
Invoke-WebRequest -Uri "https://task-reminder-agent.onrender.com/a2a/agent/taskAgent" -Method POST -Body $body -ContentType "application/json"

# List all tasks
Invoke-WebRequest -Uri "https://task-reminder-agent.onrender.com/tasks"

# Filter by user
Invoke-WebRequest -Uri "https://task-reminder-agent.onrender.com/tasks?user=victor"

# Manual reminder check
Invoke-WebRequest -Uri "https://task-reminder-agent.onrender.com/trigger-reminders"
```

---

## Success Checklist

Your integration is working if:

- ✅ Render service shows "Live" status
- ✅ Health endpoint responds instantly
- ✅ A2A endpoint creates tasks successfully
- ✅ Agent appears in Telex interface
- ✅ Agent responds to messages in Telex within 1-2 seconds
- ✅ Tasks have incrementing IDs (1, 2, 3...)
- ✅ "list my tasks" shows created tasks
- ✅ Reminders arrive at scheduled time
- ✅ Agent logs show all interactions
- ✅ Render logs show scheduler executing every 30 seconds
- ✅ No errors in Render logs

---

## Next Steps After Success

### 1. Create Documentation Assets
- [ ] Screenshot: Agent responding in Telex
- [ ] Screenshot: Task creation confirmation
- [ ] Screenshot: Reminder delivery
- [ ] GIF: Full interaction flow

### 2. Write Blog Post
**Suggested Title:** "Building an AI Task Reminder Agent with Python, FastAPI & Telex A2A Protocol"

**Sections:**
- Introduction (HNG challenge context)
- Architecture overview
- Tech stack (FastAPI, SQLite, APScheduler, dateparser)
- A2A protocol implementation
- Deployment process
- Challenges and solutions
- Testing strategy
- Demo screenshots
- Lessons learned
- Repository link

**Publish on:** Medium or Hashnode

### 3. Create Tweet
```
🤖 Just deployed my AI Task Reminder Agent for @hnginternship Stage 3!

✨ Features:
- Natural language processing
- Telex A2A protocol integration  
- Automated reminders with APScheduler
- Full REST API + comprehensive testing

Built with Python & FastAPI 🐍

🔗 https://github.com/Kalanza/telex-task-agent
📝 [blog-link]
🚀 Live: [deployed-url]

@teleximapp #HNGInternship #Python #AI

[Attach screenshot/GIF]
```

### 4. Submit to HNG
In Slack `#stage-3-backend`:
```
/submit
```

Provide:
- **Repository URL:** https://github.com/Kalanza/telex-task-agent
- **Live Endpoint:** https://task-reminder-agent.onrender.com
- **Blog Post:** [Your Medium/Hashnode link]
- **Tweet:** [Your tweet link]
- **Documentation:** README.md

---

## Support Resources

- **This Guide:** Complete integration steps
- **HNG Slack:** #stage-3-backend channel
- **Render Docs:** https://render.com/docs
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **Project README:** See README.md in repo

---

## Timeline Estimate

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Get Telex Access | 5 min | 5 min |
| Deploy to Render | 15 min | 20 min |
| Update Configuration | 2 min | 22 min |
| Register in Telex | 5 min | 27 min |
| Test Integration | 5 min | 32 min |
| Create Screenshots | 10 min | 42 min |
| Write Blog Post | 2-3 hours | ~3.5 hours |
| Tweet & Submit | 15 min | ~4 hours |

---

**🎉 Congratulations! Your Task Reminder Agent is live on Telex!**

**Good luck with your submission!** 🚀

---

*Last Updated: November 3, 2025*  
*Repository: https://github.com/Kalanza/telex-task-agent*

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
