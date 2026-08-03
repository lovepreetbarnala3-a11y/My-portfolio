#step1: importing
from tkinter import *
#step2: Gui interaction
window=Tk()
window.title("Calculator")
window.geometry("350x400",)
window.resizable(False,False)
#step3:entry box
e=Entry(window,width=40,borderwidth=5)
e.place(x=50,y=50)
#step4:buttons
def click(num):
    result=e.get()
    e.delete(0,END)
    e.insert(0,str(result)+str(num))
b=Button(window,text="1",width=10,command=lambda:click(1))
b.place(x=50,y=100)
b=Button(window,text="2",width=10,command=lambda:click(2))
b.place(x=135,y=100)
b=Button(window, text="3", width=10, command=lambda:click(3))
b.place(x=220,y=100)
b=Button(window, text="4", width=10, command=lambda:click(4))
b.place(x=50,y=130)
b=Button(window, text="5", width=10, command=lambda:click(5))
b.place(x=135,y=130)
b=Button(window, text="6", width=10, command=lambda: click(6))
b.place(x=220,y=130)
b=Button(window, text="7", width=10, command=lambda:click(7))
b.place(x=50,y=160)
b=Button(window,text="8",width=10,command=lambda:click(8))
b.place(x=135,y=160)
b=Button(window,text="9",width=10,command=lambda:click(9))
b.place(x=220,y=160)
b=Button(window,text="0",width=10,command=lambda:click(0))
b.place(x=50,y=190)
#step5: operators
def add():
    num1=e.get()
    global i
    global math
    math="addition"
    i=int(num1)
    e.delete(0,END)
b=Button(window,text="+",width=10,command=add)
b.place(x=135,y=190)
def sub():
    num1=e.get()
    global i
    global math
    math="subtraction"
    i=int(num1)
    e.delete(0,END)
b=Button(window,text="-",width=10,command=sub)
b.place(x=220,y=190)
def mul():
    num1=e.get()
    global i
    global math
    math="multiplication"
    i=int(num1)
    e.delete(0,END)
b=Button(window,text="*",width=10,command=mul)
b.place(x=50,y=220)
def div():
    num1=e.get()
    global i
    global math
    math="division"
    i=int(num1)
    e.delete(0,END)
b=Button(window,text="/",width=10,command=div)
b.place(x=135,y=220)
def equal():
    num2=e.get()
    e.delete(0,END)
    if math=="addition":
        e.insert(0,i+int(num2))
    elif math=="subtraction":
        e.insert(0,i-int(num2))
    elif math=="multiplication":
        e.insert(0,i*int(num2))
    elif math=="division":
        e.insert(0,i/int(num2))
    
b=Button(window,text="=",width=10,command=equal)
b.place(x=220,y=220)
def clear():
    e.delete(0,END)
b=Button(window,text="Clear",width=10,command=clear)
b.place(x=50,y=250)
def destroy():
    window.destroy()
b=Button(window,text="Quit",width=10,command=destroy)
b.place(x=135,y=250)
#step6: mainloop
mainloop()
window.mainloop()