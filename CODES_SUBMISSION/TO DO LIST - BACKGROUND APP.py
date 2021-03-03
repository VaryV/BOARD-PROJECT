import mysql.connector as mysql
import smtplib
import datetime as dt
import time
import calendar
from plyer import notification
import winsound


def RingTheBell():
    frequency = 2500  # Set Frequency To 2500 Hertz
    duration = 500  # Set Duration To 1000 ms == 1 second
    winsound.Beep(frequency, duration)
    winsound.Beep(frequency, duration)
    winsound.Beep(frequency, duration)
    winsound.Beep(frequency, duration)
    winsound.Beep(frequency, duration)


while True:
    sys_date = dt.date.today()
    sys_date_str = str(sys_date)
    sys_time = str(dt.datetime.now().time())[0:5]

    c = mysql.connect(
        host="localhost", user="root", passwd="MYSQLVARY", database="todolist"
    )
    cur = c.cursor()
    cur.execute(
        "SELECT usertasks.SNO, usertasks.username, mail, reminder_date, reminder_time, reminder_name, rem_description, rem_option, rem_frequency, reminded FROM USERPWD JOIN USERTASKS ON USERPWD.username = USERTASKS.username where reminder_date = '"
        + str(sys_date_str)
        + "'"
    )
    user_data = cur.fetchall()
    c.close()

    for i in user_data:
        if i[9] == "NO":
            if i[7] == "Y":
                if str(i[4])[0:5] == sys_time:
                    print("time matched")
                    if i[8] == "ONCE":
                        delta = ""
                        new_date = ""
                        c = mysql.connect(
                            host="localhost",
                            user="root",
                            passwd="MYSQLVARY",
                            database="todolist",
                        )
                        cur = c.cursor()
                        cur.execute(
                            "UPDATE USERTASKS SET reminded = 'YES' WHERE SNO="
                            + str(i[0])
                        )
                        c.commit()
                        c.close()

                    elif i[8] == "DAILY":
                        delta = dt.timedelta(days=1)
                        new_date = sys_date + delta
                    elif i[8] == "WEEKLY":
                        delta = dt.timedelta(days=7)
                        new_date = sys_date + delta
                    elif i[8] == "MONTHLY":
                        days_in_month = calendar.monthrange(
                            sys_date.year, sys_date.month
                        )[1]
                        new_date = sys_date + dt.timedelta(days=days_in_month)
                    subject = i[5]
                    body = i[6]
                    try:
                        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
                            smtp.ehlo()
                            smtp.starttls()
                            smtp.ehlo()
                            smtp.login("apptodolist24@gmail.com", "todolist123")
                            msg = f"Subject: {subject}\n\n{body}"
                            smtp.sendmail(
                                "apptodolist24@gmail.com",
                                i[2],
                                msg,
                            )
                    except Exception as e:
                        print(f'{e}')

                    # print(subject)
                    # print(body)
                    RingTheBell()
                    notification.notify(
                        title="TO DO LIST",
                        message=i[5],
                        app_icon="D:\\Varun\\PROGRAMMING\\BOARD-PROJECT\\IMAGES_SUBMISSION\\icon.ico",
                        timeout=20,
                    )
                    print("test" + str(new_date))
                    if new_date == "":
                        continue
                    else:
                        c = mysql.connect(
                            host="localhost",
                            user="root",
                            passwd="MYSQLVARY",
                            database="todolist",
                        )
                        cur = c.cursor()
                        cur.execute(
                            "UPDATE USERTASKS SET REMINDER_DATE = '"
                            + str(new_date)
                            + "' WHERE SNO="
                            + str(i[0])
                        )
                        c.commit()
                        c.close()
                    print("test2" + str(new_date))
