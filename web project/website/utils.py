import os
import pandas as pd
from flask import current_app

def get_branches_from_excel():
    try:
        excel_path = os.path.join(current_app.root_path, 'static', 'lists', 'branches.xlsx')
        df = pd.read_excel(excel_path)
        branches = df['Branch Name'].dropna().unique().tolist()
        return branches
    except Exception as e:
        print(f"Failed to load Excel: {e}")
        return []


def get_assets_from_csv():
    try:
        csv_path = os.path.join(current_app.root_path, 'static', 'lists', 'Assets Names and Categories.csv')
        df = pd.read_csv(csv_path)
        assets = df['Item Name'].dropna().unique().tolist()
        return assets
    except Exception as e:
        print(f"Failed to load CSV: {e}")
        return []
    
def get_issue_from_excel():
    try:
        excel_path = os.path.join(current_app.root_path, 'static', 'lists', 'issue type.xlsx')
        df = pd.read_excel(excel_path)
        issues = df['Issue Type'].dropna().unique().tolist()
        return issues
    except Exception as e:
        print(f"Failed to load excel: {e}")
        return []