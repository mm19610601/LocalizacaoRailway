# Metodologia do Sistema de Rastreamento

## 1. Como a Aplicação Chega ao Desktop

### Opção A: Acesso via Replit (Atual)
- URL temporária do Replit: `https://seu-projeto.replit.dev`
- Acesso direto pelo navegador no desktop
- Funciona enquanto o Replit estiver ativo

### Opção B: Deploy no Railway (Recomendado)
- Deploy da aplicação Flask no Railway
- URL permanente: `https://seu-app.railway.app`
- Funciona 24/7 sem depender do Replit

## 2. Como Enviar Localizações do Telefone

### Método 1: Aplicação Android (Recomendado)
```java
// Código básico Android para enviar localização
private void enviarLocalizacao(double lat, double lon, double precisao) {
    String url = "https://seu-app.railway.app/location/add";
    
    // Criar formulário POST
    RequestBody formBody = new FormBody.Builder()
        .add("user_id", "1")  // ID do utilizador
        .add("latitude", String.valueOf(lat))
        .add("longitude", String.valueOf(lon))
        .add("precisao", String.valueOf(precisao))
        .build();
    
    // Enviar requisição
    OkHttpClient client = new OkHttpClient();
    Request request = new Request.Builder()
        .url(url)
        .post(formBody)
        .build();
}
```

### Método 2: App Web no Telefone (Mais Simples)
- Criar página web que acede ao GPS do telefone
- JavaScript para obter localização
- Enviar automaticamente para o servidor

### Método 3: Tasker (Android) + HTTP Request
- Configurar Tasker para obter GPS
- Enviar HTTP POST para o endpoint `/location/add`

## 3. Como Testar o Railway

### Passo 1: Criar Conta no Railway
1. Ir a https://railway.app
2. Fazer login com GitHub
3. Criar novo projeto

### Passo 2: Configurar PostgreSQL no Railway
1. No Railway: "New" → "Database" → "PostgreSQL"
2. Anotar as credenciais da base de dados
3. Executar o script `database_setup.sql` na consola do PostgreSQL

### Passo 3: Deploy da Aplicação
1. Conectar repositório GitHub ao Railway
2. Configurar variáveis de ambiente:
   - `DATABASE_URL`: URL da base PostgreSQL
   - `SESSION_SECRET`: chave secreta para sessões
3. Railway faz deploy automático

### Passo 4: Testar Endpoints
```bash
# Testar se a aplicação está a funcionar
curl https://seu-app.railway.app/

# Testar endpoint de localização
curl -X POST https://seu-app.railway.app/location/add \
  -d "user_id=1&latitude=39.5&longitude=-8.7&precisao=10"

# Testar API de localizações
curl https://seu-app.railway.app/api/locations
```

## 4. Fluxo de Trabalho Completo

```
[Telefone Android] 
    ↓ (GPS + HTTP POST)
[Railway PostgreSQL] 
    ↓ (Query dados)
[Aplicação Web Flask] 
    ↓ (Render mapa)
[Desktop Browser]
```

## 5. Próximos Passos Recomendados

1. **Testar Railway**: Criar conta e fazer deploy
2. **Criar app Android simples**: Para enviar localizações
3. **Testar com dados reais**: Verificar se tudo funciona
4. **Otimizar**: Melhorar interface e funcionalidades

## 6. URLs de Teste

- **Desenvolvimento**: http://localhost:5000
- **Replit**: https://seu-projeto.replit.dev  
- **Railway**: https://seu-app.railway.app (após deploy)

## 7. Estrutura de Dados para Telefone

```json
{
  "user_id": 1,
  "latitude": 39.500000,
  "longitude": -8.700000,
  "precisao": 9.5,
  "timestamp": "2025-07-25T21:30:00Z"
}
```