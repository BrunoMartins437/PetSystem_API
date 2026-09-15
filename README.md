# PetSystem API

Este projeto consiste na API RESTful do sistema **PetSystem**, desenvolvida como parte do material didático da disciplina **Desenvolvimento Full Stack Básico**.

O objetivo desta API é fornecer os endpoints necessários para o gerenciamento completo de cadastros de pets (CRUD: criação, leitura, atualização e exclusão), incluindo suporte a upload de fotos de perfil e integração com o frontend.

---

## 🛠️ Tecnologias e Requisitos (`requirements.txt`)

Certifique-se de ter o **Python 3.9+** instalado na sua máquina. 

O arquivo `requirements.txt` do projeto deve conter as seguintes dependências principais:

```text
Flask==3.0.0
flask-cors==4.0.0
flasgger==0.9.7.1
flask-openapi3==3.0.0
Flask-SQLAlchemy==3.1.1
Pillow==10.1.0
pydantic==2.5.2
werkzeug==3.0.1
```

* **Flask**: Framework web leve para construção das rotas da API.
* **flask-cors**: Gerenciamento das permissões de requisição de origens cruzadas (CORS) para comunicação com o frontend.
* **flask-openapi3 / flasgger / pydantic**: Geração e validação automática da documentação OpenAPI/Swagger.
* **Flask-SQLAlchemy**: ORM para abstração e persistência de dados.
* **Pillow**: Processamento e manipulação dos arquivos de imagem/foto enviados.

---

## 🚀 Rotas Disponíveis

| Método | Rota | Descrição |
| :--- | :--- | :--- |
| `GET` | `/pets` | Lista os pets cadastrados ou realiza buscas com filtros. |
| `POST` | `/pets` | Cadastra um novo pet (aceita formulário `multipart/form-data` com foto). |
| `PUT` | `/pets/<id>` | Atualiza parcialmente os dados de um pet existente. |
| `DELETE` | `/pets/<id>` | Remove um pet do sistema pelo seu ID. |

---

## ⚙️ Como Executar

Para executar a API na sua máquina local, siga os passos descritos abaixo.

### 1. Clonar o repositório
Acesse o diretório onde deseja armazenar o projeto e clone o repositório via terminal:
```bash
git clone <URL_DO_REPOSITORIO>
cd petsystem-api
```

### 2. Criar e ativar o ambiente virtual
É fortemente indicado o uso de ambientes virtuais do tipo `virtualenv` para isolar as dependências:

* **Linux / macOS:**
  ```bash
  python3 -m venv env
  source env/bin/activate
  ```

* **Windows (PowerShell):**
  ```powershell
  python -m venv env
  .\env\Scripts\activate
  ```

### 3. Instalar as dependências
Com o ambiente virtual ativado `(env)`, execute o comando abaixo para instalar todas as bibliotecas necessárias:
```bash
pip install -r requirements.txt
```

### 4. Executar a aplicação
Com as dependências instaladas, inicie o servidor da API executando:
```bash
flask run --host 0.0.0.0 --port 5000
```

> **Modo de Desenvolvimento:** Para permitir que o servidor reinicie automaticamente a cada alteração realizada no código fonte, utilize o parâmetro `--reload`:
> ```bash
> flask run --host 0.0.0.0 --port 5000 --reload
> ```

---

## 📖 Documentação Interativa (Swagger)

Após iniciar o servidor, abra o seu navegador e acesse a URL abaixo para visualizar e testar todos os endpoints da API através da interface interativa do Swagger:

👉 **[http://localhost:5000/#/](http://localhost:5000/#/)**