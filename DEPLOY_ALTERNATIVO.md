# DEPLOY RAILWAY - ALTERNATIVAS

## PROBLEMA: Railway não encontrou repositório GitHub

### SOLUÇÃO 1: UPLOAD DIRETO DOS FICHEIROS
Se não conseguir conectar via GitHub:

1. **No Railway:** "New Project" → "Empty Project"
2. **Criar serviço:** "Add Service" → "Source Code"
3. **Upload ficheiros:** Arrastar todos os ficheiros do projeto
4. **Ficheiros essenciais:**
   - app.py
   - main.py
   - models.py
   - routes.py
   - templates/ (pasta completa)
   - static/ (pasta completa)
   - pyproject.toml
   - railway.json
   - Procfile

### SOLUÇÃO 2: USAR RAILWAY CLI
```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy do diretório atual
railway deploy
```

### SOLUÇÃO 3: CRIAR REPOSITÓRIO GITHUB PRIMEIRO
1. **GitHub:** Criar novo repositório
2. **Upload:** Todos os ficheiros do projeto
3. **Railway:** Conectar ao novo repositório

### CONFIGURAÇÃO EM QUALQUER CASO
Após criar projeto no Railway, adicionar em "Variables":
```
DATABASE_URL=postgresql://postgres:dUgJcxDCMgnQmfWLvZnOTDkgqYjONENL@yamanote.proxy.rlwy.net:46073/railway
SESSION_SECRET=railway-secret-2025
```

## FICHEIROS PRONTOS PARA UPLOAD
✅ Todos os ficheiros estão preparados
✅ Configuração de base de dados incluída
✅ Sistema testado e funcional