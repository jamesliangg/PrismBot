Starting local Redis DB

`docker run -d -p 6379:6379 -p 8001:8001 redis/redis-stack:latest`

Connection URL = `redis://localhost:6379`

Delete all keys in Redis DB `redis-cli flushall`

https://python.langchain.com/docs/integrations/vectorstores/redis
https://python.langchain.com/docs/integrations/providers/cohere
https://python.langchain.com/docs/use_cases/question_answering/quickstart
https://api.python.langchain.com/en/latest/vectorstores/langchain_community.vectorstores.redis.base.Redis.html#
https://python.langchain.com/docs/modules/data_connection/document_loaders/pdf
https://docs.streamlit.io/library/cheatsheet

https://python.langchain.com/docs/integrations/llms/google_vertex_ai_palm
https://python.langchain.com/docs/integrations/text_embedding/google_vertex_ai_palm
https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/overview
https://cloud.google.com/blog/products/databases/memorystore-for-redis-vector-search-and-langchain-integration
https://github.com/google-github-actions/example-workflows/blob/main/workflows/deploy-cloudrun/cloudrun-docker.yml