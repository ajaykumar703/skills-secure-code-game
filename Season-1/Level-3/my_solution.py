import os
from flask import Flask, request

app = Flask(__name__)

class TaxPayer:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.prof_picture = None
        self.tax_form_attachment = None

    def safe_path(self, path):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.normpath(os.path.join(base_dir, path))
        if base_dir != os.path.commonpath([base_dir, filepath]):
            return None
        return filepath

    def get_prof_picture(self, path=None):
        if not path:
            return None  # No path provided, return None or handle as needed

        # Use the safe_path function to ensure a secure path
        safe_path = self.safe_path(path)
        if not safe_path:
            return None  # Path traversal detected, return None or handle as needed

        with open(safe_path, 'rb') as pic:
            picture = bytearray(pic.read())

        return safe_path

    def get_tax_form_attachment(self, path=None):
        if not path:
            raise Exception("Error: Tax form is required for all users")

        # Use the safe_path function to ensure a secure path
        safe_path = self.safe_path(path)
        if not safe_path:
            return None  # Path traversal detected, raise an exception or handle as needed

        with open(safe_path, 'rb') as form:
            tax_data = bytearray(form.read())

        return safe_path

# Example route for testing
@app.route("/get_prof_picture")
def get_prof_picture_route():
    username = request.args.get("username")
    password = request.args.get("password")
    path = request.args.get("path")

    taxpayer = TaxPayer(username, password)
    result = taxpayer.get_prof_picture(path)

    if result:
        return f"Profile picture retrieved: {result}"
    else:
        return "Invalid path or path traversal detected."
