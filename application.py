import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, rupees

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["rupees"] = rupees

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

portfolio = []

@app.route("/about")
@login_required
def about():
    """Description about site"""
    username = db.execute("SELECT username FROM usernames")
    return render_template("welcome.html", name = username[0]["username"])


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    remaining = db.execute("SELECT cash FROM users WHERE id = (?)", session['user_id'])
    shares = db.execute("SELECT * FROM portfolio WHERE id=(?) ORDER BY symbol", session["user_id"])
    username = db.execute("SELECT username FROM usernames")
    amount = db.execute("SELECT SUM(total) FROM portfolio WHERE id=(?)", session["user_id"])
    total = amount[0]["SUM(total)"]
    if total == None:
        total = 0
    cash = remaining[0]["cash"]

    portfolio.clear()
    sum_price = 0.00

    for row in shares:
        quote = lookup(row["symbol"])
        symbols = quote['symbol']
        name = quote['name']
        number = row["number"]
        price = quote['price']
        total_price = float(price)*float(number)
        sum_price = sum_price + total_price
        portfolio.append({'symbol': symbols, 'name': name, 'shares': number, 'price': price, 'total': total_price})

    grand_total = sum_price + cash
    total = total + cash
    net = grand_total - total
    return render_template("index.html",names = username[0]["username"], portfolio=portfolio, cash=cash, total=total, grand_total=grand_total, message=net)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        buy_shares = request.form.get("shares")
        if not request.form.get("symbol"):
            return apology("symbol not entered", 400)
        elif lookup(symbol) == None:
            return apology("invalid symbol entered", 400)
        elif not buy_shares:
            return apology("invalid number entered", 400)
        try:
            buy_share = int(request.form.get("shares"))
        except:
            return apology("share must be an integer", 400)
        if buy_share <= 0:
            return apology("invalid number entered", 400)
        index = db.execute("SELECT * FROM portfolio WHERE id=(?)", session["user_id"])
        buy_shares = int(buy_shares)
        share = lookup(symbol)
        prices = float(buy_shares)*float(share['price'])
        Cash = db.execute("SELECT cash FROM users WHERE id=(?)", session["user_id"])
        cash = float(Cash[0]["cash"])
        if cash < prices:
            return apology("You do not have enough cash for this transaction", 400)

        count = 0
        for row in index:
            if(symbol == row["symbol"]):
                number = int(row["number"])
                table_total = float(row["total"])
                db.execute("UPDATE portfolio SET number=(?) AND total=(?)", (number+buy_shares), (prices+table_total))
                break
            else:
                count = count + 1
        if count > 0 or count == 0:
            db.execute("INSERT INTO portfolio(id, company, number, price, total, symbol) VALUES(?, ?, ?, ?, ?, ?)",
                       session["user_id"], share['name'], int(buy_shares), share['price'], prices, symbol)
            db.execute("UPDATE portfolio SET name = (SELECT username FROM usernames) WHERE name IS NULL AND company=(?) AND number=(?) AND price=(?) AND total=(?)",
                       share['name'], int(buy_shares), share['price'], prices)

        db.execute("INSERT INTO shares(id, company, number, price, total, symbol, time, status) VALUES(?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?)",
                   session["user_id"], share['name'], int(buy_shares), share['price'], prices, symbol, "Bought")
        db.execute("UPDATE shares SET name = (SELECT username FROM usernames) WHERE name IS NULL AND company=(?) AND number=(?) AND price=(?) AND total=(?) AND status=(?)",
                   share['name'], int(buy_shares), share['price'], prices, "Bought")
        db.execute("UPDATE users SET cash = (?) WHERE username=(SELECT username FROM usernames)", (cash-prices))
        flash("Bought!")
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    history = db.execute("SELECT * FROM shares WHERE id=(?) ORDER BY time ASC", session["user_id"])

    return render_template("history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # Delete sql table
    db.execute("DELETE FROM usernames")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Insert username into table
        db.execute("INSERT INTO usernames(username) VALUES (?)", rows[0]["username"])
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # DELETE From Table
    db.execute("DELETE FROM usernames")

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        if not request.form.get("symbol"):
            return apology("symbol not entered", 400)
        elif lookup(symbol) == None:
            return apology("invalid symbol entered", 400)
        return render_template("quoted.html", share=lookup(symbol))
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username", 400):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password") or not request.form.get("confirmation"):
            return apology("must provide password", 400)

        # Check if passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password must be same", 400)
        
        # Check if email entered
        elif not request.form.get("email"):
            return apology("must provide email", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        rows1 = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("email"))

        # Check if username is not taken
        if len(rows) != 0:
            return apology("username already exists", 400)
        
        # Check if email is not taken
        elif len(rows1) != 0:
            return apology("email already exists", 400)

        # Add user to database
        password = request.form.get("password")
        db.execute("INSERT INTO users(username, hash, email) VALUES(?, ?, ?)", request.form.get("username"), generate_password_hash(password), request.form.get("email"))

        flash("Registered!")

        # Redirect user to login
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        input_symbol = request.form.get("symbol")
        number = request.form.get("shares")
        share = db.execute("SELECT * FROM portfolio WHERE id = (?) AND symbol=(?)", session["user_id"], input_symbol)

        if not input_symbol:
            return apology("missing symbol", 400)
        if not number:
            return apology("missing number of shares", 400)
        if len(input_symbol) == 0:
            return apology("No shares left", 400)
        if int(number) < 1:
            return apology("Invalid number of shares", 400)
        if len(share) == 0:
            return apology("You do not own this stock", 400)
        number_table = int(share[0]["number"])
        if int(number) > number_table:
            return apology("You do not have sufficient shares", 400)

        table_total = float(share[0]["total"])
        quote = lookup(input_symbol)
        total = float(quote['price']) * int(number)
        share_number = int(number_table-int(number))
        share_total = float(table_total-total)
        Cash = db.execute("SELECT cash FROM users WHERE id=(?)", session["user_id"])
        cash = float(Cash[0]["cash"])
        final_cash = float(cash+total)
        db.execute("INSERT INTO shares(id, symbol, company, number, price, total, time, status) VALUES(?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?)",
                   session["user_id"], quote['symbol'], quote['name'], -int(int(number)), float(quote['price']), float(int(number)*float(quote['price'])), "Sold")
        db.execute("UPDATE shares SET name = (SELECT username FROM usernames) WHERE name IS NULL AND id=(?) AND company=(?) AND number=(?) AND price=(?) AND status=(?)",
                   session["user_id"], quote['name'], int(number), float(quote['price']), "Sold")
        db.execute("UPDATE users SET cash = (?) WHERE id = (?)", (final_cash), session["user_id"])
        db.execute("UPDATE portfolio SET number = (?) WHERE id=(?) AND symbol=(?)", share_number, session["user_id"], input_symbol)
        db.execute("UPDATE portfolio SET total = (?) WHERE id=(?) AND symbol=(?)", share_total, session["user_id"], input_symbol)
        if share_number == 0:
            db.execute("DELETE FROM portfolio WHERE symbol=(?)", input_symbol)
        flash("Sold!")

        return redirect("/")

    else:
        sell = db.execute("SELECT symbol FROM portfolio WHERE id=(?)", session["user_id"])
        return render_template("sell.html", sell=sell)



@app.route("/change_username", methods=["GET", "POST"])
@login_required
def change_username():
    """Changing username"""
    if request.method == "POST":
        username = request.form.get("new_username")

        # Check if user has entered username
        if not username:
            return apology("must provide new username", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE id != (?) AND username =(?)", session["user_id"], username)

        # Check if username is not taken
        if len(rows) != 0:
            return apology("username already exists", 400)

        # Update table for username
        db.execute("UPDATE users SET username=(?) WHERE id=(?)", username, session["user_id"])

        # display message
        flash("Username changed!")

        # logout user
        return redirect("/login")

    else:
        return render_template("change_username.html")

@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Changing password"""
    if request.method == "POST":
        password = request.form.get("new_password")

        # Check if user has entered password
        if not password:
            return apology("must provide new password", 400)

        # Update table for password
        db.execute("UPDATE users SET hash=(?) WHERE id=(?)", generate_password_hash(password), session["user_id"])

        # display message
        flash("Password changed!")

        # logout user
        return redirect("/login")

    else:
        return render_template("change_password.html")


cash_count = 0.00

@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_funds():
    """User can add extra funds to their account"""
    global cash_count
    if request.method == "POST":
        cash=request.form.get("add_cash")
        if not cash:
            return apology("Enter some amount", 400)
        if float(cash)<=0 :
            return apology("Enter a valid amount", 400)
        cash_count = cash_count + float(cash)

        Cash = db.execute("SELECT cash FROM users WHERE id=(?)", session["user_id"])
        table_cash = float(Cash[0]["cash"])
        db.execute("UPDATE users SET cash =(?) WHERE id=(?)", table_cash + float(cash), session["user_id"])

        flash("Cash Added!")

        return redirect("/")

    else:
        return render_template("add.html")



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
