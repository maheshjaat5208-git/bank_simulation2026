import random
from tkinter import Tk,Label,Frame ,Entry ,Button,simpledialog ,messagebox     #import tk class
from tkinter.ttk import Combobox    #import combobox from ttk module
import time              #import time module

import  dbhandler,generator,sqlite3,mailer
from PIL import Image,ImageTk

dbhandler.create_table()

def update_time():      #create a function
    lbl_date.configure(text=time.strftime("📅%A,%d-%b-%Y ⏰%r"))   #update text for date module
    lbl_date.after(1000,update_time)        #call method on lbl

def forgot_screen():    #function create for forgot frame
    def main_click():   #nested function created
        frm.destroy()   # destory current frame
        main_screen()   #call this function

    def otp():
        uemail=e_email.get()
        conobj=sqlite3.connect(database='bank.sqlite3')
        curobj=conobj.cursor()
        query='select acn,name,pass from accounts where email=?'
        curobj.execute(query,(uemail,))
        tup=curobj.fetchone()
        conobj.close()
        if tup==None:
            messagebox.showerror('forgot','Email does not exists')
        else:
            genotp=random.randint(1000,9999)
            mailer.send_otp_forgot(uemail,tup[1],genotp)
            messagebox.showinfo('Forgot password','we have sent otp to your email')
            uotp=simpledialog.askinteger("","Enter OTP")
            if genotp==uotp:
                messagebox.showinfo('password',tup[2])
                
                e_email.delete(0,'end')
                e_email.focus()
            else:
                messagebox.showerror('Forgot password','Invalid OTP')


                                 
                                 
    
    frm=Frame(root,highlightbackground='black',highlightthickness=2)     #object create for frame
    frm.configure(bg='pink')    #for frame bg
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.75)     #position of frame

    back_btn=Button(frm,text="back",font=('arial',20,'bold'),
                     bd=5,bg='powder blue',activebackground='purple',activeforeground='white',command=main_click)   #create a back button
    
    back_btn.place(relx=0,rely=0)   #place the back button on frm

    lbl_email=Label(frm,text="Email",font=('arial',20,'bold'),bg='pink')  #create label for accn
    lbl_email.place(relx=.3,rely=.2)  #position for acc on frame

    e_email=Entry(frm,font=('arial',20,'bold'),bd=5)  #entry field for emmail
    e_email.place(relx=.4,rely=.2)    #position for email field
    e_email.focus()   #method for focus of cursor on plae we want

    otp_btn=Button(frm,text="send otp",font=('arial',20,'bold'),
                     bd=5,bg='powder blue',activebackground='purple',
                     activeforeground='white',command=otp)   #create a back button
    otp_btn.place(relx=.5,rely=.3)

def admin_screen():     #create a function for admin 

    def logout_click():     #create a function for log out
        frm.destroy()       #destroy current frame
        main_screen()       #call this module


    def close_click():       #create close function
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)     #object create for iframe
        ifrm.configure(bg='white')    #for iframe bg
        ifrm.place(relx=.1,rely=.23,relwidth=.8,relheight=.6)     #position of iframe
        lbl_title=Label(ifrm,text="This is close account section",font=('arial',20,'bold',),
                        bg='white',fg='purple')    #create label for close
        lbl_title.pack()        #put label on top centred

        uacn=simpledialog.askinteger("","Enter ACN")
        
        conobj=sqlite3.connect(database='bank.sqlite3')
        curobj=conobj.cursor()
        query='select email,name from accounts where acn=?'
        curobj.execute(query,(uacn,))
        tup=curobj.fetchone()
        conobj.close()
        if tup==None:
            messagebox.showerror('View Account','ACN does not exist')
        else:
            genotp=random.randint(1111,9999)
            mailer.send_otp_close(tup[0],tup[1],genotp)
            messagebox.showinfo('Close Account','we have sent otp to your email')
            uotp=simpledialog.askinteger("","Enter OTP")
            if genotp==uotp:
                  conobj=sqlite3.connect(database='bank.sqlite3')
                  curobj=conobj.cursor()
                  query='delete from accounts where acn=?'
                  curobj.execute(query,(uacn,))
                  conobj.commit()
                  conobj.close()
                  messagebox.showinfo('Account closure','Account Closed')
            else:
                messagebox.showerror('Account closure','Invalid OTP')



    def view_click():       #create view function
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)     #object create for iframe
        ifrm.configure(bg='white')    #for iframe bg
        ifrm.place(relx=.1,rely=.23,relwidth=.8,relheight=.6)     #position of iframe
        lbl_title=Label(ifrm,text="This is view account section",font=('arial',20,'bold',),
                        bg='white',fg='purple')    #create label for view 
        lbl_title.pack()        #put label on top centred

        uacn=simpledialog.askinteger("","Enter ACN")

        conobj=sqlite3.connect(database='bank.sqlite3')
        curobj=conobj.cursor()
        query='select acn,name,adhar,opendate,bal,mob,email from accounts where acn=?'
        curobj.execute(query,(uacn,))
        tup=curobj.fetchone()
        conobj.close()
        if tup==None:
            messagebox.showerror('View Account','ACN does not exist')
        else:
            messagebox.showinfo('View Account',f'''\n
                                ACN={tup[0]}\n
                                Name={tup[1]}\n
                                Adhar={tup[2]}\n
                                Opendate={tup[3]}\n
                                Bal={tup[4]}\n
                                Mob={tup[5]}\n
                                Email={tup[6]}
                                               ''')




    def open_click():  #create pen function
        def create():       #create an create function
            uname=e_name.get()
            uemail=e_email.get()
            umob=e_mob.get()
            uadhar=e_adhar.get()
            ubal=0
            uopen=time.strftime("%A,%d-%b-%Y %r")

            upass=generator.generate_pass()

            conobj=sqlite3.connect(database="bank.sqlite3")
            curobj=conobj.cursor()
            query="insert into accounts values(null,?,?,?,?,?,?,?)"
            curobj.execute(query,(uname,upass,uemail,umob,uadhar,ubal,uopen))
            conobj.commit()
            conobj.close()

            
            conobj=sqlite3.connect(database="bank.sqlite3")
            curobj=conobj.cursor()
            query="select max(acn) from accounts"
            curobj.execute(query)
            uacn=curobj.fetchone()[0]
            
            conobj.close()

            mailer.send_openacn_email(uemail,uacn,upass,uname)

            messagebox.showinfo('Account','Account Opened and credentials are mailed to customer email')

            e_name.delete(0,'end')
            e_email.delete(0,'end')
            e_mob.delete(0,'end')
            e_adhar.delete(0,'end')

            e_name.focus()



        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)     #object create for iframe
        ifrm.configure(bg='white')    #for iframe bg
        lbl_title=Label(ifrm,text="This is open  account section",font=('arial',20,'bold',),
                        bg='white',fg='purple')    #create label for open
        lbl_title.pack()        #put label on top centred

        ifrm.place(relx=.1,rely=.23,relwidth=.8,relheight=.6)     #position of iframe


        lbl_name=Label(ifrm,text="Name",font=('arial',20,'bold'),bg='white')  #create label for name
        lbl_name.place(relx=.05,rely=.1)  #position for name on frame

        e_name=Entry(ifrm,font=('arial',20,'bold'),bd=5)  #entry field for name
        e_name.place(relx=.15,rely=.1)    #position for entry field
        e_name.focus()   #method for focus of cursor on plae we want

        lbl_email=Label(ifrm,text="Email",font=('arial',20,'bold'),bg='white')  #create label for email
        lbl_email.place(relx=.05,rely=.3)  #position for email on frame

        e_email=Entry(ifrm,font=('arial',20,'bold'),bd=5)  #entry field for email
        e_email.place(relx=.15,rely=.3)    #position for entry field

        lbl_mob=Label(ifrm,text="Mob",font=('arial',20,'bold'),bg='white')  #create label for mob
        lbl_mob.place(relx=.5,rely=.1)  #position for mob on frame

        e_mob=Entry(ifrm,font=('arial',20,'bold'),bd=5)  #entry field for mob
        e_mob.place(relx=.59,rely=.1)    #position for entry field

        lbl_adhar=Label(ifrm,text="Adhar",font=('arial',20,'bold'),bg='white')  #create label for adhar
        lbl_adhar.place(relx=.5,rely=.3)  #position for adhar on frame

        e_adhar=Entry(ifrm,font=('arial',20,'bold'),bd=5)  #entry field for adhar
        e_adhar.place(relx=.59,rely=.3)    #position for entry field


        create_btn=Button(ifrm,text="create ",font=('arial',20,'bold'),
                     bd=5,bg='powder blue',activebackground='purple',
                     activeforeground='white',command=create)     #create a logout button
        create_btn.place(relx=.4,rely=.6)   #place the logout button on frm




    frm=Frame(root,highlightbackground='black',highlightthickness=2)     #object create for frame
    frm.configure(bg='pink')    #for frame bg
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.75)     #position of frame

    lbl_wel=Label(frm,text="Welcome Admin",font=('arial',20,'bold'),bg='pink')  #create label for welcome
    lbl_wel.place(relx=0,rely=0)  #position for welcome on frame

    logout_btn=Button(frm,text="logout",font=('arial',20,'bold'),
                     bd=5,bg='powder blue',activebackground='purple',
                     activeforeground='white',command=logout_click)   #create a logout button
    logout_btn.place(relx=.9,rely=0)   #place the logout button on frm

    open_btn=Button(frm,text="open account",font=('arial',20,'bold'),
                     bd=5,activebackground='purple',
                     activeforeground='white',bg='green',fg='white',command=open_click)   #create a open button
    
    open_btn.place(relx=.2,rely=.1)   #place the open button on frm

    view_btn=Button(frm,text="view account",font=('arial',20,'bold'),
                     bd=5,activebackground='purple',
                     activeforeground='white',bg='blue',fg='white',command=view_click)   #create a view button
    view_btn.place(relx=.4,rely=.1)   #place the view button on frm

    close_btn=Button(frm,text="close account",font=('arial',20,'bold'),
                     bd=5,activebackground='purple',
                     activeforeground='white',bg='red',fg='white',command=close_click)   #create a close button
    close_btn.place(relx=.6,rely=.1)   #place the close button on frm


def customer_screen(cname,acn):
    def logout_click():     #create a function for log out
        frm.destroy()       #destroy current frame
        main_screen()       #call this module

    def details_click():



        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)     #object create for iframe
        ifrm.configure(bg='white')    #for iframe bg
        lbl_title=Label(ifrm,text="This is details section",font=('arial',20,'bold',),
                        bg='white',fg='purple')    #create label for details
        lbl_title.pack()        #put label on top centred

        ifrm.place(relx=.2,rely=.23,relwidth=.7,relheight=.6)     #position of iframe
        conobj=sqlite3.connect(database='bank.sqlite3')
        curobj=conobj.cursor()
        query='select * from accounts where acn=?'
        curobj.execute(query,(acn,))
        tup=curobj.fetchone()
        conobj.close()

        info=f'''Account No = {tup[0]}

Account open date = {tup[7]}

Account Bal = {tup[6]}

Account Adhar = {tup[5]}

Account Email = {tup[3]}

Account Mob = {tup[4]}

'''
        lbl_info=Label(ifrm,text=info,bg='white',font=('verdana',15,'bold'),)
        lbl_info.place(relx=.2,rely=.2)

    def edit_click():
        

        def update():
            uname=e_name.get()
            upass=e_pass.get()
            uemail=e_email.get()
            umob=e_mob.get()

        
            conobj=sqlite3.connect(database='bank.sqlite3')
            curobj=conobj.cursor()
            query='update accounts set name=?,pass=?,email=?,mob=? where acn=?'
            curobj.execute(query,(uname,upass,uemail,umob,acn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo('Edit','Record Updated')

            ifrm.destroy()

        
        

        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)     #object create for iframe
        ifrm.configure(bg='white')    #for iframe bg
        lbl_title=Label(ifrm,text="This is edit details section",font=('arial',20,'bold',),
                        bg='white',fg='purple')    #create label for details
        lbl_title.pack()        #put label on top centred

        ifrm.place(relx=.2,rely=.23,relwidth=.7,relheight=.6)     #position of iframe

        
        lbl_name=Label(ifrm,text="Name",font=('arial',20,'bold'),bg='white')  #create label for name
        lbl_name.place(relx=.05,rely=.1)  #position for name on frame

        e_name=Entry(ifrm,font=('arial',20,'bold'),bd=5)  #entry field for name
        e_name.place(relx=.15,rely=.1)    #position for entry field
        e_name.focus()   #method for focus of cursor on plae we want

        lbl_email=Label(ifrm,text="Email",font=('arial',20,'bold'),bg='white')  #create label for email
        lbl_email.place(relx=.05,rely=.3)  #position for email on frame

        e_email=Entry(ifrm,font=('arial',20,'bold'),bd=5)  #entry field for email
        e_email.place(relx=.15,rely=.3)    #position for entry field

        lbl_mob=Label(ifrm,text="Mob",font=('arial',20,'bold'),bg='white')  #create label for mob
        lbl_mob.place(relx=.5,rely=.1)  #position for mob on frame

        e_mob=Entry(ifrm,font=('arial',20,'bold'),bd=5)  #entry field for mob
        e_mob.place(relx=.59,rely=.1)    #position for entry field

        lbl_pass=Label(ifrm,text="Pass",font=('arial',20,'bold'),bg='white')  #create label for pass
        lbl_pass.place(relx=.5,rely=.3)  #position for pass on frame

        e_pass=Entry(ifrm,font=('arial',20,'bold'),bd=5)  #entry field for pass
        e_pass.place(relx=.59,rely=.3)    #position for entry field


        update_btn=Button(ifrm,text="update ",font=('arial',20,'bold'),
                     bd=5,bg='powder blue',activebackground='purple',
                     activeforeground='white',command=update)     #create a update  button
        update_btn.place(relx=.4,rely=.6)   #place the update button on frm

        conobj=sqlite3.connect(database='bank.sqlite3')
        curobj=conobj.cursor()
        query='select name,pass,email,mob from accounts where acn=?'
        curobj.execute(query,(acn,))
        tup=curobj.fetchone()
        conobj.close()

        e_name.insert(0,tup[0])
        e_pass.insert(0,tup[1])
        e_email.insert(0,tup[2])
        e_mob.insert(0,tup[3])

    def deposit_click():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)     #object create for iframe
        ifrm.configure(bg='white')    #for iframe bg
        lbl_title=Label(ifrm,text="This is deposit section",font=('arial',20,'bold',),
                        bg='white',fg='purple')    #create label for details
        lbl_title.pack()        #put label on top centred

        ifrm.place(relx=.2,rely=.23,relwidth=.7,relheight=.6)     #position of iframe

        amt=simpledialog.askfloat('','Amount')
        conobj=sqlite3.connect(database='bank.sqlite3')
        curobj=conobj.cursor()
        query='update accounts set bal=bal+? where acn=?'
        curobj.execute(query,(amt,acn))
        conobj.commit()
        conobj.close()
        messagebox.showinfo('Deposit',f'{amt} deposited')

    def withdraw_click():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)     #object create for iframe
        ifrm.configure(bg='white')    #for iframe bg
        lbl_title=Label(ifrm,text="This is withdraw section",font=('arial',20,'bold',),
                        bg='white',fg='purple')    #create label for details
        lbl_title.pack()        #put label on top centred

        ifrm.place(relx=.2,rely=.23,relwidth=.7,relheight=.6)     #position of iframe

        amt=simpledialog.askfloat('','Amount')
        conobj=sqlite3.connect(database='bank.sqlite3')
        curobj=conobj.cursor()
        query='select bal from accounts  where acn=?'
        curobj.execute(query,(acn,))
        bal=curobj.fetchone()[0]
        conobj.close()
        if bal>=amt:
            conobj=sqlite3.connect(database='bank.sqlite3')
            curobj=conobj.cursor()
            query='update accounts set bal=bal-? where acn=?'
            curobj.execute(query,(amt,acn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo('Withdraw',f'{amt} withdrawn')
        else:
             messagebox.showerror('Withdraw',f'Insufficient bal {bal}')

    def transfer_click():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)     #object create for iframe
        ifrm.configure(bg='white')    #for iframe bg
        lbl_title=Label(ifrm,text="This is transfer section",font=('arial',20,'bold',),
                        bg='white',fg='purple')    #create label for details
        lbl_title.pack()        #put label on top centred

        ifrm.place(relx=.2,rely=.23,relwidth=.7,relheight=.6)     #position of iframe

        
        toacn=simpledialog.askinteger('','To ACN')
        conobj=sqlite3.connect(database='bank.sqlite3')
        curobj=conobj.cursor()
        query='select * from accounts  where acn=?'
        curobj.execute(query,(toacn,))
        tup=curobj.fetchone()
        conobj.close()
        if tup!=None:
            amt=simpledialog.askfloat('','Amount')
            conobj=sqlite3.connect(database='bank.sqlite3')
            curobj=conobj.cursor()
            query='select bal from accounts  where acn=?'
            curobj.execute(query, (acn,))
            bal=curobj.fetchone()[0]
            conobj.close()
            if bal>=amt:
                conobj=sqlite3.connect(database='bank.sqlite3')
                curobj=conobj.cursor()
                query1='update accounts set bal=bal-? where acn=?'
                query2='update accounts set bal=bal+? where acn=?'

                curobj.execute(query1,(amt,acn))
                curobj.execute(query2,(amt,toacn))

                conobj.commit()
                conobj.close()
                messagebox.showinfo('Transfer',f'{amt} transferred to {toacn} ACN')
            else:
                messagebox.showerror('Withdraw',f'Insufficient bal {bal}')
       
        else:
            messagebox.showerror('Transfer',f'To ACN does not exist')
       

    frm=Frame(root,highlightbackground='black',highlightthickness=2)     #object create for frame
    frm.configure(bg='pink')    #for frame bg
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.75)     #position of frame

    lbl_wel=Label(frm,text=f"Welcome,{cname}",font=('arial',20,'bold'),bg='pink')  #create label for welcome
    lbl_wel.place(relx=0,rely=0)  #position for welcome on frame

    logout_btn=Button(frm,text="logout",font=('arial',20,'bold'),
                     bd=5,bg='powder blue',activebackground='purple',
                     activeforeground='white',command=logout_click)   #create a logout button
    logout_btn.place(relx=.9,rely=0)   #place the logout button on frm

    details_btn=Button(frm,text="view details",font=('arial',20,'bold'),
                     bd=5,activebackground='purple',width=15,
                     activeforeground='white',bg='blue',fg='white',command=details_click)   #create a details button
    
    details_btn.place(relx=0,rely=.1)   #place the details button on frm

    edit_btn=Button(frm,text="edit details",font=('arial',20,'bold'),
                     bd=5,activebackground='purple',width=15,
                     activeforeground='white',bg='powder blue',command=edit_click)   #create a edit button
    
    edit_btn.place(relx=0,rely=.25)   #place the edit button on frm

    deposit_btn=Button(frm,text="deposit",font=('arial',20,'bold'),
                     bd=5,activebackground='purple',width=15,
                     activeforeground='white',bg='green',fg='white',command=deposit_click)   #create a deposit button
    
    deposit_btn.place(relx=0,rely=.4)   #place the deposit button on frm

    withdraw_btn=Button(frm,text="withdraw",font=('arial',20,'bold'),
                     bd=5,activebackground='purple',width=15,
                     activeforeground='white',bg='red',fg='white',command=withdraw_click)   #create a withdraw button
    
    withdraw_btn.place(relx=0,rely=.55)   #place the withdraw button on frm

    transfer_btn=Button(frm,text="transfer",font=('arial',20,'bold'),
                     bd=5,activebackground='purple',width=15,
                     activeforeground='white',bg='red',fg='white',command=transfer_click)   #create a transfer button
    
    transfer_btn.place(relx=0,rely=.7)   #place the transfer button on frm




def main_screen():  #functon create for frame
    def forgot_click():         #create nested function
        frm.destroy()       #destroy current frame
        forgot_screen()     #call this function

    def login_click():      #function create for login module
        user=combo_user.get()
        uacn=e_acn.get()
        upass=e_pass.get()

        if user=="Admin" and uacn=='0' and upass=='Admin':
            frm.destroy()           #destroy current frame
            admin_screen()      #call the function
        elif user=='Customer':
            conobj=sqlite3.connect(database='bank.sqlite3')
            curobj=conobj.cursor()
            query='select * from accounts where acn=? and pass=?'
            curobj.execute(query,(uacn,upass))
            tup=curobj.fetchone()
            conobj.close()
            if tup==None:
             messagebox.showerror('Login','Invalid Credentials')
            else:
                frm.destroy()
                customer_screen(tup[1],tup[0])
        else:
            messagebox.showerror('Login','Invalid User')

    frm=Frame(root,highlightbackground='black',highlightthickness=2)     #object create for frame
    frm.configure(bg='pink')    #for frame bg
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.75)     #position of frame

    lbl_acn=Label(frm,text="ACN",font=('arial',20,'bold'),bg='pink')  #create label for accn
    lbl_acn.place(relx=.3,rely=.1)  #position for acc on frame

    e_acn=Entry(frm,font=('arial',20,'bold'),bd=5)  #entry field for acn
    e_acn.place(relx=.4,rely=.1)    #position for entry field
    e_acn.focus()   #method for focus of cursor on plae we want


    lbl_pass=Label(frm,text="PASS",font=('arial',20,'bold'),bg='pink')  #create label for pass
    lbl_pass.place(relx=.3,rely=.2)  #position for pass on frame

    e_pass=Entry(frm,font=('arial',20,'bold'),bd=5,show='*')   #entry field for pass
    e_pass.place(relx=.4,rely=.2)                       #position for entry field

    lbl_user=Label(frm,text="USER",font=('arial',20,'bold'),bg='pink')  #create label for user
    lbl_user.place(relx=.3,rely=.3)  #position for user on frame

    combo_user=Combobox(frm,values=['---select---','Admin','Customer'],font=('arial',20,'bold')) #create combobox with select options
    combo_user.current(0)       #for showing default entity
    combo_user.place(relx=.4,rely=.3)   #place the entity 

    login_btn=Button(frm,text="login",font=('arial',20,'bold'),
                     bd=5,bg='powder blue',activebackground='purple',
                     activeforeground='white',command=login_click)   #create a login button
    login_btn.place(relx=.42,rely=.4)   #place the login button on frm

    reset_btn=Button(frm,text="reset",font=('arial',20,'bold'),
                     bd=5,bg='powder blue',activebackground='purple',activeforeground='white')   #create a reset button
    reset_btn.place(relx=.52,rely=.4)   #place the reset button on frm

    forgot_btn=Button(frm,text="forgot password",font=('arial',20,'bold'),width=18,
                     bd=5,bg='powder blue',activebackground='purple',activeforeground='white',command=forgot_click)   #create a forgot pass button
    forgot_btn.place(relx=.4,rely=.52)   #place the login button on frm

root=Tk()                #create root window
root.state("zoomed")    #make window fullscreen
root.config(bg="powder blue")       #set bg color of window
root.resizable(width=False,height=False)   #resize disable 

lbl_title=Label(root,text="Banking Simulation",font=('arial',50,'bold','underline'),bg='powder blue')    #create label for project
lbl_title.pack()        #put label on top centred

lbl_date=Label(root,text=time.strftime("🗓️%A,%d-%b-%Y ⏰%r"),fg='blue',font=('arial',15,'bold',),bg='powder blue')          #show date of system
lbl_date.pack()         #place date on top centered

img=Image.open('logo.jpeg').resize((200,125))
tkimg=ImageTk.PhotoImage(img,master=root)

lbl_logo_left=Label(root,image=tkimg)
lbl_logo_left.place(relx=0,rely=0)

lbl_logo_right=Label(root,image=tkimg)
lbl_logo_right.place(relx=0.867,rely=0)


lbl_footer=Label(root,text="Developed by \n Mahesh",fg='blue',font=('arial',15,'bold',),bg='powder blue')          #create label for footer text
lbl_footer.pack(side='bottom',pady=15)  #place footer on down centered with padding

update_time()   #call method of date
main_screen()
root.mainloop()         #make the window visible
