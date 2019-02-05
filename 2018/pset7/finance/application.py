import os

from cs50 import SQL, eprint
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request  # Ensure responses aren't cached
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show portfolio of stocks"""

    # Get user id
    user_id = session["user_id"]

    # User reached route via GET
    if request.method == "GET":
        # List of dict objects: user's stocks (tickers) and shares
        stocks = db.execute("SELECT stock, shares FROM portfolio WHERE user_id = :user_id ORDER BY stock",
                            user_id=user_id)

        # List of stock symbols and shares
        stocks_list = []
        for item in stocks:
            stocks_list.append((item.get("stock"), item.get("shares")))

        # List of current prices
        current_prices = []
        for stock in stocks_list:
            quote = lookup(stock[0])  # stock is tuple element at index0
            price = quote["price"]
            current_prices.append((price,))  # append price as a singleton tuple

        # List of stock holding values
        holdings = []
        for stocks, currentprice in zip(stocks_list, current_prices):
            holding = stocks[1] * currentprice[0]  # stocks[1] = shares and currentprice[0] is singleton
            holdings.append((holding,))  # append holding value as a singleton tuple

        # Merge all lists
        portfolio = list(zip(stocks_list, current_prices, holdings))

        # Current cash balance
        cash = db.execute("SELECT cash FROM users WHERE id = :user_id",
                          user_id=user_id)
        balance = float(cash[0].get("cash"))

        # Grand total of cash + stock's total value
        grand_total = balance
        for item in holdings:
            grand_total += item[0]  # item[0] is holding singleton

        return render_template("index.html",
                               portfolio=portfolio,
                               balance=balance,
                               grand_total=grand_total)

    # User reached route via POST by submitting cash balance top-up form
    if request.method == "POST":
        deposit = float(request.form.get("deposit"))

        # Update DB user table cash balance
        db.execute("UPDATE users SET cash = (cash + :deposit) WHERE id = :user_id",
                   deposit=deposit,
                   user_id=user_id)

        # Update DB transactions table with deposit
        db.execute("INSERT INTO transactions (id, buy_sell_deposit, cost_revenue) VALUES(:user_id, :t_type, :deposit)",
                   user_id=user_id,
                   t_type='deposit',
                   deposit=deposit)

        # Redirect user to index page with portfolio overview
        return redirect("/")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via GET
    if request.method == "GET":
        return render_template("buy.html")

    # User reached route via POST
    if request.method == "POST":

        # Store number of shares and the symbol
        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("non-positive integer shares", 400)

        stock = request.form.get("symbol")

        # Ensure non-blank, valid symbol input
        if not lookup(stock):
            return apology("invalid stock symbol", 400)

        # Ensure positive integer input for number of shares
        elif not shares or shares < 1:
            return apology("invalid number of shares", 400)

        # Stock quote lookup
        quote = lookup(stock)
        price = quote["price"]

        # Can user afford the stock?
        user_id = session["user_id"]
        cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=user_id)
        balance = float(cash[0]["cash"])
        cost = -(shares * price)
        if balance < abs(cost):
            return apology("insufficient funds", 400)

        else:
            # Add stock purchase to transactions table
            trade_type = "buy"
            db.execute("INSERT INTO transactions (stock, shares, id, price, buy_sell_deposit, cost_revenue) VALUES(:stock, :shares, :user_id, :price, :trade_type, :cost)",
                       stock=stock, shares=shares, user_id=user_id, price=price, trade_type=trade_type, cost=cost)
            # Add stock purchase to portfolio
            rows = db.execute("SELECT * FROM portfolio WHERE stock = :stock AND user_id = :user_id",
                              stock=stock, user_id=user_id)

            # Add row for new stock entry
            if not rows:  # Check if stock already in user portfolio
                db.execute("INSERT INTO portfolio (user_id, stock, shares) VALUES(:user_id, :stock, :shares)",
                           user_id=user_id, stock=stock, shares=shares)

            elif rows:  # If stock already there, update existing row with new share amount
                db.execute("UPDATE portfolio SET shares = (shares + :shares) WHERE stock = :stock AND user_id = :user_id",
                           shares=shares, stock=stock, user_id=user_id)

            # Update user's cash balance
            balance -= shares * price
            db.execute("UPDATE users SET cash = :balance WHERE id = :user_id",
                       balance=balance, user_id=user_id)
            # Flash
            flash("Purchase complete!")

            # Redirect user to index page with portfolio overview
            return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # User id
    user_id = session["user_id"]

    # Get list of dictionary objects for history html table
    transactions = db.execute("SELECT transaction_id, stock, shares, datetime, price, buy_sell_deposit, cost_revenue FROM transactions WHERE id = :user_id ORDER BY datetime",
                              user_id=user_id)

    # return render_template("history.html", transactions=transactions)
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Flash message
        flash("Logged In!")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

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

    # Flash
    flash("Logged out!")

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # User reached route via GET
    if request.method == "GET":
        return render_template("quote.html")

    # User reached route via POST (by submitting the Get Quote form
    if request.method == "POST":

        # Store quote requested by user
        quote = lookup(request.form.get("symbol"))

        # Ensure non-blank, valid symbol input
        if not quote:
            return apology("Invalid Stock Quote Request", 400)

        else:
            price = quote["price"]
            return render_template("quoted.html", quote=quote, price=price)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting register form)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password and confirmation match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords must match", 400)

        # Hash user password and store in pwhash
        pwhash = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=7)

        # Check if username already exists
        row = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                         username=request.form.get("username"), hash=pwhash)
        if not row:
            return apology("Username already exists", 400)

        # Automatic login after successful registering
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))
        session["user_id"] = rows[0]["id"]

        # Flash
        flash("Successfully registered!")

        # Redirect to user home page
        return redirect("/")

    # User reached route via GET (via redirect or link click)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # User id
    user_id = session["user_id"]

    # Query and store stocks and shares user has
    stocks = db.execute("SELECT stock FROM portfolio WHERE user_id = :user_id",
                        user_id=user_id)

    # List stocks dictionary keys
    stocks_list = [value for d in stocks for value in d.values()]

    # User reached route via GET
    if request.method == "GET":
        return render_template("sell.html", stocks_list=stocks_list)

    # User reached route via POST (by submitting the Sell form)
    if request.method == "POST":

        # Ensure non-blank, valid stock symbol input
        if not lookup(request.form.get("symbol")):
            return apology("Invalid stock symbol", 400)

        # Temporary storage for form inputs
        stock_sale = request.form.get("symbol")
        shares_sale = request.form.get("shares")

        # Ensure the user owns shares of the stock
        if stock_sale not in stocks_list:
            return apology("No ownership of shares", 400)

        # Ensure user inputs amount of shares to sell
        elif not shares_sale:
            return apology("Input share amount for sale", 400)

        # Ensure user owns share amount for sale
        shares_presale = db.execute("SELECT shares FROM portfolio WHERE stock = :stock_sale AND user_id = :user_id",
                                    stock_sale=stock_sale, user_id=user_id)

        # Extract value from share_presale list of dict objects
        shares_presale = shares_presale[0].get("shares")
        if not shares_presale >= int(shares_sale):
            return apology("Insufficient shares in account", 400)

        else:
            # Update portfolio DB Table with share difference
            db.execute("UPDATE portfolio SET shares = (shares - :shares_sale) WHERE stock = :stock_sale AND user_id = :user_id",
                       shares_sale=shares_sale, stock_sale=stock_sale, user_id=user_id)

            # Delete stock entry from portfolio DB Table, if new shares held are zero
            shares_aftersale = db.execute("SELECT shares FROM portfolio WHERE stock = :stock_sale AND user_id = :user_id",
                                          stock_sale=stock_sale, user_id=user_id)
            if not shares_aftersale[0].get("shares"):
                db.execute("DELETE FROM portfolio WHERE stock = :stock_sale AND user_id = :user_id",
                           stock_sale=stock_sale, user_id=user_id)

            # Update user's cash balance
            quote = lookup(stock_sale)  # Get current stock price
            price = quote["price"]
            revenue = float(shares_sale) * price  # Calculate revenue from sale
            db.execute("UPDATE users SET cash = (cash + :revenue) WHERE id = :user_id",
                       revenue=revenue, user_id=user_id)

            # Update DB transactions table
            trade_type = "sell"
            db.execute("INSERT INTO transactions (stock, shares, id, price, buy_sell_deposit, cost_revenue) VALUES(:stock_sale, :shares_sale, :user_id, :price, :trade_type, :revenue)",
                       stock_sale=stock_sale, shares_sale=shares_sale, user_id=user_id,
                       price=price, trade_type=trade_type, revenue=revenue)

            # Flash message
            flash("Sold!")

            # Redirect user to homepage
            return redirect("/")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
