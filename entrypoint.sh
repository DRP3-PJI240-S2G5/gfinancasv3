#!/bin/sh

# Esperar o banco de dados estar disponível
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "Esperando pelo banco de dados..."
  sleep 1
done

# Banco ok
echo "Banco de dados ok..."

sleep 5



# Verificar se as migrações já foram aplicadas
if [ ! -f /app/user_admin_created ]; then
  # Aplicar as migrações do Django
  echo "Make migrations"
  python manage.py makemigrations
  echo "Migrate"
  python manage.py migrate

  # Criar o usuário admin
  echo "Criando usuario admin"
  #python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@mail.com', '123mudar!')"
  python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@mail.com', 'admin01!')"

  # Criar o arquivo de flag
  touch /app/user_admin_created
fi

# Executar o comando passado (inicialização do servidor Django)
exec "$@"