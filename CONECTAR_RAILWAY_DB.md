# Como Conectar à Base de Dados Railway

## Problema Atual
- Aplicação está a usar PostgreSQL local do Replit
- Precisa conectar à base Railway para sincronização

## Solução: Obter Credenciais Railway

### Passo 1: Ir ao Railway
1. Aceder https://railway.app
2. Login na sua conta
3. Ir ao seu projeto
4. Clicar na base PostgreSQL

### Passo 2: Obter DATABASE_URL
Na página da base Railway, procurar por:
- **Connect** ou **Variables**
- Copiar a **DATABASE_URL** completa

Será algo como:
```
postgresql://postgres:password@containers-us-west-xyz.railway.app:1234/railway
```

### Passo 3: Configurar no Replit
1. No Replit, ir aos **Secrets** (ícone de chave)
2. Adicionar nova secret:
   - **Key**: `DATABASE_URL`
   - **Value**: [colar a URL da Railway]

### Passo 4: Reiniciar Aplicação
- A aplicação vai conectar automaticamente à Railway
- Dados ficam sincronizados

## Verificação
Após configurar, a aplicação deve:
- Conectar à base Railway
- Mostrar os dados que inseriu lá
- Sincronizar localizações entre Railway e interface

## Alternativa: Configurar Variáveis Manualmente

Se não tiver a URL completa, configurar separadamente:

```
DB_HOST=containers-us-west-xyz.railway.app
DB_NAME=railway
DB_USER=postgres
DB_PASSWORD=sua-password
DB_PORT=1234
```

## Teste Final
Após configurar:
1. Reiniciar aplicação
2. Ir ao mapa
3. Verificar se mostra dados da Railway
4. Testar adicionar nova localização