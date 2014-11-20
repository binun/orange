"""
#This file is used as the main function of secure files in clouds
#This file is used to test Accumulating Automaton
#Especially for String Matching
#Date:2014 June 24
#Date:2014 June 30 Getindex and GetRecord OK.
#Date:2014 July 03, Insert and delete all works good

#add recontruct the whole database button to test.
#Author Ximing Li
#email: liximing.cn@gmail.com, liximing@scau.edu.cn
#version 26. it is an stable version. Delete is working
#this version is 27. it is an stable version. Insert and delete all works good
#version 28. for hiding pattern with two methods.

"""
from test import test
from finitefield import *
from polynomial import *
from modp import *
from getPrime import *
from AAbasictools import *
from tools import *
from tools import FileShares,AAShares
from math import *
from datetime import datetime, date, time
from Tkinter import *
import tkColorChooser
import tkFileDialog
import tkMessageBox as box
import ttk
import time
import pickle
#from PIL import Image, ImageTk

today = datetime.now()
logfilename='.\log\log_SecureFilesInClouds'
logfilename=logfilename+today.strftime("%Y%m%d%H%M%S")
logfilename=logfilename+'.txt'
#open logfile to write log
f_log = open(logfilename, 'w+')

f_log.write('\nThe {1} is {0:%d}, the {2} is {0:%B}, the {3} is {0:%I:%M%p}.'.format(today, "day", "month", "time"))
f_log.write('\n')
f_log.write('This file is:'+logfilename)
f_log.write('\n')

f_log.write('Main program begins\n'+'-------------------------------------------\n')  
#main program
#define

#Initiae the program
#give the Finite field and how many clouds we need

IFtest=1
n_clouds=15

#write log file
f_log.write('p='+str(p)+'\n')
f_log.write('n_clouds='+str(n_clouds)+'\n')

#it is different for each running!!!!!!!!!!!!!!!!
#so it ca
if IFtest:
    f_log.write('The finite filed we are using: \n Zp=')
    f_log.write(str(Zp))

#input one file to share


        
class SecureDatabaseCloud(Frame):
    canvas_width = 1000
    canvas_height =600

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.imagecloud = PhotoImage(file=".\cloud.gif")
        self.l_xs=[] #for each cloud
        self.l_Filshares=[] #for all shares of file and cloud [filelen][alphabetlistlen]
        self.l_transion=[]    # [keylen]
        self.l_NodesharesforC=[] # for shares of Key searching (AA)
        self.initUI()
        self.onChoosebtnrefreshlist()
        self.myinit()
        #for database operations
        
        self.l_Datashares=[] #this for the whole database
        self.l_refreshDatabaseshares=[] #this is to strore refresh database shares.
        ##this is for searching database
               
        self.l_Dtransion=[] #for database. Nodes transition list
        #l_transionsharesforC to hide the pattern
        #[n_clouds][keylen][alphabetlistlen]
        self.l_transionsharesforC=[]#
        self.l_DindexTransition=[] #for database. Index Nodes transition list
        self.l_DrecordTransition=[] #for database. Record Nodes transition list
        
        self.l_DNodesharesforC=[]  #for database. Nodes shares for clouds
        self.l_iDNodesharesforC=[] #this is for index nodes
        self.l_rDNodesharesforC=[] #this is for record nodes

        self.keytosearch=''
        self.findrecord=''  #to take the found record back in the system.
        self.findindex=''
        self.n_LastEmptyKeyNumber=0 #this is used for delete and insert
    def myinit(self):
        self.l_xs=GenR(n_clouds,Zp)
        if IFtest:
            f_log.write('\n')
            f_log.write('x values for each cloud:\n')
            for i in range(n_clouds):
                f_log.write('No.'+str(i)+':'+str(self.l_xs[i].n)+'\n')

        pass
        

    def initUI(self):
      
        self.parent.title("Secuely outsourcing database to open clouds")
        self.config(width=1000,height=600)
        self.pack(fill=BOTH, expand=1)

        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)
        


        w = Canvas(self,bg="#F0E0F0",width=self.canvas_width,
                   height=self.canvas_height)
        #w.place(relx=10, rely=10, anchor=CENTER)
        #self.labelselecloud = Label(self,image=self.imagecloud,\
                           #width=800, height=600)
        #self.labelselecloud.place(x=1, y=1)
        #self.labelselecloud.image=self.imagecloud
        #self.labelselecloud.pack()
        # the cloud picture is here
        w.create_image(47,28, anchor=NW, image=self.imagecloud)

        w.pack()


        
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Open",
                             command=self.onChoosebtnopenfile)
        fileMenu.add_command(label="Exit",
                             command=self.onChoosebtnopenfile)        
        menubar.add_cascade(label="File", menu=fileMenu)
        #-----------------split the screen------------------------

        w.create_line(390, 0, 390, 300, fill="blue", dash=(4, 4),width=2)

        
        w.create_line(250, 300, 250, 600, fill="blue", dash=(4, 4),width=2)

        

        w.create_line(600, 300, 600, 600, fill="blue", dash=(4, 4),width=2)

        

        w.create_line(800, 0, 800, 600, fill="blue", dash=(4, 4),width=2)
        
        w.create_line(0, 300, 800, 300, fill="blue", dash=(4, 4),width=2)
        w.create_line(0, 490, 250, 490, fill="#F0A0F0", dash=(4, 4),width=2)
        
        w.create_line(390, 230, 800, 230, fill="blue", dash=(4, 4),width=2)

        
        w.create_rectangle(1000, 600, 800, 0, fill="#F0A0C0")


        
        #pane = Frame(self)
        #Label(pane, text="Pane Title").pack()

        #w.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))
        #w.create_rectangle(50, 25, 150, 75, fill="blue")

        w.create_text(220, 290, anchor=W, font="Serif",
            text="Load File or database")
        w.create_text(395, 210, anchor=W, font="Serif",
            text="Distibute File or database")
        w.create_text(395, 310, anchor=W, font="Serif",
            text="Manipulating Database")
        
        w.create_text(640, 400, anchor=W, font="Serif",
            text="Alice Loves Bob")
        

        
        w.create_text(130, 310, anchor=W, font="Serif",
            text="Search in Files")

        
        
        #----------open files------------------------------------
        #Here we ask user to select one file to store to clouds.
        self.btn1 = Button(self, text="load file",width=12, height=2,
        command=self.onChoosebtnopenfile)
        self.btn1.place(x=2, y=210)
        
        self.btnloaddata = Button(self, text="Load Database",width=12, height=2,
        command=self.onChoosebtnloaddata)
        self.btnloaddata.place(x=2, y=255)


        
        self.labelfileseleted = Label(self,text="Select a file to send so clouds",
                           width=25, height=1)
        self.labelfileseleted.place(x=100, y=260)


        self.varSendfile= StringVar()
        self.varSendfile.set('')
        self.lblSendfile = Label(self,textvariable=self.varSendfile,width=40, height=2)
        self.lblSendfile.place(x=100, y=220)
        
        #--------------clouds- select---------------
        #here we ask user to select which cloud he will use
        self.lng1 = Checkbutton(self,text = "Cloud 1", variable="ckb1")
        self.lng1.place(x=400, y=30)
        self.lng2 = Checkbutton(self,text = "Cloud 2", variable="ckb2")
        self.lng2.place(x=480, y=30)
        self.lng3 = Checkbutton(self,text = "Cloud 3", variable="ckb3")
        self.lng3.place(x=560, y=30)
        self.lng4 = Checkbutton(self,text = "Cloud 4", variable="ckb4")
        self.lng4.place(x=640, y=30)
        self.lng5 = Checkbutton(self,text = "Cloud 5", variable="ckb5")
        self.lng5.place(x=720, y=30)
        self.lng21 = Checkbutton(self,text = "Cloud 6", variable="ckb6")
        self.lng21.place(x=400, y=60)
        self.lng22 = Checkbutton(self,text = "Cloud 7", variable="ckb7")
        self.lng22.place(x=480, y=60)
        self.lng23 = Checkbutton(self,text = "Cloud 8", variable="ckb8")
        self.lng23.place(x=560, y=60)
        self.lng24 = Checkbutton(self,text = "Cloud 9", variable="ckb9")
        self.lng24.place(x=640, y=60)
        self.lng25 = Checkbutton(self,text = "Cloud 10", variable="ckb10")
        self.lng25.place(x=720, y=60)



        self.labelselecloud = Label(self,text="Distribute the selected files to clouds",
                           width=35, height=2)
        self.labelselecloud.place(x=420, y=100)
        
        self.btnDistibute = Button(self, text="Distributing Files",width=17, height=2,
        command=self.onChoosebtndistributefile)
        self.btnDistibute.place(x=500, y=140)
        self.btnDistibutedata = Button(self, text="Distributing Database",width=17, height=2,
        command=self.onChoosebtnDistibutedata)
        self.btnDistibutedata.place(x=640, y=140)
        

        #progressbar how to define a value
        self.progressbarvalue=10
        self.progress = ttk.Progressbar(self,value=0,length=300,\
                                        variable=self.progressbarvalue)
        self.progress.pack(expand=2, fill=BOTH)
        #self.progress.bind("<Button-1>", self._loop_progress)
        self.progress.place(x=450, y=270)

        self.varinprogress= StringVar()
        self.varinprogress.set('Not working')
        self.labelinprogress = Label(self,textvariable=self.varinprogress,
                           width=40, height=1)
        self.labelinprogress.place(x=450, y=240)
 
        #----Searching area-------------------------
        self.labelInputfile = Label(self,text="file to be searched",
                                     width=15, height=1)
        self.labelInputfile.place(x=15, y=310)
        
        self.listboxfileVariable=StringVar()
        self.listboxfile= Listbox(self,width=15, height=5)
        self.listboxfile.place(x=20, y=340)


        self.labelInputkey = Label(self,text="input a key to search",
                                     width=17, height=1)
        self.labelInputkey.place(x=120, y=340)

        self.entrykeyVariable=StringVar()
        self.txtInputkey = Entry(self,textvariable=self.entrykeyVariable,width=20)
        self.txtInputkey.place(x=120, y=360)

        self.btnrefreshlist = Button(self, text="Refreshlist",width=10, height=2, 
            command=self.onChoosebtnrefreshlist)
        self.btnrefreshlist.place(x=20, y=430)
        
        self.btnsearch = Button(self, text="Search",width=10, height=2, 
            command=self.onChoosebtnsearch)
        self.btnsearch.place(x=140, y=385)
        
        self.btnsearchHPWE = Button(self, text="Search (hide pattern with vector)",width=25, height=2, 
            command=self.onChoosebtnsearchHPWE)
        self.btnsearchHPWE.place(x=10, y=500)

 
        self.btngetresult = Button(self, text="Get Result",width=10, height=2, 
            command=self.onChoosebtngetresult)
        self.btngetresult.place(x=140, y=430)
        
       

   #-------------------data side-------------------------------------


        self.labelInputDatabase = Label(self,text=\
                            "Database to be manipulated",
                                     width=20, height=1)
        self.labelInputDatabase.place(x=290, y=320)
        
        self.listboxDatabaseVariable=StringVar()
        self.listboxDatabase= Listbox(self,width=15, height=5)
        self.listboxDatabase.place(x=290, y=350)


        self.labelInputDatabasekey = Label(self,text="input a key",
                                     width=17, height=1)
        self.labelInputDatabasekey.place(x=290, y=450)

        #self.entrykeyDatabaseVariable=StringVar()
        #self.txtInputDatabasekey = \
               # Entry(self,textvariable=self.entrykeyDatabaseVariable,width=20)
        self.txtInputDatabasekey = \
                Entry(self,width=20)
      
        self.txtInputDatabasekey.place(x=290, y=480)
        

        self.btngetindex = Button(self, text="Get Index",width=8, height=2, 
            command=self.onChoosebtngetindex)
        self.btngetindex.place(x=270, y=520)
        
        self.btngetindexResult = Button(self, text="Result",width=8, height=2, 
            command=self.onChoosebtngetindexResult)
        self.btngetindexResult.place(x=270, y=560)



        self.btngetRecord = Button(self, text="Get Record",width=8, height=2, 
            command=self.onChoosebtngetindex)
        self.btngetRecord .place(x=360, y=520)

        self.btngetRecordResult = Button(self, text="Result",width=8, height=2, 
            command=self.onChoosebtngetindexResult)
        self.btngetRecordResult.place(x=360, y=560)


        
        
        #self.btngetresult = Button(self, text="Append blank Record",width=18, height=2, 
            #command=self.onChoosebtngetresult)
        #self.btngetresult.place(x=450, y=350)
        

        self.btndeleterecord = Button(self, text="Delete  Record",width=15, height=2, 
            command=self.onChoosebtndeleterecord)
        self.btndeleterecord.place(x=450, y=400)
        

        self.labelInputDatabaseRec = Label(self,text="input a record",
                                     width=17, height=1)
        self.labelInputDatabaseRec.place(x=450, y=450)
        
        self.entryRecDatabaseVariable=StringVar()
        self.txtInputDatabaseRec = Entry(self,textvariable=self.entryRecDatabaseVariable,width=20)
        self.txtInputDatabaseRec.place(x=450, y=480)

        self.btnInsertRecord = Button(self, text="Insert  Record",width=15, height=2, 
            command=self.onChoosebtnInsertRecord)
        self.btnInsertRecord.place(x=450, y=350)
        
        self.btnReconstructWholedatabase = Button(self, \
                                                  text="Reconstruct Whole\n Database (for test)",\
                                                  width=20, height=3,
            command=self.onChoosebtnReconstructWholedatabase)
        self.btnReconstructWholedatabase.place(x=440, y=520)


        self.btnclose = Button(self, text="Quit",width=10, height=2,
            command=self.onChoosebtnclose)
        self.btnclose.place(x=650, y=500)

        
        #------------------operation in clouds
        self.labelclouds = Label(self,text="Clouds operation",
                                     width=20, height=2)
        self.labelclouds.place(x=820, y=200)
        
        self.btncloudoperation = Button(self,\
                            text="Cloud Operation (file)",width=20, height=2, 
            command=self.onChoosebtncloudoperation)
        self.btncloudoperation.place(x=820, y=150)

        self.btncloudoperationHPWE = Button(self,\
                            text="Cloud Operation (file)\n(hide pattern with vector)",width=20, height=3, 
            command=self.onChoosebtncloudoperationHPWE)
        self.btncloudoperationHPWE.place(x=820, y=50)




  



  
        self.btncloudoperationdata = Button(self, \
                 text="Cloud Operation (database)",width=20, height=2, 
            command=self.onChoosebtncloudoperationdata)
        self.btncloudoperationdata.place(x=820, y=400)

       
        self.btncloudoperationRefreshdata = Button(self, \
                 text="Refresh database",width=20, height=2, 
            command=self.onChoosebtncloudoperationRefreshdata)
        self.btncloudoperationRefreshdata.place(x=820, y=450)



    def onChoosebtnopenfile(self):
        #open file for sending to clouds      
        ftypes = [('Python files', '*.txt'), ('All files', '*')]
        dlg = tkFileDialog.Open(self, filetypes = ftypes)
        fl = dlg.show()
      
        if fl != '':
            self.varSendfile.set(fl)
            #self.txt.insert(END, text)
            self.update_idletasks()
        f_log.write(self.varSendfile.get())

    def onChoosebtnloaddata(self):
                #open file for sending to clouds      
        ftypes = [('Python files', '*.dat'), ('All files', '*')]
        dlg = tkFileDialog.Open(self, filetypes = ftypes)
        fl = dlg.show()
      
        if fl != '':
            self.varSendfile.set(fl)
            #self.txt.insert(END, text)
            self.update_idletasks()
        f_log.write(self.varSendfile.get())

    def onChoosebtnDistibutedata(self):
        if self.varSendfile.get() == '':
            box.showinfo('Warning', 'No database selected')
            return
        l_xs=self.l_xs #give each value to each cloud
        self.varinprogress.set('Distributing dabatase')
        f_tosearch = open(self.varSendfile.get(), 'r')
        #FiletoBestored=f_tosearch.read()
        


        #DatabasetoBestored=[['Alice','01','it is alice '], \
                            #['Love ','02','it is love  '], \
                            #['Bob  ','03','it is Bob   '],\
                            #['Me   ','04','yes,it is Me'],]
        DatabasetoBestored=pickle.load(f_tosearch)
        f_tosearch.close()
        
        if IFtest:
            f_log.write('\n==========================\nfile stream to be searched:')
            f_log.write('\n')
            f_log.write(str(DatabasetoBestored))
            f_log.write('\n==========================\n')
        #Map File to VectorList
        vector=[]
        #for temporary store vector
        ld_Datashares=[] 
        #for one file in one cloud, one row for one cloud. (for example 10 clouds)
        #in each row, every cell for one alphabet (for example each cell consists of 53 elements)

        #put the file in a list
        
        for x in range(n_clouds):
            ld_Datashares.append(DatabaseShares())
            ld_Datashares[x].n_filelen=len(DatabasetoBestored)
            #print ld_Datashares[x].n_alphabetlistlen 
        print 'Database to Bestored=\n',DatabasetoBestored
        #open files to write in the shares
        pro_step=100.0/len(DatabasetoBestored)        
        if IFtest: f_log.write("\n pro_step"+str(pro_step))
        
        for l_0x in DatabasetoBestored:
            #['Alice', '01', 'it is alice ']
            print l_0x
            self.progress.step(pro_step)
            # Necessary to update the progress bar appearance
            self.update()
            #for key shares.
            for alpha in l_0x[0]:
                #print alpha
                l_y_vectorshares=secretshareAlpha(alpha,n_clouds,1,p,l_xs,Zp);
                for n_xx in range(n_clouds):
                    ld_Datashares[n_xx].l_Keyshares.\
                            append(l_y_vectorshares[n_xx])                              
            #for index shares. it will not be searched
            for s_value in l_0x[1]:
                print s_value
                #here we only need to share the value.
                #we do not need to map it to vectors. we secret share each digit in the value string
                l_shares=secretshare(MapAlphabetToInt(s_value),n_clouds,1,p,l_xs,Zp);
                for n_xx in range(n_clouds):
                    ld_Datashares[n_xx].l_Indexshares.\
                            append(l_shares[n_xx].n)                              
            #for Record shares. it will not be searched.
            for alpha in l_0x[2]:
                #print alpha
                #here we only need to share the value.
                #we do not need to map it to vectors
                #we need to transforn the alpha to a number first
                l_shares=secretshare(MapAlphabetToInt(alpha),n_clouds,1,p,l_xs,Zp);
                for n_xx in range(n_clouds):
                    ld_Datashares[n_xx].l_Recordshares.\
                            append(l_shares[n_xx].n)
        #send database shares out
        self.l_Datashares=ld_Datashares
        
        #save the shares in files
        for i_cloud in range(n_clouds):
            cloudfilename='.\databaseshares\\file.'
            cloudfilename=cloudfilename+GetFilenamefromPath(self.varSendfile.get())
            cloudfilename=cloudfilename+'.cloud'+str(i_cloud)+'.txt'
            c_toSaved = open(cloudfilename, 'w')
            #define a class to save file
            #ld_Datashares[i_cloud].n_xs=l_xs[i_cloud].n
            sharestosave=DatabaseShares()
            sharestosave.n_LastEmptyKeyNumber=0 #it means there is no empty record
            sharestosave.n_xs=self.l_xs[i_cloud].n #for the number or each cloud
            sharestosave.n_alphabetlistlen=len(alphabetlist)
            sharestosave.n_filelen=len(DatabasetoBestored)
            sharestosave.n_Keylen=5
            sharestosave.n_Indexlen=2
            sharestosave.n_Recordlen=12
            sharestosave.l_Keyshares=ld_Datashares[i_cloud].l_Keyshares
            sharestosave.l_Indexshares=ld_Datashares[i_cloud].l_Indexshares
            sharestosave.l_Recordshares=ld_Datashares[i_cloud].l_Recordshares
            
            pickle.dump(sharestosave,c_toSaved) 
            c_toSaved.close()        
        
        if IFtest: 
            f_log.write('\n distribute file ending... \n') 
            f_log.write('\n-------------------------------\n') 


        f_log.write('\n++++++++++++++timer++++++++++++++++++++++++++++++++++++++++\n')
        today = datetime.now()
        Time=today.strftime("%Y%m%d%H hour %M minute %S second")
        f_log.write('\n'+Time+'\n')
        #set the progressbar
        self.varinprogress.set('Finished distributing database!')

        
         #refresh the listbox for 
        self.onChoosebtnrefreshlist()
    def onChoosebtndistributefile(self):
        if self.varSendfile.get() == '':
            box.showinfo('Warning', 'No file selected')
            return
        l_xs=self.l_xs #give each value to each cloud
        self.varinprogress.set('Distributing files')
        #open file for sending to clouds
        #this file is seleted in last operation
        
        f_tosearch = open(self.varSendfile.get(), 'r')
        FiletoBestored='Alice Love Bob Love .'
        FiletoBestored=f_tosearch.read()
        f_tosearch.close()
        if IFtest:
            f_log.write('\n==========================\nfile stream to be searched:')
            f_log.write('\n')
            f_log.write(str(FiletoBestored))
            f_log.write('\n==========================\n')
        #Map File to VectorList
        vector=[]
        #for temporary store vector
        ld_Filshares=[] 
        #for one file in one cloud, one row for one cloud. (for example 10 clouds)
        #in each row, every cell for one alphabet (for example each cell consists of 53 elements)


        if IFtest: 
            f_log.write('\n distribute file Starting... \n') 
            f_log.write('\n-------------------------------\n') 
        f_log.write('\n++++++++++++++timer++++++++++++++++++++++++++++++++++++++++\n')
        today = datetime.now()
        Time=today.strftime("%Y%m%d%H hour %M minute %S second")
        f_log.write('\n'+Time+'\n')

        #put the file in a list

        for x in range(n_clouds):
            ld_Filshares.append([])
        print 'FiletoBestored=',FiletoBestored
        
        #open files to write in the shares
        pro_step=100.0/len(FiletoBestored)

        
        if IFtest: f_log.write("\n pro_step"+str(pro_step))
        for alpha in FiletoBestored:
            #self.progress.value=int(x/300)
            self.progress.step(pro_step)
            # Necessary to update the progress bar appearance
            self.update()
            l_y_vectorshares=secretshareAlpha(alpha,n_clouds,1,p,l_xs,Zp);       
            #l_y_vectorshares is a list [10][53]list
            #send to clouds
            #transfer data in l_y_vectorshares to l_Filshares
            for n_xx in range(n_clouds):
                #print 'n_xx=',n_xx
                #print l_y_vectorshares[n_xx]
                ld_Filshares[n_xx].append(l_y_vectorshares[n_xx])

        #save the shares in files
        for i_cloud in range(n_clouds):
            cloudfilename='.\cloudshares\\file.'
            cloudfilename=cloudfilename+GetFilenamefromPath(self.varSendfile.get())
            cloudfilename=cloudfilename+'.cloud'+str(i_cloud)+'.txt'
            c_toSaved = open(cloudfilename, 'w')
            #define a class to save file
            cfilesharesd=FileShares()
            cfilesharesd.n_xs=l_xs[i_cloud].n
            cfilesharesd.n_filelen=len(ld_Filshares)           
            cfilesharesd.l_Filshares=ld_Filshares[i_cloud]
            #dump the object
            pickle.dump(cfilesharesd,c_toSaved) 
            c_toSaved.close()
        #file are sent to l_Filshares;
        #l_Filshares[x] for cloud x
        if IFtest: 
            f_log.write('\n distribute file ending... \n') 
            f_log.write('\n-------------------------------\n') 


        f_log.write('\n++++++++++++++timer++++++++++++++++++++++++++++++++++++++++\n')
        today = datetime.now()
        Time=today.strftime("%Y%m%d%H hour %M minute %S second")
        f_log.write('\n'+Time+'\n')
        #set the progressbar
        self.varinprogress.set('Finished distributing!')

        


        #refresh the listbox for 
        self.onChoosebtnrefreshlist()

    def onChoosebtngetindex(self):
        n_listselect=self.listboxDatabase.curselection()
        #print n_listselect
        if  len(n_listselect) == 0:
            box.showinfo('Warning', 'No dabase input')
            return
        else:
            pass
            #box.showinfo('Warning', str(n_listselect))
        if self.txtInputDatabasekey.get() == '':
            box.showinfo('Warning', 'No key for database')
            return
        filetosearch=self.listboxDatabase.get(n_listselect)
        keytosearch=self.txtInputDatabasekey.get()
  
        print 'database='+filetosearch+',key='+keytosearch


        #here we need to load the datafile.
        #l_Databaseshares=self.l_Datashares
        self.varinprogress.set('Loading Database....')
        self.update()
        pro_step=100.0/n_clouds

        l_p_xs=[]
        l_database_shares=[]
        #load the database shares from files
        for xx in range(n_clouds):            
            self.progress.step(pro_step)
            self.update()
            cloudDataname='.\databaseshares\\file.'
            cloudDataname=cloudDataname+filetosearch
            cloudDataname=cloudDataname+'.cloud'+str(xx)+'.txt'
            #c_toget='cloud0.txt'
            c_toget = open(cloudDataname, 'r')
            #to store the shares in a class
            o_data= pickle.load(c_toget)
            #print 'o_file.l_Filshares',o_file.l_Filshares
            #here it is numbers, not in Zp
            c_toget.close()
            l_database_shares.append(o_data)
            l_p_xs.append(Zp(o_data.n_xs))
                
        self.varinprogress.set('Loading Database shares...Finished')
        self.update()
        #transfer the  database out 
        self.l_Datashares=l_database_shares
        #Initial values
        n_Keylen=l_database_shares[0].n_Keylen
        n_Indexlen=l_database_shares[0].n_Indexlen
        n_Recordlen=l_database_shares[0].n_Recordlen
        self.n_LastEmptyKeyNumber=l_database_shares[0].n_LastEmptyKeyNumber

        if len(keytosearch)>n_Keylen:
            print "input key is too long!"
            return

        if len(keytosearch)<n_Keylen: #in case the user input a short key
            for i in range(n_Keylen-len(keytosearch)):
                keytosearch=keytosearch+' '
        self.keytosearch=keytosearch     
        #print keytosearch+'0'
        l_xs=l_p_xs
        self.l_xs=l_p_xs
        n_node=len(keytosearch)+1


        if IFtest:
            f_log.write('\n Loading Database shares...Finished\n')
            f_log.write('\n x values for each cloud:\n')
            for i in range(n_clouds):
                f_log.write('No.'+str(i)+':'+str(self.l_xs[i].n)+'\n')
        #Generate automaton and secret share it between n clouds
        #inut one word to search 
        if IFtest: 
            f_log.write('\nGenerate AA for datbase searching now\n')
            f_log.write('\nfile='+filetosearch+'key='+keytosearch)
            f_log.write('\n n_node='+str(n_node))
            f_log.write('\n-------------------------------\n')
        #we need four    
        l_DNode=[]
        l_Dtransion=[]
        l_DindexNode=[] #now we need 2 INDEX nodes
        l_DrecordNode=[] #now we need 12 record nodes
        l_DindexTransition=[] #extra transitions two INDEX nodes
        l_DrecordTransition=[] #extra transitions two INDEX nodes
 
        l_DNodesharesforC=[]
        l_iDNodesharesforC=[] #this is for index Node shares
        l_rDNodesharesforC=[] #this is for index Node shares
                    

        '''
            sharestosave.n_Keylen=5
            sharestosave.n_Indexlen=2
            sharestosave.n_Recordlen=12
        '''

        for i in range(n_node): # make empty AA nodes
            l_DNode.append(Zp(0))

        # set initial value for first node
        l_DNode[0]=Zp(1); #The fist node is always 1
        #make transition below
        for i in range(len(keytosearch)): #make tansition label
            l_Dtransion.append(MapAlphabetToInt(keytosearch[i]))


       
        '''here we are doint database search, so we\
        need another $n_Indexlen$ two nodes'''
        #make eatra nodes and extra index transitions
        for i in range(n_Indexlen):
            l_DindexNode.append(Zp(0))
            #take the last letter of the keytosearch
            l_DindexTransition.append(MapAlphabetToInt(keytosearch[-1]))
        for i in range(n_Recordlen): # make empty Record nodes
            l_DrecordNode.append(Zp(0))            
            #take the last letter of the keytosearch
            l_DrecordTransition.append(MapAlphabetToInt(keytosearch[-1]))
        
        #secret share Nodes
        #each share for x cloud is stored in l_NodesharesforC[x]
        #set initial cell for n_clouds clouds
        for xx in range(n_clouds):
            l_DNodesharesforC.append([])
            l_iDNodesharesforC.append([])
            l_rDNodesharesforC.append([])


        #for each node to do secret sharing
        f_poly1=[]
        f_poly2=[]
        f_poly3=[]
        
        for i in range(n_node): #this is for secret sharing normal nodes
            #(y,n_clouds,1,p,l_xs,Zp)
            (shares,poly)=secretshareRetPoly(l_DNode[i],n_clouds,i+2,p,l_xs,Zp)
            f_poly1.append(poly)
            for xx in range(n_clouds):
                l_DNodesharesforC[xx].append(shares[xx].n)
        for i in range(n_Indexlen): #this is for secret sharing Index nodes
            (shares,poly)=secretshareRetPoly(l_DindexNode[i],n_clouds,n_node+1,p,l_xs,Zp)
            f_poly2.append(poly)
            for xx in range(n_clouds):
                l_iDNodesharesforC[xx].append(shares[xx].n)
        for i in range(n_Recordlen): #this is for secret sharing Record nodes
            (shares,poly)=secretshareRetPoly(l_DrecordNode[i],n_clouds,n_node+1,p,l_xs,Zp)
            f_poly3.append(poly)
            for xx in range(n_clouds):
                l_rDNodesharesforC[xx].append(shares[xx].n)
                

        #set the transition and node shares to global var
        #to transform it into Zp field
        self.l_Dtransion=l_Dtransion
        self.l_DindexTransition=l_DindexTransition
        self.l_DrecordTransition=l_DrecordTransition
        
        self.l_DNodesharesforC=[]
        self.l_iDNodesharesforC=[]
        self.l_rDNodesharesforC=[]
        
        for i in range(n_clouds):
            self.l_DNodesharesforC.append([])
            self.l_iDNodesharesforC.append([])
            self.l_rDNodesharesforC.append([])            
            for ix2 in range(n_node):
                self.l_DNodesharesforC[i].append(Zp(l_DNodesharesforC[i][ix2]))
            for ix3 in range(n_Indexlen):
                self.l_iDNodesharesforC[i].append(Zp(l_iDNodesharesforC[i][ix3]))
            for ix4 in range(n_Recordlen):
                self.l_rDNodesharesforC[i].append(Zp(l_rDNodesharesforC[i][ix4]))

                
           
        #write AA to clouds
        #here we write it to files

        for xx in range(n_clouds):
            
            clouddatabasename='.\AAdatabaseshares\\'
            clouddatabasename=clouddatabasename+'AA.'+filetosearch+'.'+keytosearch
            clouddatabasename=clouddatabasename+'.cloud'+str(xx)+'.txt'
            c_toSave = open(clouddatabasename, 'w')            
            cfileshares=AAdatabaseShares()
            cfileshares.l_DNodesharesforC=l_DNodesharesforC[xx]
            cfileshares.l_iDNodesharesforC=l_iDNodesharesforC[xx]
            cfileshares.l_rDNodesharesforC=l_rDNodesharesforC[xx]
            
            cfileshares.l_Dtransion=l_Dtransion          
            cfileshares.l_DindexTransition=l_DindexTransition  
            cfileshares.l_DrecordTransition=l_DrecordTransition  
           
            #to dump the shares into the file
            pickle.dump(cfileshares,c_toSave) 
            c_toSave.close()        

        if IFtest:
            f_log.write('\n key ='+keytosearch)
            f_log.write('\n-------------------------------------\n')
            f_log.write('self.l_Dtransion=')
            f_log.write(str(self.l_Dtransion))
            f_log.write("\n original AA:N0,N1,N2,N3,N4:\n")
            f_log.write(str(l_DNode))
            f_log.write('\n the polynimial we generate: str(f_poly1[i]\n')
            for i in range(n_node):
                f_log.write(str(f_poly1[i]))
                f_log.write('\n')
            f_log.write('\n-----str(f_poly2[i]-------------------------\n')
            for i in range(n_Indexlen):
                f_log.write(str(f_poly2[i]))
                f_log.write('\n')
        if IFtest: 
            f_log.write('\nGenerate AA ending...\n') 
            f_log.write('---------------------------------------\n')


        #update all the dialog
        self.update()
        #update clouds
        self.onChoosebtncloudoperationdata()
        #reconstruct the result
        self.onChoosebtngetindexResult()

    def LoadFiles(self):
        n_ret=-1
        n_listselect=self.listboxfile.curselection()
        #print n_listselect
        if  len(n_listselect) == 0:
            box.showinfo('Warning', 'No file input')
            return n_ret
        else:
            pass
            #box.showinfo('Warning', str(n_listselect))
   
        
        #find the file  and key
        filetosearch=self.listboxfile.get(n_listselect)
        keytosearch=self.entrykeyVariable.get()
        print 'datafile='+filetosearch

        #here we need to load the datafile.
        #send it to a long list.
        self.varinprogress.set('Loading file shares...')
        self.update()
        pro_step=100.0/n_clouds

        l_s_xs=[]
        l_Filshares=[]
        for xx in range(n_clouds):            
            self.progress.step(pro_step)
            self.update()
            cloudfilename='.\cloudshares\\file.'
            cloudfilename=cloudfilename+filetosearch
            cloudfilename=cloudfilename+'.cloud'+str(xx)+'.txt'
            #c_toget='cloud0.txt'
            c_toget = open(cloudfilename, 'r')
            #to store the shares in a class
            o_file= pickle.load(c_toget)
            #print 'o_file.l_Filshares',o_file.l_Filshares
            #here it is numbers, not in Zp
            c_toget.close()
            l_Filshares.append(o_file.l_Filshares)
            l_s_xs.append(Zp(o_file.n_xs))
            
        self.varinprogress.set('Loading file shares....Finished')
        self.update()  
        #transfer the file out 
        self.l_Filshares=l_Filshares
        self.l_xs=l_s_xs
        l_xs=l_s_xs
        
        n_ret=1
        return n_ret
        
    def onChoosebtnsearchHPWE(self):
        #here we want to search in file
        #here we also want to hide the pattern by mapping Transitions to vectors.
        if self.LoadFiles()!=1:
            return
        if self.entrykeyVariable.get() == '':
            box.showinfo('Warning', 'No key input')
            return
       
        keytosearch=self.entrykeyVariable.get()
        print 'keytosearch='+keytosearch 
        #Get the file out 
        l_Filshares=self.l_Filshares
        l_xs=self.l_xs        
        n_node=len(keytosearch)+1

        #Generate automaton and secret share it between n clouds
        if IFtest: 
            f_log.write('\nGenerate AA now\n')
            f_log.write('\n-------------------------------\n')
            

        l_Node=[]
        #l_transion=[]
        l_transionsharesforC=[] #it will be [n_clouds][keylen][alphabetlistlen]
        l_NodesharesforC=[]
        for i in range(n_node):
            l_Node.append(Zp(0))
        #for i in range(len(keytosearch)):
            #l_transion.append(MapAlphabetToInt(keytosearch[i]))
            
        # set initial value for each node
        l_Node[0]=Zp(1); #The fist node is always 1

        #set initial cell for n_clouds clouds
        for xx in range(n_clouds):
            l_NodesharesforC.append([])
            l_transionsharesforC.append([])
            n_count=-1
            for alpha in keytosearch:
                n_count=n_count+1
                l_transionsharesforC[xx].append([])
            

        #here we need to map and secret share the Transitions
        n_count=-1
        for alpha in keytosearch:
            #each
            #print alpha
            n_count=n_count+1
            l_vectorshares=secretshareAlpha(alpha,n_clouds,1,p,l_xs,Zp);       
            #l_vectorshares is a list [10][63]list
            for n_xx in range(n_clouds):
                #print 'n_xx=',n_xx
                l_transionsharesforC[n_xx][n_count]=l_vectorshares[n_xx]            

        #secret share AA
        #each share for x cloud is stored in l_NodesharesforC[x]
        f_poly=[]
        for i in range(n_node):
            #(y,n_clouds,1,p,l_xs,Zp)
            #(shares,poly)=secretshareRetPoly(l_Node[i],n_clouds,i+2,p,l_xs,Zp)
            (shares,poly)=secretshareRetPoly(l_Node[i],n_clouds,2*i+2,p,l_xs,Zp)
            
            f_poly.append(poly)
            for xx in range(n_clouds):
                l_NodesharesforC[xx].append(shares[xx].n)
             
        #set the transition and node shares to global var
        #because the global var should be in Zp
        #self.l_transion=l_transion
        self.l_transionsharesforC=l_transionsharesforC
        self.l_NodesharesforC=[]
        for i in range(n_clouds):
            self.l_NodesharesforC.append([])
            for ix2 in range(n_node):
                self.l_NodesharesforC[i].append(Zp(l_NodesharesforC[i][ix2]))     

        
        #write AA to clouds---omitted here.
        #print 'l_transionsharesforC',len(l_transionsharesforC),\
              #len(l_transionsharesforC[0]),len(l_transionsharesforC[0][0])
        #print l_transionsharesforC[0][0]
        
        #update all the dialog
        self.update()
        #update clouds
        self.onChoosebtncloudoperationHPWE()
        #reconstruct the result
        self.onChoosebtngetresultHPWE()

        print 'onChoosebtnsearchHPWE Finshed'

    def onChoosebtnsearch(self):
        #here we want to search in file.
        n_listselect=self.listboxfile.curselection()
        #print n_listselect
        if  len(n_listselect) == 0:
            box.showinfo('Warning', 'No file input')
            return
        else:
            pass
            #box.showinfo('Warning', str(n_listselect))
        if self.entrykeyVariable.get() == '':
            box.showinfo('Warning', 'No key input')
            return
        
        #find the file  and key
        filetosearch=self.listboxfile.get(n_listselect)
        keytosearch=self.entrykeyVariable.get()
        print 'datafile='+filetosearch+',key='+keytosearch

        #here we need to load the datafile.
        #send it to a long list.
        self.varinprogress.set('Loading file shares...')
        self.update()
        pro_step=100.0/n_clouds

        l_s_xs=[]
        l_Filshares=[]
        for xx in range(n_clouds):            
            self.progress.step(pro_step)
            self.update()
            cloudfilename='.\cloudshares\\file.'
            cloudfilename=cloudfilename+filetosearch
            cloudfilename=cloudfilename+'.cloud'+str(xx)+'.txt'
            #c_toget='cloud0.txt'
            c_toget = open(cloudfilename, 'r')
            #to store the shares in a class
            o_file= pickle.load(c_toget)
            #print 'o_file.l_Filshares',o_file.l_Filshares
            #here it is numbers, not in Zp
            c_toget.close()
            l_Filshares.append(o_file.l_Filshares)
            l_s_xs.append(Zp(o_file.n_xs))
            
        self.varinprogress.set('Loading file shares....Finished')
        self.update()  
        #transfer the file out 
        self.l_Filshares=l_Filshares
        self.l_xs=l_s_xs
        l_xs=l_s_xs
        n_node=len(keytosearch)+1

        #Generate automaton and secret share it between n clouds
        #inut one word to search 
        #here we give the word "Love"
        if IFtest: 
            f_log.write('\nGenerate AA now\n')
            f_log.write('\nfile='+filetosearch+'key='+keytosearch)
            f_log.write('\n n_node='+str(n_node))
            f_log.write('\n-------------------------------\n')
            

        l_Node=[]
        l_transion=[]
        l_NodesharesforC=[]
        for i in range(n_node):
            l_Node.append(Zp(0))
        for i in range(len(keytosearch)):
            l_transion.append(MapAlphabetToInt(keytosearch[i]))
            
        # set initial value for each node
        l_Node[0]=Zp(1); #The fist node is always 1

        #set initial cell for n_clouds clouds
        for xx in range(n_clouds):
            l_NodesharesforC.append([])

        #secret share AA
        #each share for x cloud is stored in l_NodesharesforC[x]
        f_poly=[]
        for i in range(n_node):
            #(y,n_clouds,1,p,l_xs,Zp)
            (shares,poly)=secretshareRetPoly(l_Node[i],n_clouds,i+2,p,l_xs,Zp)
            f_poly.append(poly)
            for xx in range(n_clouds):
                l_NodesharesforC[xx].append(shares[xx].n)
             
        #set the transition and node shares to global var
        #because the global var should be in Zp
        self.l_transion=l_transion
        self.l_NodesharesforC=[]
        for i in range(n_clouds):
            self.l_NodesharesforC.append([])
            for ix2 in range(n_node):
                self.l_NodesharesforC[i].append(Zp(l_NodesharesforC[i][ix2]))     

        
        #write AA to clouds

        for xx in range(n_clouds):
            
            cloudfilename='.\AAshares\\'
            cloudfilename=cloudfilename+'AA.'+filetosearch+'.'+keytosearch
            cloudfilename=cloudfilename+'.cloud'+str(xx)+'.txt'
            c_toSave = open(cloudfilename, 'w')            
            cfileshares=AAShares()
            cfileshares.l_NodesharesforC=l_NodesharesforC[xx]
            cfileshares.l_transion=l_transion            
            #to dump the shares into the file
            pickle.dump(cfileshares,c_toSave) 
            c_toSave.close()


        #print l_NodesharesforC
        if IFtest:
            f_log.write('\n key ='+keytosearch)
            f_log.write('\n-------------------------------------\n')
            f_log.write('self.l_transion=')
            f_log.write(str(l_transion))
            f_log.write("\n original AA:N0,N1,N2,N3,N4:\n")
            f_log.write(str(l_Node))
            f_log.write('\n the polynimial we generate\n')
            for i in range(n_node):
                f_log.write(str(f_poly[i]))
        if IFtest: 
            f_log.write('\nGenerate AA ending...\n') 
            f_log.write('---------------------------------------\n')

            
        #update all the dialog
        self.update()
        #update clouds
        self.onChoosebtncloudoperation()
        #reconstruct the result
        self.onChoosebtngetresult()

    def onChoosebtncloudoperationRefreshdata(self):
        #it is for refreshing database shares in clouds
        #write back to files again
        n_listselect=self.listboxDatabase.curselection()            
        filetorefresh=self.listboxDatabase.get(n_listselect)
        
        l_reDatashares=self.l_refreshDatabaseshares
        l_Datashares=self.l_Datashares #this for the whole database
        n_fl=self.l_Datashares[0].n_filelen
        n_kl=self.l_Datashares[0].n_Keylen
        n_Il=self.l_Datashares[0].n_Indexlen
        n_Rl=self.l_Datashares[0].n_Recordlen
        #each cloud will update database AA  for theirselves
        self.varinprogress.set('Refresh database now !')        
        pro_step=100.0/n_clouds
        n_ret=1
        for xx in range(n_clouds):
            self.progress.step(pro_step)
            self.update()          
            #for each cloud
            if IFtest: f_log.write('\n refreshing database cloud No.:'+str(xx)+'\n')
            if IFtest: f_log.write('---------------------------------------\n')
            retDataShares=refreshDataCloudshares(l_Datashares[xx],l_reDatashares[xx])
            l_Datashares[xx]=retDataShares
        self.l_Datashares=l_Datashares
        #l_Datashares=l_reDatashares #only for test

        #save the shares in files
        for i_cloud in range(n_clouds):
            cloudfilename='.\databaseshares\\file.'
            cloudfilename=cloudfilename+GetFilenamefromPath(filetorefresh)
            cloudfilename=cloudfilename+'.cloud'+str(i_cloud)+'.txt'
            c_toSaved = open(cloudfilename, 'w')
            #define a class to save file
            #ld_Datashares[i_cloud].n_xs=l_xs[i_cloud].n
            sharestosave=DatabaseShares()
            sharestosave.n_LastEmptyKeyNumber=self.n_LastEmptyKeyNumber #it means there is no empty record
            sharestosave.n_xs=self.l_xs[i_cloud].n #for the number or each cloud
            sharestosave.n_alphabetlistlen=len(alphabetlist)
            sharestosave.n_filelen=n_fl
            sharestosave.n_Keylen=n_kl
            sharestosave.n_Indexlen=n_Il
            sharestosave.n_Recordlen=n_Rl
            sharestosave.l_Keyshares=l_Datashares[i_cloud].l_Keyshares
            sharestosave.l_Indexshares=l_Datashares[i_cloud].l_Indexshares
            sharestosave.l_Recordshares=l_Datashares[i_cloud].l_Recordshares
            
            pickle.dump(sharestosave,c_toSaved) 
            c_toSaved.close()  




        
        self.varinprogress.set('Refresh database finished!')
        
        print 'onChoosebtncloudoperationRefreshdata'

    def onChoosebtncloudoperationdata(self):
        '''         self.l_Dtransion=l_Dtransion
        self.l_DindexTransition=l_DindexTransition
        self.l_DNodesharesforC=[]
        self.l_iDNodesharesforC=[]'''
        if IFtest: 
            f_log.write('\n Updating AA database now')
        l_Datashares=self.l_Datashares #this for the whole database         
        #each cloud will update database AA  for theirselves
        l_Dtransion= self.l_Dtransion
        l_DindexTransition=self.l_DindexTransition
        l_DrecordTransition=self.l_DrecordTransition
        
        l_DNodesharesforC=self.l_DNodesharesforC
        l_iDNodesharesforC=self.l_iDNodesharesforC
        l_rDNodesharesforC=self.l_rDNodesharesforC
        
        self.varinprogress.set('Cloud updating for database!')
        
        if len(l_Dtransion)==0:
            box.showinfo('Yes', 'Click Getindex or GetRecord  button first!')
            return

        n_fl=l_Datashares[0].n_filelen
        n_kl=l_Datashares[0].n_Keylen
        n_Il=l_Datashares[0].n_Indexlen
        n_Rl=l_Datashares[0].n_Recordlen
        SearchKeyLen=len(l_Dtransion)#4 =len('LOVE')    
        #if IFtest:
            #print 'n_fl,n_kl,n_Il,n_Rl,SearchKeyLen=',\
                  #n_fl,n_kl,n_Il,n_Rl,SearchKeyLen
        pro_step=100.0/n_clouds
        n_ret=1
        for xx in range(n_clouds):
            self.progress.step(pro_step)
            self.update()          
            #for each cloud
            if IFtest: f_log.write('\nUpdating database cloud No.:'+str(xx)+'\n')
            if IFtest: f_log.write('---------------------------------------\n')
            n_ret=updateDataCloudshares(l_Datashares[xx],\
                          l_DNodesharesforC[xx],l_iDNodesharesforC[xx],\
                                        l_rDNodesharesforC[xx],\
                          l_Dtransion,l_DindexTransition,l_DrecordTransition)   
            
        self.varinprogress.set('Cloud updating finished (database)')     


    def onChoosebtncloudoperationHPWE(self):
        #todo upate AA in clouds.
        if IFtest: 
            f_log.write('\n Updating AA now for hiding pattern with vectors')
        #each cloud will update AA for theirselves
        lo_Filshares=self.l_Filshares
        #lo_transion=self.l_transion
        lo_transionsharesforC=self.l_transionsharesforC
        lo_NodesharesforC=self.l_NodesharesforC
        
        self.varinprogress.set('Cloud updating!')
        self.update() 
        
        if len(lo_transionsharesforC[0])==0:
            box.showinfo('Yes', 'Click Search button first!')
            return
            
        
        if IFtest:
            FileLen=len(lo_Filshares[0])#
            KeyLen=len(lo_transionsharesforC[0])#4 =len('LOVE')
        # it is 14 for 'Alice Love Bob'
            print 'Keylen, Filelen',KeyLen, FileLen
        pro_step=100.0/n_clouds
        n_ret=1
        for xx in range(n_clouds):
            self.progress.step(pro_step)
            self.update()
            #lo_t_NodesharesforC.append([])
            #for each cloud
            if IFtest: f_log.write('\nUpdating cloud No.:'+str(xx)+'\n')
            if IFtest: f_log.write('---------------------------------------\n')
            n_ret=updateCloudsharesHPWE\
                                   (lo_NodesharesforC[xx],\
                                    lo_Filshares[xx],\
                                    lo_transionsharesforC[xx])
        #self.l_NodesharesforC=lo_NodesharesforC
        self.varinprogress.set('Cloud updating finished')
        if IFtest: 
            f_log.write('\nUpate AA ending...')
            f_log.write('\n--------------------------------------------\n')
            f_log.write('\n++++++++++++++timer++++++++++++++++++++++++++++++++++++++++\n')
            today = datetime.now()
            Time=today.strftime("%Y%m%d%H hour %M minute %S second")
            f_log.write('\n'+Time+'\n')
        
        print 'onChoosebtncloudoperationHPWE finished' 

    def onChoosebtncloudoperation(self):

        #todo upate AA in clouds.
        if IFtest: 
            f_log.write('\n Updating AA now')
        #each cloud will update AA for theirselves
        lo_Filshares=self.l_Filshares
        lo_transion=self.l_transion
        lo_NodesharesforC=self.l_NodesharesforC
        
        self.varinprogress.set('Cloud updating!')
        self.update() 
        
        if len(lo_transion)==0:
            box.showinfo('Yes', 'Click Search button first!')
            return
            
        
        if IFtest:
            FileLen=len(lo_Filshares[0])#
            KeyLen=len(lo_transion)#4 =len('LOVE')
        # it is 14 for 'Alice Love Bob'
            print 'Keylen, Filelen',KeyLen, FileLen
        pro_step=100.0/n_clouds
        n_ret=1
        for xx in range(n_clouds):
            self.progress.step(pro_step)
            self.update()
            #lo_t_NodesharesforC.append([])
            #for each cloud
            if IFtest: f_log.write('\nUpdating cloud No.:'+str(xx)+'\n')
            if IFtest: f_log.write('---------------------------------------\n')
            n_ret=updateCloudshares\
                                   (lo_NodesharesforC[xx],\
                                    lo_Filshares[xx],\
                                    lo_transion)
        #self.l_NodesharesforC=lo_NodesharesforC
        self.varinprogress.set('Cloud updating finished')
        if IFtest: 
            f_log.write('\nUpate AA ending...')
            f_log.write('\n--------------------------------------------\n')
            f_log.write('\n++++++++++++++timer++++++++++++++++++++++++++++++++++++++++\n')
            today = datetime.now()
            Time=today.strftime("%Y%m%d%H hour %M minute %S second")
            f_log.write('\n'+Time+'\n')
        
        print 'AA update finish'    
                
    def onChoosebtnrefreshlist(self):
        self.listboxfile.delete(0, END)
        allsharedfiles=ListFiles(".\cloudshares")
        lisboxcon=[]
        for strx in allsharedfiles:
            strl=strx.split('.')
            lisboxcon.append(strl[1])

        lisboxcon_n=[]
        for x in lisboxcon:
             try:
                 i=lisboxcon_n.index(x)
             except ValueError:
                 lisboxcon_n.append(x)
        
        for item in lisboxcon_n:
            self.listboxfile.insert(END, item)
        self.update()

        self.listboxDatabase.delete(0, END)
        allsharedfiles=ListFiles(".\databaseshares")
        lisboxcon=[]
        for strx in allsharedfiles:
            strl=strx.split('.')
            lisboxcon.append(strl[1])

        lisboxcon_n=[]
        for x in lisboxcon:
             try:
                 i=lisboxcon_n.index(x)
             except ValueError:
                 lisboxcon_n.append(x)
        
        for item in lisboxcon_n:
            self.listboxDatabase.insert(END, item)
        self.update()
        
    def onChoosebtngetindexResult(self):
        #this function reconstruct the search result
        #it is for searching Index and Record at the same time
        if IFtest: 
            f_log.write('\n Reconstruct getindex result. now')
        l_Datashares=self.l_Datashares #this for the whole database         
        l_Dtransion= self.l_Dtransion
        l_DindexTransition=self.l_DindexTransition
        l_DrecordTransition=self.l_DrecordTransition

        l_DNodesharesforC=self.l_DNodesharesforC
        l_iDNodesharesforC=self.l_iDNodesharesforC
        l_rDNodesharesforC=self.l_rDNodesharesforC
        
        self.varinprogress.set('Getindex result for database!')
        self.update() 
        
        if len(l_Dtransion)==0:
            box.showinfo('Yes', 'Click Getindex or GetRecord  button first!')
            return
        KeyLen=len(l_Dtransion)        

        n_indextransition=len(l_DindexTransition)
        n_recordtransition=len(l_DrecordTransition)
        
        l_Node=[]
        l_iNode=[]
        l_rNode=[]
        #n_recordlen=l_Datashares[0].n_Recordlen
        
        n_node=KeyLen+1
        #l_transion=[]
        for i in range(n_node):
            l_Node.append(Zp(0))
        for n_index in range(n_indextransition):
            l_iNode.append(0)
        for n_index in range(n_recordtransition):
            l_rNode.append(0)

            
        for xx in range(n_node):
            lxs=[]
            lys=[]
            #print '--',lxs,lys
            for y in range(xx+4):
                lxs.append(self.l_xs[y]) #l_xs is a global Var for each cloud
                lys.append(l_DNodesharesforC[y][xx])
                #print '===',xx,y,lxs,lys
            f_log.write('\nxx='+str(xx))
            f_log.write('\n lxs=')
            f_log.write(str(lxs))
            f_log.write('\n lys=')
            f_log.write(str(lys))
            #below we Reconstruct the poly
            f_poly=lagran(lxs,lys)
            lenofpoly=len(f_poly)
            actual_poly=[]
            for i in range(lenofpoly-1):
                #print actual_poly
                actual_poly.append(f_poly[lenofpoly-i-2])
                
            #g=f_poly.polynomial(ZZ)

            f_log.write('\nthe reconstructed polynomial:\n')
            f_log.write(str(f_poly))
            f_log.write('\nthe reconstructed polynomial (reverse):\n')
            f_log.write(str(actual_poly))

            if lenofpoly>0:
                #input: order, efficiency, xvlaues,finite fileld
                l_Node[xx]=EvalPolynomial(xx+1,actual_poly,0,Zp)
            else:
                l_Node[xx]=0

        if IFtest:
            f_log.write('\n-------------------------------------')
            f_log.write('\nReconstructed AA:N0,N1,N2,N3,N4\n')
            f_log.write(str(l_Node))


        #for the Index reconstructions
        s_index=[]
        for n_index in range(n_indextransition):
            lxs=[]
            lys=[]
            #print '--',lxs,lys
            for y in range(n_node+4+1):
                lxs.append(self.l_xs[y]) #l_xs is a global Var for each cloud
                lys.append(l_iDNodesharesforC[y][n_index])
                #print '===',xx,y,lxs,lys
            f_log.write('\n  n_index='+str(n_index))
            f_log.write('\n lxs=')
            f_log.write(str(lxs))
            f_log.write('\n lys=')
            f_log.write(str(lys))
            #below we Reconstruct the poly
            f_poly=lagran(lxs,lys)
            lenofpoly=len(f_poly)
            actual_poly=[]
            for i in range(lenofpoly-1):
                #print actual_poly
                actual_poly.append(f_poly[lenofpoly-i-2])

            f_log.write('\nthe reconstructed polynomial:\n')
            f_log.write(str(f_poly))
            f_log.write('\nthe reconstructed polynomial (reverse):\n')
            f_log.write(str(actual_poly))

            if lenofpoly>0:
                #input: order, co-efficiencies, xvlaues,finite fileld
                l_iNode[n_index]=EvalPolynomial(n_node+2,actual_poly,0,Zp).n
            else:
                l_iNode[n_index]=0
        for n_index in range(n_indextransition):
            s_index.append(MapIntToAlphabet(l_iNode[n_index]))
        if IFtest:
            f_log.write('\n-------------------------------------')
            f_log.write('\nReconstructed AA:N0,N1,N2,N3,N4\n')
            f_log.write(str(l_iNode))

        #for the Record reconstructions
        s_record=[]
        for n_record in range(n_recordtransition):
            lxs=[]
            lys=[]
            #print '--',lxs,lys
            for y in range(n_node+4+1):
                lxs.append(self.l_xs[y]) #l_xs is a global Var for each cloud
                lys.append(l_rDNodesharesforC[y][n_record])
                #print '===',xx,y,lxs,lys
            f_log.write('\n  n_record='+str(n_record))
            f_log.write('\n lxs=')
            f_log.write(str(lxs))
            f_log.write('\n lys=')
            f_log.write(str(lys))
            #below we Reconstruct the poly
            f_poly=lagran(lxs,lys)
            lenofpoly=len(f_poly)
            actual_poly=[]
            for i in range(lenofpoly-1):
                #print actual_poly
                actual_poly.append(f_poly[lenofpoly-i-2])

            f_log.write('\nthe reconstructed polynomial:\n')
            f_log.write(str(f_poly))
            f_log.write('\nthe reconstructed polynomial (reverse):\n')
            f_log.write(str(actual_poly))

            if lenofpoly>0:
                #input: order, co-efficiencies, xvlaues,finite fileld
                l_rNode[n_record]=EvalPolynomial(n_node+2,actual_poly,0,Zp).n
            else:
                l_rNode[n_record]=0
        for n_record in range(n_recordtransition):
            s_record.append(MapIntToAlphabet(l_rNode[n_record]))
        if IFtest:
            f_log.write('\n-------------------------------------')
            f_log.write('\nReconstructed Record:\n')
            for n_record in range(n_recordtransition):
                f_log.write(MapIntToAlphabet(l_rNode[n_record]))
            f_log.write('\n-------------------------------------')

            
        #How many mached found.
        #it depends on the last node values.
        n_matches=l_Node[KeyLen]
        s_msbox='The searching key is :['+self.keytosearch
        s_msbox=s_msbox+']\n Matchs=:['+str(n_matches)        
        s_msbox=s_msbox+']\nThe Index is: ['+''.join(s_index)+']\n'
        s_msbox=s_msbox+'The Record is: ['+''.join(s_record)+']\n'
        print s_msbox

        if n_matches==1:
            self.findrecord=''.join(s_record)
            self.findindex=''.join(s_index)
        else:
            self.findrecord=''
            self.findindex=''        
        self.varinprogress.set('Getindex result for database....finished')
        self.update()             

        if IFtest: 
            f_log.write('\nReconstruct AA ending.(database)')
            f_log.write('\n-------------------------------------')
        
        print 'onChoosebtngetindexResult Finshed'
    def onChoosebtngetRecordResult(self):
        if IFtest: 
            f_log.write('\n Reconstruct Getrecordresult now')
        
        print 'onChoosebtngetRecordResult Finshed'

    def onChoosebtngetresultHPWE(self):

        #todo Reconstruct AA for hiding pattern
        if IFtest: 
            f_log.write('\n Reconstruct AA now for hiding pattern')
        #From shares got from clouds 
        #which are stored in list l_NodesharesforC
        lg_transionsharesforC= self.l_transionsharesforC
        if len(lg_transionsharesforC)==0:
            box.showinfo('Yes', 'Click Search button first!')
            return
        lg_NodesharesforC=self.l_NodesharesforC
        KeyLen=len(lg_transionsharesforC[0])
        
        l_Node=[]
        n_node=KeyLen+1
        #l_transion=[]
        for i in range(n_node):
            l_Node.append(Zp(0))

        for xx in range(n_node):
            lxs=[]
            lys=[]
            #print '--',lxs,lys
            for y in range(2*xx+4):
                lxs.append(self.l_xs[y]) #l_xs is a global Var for each cloud
                lys.append(lg_NodesharesforC[y][xx])
                #print '===',xx,y,lxs,lys
            f_log.write('\nxx='+str(xx))
            f_log.write('\n lxs=')
            f_log.write(str(lxs))
            f_log.write('\n lys=')
            f_log.write(str(lys))
            #below we Reconstruct the poly
            f_poly=lagran(lxs,lys)
            lenofpoly=len(f_poly)
            actual_poly=[]
            for i in range(lenofpoly-1):
                #print actual_poly
                actual_poly.append(f_poly[lenofpoly-i-2])
                
            #g=f_poly.polynomial(ZZ)

            f_log.write('\nthe reconstructed polynomial:\n')
            f_log.write(str(f_poly))
            f_log.write('\nthe reconstructed polynomial (reverse):\n')
            f_log.write(str(actual_poly))

            if lenofpoly>0:
                #input: order, efficiency, xvlaues,finite fileld
                l_Node[xx]=EvalPolynomial(xx+1,actual_poly,0,Zp)
            else:
                l_Node[xx]=0
            
           

        #How many mached found.
        #it depends on the last node values.
        n_matches=l_Node[KeyLen]
        box.showinfo('Yes', 'Totally: '+str(n_matches)+' matches found!\n \
                   We are also hiding pattern!')
        


        if IFtest:
            f_log.write('\n-------------------------------------')
            f_log.write('\nReconstructed AA:N0,N1,N2,N3,N4\n')
            f_log.write(str(l_Node))
        if IFtest: 
            f_log.write('\nReconstruct AA ending...')
            f_log.write('\n-------------------------------------')



        print 'onChoosebtngetresultHPWE Finshed'



    def onChoosebtngetresult(self):

        #todo Reconstruct AA
        if IFtest: 
            f_log.write('\n Reconstruct AA now')
        #From shares got from clouds 
        #which are stored in list l_NodesharesforC
        lg_transion=self.l_transion
        if len(lg_transion)==0:
            box.showinfo('Yes', 'Click Search button first!')
            return
        lg_NodesharesforC=self.l_NodesharesforC
        KeyLen=len(lg_transion)
        
        l_Node=[]
        n_node=KeyLen+1
        #l_transion=[]
        for i in range(n_node):
            l_Node.append(Zp(0))

        for xx in range(n_node):
            lxs=[]
            lys=[]
            #print '--',lxs,lys
            for y in range(xx+4):
                lxs.append(self.l_xs[y]) #l_xs is a global Var for each cloud
                lys.append(lg_NodesharesforC[y][xx])
                #print '===',xx,y,lxs,lys
            f_log.write('\nxx='+str(xx))
            f_log.write('\n lxs=')
            f_log.write(str(lxs))
            f_log.write('\n lys=')
            f_log.write(str(lys))
            #below we Reconstruct the poly
            f_poly=lagran(lxs,lys)
            lenofpoly=len(f_poly)
            actual_poly=[]
            for i in range(lenofpoly-1):
                #print actual_poly
                actual_poly.append(f_poly[lenofpoly-i-2])
                
            #g=f_poly.polynomial(ZZ)

            f_log.write('\nthe reconstructed polynomial:\n')
            f_log.write(str(f_poly))
            f_log.write('\nthe reconstructed polynomial (reverse):\n')
            f_log.write(str(actual_poly))

            if lenofpoly>0:
                #input: order, efficiency, xvlaues,finite fileld
                l_Node[xx]=EvalPolynomial(xx+1,actual_poly,0,Zp)
            else:
                l_Node[xx]=0
            
           

        #How many mached found.
        #it depends on the last node values.
        n_matches=l_Node[KeyLen]
        box.showinfo('Yes', 'Totally: '+str(n_matches)+' matches found!')
        


        if IFtest:
            f_log.write('\n-------------------------------------')
            f_log.write('\nReconstructed AA:N0,N1,N2,N3,N4\n')
            f_log.write(str(l_Node))
        if IFtest: 
            f_log.write('\nReconstruct AA ending...')
            f_log.write('\n-------------------------------------')



        print 'onChoosebtngetresult Finshed'

    def onChoosebtnclose(self):
        f_log.write('\n--------closed----------------\n')
        f_log.close()
        self.parent.destroy()
##        if box.askyesno('Verify', 'Really quit?'):
##            f_log.close()
##            self.parent.destroy()
##        else:
##            pass
        #box.askquestion("Question", "Are you sure to quit?")

    def onChoosebtndeleterecord(self):
        #First find the key. take, Index and record back.
        #get the point back
        #then create an empty database, put the point - key in the right place
        #leave the Index. change Record to 0s.
        #refresh the database in the cloud.
        
        self.onChoosebtngetindex()
        n_fl=self.l_Datashares[0].n_filelen
        n_kl=self.l_Datashares[0].n_Keylen
        n_Il=self.l_Datashares[0].n_Indexlen
        n_Rl=self.l_Datashares[0].n_Recordlen
        #the key and record if found.
        s_findrecord=self.findrecord
        s_findindex=self.findindex
        if len(s_findindex)<1:
            box.showinfo('Yes', 'Can not delete empty key!')
            return
        n_findindex=int(s_findindex)
        s_keytosearch=self.keytosearch

        #take the +count back from cloud
        n_LEKN=self.l_Datashares[0].n_LastEmptyKeyNumber
        s_LEKN=str(n_LEKN)
        if len(s_LEKN)<(n_kl-1): #in case the user input a short key
            for i in range(n_kl-1-len(s_LEKN)):
                s_LEKN='0'+s_LEKN
        s_LEKN='+'+s_LEKN
        #print s_LEKN  
           
        #create a database with all 0s
        l_data=createallzerodatabase(n_fl,n_kl,n_Il,n_Rl)
        #print l_data

        self.varinprogress.set('Delete record...')
        self.update()
        l_xs=self.l_xs #give each value to each cloud
        ld_Datashares=[] 
        for x in range(n_clouds):
            ld_Datashares.append(DatabaseShares())
            ld_Datashares[x].n_filelen=len(l_data)
        pro_step=100.0/len(l_data)
        c_count=0
        for l_0x in l_data:
            c_count=c_count+1            
            #print l_0x
            self.progress.step(pro_step)
            self.update()
            #for key shares.
            n_num=-1
            for alpha in l_0x[0]:
                n_num=n_num+1
                if c_count != n_findindex:
                    l_y_vectorshares=secretshareAlpha(alpha,n_clouds,1,p,l_xs,Zp)
                else:
                    letterNk=s_LEKN[n_num]
                    letterDe=s_keytosearch[n_num]
                    #find -beta
                    #print n_num
                    #print letterNk
                    #print letterDe                    
                    l_y_vectorshares=secretshareAlphaToBeta(letterDe,letterNk,n_clouds,1,p,l_xs,Zp)                    
                for n_xx in range(n_clouds):
                    ld_Datashares[n_xx].l_Keyshares.\
                            append(l_y_vectorshares[n_xx])                              
            #for index shares. it will not be searched
            for s_value in l_0x[1]:
                l_shares=secretshare(MapAlphabetToInt(s_value),n_clouds,1,p,l_xs,Zp);
                for n_xx in range(n_clouds):
                    ld_Datashares[n_xx].l_Indexshares.\
                            append(l_shares[n_xx].n)                              
            #for Record shares. it will not be searched.
            n_num=-1
            for alpha in l_0x[2]:
                n_num=n_num+1
                if c_count != n_findindex:
                    l_shares=secretshare(MapAlphabetToInt(alpha),n_clouds,1,p,l_xs,Zp);
                else:
                    n_tem=MapAlphabetToInt(s_findrecord[n_num])
                    l_shares=secretshare(p-n_tem,n_clouds,1,p,l_xs,Zp);
                  
                for n_xx in range(n_clouds):
                    ld_Datashares[n_xx].l_Recordshares.\
                            append(l_shares[n_xx].n)
        self.l_refreshDatabaseshares=ld_Datashares            
        #update in each cloud to refresh the cloud data
        self.n_LastEmptyKeyNumber=self.n_LastEmptyKeyNumber+1

        #refresh database
        self.onChoosebtncloudoperationRefreshdata()



        self.varinprogress.set('Delete record....finished')
        self.update()  

    def onChoosebtnReconstructWholedatabase(self):
        n_listselect=self.listboxDatabase.curselection()
        #print n_listselect
        if  len(n_listselect) == 0:
            box.showinfo('Warning', 'No dabase input')
            return
        else:
            pass       
        if IFtest: 
            f_log.write('\n Reconstruct the whole datbase (for test). now')
        l_Datashares=self.l_Datashares #this for the whole database
        self.varinprogress.set('Reconstruct the whole datbase (for test)..')
        self.update() 

        filetosearch=self.listboxDatabase.get(n_listselect)

  
        print 'database to be reconstructed='+filetosearch


        #here we need to load the datafile.
        #l_Databaseshares=self.l_Datashares
        self.varinprogress.set('Loading Database....')
        self.update()
        pro_step=100.0/n_clouds

        l_p_xs=[]
        l_database_shares=[]
        #load the database shares from files
        for xx in range(n_clouds):            
            self.progress.step(pro_step)
            self.update()
            cloudDataname='.\databaseshares\\file.'
            cloudDataname=cloudDataname+filetosearch
            cloudDataname=cloudDataname+'.cloud'+str(xx)+'.txt'
            #c_toget='cloud0.txt'
            c_toget = open(cloudDataname, 'r')
            #to store the shares in a class
            o_data= pickle.load(c_toget)
            #print 'o_file.l_Filshares',o_file.l_Filshares
            #here it is numbers, not in Zp
            c_toget.close()
            l_database_shares.append(o_data)
            l_p_xs.append(Zp(o_data.n_xs))
                
        self.varinprogress.set('Loading Database shares...Finished')
        self.update()
        #transfer the  database out 

        n_alphabetlistlen=l_database_shares[0].n_alphabetlistlen
        n_fl=l_database_shares[0].n_filelen
        n_kl=l_database_shares[0].n_Keylen
        n_Il=l_database_shares[0].n_Indexlen
        n_Rl=l_database_shares[0].n_Recordlen

           
       
        lxs=[]
        lxs.append(l_p_xs[0])
        lxs.append(l_p_xs[1])
        lxs.append(l_p_xs[2])
        
        #create a database with all 0s
        l_data=createallzerodatabase(n_fl,n_kl,n_Il,n_Rl)
        pro_step=100.0/n_fl        
        for i in range(n_fl):
            self.progress.step(pro_step)
            self.update()
            s_key=''
            for i_x in range(n_kl):
                l_rconstrucVector=[]
                for i_kx in range(n_alphabetlistlen):#each get one element of the vetor
                    lys=[]
                    lys.append(l_database_shares[0].l_Keyshares[i*n_kl+i_x][i_kx])
                    lys.append(l_database_shares[1].l_Keyshares[i*n_kl+i_x][i_kx])
                    lys.append(l_database_shares[2].l_Keyshares[i*n_kl+i_x][i_kx])
                    f_poly=lagran(lxs,lys)
                    lenofpoly=len(f_poly)
                    actual_poly=[]
                    for i_kkx in range(lenofpoly-1):
                        #print actual_poly
                        actual_poly.append(f_poly[lenofpoly-i_kkx-2])                    
                    l_rconstrucVector.append(EvalPolynomial(1,actual_poly,0,Zp))
                #make the string
                try:
                    n_num=l_rconstrucVector.index(1)
                except ValueError:
                    n_num=0
                s_key=s_key+MapIntToAlphabet(n_num)        
            #whloe vector achieve one alphabet!
            #print s_key
            l_data[i][0]=s_key
        #for i in range(n_fl):
            s_index=''
            for i_x in range(n_Il):
                lys=[]
                lys.append(l_database_shares[0].l_Indexshares[i*n_Il+i_x])
                lys.append(l_database_shares[1].l_Indexshares[i*n_Il+i_x])
                lys.append(l_database_shares[2].l_Indexshares[i*n_Il+i_x])
                f_poly=lagran(lxs,lys)
                lenofpoly=len(f_poly)
                actual_poly=[]
                for j in range(lenofpoly-1):
                    #print actual_poly
                    actual_poly.append(f_poly[lenofpoly-j-2])                    
                n_num=EvalPolynomial(1,actual_poly,0,Zp)
                #print n_num,i,i_x
                s_index=s_index+MapIntToAlphabet(n_num) 
            #print s_index
            l_data[i][1]= s_index          
        #for i in range(n_fl):
            s_record=''
            for i_x in range(n_Rl):
                lys=[]
                lys.append(l_database_shares[0].l_Recordshares[i*n_Rl+i_x])
                lys.append(l_database_shares[1].l_Recordshares[i*n_Rl+i_x])
                lys.append(l_database_shares[2].l_Recordshares[i*n_Rl+i_x])
                f_poly=lagran(lxs,lys)
                lenofpoly=len(f_poly)
                actual_poly=[]
                for j in range(lenofpoly-1):
                    #print actual_poly
                    actual_poly.append(f_poly[lenofpoly-j-2])                    
                n_num=EvalPolynomial(1,actual_poly,0,Zp)
                s_record=s_record+MapIntToAlphabet(n_num) 
            #print s_record
            l_data[i][2]= s_record 
        print 'the reconstructed database'
        print l_data
        
        self.varinprogress.set('Reconstructed database...Finished')        
        self.update()
        
       # box.showinfo('Yes', 'test')

    def onChoosebtnInsertRecord(self):
        n_listselect=self.listboxDatabase.curselection()
        #print n_listselect
        if  len(n_listselect) == 0:
            box.showinfo('Warning', 'No dabase input')
            return
        else:
            pass
            #box.showinfo('Warning', str(n_listselect))
        if self.txtInputDatabasekey.get() == '':
            box.showinfo('Warning', 'No key for database')
            return
        if self.entryRecDatabaseVariable.get() == '':
            box.showinfo('Warning', 'No key for database')
            return
        #to check whether there is same key or not.
        self.onChoosebtngetindex()
        
        s_findrecord=self.findrecord 
        s_findindex=self.findindex
        
        if len(s_findindex)>1:
            box.showinfo('Yes', 'Key is not unique!')
            return
        n_fl=self.l_Datashares[0].n_filelen
        n_kl=self.l_Datashares[0].n_Keylen
        n_Il=self.l_Datashares[0].n_Indexlen
        n_Rl=self.l_Datashares[0].n_Recordlen

        filetoinsert=self.listboxDatabase.get(n_listselect)
        keytoinsert=self.txtInputDatabasekey.get()
        recordtoinsert=self.entryRecDatabaseVariable.get()

        if len(keytoinsert)<n_kl: #in case the user input a short key
            for i in range(n_kl-len(keytoinsert)):
                keytoinsert=keytoinsert+' '
        if len(recordtoinsert)<n_Rl: #in case the user input a short key
            for i in range(n_Rl-len(recordtoinsert)):
                recordtoinsert=recordtoinsert+' '
                

        #take the $count back from cloud
        n_LEKN=self.l_Datashares[0].n_LastEmptyKeyNumber-1
        s_LEKN=str(n_LEKN)
        if len(s_LEKN)<(n_kl-1): #in case the user input a short key
            for i in range(n_kl-1-len(s_LEKN)):
                s_LEKN='0'+s_LEKN
        s_LEKN='+'+s_LEKN
        #print s_LEKN  
           

        
        print 'database=['+filetoinsert+']'
        print 'keytoinsert=['+keytoinsert+']'
        print 'recordtoinsert=['+recordtoinsert+']'
        self.txtInputDatabasekey.delete(0,END)

        self.txtInputDatabasekey.insert(END,s_LEKN)

        #to find the index place
        self.onChoosebtngetindex()

        #the result is below. to change it to new record
        s_findrecord=self.findrecord 
        s_findindex=self.findindex
        n_findindex=int(s_findindex)

        #create a database with all 0s
        l_data=createallzerodatabase(n_fl,n_kl,n_Il,n_Rl)
        #print l_data
                
        self.varinprogress.set('insert record...')
        self.update()
        l_xs=self.l_xs #give each value to each cloud
        ld_Datashares=[] 
        for x in range(n_clouds):
            ld_Datashares.append(DatabaseShares())
            ld_Datashares[x].n_filelen=len(l_data)
        pro_step=100.0/len(l_data)
        c_count=0
        for l_0x in l_data:
            c_count=c_count+1            
            #print l_0x
            self.progress.step(pro_step)
            self.update()
            #for key shares.
            n_num=-1
            for alpha in l_0x[0]:
                n_num=n_num+1
                if c_count != n_findindex:
                    l_y_vectorshares=secretshareAlpha(alpha,n_clouds,1,p,l_xs,Zp)
                else:
                    letterDe=s_LEKN[n_num]
                    letterNk=keytoinsert[n_num]
                    #find -beta
                    #print n_num
                    #print letterNk
                    #print letterDe                    
                    l_y_vectorshares=secretshareAlphaToBeta(letterDe,letterNk,n_clouds,1,p,l_xs,Zp)                    
                for n_xx in range(n_clouds):
                    ld_Datashares[n_xx].l_Keyshares.\
                            append(l_y_vectorshares[n_xx])                              
            #for index shares. it will not be searched
            for s_value in l_0x[1]:
                l_shares=secretshare(MapAlphabetToInt(s_value),n_clouds,1,p,l_xs,Zp);
                for n_xx in range(n_clouds):
                    ld_Datashares[n_xx].l_Indexshares.\
                            append(l_shares[n_xx].n)                              
            #for Record shares. it will not be searched.
            n_num=-1
            for alpha in l_0x[2]:
                n_num=n_num+1
                if c_count != n_findindex:
                    l_shares=secretshare(MapAlphabetToInt(alpha),n_clouds,1,p,l_xs,Zp);
                else:
                    n_tem=MapAlphabetToInt(recordtoinsert[n_num])
                    l_shares=secretshare(n_tem,n_clouds,1,p,l_xs,Zp);
                  
                for n_xx in range(n_clouds):
                    ld_Datashares[n_xx].l_Recordshares.\
                            append(l_shares[n_xx].n)
        self.l_refreshDatabaseshares=ld_Datashares            
        #update in each cloud to refresh the cloud data
        self.n_LastEmptyKeyNumber=self.n_LastEmptyKeyNumber-1

        #refresh database
        self.onChoosebtncloudoperationRefreshdata()



        self.varinprogress.set('Insert record....finished')
        self.update()  

     
    def onChoosebtntest(self):
        #Botton test
        self.update()
        box.showinfo('Yes', 'test')

        
    def _loop_progress(self, *args):
        self.update()

def main():
  
    root = Tk()
    ex =  SecureDatabaseCloud(root)
    root.geometry("1000x600+20+20")
    root.mainloop()  


if __name__ == '__main__':
    main() 
