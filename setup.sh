# file to create .env file through a series of prompts

# delete the .env file if it exists
rm -f .env

read -p "Enter the database host: " db_host
read -p "Enter the database port: " db_port
read -p "Enter the database name: " db_name
read -p "Enter the database user: " db_user
read -s -p "Enter the database password: "  db_password

echo
read -s -p "Enter Spotify Cleint ID: " SPOTIFY_CLIENT_ID

echo
read -s -p "Enter Spotify Client Secret: " SPOTIFY_CLIENT_SECRET
echo

# create the .env file
echo "DB_NAME=$db_name" >> .env
echo "DB_USER=$db_user" >> .env
echo "DB_PASSWORD=$db_password" >> .env
echo "DB_HOST=$db_host" >> .env
echo "DB_PORT=$db_port" >> .env
echo "SPOTIFY_CLIENT_ID=$SPOTIFY_CLIENT_ID" >> .env
echo "SPOTIFY_CLIENT_SECRET=$SPOTIFY_CLIENT_SECRET" >> .env


echo "====================================="
echo ".env file created successfully"
echo "====================================="
