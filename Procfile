web: python manage.py collectstatic --noinput
web: daphne chat-con.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python runner.py runworker -v2
