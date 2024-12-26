from flask import Flask, render_template, request, redirect, url_for
from models import db, Invoice

app = Flask(__name__)

# Configure Database (SQLite in this case)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///invoices.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    invoices = Invoice.query.all()  # Fetch all invoices from database
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
        
        # Create new invoice object and add it to the database
        new_invoice = Invoice(
            invoice_number=invoice_number,
            date=date,
            amount=amount,
            vendor_name=vendor_name,
            description=description
        )
        db.session.add(new_invoice)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('create_invoice.html')

@app.route('/delete/<int:id>', methods=['GET'])
def delete_invoice(id):
    invoice_to_delete = Invoice.query.get_or_404(id)
    db.session.delete(invoice_to_delete)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
