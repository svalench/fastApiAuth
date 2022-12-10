# Документация

### 1. Миграции и ORM

В качестве ORM используется [tortoise](https://tortoise-orm.readthedocs.io/).  
Дя проведения миграций используется [aerich](https://github.com/tortoise/aerich).
[Дока](https://tortoise-orm.readthedocs.io/en/latest/migration.html#quick-start)

Чтобы применить миграции выполните команду:
```
aerich migrate  --name namemigration
aerich upgrade
```
