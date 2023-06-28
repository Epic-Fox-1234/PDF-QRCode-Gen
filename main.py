import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import threading
import utils
import generator

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.outputFile=None

        self.title("QR Code Page generator")
        self.geometry("600x200")

        logo=tk.PhotoImage(file=utils.resource_path("assets/logo-512x512.png"))
        self.iconphoto(False,logo)


        # Column proportions
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        self.columnconfigure(2,weight=3)


        self.label_data=ttk.Label(self,text="Daten: ")
        self.label_data.grid(row=0,column=0,sticky=tk.E)

        self.input_data=ttk.Entry(self)
        self.input_data.grid(row=0,column=1,columnspan=2,sticky=tk.W+tk.E)


        self.label_cols=ttk.Label(self,text="Spalten: ")
        self.label_cols.grid(row=1,column=0,sticky=tk.E)

        vIcmd=self.register(self.validateInt)
        self.input_cols=ttk.Entry(self,validatecommand=(vIcmd,"%P"),validate="key")
        self.input_cols.grid(row=1,column=1,columnspan=2,sticky=tk.W)


        self.label_rows=ttk.Label(self,text="Zeilen: ")
        self.label_rows.grid(row=2,column=0,sticky=tk.E)

        self.input_rows=ttk.Entry(self,validatecommand=(vIcmd,"%P"),validate="key")
        self.input_rows.grid(row=2,column=1,columnspan=2,sticky=tk.W)


        self.label_output_file=ttk.Label(self,text="Ziel Datei: ")
        self.label_output_file.grid(row=3,column=0,sticky=tk.E)

        self.input_output_file=ttk.Button(self,text="Ziel Datei ändern",command=lambda :self.setOutputFile())
        self.input_output_file.grid(row=3,column=1,sticky=tk.W)

        self.label_output_file_feedback_label=ttk.Label(self,text="Ziel Datei: ") 
        self.label_output_file_feedback_label.grid(row=4,column=0,sticky=tk.E)

        self.label_output_file_feedback=ttk.Label(self,text="") 
        self.label_output_file_feedback.grid(row=4,column=1,columnspan=2,sticky=tk.W)


        self.make_Code_button=ttk.Button(self,text="PDF generieren!",command=self.makePDF)
        self.make_Code_button.grid(row=5,column=0,columnspan=3,sticky=tk.W+tk.E)

    def validateInt(self,P):
        if P.isdigit() or P=="":
            return True
        else:
            return False
    
    def makePDF(self):
        if not self.checkInput():
            messagebox.askokcancel(title="Eingabe ungültig",message="Deine Eingabe ist falsch oder unvollständig.")
            return False
    
        startPDF_Thread=threading.Thread(target=self._makePDF)
        self.make_Code_button.config(text="PDF wird erstellt...",state=tk.DISABLED)
        self.config(cursor="watch")
        startPDF_Thread.start()

    def _makePDF(self):
        generator.generate_qr_code_pdf(self.input_data.get(), self.outputFile, qr_per_row=int(self.input_cols.get()),qr_per_col=int(self.input_rows.get()), margin=0, qr_scale=50)
    
        self.make_Code_button.config(text="PDF generieren!",state=tk.NORMAL)
        self.config(cursor="")
        messagebox.showinfo(title="Fertig!",message="PDF wurde erstellt und gespeichert.")
        return True
    

    def checkInput(self):
        if self.input_cols.get() in (None,""):return False
        if self.input_rows.get() in (None,""):return False
        if self.input_data.get() in (None,""):return False
        if self.outputFile in (None,""):return False

        return True

    def setOutputFile(self,*args,**kwargs):
        _temp=None
        while _temp==None:
            _temp=filedialog.asksaveasfilename(title="Wo soll das PDF gespeichert werden?", filetypes=[("PDF","*.pdf")],initialfile="*.pdf")
        self.outputFile=_temp
        self.label_output_file_feedback.config(text=self.outputFile)



if __name__=="__main__":

    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        print("Failed to change DPI")

    app=App()
    app.mainloop()

