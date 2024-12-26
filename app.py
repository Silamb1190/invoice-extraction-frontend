import Flask
from flask_sqlalchemy
import SQLAlchemy
import os

app = Flask(__name__)

# Configure Database (PostgreSQL in this case)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://simbu_user:0I8SIbyx8mLzjnuFTEsoWLgTPMZvLNFK@dpg-ctgs1faj1k6c73a6docg-a:5432/simbu')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the Invoice model
class Invoice(db.Model):
    __tablename__ = 'invoice'
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    vendor_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Invoice {self.invoice_number}>"

# Create the tables (if they do not exist yet) - only in dev
if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()  # Creates the tables
            print("Database tables created successfully!")
        except Exception as e:
            print(f"Error creating database tables: {e}")

@app.route('/')
def index():
    invoices = Invoice.query.all()  # Fetch all invoices from the database
    return render_template('index.html', invoices=invoices)

@app.route('/create', methods=['GET', 'POST'])
def create_invoice():
    if request.method == 'POST':
        # Extract invoice details from the form
        invoice_number = request.form['invoice_number']
        date = request.form['date']
        amount = request.form['amount']
        vendor_name = request.form['vendor_name']
        description = request.form['description']
        
        # Create a new invoice object and add it to the database
        new_invoice = Invoice(
            invoice_number=invoice_number,
            date=date,
            amount=amount,
            vendor_name=vendor_name,
            description=description
        )
        try:
            db.session.add(new_invoice)
            db.session.commit()  # Commit the transaction to save the new invoice
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            print(f"Error saving invoice: {e}")
            return redirect(url_for('index'))  # Handle as needed (e.g., error page)

    return render_template('create_invoice.html')

@app.route('/delete/<int:id>', methods=['GET'])
def delete_invoice(id):
    invoice_to_delete = Invoice.query.get_or_404(id)  # Fetch the invoice to delete
    try:
        db.session.delete(invoice_to_delete)  # Delete the invoice
        db.session.commit()  # Commit the transaction to remove it from the database
        return redirect(url_for('index'))
    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        print(f"Error deleting invoice: {e}")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
