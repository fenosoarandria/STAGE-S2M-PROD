def format_date(date_str):
    """Convertit une date au format DDMMYY en DD/MM/YYYY."""
    # Assurez-vous que date_str est bien une chaîne de caractères
    date_str = str(date_str)
    if len(date_str) == 6 and date_str.isdigit():
        day = date_str[:2]
        month = date_str[2:4]
        year = date_str[4:]
        return f"{day}/{month}/{year}"
    return date_str
