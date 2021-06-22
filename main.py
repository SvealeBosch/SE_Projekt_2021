from src import create_app

app = create_app()

#starts the app on the given port (if none is given :5000 is set as default)
if __name__ == "__main__":
    app.run()
