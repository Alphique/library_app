# run.py
from app import create_app, db
from app.models import User, Book, Transaction, Wallet, Rental

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 
        'User': User, 
        'Book': Book, 
        'Transaction': Transaction,
        'Wallet': Wallet,
        'Rental': Rental
    }

if __name__ == '__main__':
    app.run(debug=True)