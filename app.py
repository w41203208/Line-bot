# coding=UTF-8
from Line_Bot_backend import create_app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)