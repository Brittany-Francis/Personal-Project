from app import app
from app.controllers import users_controller, books_controller, characters_controller

 
if __name__=="__main__":   
    app.run(debug=True, port=8000)