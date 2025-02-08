export FLASK_RUN_EXTRA_FILES="templates/index.html"
export FLASK_DEBUG=1

flask --app main run --host=0.0.0.0 --port=8080