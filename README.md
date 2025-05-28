# 📚 API de Atividades

Esta API gerencia atividades escolares, permitindo listar, criar atividades, adicionar respostas dos alunos, atualizar notas e deletar atividades.

---

## ⚙ Como Rodar

```bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
docker build -t activities
docker run -d -p 5003:5003 --name activities activities -d
```

---

## 🛠️ Endpoints

---

### 🔍 GET `/`

Lista todas as atividades cadastradas, enriquecendo os dados com informações do professor e das respostas dos alunos.

#### ✅ Exemplo de resposta:

```json
[
  {
    "id": 1,
    "id_disciplina": 3,
    "professor_id": 2,
    "enunciado": "Explique a teoria da relatividade",
    "professor": {
      "id": 2,
      "nome": "Ana Paula",
      "disciplina": "Física"
    },
    "respostas": [
      {
        "id_aluno": 10,
        "resposta": "A teoria foi formulada por Einstein...",
        "nota": 9,
        "aluno": {
          "id": 10,
          "nome": "João Silva"
        }
      }
    ]
  }
]
```

---

### ➕ POST `/`

Cria uma nova atividade.

#### 📥 Corpo da requisição (JSON):

```json
{
  "id_disciplina": 3,
  "professor_id": 2,
  "enunciado": "Descreva a fotossíntese"
}
```

#### ✅ Exemplo de resposta:

```json
{
  "mensagem": "Atividade criada com sucesso",
  "atividade": {
    "id": 5,
    "id_disciplina": 3,
    "professor_id": 2,
    "enunciado": "Descreva a fotossíntese",
    "professor": {
      "id": 2,
      "nome": "Ana Paula",
      "disciplina": "Física"
    },
    "respostas": []
  }
}
```

#### ❌ Resposta de erro (400 - Bad Request):

```json
{
  "erro": "id_disciplina, professor_id e enunciado são obrigatórios"
}
```

---

### ➕ POST `/<id_atividade>/respostas`

Adiciona uma resposta para uma atividade específica.

#### 🔗 Parâmetros de rota:

* `id_atividade` *(integer)*: ID da atividade.

#### 📥 Corpo da requisição (JSON):

```json
{
  "id_aluno": 10,
  "resposta": "Minha resposta detalhada..."
}
```

#### ✅ Exemplo de resposta:

```json
{
  "mensagem": "Resposta adicionada com sucesso",
  "resposta": {
    "id_aluno": 10,
    "resposta": "Minha resposta detalhada...",
    "nota": null
  }
}
```

#### ❌ Resposta de erro (400 - Bad Request):

```json
{
  "erro": "id_aluno e resposta são obrigatórios"
}
```

#### ❌ Resposta de erro (404 - Not Found):

```json
{
  "erro": "Atividade não encontrada"
}
```

---

### ✏️ PUT `/<id_atividade>/respostas/<id_aluno>/nota`

Atualiza a nota da resposta de um aluno para uma atividade específica.

#### 🔗 Parâmetros de rota:

* `id_atividade` *(integer)*: ID da atividade.
* `id_aluno` *(integer)*: ID do aluno.

#### 📥 Corpo da requisição (JSON):

```json
{
  "nota": 8.5
}
```

#### ✅ Exemplo de resposta:

```json
{
  "mensagem": "Nota atualizada com sucesso",
  "resposta": {
    "id_aluno": 10,
    "resposta": "Minha resposta detalhada...",
    "nota": 8.5
  }
}
```

#### ❌ Resposta de erro (400 - Bad Request):

```json
{
  "erro": "O campo \"nota\" é obrigatório"
}
```

#### ❌ Resposta de erro (404 - Not Found):

```json
{
  "erro": "Atividade não encontrada"
}
```

#### ❌ Resposta de erro (404 - Not Found):

```json
{
  "erro": "Resposta para aluno não encontrada"  // Exemplo de ValueError tratado
}
```

---

### 🗑️ DELETE `/<id_atividade>`

Deleta uma atividade pelo seu ID.

#### 🔗 Parâmetros de rota:

* `id_atividade` *(integer)*: ID da atividade.

#### ✅ Exemplo de resposta:

* Status HTTP: 204 No Content
  Sem corpo de resposta.

#### ❌ Resposta de erro (404 - Not Found):

```json
{
  "erro": "Atividade não encontrada"
}
```
