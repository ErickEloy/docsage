# docsage — Agente RAG que responde perguntas sobre PDFs

Cole o bloco abaixo no claude-free (aberto nesta pasta):

```
Crie o projeto "docsage": um agente de perguntas e respostas sobre PDFs usando LangChain.
- Backend FastAPI: upload de PDFs, chunking, embeddings, banco vetorial Chroma, endpoint /ask com citação da página de origem.
- Provedor de LLM plugável via OPENAI_BASE_URL e OPENAI_API_KEY (qualquer API compatível com OpenAI).
- Frontend Next.js simples: upload, chat e fontes clicáveis.
- docker-compose subindo tudo com um comando.
- Pasta /evals com 10 perguntas sobre um PDF de exemplo de domínio público e um script que mede a taxa de acerto.
- Testes pytest no backend.

Regras gerais:
- Trabalhe SOMENTE dentro desta pasta: C:\Users\erick\Documents\Projetos Pessoais\docsage
- Etapas pequenas; ao fim de cada etapa rode os testes e faça um commit (Conventional Commits).
- Nunca commite segredos: use .env.example e coloque .env no .gitignore.
- README em português e inglês, com diagrama da arquitetura em mermaid, como rodar, prints/GIF e roadmap.
- Licença MIT, GitHub Actions (lint com ruff/eslint + testes).
- No final: git push para o remoto origin.
```
