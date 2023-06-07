0. [Installation and installing in editable mode](https://alembic.sqlalchemy.org/en/latest/front.html#installation)
1. [Creating Environment](https://alembic.sqlalchemy.org/en/latest/tutorial.html#creating-an-environment)
2. To Creating Migrations Location Use the following >> alembic init src/infra/data/migrations  <<
3. [Editing the .ini File](https://alembic.sqlalchemy.org/en/latest/tutorial.html#editing-the-ini-file)
4. Create __init__.py under migrations folder
5. Move alembic.ini under migrations folder
6. Confirm script_location under alembic section
7. Comment sqlalchemy.url
8. [Change Basic Formatter Configuration](https://alembic.sqlalchemy.org/en/latest/autogenerate.html#basic-formatter-configuration)
9. Modify hooks to autopep8 shown in documentation
10. Comment Logger Configuration in alembic.ini
11. Modify env.py as required -> Check #CUSTOM-MODIFICATION
12. Add target_metadata
13. Modify run_migrations_online
14. Add MigrationEngine class
15. [Create a Migration Script](https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script)
16. To generate migration script set APPLY_MIGRATIONS & ALEMBIC_CONFIG
17. export APPLY_MIGRATIONS=0
18. export ALEMBIC_CONFIG=src/infra/data/migrations/alembic.ini
19. Run <<alembic revision --autogenerate -m "create user table">>
20. Generation of migration script at >> src/infra/data/migrations/versions/c9af2226c4d8_create_user_table.py
21. set APPLY_MIGRATIONS=1 by running >> export APPLY_MIGRATIONS=1
22. Run Development Server