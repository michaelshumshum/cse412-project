if [ -e ".env" ]; then
    source .env

    # for file in templates/*
    # do
    #     export FLASK_RUN_EXTRA_FILES="$FLASK_RUN_EXTRA_FILES:$file"
    # done

    export FLASK_DEBUG=1

    flask --app main run --host=0.0.0.0 --port=8080
else
    echo "!!! No .env file found. Please run 'setup.sh' first. !!!"
fi