# Projeto 1 Megadados - API REST de filmes com SQL

# Para rodar o servidor local:
1. Clone o repositório: 
```sh 
git clone https://github.com/insper-classroom/23-1-projeto-sql-registrogeral
```
2. Baixe as dependências: 
```sh 
pip install -r requirements.txt
```
3. Coloque as credenciais necessarias em um arquivo .env
```sh
export MD_DB_SERVER="{SEU_SERVIDOR_MYSQL}"
export MD_DB_USERNAME="{SEU_USUARIO}"
export MD_DB_PASSWORD="{SUA_SENHA}" 
```
4. Crie o banco de dados no MYSQL WORKBENCH ou utilizando o script que fizemos.
```sh
python create_or_reset_db.py
```
5. Rode o servidor com: 
```sh
uvicorn main:app --reload
```

# Diagrama do banco de dados:

![Diagrama do banco de dados](diagrama.png "Diagrama")


# Vídeo do projeto:

[![Thumbnail do video](http://img.youtube.com/vi/_TvoIRiWiOU/0.jpg)](https://youtu.be/_TvoIRiWiOU "Demonstração da API")

# Vídeo do projeto parte 2:

[![Thumbnail do video](http://img.youtube.com/vi/DHtEh5DUFto/0.jpg)](https://youtu.be/DHtEh5DUFto "Demonstração da API com ORM")

# Alunos:
- [Guilherme Fontana Louro](https://github.com/guifl2001)
- [Ricardo Ribeiro Rodrigues](https://github.com/RicardoRibeiroRodrigues)