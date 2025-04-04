# Projeto Verdinho 1.5

Este projeto é uma aplicação que utiliza inteligência artificial para recomendar plantas e analisar dados de reflorestamento, incluindo análise de NDVI (Índice de Vegetação por Diferença Normalizada).

## Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Google Earth Engine account (para funcionalidades de NDVI)
- Google Cloud SDK (gcloud)
- Earth Engine Python API

### Instalação do Google Cloud SDK e Earth Engine

1. Instale o Google Cloud SDK:
```bash
# Adicione a URI de distribuição do Google Cloud SDK como fonte de pacotes
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

# Atualize e instale o Google Cloud SDK
sudo apt-get update
sudo apt-get install google-cloud-sdk
```

2. Inicialize o gcloud e autentique:
```bash
gcloud init
```

3. Instale a API do Earth Engine:
```bash
pip install earthengine-api
```

4. Autentique o Earth Engine:
```bash
earthengine authenticate
```

5. Configure o Google Earth Engine:
   - Crie uma conta no [Google Earth Engine](https://earthengine.google.com/)
   - Solicite ao João (proprietário do projeto) para adicionar seu email ao projeto com as seguintes permissões:
     1. Gravador de recursos do Earth Engine (Earth Engine Resource Writer)
     2. Consumidor do Service Usage (Service Usage Consumer)
   - Após receber a confirmação de que foi adicionado ao projeto, execute o comando de autenticação:
   ```bash
   earthengine authenticate
   ```

**Nota**: Sem as permissões concedidas pelo João, não será possível utilizar as funcionalidades de NDVI do projeto.

## Configuração do Ambiente

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITÓRIO]
cd "Projeto Verdinho 1.5"
```

2. Crie um ambiente virtual Python:
```bash
python -m venv venv
```

3. Ative o ambiente virtual:

No Linux/Mac:
```bash
source venv/bin/activate
```

No Windows:
```bash
.\venv\Scripts\activate
```

4. Instale as dependências:
```bash
cd ia
pip install -r requirements.txt
```

5. Configure o Google Earth Engine:
   - Crie uma conta no [Google Earth Engine](https://earthengine.google.com/)
   - Certifique-se de ter as seguintes permissões no projeto:
     1. Gravador de recursos do Earth Engine (Earth Engine Resource Writer)
     2. Consumidor do Service Usage (Service Usage Consumer)
   - Execute o comando de autenticação:
   ```bash
   earthengine authenticate
   ```

## Estrutura do Projeto

- `ia/` - Diretório principal do backend Python
  - `api_ia.py` - API principal com endpoints Flask
  - `geolocalizacao.py` - Módulo de geolocalização
  - `*.joblib` - Modelos de machine learning
  - `*.csv` - Datasets e embeddings
- `verdinho/` - Diretório do frontend

## Executando o Projeto

1. Certifique-se de que o ambiente virtual está ativado

2. Inicie o servidor backend:
```bash
cd ia
python api_ia.py
```

O servidor estará disponível em `http://localhost:5000`

## Endpoints da API

- `/recomendar` (POST) - Recomenda plantas baseado em condições ambientais
- `/melhor-planta` (POST) - Encontra a melhor planta para uma localização específica
- `/ndvi-real` (POST) - Calcula o NDVI para uma localização
- `/adicionar-planta` (POST) - Adiciona uma nova planta ao sistema

## Desenvolvimento

Para desenvolvimento, recomenda-se:
1. Manter o ambiente virtual ativado durante o desenvolvimento
2. Usar um editor com suporte a Python (VS Code recomendado)
3. Instalar extensões Python relevantes no VS Code

## Solução de Problemas

Se encontrar problemas com o Google Earth Engine:
1. Verifique se sua conta está ativa
2. Reautentique usando `earthengine authenticate`
3. Verifique se o projeto 'ndvi-reflorestamento' está configurado corretamente

## Contribuindo

1. Crie uma branch para sua feature
2. Faça commit das mudanças
3. Envie um pull request

## Licença

[Adicione informações sobre a licença do projeto]
