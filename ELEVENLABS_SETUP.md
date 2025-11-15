# ElevenLabs Knowledge Base Integration

This project automatically uploads project summaries and resumes to ElevenLabs Knowledge Base for building a conversational AI agent about your professional profile.

## 📋 Setup Instructions

### 1. Get Your ElevenLabs API Key

1. Go to [ElevenLabs Settings](https://elevenlabs.io/app/settings/api-keys)
2. Click "Generate API Key"
3. Copy the key (it will look like: `sk_...`)

### 2. (Optional) Create an Agent

If you want to automatically update an agent's knowledge base:

1. Go to [ElevenLabs Agents Dashboard](https://elevenlabs.io/app/conversational-ai)
2. Create a new conversational agent or select an existing one
3. Copy the Agent ID from the URL or agent settings

### 3. Configure Environment Variables

Create a `.env` file in the project root with:

```env
# Required: ElevenLabs API Key
ELEVENLABS_API_KEY=sk_your_key_here

# Optional: Agent ID for automatic updates
ELEVENLABS_AGENT_ID=agent_your_id_here

# Other required keys
GITHUB_TOKEN=ghp_your_github_token
OPENROUTER_API_KEY=sk-or-v1-your_key
```

## 🚀 How It Works

### When You Analyze GitHub Repositories

The backend will:
1. ✅ Generate AI summaries for all your repositories
2. ✅ Upload each project summary `.txt` file to ElevenLabs
3. ✅ Tag documents as "GitHub Project: [project-name]"
4. ✅ (Optional) Update your agent's knowledge base

**Example:**
```bash
# Analyze GitHub profile
curl -X POST http://localhost:8000/api/github/analyze \
  -H "Content-Type: application/json" \
  -d '{"username": "yourusername"}'

# Result: All project summaries uploaded to ElevenLabs KB
```

### When You Upload a Resume

The backend will:
1. ✅ Save the resume file locally
2. ✅ Upload the PDF/DOCX to ElevenLabs
3. ✅ Tag as "Resume: [username]"
4. ✅ (Optional) Update your agent's knowledge base

**Example:**
```bash
# Upload resume via API
curl -X POST http://localhost:8000/api/resume/analyze \
  -F "resume=@my_resume.pdf" \
  -F "username=john_doe"

# Result: Resume uploaded to ElevenLabs KB
```

## 📊 Knowledge Base Structure

After running the analysis, your ElevenLabs knowledge base will contain:

```
Knowledge Base Documents:
├── Resume: john_doe                    [FILE]
├── GitHub Project: awesome-app         [TEXT]
├── GitHub Project: react-component     [TEXT]
├── GitHub Project: python-tool         [TEXT]
└── ... (all your projects)
```

## 🤖 Using Your Agent

Once uploaded, your ElevenLabs conversational agent can answer questions like:

- "What projects has [name] worked on?"
- "Tell me about the awesome-app project"
- "What programming languages does [name] know?"
- "Summarize [name]'s experience with React"
- "What's on [name]'s resume?"

## 🔍 API Response Details

### GitHub Analysis Response

```json
{
  "success": true,
  "message": "GitHub analysis completed successfully",
  "data": {
    "username": "yourusername",
    "repositories": 15,
    "kb_uploaded": 15,
    "kb_documents": [
      {
        "type": "text",
        "name": "GitHub Project: awesome-app",
        "id": "doc_abc123",
        "status": "success"
      },
      ...
    ]
  }
}
```

### Resume Upload Response

```json
{
  "success": true,
  "message": "Resume uploaded and processed successfully",
  "data": {
    "filename": "john_doe_resume_20250115_143022.pdf",
    "kb_uploaded": true,
    "kb_document": {
      "type": "file",
      "name": "Resume: john_doe",
      "id": "doc_xyz789",
      "status": "success"
    }
  }
}
```

## 🛠️ Manual Knowledge Base Management

You can also use the `elevenlabs_kb.py` module directly:

```bash
# Upload a text file
python elevenlabs_kb.py --test-text "Some text content"

# Upload a file
python elevenlabs_kb.py --test-file path/to/document.pdf

# Upload all summaries from a directory
python elevenlabs_kb.py --upload-summaries project_summaries/username --username username
```

## 📚 ElevenLabs Knowledge Base Limits

- **Non-Enterprise**: Maximum 20MB or 300k characters
- **Enterprise**: Contact [ElevenLabs Sales](https://elevenlabs.io/contact-sales) for higher limits

## 🔐 Security Notes

- ✅ API keys are stored in `.env` (not committed to git)
- ✅ Files are uploaded securely via HTTPS
- ✅ Only you can access your knowledge base documents
- ⚠️ Make sure you have permission to upload the content

## 🐛 Troubleshooting

### "Client not initialized" Error
- Ensure `ELEVENLABS_API_KEY` is set in `.env`
- Restart the backend server after adding the key

### "Failed to upload to ElevenLabs KB" Warning
- Check your API key is valid
- Verify you haven't exceeded the knowledge base size limit
- Check the console logs for detailed error messages

### Agent Not Updating
- Ensure `ELEVENLABS_AGENT_ID` is correctly set
- Verify the agent ID exists in your ElevenLabs dashboard
- Check agent permissions and settings

## 📖 Additional Resources

- [ElevenLabs Knowledge Base Docs](https://elevenlabs.io/docs/agents-platform/customization/knowledge-base)
- [ElevenLabs API Reference](https://elevenlabs.io/docs/api-reference)
- [Conversational AI Agents](https://elevenlabs.io/docs/agents-platform)

---

**Need Help?** Check the console logs or open an issue on GitHub.

