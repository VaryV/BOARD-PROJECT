# IMPORTING REQUIRED MODULES/LIBRARIES #
import tkinter as tk  # FOR THE GRAPHICAL USER INTERFACE
import mysql.connector as my  # TO CONNECT TO THE MYSQL DATABASE WHERE THE REQUIRED TABLES ARE STORED
from tkinter import messagebox  # TO IMPORT MESSAGEBOX FROM TKINTER TO DISPLAY MESSAGES
import tkcalendar as tkc  # TO IMPORT THE CALENDAR WIDGET
import datetime as dt  # TO WORK WITH CURRENT DATES AND TIMES AND TIME DELTAS
from tkinter import ttk  # TO MODIFY APPEARANCE OF CERTAIN WIDGETS

# GLOABLISING THE REQUIRED VARIABLES
global success
global user
success = False
user = False

# HOME SCREEN FUNCTION #
def homepage():
    global success
    success = False
    # CREATING THE 'Tk' WINDOW WHERE ANY OUTPUT IS DISPLAYED
    p_win = tk.Tk("zoomed")
    p_win.title(
        "TO-DO-LIST!!"
    )  # SETTING THE TITLE OF THE WINDOW TO THE NAME OF THE APPLICATION
    p_win.state("zoomed")  # MAKING THE WINDOW GET DISPLAYED IN A MAXIMISED STATE
    p_win.iconbitmap(
        "IMAGES_SUBMISSION\\icon.ico"
    )  # SETTING ICON OF THE APP WINDOW

    bg_img = tk.PhotoImage(
        file="IMAGES_SUBMISSION\\scenery.png"
    )  # INITIALISING IMAGE
    bg_label = tk.Label(p_win, image=bg_img)  # LABEL WITH THE BACKGROUND IMAGE
    bg_label.place(x=0, y=0)  # PLACING THE LABEL

    global hide_img
    global show_img
    hide_img = tk.PhotoImage(
        file="IMAGES_SUBMISSION\\hide_pwd.png"
    )  # INITIALISING IMAGE
    show_img = tk.PhotoImage(
        file="IMAGES_SUBMISSION\\show_pwd.png"
    )  # INITIALISING IMAGE

    # DEFINING SIGNIN AND LOGIN FUNCTIONS AND CHANGE PASSWORD FUNCTION #

    # SIGN UP FUNCTION #
    def signup():
        # DISABLING THE SIGNUP, LOGIN AND CHANGE PASSWORD FUNCTION SO THAT USER CANNOT GO TO OTHER BUTTONS WHEN SIGNIN IS ACTIVE
        signup_btn.config(state="disabled")
        login_btn.config(state="disabled")
        pwdcng_btn.config(state="disabled")

        # SIGNUP, USERNAME, PASSWORD AND EMAIL LABELS
        signup = tk.Label(
            p_win,
            text="   SIGN - UP   ",
            font=("Fugaz One", 26),
            fg="black",
            padx=15,
            pady=10,
        )
        usn = tk.Label(
            p_win,
            text="USERNAME :",
            font=("Fugaz One", 18),
            fg="black",
            padx=15,
            pady=10,
        )
        pwd = tk.Label(
            p_win,
            text="PASSWORD :",
            font=("Fugaz One", 18),
            fg="black",
            padx=14,
            pady=10,
        )
        mail = tk.Label(
            p_win,
            text="E-MAIL ID    :",
            font=("Fugaz One", 18),
            fg="black",
            padx=16,
            pady=10,
        )
        # ENTRY BOXES FOR THE USER TO ENTER USERNAME PASSWORD AND MAIL
        e_usn = tk.Entry(p_win, width=18, font=("Fugaz One", 18))
        e_mail = tk.Entry(p_win, width=18, font=("Fugaz One", 18))
        e_pwd = tk.Entry(p_win, width=16, show="*", font=("Fugaz One", 18))

        e_usn.focus()

        # FUNCTION TO SHOW THE PASSWORD WHEN USER CLICKS ON THE SHOW PASSWORD BUTTON #
        def hide_signup():
            pwd_btn.config(image=hide_img, command=show_signup)
            e_pwd.config(show="*")

        # FUNCTION TO HIDE THE PASSWORD WHEN THE USER CLICKS ON THE HIDE PASSWORD BUTTON #
        def show_signup():
            pwd_btn.config(image=show_img, command=hide_signup)
            e_pwd.config(show="")

        # FUNCTION FOR BACK BUTTON #
        def back_signup():
            # TO ENABLE THE SIGNIN, LOGIN AND CHANGE PASSWORD BUTTONS THAT WERE DISABLED BEFORE
            signup_btn.config(state="normal")
            login_btn.config(state="normal")
            pwdcng_btn.config(state="normal")
            # TO MAKE THE NEW WIDGETS THAT SHOWED UP WHEN SIGNUP WAS CLICKED TO DIASAPPEAR
            signup.destroy()
            usn.destroy()
            pwd.destroy()
            mail.destroy()
            e_usn.destroy()
            e_pwd.destroy()
            e_mail.destroy()
            pwd_btn.destroy()
            confirm_btn.destroy()
            back_btn.destroy()

        # FUNCTION FOR CONFIRM BUTTON #
        def confirm_signup():

            # TO GET WHAT TEXT IS CURRENTLY PRESENT IN THE ENTRY BOXES
            username = e_usn.get()
            password = e_pwd.get()
            email = e_mail.get()
            # TO CLEAR WHAT TEXT IS CURRENTLY PRESENT IN THE ENTRY BOXES
            e_usn.delete(0, "end")
            e_pwd.delete(0, "end")
            e_mail.delete(0, "end")

            # CONNECTING TO MySQL TO GET THE DATA IN THE TABLE
            c = my.connect(
                host="localhost", user="root", passwd="MYSQLVARY", database="todolist"
            )
            cur = c.cursor()
            # TO GET DATA FROM MySQL DATABASE
            cur.execute("select * from userpwd")
            data = cur.fetchall()
            c.close()

            # SETTING A FLAG IN WHICH USER IS TRUE
            user = True
            for x in data:
                # IF CONDITION TO CHECK IF THE USERNAME ALREADY EXISTS AND SETS USER FLAG TO FALSE
                if x[1] == username:
                    user = False
                    messagebox.showinfo(
                        "INVALID USERNAME", "SORRY! THIS USERNAME HAS BEEN TAKEN"
                    )
                    break

            if email.endswith("@gmail.com") == False:
                user = False
                messagebox.showinfo(
                    "INVALID MAIL ID",
                    "MAIL ID IS SUPPOSED TO END WITH '@gmail.com'.",
                )

            for x in data:
                # IF CONDITION TO CHECK IF MAIL HAS ALREADY BEEN USED BY SOME OTHER USER AND SETS USER FLAG TO FALSE
                if x[3] == email:
                    user = False
                    messagebox.showinfo(
                        "WRONG MAIL",
                        "OOPS! AN ACCOUNT ALREADY EXISTS WITH THIS MAIL ID.",
                    )
                    break

            # IF THE USER FLAG IS TRUE AFTER PASSING THROUGH THE IF CONDITIONS
            if user == True:
                # CONNECTS TO MySQL DATABASE AND INSERTS THE USERNAME, PASSWORD AND MAIL ENTERED BY USER
                c = my.connect(
                    host="localhost",
                    user="root",
                    passwd="MYSQLVARY",
                    database="todolist",
                )
                cur = c.cursor()
                # TO INSERT THE DATA ADDED BY THE USER
                cur.execute(
                    "insert into userpwd (username, password, mail) values("
                    + "'"
                    + str(username)
                    + "','"
                    + str(password)
                    + "','"
                    + str(email)
                    + "')"
                )
                c.commit()
                c.close()
                messagebox.showinfo(
                    "SIGN-UP SUCCESSFUL",
                    "YOU HAVE COMPLETED SIGNING UP. LOGIN TO GET STARTED",
                )

            else:
                pass
            # CALLS THE BELOW FUNCTION TO FO BACK TO THE DEFAULT MAIN MENU AFTER SIGNING UP
            back_signup()

        # PASSWORD HIDE OR SHOW BUTTON, CONFIRM BUTTON AND BACK BUTTON
        pwd_btn = tk.Button(image=hide_img, command=show_signup)
        confirm_btn = tk.Button(
            p_win,
            text="CONFIRM",
            font=("Fugaz One", 18),
            fg="black",
            padx=16,
            command=confirm_signup,
        )
        back_btn = tk.Button(
            p_win,
            text="    BACK    ",
            font=("Fugaz One", 18),
            fg="black",
            padx=15,
            command=back_signup,
        )

        # PLACING ALL THE SIGN UP WIDGETS #
        signup.place(x=653, y=136)
        usn.place(x=503, y=236)
        pwd.place(x=503, y=381)
        mail.place(x=503, y=311)
        e_usn.place(x=701, y=241)
        e_pwd.place(x=701, y=386)
        pwd_btn.place(x=952, y=386)
        e_mail.place(x=701, y=316)
        confirm_btn.place(x=588, y=461)
        back_btn.place(x=768, y=461)

    # LOGIN FUNCTION #
    def login():
        # DISABLING THE SIGNUP, LOGIN AND CHANGE PASSWORD FUNCTION SO THAT USER CANNOT GO TO OTHER BUTTONS WHEN SIGNIN IS ACTIVE
        signup_btn.config(state="disabled")
        login_btn.config(state="disabled")
        pwdcng_btn.config(state="disabled")

        # LOGIN, USERNAME AND PASSWORD LABELS
        login = tk.Label(
            p_win,
            text="     LOGIN     ",
            font=("Fugaz One", 26),
            fg="black",
            padx=15,
            pady=10,
        )
        usn = tk.Label(
            p_win,
            text="USERNAME :",
            font=("Fugaz One", 18),
            fg="black",
            padx=15,
            pady=10,
        )
        pwd = tk.Label(
            p_win,
            text="PASSWORD :",
            font=("Fugaz One", 18),
            fg="black",
            padx=14,
            pady=10,
        )
        # USERNAME AND PASSWORD ENTRY BOXES IN WHICH USER ENTERS TEXT
        e_usn = tk.Entry(p_win, width=18, font=("Fugaz One", 18))
        e_pwd = tk.Entry(p_win, width=16, show="*", font=("Fugaz One", 18))

        e_usn.focus()

        # FUNCTION TO HIDE THE PASSWORD #
        def hide_login():
            pwd_btn.config(image=hide_img, command=show_login)
            e_pwd.config(show="*")

        # FUNCTION TO SHOW THE PASSWORD #
        def show_login():
            pwd_btn.config(image=show_img, command=hide_login)
            e_pwd.config(show="")

        # FUNCTION FOR BACK BUTTON #
        def back_login():
            # TO ENABLE THE SIGNIN, LOGIN AND CHANGE PASSWORD BUTTONS THAT WERE DISABLED BEFORE
            signup_btn.config(state="normal")
            login_btn.config(state="normal")
            pwdcng_btn.config(state="normal")
            # TO MAKE THE NEW WIDGETS THAT SHOWED UP WHEN LOGIN WAS CLICKED TO DIASAPPEAR
            login.destroy()
            usn.destroy()
            pwd.destroy()
            e_usn.destroy()
            e_pwd.destroy()
            pwd_btn.destroy()
            confirm_btn.destroy()
            back_btn.destroy()

        # FUNCTION FOR CONFIRM BUTTON #
        def confirm_login():
            global success
            global user
            # TO GET THE USERNAME AND PASSWORD ENTERED BY THE USER
            username = e_usn.get()
            password = e_pwd.get()
            # TO CLEAR THE USERNAME AND PASSWORD THE USER ENTERED FROM THE ENTRY BOX
            e_usn.delete(0, "end")
            e_pwd.delete(0, "end")

            # CONNECTING TO MySQL DATABASE
            c = my.connect(
                host="localhost", user="root", passwd="MYSQLVARY", database="todolist"
            )
            cur = c.cursor()
            # TO GET DATA FROM MySQL DATABASE
            cur.execute("select * from userpwd")
            data = cur.fetchall()
            c.close()

            # CREATING A LIST WITH ALL USERNAMES
            usernames = []
            for x in data:
                usernames.append(x[1])

            # SETTING A FLAG THAT SAYS USER = TRUE
            user = True
            # IF CONDITION TO CHECK IF THE USERNAME ENTERED BY THE USER IS THERE IN THE DATABASE, IF NOT SETS USER FLAG TO FALSE
            if username not in usernames:
                user = False
                messagebox.showinfo(
                    "INVALID USERNAME",
                    "THE USERNAME DOESNT EXIST. PLEASE SIGNUP AND LOGIN.",
                )

            if username in usernames:
                for x in data:
                    # IF CONDITION TO CHECK IF PASSWORD IS RIGHT FOR THE CORRESPONDING USERNAME, IF NOT SETS USER FLAG TO FALSE
                    if x[1] == username and x[2] != password:
                        user = False
                        messagebox.showinfo(
                            "OOPS!!!", "YOU HAVE ENTERED THE WRONG PASSWORD."
                        )
                        break

                for x in data:
                    # IF USERNAME AND PASSWORD ARE RIGHT, SETS USER FLAG TO TRUE AND THE GLOBAL VARIABLE SUCCESS TO TRUE
                    if x[1] == username and x[2] == password:
                        user = True
                        success = True
                        user = username
                        messagebox.showinfo(
                            "LOGIN SUCCESFUL", "YOU HAVE SUCCESSFULLY LOGGED IN!!!"
                        )
                        p_win.destroy()
                        break

        # SHOW AND HIDE PASSWORD BUTTONS, CONFIRM AND BACK BUTTONS
        pwd_btn = tk.Button(image=hide_img, command=show_login)
        confirm_btn = tk.Button(
            p_win,
            text="CONFIRM",
            font=("Fugaz One", 18),
            fg="black",
            padx=16,
            command=confirm_login,
        )
        back_btn = tk.Button(
            p_win,
            text="    BACK    ",
            font=("Fugaz One", 18),
            fg="black",
            padx=15,
            command=back_login,
        )

        # PLACING ALL THE LOGIN WIDGETS #
        login.place(x=653, y=136)
        usn.place(x=503, y=236)
        pwd.place(x=503, y=311)
        e_usn.place(x=701, y=241)
        e_pwd.place(x=701, y=316)
        pwd_btn.place(x=952, y=316)
        confirm_btn.place(x=693, y=386)
        back_btn.place(x=693, y=461)

    # CHANGE PASSWORD FUNCTION #
    def pwdcng():
        # DISABLING THE SIGNUP, LOGIN AND CHANGE PASSWORD FUNCTION SO THAT USER CANNOT GO TO OTHER BUTTONS WHEN SIGNIN IS ACTIVE
        signup_btn.config(state="disabled")
        login_btn.config(state="disabled")
        pwdcng_btn.config(state="disabled")

        # CHANGE PASSWORD, USERNAME, CURRENT PASSWORD, NEW PASSWORD LABELS
        pwdcng_label = tk.Label(
            p_win,
            text="     CHANGE PASSWORD     ",
            font=("Fugaz One", 26),
            fg="black",
            padx=15,
            pady=10,
        )
        usn = tk.Label(
            p_win,
            text="USERNAME                     :",
            font=("Fugaz One", 18),
            fg="black",
            padx=15,
            pady=10,
        )
        c_pwd = tk.Label(
            p_win,
            text="CURRENT PASSWORD :",
            font=("Fugaz One", 18),
            fg="black",
            padx=14,
            pady=10,
        )
        n_pwd = tk.Label(
            p_win,
            text="NEW PASSWORD          :",
            font=("Fugaz One", 18),
            fg="black",
            padx=16,
            pady=10,
        )
        # ENTRY BOXES FOR USERNAME, CURRENT PASSWORD AND NEW PASSWORD
        e_usn = tk.Entry(p_win, width=18, font=("Fugaz One", 18))
        e_pwd = tk.Entry(p_win, width=18, show="", font=("Fugaz One", 18))
        e_npwd = tk.Entry(p_win, width=16, show="*", font=("Fugaz One", 18))

        e_usn.focus()

        # FUNCTION TO HIDE THE PASSWORD #
        def hide_pwdcng():
            pwd_btn.config(image=hide_img, command=show_pwdcng)
            e_npwd.config(show="*")

        # FUNCTION TO SHOW THE PASSWORD #
        def show_pwdcng():
            pwd_btn.config(image=show_img, command=hide_pwdcng)
            e_npwd.config(show="")

        # FUNCTION FOR BACK BUTTON #
        def back_pwdcng():
            # TO ENABLE THE SIGNIN, LOGIN AND CHANGE PASSWORD BUTTONS THAT WERE DISABLED BEFORE
            signup_btn.config(state="normal")
            login_btn.config(state="normal")
            pwdcng_btn.config(state="normal")
            # TO MAKE THE NEW WIDGETS THAT SHOWED UP WHEN CHANGE PASSWORD WAS CLICKED TO DIASAPPEAR
            pwdcng_label.destroy()
            usn.destroy()
            c_pwd.destroy()
            n_pwd.destroy()
            e_usn.destroy()
            e_pwd.destroy()
            e_npwd.destroy()
            pwd_btn.destroy()
            confirm_btn.destroy()
            back_btn.destroy()

        # FUNCTION FOR CONFIRM BUTTON #
        def confirm_pwdcng():

            # TO GET THE USERNAME, CURRENT PASSWORD AND NEW PASSWORD ENTERED BY THE USER
            username = e_usn.get()
            password = e_pwd.get()
            n_password = e_npwd.get()
            # TO CLEAR THE USERNAME, CURRENT PASSWORD AND NEW PASSWORD ENTERED BY THE USER
            e_usn.delete(0, "end")
            e_pwd.delete(0, "end")
            e_npwd.delete(0, "end")

            # TO CONNECT TO MySQL DATABASE
            c = my.connect(
                host="localhost", user="root", passwd="MYSQLVARY", database="todolist"
            )
            cur = c.cursor()
            # TO GET DATA FROM MySQL DATABASE
            cur.execute("select * from userpwd")
            data = cur.fetchall()
            c.close()

            # LISTS WITH ALL USERNAMES AND EMAILS
            usernames = []
            emails = []
            for x in data:
                usernames.append(x[1])
                emails.append(x[3])

            # SETTING FLAG USER = TRUE
            user = True
            # IF USERNAME IS NOT PRESENT IN LIST 'usernames', FLAG IS SET TO FALSE
            if username not in usernames:
                user = False
                messagebox.showinfo(
                    "INVALID USERNAME",
                    "THE USERNAME DOESNT EXIST. PLEASE SIGNUP FIRST.",
                )

            if username in usernames:
                for x in data:
                    # IF CURRENT PASSWORDS DONT MATCH, FLAG IS SET TO FALSE
                    if x[1] == username and x[2] != password:
                        user = False
                        messagebox.showinfo(
                            "OOPS!!!", "YOU HAVE ENTERED THE WRONG PASSWORD."
                        )
                        break

                for x in data:
                    # IF USERNAME AND CURRENT PASSWORDS MATCH, THEN FLAG IS SET TO TRUE
                    if x[1] == username and x[2] == password:
                        user = True
                        # CONNECTING TO MySQL DATABASE
                        c = my.connect(
                            host="localhost",
                            user="root",
                            passwd="MYSQLVARY",
                            database="todolist",
                        )
                        cur = c.cursor()
                        # TO DELETE THE PREVIOUS ENTRY FROM MySQL DATABASE
                        cur.execute(
                            "delete from userpwd where username='" + str(username) + "'"
                        )
                        # INSERTING THE SAME ENTRY WITH NEW PASSWORD REPLACING THE OLD PASSWORD
                        cur.execute(
                            "insert into userpwd(username, password, mail) values('"
                            + str(username)
                            + "','"
                            + str(n_password)
                            + "','"
                            + str(x[2])
                            + "')"
                        )
                        c.commit()
                        c.close()
                        messagebox.showinfo(
                            "PASSWORD CHANGE SUCCESFUL",
                            "YOU HAVE CHANGED YOUR PASSWORD!!!",
                        )
                        break
            # CALLS BELOW FUNCTION TO MAKE ALL CHANGE PASSWORD WIDGETS DISAPPEAR
            back_pwdcng()

        # SHOW AND HIDE PASSWORD BUTTONS, CONFIRM AND BACK BUTTONS
        pwd_btn = tk.Button(image=hide_img, command=show_pwdcng)
        confirm_btn = tk.Button(
            p_win,
            text="CONFIRM",
            font=("Fugaz One", 18),
            fg="black",
            padx=16,
            command=confirm_pwdcng,
        )
        back_btn = tk.Button(
            p_win,
            text="    BACK    ",
            font=("Fugaz One", 18),
            fg="black",
            padx=15,
            command=back_pwdcng,
        )

        # PLACING ALL THE WIDGETS IN CHANGE PASSWORD #
        pwdcng_label.place(x=533, y=136)
        usn.place(x=448, y=236)
        e_usn.place(x=766, y=241)
        c_pwd.place(x=448, y=311)
        e_pwd.place(x=766, y=316)
        n_pwd.place(x=448, y=386)
        e_npwd.place(x=766, y=391)
        pwd_btn.place(x=1018, y=391)
        confirm_btn.place(x=588, y=461)
        back_btn.place(x=768, y=461)

    # DISPLAYING HOME SCREEN #

    # HOME SCREEN TITLE #
    title_label = tk.Label(
        text="     WELCOME TO YOUR PERSONAL TASK REMINDER !     ",
        font=("Fugaz One", 30),
        padx=25,
        pady=25,
        fg="yellow",
        bg="black",
    )

    # HOME SCREEN SIGIN BUTTON #
    signup_btn = tk.Button(
        text="        SIGN   UP         ",
        font=("Fugaz One", 18),
        border=10,
        fg="white",
        bg="black",
        command=signup,
    )

    # HOME SCREEN LOGIN BUTTON #
    login_btn = tk.Button(
        text="           LOGIN             ",
        font=("Fugaz One", 18),
        border=10,
        fg="white",
        bg="black",
        command=login,
    )

    # HOME SCREEN CHANGE PASSWORD BUTTON #
    pwdcng_btn = tk.Button(
        p_win,
        text="CHANGE PASSWORD",
        font=("Fugaz One", 18),
        border=10,
        fg="white",
        bg="black",
        command=pwdcng,
    )

    # HOME SCREEN EXIT BUTTON #
    exit_btn = tk.Button(
        p_win,
        text="              EXIT                ",
        font=("Fugaz One", 18),
        border=10,
        fg="red",
        bg="black",
        command=p_win.destroy,
    )

    # PLACING ALL WIDGETS IN HOME SCREEN #
    title_label.place(x=213, y=6)
    signup_btn.place(x=503, y=538)
    login_btn.place(x=763, y=538)
    pwdcng_btn.place(x=633, y=626)
    exit_btn.place(x=633, y=716)

    p_win.mainloop()  # FOR THE WINDOW TO RUN TILL EXIT BUTTON OR THE RED CROSS IN THE TOP RIGHT IS CLICKED


# FUNCTION TO CREATE A NEW WINDOW #
def new_window(text):
    # CREATING NEW TKINTER WINDOW FOR THE VARIOUS FUNCTIONS
    n_win = tk.Tk()
    n_win.state("zoomed")  # MAKING THE WINDOW GET DISPLAYED IN A MAXIMISED STATE
    n_win.title(
        "Logged Into To Do List!!"
    )  # SETTING THE TITLE OF THE WINDOW TO THE NAME OF THE APPLICATION
    n_win.iconbitmap(
        "IMAGES_SUBMISSION\\icon.ico"
    )  # SETTING ICON OF THE APP WINDOW

    n_win_bg_img = tk.PhotoImage(
        file="IMAGES_SUBMISSION\\scenery2.png"
    )  # BACKGROUND IMAGE FOR THE NEW WINDOW
    # LABEL THAT CONTAINS THE BACKGROUND IMAGE AND THE WELCOME MESSAGE
    n_win_bg_img_label = tk.Label(
        n_win,
        image=n_win_bg_img,
        text="  Welcome " + text + "  \n\n\n\n\n\n\n\n\n\n\n\n\n",
        fg="yellow",
        compound="center",
        font=("Fugaz One", 30),
    )
    n_win_bg_img_label.place(x=0, y=0)

    # FUNCTION TO ADD TASK #
    def add_task():
        # TO DISABLE THE OTHER FUNCTIONS WHEN ADD TASK BUTTON IS CLICKED AND ADD TASK FUNCTION IS BEING PERFROMED
        add_task_btn.config(state="disabled")
        edit_task_btn.config(state="disabled")
        delete_task_btn.config(state="disabled")
        view_task_btn.config(state="disabled")
        back_btn.config(state="disabled")

        # WIDGETS REQUIRED TO PERFORM ALL FUNCTIONS IN ADD TASK
        rem_name_label = tk.Label(
            n_win,
            text="NAME OF THE REMINDER : ",
            fg="white",
            bg="black",
            font=("Fugaz One", 18),
        )
        e_rem_name = tk.Entry(width=30, font=("Fugaz One", 18))

        e_rem_name.focus()

        rem_name_label.place(x=386, y=225)
        e_rem_name.place(x=706, y=225)

        c_datentime = dt.datetime.now()
        c_date = c_datentime.date()
        c_year = int(str(c_date)[0:4])
        c_month = int(str(c_date)[5:7])
        c_date = int(str(c_date)[8:10])
        c_hour = int(str(c_datentime.time())[0:2])
        c_minute = int(str(c_datentime.time())[3:5])
        # SELECTING THE CURRENT DAY'S DATE ON THE CALENDAR BY DEFAULT
        cal = tkc.Calendar(
            n_win,
            selectmode="day",
            year=c_year,
            month=c_month,
            day=c_date,
            pady=10,
            fill="BOTH",
        )
        cal.place(x=458, y=275)

        reminder_option_label = tk.Label(
            n_win, text="REMIND ME? : ", font=("Fugaz One", 18), fg="white", bg="black"
        )
        reminder_option_label.place(x=730, y=275)
        rem_option = tk.StringVar()
        yes_rem_rb = tk.Radiobutton(n_win, text="YES", variable=rem_option, value="Y")
        no_rem_rb = tk.Radiobutton(n_win, text="NO", variable=rem_option, value="N")
        yes_rem_rb.place(x=930, y=280)
        no_rem_rb.place(x=930, y=315)
        no_rem_rb.select()  # TO HAVE 'No' SELECTED BY DEFAULT

        frequency_label = tk.Label(
            n_win,
            text="FREQUENCY OF REMINDERS : ",
            fg="white",
            bg="black",
            font=("Fugaz One", 18),
        )
        frequency_label.place(x=730, y=380)
        rec_options = ["ONCE", "DAILY", "WEEKLY", "MONTHLY"]
        recurring_freq_var = tk.StringVar()
        recurring_freq_var.set(
            rec_options[0]
        )  # TO SET 'ONCE' AS THE FREQUENCY BY DEFAULT
        rec_or_not_dropdown = tk.OptionMenu(n_win, recurring_freq_var, *rec_options)
        rec_or_not_dropdown.place(x=1088, y=385)

        hour_label = tk.Label(
            n_win, text="HOUR : ", font=("Fugaz One", 18), fg="white", bg="black"
        )
        hour_label.place(x=400, y=500)
        hours = []
        # LOOP TO GET THE STRING OF ALL HOURS AS A 2 CHARACTERS
        for i in range(0, 12):
            if i < 10:
                i = "0" + str(i)
                hours.append(i)
            else:
                i = str(i)
                hours.append(i)

        hour_var = tk.StringVar()
        am_pm_dropdown_set = "a.m"
        if c_hour > 11:
            c_hour -= 12
            am_pm_dropdown_set = "p.m"

        # TO KEEP THE CURRENT TIME SELECTED BY DEFAULT
        if len(str(c_hour)) == 1:
            c_hour = "0" + str(c_hour)
        else:
            c_hour = str(c_hour)

        for i in hours:
            if i == c_hour:
                hour_var.set(i)
        hour_dropdown = tk.OptionMenu(n_win, hour_var, *hours)
        hour_dropdown.place(x=500, y=505)

        minute_label = tk.Label(
            n_win, text="MINUTE : ", font=("Fugaz One", 18), fg="white", bg="black"
        )
        minute_label.place(x=690, y=500)
        minutes = []
        for i in range(0, 60):
            if i < 10:
                i = "0" + str(i)
                minutes.append(i)
            else:
                i = str(i)
                minutes.append(i)
        minute_var = tk.StringVar()
        if len(str(c_minute)) == 1:
            c_minute = "0" + str(c_minute)
        else:
            c_minute = str(c_minute)
        for i in minutes:
            if i == c_minute:
                minute_var.set(i)
        minute_dropdown = tk.OptionMenu(n_win, minute_var, *minutes)
        minute_dropdown.place(x=820, y=505)

        am_pm_label = tk.Label(
            n_win, text="A.M / P.M : ", font=("Fugaz One", 18), fg="white", bg="black"
        )
        am_pm_label.place(x=980, y=500)

        am_pm_list = ["a.m", "p.m"]
        am_pm_var = tk.StringVar()
        if am_pm_dropdown_set == "a.m":
            am_pm_var.set(am_pm_list[0])
        elif am_pm_dropdown_set == "p.m":
            am_pm_var.set(am_pm_list[1])
        am_pm_dropdown = tk.OptionMenu(n_win, am_pm_var, *am_pm_list)
        am_pm_dropdown.place(x=1130, y=505)

        rem_desc_label = tk.Label(
            n_win,
            text="REMINDER DESCRIPTION : ",
            font=("Fugaz One", 18),
            fg="white",
            bg="black",
        )
        rem_desc_label.place(x=386, y=550)
        rem_desc_text = tk.Text(n_win, font=("Fugaz One", 18), height=5, width=30)
        rem_desc_text.place(x=706, y=550)

        # FUNCTION OF BACK BUTTON INSIDE ADD TASK #
        def back_at_fn():
            # TO ENABLE THE DISABLED WIDGETS
            add_task_btn.config(state="normal")
            edit_task_btn.config(state="normal")
            delete_task_btn.config(state="normal")
            view_task_btn.config(state="normal")
            back_btn.config(state="normal")
            # TO DESTROY ALL ADD TASK WIDGETS THAT WERE ADDED
            rem_name_label.destroy()
            e_rem_name.destroy()
            cal.destroy()
            hour_label.destroy()
            hour_dropdown.destroy()
            minute_label.destroy()
            minute_dropdown.destroy()
            am_pm_label.destroy()
            am_pm_dropdown.destroy()
            rem_desc_label.destroy()
            rem_desc_text.destroy()
            add_btn.destroy()
            back_at_btn.destroy()
            reminder_option_label.destroy()
            yes_rem_rb.destroy()
            no_rem_rb.destroy()
            frequency_label.destroy()
            rec_or_not_dropdown.destroy()

        # FUNCTION OF ADD BUTTON INSIDE ADD TASK #
        def add_btn_fn():
            # COLLECTING THE DATA ENTERED BY THE USER AS SOON AS ADD TASK BUTTON IS CLICKED
            reminder_option = rem_option.get()
            reminder_frequency = recurring_freq_var.get()
            reminder_name = e_rem_name.get()
            reminder_desc = rem_desc_text.get(1.0, "end")
            date_raw = str(cal.get_date())
            ymd = date_raw.split("/")
            year = "20" + ymd[2]
            if int(ymd[0]) > 9:
                month = ymd[0]
            else:
                month = "0" + ymd[0]

            if int(ymd[1]) > 9:
                day = ymd[1]
            else:
                day = "0" + ymd[1]

            date = year + "-" + month + "-" + day

            hour = hour_var.get()
            minute = minute_var.get()
            am_pm = am_pm_var.get()

            if am_pm == "p.m":
                hour = str(int(hour) + 12)

            time = str(hour) + ":" + str(minute) + ":" + "00"

            # SETTING A FLAG ADD TASK TO TABLE = TRUE
            add_task_table = True
            # IF NAME OF THE REMINDER IS NULL, FLAG BECOMES FALSE
            if len(reminder_name) == 0:
                messagebox.showinfo(
                    "INVALID NAME OF REMINDER",
                    "NOTE : NAME OF THE REMINDER CANNOT BE NULL. ",
                )
                add_task_table = False

            # IF NAME OF THE REMINDER IS MORE THAN 30 CHARACTERS, FLAG BECOMES FALSE
            if len(reminder_name) > 30:
                messagebox.showinfo(
                    "INVALID NAME OF REMINDER",
                    "NOTE : NAME OF THE REMINDER HAS EXCEEDED 30 CHARACTERS.",
                )
                add_task_table = False

            # IF REMINDER DESCRIPTION IS NULL, FLAG BECOMES FALSE
            if len(reminder_desc) == 0:
                messagebox.showinfo(
                    "INVALID DESCEIPTION OF REMINDER",
                    "NOTE : DESCRIPTION OF REMINDER CANNOT BE NULL.",
                )
                add_task_table = False

            # IF REMINDER DESCRIPTION IS MORE THAN 150 CHARACTERS, FLAG BECOMES FALSE
            if len(reminder_desc) > 150:
                messagebox.showinfo(
                    "INVALID DESCEIPTION OF REMINDER",
                    "NOTE : DESRIPTION OF REMINDER HAS REACHED 150 CHARACTERS",
                )
                add_task_table = False

            # AT THE END OF ALL REQUIRED IF CONDITIONS, IF FLAG IS TRUE TASK IS ADDED TO THE DATABASE
            if add_task_table == True:
                # CONNECTING TO MySQL DATABASE
                c = my.connect(
                    host="localhost",
                    user="root",
                    passwd="MYSQLVARY",
                    database="todolist",
                )
                cur = c.cursor()
                # TO INSERT THE TASK THAT THE USER WANTS TO ADD
                cur.execute(
                    "INSERT INTO usertasks(username, reminder_date, reminder_time, reminder_name, rem_description, rem_option, rem_frequency) VALUES('"
                    + text
                    + "','"
                    + date
                    + "','"
                    + time
                    + "','"
                    + reminder_name
                    + "','"
                    + reminder_desc
                    + "','"
                    + reminder_option
                    + "','"
                    + reminder_frequency
                    + "')"
                )
                c.commit()
                c.close()
                messagebox.showinfo(
                    "TASK ADDED!!", "TASK HAS BEEN ADDED SUCCESFULLY!!!"
                )
                # CALLS THE BELOW FUNCTION SO THAT USER IS TAKEN BACK TO THE MAIN MENU AFTER ADDING A TASK
                back_at_fn()

        # ADD AND BACK BUTTONS
        add_btn = tk.Button(
            n_win,
            text="  ADD  ",
            font=("Fugaz One", 18),
            bg="black",
            fg="green",
            command=add_btn_fn,
        )
        add_btn.place(x=650, y=735)
        back_at_btn = tk.Button(
            n_win,
            text="  BACK ",
            font=("Fugaz One", 18),
            bg="black",
            fg="red",
            command=back_at_fn,
        )
        back_at_btn.place(x=750, y=735)

    # FUNCTION TO EDIT TASK #
    def edit_task():
        # SETTING A FLAG WITH EDIT TASK STATUS = FALSE
        edit_task_status = False
        # DISABLING ALL THE MENU BUTTONS SO THAT THE USER CANNOT ACCESS ANOTHER FUNCTION WHILE INSIDE THIS FUNCTION
        add_task_btn.config(state="disabled")
        edit_task_btn.config(state="disabled")
        delete_task_btn.config(state="disabled")
        view_task_btn.config(state="disabled")
        back_btn.config(state="disabled")

        # WIDGETS TO DISPLAY THE LISTBOX WITH EVENTS AND THE EDIT AND BACK BUTTONS
        events_label = tk.Label(
            n_win,
            text="THESE ARE YOUR EVENTS : ",
            font=("Fugaz One", 18),
            fg="white",
            bg="black",
        )
        events_label.place(x=165, y=225)  # x=615, y=275
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=25)
        style.map("Treeview", background=[("selected", "blue")])
        listbox_scrollbar_frame = tk.Frame(n_win)
        scrollbar = tk.Scrollbar(listbox_scrollbar_frame, orient="vertical")
        h_scrollbar = tk.Scrollbar(listbox_scrollbar_frame, orient="horizontal")
        scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        events_treeview = ttk.Treeview(
            listbox_scrollbar_frame,
            yscrollcommand=scrollbar.set,
            xscrollcommand=h_scrollbar.set,
            selectmode="browse",
            height=16,
        )
        events_treeview.pack()

        scrollbar.config(command=events_treeview.yview)
        h_scrollbar.config(command=events_treeview.xview)

        events_treeview.pack()

        events_treeview["columns"] = (
            "TASK ID",
            "REMINDER NAME",
            "DATE",
            "TIME",
            "FREQUENCY",
            "REMINDER OPTION",
        )

        # FORMATE THE COLUMNS
        events_treeview.column("#0", width=0)
        events_treeview.column("TASK ID", width=40, minwidth=40, anchor="center")
        events_treeview.column("REMINDER NAME", width=200, minwidth=200, anchor="w")
        events_treeview.column("DATE", width=130, minwidth=130, anchor="center")
        events_treeview.column("TIME", width=110, minwidth=110, anchor="w")
        events_treeview.column("FREQUENCY", width=100, minwidth=100, anchor="w")
        events_treeview.column(
            "REMINDER OPTION", width=90, minwidth=90, anchor="center"
        )

        # CREATE HEADINGS
        events_treeview.heading("#0", text="", anchor="center")
        events_treeview.heading("TASK ID", text="S.NO", anchor="center")
        events_treeview.heading("REMINDER NAME", text="REMINDER NAME", anchor="center")
        events_treeview.heading("DATE", text="DATE", anchor="center")
        events_treeview.heading("TIME", text="TIME", anchor="center")
        events_treeview.heading("FREQUENCY", text="FREQUENCY", anchor="center")
        events_treeview.heading("REMINDER OPTION", text="REMINDER?", anchor="center")

        # CONNECTING TO MySQL DATABASE
        c = my.connect(
            host="localhost", user="root", passwd="MYSQLVARY", database="todolist"
        )
        cur = c.cursor()
        # TO GET ALL DATA FROM DATABASE FOR THE CURRENT USER
        cur.execute(
            "SELECT  SNO, REMINDER_NAME, REMINDER_DATE, REMINDER_TIME, REM_FREQUENCY, REM_OPTION, REM_DESCRIPTION FROM usertasks WHERE username = '"
            + text
            + "' ORDER BY REMINDER_DATE DESC"
        )
        tasks_dt_listbox = cur.fetchall()
        c.close()

        events_treeview.tag_configure(
            "oddrow", background="white", font=("Source Code Pro", 12)
        )
        events_treeview.tag_configure(
            "evenrow", background="lightblue", font=("Source Code Pro", 12)
        )
        c = 0
        for i in tasks_dt_listbox:
            if c % 2 == 0:
                events_treeview.insert(
                    parent="",
                    index="end",
                    iid=c,
                    values=(i[0], i[1], i[2], i[3], i[4], i[5]),
                    tags=("evenrow",),
                )
            else:
                events_treeview.insert(
                    parent="",
                    index="end",
                    iid=c,
                    values=(i[0], i[1], i[2], i[3], i[4], i[5]),
                    tags=("oddrow",),
                )
            c += 1

        listbox_scrollbar_frame.place(x=10, y=275)  # x=395, y=325

        # FUNCTION OF BACK BUTTON INSIDE DELETE TASK #
        def back_et_fn():
            # TO NORMALISE THE BUTTONS THAT WERE DISABLED EARLIER
            add_task_btn.config(state="normal")
            edit_task_btn.config(state="normal")
            delete_task_btn.config(state="normal")
            view_task_btn.config(state="normal")
            back_btn.config(state="normal")
            # TO MAKE ALL THE EDIT TASK WIDGETS DISAPPEAR
            events_label.destroy()
            listbox_scrollbar_frame.destroy()
            edit_btn.destroy()
            back_et_btn.destroy()

        # FUNCTION OF EDIT BUTTON INSIDE EDIT TASK #
        def edit_btn_fn():
            if len(events_treeview.selection()) == 1:
                edit_btn.config(state="disabled")
                back_et_btn.config(state="disabled")
                et = events_treeview.selection()[0]
                print(et)
                print(tasks_dt_listbox[int(et)])
                rem_name_label = tk.Label(
                    n_win,
                    text="NAME OF THE REMINDER : ",
                    fg="white",
                    bg="black",
                    font=("Fugaz One", 18),
                )
                e_rem_name = tk.Entry(width=30, font=("Fugaz One", 18))
                e_rem_name.insert(0, tasks_dt_listbox[int(et)][1])

                e_rem_name.focus()

                rem_name_label.place(
                    x=726, y=225
                )
                e_rem_name.place(x=1046, y=225)

                cal = tkc.Calendar(
                    n_win,
                    selectmode="day",
                    year=int(str(tasks_dt_listbox[int(et)][2])[0:4]),
                    month=int(str(tasks_dt_listbox[int(et)][2])[5:7]),
                    day=int(str(tasks_dt_listbox[int(et)][2])[8:]),
                    pady=10,
                    fill="BOTH",
                )
                cal.place(x=798, y=275)

                reminder_option_label = tk.Label(
                    n_win,
                    text="REMIND ME? : ",
                    font=("Fugaz One", 18),
                    fg="white",
                    bg="black",
                )
                reminder_option_label.place(x=1070, y=275)
                rem_option = tk.StringVar()
                yes_rem_rb = tk.Radiobutton(
                    n_win, text="YES", variable=rem_option, value="Y"
                )
                no_rem_rb = tk.Radiobutton(
                    n_win, text="NO", variable=rem_option, value="N"
                )
                yes_rem_rb.place(x=1270, y=280)
                no_rem_rb.place(x=1270, y=315)
                if tasks_dt_listbox[int(et)][5] == "Y":
                    yes_rem_rb.select()
                elif tasks_dt_listbox[int(et)][5] == "N":
                    no_rem_rb.select()

                frequency_label = tk.Label(
                    n_win,
                    text="FREQUENCY OF REMINDERS : ",
                    fg="white",
                    bg="black",
                    font=("Fugaz One", 18),
                )
                frequency_label.place(x=1070, y=380)
                rec_options = ["ONCE", "DAILY", "WEEKLY", "MONTHLY"]
                recurring_freq_var = tk.StringVar()
                if tasks_dt_listbox[int(et)][4] == "ONCE":
                    recurring_freq_var.set(rec_options[0])
                elif tasks_dt_listbox[int(et)][4] == "DAILY":
                    recurring_freq_var.set(rec_options[1])
                elif tasks_dt_listbox[int(et)][4] == "WEEKLY":
                    recurring_freq_var.set(rec_options[2])
                elif tasks_dt_listbox[int(et)][4] == "MONTHLY":
                    recurring_freq_var.set(rec_options[3])

                rec_or_not_dropdown = tk.OptionMenu(
                    n_win, recurring_freq_var, *rec_options
                )
                rec_or_not_dropdown.place(
                    x=1428, y=385
                )

                hour_label = tk.Label(
                    n_win,
                    text="HOUR : ",
                    font=("Fugaz One", 18),
                    fg="white",
                    bg="black",
                )
                hour_label.place(x=740, y=500)
                hours = []
                for i in range(0, 12):
                    if i < 10:
                        i = "0" + str(i)
                        hours.append(i)
                    else:
                        i = str(i)
                        hours.append(i)

                hour_var = tk.StringVar()
                if len(str(tasks_dt_listbox[int(et)][3])) == 8:
                    if int(str(tasks_dt_listbox[int(et)][3])[0:2]) < 12:
                        if len(str(tasks_dt_listbox[int(et)][3])[0:2]) == 1:
                            hour_var.set("0" + str(tasks_dt_listbox[int(et)][3])[0:2])
                        else:
                            hour_var.set(str(tasks_dt_listbox[int(et)][3])[0:2])
                        amorpm = "a.m"
                    else:
                        if (
                            len(str(int(str(tasks_dt_listbox[int(et)][3])[0:2]) - 12))
                            == 1
                        ):
                            hour_var.set(
                                "0"
                                + str(int(str(tasks_dt_listbox[int(et)][3])[0:2]) - 12)
                            )
                        else:
                            hour_var.set(
                                str(int(str(tasks_dt_listbox[int(et)][3])[0:2]) - 12)
                            )
                        amorpm = "p.m"
                elif len(str(tasks_dt_listbox[int(et)][3])) == 7:
                    if int(str(tasks_dt_listbox[int(et)][3])[0:1]) < 12:
                        hour_var.set("0" + str(tasks_dt_listbox[int(et)][3])[0:1])
                        amorpm = "a.m"
                hour_dropdown = tk.OptionMenu(n_win, hour_var, *hours)
                hour_dropdown.place(x=840, y=505)

                minute_label = tk.Label(
                    n_win,
                    text="MINUTE : ",
                    font=("Fugaz One", 18),
                    fg="white",
                    bg="black",
                )
                minute_label.place(x=1030, y=500)
                minutes = []
                for i in range(0, 60):
                    if i < 10:
                        i = "0" + str(i)
                        minutes.append(i)
                    else:
                        i = str(i)
                        minutes.append(i)

                minute_var = tk.StringVar()
                if len(str(tasks_dt_listbox[int(et)][3])) == 8:
                    minute_var.set(str(tasks_dt_listbox[int(et)][3])[3:5])
                elif len(str(tasks_dt_listbox[int(et)][3])) == 7:
                    minute_var.set(str(tasks_dt_listbox[int(et)][3])[2:4])
                minute_dropdown = tk.OptionMenu(n_win, minute_var, *minutes)
                minute_dropdown.place(x=1160, y=505)

                am_pm_label = tk.Label(
                    n_win,
                    text="A.M / P.M : ",
                    font=("Fugaz One", 18),
                    fg="white",
                    bg="black",
                )
                am_pm_label.place(x=1320, y=500)

                am_pm_list = ["a.m", "p.m"]
                am_pm_var = tk.StringVar()
                if amorpm == "a.m":
                    am_pm_var.set(am_pm_list[0])
                elif amorpm == "p.m":
                    am_pm_var.set(am_pm_list[1])
                am_pm_dropdown = tk.OptionMenu(n_win, am_pm_var, *am_pm_list)
                am_pm_dropdown.place(x=1470, y=505)

                rem_desc_label = tk.Label(
                    n_win,
                    text="REMINDER DESCRIPTION : ",
                    font=("Fugaz One", 18),
                    fg="white",
                    bg="black",
                )
                rem_desc_label.place(
                    x=726, y=550
                )
                rem_desc_text = tk.Text(
                    n_win, font=("Fugaz One", 18), height=5, width=30
                )
                # reminder_description = tasks_dt_listbox[int(et)][6]
                rem_desc_text.insert(1.0, str(tasks_dt_listbox[int(et)][6]))
                rem_desc_text.place(x=1046, y=550)

                # FUNCTION OF BACK BUTTON INSIDE ADD TASK #
                def back_at_fn():
                    # TO NORMALISE THE EARLIER EDIT TASK WIDGETS THAT WERE DISABLED
                    edit_btn.config(state="normal")
                    # listbox_scrollbar_frame.config(state="normal")
                    back_et_btn.config(state="normal")
                    # TO MAKE THE ADD TASK WIDGETS IN EDIT TASK FUNCTION TO DISAPPEAR
                    rem_name_label.destroy()
                    e_rem_name.destroy()
                    cal.destroy()
                    hour_label.destroy()
                    hour_dropdown.destroy()
                    minute_label.destroy()
                    minute_dropdown.destroy()
                    am_pm_label.destroy()
                    am_pm_dropdown.destroy()
                    rem_desc_label.destroy()
                    rem_desc_text.destroy()
                    add_btn.destroy()
                    back_at_btn.destroy()
                    reminder_option_label.destroy()
                    yes_rem_rb.destroy()
                    no_rem_rb.destroy()
                    frequency_label.destroy()
                    rec_or_not_dropdown.destroy()

                    # FUNCTION OF UPDATE BUTTON INSIDE ADD TASK #

                def update_btn_fn():
                    # TO GET ALL THE DETAILS ENTERED IN BY THE USER AS SOON AS UPDATE BUTTON IS CLICKED
                    reminder_option = rem_option.get()
                    reminder_frequency = recurring_freq_var.get()
                    reminder_name = e_rem_name.get()
                    print(reminder_name)
                    reminder_desc = rem_desc_text.get(1.0, "end")
                    print(reminder_desc)
                    date_raw = str(cal.get_date())
                    ymd = date_raw.split("/")
                    year = "20" + ymd[2]
                    if int(ymd[0]) > 9:
                        month = ymd[0]
                    else:
                        month = "0" + ymd[0]

                    if int(ymd[1]) > 9:
                        day = ymd[1]
                    else:
                        day = "0" + ymd[1]

                    date = year + "-" + month + "-" + day

                    hour = hour_var.get()
                    minute = minute_var.get()
                    am_pm = am_pm_var.get()

                    if am_pm == "p.m":
                        hour = str(int(hour) + 12)

                    time = str(hour) + ":" + str(minute) + ":" + "00"
                    # SETTING A FLAG ADD TASK STATUS = TRUE
                    add_task_table = True
                    # IF NAME OF THE REMINDER IS NULL, FLAG IS SET TO FALSE
                    if len(reminder_name) == 0:
                        messagebox.showinfo(
                            "INVALID NAME OF REMINDER",
                            "NOTE : NAME OF THE REMINDER CANNOT BE NULL. ",
                        )
                        add_task_table = False
                    # IF NAME OF REMINDER EXCEEDS 30 CHARACTERS, FLAG IS SET TO FALSE
                    if len(reminder_name) > 30:
                        messagebox.showinfo(
                            "INVALID NAME OF REMINDER",
                            "NOTE : NAME OF THE REMINDER HAS EXCEEDED 30 CHARACTERS.",
                        )
                        add_task_table = False
                    # IF REMINDER DESCRIPTION IS NULL, FLAG IS SET TO FALSE
                    if len(reminder_desc) == 0:
                        messagebox.showinfo(
                            "INVALID DESCEIPTION OF REMINDER",
                            "NOTE : DESCRIPTION OF REMINDER CANNOT BE NULL.",
                        )
                        add_task_table = False
                    # IF REMINDER DESCRIPTION IS MORE THAN 150 CHARACTERS, FLAG IS SET TO FALSE
                    if len(reminder_desc) > 150:
                        messagebox.showinfo(
                            "INVALID DESCEIPTION OF REMINDER",
                            "NOTE : DESRIPTION OF REMINDER HAS REACHED 150 CHARACTERS",
                        )
                        add_task_table = False
                    # AT END OF ALL IF CONDITIONS, IF ADD TASK TO TABLES FLAG IS TRUE, TASK IS UPDATE
                    if add_task_table == True:
                        print(date)
                        print(time)
                        print(reminder_name)
                        print(reminder_desc)
                        # CONNECTING TO MySQL DATABASE
                        c = my.connect(
                            host="localhost",
                            user="root",
                            passwd="MYSQLVARY",
                            database="todolist",
                        )
                        cur = c.cursor()
                        # UPDATING THE TASK IN TABLE WITH THE EDITED INFO AS THE USER WANTS IT TO BE
                        cur.execute(
                            "UPDATE usertasks SET reminder_date='"
                            + str(date)
                            + "', reminder_time='"
                            + str(time)
                            + "',reminder_name='"
                            + reminder_name
                            + "',rem_description='"
                            + reminder_desc
                            + "',rem_option='"
                            + reminder_option
                            + "',rem_frequency='"
                            + reminder_frequency
                            + "' where SNO="
                            + str(tasks_dt_listbox[int(et)][0])
                        )

                        c.commit()
                        c.close()
                        messagebox.showinfo(
                            "TASK EDITED!!",
                            "TASK HAS BEEN EDITED SUCCESFULLY!!!",
                        )
                        back_at_fn()
                        back_et_fn()

                # UPDATE AND BACK BUTTONS INSIDE EDIT TASK FUNCTION
                add_btn = tk.Button(
                    n_win,
                    text=" UPDATE ",
                    font=("Fugaz One", 18),
                    bg="black",
                    fg="green",
                    command=update_btn_fn,
                )
                add_btn.place(x=975, y=735)
                back_at_btn = tk.Button(
                    n_win,
                    text="  BACK ",
                    font=("Fugaz One", 18),
                    bg="black",
                    fg="red",
                    command=back_at_fn,
                )
                back_at_btn.place(x=1110, y=735)

            # IF THERE ARE CURRENTLY NO TASKS PRESENT IN THE USER'S ACCOUNT
            else:
                messagebox.showinfo(
                    "NO TASK SELECTED",
                    "SELECT A TASK TO CONTINUE",
                )
                edit_btn.config(state="normal")
                back_et_btn.config(state="normal")

        # EDIT AND BACK BUTTON
        edit_btn = tk.Button(
            n_win,
            text="  EDIT  ",
            font=("Fugaz One", 18),
            bg="black",
            fg="red",
            command=edit_btn_fn,
        )
        edit_btn.place(x=210, y=735)

        back_et_btn = tk.Button(
            n_win,
            text="  BACK  ",
            font=("Fugaz One", 18),
            bg="black",
            fg="white",
            command=back_et_fn,
        )
        back_et_btn.place(x=320, y=735)

    # FUNCTION TO DELETE TASK #
    def delete_task():
        # TO DISABLE THE OTHER FUNCTIONS IN THE MAIN MENU SO THAT THE USER CANNOT ACCESS OTHER TASKS FROM DELETE TASK FUNCTION
        add_task_btn.config(state="disabled")
        edit_task_btn.config(state="disabled")
        delete_task_btn.config(state="disabled")
        view_task_btn.config(state="disabled")
        back_btn.config(state="disabled")

        # WIDGETS IN THE DELETE TASK FUNCTION
        events_label = tk.Label(
            n_win,
            text="THESE ARE YOUR EVENTS : ",
            font=("Fugaz One", 18),
            fg="white",
            bg="black",
        )
        events_label.place(x=615, y=275)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=25)
        style.map("Treeview", background=[("selected", "blue")])
        listbox_scrollbar_frame = tk.Frame(n_win)
        scrollbar = tk.Scrollbar(listbox_scrollbar_frame, orient="vertical")
        ho_scrollbar = tk.Scrollbar(listbox_scrollbar_frame, orient="horizontal")
        scrollbar.pack(side="right", fill="y")
        ho_scrollbar.pack(side="bottom", fill="x")
        events_treeview = ttk.Treeview(
            listbox_scrollbar_frame,
            yscrollcommand=scrollbar.set,
            xscrollcommand=ho_scrollbar.set,
            selectmode="browse",
            height=14,
        )
        events_treeview.pack()

        scrollbar.config(command=events_treeview.yview)
        ho_scrollbar.config(command=events_treeview.xview)

        events_treeview.pack()

        events_treeview["columns"] = (
            "TASK ID",
            "REMINDER NAME",
            "DATE",
            "TIME",
            "FREQUENCY",
            "REMINDER OPTION",
        )

        # FORMATE THE COLUMNS
        events_treeview.column("#0", width=0)
        events_treeview.column("TASK ID", width=60, minwidth=60, anchor="center")
        events_treeview.column("REMINDER NAME", width=200, minwidth=200, anchor="w")
        events_treeview.column("DATE", width=150, minwidth=150, anchor="center")
        events_treeview.column("TIME", width=110, minwidth=110, anchor="w")
        events_treeview.column("FREQUENCY", width=100, minwidth=100, anchor="w")
        events_treeview.column(
            "REMINDER OPTION", width=140, minwidth=140, anchor="center"
        )

        # CREATE HEADINGS
        events_treeview.heading("#0", text="", anchor="center")
        events_treeview.heading("TASK ID", text="TASK ID", anchor="center")
        events_treeview.heading("REMINDER NAME", text="REMINDER NAME", anchor="center")
        events_treeview.heading("DATE", text="DATE", anchor="center")
        events_treeview.heading("TIME", text="TIME", anchor="center")
        events_treeview.heading("FREQUENCY", text="FREQUENCY", anchor="center")
        events_treeview.heading(
            "REMINDER OPTION", text="REMINDER OPTION", anchor="center"
        )

        # CONNECTING TO MySQL DATABASE
        c = my.connect(
            host="localhost", user="root", passwd="MYSQLVARY", database="todolist"
        )
        cur = c.cursor()
        # TO GET ALL DATA FROM DATABASE FOR THE CURRENT USER
        cur.execute(
            "SELECT  SNO, REMINDER_NAME, REMINDER_DATE, REMINDER_TIME, REM_FREQUENCY, REM_OPTION FROM usertasks WHERE username = '"
            + text
            + "' ORDER BY REMINDER_DATE DESC"
        )
        tasks_dt_listbox = cur.fetchall()
        c.close()

        events_treeview.tag_configure(
            "oddrow", background="white", font=("Source Code Pro", 12)
        )
        events_treeview.tag_configure(
            "evenrow", background="lightblue", font=("Source Code Pro", 12)
        )
        c = 0
        for i in tasks_dt_listbox:
            if c % 2 == 0:
                events_treeview.insert(
                    parent="", index="end", iid=c, values=i, tags=("evenrow",)
                )
            else:
                events_treeview.insert(
                    parent="", index="end", iid=c, values=i, tags=("oddrow",)
                )
            c += 1

        listbox_scrollbar_frame.place(x=395, y=325)

        # FUNCTION OF BACK BUTTON INSIDE DELETE TASK #
        def back_dt_fn():
            # TO NORMALISE THE OTHER FUNCTIONS THAT WERE DISABLED EARLIER
            add_task_btn.config(state="normal")
            edit_task_btn.config(state="normal")
            delete_task_btn.config(state="normal")
            view_task_btn.config(state="normal")
            back_btn.config(state="normal")
            # TO MAKE ALL DELETE TASK WIDGETS TO DISAPPEAR
            events_label.destroy()
            listbox_scrollbar_frame.destroy()
            delete_btn.destroy()
            back_dt_btn.destroy()

        # FUNCTION OF DELETE BUTTON INSIDE DELETE TASK #
        def delete_dt_fn():
            if len(events_treeview.selection()) == 1:
                dt = events_treeview.selection()[0]
                print(dt)
                print(tasks_dt_listbox[int(dt)])
                c = my.Connect(
                    host="localhost",
                    user="root",
                    passwd="MYSQLVARY",
                    database="todolist",
                )
                cur = c.cursor()
                qry = (
                    "DELETE FROM usertasks WHERE username='"
                    + text
                    + "' and SNO="
                    + str(tasks_dt_listbox[int(dt)][0])
                )
                cur.execute(qry)
                c.commit()
                c.close()
                messagebox.showinfo(
                    "TASK DELETED!!", "THE SELECTED TASK HAS BEEN DELETED!"
                )
                events_treeview.delete(dt)
                back_dt_fn()
            elif len(events_treeview.selection()) == 0:
                messagebox.showinfo(
                    "NO TASK SELECTED",
                    "SELECT A TASK TO DELETE\nIF YOU DO NOT HAVE TASKS,\nADD TASKS AND USE THIS FUNCTIONALITY",
                )

        # DELETE AND BACK BUTTONS
        delete_btn = tk.Button(
            n_win,
            text="DELETE",
            font=("Fugaz One", 18),
            bg="black",
            fg="red",
            command=delete_dt_fn,
        )
        delete_btn.place(x=680, y=725)

        back_dt_btn = tk.Button(
            n_win,
            text="  BACK  ",
            font=("Fugaz One", 18),
            bg="black",
            fg="white",
            command=back_dt_fn,
        )
        back_dt_btn.place(x=800, y=725)

    # FUNCTION TO VIEW TASK #
    def view_task():
        # TO DISABLE ALL THE OTHER MAIN MENU FUNCTIONS TO THAT USER CANNOT ACCESS OTHER FUNCTIONS INSIDE VIEW TASK FUNCTION
        add_task_btn.config(state="disabled")
        edit_task_btn.config(state="disabled")
        delete_task_btn.config(state="disabled")
        view_task_btn.config(state="disabled")
        back_btn.config(state="disabled")
        # WIDGETS IN VIEW TASK FUNCTION
        events_label = tk.Label(
            n_win,
            text="THESE ARE YOUR EVENTS : ",
            font=("Fugaz One", 18),
            fg="white",
            bg="black",
        )
        events_label.place(x=615, y=275)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=25)
        style.map("Treeview", background=[("selected", "blue")])
        listbox_scrollbar_frame = tk.Frame(n_win)
        scrollbar = tk.Scrollbar(listbox_scrollbar_frame, orient="vertical")
        hor_scrollbar = tk.Scrollbar(listbox_scrollbar_frame, orient="horizontal")
        scrollbar.pack(side="right", fill="y")
        hor_scrollbar.pack(side="bottom", fill="x")
        events_treeview = ttk.Treeview(
            listbox_scrollbar_frame,
            yscrollcommand=scrollbar.set,
            xscrollcommand=hor_scrollbar.set,
            selectmode="browse",
            height=14,
        )
        events_treeview.pack()

        scrollbar.config(command=events_treeview.yview)
        hor_scrollbar.config(command=events_treeview.xview)

        events_treeview.pack()

        events_treeview["columns"] = (
            "TASK ID",
            "REMINDER NAME",
            "DATE",
            "TIME",
            "FREQUENCY",
            "REMINDER OPTION",
        )

        # FORMATE THE COLUMNS
        events_treeview.column("#0", width=0)
        events_treeview.column("TASK ID", width=60, minwidth=60, anchor="center")
        events_treeview.column("REMINDER NAME", width=200, minwidth=200, anchor="w")
        events_treeview.column("DATE", width=150, minwidth=150, anchor="center")
        events_treeview.column("TIME", width=110, minwidth=110, anchor="w")
        events_treeview.column("FREQUENCY", width=100, minwidth=100, anchor="w")
        events_treeview.column(
            "REMINDER OPTION", width=140, minwidth=140, anchor="center"
        )

        # CREATE HEADINGS
        events_treeview.heading("#0", text="", anchor="center")
        events_treeview.heading("TASK ID", text="TASK ID", anchor="center")
        events_treeview.heading("REMINDER NAME", text="REMINDER NAME", anchor="center")
        events_treeview.heading("DATE", text="DATE", anchor="center")
        events_treeview.heading("TIME", text="TIME", anchor="center")
        events_treeview.heading("FREQUENCY", text="FREQUENCY", anchor="center")
        events_treeview.heading(
            "REMINDER OPTION", text="REMINDER OPTION", anchor="center"
        )

        # CONNECTING TO MySQL DATABASE
        c = my.connect(
            host="localhost", user="root", passwd="MYSQLVARY", database="todolist"
        )
        cur = c.cursor()
        # TO GET ALL DATA FROM DATABASE FOR THE CURRENT USER
        cur.execute(
            "SELECT  SNO, REMINDER_NAME, REMINDER_DATE, REMINDER_TIME, REM_FREQUENCY, REM_OPTION FROM usertasks WHERE username = '"
            + text
            + "' ORDER BY REMINDER_DATE DESC"
        )
        tasks_dt_listbox = cur.fetchall()
        c.close()

        events_treeview.tag_configure(
            "oddrow", background="white", font=("Source Code Pro", 12)
        )
        events_treeview.tag_configure(
            "evenrow", background="lightblue", font=("Source Code Pro", 12)
        )
        c = 0
        for i in tasks_dt_listbox:
            if c % 2 == 0:
                events_treeview.insert(
                    parent="", index="end", iid=c, values=i, tags=("evenrow",)
                )
            else:
                events_treeview.insert(
                    parent="", index="end", iid=c, values=i, tags=("oddrow",)
                )
            c += 1

        listbox_scrollbar_frame.place(x=395, y=325)

        # FUNCTION OF BACK BUTTON INSIDE EDIT TASK #
        def back_vt_fn():
            # TO NORMALISE THE FUNCTIONS THAT WERE DISABLED EARLIER
            add_task_btn.config(state="normal")
            edit_task_btn.config(state="normal")
            delete_task_btn.config(state="normal")
            view_task_btn.config(state="normal")
            back_btn.config(state="normal")
            # TO MAKE THE VIEW TASKS WIDGETS DISAPPEAR
            listbox_scrollbar_frame.destroy()
            events_label.destroy()
            back_vt_btn.destroy()

        # BACK BUTTON IN VIEW TASKS
        back_vt_btn = tk.Button(
            n_win,
            text="  BACK  ",
            font=("Fugaz One", 18),
            bg="black",
            fg="white",
            command=back_vt_fn,
        )
        back_vt_btn.place(x=730, y=725)

    # SETTING UP ADD TASK, EDIT TASK, DELETE TASK, VIEW TASKS WIDGETS, BUTTONS, IMAGES, LABELS, ETC.
    add_task_img = tk.PhotoImage(
        file="IMAGES_SUBMISSION\\add_task.png"
    )
    add_task_btn = tk.Button(n_win, image=add_task_img, command=add_task)
    add_task_label = tk.Label(n_win, text="ADD TASK")

    edit_task_img = tk.PhotoImage(
        file="IMAGES_SUBMISSION\\edit_task.png"
    )
    edit_task_btn = tk.Button(n_win, image=edit_task_img, command=edit_task)
    edit_task_label = tk.Label(n_win, text="EDIT TASK")

    delete_task_img = tk.PhotoImage(
        file="IMAGES_SUBMISSION\\delete_task.png"
    )
    delete_task_btn = tk.Button(n_win, image=delete_task_img, command=delete_task)
    delete_task_label = tk.Label(n_win, text="DELETE TASK")

    view_img = tk.PhotoImage(
        file="IMAGES_SUBMISSION\\view_task.png"
    )
    view_task_btn = tk.Button(n_win, image=view_img, command=view_task)
    view_task_label = tk.Label(n_win, text="VIEW TASKS")

    back_img = tk.PhotoImage(
        file="IMAGES_SUBMISSION\\back.png"
    )
    back_btn = tk.Button(n_win, image=back_img, command=n_win.destroy)

    # PLACING ALL WIDGETS IN THE NEW WINDOW
    back_btn.place(x=0, y=0)

    add_task_btn.place(x=483, y=100)
    add_task_label.place(x=488, y=180)

    edit_task_btn.place(x=653, y=100)
    edit_task_label.place(x=658, y=180)

    delete_task_btn.place(x=823, y=100)
    delete_task_label.place(x=820, y=180)

    view_task_btn.place(x=983, y=100)
    view_task_label.place(x=983, y=180)

    n_win.mainloop()  # TO RUN THE MAIN WINDOW TILL BACK BUTTON OR CROSS


while True:
    # STARTS WITH THE HOMEPAGE
    homepage()
    # IF GLOBAL VARIABLE IS TRUE, CALLS NEW WINDOW FUNCTION
    if success == True:
        new_window(user)
    # IF GLOBAL VARIABLE IS FALSE, CALLS NEW WINDOW FUNCTION, BREAKS THE LOOP AND COMES BACK RO HOMEPAGE
    else:
        break
