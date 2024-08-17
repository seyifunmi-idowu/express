# Express

## Install
- Clone the repository:

- Check into the folder:
```
cd express
```

- Install pre-commit hooks
```
pre-commit install
```

- Copy .env.sample to .env
- Copy .db-env.sample to .db-env

### Without Docker
- Create & activate virtual environment
```
python3 -m venv ./venv && source ./venv/bin/activate
```

- Install packages
```
pip install -r requirements.txt
```

### With Docker
- Copy .env.sample to .env

- Make sure `DATABASE_URL` in `.env` points to:
```postgres://root:password@postgres:5432/express```

- Build the application:
```docker-compose -f docker-compose.yml build```

- Start the server:
```docker-compose -f docker-compose.yml up```

- To stop the server:
```docker-compose -f docker-compose.yml down```

## Run the app
### With Docker
- Start the server:
```docker-compose -f docker-compose.yml up```

- To stop the server:
```docker-compose -f docker-compose.yml down```

