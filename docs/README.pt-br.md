# Recomendação de perfumes com base em gostos do usuário

[![en](https://img.shields.io/badge/lang-en-red.svg)](../README.md) [![pt-br](https://img.shields.io/badge/lang-pt--br-green.svg)](README.pt-br.md)

## Caso de Uso
Esta aplicação tem como objetivo fornecer recomendações inteligentes de perfumes com base nas preferências pessoais de cada usuário. A API permite que os usuários informem quais perfumes possuem, quais gostam, quais não gostam, além de notas e acordes olfativos que apreciam ou desejam evitar.

Com base nessas informações, aliadas a dados contextuais — como clima, estação do ano e turno do dia em que o perfume será usado —, a API filtra e sugere perfumes ideais, respeitando os critérios de preferência e evitando fragrâncias indesejadas ou já adquiridas.

A base de perfumes armazenada contém atributos ricos, como acordes, notas, recomendações de uso e imagem ilustrativa. A recomendação é feita de forma dinâmica: o usuário pode fornecer filtros personalizados na chamada da API ou, caso prefira, a recomendação será baseada unicamente em seu perfil salvo na base de dados.

Essa abordagem torna a experiência altamente personalizada, útil tanto para consumidores em busca do próximo perfume ideal quanto para e-commerces ou marketplaces que desejam oferecer recomendações mais assertivas e contextuais.


## 🚀 Passo a Passo do processo de Recomendação de Perfumes

### 1. 📥 Recebimento da Requisição

A API recebe uma requisição com o seguinte payload (todos os campos são opcionais):

```json
{
   "ownedPerfumes": ["1", "2", "3"],
   "likedPerfumes": ["3"],
   "notLikedPerfumes": ["4"],
   "likedNotes": ["vanilla", "eucalyptus"],
   "notLikedNotes": ["pine", "oud"],
   "likedAccords": ["leather", "sweet"],
   "notLikedAccords": ["balsamic", "powdery"], 
   "dayShifts": ["night"], 
   "climates": ["cold"],
   "seasons": ["winter", "spring"]
}
```

### 2. 🧠 Definição dos Critérios de Filtro

- Se o input da requisição contiver filtros, eles são utilizados.
- Caso contrário, são utilizados os dados previamente salvos no perfil do usuário.
- Caso nenhum dado esteja presente, o sistema pode retornar perfumes genéricos ou mais populares (opcional).

### 3. 🧩 Enriquecimento de Dados com Inferência

Para perfumes que não possuem informações de uso (clima, turno, estação), o sistema infere essas informações com base nos acordes usando regras predefinidas.

### 4. 🔍 Montagem da Consulta no MongoDB

A consulta aplica as seguintes regras:

- ❌ Exclui:
  - Perfumes que o usuário já possui.
  - Perfumes que o usuário não gosta.
  - Perfumes com notas ou acordes que o usuário não gosta.


- ✅ Inclui:
  - Perfumes compatíveis com o clima, turno e estação informados.
  - Perfumes com notas/acordes preferidos.
  - Perfumes similares aos que o usuário gosta, analisando os acordes e notas mais comuns entre eles.


### 5. 🎯 Priorização de Resultados

Os perfumes são ordenados com base em:
- Compatibilidade com o contexto de uso (ex: exclusivamente noturno se "night" foi solicitado).
- Quantidade de características em comum com os perfumes que o usuário gosta.
- Presença de notas e acordes desejados.

### 6. 📤 Retorno da Recomendação
- A API retorna até 10 perfumes recomendados.
- Exemplo de retorno:

```json
{
  "items": [
    {
      "_id": "23569",
      "name": "shisha-lounge",
      "brand": "ricardo-ramos-perfumes-de-autor",
      "top_notes": [ "anise", "red fruits", "hazelnut", "neroli" ],
      "mid_notes": [ "tobacco", "labdanum", "oakmoss", "patchouli" ],
      "base_notes": [ "amber", "madagascar vanilla", "tonka bean", "musk" ],
      "accords": [ "sweet", "amber", "anis", "soft spicy", "tobacco" ],
      "day_shifts": [ "night" ],
      "climates": [ "cold" ],
      "seasons": [ "winter" ],
      "url": "https://www.fragrantica.com/perfume/ricardo-ramos-perfumes-de-autor/shisha-lounge-58575.html",
      "image_url": "https://fimgs.net/mdimg/perfume/375x500.58575.jpg",
      "rating": 4.46,
      "match_probability": 0.53
    }
  ]
}
```

### 7. 📤 Retorno da Busca de Pefumes
- A API retorna até 10 perfumes encontrados com o os dados fornecidos.
- Exemplo de retorno:

```json
{
  "items": [
    {
      "_id": "4467",
      "name": "Invictus Paco Rabanne",
      "brand": "paco-rabanne",
      "url": "https://www.fragrantica.com/perfume/paco-rabanne/invictus-18471.html",
      "image_url": "https://fimgs.net/mdimg/perfume/375x500.18471.jpg",
      "rating": 3.73,
      "score": 0.6666666666666666
    }
  ]
}
```

---

## 🛠️ Passo a Passo para Rodar o Projeto Localmente

### 1. 📦 Pré-requisitos

Certifique-se de que você tem instalado:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- Python 3.10+ com `pip`


### 2. 🐳 Subindo os Serviços com Docker Compose

1. Clone o repositório do projeto:

```bash
  git clone https://github.com/rodrigogmartins/perfume-recommendations.git
  cd perfume-recommendations
```

2. Suba o MongoDB

```bash
  docker-compose up -d
```


### 3. 📚 Criar Ambiente Virtual e Instalar Dependências

```bash
  python -m venv venv
  source venv/bin/activate  # no Windows use: venv\Scripts\activate
  pip install -r requirements.txt
```


### 4. 📥 Popular o Banco de Dados com Perfumes

Execute o script para salvar os dados de perfumes do dataset no MongoDB:

```bash
  python -m scripts.fill_perfume_dataset
```

Esse script:
- Lê o arquivo .csv com perfumes.
- Faz inferência de uso (clima, estação, turno).
- Monta a URL da imagem do perfume.
- Insere os perfumes na coleção perfumes no MongoDB.

#### 4.1. Consultar perfumes no Banco de Dados

```bash
  docker exec -it mongodb mongosh -u root -p example
  use perfume_db
  db.perfumes.find().limit(5).pretty()
```

### 5. 🚀 Rodar a API

Com tudo instalado, rode a aplicação localmente:

```bash
  python server.py
```

A API estará disponível em: http://localhost:8000


### 6. 📘 Acessar a Documentação

Acesse a documentação Swagger da API:

```bash
  http://localhost:8000/docs
```


### 7. 🧪 Testar as Requisições

```bash
  curl --request POST \
    --url http://localhost:8000/api/perfumes/recommendations \
    --header 'Content-Type: application/json' \
    --scripts '{
      "ownedPerfumes": ["1", "2", "3"],
      "likedPerfumes": ["1", "4"],
      "notLikedPerfumes": [],
      "notLikedNotes": ["pine", "oud"],
      "notLikedAccords": ["balsamic", "powdery"],
      "dayShifts": ["night"],
      "climates": ["cold"]
    }'
```

```bash
  curl --request GET \
    --url 'http://localhost:8000/api/perfumes/search?query=invictus'
```

### 8. 🧹 Encerrar os Serviços

Para parar os serviços do Docker:

```bash
  docker-compose down
```

---

## 📊 Dados Utilizados

Este projeto utiliza dados coletados a partir da comunidade de usuários do Fragrantica, organizados no dataset "Fragrantica.com Fragrance Dataset" disponível em [https://www.kaggle.com/datasets/olgagmiufana1/fragrantica-com-fragrance-dataset](https://www.kaggle.com/datasets/olgagmiufana1/fragrantica-com-fragrance-dataset).

**Créditos:**  
Dataset organizado por [Olga G](https://www.kaggle.com/olgagmiufana1)  
Licença: [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)

Modificações foram realizadas para inferência de clima, estação e turno de uso dos perfumes.  
Distribuição e uso estão em conformidade com a licença, sem fins comerciais.


