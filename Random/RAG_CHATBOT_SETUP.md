# RAG Chatbot Workflow - Setup & Deployment Guide

## Overview

This is a production-ready **Retrieval Augmented Generation (RAG) Chatbot** workflow for n8n that answers questions about the GitHub API using semantic search and AI.

### Architecture

**Part 1: Data Indexing Pipeline**
```
HTTP Request (fetch GitHub OpenAPI spec)
    ↓
Default Data Loader (process document)
    ↓
Recursive Character Text Splitter (chunk text into 1000-char pieces)
    ↓
Embeddings OpenAI (generate vector embeddings)
    ↓
Pinecone Vector Store (save embeddings to vector DB)
```

**Part 2: Chat Query Pipeline**
```
Chat Trigger (user input)
    ↓
AI Agent (orchestrate tools & LLM)
    ├→ Simple Memory (conversation context)
    ├→ Vector Store Tool (search knowledge base)
    │   ↓
    │   Pinecone Vector Store (retrieve relevant docs)
    │   ↓
    │   Embeddings OpenAI (generate query embeddings)
    │
    └→ OpenAI Chat Model (generate response)
```

## Prerequisites

You'll need accounts and API keys for:

### 1. **OpenAI** (for embeddings and chat)
- Create account: https://platform.openai.com/signup
- Get API key: https://platform.openai.com/api/keys
- Required models:
  - `text-embedding-3-small` (for embeddings)
  - `gpt-4o-mini` (for chat responses)
- Ensure you have credits available

### 2. **Pinecone** (for vector database)
- Create account: https://www.pinecone.io/
- Create an index named: `github-api-docs`
- Dimension: 1536 (for text-embedding-3-small)
- Get API key from dashboard
- Index setup:
  ```
  Name: github-api-docs
  Dimension: 1536
  Metric: cosine
  ```

### 3. **n8n** (already running at http://localhost:5678)
- Your local n8n instance
- MCP configured to access the instance

## Deployment Steps

### Step 1: Import the Workflow

1. Open your local n8n: http://localhost:5678
2. Click **"New"** → **"From URL"** or **"Import from file"**
3. Upload the `rag-chatbot-workflow.json` file
4. Click **"Import"**

### Step 2: Add Credentials

In n8n, go to **Credentials** and create/update:

#### OpenAI Credential
- Type: `OpenAI`
- API Key: Your OpenAI API key
- Name: `OpenAI`

#### Pinecone Credential
- Type: `Pinecone`
- API Key: Your Pinecone API key
- Name: `Pinecone`
- Environment: Your Pinecone environment (e.g., `us-east-1-gcp`)

### Step 3: Configure Credentials in Workflow

1. Open the imported workflow
2. For each of these nodes, click and select the credentials:
   - **HTTP Request**: No credentials needed (public GitHub URL)
   - **Embeddings OpenAI (Indexing)**: Select your OpenAI credential
   - **Pinecone Vector Store (Insert)**: Select your Pinecone credential
   - **Embeddings OpenAI (Query)**: Select your OpenAI credential
   - **Pinecone Vector Store (Retrieve)**: Select your Pinecone credential
   - **OpenAI Chat Model**: Select your OpenAI credential

### Step 4: Index GitHub API Documentation

1. Navigate to the **Data Indexing** section of the workflow (nodes 1-5)
2. Click **"Execute Workflow"** button
3. Wait for completion (may take 2-3 minutes for embeddings)
4. Monitor the Pinecone dashboard to see documents being indexed
5. You should see vectors appearing in your index

**Expected Result**: Your Pinecone dashboard will show indexed data with vectors.

### Step 5: Test the Chatbot

1. Once indexing is complete, click the **"Chat"** button (bottom-right)
2. Try asking a question like:
   ```
   "How do I create a GitHub App from a manifest?"
   ```
3. The chatbot will:
   - Convert your question to embeddings
   - Search Pinecone for relevant API documentation
   - Generate a response using GPT-4o-mini

**Expected Response**: Detailed answer with relevant GitHub API documentation references.

## Node-by-Node Configuration

### Chat Trigger
- **Type**: `@n8n/n8n-nodes-langchain.chatTrigger`
- **Settings**: Default (Leave as-is)
- **Purpose**: Entry point for user messages

### AI Agent
- **Type**: `@n8n/n8n-nodes-langchain.agent`
- **Agent Type**: `Tools Agent`
- **System Message**: 
  ```
  You are a helpful assistant providing information about the GitHub API 
  based on the OpenAPI V3 specifications. Answer questions accurately 
  using the provided tools.
  ```
- **Purpose**: Orchestrates tool usage and LLM calls

### Simple Memory
- **Type**: `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- **Settings**: Default
- **Purpose**: Maintains conversation history for follow-up questions

### Vector Store Question Answer Tool
- **Type**: `@n8n/n8n-nodes-langchain.toolVectorStore`
- **Name**: `Search GitHub API Documentation`
- **Description**: `Use this tool to search the GitHub API documentation.`
- **Top K**: `4` (retrieve top 4 relevant documents)
- **Purpose**: Tells AI Agent when and how to search the vector database

### Pinecone Vector Store (Insert Mode)
- **Operation**: `insert`
- **Index Name**: `github-api-docs`
- **Text Key**: `text`
- **Purpose**: Saves document embeddings during indexing

### Pinecone Vector Store (Retrieve Mode)
- **Operation**: `retrieve`
- **Index Name**: `github-api-docs`
- **Text Key**: `text`
- **Purpose**: Searches vector database for relevant documents

### Embeddings OpenAI
- **Model**: `text-embedding-3-small`
- **Purpose**: Converts text to 1536-dimensional vectors

### OpenAI Chat Model
- **Model**: `gpt-4o-mini`
- **Purpose**: Generates chatbot responses

### HTTP Request
- **Method**: `GET`
- **URL**: `https://raw.githubusercontent.com/github/rest-api-description/refs/heads/main/descriptions/api.github.com/api.github.com.json`
- **Purpose**: Fetches GitHub OpenAPI specification

### Default Data Loader
- **Text Key**: `body`
- **Purpose**: Extracts document content from HTTP response

### Recursive Character Text Splitter
- **Chunk Size**: `1000` characters
- **Chunk Overlap**: `200` characters
- **Purpose**: Splits large documents into semantic chunks for embedding

## Testing Commands

Once deployed, try these questions to test the RAG chatbot:

1. **Basic Question**:
   ```
   How do I create a GitHub App?
   ```

2. **Authentication Question**:
   ```
   What are the different authentication methods supported by the GitHub API?
   ```

3. **Follow-up Question** (tests memory):
   ```
   Can you give me an example in Python?
   ```

4. **Complex Query**:
   ```
   What is the difference between personal access tokens and OAuth tokens?
   ```

## Troubleshooting

### Issue: "Pinecone credentials not found"
- **Solution**: Make sure you've created and selected the Pinecone credential in each Pinecone node

### Issue: "OpenAI API key invalid"
- **Solution**: Verify your API key is correct and has sufficient credits (check OpenAI dashboard)

### Issue: "Index 'github-api-docs' not found"
- **Solution**: Create the index in Pinecone dashboard with dimension 1536

### Issue: "No documents retrieved"
- **Solution**: Run the indexing pipeline first (Part 1) to populate the vector store

### Issue: "Workflow runs but chat doesn't respond"
- **Solution**: 
  1. Check n8n logs for errors
  2. Verify all node credentials are properly set
  3. Run a test execution of the indexing pipeline

## Cost Considerations

- **OpenAI**: ~$0.02 per 1M embeddings tokens, ~$0.15 per 1M chat tokens
- **Pinecone**: Free tier includes 1 pod with 5 million vectors
- **n8n**: Local installation = free

For the GitHub API documentation (~100KB):
- Initial indexing: ~$0.01-0.05
- Per chat message: ~$0.001-0.01

## Next Steps

### Customize for Your Data
1. Replace the HTTP Request URL with your own data source
2. Update the system message in the AI Agent node
3. Create a new Pinecone index for your data
4. Re-run the indexing pipeline

### Integrate with Other Services
- Add Slack node to make it a Slack bot
- Add Telegram node for Telegram integration
- Add Webhook trigger for API access

### Production Deployment
- Deploy n8n to cloud (n8n Cloud, AWS, GCP, etc.)
- Set up proper authentication
- Monitor execution logs
- Set up alerts for failures

## Resources

- [n8n Documentation](https://docs.n8n.io/)
- [LangChain in n8n](https://docs.n8n.io/integrations/builtin/cluster-nodes/)
- [Pinecone Documentation](https://docs.pinecone.io/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [GitHub API Documentation](https://docs.github.com/en/rest)

## Workflow File

The complete workflow JSON is saved as: `rag-chatbot-workflow.json`

**Import Steps**:
1. Open n8n at http://localhost:5678
2. Click "+ New"
3. Select "Import from file"
4. Choose `rag-chatbot-workflow.json`
5. Click "Import"
