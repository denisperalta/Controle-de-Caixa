def format_number(value):
    try:
        # Convert string to float
        number = float(value)
        # Format with dot as thousands separator and comma as decimal
        formatted = f"{number:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return formatted
    except ValueError:
        return "Invalid number"