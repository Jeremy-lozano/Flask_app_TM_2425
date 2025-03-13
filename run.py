from app import create_app,session

app = create_app()
app.before_first_request(lambda: session.clear())




if __name__ == "__main__":
    app.run(debug=True)

