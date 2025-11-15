# ElevenLabs Integration - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Get Your ElevenLabs API Key (2 min)

1. Go to **https://elevenlabs.io/app/settings/api-keys**
2. Click "Generate API Key"
3. Copy the key (starts with `sk_`)
4. Keep it safe!

### Step 2: Add to Environment (1 min)

Create or edit `.env` file in project root:

```env
# Add this line with your actual key
ELEVENLABS_API_KEY=sk_your_actual_key_here

# Optional: If you have an agent
ELEVENLABS_AGENT_ID=agent_your_id
```

### Step 3: Install Dependencies (1 min)

```bash
pip install -r requirements.txt
```

That's it! You're ready to go! 🎉

## 🎯 What Happens Now?

### When You Analyze a GitHub Profile:

```bash
# Run the backend
python backend_api.py

# Then in the frontend UI, enter a GitHub username
```

**Automatic actions:**
1. ✅ Scrapes all repositories
2. ✅ Generates AI summaries with GPT-4o
3. ✅ **Uploads ALL summaries to ElevenLabs KB**
4. ✅ Tags as "GitHub Project: [name]"
5. ✅ Updates your agent (if configured)

### When You Upload a Resume:

**Automatic actions:**
1. ✅ Saves resume locally
2. ✅ **Uploads to ElevenLabs KB**
3. ✅ Tags as "Resume: [username]"
4. ✅ Updates your agent (if configured)

## 📊 Check Your Results

After running analysis:

### In Console:
```
[API] ✓ Uploaded 15 summaries to ElevenLabs KB
[API] ✓ Resume uploaded to ElevenLabs KB
```

### In Backend Response:
```json
{
  "kb_uploaded": 15,
  "kb_documents": [...]
}
```

### In ElevenLabs Dashboard:
1. Go to **https://elevenlabs.io/app/conversational-ai**
2. Check your agent's knowledge base
3. See all uploaded documents!

## 🤖 Test Your Agent

If you configured an agent, try asking:

- "What projects has [name] worked on?"
- "Tell me about [project-name]"
- "What programming languages does [name] use?"
- "Summarize [name]'s experience"

## ⚡ Pro Tips

### Want to Update an Agent Automatically?

1. Create/select an agent in ElevenLabs dashboard
2. Copy the Agent ID from the URL
3. Add to `.env`:
   ```env
   ELEVENLABS_AGENT_ID=agent_abc123xyz
   ```
4. Now every upload automatically updates the agent!

### Want to See What's Uploaded?

Check the console logs:
```
[ElevenLabs KB] ✓ Text document created: GitHub Project: awesome-app (ID: doc_abc123)
[ElevenLabs KB] ✓ File document created: Resume: johndoe (ID: doc_xyz789)
```

### Need to Upload Existing Summaries?

```bash
# Use the standalone module
python elevenlabs_kb.py --upload-summaries project_summaries/username --username username
```

## 🔍 Verify It's Working

### 1. Check Backend Startup Logs:
```
[Backend API] ElevenLabs API Key: ✓ Configured
```

### 2. Check Health Endpoint:
```bash
curl http://localhost:8000/api/health
```

Should return:
```json
{
  "elevenlabs_configured": true
}
```

### 3. Upload a Test Resume:
```bash
curl -X POST http://localhost:8000/api/resume/analyze \
  -F "resume=@your_resume.pdf" \
  -F "username=testuser"
```

Look for:
```json
{
  "kb_uploaded": true
}
```

## ❌ Not Working?

### If you see: "Client not initialized"
- ✅ Check `.env` file exists in project root
- ✅ Check `ELEVENLABS_API_KEY` is set correctly
- ✅ Restart the backend server

### If you see: "Failed to upload to ElevenLabs KB"
- ✅ Verify your API key is valid
- ✅ Check you haven't exceeded 20MB limit (non-enterprise)
- ✅ Check the console for detailed error message

### If agent doesn't update:
- ✅ Verify `ELEVENLABS_AGENT_ID` is correct
- ✅ Check agent exists in your ElevenLabs dashboard
- ✅ Note: Agent updates are optional, uploads still work without it

## 📚 Next Steps

1. **Read full setup guide:** `ELEVENLABS_SETUP.md`
2. **See integration details:** `ELEVENLABS_INTEGRATION_SUMMARY.md`
3. **Check main README:** `README.md`

## 🎉 That's It!

You now have automatic knowledge base population for your Personal Digital Twin!

Every time you:
- Analyze a GitHub profile → **Summaries uploaded to ElevenLabs**
- Upload a resume → **Resume uploaded to ElevenLabs**

Zero manual work required! 🚀

---

**Questions?** Check the full documentation or console logs for detailed information.

**Need Enterprise Limits?** Contact: https://elevenlabs.io/contact-sales

