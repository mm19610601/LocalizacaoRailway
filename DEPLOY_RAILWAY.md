# Guia de Deploy no Railway - Sistema Permanente

## Passo 1: Preparar o Sistema Local (✓ COMPLETO)
- [x] Base de dados PostgreSQL configurada
- [x] Aplicação Flask funcionando
- [x] Dados de teste inseridos

## Passo 2: Configurar Railway

### 2.1 Criar Conta no Railway
1. Ir a https://railway.app
2. Clicar em "Login" 
3. Escolher "Login with GitHub" (recomendado)
4. Autorizar Railway no GitHub

### 2.2 Criar Projeto no Railway
1. No dashboard: "New Project"
2. Escolher "Deploy from GitHub repo"
3. Conectar este repositório
4. Railway vai detectar automaticamente que é uma aplicação Python/Flask

### 2.3 Configurar Base de Dados PostgreSQL
1. No projeto Railway: "New" → "Database" → "PostgreSQL"
2. Railway criará uma base de dados automática
3. Anotar as credenciais que aparecerão no dashboard

### 2.4 Configurar Variáveis de Ambiente
No Railway, ir a "Variables" e adicionar:

```
DATABASE_URL=postgresql://username:password@host:port/database
SESSION_SECRET=sua-chave-secreta-aqui-123456789
PORT=5000
```

(Railway fornecerá automaticamente DATABASE_URL quando criar a base)

## Passo 3: Executar Script na Base Railway

1. No Railway PostgreSQL, clicar em "Connect"
2. Escolher "psql" 
3. Executar os comandos do script database_setup.sql:

```sql
-- Copiar e colar cada comando do ficheiro database_setup.sql
CREATE TABLE IF NOT EXISTS utilizadores (...);
CREATE TABLE IF NOT EXISTS localizacoes (...);
-- etc.
```

## Passo 4: Deploy Automático

1. Railway fará deploy automático do código
2. Aguardar deploy concluir (~2-3 minutos)
3. Railway fornecerá URL permanente: `https://seu-projeto.up.railway.app`

## Passo 5: Testar Sistema Online

### Testar Aplicação Web
```bash
# Abrir no navegador
https://seu-projeto.up.railway.app

# Verificar dashboard
https://seu-projeto.up.railway.app/users
https://seu-projeto.up.railway.app/locations
```

### Testar Endpoint para Telefone
```bash
# Testar endpoint de localização (substitua pela sua URL)
curl -X POST https://seu-projeto.up.railway.app/location/add \
  -d "user_id=1&latitude=39.5&longitude=-8.7&precisao=10"

# Verificar se apareceu no mapa
curl https://seu-projeto.up.railway.app/api/locations
```

## Passo 6: URL para Desktop e Telefone

**Desktop (Browser):**
- https://seu-projeto.up.railway.app

**Telefone (HTTP POST):**
- Endpoint: https://seu-projeto.up.railway.app/location/add
- Método: POST
- Dados: user_id, latitude, longitude, precisao

## Vantagens do Railway

✓ **24/7 Online**: Funciona permanentemente
✓ **SSL Automático**: HTTPS configurado automaticamente  
✓ **Auto-Deploy**: Actualiza quando fizer changes no código
✓ **Backups**: Base de dados com backup automático
✓ **Escalável**: Pode aumentar recursos se necessário

## Custos Railway

- **Hobby Plan**: $5/mês - Ideal para este projeto
- **PostgreSQL**: Incluído no plano
- **Trafego**: 500GB/mês incluído

## Alternativas Gratuitas (Limitadas)

- **Render**: Deploy gratuito mas "dorme" após 15min inatividade
- **Heroku**: Planos pagos apenas
- **Vercel**: Só para frontend, precisaria base externa

## Próximos Passos Após Deploy

1. **Testar URL permanente** no desktop
2. **Configurar telefone** para enviar para nova URL
3. **Partilhar URL** com utilizadores
4. **Monitorizar logs** no dashboard Railway

## Comandos de Emergência

Se algo correr mal, pode sempre:
```bash
# Ver logs em tempo real no Railway dashboard
# Ou fazer rollback para versão anterior
# Ou redeploy clicando em "Redeploy"
```