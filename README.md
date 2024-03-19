# Flask API Example

This project is a simple CRUD (Create, Read, Update, Delete) API built with Python's Flask framework and PostgreSQL as the database.
Created for fun only.

## Specifications

The API operates on a table with the following columns:

- String
- Int
- Primary Key
- Date (two columns)
- Boolean
- Datetime

## Operations

The API supports the following operations:

- **CREATE**: Inserts new entries into the table.
- **READ**: Retrieves all entries from the table.
- **UPDATE**: Modifies existing entries in the table. Requires the column name and the new value.
- **DELETE**: Removes entries from the table. Requires either the ID or NAME as a parameter.

## Setup

To run this project, you need to install the following:

- PostgreSQL: The database used by the API.
- DBeaver (optional): A database management tool.
- Postman: A tool for testing APIs.
- Python: The programming language used to build the API.

You also need to install the following Python libraries:

- Flask: A lightweight web framework.
- Flask-SQLAlchemy: An extension for Flask that adds support for SQLAlchemy.
- SQLAlchemy: A SQL toolkit and ORM.
- Psycopg2: A PostgreSQL adapter for Python.


## Preparation

Prepare for using this project.

### PostgreSQL Setup

1. **Install PostgreSQL:** Use the following commands to install PostgreSQL and its additional modules:

    ```bash
    sudo apt-get update
    sudo apt-get install postgresql postgresql-contrib
    ```

2. **Start PostgreSQL service:** Start the PostgreSQL service with the following command:

    ```bash
    sudo service postgresql start
    ```

3. **Access PostgreSQL command line:** Switch to the `postgres` user and access the PostgreSQL command line:

    ```bash
    sudo su - postgres
    psql
    ```

4. **Create a database and a user:** Create a new PostgreSQL user and a new database, and grant all privileges on the database to the user:

    ```sql
    CREATE USER angeliav WITH PASSWORD 'Angel14^_^';
    CREATE DATABASE flask_example;
    GRANT ALL PRIVILEGES ON DATABASE flask_example TO angeliav;
    \q
    ```

    Then exit the PostgreSQL command line and the `postgres` user:

    ```bash
    exit
    ```

5. **Login to the new database and create a table:** Login to the new database as the new user and create a table:

    ```bash
    psql -h localhost -U angeliav -d flask_example
    ```

    Then create a `users` table:

    ```sql
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        is_active BOOLEAN DEFAULT TRUE
    );
    ```

### Python & Libraries Setup

1. **Set up a virtual environment:** Use the following commands to create and activate a virtual environment:

    ```bash
    python3 -m venv env
    source env/bin/activate # Linux
    . .\env\Scripts\activate # Powershell
    ```

2. **Install dependencies:** Use the following commands to install the necessary Python libraries:

    ```bash
    pip install flask
    pip install flask_sqlalchemy
    pip install sqlalchemy
    pip install psycopg2-binary
    ```

    Note: `psycopg2-binary` is a stand-alone package used to avoid build dependencies problem which sometimes occur while installing `psycopg2`.


## LICENSE

 [Do What The Fuck You Want To Public License.](LICENSE)