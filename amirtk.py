
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import mysql.connector


ctk.set_appearance_mode('dark')
app = ctk.CTk()
app.geometry('645x535')
app.title('Amir Alizade')
app.resizable(False,False)


mydb = None
conn = None

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '836547',
    database = 'amir'
)

mycursor = mydb.cursor()


temp_label = None

def show_temp_message(message, color='green',duration=3000):
    temp_label = ctk.CTkLabel(frame, text=message, text_color=color, font=('Georgia', 13, 'bold'))
    temp_label.place(x=100,y=220)
    frame.after(duration,temp_label.destroy)





def confirm():
    id = id_entry.get()
    name = name_entry.get()
    lname = lname_entry.get()
    phone = phone_entry.get()

    try:
        sql = "INSERT INTO customer (id, name, last_name, phone) VALUES (%s, %s, %s, %s)"
        val = (id, name, lname, phone)

        mycursor.execute(sql, val)
        mydb.commit()
        # error_label.configure(text='✔️Successfully Entered',text_color='green')
        show_temp_message('✔️ Successfully Entered', 'green')


    except Exception as e:
        # error_label.configure(text=f'error : {e}')
        show_temp_message(f'error : {e}','red')


    mycursor.execute('SELECT * FROM customer')
    result = mycursor.fetchall()

    treeview.delete(*treeview.get_children())
    for row in result:
        treeview.insert('','end', values=row)

    id_entry.delete(0,'end')
    name_entry.delete(0,'end')
    lname_entry.delete(0,'end')
    phone_entry.delete(0,'end')

def show():
    id = id_entry.get()
    name = name_entry.get()
    lname =lname_entry.get()

    treeview.delete(*treeview.get_children())

    if id:
        values = (id,)
        sql = 'SELECT * FROM customer WHERE ID = %s'
        mycursor.execute(sql, values)
        result = mycursor.fetchall()  

        for row in result:
            treeview.insert('', 'end', values=row)


    elif name:
        values = (name,)
        sql = 'SELECT * FROM customer WHERE Name = %s'
        mycursor.execute(sql, values)
        result = mycursor.fetchall() 
        for row in result:
            treeview.insert('', 'end', values=row)

    elif lname:
        values = (lname,)
        sql = 'SELECT * FROM customer WHERE Last_name = %s'
        mycursor.execute(sql,values)
        result = mycursor.fetchall()
        for row in result:
            treeview.insert('','end',values=row)
        

    else:
        mycursor.execute('SELECT * FROM customer')
        result = mycursor.fetchall()

        treeview.delete(*treeview.get_children())
        for row in result:
            treeview.insert('','end', values=row)

    id_entry.delete(0,'end')
    name_entry.delete(0,'end')
    lname_entry.delete(0,'end')
    phone_entry.delete(0,'end')

def delete():
    id = id_entry.get()

    if not id:
        # error_label.configure(text='❗ Enter a Value', text_color='orange')
        show_temp_message('❗ Enter a Valid ID', 'orange')
        return

    try:
        values = (id,)
        sql = 'DELETE FROM customer WHERE id = %s'
        mycursor.execute(sql, values)
        mydb.commit()

        if mycursor.rowcount == 0:
            # error_label.configure(text='❌ id not found', text_color='red')
            show_temp_message('❌ id not found', 'red')

        else:
            # error_label.configure(text='✔️ Deleted', text_color='green')
            show_temp_message('✔️ Deleted', 'green')


        

    except Exception as e:
        # error_label.configure(text=f'خطا: {e}', text_color='red')
        show_temp_message(f'خطا: {e}', 'red')

    

    mycursor.execute('SELECT * FROM customer')
    result = mycursor.fetchall()
    treeview.delete(*treeview.get_children())
    for row in result:
        treeview.insert('','end', values=row)

    id_entry.delete(0,'end')



def on_treeview_click(event):
    selected_item  = treeview.focus()
    if not selected_item:
        return
    
    values = treeview.item(selected_item,'values')
    if values:
        id_entry.delete(0,'end')
        id_entry.insert(0,values[0])

        name_entry.delete(0,'end')
        name_entry.insert(0,values[1])

        lname_entry.delete(0,'end')
        lname_entry.insert(0,values[2])

        phone_entry.delete(0,'end')
        phone_entry.insert(0,values[3])



#------------------------------------------------------------------------------------------------------------------
frame = ctk.CTkFrame (app, width=635, height=256, bg_color='transparent',
                      corner_radius=1, border_width=3,border_color=('#000000','black'))
frame.place(x=3, y=6)
#------------------------------------------------------------------------------------------------------------------
id_label = ctk.CTkLabel(frame, text='ID :', text_color=('black','white'), font=("Georgia", 13, "bold"))
id_label.place(x=50,y=10)

id_entry = ctk.CTkEntry(frame, width=200, height=4, bg_color='#2B2B2B',border_color='#979998',border_width=0,corner_radius=2)
id_entry.place(x=150,y=15)

id_frame = ctk.CTkFrame(frame, width=200, height=3, bg_color=('black','#979998'),corner_radius=1)
id_frame.place(x=150, y=30)
#------------------------------------------------------------------------------------------------------------------------------
name_label = ctk.CTkLabel(frame,text='Name :',text_color=('black','white'),font=("Georgia", 13, "bold"))
name_label.place(x=50,y=70)

name_entry = ctk.CTkEntry(frame, width=200,height=4, bg_color='black',border_color='black',border_width=0,corner_radius=0)
name_entry.place(x=150,y=75)

name_frame = ctk.CTkFrame(frame,width=200,height=3,bg_color=('black','#979998'),corner_radius=1,border_width=0)
name_frame.place(x=150,y=90)
#------------------------------------------------------------------------------------------------------------------------------
lname_label = ctk.CTkLabel(frame,text='Last name :',text_color=('black','white'),font=('Georgia',13,'bold'))
lname_label.place(x=50, y=130)

lname_entry = ctk.CTkEntry(frame, width=200,height=4, bg_color='black',border_color='black',border_width=0,corner_radius=0)
lname_entry.place(x=150,y=135)

lname_frame = ctk.CTkFrame(frame,width=200,height=3,bg_color=('black','#979998'),corner_radius=1,border_width=0)
lname_frame.place(x=150,y=150)
#------------------------------------------------------------------------------------------------------------------------------
phone_label = ctk.CTkLabel(frame,text='Phone :',text_color=('black','white'),font=('Georgia',13,'bold'))
phone_label.place(x=50, y=192)

phone_entry = ctk.CTkEntry(frame, width=200,height=4, bg_color='black',border_color='black',border_width=0,corner_radius=0)
phone_entry.place(x=150,y=195)

phone_frame = ctk.CTkFrame(frame,width=200,height=3,bg_color=('black','#979998'),corner_radius=1,border_width=0)
phone_frame.place(x=150,y=210)
#------------------------------------------------------------------------------------------------------------------------------
# error_label = ctk.CTkLabel(frame,text='',text_color='red',font=('Georgia',13,'bold'))
# error_label.place(x=440,y=200)
#------------------------------------------------------------------------------------------------------------------------------
confirm_btn = ctk.CTkButton(frame, width=100, height=25, text='Confirm', border_width=2,border_color='black' , fg_color='#3ECA75', text_color=('black','black'),corner_radius=1,font=('Georgia',15,'bold'),command=confirm)
confirm_btn.place(x=450, y=40)

show_btn = ctk.CTkButton(frame, width=100, height=25, text='Show', border_width=2,border_color='black',fg_color='#FEBE10', text_color=('white','black'),corner_radius=1,font=('Georgia',15,'bold'),command=show)
show_btn.place(x=450, y = 100)

del_btn = ctk.CTkButton(frame, width=100, height=25, text='Delete', border_width=2,border_color='black', fg_color='#ED1C24', text_color=('white','black'),corner_radius=1,font=('Georgia',15,'bold'),command=delete)
del_btn.place(x=450, y = 160)

#------------------------------------------------------------------------------------------------------------------------------
treeview_frame = ttk.Frame(app)
treeview_frame.place(x=9,y=330)

style = ttk.Style(app)
style.theme_use('clam')
style.configure('Treeview',background = '#242424',fieldbackground = '#242424',foreground = 'cyan',font=('Georgia', 12))
treeview = ttk.Treeview(treeview_frame, columns=('1','2','3','4'), show ='headings',height=15)
style.configure('Treeview.Heading', font=('TkDeafultFont',13,'bold'))
treeview.pack(side=tk.LEFT, fill=tk.BOTH)
treeview.bind('<ButtonRelease-1>',on_treeview_click)

treeview.column('1', width=192)
treeview.column('2', width=192)
treeview.column('3', width=192)
treeview.column('4', width=192)
treeview.heading('1', text='ID')
treeview.heading('2', text='First_name')
treeview.heading('3', text='Last_name')
treeview.heading('4', text='Telephone')

scrollbar = ttk.Scrollbar(treeview_frame , orient=tk.VERTICAL, command=treeview.yview)
scrollbar.pack(side=tk.RIGHT ,fill=tk.Y)


app.mainloop()