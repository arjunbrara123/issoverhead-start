import requests
import smtplib
from datetime import datetime

MY_LAT = 55.953251  # 51.507351 # Your latitude
MY_LONG = -3.188267  # -0.127758 # Your longitude

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()
print(data)

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

dist = ((iss_latitude - MY_LAT) ** 2 + (iss_longitude - MY_LONG) ** 2) ** 0.5
print(dist)
# Your position is within +5 or -5 degrees of the ISS position.
if dist < 7:

    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    hour_now = time_now.hour

    # If the ISS is close to my current position
    # and it is currently dark
    # Then send me an email to tell me to look up.
    # BONUS: run the code every 60 seconds.

    if sunrise <= hour_now <= sunset:
        # Send email
        my_email = "codingonlineplatform@gmail.com"
        pwd = "Password123#"  # input(f"Email: {my_email}, Password: ")
        msg = "Subject:ISS Overhead!\n\nISS Passing overhead, Distance Away: " + str(dist)

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=pwd)
            connection.sendmail(from_addr=my_email, to_addrs="arjunbrara@hotmail.co.uk", msg=msg)
