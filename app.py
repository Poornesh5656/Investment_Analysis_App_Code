from Flask import Flask, render_template, request, jsonify
import sqlite3
import hashlib
from datetime import datetime

app = Flask(__name__)

# Function to create database
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS npv_calculations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            initial_investment REAL,
            discount_rate REAL,
            cashflows TEXT,
            npv REAL
        )
    """)
    conn.commit()
    conn.close()

# Function to calculate NPV
def calculate_npv(initial_investment, discount_rate, cashflows):
    npv = -initial_investment
    for i, cashflow in enumerate(cashflows):
        npv += cashflow / ((1 + discount_rate) ** (i + 1))
    return round(npv, 2)

# SHA-256 encryption function
def encrypt_data(data):
    return hashlib.sha256(data.encode()).hexdigest()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            initial_investment = float(request.form["initial_investment"])
            discount_rate = float(request.form["discount_rate"]) / 100
            cashflows = list(map(float, request.form["cashflows"].split(",")))

            npv_result = calculate_npv(initial_investment, discount_rate, cashflows)

            # Save to database
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO npv_calculations (timestamp, initial_investment, discount_rate, cashflows, npv) 
                VALUES (?, ?, ?, ?, ?)""",
                (datetime.now(), initial_investment, discount_rate, ",".join(map(str, cashflows)), npv_result)
            )
            conn.commit()
            conn.close()

            return render_template("index.html", npv=npv_result, success=True)

        except Exception as e:
            return render_template("index.html", error=str(e))

    return render_template("index.html")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
