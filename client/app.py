from source import create_app, celery

app = create_app()

print(app.config)
