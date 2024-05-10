# Tg bot 

## Getting started

### Token
get a token from BotFather 

### create virtual venv
    python -m venv venv
    source venv/bin/activate

### Create database PostgreSQL
    sudo -u postgres psql
    
    CREATE DATABASE anverali;

### Create Table
    CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    task_text TEXT
                );

### run docker 
    docker build -t tgbot .
    docker compose up --build


