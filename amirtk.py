
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import mysql.connector
import winsound

ctk.set_appearance_mode('dark')
app = ctk.CTk()
app.geometry('645x535+500+150')
app.title('Amir Alizade')
app.resizable(False,False)

current_theme = ctk.get_appearance_mode()



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



def esc(event=None):
    app.destroy()




def custom_confirm(title,message):
    dialog = ctk.CTkToplevel(app)
    dialog.title(title)
    dialog.geometry('400x200')
    dialog.resizable(False,False)
    dialog.grab_set()
    dialog.transient(app)


    app.update_idletasks()
    x = app.winfo_x() + (app.winfo_width() // 2) - 200
    y = app.winfo_y() + (app.winfo_height() // 2) - 200
    dialog.geometry(f'400x200+{x}+{y}')

    label = ctk.CTkLabel(dialog,text=message,font=('georgia',15,'bold'))
    label.pack(pady=40)

    result = False

    def on_yes():
        nonlocal result
        result = True
        dialog.destroy()
    
    def on_no():
        nonlocal result
        result = False
        dialog.destroy()

    yes_btn = ctk.CTkButton(dialog,text='Yes',fg_color='#3ECA75',font=('georgia',15,'bold'),text_color='black',command=on_yes,)    
    yes_btn.place(x=50,y=120)

    no_btn = ctk.CTkButton(dialog,text='No',fg_color='#ED1C24',font=('georgia',15,'bold'),text_color='black',command=on_no,)    
    no_btn.place(x=220,y=120)

    dialog.bind('<Escape>', lambda e: on_no())

    app.wait_window(dialog)
    return result



def show_temp_message(message, color='green',duration=3000):
    temp_label = ctk.CTkLabel(frame, text=message, text_color=color, font=('Georgia', 13, 'bold'))
    temp_label.place(x=100,y=220)
    frame.after(duration,temp_label.destroy)

def play_sound():
    winsound.Beep(600, 150)


def add(event=None):
    id = id_entry.get()
    name = name_entry.get()
    lname = lname_entry.get()
    phone = phone_entry.get()
    
    play_sound()

    if id and name and lname :
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
    else:
        show_temp_message('Enter ID,Name,Last name', 'orange')

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

    play_sound()

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

    play_sound()

    if not id:
        # error_label.configure(text='❗ Enter a Value', text_color='orange')
        show_temp_message('❗ Enter a Valid ID', 'orange')
        return
    

    confirm = custom_confirm("Confirm Delete", f"Are you sure you want to delete customer ID {id}?")

    if confirm:

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
    name_entry.delete(0,'end')
    lname_entry.delete(0,'end')
    phone_entry.delete(0,'end')

def edit():
    i = id_entry.get()
    n = name_entry.get()
    l = lname_entry.get()
    p = phone_entry.get()

    play_sound()

    if n :
        sql = ('UPDATE customer SET Name =  %s WHERE ID = %s')
        val = (n,i)
        mycursor.execute(sql,val)
    if l :
        sql = ('UPDATE customer SET Last_name =  %s WHERE ID = %s')
        val = (l,i)
        mycursor.execute(sql,val)
    if p :
        sql = ('UPDATE customer SET Phone =  %s WHERE ID = %s')
        val = (p,i)
        mycursor.execute(sql,val)

    mydb.commit()

    mycursor.execute('SELECT * FROM customer')
    result = mycursor.fetchall()
    treeview.delete(*treeview.get_children())
    for i in result:
        treeview.insert('','end',values=i)
    
    id_entry.delete(0,'end')
    name_entry.delete(0,'end')
    lname_entry.delete(0,'end')
    phone_entry.delete(0,'end')



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
add_btn = ctk.CTkButton(frame, width=100, height=25, text='Add', border_width=2,border_color='black' , fg_color='#3ECA75', text_color='black',corner_radius=1,font=('Georgia',15,'bold'),command=add)
add_btn.place(x=400, y=75)

show_btn = ctk.CTkButton(frame, width=100, height=25, text='Show', border_width=2,border_color='black',fg_color='#FEBE10', text_color='black',corner_radius=1,font=('Georgia',15,'bold'),command=show)
show_btn.place(x=400, y = 15)

del_btn = ctk.CTkButton(frame, width=100, height=25, text='Delete', border_width=2,border_color='black', fg_color='#ED1C24', text_color='black',corner_radius=1,font=('Georgia',15,'bold'),command=delete)
del_btn.place(x=400, y = 135)

edit_btn = ctk.CTkButton(frame, width=100, height=25, text='Edit',border_width=2,border_color='black', fg_color='cyan', text_color='black',corner_radius=1,font=('Georgia',15,'bold'),command=edit)
edit_btn.place(x=400, y=195)
#------------------------------------------------------------------------------------------------------------------------------
def change_theme(choice):
    ctk.set_appearance_mode(choice)

theme_menu = ctk.CTkOptionMenu(frame,width=80,values=["Dark", "Light"],fg_color=('white',"#4B4B4B"),text_color=('black','white'),
                               button_color=('white',"#2B2B2B"),button_hover_color="#0077b6",dropdown_fg_color=('white',"#3B3B3B"),
                               font=('georgia',15,'bold'),dropdown_font=('georgia',12,'bold'),corner_radius=2,command=change_theme,)
theme_menu.place(x=550,y=3)

theme_menu.set("Dark")
#------------------------------------------------------------------------------------------------------------------------------
treeview_frame = ttk.Frame(app)
treeview_frame.place(x=9,y=330)

style = ttk.Style(app)
style.theme_use('clam')

style.configure('Treeview',background = '#242424',fieldbackground = '#242424',foreground = 'lime green',font=('Georgia', 12))
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



app.bind('<Escape>', esc)
app.mainloop()
