# Quick Start: Deploy RAG Chatbot in 5 Minutes

## ⚡ TL;DR - Fast Setup

### Prerequisites Check
```powershell
# Verify n8n is running
curl http://localhost:5678
```

### Step 1: Get Your API Keys (2 min)

**OpenAI:**
1. Go to https://platform.openai.com/api/keys
2. Create new secret key
3. Copy it

**Pinecone:**
1. Go to https://www.pinecone.io
2. Create account (or login)
3. Create index: Name=`github-api-docs`, Dimension=`1536`
4. Copy API key

### Step 2: Import Workflow (1 min)

1. Open http://localhost:5678
2. Click **+ New** → **Import from file**
3. Upload `rag-chatbot-workflow.json`
4. Click **Import**

### Step 3: Add Credentials (1 min)

In n8n:
1. Go to **Credentials** tab
2. Click **+ New** → Search for **OpenAI**
3. Paste your OpenAI API key
4. Click **Create**
5. Repeat for **Pinecone** credential

### Step 4: Update Nodes (1 min)

For each node that says "❌ Credentials missing":
1. Click the node
2. Select your credential from dropdown
3. Save

### Step 5: Run & Test!

1. Click **Execute Workflow** button
2. Wait for indexing (2-3 min)
3. Click **Chat** button
4. Ask: "How do I create a GitHub App?"

✅ Done! Your RAG chatbot is working!

---

## What Just Happened?

```
[Your Question]
      ↓
[Embedding (OpenAI)]
      ↓
[Vector Search (Pinecone)]
      ↓
[Retrieved Docs + Question]
      ↓
[AI Response (GPT-4o-mini)]
      ↓
[Answer with Sources]
```

## Test Questions

```
1. "How do I authenticate to the GitHub API?"
2. "What are the rate limits?"
3. "How do I create a webhook?"
4. "Can you show me a Python example?"
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| ❌ No credentials | Add OpenAI & Pinecone credentials in Credentials tab |
| ❌ No vector DB | Create index "github-api-docs" in Pinecone |
| ❌ Chat not working | Run indexing part first (Part 1 nodes) |
| ❌ API errors | Check OpenAI/Pinecone dashboard for quota/billing |

## Files Included

- `rag-chatbot-workflow.json` - Complete workflow (import this!)
- `RAG_CHATBOT_SETUP.md` - Detailed setup guide
- `RAG_CHATBOT_QUICKSTART.md` - This file

## Next: Customize

Want to use your own data instead of GitHub API?

1. Replace HTTP Request URL
2. Update AI Agent system message
3. Create new Pinecone index
4. Re-run indexing

See `RAG_CHATBOT_SETUP.md` for details.

---

**Need Help?**
- n8n Docs: https://docs.n8n.io
- Discord: https://discord.gg/n8n
- GitHub: https://github.com/n8n-io/n8n
