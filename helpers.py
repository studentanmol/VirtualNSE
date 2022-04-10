import os
import requests
import urllib.parse

from nsetools import Nse
from flask import redirect, render_template, request, session
from functools import wraps

nse = Nse()

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def rupees(value):
    """Format value as Rupees"""
    #rupee =  u"\u20B9"
    return (u"\u20B9"f"{value:,.2f}")

def lookup(symbol):
    """Look up quote for symbol."""

    # Parse response
    try:
        quote = nse.get_quote(symbol)
        return {
            "name": quote["companyName"],
            "price": float(quote["lastPrice"]),
            "symbol": quote["symbol"],
            "dayHigh": quote["dayHigh"],
            "dayLow": quote["dayLow"],
            "yearHigh": quote["high52"],
            "yearLow": quote["low52"]
        }
    except (KeyError, TypeError, ValueError):
        return None


def apology(message, code=400):
    """Render message as an apology to user."""
    
    return render_template("apology.html", top=code, bottom=(message))