from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
import matplotlib.pyplot as plt
import bs4
import requests


def f1():
	add_window.deiconify()
	main_window.withdraw()

def f2():
	main_window.deiconify()
	add_window.withdraw()

def f3():
	view_window.deiconify()
	main_window.withdraw()
	view_window_st_data.delete(1.0, END)
	info = ""
	con = None
	try:
		con = connect('kit.db')
		cursor = con.cursor()
		sql = "select * from student"
		cursor.execute(sql)
		data = cursor.fetchall()
		for d in data:
			info = info + " rno = " + str(d[0]) + " name= "+ str(d[1]) + " marks= "+ str(d[2])+ "\n"
		view_window_st_data.insert(INSERT, info)
	except Exception as e:
		showerror('Failure', e)
	finally:
		if con is not None:
			con.close()

def f4():
	main_window.deiconify()
	view_window.withdraw()

def f5():
	con = None
	try:
		con = connect('kit.db')
		cursor = con.cursor()
		#sql = "create table student(rno int primary key, name text, marks int )"
		#cursor.execute(sql)
		sql = "insert into student values('%d', '%s','%d')"
		rno = add_window_ent_rno.get()
		name = add_window_ent_name.get()
		marks = add_window_ent_marks.get()
		try:
			rno = int(add_window_ent_rno.get())
			marks = int(add_window_ent_marks.get())
			if (rno>0) and (len(name)>=2) and (0<=marks<=100) and (name.isalpha()) : 
				cursor.execute(sql % (rno, name, marks))
				con.commit()
				showinfo("Success", "Record added successfully")
			elif  (rno<0):
				showerror("Failure", "Enter valid rno")
			elif (len(name)<2):
				showerror("Failure", "Enter valid name")
			elif (marks<0) or (marks>100):
				showerror("Failure", "Enter valid marks")
			elif name.isdigit():
				showerror("Failure", "Please enter characters only")
		except ValueError:
			showerror("Failure", "Enter digits only")
		except:
			showerror("Failure", "Record already exists")
		

		add_window_ent_rno.delete(0,END)
		add_window_ent_name.delete(0,END)
		add_window_ent_marks.delete(0,END)
	except Exception as e:
		showerror("Issue", e)
	
	finally:
		if con is not None:
			con.close()

def f6():
	con=None
	try:
		con=connect("kit.db")
		cursor=con.cursor()
		sql="update student set name = '%s',marks= '%d' where rno = '%d'"
		rno=update_window_ent_rno.get()
		marks=update_window_ent_marks.get()
		name=update_window_ent_name.get()
		try:
			rno = int(update_window_ent_rno.get())
			marks = int(update_window_ent_marks.get())
			if (rno>0) and (len(name)>=2) and (0<=marks<=100) and (name.isalpha()):
				cursor.execute(sql % (name, marks, rno))
			if cursor.rowcount == 1:
				con.commit()
				showinfo("Success", "Record updated successfully")
				
			elif  (rno<0):
				showerror("Failure", "Enter valid rno")
			elif (len(name)<2):
				showerror("Failure", "Enter valid name")
			elif (marks<0) or (marks>100):
				showerror("Failure", "Enter valid marks")
			elif name.isdigit():
				showerror("Failure", "Please enter characters only")
			else:
				showerror("Failure", "No such record found")

		except ValueError:
			showerror("Failure", "Enter digits only")
		update_window_ent_rno.delete(0,END)
		update_window_ent_name.delete(0,END)
		update_window_ent_marks.delete(0,END)
	except Exception as e:
		showerror("Failure",e)
				
def f7():
	con=None
	try:
		con=connect("kit.db")
		cursor=con.cursor()
		sql="delete from student where rno= '%d' "
		rno=delete_window_ent_rno.get()
		try:
			rno=int(delete_window_ent_rno.get())
			if  (rno>0):
				cursor.execute(sql % (rno))
			if cursor.rowcount==1:
				showinfo("success", "Record deleted")
				con.commit()
			else:
				showerror("failure", "Record does not exist")
		except ValueError:
			showerror("Failure", "Enter digits only")
		delete_window_ent_rno.delete(0,END)
	except Exception as e:
		showerror("Issue",e)
		con.rollback()
	finally:
		if con is not None:
			con.close()
			

def f8():
	update_window.deiconify()
	main_window.withdraw()
def f9():
	delete_window.deiconify()
	main_window.withdraw()
def f10():
	main_window.deiconify()
	update_window.withdraw()
def f11():
	main_window.deiconify()
	delete_window.withdraw()

def f12():
	charts_window.deiconify()
	main_window.withdraw()
def f13():
	con=None
	marks=[]
	name=[]
	try:
		con=connect("kit.db")
		cursor=con.cursor()
		sql="select * from student order by marks ASC"
		cursor.execute(sql)
		data=cursor.fetchall()
		for d in data:
			marks.append(int(str(d[2])))
			name.append(str(d[1]))
		plt.bar(name,marks,color=['red','blue','green',])
		plt.xlabel("Name")
		plt.ylabel("Marks")
		plt.title("Batch Information")
		plt.show()
	except Exception as e:
		showerror("Issue",e)
	finally:
		if con is not None:
			con.close()




	



main_window = Tk()
main_window.title("S.M.S")
main_window.geometry("600x600+400+100")
main_window_btn_add = Button(main_window, text="Add", font=('Arial', 20, 'bold'), width=10, command=f1)
main_window_btn_view = Button(main_window, text="View", font=('Arial', 20, 'bold'), width=10, command=f3)
main_window_btn_update = Button(main_window, text="Update", font=('Arial', 20, 'bold'), width=10,command=f8)
main_window_btn_delete = Button(main_window, text="Delete", font=('Arial', 20, 'bold'), width=10,command=f9)
main_window_btn_charts = Button(main_window, text="Charts", font=('Arial', 20, 'bold'), width=10,command=f13)
try:
	wa = "https://ipinfo.io/"
	res = requests.get(wa)
	data=res.json()
	loc=data['loc']
except Exception as e:
	print("Issue",e)
main_window_lbl_location = Label(main_window, text="Location:" + loc, font=('Arial', 20, 'bold'))
try:
	a1 = "https://api.openweathermap.org/data/2.5/weather?units=metric"
	a2 = "&q=" + "mumbai"
	a3 = "&appid=" + "c6e315d09197cec231495138183954bd"
	ta= a1+a2+a3
	response=requests.get(ta)
	data=response.json()
	temp=str(data['main']['temp'])
except Exception as e:
	print("issue", e)
main_window_lbl_temp = Label(main_window, text="Temp:" + temp, font=('Arial', 20, 'bold'))
try:
	wa= "https://www.brainyquote.com/quote_of_the_day"
	res=requests.get(wa)
	data=bs4.BeautifulSoup(res.text, 'html.parser')
	info=data.find('img',{'class':'p-qotd'})
	msg=info['alt']
except Exception as e:
	print("Issue",e)
main_window_lbl_qotd = Label(main_window, text="QOTD: " + msg, font=('Arial', 20, 'bold'))
main_window_btn_add.pack(pady=10)
main_window_btn_view.pack(pady=10)
main_window_btn_update.pack(pady=10)
main_window_btn_delete.pack(pady=10)
main_window_btn_charts.pack(pady=10)
main_window_lbl_location.place(x=10,y=400)
main_window_lbl_temp.place(x=350,y=400)
main_window_lbl_qotd.place(x=10,y=500)



add_window = Toplevel(main_window)
add_window.title("Add St.")
add_window.geometry("600x600+400+100")

add_window_lbl_rno = Label(add_window, text="enter rno", font=('Arial', 20, 'bold'))
add_window_ent_rno = Entry(add_window, bd=5, font=('Arial', 20, 'bold'))
add_window_lbl_name = Label(add_window, text="enter name", font=('Arial', 20, 'bold'))
add_window_ent_name = Entry(add_window, bd=5, font=('Arial', 20, 'bold'))
add_window_lbl_marks = Label(add_window, text="enter marks", font=('Arial', 20, 'bold'))
add_window_ent_marks = Entry(add_window, bd=5, font=('Arial', 20, 'bold'))
add_window_btn_save = Button(add_window, text="Save", font=('Arial', 20, 'bold'), command=f5)
add_window_btn_back = Button(add_window, text="Back", font=('Arial', 20, 'bold'), command=f2)

add_window_lbl_rno.pack(pady=10)
add_window_ent_rno.pack(pady=10)
add_window_lbl_name.pack(pady=10)
add_window_ent_name.pack(pady=10)
add_window_lbl_marks.pack(pady=10)
add_window_ent_marks.pack(pady=10)
add_window_btn_save.pack(pady=10)
add_window_btn_back.pack(pady=10)
add_window.withdraw()

view_window = Toplevel(main_window)
view_window.title("View St.")
view_window.geometry("600x600+400+100")

view_window_st_data = ScrolledText(view_window, width=50, height=10, font=('Arial', 20, 'bold'))
view_window_btn_back = Button(view_window, text="Back", font=('Arial', 20, 'bold'), command=f4)
view_window_st_data.pack(pady=10)
view_window_btn_back.pack(pady=10)
view_window.withdraw()

update_window = Toplevel(main_window)
update_window.title("Update St.")
update_window.geometry("600x600+400+100")

update_window_lbl_rno = Label(update_window, text="enter rno", font=('Arial', 20, 'bold'))
update_window_ent_rno = Entry(update_window, bd=5, font=('Arial', 20, 'bold'))
update_window_lbl_name = Label(update_window, text="enter name", font=('Arial', 20, 'bold'))
update_window_ent_name = Entry(update_window, bd=5, font=('Arial', 20, 'bold'))
update_window_lbl_marks = Label(update_window, text="enter marks", font=('Arial', 20, 'bold'))
update_window_ent_marks = Entry(update_window, bd=5, font=('Arial', 20, 'bold'))
update_window_btn_save = Button(update_window, text="Update", font=('Arial', 20, 'bold'), command=f6)
update_window_btn_back = Button(update_window, text="Back", font=('Arial', 20, 'bold'), command=f10)

update_window_lbl_rno.pack(pady=10)
update_window_ent_rno.pack(pady=10)
update_window_lbl_name.pack(pady=10)
update_window_ent_name.pack(pady=10)
update_window_lbl_marks.pack(pady=10)
update_window_ent_marks.pack(pady=10)
update_window_btn_save.pack(pady=10)
update_window_btn_back.pack(pady=10)
update_window.withdraw()

delete_window = Toplevel(main_window)
delete_window.title("Delete St.")
delete_window.geometry("600x600+400+100")

delete_window_lbl_rno = Label(delete_window, text="enter rno", font=('Arial', 20, 'bold'))
delete_window_ent_rno = Entry(delete_window, bd=5, font=('Arial', 20, 'bold'))
delete_window_btn_save = Button(delete_window, text="Delete", font=('Arial', 20, 'bold'), command=f7)
delete_window_btn_back = Button(delete_window, text="Back", font=('Arial', 20, 'bold'), command=f11)

delete_window_lbl_rno.pack(pady=10)
delete_window_ent_rno.pack(pady=10)
delete_window_btn_save.pack(pady=10)
delete_window_btn_back.pack(pady=10)
delete_window.withdraw()

main_window.mainloop()