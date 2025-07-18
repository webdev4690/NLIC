from website import create_app, db
from website.models import AssetRequest, ExpenseRequest

app = create_app()

with app.app_context():
    records = ExpenseRequest.query.all()
    for r in records:
        print("=" * 50)
        print(f"ID: {r.id}")
        print(f"Branch: {r.branch}")
        print(f"Asset Name: {r.asset_name}")
        print(f"Description: {r.description}")
        print(f"Amount: {r.amount}")
        print(f"Approver: {r.approver}")
        print(f"Old Condition: {r.old_condition}")
        print(f"Old Location: {r.old_location}")
        print(f"Old Code: {r.expense_month}")
        print(f"Quantity: {r.quantity}")
        print(f"Attachment: {r.letter_filename}")
        print(f"Date Submitted: {r.date_submitted}")       


