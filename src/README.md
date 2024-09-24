# Source Files Documentation

# API Documentation
- apiDocumentation.qmd 
- app.py

In order to Create the API Documentation, you must run app.py to create a local host for the 
API Documentation.

Run Steps:
1. Install flask, Quarto & SQL
2. Run app.py
3. Run Quarto on ApiDocumentation
4. Open Local Host URL given.

# Database Source Code
- Game Database.qmd
- GameDB-ddl.qmd
- GameDN-DML.sql

Game Database.qmd is a renderable documentation to determine if one is succesfully connected to the 
database

GameDB-ddl.qmd is a documentation that is used to create the Database.

GameDN-dml.sql is a documentation that is used to insert information into the database.

Rendering Steps:
1. Render Game Database.qmd
2. Run GameDB-ddl.qmd, First
3. Run GameDN-DML.sql, Second
