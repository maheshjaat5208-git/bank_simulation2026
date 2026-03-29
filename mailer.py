import gmail

#credentials
email=""  #mention your gmail id
app_pass="" #mention your password

def send_openacn_email(uemail,uacn,upass,uname):
    con=gmail.GMail(email,app_pass) 
    text_msg=f'''Welcome {uname},
    You have succesfully opened your account with our bank ABC
    Here is your credentials
    ACN  = {uacn}
    Pass = {upass}

    kindly Change your password on 1st login

    Thanks
    ABC Bank
    Kosikalan,Mathura,UP,India
    '''
    msg=gmail.Message(to=uemail,subject='Account Opened',text=text_msg)
    con.send(msg)


def send_otp_forgot(uemail,uname,otp):
    con=gmail.GMail(email,app_pass) 
    text_msg=f'''Hello {uname},
    Here is your otp to recover password
    OTP ={otp}
    kindly do not share otp to others


    Thanks
    ABC Bank
    Kosikalan,Mathura,UP,India
    '''
    msg=gmail.Message(to=uemail,subject='Password Recovery',text=text_msg)
    con.send(msg)


def send_otp_close(uemail,uname,otp):
    con=gmail.GMail(email,app_pass) 
    text_msg=f'''Hello {uname},
    Here is your otp to close your account
    OTP ={otp}
    kindly do not share otp to others


    Thanks
    ABC Bank
    Kosikalan,Mathura,UP,India
    '''
    msg=gmail.Message(to=uemail,subject='Account Closure',text=text_msg)
    con.send(msg)