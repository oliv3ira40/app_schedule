
# Deploy de Aplicação Django no Ubuntu 24.04 com PostgreSQL e Nginx

Este documento fornece um guia passo a passo para fazer o deploy de uma aplicação Django no Ubuntu 24.04 usando PostgreSQL e Nginx. Ele também inclui as soluções para problemas comuns encontrados durante o processo.

## Pré-requisitos
- Um VPS rodando Ubuntu 24.04
- Acesso SSH ao servidor
- Um projeto Django armazenado em um repositório Git
- Banco de dados PostgreSQL
- Ainda sem domínio; o app será acessado via IP do servidor

## Passos para o Deploy

### 1. Conectar ao Servidor
Use SSH para se conectar ao servidor:
```bash
ssh usuario@ip_do_servidor
```

### 2. Atualizar o Sistema
Certifique-se de que o sistema está atualizado:
```bash
sudo apt update && sudo apt upgrade -y
```

### 3. Instalar Pacotes Necessários
Instale Python, PostgreSQL e Nginx, além de outros pacotes necessários:
```bash
sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl -y
```

### 4. Clonar o Projeto do Git
Navegue até o diretório apropriado e clone o projeto:
```bash
cd /var/www
sudo git clone https://github.com/seu-usuario/seu-projeto.git
```

### 5. Configurar o PostgreSQL
1. Troque para o usuário PostgreSQL:
    ```bash
    sudo -i -u postgres
    ```

2. Abra o shell do PostgreSQL e crie o banco de dados e o usuário:
    ```bash
    psql
    CREATE DATABASE nome_do_banco;
    CREATE USER usuario_banco WITH PASSWORD 'senha';
    ALTER ROLE usuario_banco SET client_encoding TO 'utf8';
    ALTER ROLE usuario_banco SET default_transaction_isolation TO 'read committed';
    ALTER ROLE usuario_banco SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE nome_do_banco TO usuario_banco;
    \q
    exit
    ```

### 6. Configurar Ambiente Virtual Python
Navegue até o diretório do projeto e configure um ambiente virtual:
```bash
cd /var/www/seu-projeto
python3 -m venv venv
```

- **Possíveis erros deste passo**:
  - **Erro**: `python3 -m venv venv` falha devido à ausência do `python3-venv`.
  - **Solução**: Instalar o pacote `python3-venv`:
    ```bash
    sudo apt install python3.12-venv
    ```

Ative o ambiente virtual:
```bash
source venv/bin/activate
```

### 7. Instalar Dependências do Projeto
Instale as dependências necessárias:
```bash
pip install -r requirements.txt
```

### 8. Configurar Variáveis de Ambiente
Crie um arquivo `.env` para armazenar as variáveis de ambiente, como `SECRET_KEY` e a configuração do banco de dados:
```bash
nano .env
```
Exemplo de configuração:
```
SECRET_KEY=sua_chave_secreta
DEBUG=False
ALLOWED_HOSTS=['ip_do_servidor']
DATABASE_URL=postgres://usuario_banco:senha@localhost/nome_do_banco
```

### 9. Aplicar Migrações
Execute as migrações no banco de dados:
```bash
python manage.py migrate
```

### 10. Coletar Arquivos Estáticos
Execute o comando `collectstatic` para reunir os arquivos estáticos no `STATIC_ROOT`:
```bash
python manage.py collectstatic --noinput
```

- **Possíveis erros deste passo**:
  - **Erro**: Problemas relacionados a arquivos estáticos não sendo servidos corretamente, como ausência de estilos no Django Admin.
  - **Solução**:
    - Certifique-se de que o comando `collectstatic` foi executado corretamente.
    - Verifique a configuração do Nginx para servir os arquivos estáticos.

### 11. Configurar o Gunicorn
Instale o Gunicorn e teste-o:
```bash
pip install gunicorn
gunicorn --workers 3 seu_projeto.wsgi:application
```

### 12. Configurar o Gunicorn como um Serviço no Systemd
Crie um arquivo de serviço para o Gunicorn:
```bash
sudo nano /etc/systemd/system/gunicorn.service
```

Adicione a seguinte configuração (ajuste os caminhos conforme necessário):
```
[Unit]
Description=gunicorn daemon para o projeto Django
After=network.target

[Service]
User=seu-usuario
Group=www-data
WorkingDirectory=/var/www/seu-projeto
ExecStart=/var/www/seu-projeto/venv/bin/gunicorn --workers 3 --bind unix:/var/www/seu-projeto/gunicorn.sock seu_projeto.wsgi:application

[Install]
WantedBy=multi-user.target
```

Inicie e habilite o serviço Gunicorn:
```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

### 13. Configurar o Nginx
Crie um arquivo de configuração para o seu site no Nginx:
```bash
sudo nano /etc/nginx/sites-available/seu-projeto
```

Adicione a seguinte configuração (substitua os caminhos conforme necessário):
```
server {
    listen 80;
    server_name ip_do_servidor;

    location /static/ {
        alias /var/www/seu-projeto/staticfiles/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/seu-projeto/gunicorn.sock;
    }
}
```

Ative o site criando um link simbólico:
```bash
sudo ln -s /etc/nginx/sites-available/seu-projeto /etc/nginx/sites-enabled
```

Teste a configuração do Nginx:
```bash
sudo nginx -t
```

Reinicie o Nginx:
```bash
sudo systemctl restart nginx
```

### 14. Abrir as Portas no Firewall
Permitir tráfego HTTP e HTTPS usando o UFW:
```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

Verifique o status do firewall:
```bash
sudo ufw status
```

### 15. Criar um Superusuário
Crie um superusuário no Django admin:
```bash
python manage.py createsuperuser
```

### 16. Acessar a Aplicação
Abra o navegador e vá para `http://ip_do_servidor/admin/` para fazer login como superusuário.

---

Este documento fornece um guia completo para o deploy de sua aplicação Django, com soluções para problemas comuns encontrados durante o processo.
