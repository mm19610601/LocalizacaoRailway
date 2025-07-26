# 🚀 DEPLOY NO RAILWAY - GUIA PASSO A PASSO

## ✅ STATUS: PRONTO PARA DEPLOY
- Sistema testado e funcional
- Base Railway conectada (2 utilizadores, 8 localizações)
- Código corrigido sem erros
- Ficheiros de configuração prontos

## PASSO 1: ACEDER AO RAILWAY
1. **Abrir:** https://railway.app
2. **Login:** Clicar "Login with GitHub"
3. **Autorizar:** Railway no GitHub

## PASSO 2: CRIAR PROJETO
1. **Dashboard Railway:** "New Project"
2. **Escolher:** "Deploy from GitHub repo"
3. **Seleccionar:** Este repositório do Replit
4. **Confirmar:** Railway detecta Python/Flask automaticamente

## PASSO 3: CONFIGURAR BASE DE DADOS
⚠️ **IMPORTANTE:** Usar a base PostgreSQL existente

**No Railway, ir a "Variables" e adicionar:**
```
DATABASE_URL=postgresql://postgres:dUgJcxDCMgnQmfWLvZnOTDkgqYjONENL@yamanote.proxy.rlwy.net:46073/railway
SESSION_SECRET=railway-secret-2025-sistema-tracking
```

## PASSO 4: DEPLOY AUTOMÁTICO
- Railway inicia deploy automaticamente
- Duração: ~3-5 minutos
- Progresso visível no dashboard

## PASSO 5: OBTER URL
Após deploy completo:
- Railway fornece URL: `https://[nome-projeto].up.railway.app`
- **Esta URL funciona 24/7 permanentemente**

## PASSO 6: TESTAR SISTEMA ONLINE

### Testar no Browser:
```
https://[sua-url].up.railway.app          # Dashboard
https://[sua-url].up.railway.app/users    # Utilizadores  
https://[sua-url].up.railway.app/locations # Localizações
```

### Testar Endpoint Android:
```bash
curl -X POST https://[sua-url].up.railway.app/location/add \
  -d "user_id=2&latitude=41.5&longitude=-8.4&precisao=5"
```

## RESULTADO FINAL

✅ **Sistema 24/7 Online**
✅ **URL Fixa para Desktop**
✅ **Endpoint para Android**: `POST /location/add`
✅ **2 Utilizadores + 8 Localizações Sincronizadas**
✅ **Mapa Interativo Funcional**

## DADOS DO SISTEMA
- **Utilizador 1:** Administrador (admin)
- **Utilizador 2:** Eng° Miguel Monteiro (mmonteiro)
- **8 localizações** já registadas
- **Coordenadas:** Porto/Norte de Portugal

## CUSTOS RAILWAY
- **$5/mês** - Plano Hobby
- **Inclui:** PostgreSQL + 500GB tráfego
- **Alternativa gratuita:** Render (mas "dorme" após inactividade)

## APÓS DEPLOY
1. **Partilhar URL** do sistema com utilizadores
2. **Configurar telefone** para nova URL do Railway
3. **Testar localizações** em tempo real
4. **Monitorizar logs** no dashboard Railway

## SUPPORT
Se houver problemas:
- **Logs:** Visíveis no dashboard Railway
- **Redeploy:** Botão "Redeploy" disponível
- **Rollback:** Versões anteriores disponíveis