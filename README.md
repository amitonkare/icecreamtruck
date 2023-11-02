The project is developed with python version 3.11.

# How to run the application


## Setup and Run Apis

- Open terminal, make sure you are in the root directory

- Lets create a postgres database container with docker compose, enter below command.
```
docker-compose up
```

- Create a virtual env and install dependencies with
```
pipenv install -r requirements.txt
```

- Make a copy of .env-example file as .env

- Activate virtual env with
```
pipenv shell
```

- Run below commands, data will be created in the database.
```
python manage.py feed_data

python manage.py fill_inventory

```

- To run api server, make sure you are in apis/icecreamtruck folder.
```
python manage.py runserver
```

- Run the tests
```
python manage.py test
```


## Setup and Run Frontend

- Open another termnial, install dependencies with
```
cd frontend/icecreamtruck
npm install
```

- Make a copy of .env.local.example file as .env.local

- To run frontend, open another terminal and make sure you are in frontend/icecreamtruck
```
npm run dev
```

- Open http://localhost:3000 to see the frontend.
