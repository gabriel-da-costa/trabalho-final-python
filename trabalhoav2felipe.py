from tkinter import *
from tkinter import messagebox as msgb
from tkinter import ttk as ttk
import sqlite3


def database():
    conn = sqlite3.connect('./Notas.db')
    cur = conn.cursor()
    conn.execute("""CREATE TABLE IF NOT EXISTS notas(
                    idnota INTEGER PRIMARY KEY AUTOINCREMENT,
                    materia TEXT NOT NULL,
                    nota1 DOUBLE NOT NULL,
                    nota2 DOUBLE NOT NULL,
                    nota3 DOUBLE NOT NULL,                    
                    media DOUBLE NOT NULL,
                    resultado TEXT NOT NULL)""")
    cur.execute('SELECT * FROM notas ORDER BY materia')
    fetch = cur.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cur.close()
    conn.close()


def insertNota(materia, nota, nota2, nota3, media, resultado):
    conn = sqlite3.connect('./Notas.db')
    cur = conn.cursor()
    conn.execute('INSERT INTO notas (materia, nota1, nota2, nota3, media, resultado) VALUES(?, ?, ?, ?, ?, ?)',(materia, nota, nota2, nota3, media, resultado))
    conn.commit()
    cur.execute('SELECT * FROM notas ORDER BY materia')
    fetch = cur.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cur.close()
    conn.close()


def updateNota(materia, nota, nota2, nota3, media, resultado, idnota):
    conn = sqlite3.connect('./Notas.db')
    cur = conn.cursor()
    conn.execute('UPDATE notas SET materia = ?, nota1 = ?, nota2 = ?, nota3 = ?, media = ?, resultado = ? WHERE idnota = ?',(materia, nota, nota2, nota3, media, resultado, idnota))
    conn.commit()
    cur.execute('SELECT * FROM notas ORDER BY materia')
    fetch = cur.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cur.close()
    conn.close()


def deleteNota(idnota):
    conn = sqlite3.connect('./Notas.db')
    cur = conn.cursor()
    conn.execute('DELETE FROM notas WHERE idnota = ?', (idnota, ))
    conn.commit()
    conn.close()

def deleteData():
    if not tree.selection():
        msgb.showwarning("Nenhum item selecionado.", "Selecione o item que deseja excluir!", icon="warning")
    else:
        ask = msgb.askquestion("Tem certeza?", "Tem certeza que deseja excluir esse item? ", icon="warning")
        if ask == 'yes':            
            selectItem = tree.focus()
            content = (tree.item(selectItem))
            selectedItem = content["values"]
            tree.delete(selectItem)
            id = selectedItem[0]
            deleteNota(id)

def updateData():
    tree.delete(*tree.get_children())
    if (AV3.get() > AV1.get()):
        nota1 = AV3.get()
        nota2 = AV2.get()
    else:
        nota1 = AV1.get()
        if (AV3.get()>AV2.get()):
            nota2 = AV3.get()
        else:
            nota2 = AV2.get()
    if(AVDS.get()>AVD.get()):
        nota3 = AVDS.get()
    else:
        nota3 = AVD.get()
    average.set((nota1+nota2+nota3)/3)
    if(average.get()>=6):
        result = ' PARAB??NS, VOC?? EST?? APROVADO!'
    else:
        result = 'REPROVADO, ESTUDE MAIS!'
    updateNota(subject.get(), nota1, nota2, nota3, average.get(), result, id)
    subject.set("")
    AV1.set("")
    AV2.set("")
    AV3.set("")
    AVD.set("")
    AVDS.set("")
    average.set("")
    updateWindow.destroy()

def onSelected(event):
    global id, updateWindow
    selectItem = tree.focus()
    content = (tree.item(selectItem))
    selectedItem = content["values"]
    id = selectedItem[0]
    subject.set(selectedItem[1])
    AV1.set(selectedItem[2])
    AV2.set(selectedItem[3])
    AVD.set(selectedItem[4])
    average.set(selectedItem[5])
    result.set(selectedItem[6])
    updateWindow = Toplevel()
    updateWindow.title("Atualizar notas")
    width = 480
    height = 270
    sc_width = updateWindow.winfo_screenwidth()
    sc_height = updateWindow.winfo_screenheight()
    x = (sc_width/2) - (width/2)
    y = (sc_height/2) - (height/2)
    updateWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    updateWindow.resizable(0, 0)
    registerTitle = Frame(updateWindow)
    registerTitle.pack(side=TOP)
    registerContact = Frame(updateWindow)
    registerContact.pack(side=TOP, pady=10)
    registerWarning = Frame(updateWindow)
    registerWarning.pack(side=BOTTOM)
    lblWarning = Label(registerWarning, text="Caso n??o tenha realizado a avalia????o,por favor deixe como zero!", font=("consolas", 10), bg="#d1ad5e", width=250)
    lblTitle = Label(registerTitle, text="Atualize os dados",font=("consolas", 25), bg="#7cbb63", width=300)
    lblTitle.pack(fill=X)
    lblsubject = Label(registerContact, text="Digite a materia", font=("consolas", 10))
    lblsubject.grid(row=0, sticky=W)
    lblAV1 = Label(registerContact, text="Digite a sua nota da AV1",font=("consolas", 10))
    lblAV1.grid(row=1, sticky=W)
    lblAV2 = Label(registerContact, text="Digite a sua nota da AV2",font=("consolas", 10))
    lblAV2.grid(row=2, sticky=W)
    lblAV3 = Label(registerContact, text="Digite a sua nota da AV3",font=("consolas", 10))
    lblAV3.grid(row=3, sticky=W)
    lblAVD = Label(registerContact, text="Digite a nota da AVD",font=("consolas", 10))
    lblAVD.grid(row=4, sticky=W)
    lblAVDS = Label(registerContact,text="Digite a nota da AVDS", font=("consolas", 10))
    lblAVDS.grid(row=5, sticky=W)
    subjectEntry = Entry(registerContact, textvariable=subject, font=('arial', 12))
    subjectEntry.grid(row=0, column=1)
    AV1Entry = Entry(registerContact, textvariable=AV1, font=('arial', 12))
    AV1Entry.grid(row=1, column=1)
    AV2Entry = Entry(registerContact, textvariable=AV2, font=('arial', 12))
    AV2Entry.grid(row=2, column=1)
    AV3Entry = Entry(registerContact, textvariable=AV3, font=('arial', 12))
    AV3Entry.grid(row=3, column=1)
    AVDEntry = Entry(registerContact, textvariable=AVD, font=('arial', 12))
    AVDEntry.grid(row=4, column=1)
    AVDSEntry = Entry(registerContact, textvariable=AVDS, font=('arial', 12))
    AVDSEntry.grid(row=5, column=1)
    bttnInsert = Button(registerContact, text="Atualizar dados", bg="#c98654", width=50, command=validateDataUpdate)
    bttnInsert.grid(row=7, columnspan=2, pady=10)    
    insertWindow.mainloop()

def validateData():
    try:
        AV1.get()
        AV2.get()
        AV3.get()
        AVD.get()
        AVDS.get()
    except:
        msgb.showwarning("Tipo inv??lido!", "Por favor, insira um tipo v??lido!")
        insertWindow.destroy()
        insertData()
    else:
        submitData()

def validateDataUpdate():
    try:
        AV1.get()
        AV2.get()
        AV3.get()
        AVD.get()
        AVDS.get()
    except:
        msgb.showwarning("Tipo inv??lido!", "Por favor, insira um tipo v??lido!")
        updateWindow.destroy()
    else:
        updateData()

def submitData():
    if AV1.get() == None or subject.get() == "" or AV2.get() == None or AV3.get() == None or AVD.get() == None or AVDS.get() == None:
        resultado = msgb.showwarning("Voc?? esqueceu de preencher algum campo. Verifique os campos!", icon="warning")
    else:
        tree.delete(*tree.get_children())
        nota1 = 0.0
        nota2 = 0.0
        nota3 = 0.0
        if (AV3.get()>AV1.get()):
            nota1 = AV3.get()
            nota2 = AV2.get()
        else:
            nota1 = AV1.get()
            if (AV3.get()>AV2.get()):
                nota2 = AV3.get()
            else:
                nota2 = AV2.get()
        if(AVDS.get()>AVD.get()):
            nota3 = AVDS.get()
        else:
            nota3 = AVD.get()
        average.set((nota1+nota2+nota3)/3)
        if(average.get()>=6):
            result = 'PARAB??NS, VOC?? EST?? APROVADO!'
        else:
            result = 'REPROVADO, ESTUDE MAIS!'
        insertNota(subject.get(),nota1, nota2, nota3, average.get(), result)
        subject.set("")
        AV1.set(0)
        AV2.set(0)
        AV3.set(0)
        AVD.set(0)
        AVDS.set(0)
        average.set("")

def insertData():
    subject.set("")
    AV1.set(0)
    AV2.set(0)
    AV3.set(0)
    AVD.set(0)
    AVDS.set(0)
    global insertWindow    
    insertWindow = Toplevel()
    insertWindow.title("Inserir Nota")
    width = 480
    height = 270
    sc_width = insertWindow.winfo_screenwidth()
    sc_height = insertWindow.winfo_screenheight()
    x = (sc_width/2) - (width/2)
    y = (sc_height/2) - (height/2)
    insertWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    insertWindow.resizable(0, 0)
    registerTitle = Frame(insertWindow)
    registerTitle.pack(side=TOP)
    registerContact = Frame(insertWindow)
    registerContact.pack(side=TOP, pady=10)
    registerWarning = Frame(insertWindow)
    registerWarning.pack(side=BOTTOM)
    lblWarning = Label(registerWarning, text="Se n??o tiver feito a avalia????o, por favor deixe como zero!", font=("consolas", 12), bg="#d1ad5e", width=200)
    lblWarning.pack(fill=X)
    lblTitle = Label(registerTitle, text="Insira os dados",font=("consolas", 25), bg="#7cbb63", width=300)
    lblTitle.pack(fill=X)
    lblsubject = Label(registerContact, text="Digite a materia", font=("consolas", 10))
    lblsubject.grid(row=0, sticky=W)
    lblAV1 = Label(registerContact, text="Digite a sua nota da AV1",font=("consolas", 10))
    lblAV1.grid(row=1, sticky=W)
    lblAV2 = Label(registerContact, text="Digite a sua nota da AV2", font=("consolas", 10))
    lblAV2.grid(row=2, sticky=W)
    lblAV3 = Label(registerContact, text="Digite a sua nota da AV3",font=("consolas", 10))
    lblAV3.grid(row=3, sticky=W)
    lblAVD = Label(registerContact, text="Digite a sua nota da AVD",font=("consolas", 10))
    lblAVD.grid(row=4, sticky=W)
    lblAVDS = Label(registerContact, text="Digite a sua nota da AVDS",font=("consolas", 10))
    lblAVDS.grid(row=5, sticky=W)
    subjectEntry = Entry(registerContact, textvariable=subject, font=('arial', 12))
    subjectEntry.grid(row=0, column=1)
    AV1Entry = Entry(registerContact, textvariable=AV1, font=('arial', 12))
    AV1Entry.grid(row=1, column=1)
    AV2Entry = Entry(registerContact, textvariable=AV2, font=('arial', 12))
    AV2Entry.grid(row=2, column=1)
    AV3Entry = Entry(registerContact, textvariable=AV3, font=('arial', 12))
    AV3Entry.grid(row=3, column=1)
    AVDEntry = Entry(registerContact, textvariable=AVD, font=('arial', 12))
    AVDEntry.grid(row=4, column=1)
    AVDSEntry = Entry(registerContact, textvariable=AVDS, font=('arial', 12))
    AVDSEntry.grid(row=5, column=1)
    bttnInsert = Button(registerContact, text="Inserir dados",bg="#acc954", width=50, command=validateData)
    bttnInsert.grid(row=7, columnspan=2, pady=10)
    insertWindow.mainloop()

root = Tk()
subject = StringVar()
AV1 = DoubleVar()
AV2 = DoubleVar()
AV3 = DoubleVar()
AVD = DoubleVar()
AVDS = DoubleVar()
average = DoubleVar()
result = StringVar()
id = None
insertWindow = None
updateWindow = None
root.title('Gerenciador de notas')
width = 1024
height = 600
scWidth = root.winfo_screenwidth()
scHeight = root.winfo_screenheight()
x = (scWidth/2) - (width/2)
y = (scHeight/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.config(bg='#26547C')
root.resizable(0,0)
top = Frame(root, width=1250, bd=1, relief=SOLID)
top.pack(side=TOP)
mid = Frame(root, width=1250, bg="#6666ff")
mid.pack(side=TOP)
midLeft = Frame(mid, width=250)
midLeft.pack(side=LEFT)
midLeftPadding = Frame(mid, width=750, bg="#6666ff")
midLeftPadding.pack(side=LEFT)
midRight = Frame(mid, width=250)
midRight.pack(side=RIGHT)
bottom = Frame(root, width=500)
bottom.pack(side=BOTTOM)
tableMargim = Frame(root, width=1250)
tableMargim.pack(side=TOP)
bttnInsert = Button(midLeft, text="Inserir", bg="#639bbf", command=insertData)
bttnInsert.pack()
bttnDelete = Button(midRight, text="Deletar", bg="#c954ba", command=deleteData)
bttnDelete.pack(side=RIGHT)
scrollX = Scrollbar(tableMargim, orient=HORIZONTAL)
scrollY = Scrollbar(tableMargim, orient=VERTICAL)
tree = ttk.Treeview(tableMargim, columns=("ID", "MATERIA", "NOTA 1", "NOTA 2","NOTA 3", "MEDIA", "RESULTADO"),height=400, selectmode="extended", yscrollcommand=scrollY.set, xscrollcommand=scrollX.set)
scrollY.config(command=tree.yview)
scrollY.pack(side=RIGHT, fill=Y)
scrollX.config(command=tree.xview)
scrollX.pack(side=BOTTOM, fill=X)
tree.heading("ID", text="ID", anchor=W)
tree.heading("MATERIA", text="Materia", anchor=W)
tree.heading("NOTA 1", text="Nota1", anchor=W)
tree.heading("NOTA 2", text="Nota2", anchor=W)
tree.heading("NOTA 3", text="Nota3", anchor=W)
tree.heading("MEDIA", text="Media", anchor=W)
tree.heading("RESULTADO", text="Resultado", anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=3)
tree.column('#1', stretch=NO, minwidth=0, width=100)
tree.column('#2', stretch=NO, minwidth=0, width=150)
tree.column('#3', stretch=NO, minwidth=0, width=150)
tree.column('#4', stretch=NO, minwidth=0, width=155)
tree.column('#5', stretch=NO, minwidth=0, width=155)
tree.column('#6', stretch=NO, minwidth=0, width=155)
tree.pack()
tree.bind('<Double-Button-1>', onSelected)
database()
root.mainloop()