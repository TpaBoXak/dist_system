# Создание Реплики
1. docker-compose up -d - создание контейнеров
2. docker exec -it postgresql_01 bash - подключение к первому контейнеру
3. su - postgres заходим под пользователем postgres
4. createuser --replication -P repluser - создание пользователя для реплики
5. exit -> exit - выход из контейнера
6. ./postgresql_01/postgresql.conf - добовляем в файл:
wal_level = replica
max_wal_senders = 2
max_replication_slots = 2
hot_standby = on
hot_standby_feedback = on
7. docker network inspect postgresql_default | grep Subnet - узнаем адресс сети
8. ./postgresql_01/pg_hba.conf - добавляем в файл:
host    replication     all             172.21.0.0/16           md5
9. docker restart postgresql_01
10. docker exec -it postgresql_02 bash - заходим во второй контейнер
11. sudo rm -rf /var/lib/postgresql/data/* - удаляем данные
12. su - postgres -c "pg_basebackup --host=postgresql_01 --username=repluser --pgdata=/var/lib/postgresql/data --wal-method=stream --write-recovery-conf"
# Проверка реплики
1. Смотрим статус работы главного:
docker exec -it postgresql_01 su - postgres -c "psql -c 'select * from pg_stat_replication;'"
2. Смотрим статус работы реплики:
docker exec -it postgresql_02 su - postgres -c "psql -c 'select * from pg_stat_wal_receiver;'"