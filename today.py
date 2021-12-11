from datetime import date

today = date.today()
print("Today's date:", today)

# dd/mm/YY
d1 = today.strftime("%d/%m/%Y")
print("d1 =", d1)