from source import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(use_reloader=True, debug=True)
