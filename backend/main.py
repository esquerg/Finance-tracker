from app import create_app, db

#Create the Flask app instance
app = create_app()

with app.app_context():
    db.create_all()

#Only run the app when this script is executed directly not when imported
if __name__ == '__main__':
    app.run(debug=True)

