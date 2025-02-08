# cse412-project

## Running the project

1. Clone the repository
2. Run the following command to install the required packages

```bash
pip install -r requirements.txt
```

3. Run `setup.sh` to setup the environment variables.

```bash
./setup.sh
```

You will be prompted to enter some information about your PostgreSQL database.

> For the host, you can use `localhost` if you followed the Canvas tutorial.

> The port is usually `5432` but might be different if you followed the tutorial from Canvas.

> The database name is the name of the database you created. It is recommended that you create a blank database for this project using the command `createdb`.

> The username and password are the credentials you use to access the database.

4. Run the `start.sh` script to start the server after setting up the environment variables.

```bash
./start.sh
```

The server will be running on `http://localhost:8080` and will available on your network as well.

If there are exceptions about the database connection from `pyscopg2`, make sure the PostgreSQL server is running (you can check with `pg_isready`) and that the details you entered are correct.
