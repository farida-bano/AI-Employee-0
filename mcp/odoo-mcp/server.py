import os
import requests
import json
import datetime
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = FastMCP(
    name="OdooMCP",
)

ODOO_URL = os.getenv("ODOO_URL")
ODOO_DB = os.getenv("ODOO_DATABASE")
ODOO_USERNAME = os.getenv("ODOO_USERNAME")
ODOO_API_KEY = os.getenv("ODOO_API_KEY")

def execute_kw(model, method, args, kwargs=None):
    """Executes a JSON-RPC call to Odoo."""
    if kwargs is None:
        kwargs = {}
    
    # 1. Authenticate
    auth_payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "service": "common",
            "method": "authenticate",
            "args": [ODOO_DB, ODOO_USERNAME, ODOO_API_KEY, {}]
        },
        "id": 1
    }
    
    try:
        response = requests.post(f"{ODOO_URL}/jsonrpc", json=auth_payload, timeout=10)
        response.raise_for_status()
        uid = response.json().get("result")
        
        if not uid:
            error = response.json().get("error")
            raise Exception(f"Authentication failed: {error}")

        # 2. Execute method
        call_payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [ODOO_DB, uid, ODOO_API_KEY, model, method, args, kwargs]
            },
            "id": 2
        }
        response = requests.post(f"{ODOO_URL}/jsonrpc", json=call_payload, timeout=10)
        response.raise_for_status()
        return response.json().get("result")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Network error communicating with Odoo: {str(e)}")

@app.tool()
def create_invoice(partner_id: int, invoice_line_ids: list) -> str:
    """
    Creates an invoice (account.move) in Odoo.
    
    Args:
        partner_id: The ID of the customer (res.partner).
        invoice_line_ids: A list of invoice lines in Odoo command format. 
                         Example: [[0, 0, {'product_id': 1, 'quantity': 1, 'price_unit': 100}]]
    """
    try:
        invoice_id = execute_kw('account.move', 'create', [{
            'partner_id': partner_id,
            'move_type': 'out_invoice',
            'invoice_line_ids': invoice_line_ids
        }])
        return f"Invoice created successfully with ID: {invoice_id}"
    except Exception as e:
        return f"Error creating invoice: {str(e)}"

@app.tool()
def list_invoices(limit: int = 10) -> str:
    """
    Lists recent customer invoices.
    
    Args:
        limit: Maximum number of invoices to retrieve.
    """
    try:
        invoices = execute_kw('account.move', 'search_read', [[['move_type', '=', 'out_invoice']]], {
            'fields': ['name', 'partner_id', 'amount_total', 'state', 'invoice_date'],
            'limit': limit,
            'order': 'id desc'
        })
        return json.dumps(invoices, indent=2)
    except Exception as e:
        return f"Error listing invoices: {str(e)}"

@app.tool()
def record_payment(invoice_id: int, amount: float, payment_date: str = None) -> str:
    """
    Records a payment for a specific invoice.
    
    Args:
        invoice_id: The ID of the invoice to pay.
        amount: The payment amount.
        payment_date: Optional payment date (YYYY-MM-DD). Defaults to today.
    """
    try:
        # Get invoice details to identify journal and partner
        invoice_data = execute_kw('account.move', 'read', [[invoice_id]], {'fields': ['journal_id', 'partner_id', 'name', 'currency_id']})
        if not invoice_data:
            return f"Invoice with ID {invoice_id} not found."
        
        invoice = invoice_data[0]
        journal_id = invoice['journal_id'][0]
        partner_id = invoice['partner_id'][0]
        
        payment_vals = {
            'payment_type': 'inbound',
            'partner_type': 'customer',
            'partner_id': partner_id,
            'amount': amount,
            'journal_id': journal_id,
            'date': payment_date or datetime.date.today().isoformat(),
            'ref': f"Payment for {invoice['name']}"
        }
        
        payment_id = execute_kw('account.payment', 'create', [payment_vals])
        execute_kw('account.payment', 'action_post', [[payment_id]])
        
        return f"Payment of {amount} recorded and posted for invoice {invoice_id}. Payment ID: {payment_id}"
    except Exception as e:
        return f"Error recording payment: {str(e)}"

if __name__ == "__main__":
    import uvicorn
    # Defaulting to 8001 to avoid conflict with business_mcp on 8000
    uvicorn.run(app, host="0.0.0.0", port=8001)
