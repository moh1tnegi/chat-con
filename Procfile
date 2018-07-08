web: python manage.py collectstatic
web: daphne chat-con.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker -v2 channels
