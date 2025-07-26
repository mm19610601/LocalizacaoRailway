# Como Executar Script SQL no Railway

## Método 1: Via Dashboard Railway (Mais Simples)

### Passo 1: Aceder à Base de Dados
1. No seu projeto Railway, clicar na base PostgreSQL
2. Ir ao separador "Connect"
3. Escolher a opção "Query" ou "psql"

### Passo 2: Executar Comandos SQL
Copiar e colar cada comando, um de cada vez:

```sql
-- 1. Criar tabela utilizadores
CREATE TABLE IF NOT EXISTS utilizadores (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    nome_completo TEXT,
    funcao TEXT,
    telemovel TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Criar tabela localizacoes
CREATE TABLE IF NOT EXISTS localizacoes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    latitude NUMERIC(10, 6) NOT NULL,
    longitude NUMERIC(10, 6) NOT NULL,
    precisao NUMERIC(5, 2),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES utilizadores(id) ON DELETE CASCADE
);

-- 3. Criar índices
CREATE INDEX IF NOT EXISTS idx_localizacoes_user_id ON localizacoes(user_id);
CREATE INDEX IF NOT EXISTS idx_localizacoes_timestamp ON localizacoes(timestamp);
CREATE INDEX IF NOT EXISTS idx_localizacoes_coordinates ON localizacoes(latitude, longitude);
CREATE INDEX IF NOT EXISTS idx_utilizadores_username ON utilizadores(username);

-- 4. Inserir dados de teste
INSERT INTO utilizadores (username, password, nome_completo, funcao, telemovel) 
VALUES 
    ('admin', 'admin123', 'Administrador', 'Admin', '969081497'),
    ('mmonteiro', '19610601-mM', 'Eng° Miguel Monteiro', 'Admin', NULL)
ON CONFLICT (username) DO NOTHING;

-- 5. Inserir localizações de teste
INSERT INTO localizacoes (user_id, latitude, longitude, precisao, timestamp) 
VALUES 
    (1, 39.500000, -8.700000, 9.00, '2025-07-21 13:18:50'::timestamp),
    (1, 39.600000, -8.700000, 9.00, '2025-07-21 13:18:54'::timestamp),
    (1, 39.700000, -8.700000, 9.00, '2025-07-21 13:18:58'::timestamp);

-- 6. Verificar se funcionou
SELECT 'utilizadores' as tabela, COUNT(*) as total FROM utilizadores
UNION ALL
SELECT 'localizacoes' as tabela, COUNT(*) as total FROM localizacoes;
```

## Método 2: Via psql (Terminal)

### Passo 1: Obter Credenciais
No Railway, na base PostgreSQL:
- Host: `containers-us-west-xyz.railway.app`
- Port: `1234`
- Database: `railway`  
- Username: `postgres`
- Password: `abc123xyz` (exemplo)

### Passo 2: Conectar via psql
```bash
psql postgresql://postgres:password@host:port/database
```

### Passo 3: Executar Script
```sql
\i database_setup.sql
```

## Método 3: Via Railway CLI (Avançado)

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Conectar ao projeto
railway link

# Executar comando SQL
railway run psql $DATABASE_URL -f database_setup.sql
```

## Método 4: Automatizar no Deploy

Criar ficheiro `migrate.py`:

```python
import os
import psycopg2
from psycopg2 import sql

def run_migration():
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    # Executar comandos SQL aqui
    sql_commands = [
        """
        CREATE TABLE IF NOT EXISTS utilizadores (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password TEXT NOT NULL,
            nome_completo TEXT,
            funcao TEXT,
            telemovel TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        # ... mais comandos
    ]
    
    for command in sql_commands:
        cur.execute(command)
    
    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    run_migration()
```

## Verificação Final

Após executar qualquer método, verificar com:

```sql
-- Ver estrutura das tabelas
\d utilizadores;
\d localizacoes;

-- Ver dados
SELECT * FROM utilizadores;
SELECT * FROM localizacoes;

-- Contar registos
SELECT 
    'utilizadores' as tabela, 
    COUNT(*) as total 
FROM utilizadores
UNION ALL
SELECT 
    'localizacoes' as tabela, 
    COUNT(*) as total 
FROM localizacoes;
```

## Resultado Esperado:
```
tabela        | total
--------------+-------
utilizadores  | 2
localizacoes  | 3
```

## Dicas Importantes:

1. **Executar um comando de cada vez** - Não colar tudo junto
2. **Verificar erros** - Railway mostra erros na consola
3. **Testar ligação** - Primeiro fazer `SELECT 1;` para testar
4. **Backup automático** - Railway faz backup automático
5. **Variáveis automáticas** - Railway define DATABASE_URL automaticamente

## Troubleshooting:

**Erro "permission denied":**
- Railway já dá permissões necessárias automaticamente

**Erro "table already exists":**
- Normal, `IF NOT EXISTS` previne erro

**Erro de conexão:**
- Verificar se base PostgreSQL está a correr no Railway

**Dados não aparecem:**
- Verificar se INSERT foi executado com sucesso
- Fazer `SELECT * FROM utilizadores;` para confirmar