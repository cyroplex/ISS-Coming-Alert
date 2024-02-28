import requests
from datetime import datetime
import smtplib
import time

MY_LAT = "YOUR LOCATION LATITUDE e.g 39.925533"
MY_LONG = "YOUR LOCATION LONGITUDE e.g 32.866287"


def is_iss_close():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True


def is_night():
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

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    time.sleep(60)
    if is_iss_close() and is_night():
        user = "YOUR_MAIL"
        password = "YOUR APP PASSWORD"
        connection = smtplib.SMTP("SMTP ADDRESS OF YOUR MAIL SERVER e.g smtp.gmail.com", port=587)
        connection.starttls()
        connection.login(user=user, password=password)
        connection.sendmail(from_addr=user,
                            to_addrs="TARGET_MAIL",
                            msg="Subject: ISS COMING LOOK UP!!!\n\n ISS IS APPROACHING!.")
        connection.close()
