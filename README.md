### Esboço do projeto para gerenciar clientes e serviços prestados

### Comandos úteis

```bash

# Iniciar o projeto
$ python manage.py runserver

# Criar o banco de dados
$ python manage.py migrate

# Criar um super usuário
$ python manage.py createsuperuser

# Compilar as mensagens
$ python manage.py compilemessages

# Criar a env
$ python -m venv venv

# Ativar a env
$ source {nome da env}/bin/activate

# Desativar a env
$ deactivate

# Criar arquivo requirements.txt
$ pip freeze > requirements.txt

# Mandar dependências para o arquivo requirements.txt
$ pip freeze > requirements.txt

# Instalar as dependências
$ pip install -r requirements.txt

# Link para a documentação do unfold:
[Git Django Unfold](https://github.com/unfoldadmin/django-unfold)

# Reiniciar o gunicorn
sudo systemctl restart gunicorn
# Reiniar o nginx
sudo systemctl restart nginx

# Coletar arquivos estáticos
python manage.py collectstatic --noinput

```
