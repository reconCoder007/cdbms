from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry

crimes = ['Murder', 'Chain Snatching', 'other']
data = []


import mysql.connector as ms
myconn = ms.connect(host="localhost", user="root", password="admin" )
mycursor = myconn.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS cdbms")
myconn.close()


myconn=ms.connect(host="localhost", user="root", password="admin", database="cdbms")
mycursor=myconn.cursor()
mycursor.execute("""CREATE TABLE IF NOT EXISTS criminals
                 (crno INT PRIMARY KEY, name VARCHAR(200), age INT, gender VARCHAR(200), crime VARCHAR(200)
                  , lastlocation VARCHAR(200) ,aboutcrime VARCHAR(200),dateofarrest date, punishment VARCHAR(200))""")
mycursor.execute("CREATE TABLE IF NOT EXISTS crimes(crimes VARCHAR(200))")
mycursor.execute("CREATE TABLE IF NOT EXISTS logincredintials(username VARCHAR(200),password VARCHAR(200))")
mycursor.execute("CREATE TABLE IF NOT EXISTS alteringcredintials(username VARCHAR(200), password VARCHAR(200))")
mycursor.execute("CREATE TABLE IF NOT EXISTS ownershipinfo(ownername VARCHAR(200), details VARCHAR(200))")


def login():
    u = username.get()
    p = password.get()
    mycursor.execute("INSERT INTO logincredintials VALUES('admin','admin123')")
    if u == 'admin' and p == 'admin123':
        messagebox.showinfo('Login Status', 'Access Granted')
        root1.destroy()
        root2 = Tk()
        root2.geometry('1200x1000')
        root2.attributes('-fullscreen', True)
        def quit_app():
            root2.destroy()
            myconn.close()
        Button(root2, text='QUIT', font=('impact'), command=quit_app, relief='raised', bd=4, fg='red').place(x=1840, y=0)
        Label(root2, text='Criminal Records', font=('impact', 26, 'underline'), relief='sunken', bd=4).pack()

        def load_data():
            mycursor.execute("SELECT * FROM criminals")
            rows = mycursor.fetchall()
            for row in rows:
                table.insert("", "end", values=row)


        frame = Frame(root2)
        frame.pack(padx=10, pady=10, fill=BOTH, expand=True)

        table = ttk.Treeview(frame, columns=("Criminal No.","Name", "Age", "Gender", "Crime", "Info."))
        table.heading("#0", text="")
        table.heading("Criminal No.", text="Criminal No.")
        table.heading("Name", text="Name")
        table.heading("Age", text="Age")
        table.heading("Gender", text="Gender")
        table.heading("Crime", text="Crime")
        

        table.column('#0',width=1)
        table.column("Criminal No.", width=300, anchor=W)
        table.column("Name", width=500, anchor=W)
        table.column("Age", width=350, anchor=W)
        table.column("Gender", width=350, anchor=W)
        table.column("Crime", width=475, anchor=W)
        

        vsb = Scrollbar(frame, orient="vertical", command=table.yview)
        table.configure(yscrollcommand=vsb.set)

        table.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        style = ttk.Style()
        style.theme_use("default")   # optional
        style.configure("Treeview.Heading", font=("Calibri", 12, "bold"), background="#000000")

        style.configure("Treeview.Heading", foreground="white")


        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        load_data()

        def add_criminal():
            mywin2 = Toplevel(root2)
            mywin2.geometry('400x500+40+20')
            mywin2.title('Add Criminal')
            Label(mywin2, text='New Criminal', font=('impact'), relief='sunken', bd=4).pack()
            Label(mywin2, text='CRIMINAL NUMBER').place(x=25, y=50)
            name = StringVar()
            age = IntVar()
            age.set('')
            crime = StringVar()
            crno = IntVar()
            mycursor.execute("SELECT MAX(crno) FROM criminals")
            result = mycursor.fetchone()
            if result and result[0]:
                next_crno = result[0] + 1
            else:
                next_crno = 1   # first record
            crno.set(next_crno)
            f1 = Entry(mywin2, textvariable=crno,state='readonly')
            f1.place(x=150, y=50)
            
            

          
            Label(mywin2, text='NAME').place(x=25, y=90)
            f2 = Entry(mywin2, textvariable=name)
            f2.place(x=150, y=90)
            f2.focus_set()
            Label(mywin2, text='AGE').place(x=25, y=130)
            f3 = Entry(mywin2, textvariable=age)
            f3.place(x=150, y=130)
            
            
            Label(mywin2, text='CRIME COMMITTED').place(x=25, y=210)
            f4 = OptionMenu(mywin2, crime, *crimes)
            f4.place(x=150, y=205)
            crime.set('Murder')
            othercrime = StringVar()

            def addlarg(*args):
                if crime.get() == 'other':
                    mywin3 = Toplevel(mywin2)
                    mywin3.geometry('250x250+40+20')
                    mywin3.title('Other Crime')
                    Label(mywin3, text='Other Crime', relief='sunken', bd=4, font=('impact', 16)).pack(padx=10)
                    Label(mywin3, text='Enter Crime', font=('impact')).pack(pady=10, padx=10)
                    v = Entry(mywin3, textvariable=othercrime, font=('calibri', 12), highlightthickness=2, highlightbackground='gray', highlightcolor='green')
                    v.pack(padx=10)
                    v.focus_set()
                    mywin3.resizable(False, False)

                    def addcrim_e():
                        u = othercrime.get()
                        crime.set(u)
                        if u not in crimes:
                            crimes.append(u)
                        mycursor.execute("INSERT INTO crimes VALUES(%s)",(u,))
                        mywin3.destroy()

                    Button(mywin3, text='Add Crime', font=('impact'), command=addcrim_e, relief='raised', bd=4, fg='black').pack(padx=10, pady=10)

            crime.trace('w', addlarg)

            gender = StringVar()
            gender.set('male')

            Label(mywin2, text='GENDER').place(x=25, y=170)
            v1 = Radiobutton(mywin2, text='Male', value='male', variable=gender)
            v1.place(x=150, y=170)
            v2 = Radiobutton(mywin2, text='Female', value='female', variable=gender)
            v2.place(x=210, y=170)
            v3 = Radiobutton(mywin2, text='Other', value='other', variable=gender)
            v3.place(x=280, y=170)

            Label(mywin2, text='CRIME DESCRIPTION').place(x=25, y=250)
            aboutcrime = StringVar()
            v4 = Entry(mywin2, textvariable=aboutcrime)
            v4.place(x=150, y=250)
            
            Label(mywin2, text='LAST LOCATION').place(x=25, y=290)
            location = StringVar()
            v5 = Entry(mywin2, textvariable=location)
            v5.place(x=150, y=290)
            
            Label(mywin2, text='DATE OF ARREST').place(x=25, y=330)
            date=StringVar()
            v6 = DateEntry(mywin2,textvariable=date,date_pattern='yyyy/mm/dd')
            v6.place(x=150,y=330)

            Label(mywin2, text='SENTENCE').place(x=25, y=370)
            sentence=StringVar()
            v7 = Entry(mywin2, textvariable=sentence)
            v7.place(x=150,y=370)
            
            

            

            def addd():
                try:
                    no=age.get()
                    ag=crno.get()
                    if ag<=0:
                        messagebox.showinfo('Invalid Argument','Please enter valid argument.')
                        mywin2.destroy()
                    if no<=0:
                        messagebox.showinfo('Invalid Argument','Please enter valid argument.')
                        mywin2.destroy()
                    if no<18 and no>0:
                        messagebox.showinfo('Minor','Minors cannot be added.')
                        mywin2.destroy()
                    if ag>0 and no>=18:
                        t = crno.get(),name.get(), age.get(), gender.get(), crime.get(),location.get(),aboutcrime.get(),date.get(),sentence.get()
                        data.append(t)
                        table.insert("", "end", values=t)
                        mycursor.execute("INSERT INTO criminals VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(crno.get(),name.get(), age.get(), gender.get(), crime.get(),location.get(),aboutcrime.get(),date.get(),sentence.get()))
                        myconn.commit()
                        mywin2.destroy()
                except Exception as e:
                    print(e)
                    messagebox.showinfo('Invalid Argument','Please enter valid argument.')
                    mywin2.destroy()
               
            Button(mywin2, text='Add', font=('impact'), command=addd, relief='raised', bd=4, fg='black').place(x=155, y=410)


        def updatecriminalrecord():
            si=table.selection()
            if si:
                itema = table.item(si[0]) # Get the data for the selected row
                ama = itema['values'][0]  # Criminal No.
                bma = itema['values'][1]  # Name
                cma = itema['values'][2]  # Age
                dma = itema['values'][3]  # Gender
                ema = itema['values'][4]  # Crime
                fma = itema['values'][5]  # location
                gma = itema['values'][6]  # aboutcrime
                hma = itema['values'][7]  # date of arrest
                ima = itema['values'][8]  # sentence
                mywin10 = Toplevel(root2)
                mywin10.geometry('400x500+40+20')
                mywin10.title('Update Criminal')
                Label(mywin10, text='Update Criminal', font=('impact'), relief='sunken', bd=4).pack()
                Label(mywin10, text='CRIMINAL NUMBER').place(x=25, y=50)
                name = StringVar()
                name.set(bma)
                age = IntVar()
                age.set(cma)
                crime = StringVar()
                crime.set(ema)
                crno = IntVar()
                crno.set(ama)
                f1 = Entry(mywin10, textvariable=crno, state='readonly')
                f1.place(x=150, y=50)
                f1.focus_set()
                

              
                Label(mywin10, text='NAME').place(x=25, y=90)
                f2 = Entry(mywin10, textvariable=name)
                f2.place(x=150, y=90)
                Label(mywin10, text='AGE').place(x=25, y=130)
                f3 = Entry(mywin10, textvariable=age)
                f3.place(x=150, y=130)
                
                
                Label(mywin10, text='CRIME COMMITTED').place(x=25, y=210)
                f4 = OptionMenu(mywin10, crime, *crimes)
                f4.place(x=150, y=205)
                crime.set('Murder')
                othercrime = StringVar()

                def addlarg(*args):
                    if crime.get() == 'other':
                        mywin30 = Toplevel(mywin10)
                        mywin30.geometry('250x250+40+20')
                        mywin30.title('Other Crime')
                        Label(mywin30, text='Other Crime', relief='sunken', bd=4, font=('impact', 16)).pack(padx=10)
                        Label(mywin30, text='Enter Crime', font=('impact')).pack(pady=10, padx=10)
                        v = Entry(mywin30, textvariable=othercrime, font=('calibri', 12), highlightthickness=2, highlightbackground='gray', highlightcolor='green')
                        v.pack(padx=10)
                        v.focus_set()
                        mywin30.resizable(False, False)

                        def addcrim_e():
                            u = othercrime.get()
                            crime.set(u)
                            if u not in crimes:
                                crimes.append(u)
                            mycursor.execute("INSERT INTO crimes VALUES(%s)",(u,))
                            mywin30.destroy()

                        Button(mywin30, text='Add Crime', font=('impact'), command=addcrim_e, relief='raised', bd=4, fg='black').pack(padx=10, pady=10)

                crime.trace('w', addlarg)

                gender = StringVar()
                gender.set(dma)

                Label(mywin10, text='GENDER').place(x=25, y=170)
                v1 = Radiobutton(mywin10, text='Male', value='male', variable=gender)
                v1.place(x=150, y=170)
                v2 = Radiobutton(mywin10, text='Female', value='female', variable=gender)
                v2.place(x=210, y=170)
                v3 = Radiobutton(mywin10, text='Other', value='other', variable=gender)
                v3.place(x=280, y=170)

                Label(mywin10, text='CRIME DESCRIPTION').place(x=25, y=250)
                aboutcrime = StringVar()
                aboutcrime.set(gma)
                v4 = Entry(mywin10, textvariable=aboutcrime)
                v4.place(x=150, y=250)
                
                Label(mywin10, text='LAST LOCATION').place(x=25, y=290)
                location = StringVar()
                location.set(fma)
                v5 = Entry(mywin10, textvariable=location)
                v5.place(x=150, y=290)
                
                Label(mywin10, text='DATE OF ARREST').place(x=25, y=330)
                date=StringVar()
                
                v6 = DateEntry(mywin10,textvariable=date,date_pattern='yyyy/mm/dd')
                v6.place(x=150,y=330)
                date.set(hma)

                Label(mywin10, text='SENTENCE').place(x=25, y=370)
                sentence=StringVar()
                sentence.set(ima)
                v7 = Entry(mywin10, textvariable=sentence)
                v7.place(x=150, y=370)

                def updatebutton():
                    usernamea=StringVar()
                    passworda=StringVar()
                    mywin8=Toplevel(mywin10)
                    mywin8.title('Security Check')
                    Label(mywin8, text='VERIFICATION', font=('impact', 26)).pack(pady=10)
                    Label(mywin8, text='Username', font=('calibri', 12), highlightthickness=2, highlightbackground='gray', highlightcolor='green').pack(padx=10)
                    m1 = Entry(mywin8, textvariable=usernamea, highlightthickness=4, highlightbackground='gray', highlightcolor='green')
                    m1.pack(padx=10)
                    Label(mywin8, text='Password', font=('calibri', 12), highlightthickness=2, highlightbackground='gray', highlightcolor='green').pack(padx=10)
                    m2 = Entry(mywin8, textvariable=passworda, highlightthickness=4, highlightbackground='gray', highlightcolor='green', show='*')
                    m2.pack(padx=10)
                    m1.focus_set()
                    
                    def verification():
                        if usernamea.get()=='admin***' and passworda.get()=='admin123***':    

                            table.delete(si)
                            mywin8.destroy()
                            t1 = crno.get(),name.get(), age.get(), gender.get(), crime.get(),location.get(),aboutcrime.get(),date.get(),sentence.get()
                            mycursor.execute("UPDATE criminals SET name=%s, age=%s, gender=%s, crime=%s, lastlocation=%s, aboutcrime=%s, dateofarrest=%s, punishment=%s WHERE crno=%s",(name.get(), age.get(), gender.get(), crime.get(),location.get(),aboutcrime.get(),date.get(),sentence.get(),crno.get()))
                            myconn.commit()
    
                            data.append(t1)
                            table.insert("", "end", values=t1)
                            mywin8.destroy()
                            mywin10.destroy()
                            messagebox.showinfo("Success", "Record updated successfully.")

                        else:
                            mywin8.destroy()
                            mywin10.destroy()
                            root2.destroy()
                            messagebox.showinfo('Threat Found','Record Encrypted.')
                    Button(mywin8, text='VERIFY', font=('impact'), relief='raised', bd=4, command=verification).pack(padx=10, pady=20)
                    mywin8.resizable(False, False)
                    print("DEBUG - CRNO =", crno.get())
                    print("DEBUG - Query Data =", (name.get(), age.get(), gender.get(), crime.get(),
                          location.get(), aboutcrime.get(), date.get(), sentence.get(), crno.get()))
                    print("DEBUG - Rows affected:", mycursor.rowcount)


                Button(mywin10, text='Update', font=('impact'), command=updatebutton, relief='raised', bd=4, fg='black').place(x=155, y=410)
            else:
                    messagebox.showinfo('Error','Please Select An Item First.')


        def deleterecord():
            usernamea=StringVar()
            passworda=StringVar()

            selected_item = table.selection()  
            if selected_item:
                mywin7=Toplevel(root2)
                mywin7.title('Security Check')
                Label(mywin7, text='VERIFICATION', font=('impact', 26)).pack(pady=10)
                Label(mywin7, text='Username', font=('calibri', 12), highlightthickness=2, highlightbackground='gray', highlightcolor='green').pack(padx=10)
                m1 = Entry(mywin7, textvariable=usernamea, highlightthickness=4, highlightbackground='gray', highlightcolor='green')
                m1.pack(padx=10)
                Label(mywin7, text='Password', font=('calibri', 12), highlightthickness=2, highlightbackground='gray', highlightcolor='green').pack(padx=10)
                m2 = Entry(mywin7, textvariable=passworda, highlightthickness=4, highlightbackground='gray', highlightcolor='green', show='*')
                m2.pack(padx=10)
                m1.focus_set()
                def verification():
                    if usernamea.get()=='admin***' and passworda.get()=='admin123***':
                        malik=table.item(selected_item)['values'][0]

                        mycursor.execute("DELETE FROM criminals WHERE crno=%s",(table.item(selected_item)['values'][0],))
                        table.delete(selected_item)
                        myconn.commit()
                        mywin7.destroy()
                        messagebox.showinfo('success',f'criminal number {malik} deleted successfully ')
                        
                    else:
                        mywin7.destroy()
                        root2.destroy()
                        mycursor.close()
                        messagebox.showinfo('Threat Found','Record Encrypted.')
                Button(mywin7, text='VERIFY', font=('impact'), relief='raised', bd=4, command=verification).pack(padx=10, pady=20)
                mywin7.resizable(False, False)
            else:
                messagebox.showinfo('Error','Please Select An Item First.')          
                

        def moreinfo():
            
            c = table.selection()
            if c:
                item = table.item(c[0]) # Get the data for the selected row
                am = item['values'][0]  # Criminal No.
                bm = item['values'][1]  # Name
                cm = item['values'][2]  # Age
                dm = item['values'][3]  # Gender
                em = item['values'][4]  # Crime
                fm = item['values'][5]  # location
                gm = item['values'][6]  # aboutcrime
                hm = item['values'][7]  # date of arrest
                im = item['values'][8]  # tsentence
                root4 = Toplevel(root2)
                root4.geometry('1000x280+350+150')
                root4.title('INFORMATION')
                Label(root4,text=bm,font=('impact',25),relief='sunken',bd=6).place(x=10,y=10)
                Label(root4,text='Criminal Number: ',font=('impact',14)).place(x=450,y=10)
                Label(root4,text=am,font=('impact',14),fg='blue').place(x=650,y=10)
                Button(root4,text='Close',font=('impact',10),fg='red',relief='sunken',bd=4,command=root4.destroy).place(x=850,y=40)
                Label(root4,text='Age: ',font=('impact',14)).place(x=450,y=40)
                Label(root4,text=cm,font=('impact',14),fg='blue').place(x=650,y=40)
                Label(root4,text='Gender: ',font=('impact',14)).place(x=450,y=70)
                Label(root4,text=dm,font=('impact',14),fg='blue').place(x=650,y=70)
                Label(root4,text='Crime: ',font=('impact',14)).place(x=10,y=100)
                Label(root4,text=em,font=('impact',14),fg='blue').place(x=110,y=100)
                Label(root4,text='Crime Info.: ',font=('impact',14),fg='black').place(x=10,y=130)
                Label(root4,text=gm,font=('impact',14),fg='blue').place(x=110,y=130)
                Label(root4,text='Last Known Location: ',font=('impact',14)).place(x=10,y=160)
                Label(root4,text=fm,font=('impact',14),fg='blue').place(x=180,y=160)
                Label(root4,text='Date Of Arrest: ',font=('impact',14)).place(x=10,y=190)
                Label(root4,text=hm,font=('impact',14),fg='blue').place(x=130,y=190)
                Label(root4,text='Sentence: ',font=('impact',14)).place(x=10,y=220)
                Label(root4,text=im,font=('impact',14),fg='blue').place(x=100,y=220)

                

            else:
                messagebox.showinfo('Error','Please Select An Item First.')

        def ownership():
            newwin = Toplevel(root2)
            newwin.geometry('400x200')  
            newwin.title('Project Information')
            mycursor.execute("INSERT INTO ownershipinfo VALUES('Siddharth Vishwakarma, Akshat Tiwari, Atharv Singh Kinaria','This project is developed as a part of academic curriculum and submitted to Mr. V.K.Verma.')")
            
            
            Label(newwin, text='Criminal Database Management System', font=('Impact', 15,'underline')).pack(pady=10)
            Label(newwin, text='Submitted to Mr. V.K. Verma', font=('Arial', 12,'bold')).pack(pady=5)
            Label(newwin, text='''Submitted by:
        Siddharth Vishwakarma
        Akshat Tiwari
        Atharv Singh Kinaria''', font=('Arial', 12,'bold')).pack(pady=10)

        Button(root2,text='Update Criminal', font=('impact'), command=updatecriminalrecord, relief='raised', bd=4, fg='blue').place(x=1280, y=0)            
        Button(root2,text='More Info.', font=('impact'), command=moreinfo, relief='raised', bd=4, fg='blue').place(x=350, y=0)
        Button(root2,text='Delete Criminal', font=('impact'), command=deleterecord, relief='raised', bd=4, fg='blue').place(x=10, y=0)
        Button(root2, text='Add Criminal', font=('impact'), command=add_criminal, relief='raised', bd=4, fg='blue').place(x=1480, y=0)
        Button(root2, text='⚠',fg='red',command=ownership,relief='flat',font=('calibri',15)).place(x=1100,y=0)
        
        def search():
            root3 = Toplevel(root2)
            root3.geometry('380x250+40+40')
            root3.title('Search Criminal')

            def search_by_name():
                room1 = Toplevel(root2)
                room1.geometry('400x200+40+40')
                room1.title('Search By Name')

                Label(room1, text='Enter Name:', font=('impact', 12),relief='sunken',bd=4).pack(pady=5)
                name_search = StringVar()
                ma0=Entry(room1, textvariable=name_search, highlightthickness=2, highlightbackground='gray', highlightcolor='green')
                ma0.focus_set()
                ma0.pack(pady=5)

                def perform_search():
                    name = name_search.get().lower()
                    results = [
                        row for row in table.get_children()
                        if name in table.item(row)['values'][1].lower()
                    ]

                    if results:
                        for item in table.get_children():
                            table.selection_remove(item)
                        for result in results:
                            table.selection_add(result)
                        messagebox.showinfo("Search Results", f"{len(results)} record(s) found.")
                    else:
                        messagebox.showinfo("Search Results", "No records found.")

                    room1.destroy()

                Button(room1, text='Search', command=perform_search).pack(pady=10)

            def search_by_crno():
                room2 = Toplevel(root2)
                room2.geometry('400x200+40+40')
                room2.title('Search By Criminal Number')

                Label(room2, text='Enter Criminal Number:', font=('impact', 12),relief='sunken',bd=4).pack(pady=5)
                crno_search = IntVar()
                crno_search.set('')
                ma1=Entry(room2, textvariable=crno_search, highlightthickness=2, highlightbackground='gray', highlightcolor='green')
                ma1.pack(pady=5)
                ma1.focus_set() 

                def perform_search():
                    crno = crno_search.get()
                    results = [
                        row for row in table.get_children()
                        if crno == table.item(row)['values'][0]
                    ]

                    if results:
                        for item in table.get_children():
                            table.selection_remove(item)
                        for result in results:
                            table.selection_add(result)
                        messagebox.showinfo("Search Results", f"{len(results)} record(s) found.")
                    else:
                        messagebox.showinfo("Search Results", "No records found.")

                    room2.destroy()

                Button(room2, text='Search', command=perform_search).pack(pady=10)

            def search_by_crime():
                room3 = Toplevel(root2)
                room3.geometry('400x200+40+40')
                room3.title('Search By Crime')

                Label(room3, text='Enter Crime:', font=('impact', 12),relief='sunken',bd=4).pack(pady=5)
                crime_search = StringVar()
                ma2=Entry(room3, textvariable=crime_search, highlightthickness=2, highlightbackground='gray', highlightcolor='green')
                ma2.pack(pady=5)
                ma2.focus_set()

                def perform_search():
                    crime = crime_search.get().lower()
                    results = [
                        row for row in table.get_children()
                        if crime in table.item(row)['values'][4].lower()
                    ]

                    if results:
                        for item in table.get_children():
                            table.selection_remove(item)
                        for result in results:
                            table.selection_add(result)
                        messagebox.showinfo("Search Results", f"{len(results)} record(s) found.")
                    else:
                        messagebox.showinfo("Search Results", "No records found.")

                    room3.destroy()

                Button(room3, text='Search', command=perform_search).pack(pady=10)

            Button(root3, text='Search By Name', font=('impact'), command=search_by_name, relief='raised', bd=4).pack(padx=10, pady=10)
            Button(root3, text='Search By Criminal Number', font=('impact'), command=search_by_crno, relief='raised', bd=4).pack(padx=10, pady=10)
            Button(root3, text='Search By Crime', font=('impact'), command=search_by_crime, relief='raised', bd=4).pack(padx=10, pady=10)

        Button(root2, text='Search', font=('impact'), command=search, relief='raised', bd=4, fg='blue').place(x=200, y=0)

        
    else:
        messagebox.showinfo('Login Status', 'Access Denied')
        password.set('')
        username.set('')
        e1.focus_set()

root1 = Tk()
root1.geometry('400x260+400+50')
root1.title('Login')

password = StringVar()
username = StringVar()

Label(root1, text='LOGIN TO SYSTEM', font=('impact', 26)).pack(pady=10)
Label(root1, text='Username', font=('calibri', 12), highlightthickness=2, highlightbackground='gray', highlightcolor='green').pack(padx=10)
e1 = Entry(root1, textvariable=username, highlightthickness=4, highlightbackground='gray', highlightcolor='green')
e1.pack(padx=10)
Label(root1, text='Password', font=('calibri', 12), highlightthickness=2, highlightbackground='gray', highlightcolor='green').pack(padx=10)
e2 = Entry(root1, textvariable=password, highlightthickness=4, highlightbackground='gray', highlightcolor='green', show='*')
e2.pack(padx=10)
Button(root1, text='LOGIN', font=('impact'), relief='raised', bd=4, command=login).pack(padx=10, pady=20)
root1.resizable(False, False)
e1.focus_set()
root1.mainloop()
