# feleexpress

Git pull
`git pull https://github.com/FeleExpress/feleexpress.git`

Install your virtual environment
`pip3 install virtualenv`

Create virtual environment
`virtualenv venv`

Copy `sample.env` to create your `.env`
`cat sample.env > .env`


# Fele Express

This repository holds the `backend api` code base for the Fele Express Application.

## Install
- Clone the repository:
```
git clone https://github.com/FeleExpress/feleexpress.git
```

- Check into the folder:
```
cd fele
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
```postgres://root:password@postgres:5432/feleexpress```

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

### Without Docker
- Start the server
```./manage.py runserver```
## Deployment Links
- [Staging Server](https://api-staging.feleexpress.com/)
- [Production Server](https://api.feleexpress.com/) - to be updated
