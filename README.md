# Getting Started
## Folder Structure
```markdown
.
├── .github                                             # Github Actions
│   └── workflows                                       # Workflows
│       └── gcp_deploy.yaml                             # The cooler package
├── .gitattribute                                       # Git attributes
├── .gitignore                                          # Git ignore
├── Dockerfile                                          # Dockerfile
├── Guidelines-FINAL-4TH-EDITION-With-2023-Updates.pdf  # Sample PDF
├── README.md                                           # Readme
├── chat.py                                             # Chatbot
├── lit.py                                              # Streamlit app
├── requirements.txt                                    # Python requirements
└── vectorstore.pkl                                     # Vectorstore configuration
```
## Redis Database
### Locally
- Run `docker run -d -p 6379:6379 -p 8001:8001 redis/redis-stack:latest`
- Connection URL = `redis://localhost:6379`
- If hosting on a cloud service, can use ngrok to connect to Redis
  - Run `ngrok tcp 6379`
  - Example output is `tcp://2.tcp.ngrok.io:17000` use `2.tcp.ngrok.io` as host and `17000` as port
  - Redis url becomes `redis://2.tcp.ngrok.io:17000`
### Cloud
All you need is the connection URL to your database
## .env File
Create a `.env` file in the root directory with the following content:
```
REDIS_URL=<REDIS_URL>
GOOGLE_APPLICATION_CREDENTIALS=GOOGLE_APPLICATION_CREDENTIALS.json
```
You'll also need to create a service account key for Google Cloud and save it as `GOOGLE_APPLICATION_CREDENTIALS.json` in the root directory
### Service Account Scopes
- Compute Engine API
- Cloud Run Admin API
- Vertex AI API
## Starting Streamlit
- Start Streamlit with `streamlit run lit.py --server.port=8080`
- Access the app at `http://localhost:8080`
## Useful Commands 
Delete all keys in Redis DB `redis-cli flushall`

## References
- https://python.langchain.com/docs/integrations/vectorstores/redis
- https://python.langchain.com/docs/integrations/providers/cohere
- https://python.langchain.com/docs/use_cases/question_answering/quickstart
- https://api.python.langchain.com/en/latest/vectorstores/langchain_community.vectorstores.redis.base.Redis.html#
- https://python.langchain.com/docs/modules/data_connection/document_loaders/pdf
- https://docs.streamlit.io/library/cheatsheet
- https://python.langchain.com/docs/integrations/llms/google_vertex_ai_palm
- https://python.langchain.com/docs/integrations/text_embedding/google_vertex_ai_palm
- https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/overview
- https://cloud.google.com/blog/products/databases/memorystore-for-redis-vector-search-and-langchain-integration
- https://github.com/google-github-actions/example-workflows/blob/main/workflows/deploy-cloudrun/cloudrun-docker.yml
- https://cloud.google.com/run/docs/securing/managing-access