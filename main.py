from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import json
import os

import tkinter as tk
from serialComm import *

from inputCheck import *

TITLE_FONT= ("Arial", 20)
LARGE_FONT= ("Arial", 15)
SMALL_FONT= ("Arial", 12)

class MainDCM(tk.Tk):
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self,width=650, height=650, relief='raised', borderwidth=10) #initialize a 650 x 650 frame

        container.pack(side="top", fill="both", expand = False)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid_propagate(0)

        self.frames = {}

        #initialize a Tkinter frame from each module given below
        for F in (HomePage, LogIn, ModeAOO, ModeVOO, ModeAAI, ModeVVI, ModeDOO, ModeAOOR, ModeVOOR, ModeAAIR, ModeVVIR, ModeDOOR):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            frame.grid_propagate(0)
        
        self.show_frame(LogIn)

    def show_frame(self, cont):
        #show the currently selected frame
        frame = self.frames[cont]
        frame.tkraise()

class LogIn(tk.Frame):

    currentUser = '' #username of the currently logged in user('' on start)
    dbFile = 'data.txt' #where json data is being stored
    tempUserObject = {}

    def __init__(self, parent, controller):
        #initialize widgets on LogIn screen
        
        global usernameInput
        global pwInput
        self.controller = controller

        tk.Frame.__init__(self, parent)

        logLabel = ttk.Label(self, text = "Login With Your Username and Password", font = LARGE_FONT)
        logLabel.pack(side = TOP, anchor = N, expand = YES, pady=(50,0))

        userLabel = Label(self, text = 'Username')
        userLabel.pack(side = TOP, anchor = N, pady=(0,10))
        usernameInput = Entry(self)
        usernameInput.pack(side = TOP, pady=(0,30))

        pwLabel = Label(self, text = 'Password')
        pwLabel.pack(side = TOP, anchor = N, pady = (0,10))
        pwInput = Entry(self, show="*")
        pwInput.pack(side = TOP, pady=(0,30))

         #runs the 'LoginCheck' function
        logInButton = tk.Button(self, text = "Login",
                                 command = self.LogInCheck)
        logInButton.pack(side = TOP, anchor = S, pady=(0,10))

        #runs the 'registerUser' function
        registerButton = tk.Button(self, text="Register",
                                    command = self.registerUser)
        registerButton.pack(side=TOP, anchor = S, pady=(0,200))

    def LogInCheck(self):
        userInDB = False 
        
        #retrieve inputted username and password fields
        tempUsername = usernameInput.get()
        tempPw = pwInput.get()
        
        with open(LogIn.dbFile, 'r') as json_file:
            if (not os.path.getsize(LogIn.dbFile)):
                #if json file is blank, initialize JSON data
               data = {
                   'users':[]
               }
            else: 
                data = json.load(json_file)
                
            if (data['users']): #traverse list if not empty
                for user in data['users']:
                    #find matching entry in db
                    if tempUsername == user['username'] and tempPw == user['password']:
                        userInDB = True
                        LogIn.currentUser = tempUsername
                        LogIn.tempUserObject = user
                        self.controller.show_frame(HomePage)
                        break
    
        if (not userInDB): 
            messagebox.showerror('Error', 'Incorrect username or password.')

    def registerUser(self):
        MAX_NUM_USERS = 10
        
        tempUsername = usernameInput.get()
        tempPw = pwInput.get()

        userList = []
        userInDB = False

        with open(LogIn.dbFile,'r') as json_file:
            if (not os.path.getsize(LogIn.dbFile)):
                #if json file is blank, initialize JSON data
               data = {
                   'users':[]
               }
            else: 
                data = json.load(json_file)

            userList = data['users']

            for user in data['users']:
                if tempUsername == user['username']:
                    userInDB = True #set true if user already exists
                    break
            
            count = len(data['users']) #number of users currently stored
            userList = data['users']

        if (userInDB):
            messagebox.showerror('Error', 'This user already exists!')
        elif (count >= MAX_NUM_USERS):
            messagebox.showerror('Error','The number of users in the system has reached its maximum capacity.')
        elif (tempUsername == '' or tempPw == ''):
            messagebox.showerror('Error','The username and password fields cannot be blank.')
        else:
            userList.append({ #add user to db file
                "username": tempUsername,
                "password": tempPw,
                "Mode": '',         # current mode being operated
                "LRL": "0",         # Lower Rate Limit
                "URL": "0",         # Upper Rate Limit
                "MSR": "0",         # Maximum Sensor Rate
                "FAVD": "0",        # Fixed AV Delay
                "AA": "0",          # Atrial Amplitude
                "VA": "0",          # Ventricular Amplitude
                "APW": "0",         # Atrial Pulse Width
                "VPW": "0",         # Ventricular Pulse Width
                "ARP": "0",         # Atrial Refractory Period
                "VRP": "0",         # Ventricular Refractory Period
                "AT": "0",          # Activity Threshold
                "ReactTime": "0",   # Reaction Time
                "RF": "0",          # Response Factor
                "RecovTime": "0"    # Recovery Time
            })
            data['users'] = userList

            with open(LogIn.dbFile, 'w') as outfile:
                json.dump(data, outfile)

            messagebox.showinfo('Success', 'User has been registered.')
            self.controller.show_frame(LogIn)

class HomePage(tk.Frame):
    PACEMAKER_DEVICE = '' #holds value for currently connected pacemaker device
    def __init__(self, parent, controller):
        #initialize widgets
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="DCM Homepage", font=TITLE_FONT)
        label.pack(pady=(20,20),padx=10)
        
        button = tk.Button(self, text="AOO Mode",
                            command=lambda: controller.show_frame(ModeAOO))
        button.pack(pady=(30,10))

        button2 = tk.Button(self, text="VOO Mode",
                            command=lambda: controller.show_frame(ModeVOO))
        button2.pack(pady=(10,10))

        button3 = tk.Button(self, text="AAI Mode",
                            command=lambda: controller.show_frame(ModeAAI))
        button3.pack(pady=(10,10))

        button4 = tk.Button(self, text="VVI Mode",
                           command=lambda: controller.show_frame(ModeVVI))
        button4.pack(pady=(10,10))

        button5 = tk.Button(self, text="DOO Mode",
                            command=lambda: controller.show_frame(ModeDOO))
        button5.pack(pady=(10,10))

        button6 = tk.Button(self, text="AOOR Mode",
                            command=lambda: controller.show_frame(ModeAOOR))
        button6.pack(pady=(10,10))

        button7 = tk.Button(self, text="VOOR Mode",
                            command=lambda: controller.show_frame(ModeVOOR))
        button7.pack(pady=(10,10))

        button8 = tk.Button(self, text="AAIR Mode",
                            command=lambda: controller.show_frame(ModeAAIR))
        button8.pack(pady=(10,10))

        button9 = tk.Button(self, text="VVIR Mode",
                            command=lambda: controller.show_frame(ModeVVIR))
        button9.pack(pady=(10,10))

        button10 = tk.Button(self, text="DOOR Mode",
                            command=lambda: controller.show_frame(ModeDOOR))
        button10.pack(pady=(10,10))
    
    def pacemakerStatus(self):
        #provide visual cue if connected pacemaker device is different from currently stored
        if (not checkPacemakerDevice()):
            messagebox.showerror('Error', 'Connection with pacemaker device could not be established')
        else:
            messagebox.showinfo('Update', 'Pacemaker device has been changed.')


class ModeAOO(tk.Frame):
    def __init__(self, parent, controller):
        #initialize widgets
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="AOO Mode", font="LARGE_FONT")
        label.grid(pady=20, padx=(300,0), row = 1, column = 2)

        self.LRL_entry = tk.StringVar()
        ttk.Label(self, text="Lower Rate Limit | 30-175 ppm").grid(row = 3, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.LRL_entry).grid(row = 3, column = 3, pady=(20,0), padx=(0,10))

        self.URL_entry = tk.StringVar()
        ttk.Label(self, text="Upper Rate Limit | 50-175 ppm").grid(row = 4, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.URL_entry).grid(row = 4, column = 3, pady=(20,0), padx=(0,10))

        self.AA_entry = tk.StringVar()
        ttk.Label(self, text="Atrial Amplitude | 0, 0.5-3.2V, 3.5-7.0 V").grid(row = 5, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.AA_entry).grid(row = 5, column = 3, pady=(20,0), padx=(0,10))

        self.APW_entry = tk.StringVar()
        ttk.Label(self, text="Atrial Pulse Width | 0.05 ns, 0.1-1.9 ms").grid(row = 6, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.APW_entry).grid(row = 6, column = 3, pady=(20,0), padx=(0,10))

        backButton = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage))
        backButton.grid(row = 7, column = 2,  pady=(100,20), padx=(10,10))

        setValuesBtn = ttk.Button(self, text="Set Values",
                            command=self.setValues)
        setValuesBtn.grid(row = 7, column = 3,  pady=(100,20), padx=(10,10))

    def setValues(self):
        userList = []
        correctVals = False

        with open(LogIn.dbFile) as json_file:
            data = json.load(json_file)
            userList = data['users']

        for user in userList:
            if (user['username'] == LogIn.currentUser):
                if (
                    checkLRL(self.LRL_entry.get()) and
                    checkURL(self.URL_entry.get()) and
                    checkAmp(self.AA_entry.get()) and
                    checkPW(self.APW_entry.get()) #check valid nums are entered
                ):
                    user['LRL'] = self.LRL_entry.get() 
                    user['URL'] = self.URL_entry.get()
                    user['AA'] = self.AA_entry.get()
                    user['APW'] = self.APW_entry.get()
                    user['Mode'] = 'AOO'
                    correctVals = True

                else:
                    messagebox.showerror('Error', 'Try again. Please enter a valid input that is within the specified range.')
                    break

                data['users'] = userList
                with open(LogIn.dbFile,'w') as outfile:
                    json.dump(data,outfile)
                
                with open(LogIn.dbFile) as json_file:
                    data = json.load(json_file)
                    userList = data['users']

                    for user in userList:
                        if (user['username'] == LogIn.currentUser and correctVals):
                            sendSerialInfo(33, LogIn.tempUserObject)
                            break
                
                messagebox.showinfo('Success', 'Successfully added values.')
                break
        
class ModeVOO(tk.Frame):
    def __init__(self, parent, controller):
        #initialize widgets

        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="VOO Mode", font="LARGE_FONT")
        label.grid(pady=20, padx=(300,0), row = 1, column = 2)

        self.LRL_entry = tk.StringVar()
        ttk.Label(self, text="Lower Rate Limit | 30-175 ppm").grid(row = 3, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.LRL_entry).grid(row = 3, column = 3, pady=(20,0), padx=(0,10))

        self.URL_entry = tk.StringVar()
        ttk.Label(self, text="Upper Rate Limit | 50-175 ppm").grid(row = 4, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.URL_entry).grid(row = 4, column = 3, pady=(20,0), padx=(0,10))

        self.VA_entry = tk.StringVar()
        ttk.Label(self, text="Ventricular Amplitude | 0, 0.5-3.2V, 3.5-7.0 V").grid(row = 5, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.VA_entry).grid(row = 5, column = 3, pady=(20,0), padx=(0,10))

        self.VPW_entry = tk.StringVar()
        ttk.Label(self, text="Ventricular Pulse Width | 0.05 ns, 0.1-1.9 ms").grid(row = 6, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.VPW_entry).grid(row = 6, column = 3, pady=(20,0), padx=(0,10))

        backButton = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage))
        backButton.grid(row = 7, column = 2,  pady=(100,20), padx=(10,10))

        setValuesBtn = ttk.Button(self, text="Set Values",
                            command=self.setValues)
        setValuesBtn.grid(row = 7, column = 3,  pady=(100,20), padx=(10,10))

    def setValues(self):
        userList = []
        correctVals = False

        with open(LogIn.dbFile) as json_file:
            data = json.load(json_file)
            userList = data['users']

        for user in userList:
            if (user['username'] == LogIn.currentUser):
                if (
                    checkLRL(self.LRL_entry.get()) and
                    checkURL(self.URL_entry.get()) and
                    checkAmp(self.VA_entry.get()) and
                    checkPW(self.VPW_entry.get()) #check valid nums are entered
                ):
                    user['LRL'] = self.LRL_entry.get() 
                    user['URL'] = self.URL_entry.get()
                    user['VA'] = self.VA_entry.get()
                    user['VPW'] = self.VPW_entry.get()
                    user['Mode'] = 'VOO'

                    correctVals = True
                else:
                    messagebox.showerror('Error', 'Try again. Please enter a valid input that is within the specified range.')
                    break

                data['users'] = userList
                with open(LogIn.dbFile,'w') as outfile:
                    json.dump(data,outfile)

                with open(LogIn.dbFile) as json_file:
                    data = json.load(json_file)
                    userList = data['users']

                    for user in userList:
                        if (user['username'] == LogIn.currentUser and correctVals):
                            sendSerialInfo(33, LogIn.tempUserObject)
                            break
                
                messagebox.showinfo('Success', 'Successfully added values.')
                break

class ModeAAI(tk.Frame):
    def __init__(self, parent, controller):
        #initialize widgets
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="AAI Mode", font="LARGE_FONT")
        label.grid(pady=20, padx=(300,0), row = 1, column = 2)

        self.LRL_entry = tk.StringVar()
        ttk.Label(self, text="Lower Rate Limit | 30-175 ppm").grid(row = 3, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.LRL_entry).grid(row = 3, column = 3, pady=(20,0), padx=(0,10))

        self.URL_entry = tk.StringVar()
        ttk.Label(self, text="Upper Rate Limit | 50-175 ppm").grid(row = 4, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.URL_entry).grid(row = 4, column = 3, pady=(20,0), padx=(0,10))

        self.AA_entry = tk.StringVar()
        ttk.Label(self, text="Atrial Amplitude | 0, 0.5-3.2V, 3.5-7.0 V").grid(row = 5, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.AA_entry).grid(row = 5, column = 3, pady=(20,0), padx=(0,10))

        self.APW_entry = tk.StringVar()
        ttk.Label(self, text="Atrial Pulse Width | 0.05 ns, 0.1-1.9 ms").grid(row = 6, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.APW_entry).grid(row = 6, column = 3, pady=(20,0), padx=(0,10))

        self.ARP_entry = tk.StringVar()
        ttk.Label(self, text="Atrial Refractory Period | 150-500 ms").grid(row = 7, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.ARP_entry).grid(row = 7, column = 3, pady=(20,0), padx=(0,10))

        backButton = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage))
        backButton.grid(row = 8, column = 2,  pady=(100,20), padx=(10,10))

        setValuesBtn = ttk.Button(self, text="Set Values",
                            command=self.setValues)
        setValuesBtn.grid(row = 8, column = 3,  pady=(100,20), padx=(10,10))

    def setValues(self):
        userList = []
        correctVals = False

        with open(LogIn.dbFile) as json_file:
            data = json.load(json_file)
            userList = data['users']

        for user in userList:
            if (user['username'] == LogIn.currentUser):
                if (
                    checkLRL(self.LRL_entry.get()) and
                    checkURL(self.URL_entry.get()) and
                    checkAmp(self.AA_entry.get()) and
                    checkPW(self.APW_entry.get()) and
                    checkRP(self.ARP_entry.get()) #check valid nums are entered
                ):
                    user['LRL'] = self.LRL_entry.get() 
                    user['URL'] = self.URL_entry.get()
                    user['AA'] = self.AA_entry.get()
                    user['APW'] = self.APW_entry.get()
                    user['ARP'] = self.ARP_entry.get()
                    user['Mode'] = 'AAI'
                    correctVals = True

                else:
                    messagebox.showerror('Error', 'Try again. Please enter a valid input that is within the specified range.')
                    break

                data['users'] = userList
                with open(LogIn.dbFile,'w') as outfile:
                    json.dump(data,outfile)

                with open(LogIn.dbFile) as json_file:
                    data = json.load(json_file)
                    userList = data['users']

                    for user in userList:
                        if (user['username'] == LogIn.currentUser and correctVals):
                            sendSerialInfo(33, LogIn.tempUserObject)
                            break
                
                messagebox.showinfo('Success', 'Successfully added values.')
                break

class ModeVVI(tk.Frame):
    def __init__(self, parent, controller):
        #initialize widgets

        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="VVI Mode", font="LARGE_FONT")
        label.grid(pady=20, padx=(300,0), row = 1, column = 2)

        self.LRL_entry = tk.StringVar()
        ttk.Label(self, text="Lower Rate Limit | 30-175 ppm").grid(row = 3, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.LRL_entry).grid(row = 3, column = 3, pady=(20,0), padx=(0,10))

        self.URL_entry = tk.StringVar()
        ttk.Label(self, text="Upper Rate Limit | 50-175 ppm").grid(row = 4, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.URL_entry).grid(row = 4, column = 3, pady=(20,0), padx=(0,10))

        self.VA_entry = tk.StringVar()
        ttk.Label(self, text="Ventricular Amplitude | 0, 0.5-3.2V, 3.5-7.0 V").grid(row = 5, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.VA_entry).grid(row = 5, column = 3, pady=(20,0), padx=(0,10))

        self.VPW_entry = tk.StringVar()
        ttk.Label(self, text="Ventricular Pulse Width | 0.05 ns, 0.1-1.9 ms").grid(row = 6, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.VPW_entry).grid(row = 6, column = 3, pady=(20,0), padx=(0,10))

        self.VRP_entry = tk.StringVar()
        ttk.Label(self, text="Ventricular Refractory Period | 150-500 ms").grid(row = 7, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.VRP_entry).grid(row = 7, column = 3, pady=(20,0), padx=(0,10))

        backButton = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage))
        backButton.grid(row = 8, column = 2,  pady=(100,20), padx=(10,10))

        setValuesBtn = ttk.Button(self, text="Set Values",
                            command=self.setValues)
        setValuesBtn.grid(row = 8, column = 3,  pady=(100,20), padx=(10,10))

    def setValues(self):
        userList = []
        correctVals = False

        with open(LogIn.dbFile) as json_file:
            data = json.load(json_file)
            userList = data['users']

        for user in userList:
            if (user['username'] == LogIn.currentUser):
                if (
                    checkLRL(self.LRL_entry.get()) and
                    checkURL(self.URL_entry.get()) and
                    checkAmp(self.VA_entry.get()) and
                    checkPW(self.VPW_entry.get()) and
                    checkRP(self.VRP_entry.get()) #check valid nums are entered
                ):
                    user['LRL'] = self.LRL_entry.get() 
                    user['URL'] = self.URL_entry.get()
                    user['VA'] = self.VA_entry.get()
                    user['VPW'] = self.VPW_entry.get()
                    user['VRP'] = self.VRP_entry.get()
                    user['Mode'] = 'VVI' 

                    correctVals = True
                else:
                    messagebox.showerror('Error', 'Try again. Please enter a valid input that is within the specified range.')
                    break

                data['users'] = userList
                with open(LogIn.dbFile,'w') as outfile:
                    json.dump(data,outfile)

                with open(LogIn.dbFile) as json_file:
                    data = json.load(json_file)
                    userList = data['users']

                    for user in userList:
                        if (user['username'] == LogIn.currentUser and correctVals):
                            sendSerialInfo(33, LogIn.tempUserObject)
                            break
                
                messagebox.showinfo('Success', 'Successfully added values.')
                break

class ModeDOO(tk.Frame):
    def __init__(self, parent, controller):
        #initialize widgets

        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="DOO Mode", font="LARGE_FONT")
        label.grid(pady=20, padx=(300,0), row = 1, column = 2)

        self.LRL_entry = tk.StringVar()
        ttk.Label(self, text="Lower Rate Limit | 30-175 ppm").grid(row = 3, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.LRL_entry).grid(row = 3, column = 3, pady=(20,0), padx=(0,10))

        self.URL_entry = tk.StringVar()
        ttk.Label(self, text="Upper Rate Limit | 50-175 ppm").grid(row = 4, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.URL_entry).grid(row = 4, column = 3, pady=(20,0), padx=(0,10))

        self.AA_entry = tk.StringVar()
        ttk.Label(self, text="Atrial Amplitude | 0, 0.5-3.2V, 3.5-7.0 V").grid(row = 5, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.AA_entry).grid(row = 5, column = 3, pady=(20,0), padx=(0,10))

        self.VA_entry = tk.StringVar()
        ttk.Label(self, text="Ventricular Amplitude | 0, 0.5-3.2V, 3.5-7.0 V").grid(row = 6, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.VA_entry).grid(row = 6, column = 3, pady=(20,0), padx=(0,10))

        self.APW_entry = tk.StringVar()
        ttk.Label(self, text="Atrial Pulse Width | 0.05 ns, 0.1-1.9 ms").grid(row = 7, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.APW_entry).grid(row = 7, column = 3, pady=(20,0), padx=(0,10))

        self.VPW_entry = tk.StringVar()
        ttk.Label(self, text="Ventricular Pulse Width | 0.05 ns, 0.1-1.9 ms").grid(row = 8, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.VPW_entry).grid(row = 8, column = 3, pady=(20,0), padx=(0,10))

        self.FAVD_entry = tk.StringVar()
        ttk.Label(self, text="Fixed AV Delay | 70-300 ms").grid(row = 9, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.FAVD_entry).grid(row = 9, column = 3, pady=(20,0), padx=(0,10))

        backButton = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage))
        backButton.grid(row = 10, column = 2,  pady=(100,20), padx=(10,10))

        setValuesBtn = ttk.Button(self, text="Set Values",
                            command=self.setValues)
        setValuesBtn.grid(row = 10, column = 3,  pady=(100,20), padx=(10,10))

    def setValues(self):
        userList = []
        correctVals = False

        with open(LogIn.dbFile) as json_file:
            data = json.load(json_file)
            userList = data['users']

        for user in userList:
            if (user['username'] == LogIn.currentUser):
                if (
                    checkLRL(self.LRL_entry.get()) and
                    checkURL(self.URL_entry.get()) and
                    checkAmp(self.AA_entry.get()) and
                    checkAmp(self.VA_entry.get()) and
                    checkPW(self.APW_entry.get()) and 
                    checkPW(self.VPW_entry.get()) and
                    checkFAVD(self.FAVD_entry.get())
                ):
                    user['LRL'] = self.LRL_entry.get() 
                    user['URL'] = self.URL_entry.get()
                    user['AA'] = self.AA_entry.get()
                    user['VA'] = self.VA_entry.get()
                    user['APW'] = self.APW_entry.get()
                    user['VPW'] = self.VPW_entry.get()
                    user['FAVD'] = self.FAVD_entry.get()
                    user['Mode'] = 'DOO'

                    correctVals = True
                else:
                    messagebox.showerror('Error', 'Try again. Please enter a valid input that is within the specified range.')
                    break

                data['users'] = userList
                with open(LogIn.dbFile,'w') as outfile:
                    json.dump(data,outfile)

                with open(LogIn.dbFile) as json_file:
                    data = json.load(json_file)
                    userList = data['users']

                    for user in userList:
                        if (user['username'] == LogIn.currentUser and correctVals):
                            sendSerialInfo(33, LogIn.tempUserObject)
                            break
                
                messagebox.showinfo('Success', 'Successfully added values.')
                break

class ModeAOOR(tk.Frame):
    def __init__(self, parent, controller):
        #initialize widgets

        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="AOOR Mode", font="LARGE_FONT")
        label.grid(pady=20, padx=(300,0), row = 1, column = 2)

        self.LRL_entry = tk.StringVar()
        ttk.Label(self, text="Lower Rate Limit | 30-175 ppm").grid(row = 3, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.LRL_entry).grid(row = 3, column = 3, pady=(20,0), padx=(0,10))

        self.URL_entry = tk.StringVar()
        ttk.Label(self, text="Upper Rate Limit | 50-175 ppm").grid(row = 4, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.URL_entry).grid(row = 4, column = 3, pady=(20,0), padx=(0,10))

        self.AA_entry = tk.StringVar()
        ttk.Label(self, text="Atrial Amplitude | 0, 0.5-3.2V, 3.5-7.0 V").grid(row = 5, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.AA_entry).grid(row = 5, column = 3, pady=(20,0), padx=(0,10))

        self.APW_entry = tk.StringVar()
        ttk.Label(self, text="Atrial Pulse Width | 0.05 ns, 0.1-1.9 ms").grid(row = 6, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.APW_entry).grid(row = 6, column = 3, pady=(20,0), padx=(0,10))

        self.MSR_entry = tk.StringVar()
        ttk.Label(self, text="Maximum Sensor Rate | 50-175 ppm").grid(row = 7, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.MSR_entry).grid(row = 7, column = 3, pady=(20,0), padx=(0,10))

        self.AT_entry = tk.StringVar()
        ttk.Label(self, text="Activity Threshold | V-Low, Low, Med-Low, Med, Med-High, High, V-High").grid(row = 8, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.AT_entry).grid(row = 8, column = 3, pady=(20,0), padx=(0,10))

        self.ReactTime_entry = tk.StringVar()
        ttk.Label(self, text="Reaction Time | 10-50 sec").grid(row = 9, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.ReactTime_entry).grid(row = 9, column = 3, pady=(20,0), padx=(0,10))

        self.RF_entry = tk.StringVar()
        ttk.Label(self, text="Response Factor | 1-16").grid(row = 10, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.RF_entry).grid(row = 10, column = 3, pady=(20,0), padx=(0,10))

        self.RecovTime_entry = tk.StringVar()
        ttk.Label(self, text="Recovery Time | 2-16 min").grid(row = 11, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.RecovTime_entry).grid(row = 11, column = 3, pady=(20,0), padx=(0,10))

        backButton = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage))
        backButton.grid(row = 12, column = 2,  pady=(30,20), padx=(10,10))

        setValuesBtn = ttk.Button(self, text="Set Values",
                            command=self.setValues)
        setValuesBtn.grid(row = 12, column = 3,  pady=(30,20), padx=(10,10))

    def setValues(self):
        userList = []
        correctVals = False

        with open(LogIn.dbFile) as json_file:
            data = json.load(json_file)
            userList = data['users']

        for user in userList:
            if (user['username'] == LogIn.currentUser):
                if (
                    checkLRL(self.LRL_entry.get()) and
                    checkURL(self.URL_entry.get()) and
                    checkAmp(self.AA_entry.get()) and
                    checkPW(self.APW_entry.get()) and
                    checkMSR(self.MSR_entry.get())and 
                    checkAT(self.AT_entry.get()) and
                    checkReactTime(self.ReactTime_entry.get()) and
                    checkRF(self.RF_entry.get()) and
                    checkRecovTime(self.RecovTime_entry.get())
                ):
                    user['LRL'] = self.LRL_entry.get() 
                    user['URL'] = self.URL_entry.get()
                    user['AA'] = self.AA_entry.get()
                    user['APW'] = self.APW_entry.get()
                    user['MSR'] = self.MSR_entry.get()
                    user['AT'] = self.AT_entry.get()
                    user['ReactTime'] = self.ReactTime_entry.get()
                    user['RF'] = self.RF_entry.get()
                    user['RecovTime'] = self.RecovTime_entry.get()
                    user['Mode'] = 'AOOR'

                    correctVals = True

                else:
                    messagebox.showerror('Error', 'Try again. Please enter a valid input that is within the specified range.')
                    break

                data['users'] = userList
                with open(LogIn.dbFile,'w') as outfile:
                    json.dump(data,outfile)
                
                with open(LogIn.dbFile) as json_file:
                    data = json.load(json_file)
                    userList = data['users']

                    for user in userList:
                        if (user['username'] == LogIn.currentUser and correctVals):
                            sendSerialInfo(33, LogIn.tempUserObject)
                            break

                messagebox.showinfo('Success', 'Successfully added values.')
                break

class ModeVOOR(tk.Frame):
    def __init__(self, parent, controller):
        #initialize widgets

        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="VOOR Mode", font="LARGE_FONT")
        label.grid(pady=20, padx=(300,0), row = 1, column = 2)

        self.LRL_entry = tk.StringVar()
        ttk.Label(self, text="Lower Rate Limit | 30-175 ppm").grid(row = 3, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.LRL_entry).grid(row = 3, column = 3, pady=(20,0), padx=(0,10))

        self.URL_entry = tk.StringVar()
        ttk.Label(self, text="Upper Rate Limit | 50-175 ppm").grid(row = 4, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.URL_entry).grid(row = 4, column = 3, pady=(20,0), padx=(0,10))

        self.VA_entry = tk.StringVar()
        ttk.Label(self, text="Ventricular Amplitude | 0, 0.5-3.2V, 3.5-7.0 V").grid(row = 5, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.VA_entry).grid(row = 5, column = 3, pady=(20,0), padx=(0,10))

        self.VPW_entry = tk.StringVar()
        ttk.Label(self, text="Ventricular Pulse Width | 0.05 ns, 0.1-1.9 ms").grid(row = 6, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.VPW_entry).grid(row = 6, column = 3, pady=(20,0), padx=(0,10))

        self.MSR_entry = tk.StringVar()
        ttk.Label(self, text="Maximum Sensor Rate | 50-175 ppm").grid(row = 7, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.MSR_entry).grid(row = 7, column = 3, pady=(20,0), padx=(0,10))

        self.AT_entry = tk.StringVar()
        ttk.Label(self, text="Activity Threshold | V-Low, Low, Med-Low, Med, Med-High, High, V-High").grid(row = 8, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.AT_entry).grid(row = 8, column = 3, pady=(20,0), padx=(0,10))

        self.ReactTime_entry = tk.StringVar()
        ttk.Label(self, text="Reaction Time | 10-50 sec").grid(row = 9, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.ReactTime_entry).grid(row = 9, column = 3, pady=(20,0), padx=(0,10))

        self.RF_entry = tk.StringVar()
        ttk.Label(self, text="Response Factor | 1-16").grid(row = 10, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.RF_entry).grid(row = 10, column = 3, pady=(20,0), padx=(0,10))

        self.RecovTime_entry = tk.StringVar()
        ttk.Label(self, text="Recovery Time | 2-16 min").grid(row = 11, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.RecovTime_entry).grid(row = 11, column = 3, pady=(20,0), padx=(0,10))

        backButton = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage))
        backButton.grid(row = 12, column = 2,  pady=(30,20), padx=(10,10))

        setValuesBtn = ttk.Button(self, text="Set Values",
                            command=self.setValues)
        setValuesBtn.grid(row = 12, column = 3,  pady=(30,20), padx=(10,10))

    def setValues(self):
        userList = []
        correctVals = False

        with open(LogIn.dbFile) as json_file:
            data = json.load(json_file)
            userList = data['users']

        for user in userList:
            if (user['username'] == LogIn.currentUser):
                if (
                    checkLRL(self.LRL_entry.get()) and
                    checkURL(self.URL_entry.get()) and
                    checkAmp(self.VA_entry.get()) and
                    checkPW(self.VPW_entry.get()) and
                    checkMSR(self.MSR_entry.get()) and 
                    checkAT(self.AT_entry.get()) and
                    checkReactTime(self.ReactTime_entry.get()) and
                    checkRF(self.RF_entry.get()) and
                    checkRecovTime(self.RecovTime_entry.get())
                ):
                    user['LRL'] = self.LRL_entry.get() 
                    user['URL'] = self.URL_entry.get()
                    user['VA'] = self.VA_entry.get()
                    user['VPW'] = self.VPW_entry.get()
                    user['MSR'] = self.MSR_entry.get()
                    user['AT'] = self.AT_entry.get()
                    user['ReactTime'] = self.ReactTime_entry.get()
                    user['RF'] = self.RF_entry.get()
                    user['RecovTime'] = self.RecovTime_entry.get()
                    user['Mode'] = 'VOOR'

                    correctVals = True
                else:
                    messagebox.showerror('Error', 'Try again. Please enter a valid input that is within the specified range.')
                    break

                data['users'] = userList
                with open(LogIn.dbFile,'w') as outfile:
                    json.dump(data,outfile)

                with open(LogIn.dbFile) as json_file:
                    data = json.load(json_file)
                    userList = data['users']

                    for user in userList:
                        if (user['username'] == LogIn.currentUser and correctVals):
                            sendSerialInfo(33, LogIn.tempUserObject)
                            break
                
                messagebox.showinfo('Success', 'Successfully added values.')
                break

class ModeAAIR(tk.Frame):
    def __init__(self, parent, controller):
        #initialize widgets

        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="AAIR Mode", font="LARGE_FONT")
        label.grid(pady=20, padx=(300,0), row = 1, column = 2)

        self.LRL_entry = tk.StringVar()
        ttk.Label(self, text="Lower Rate Limit | 30-175 ppm").grid(row = 3, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.LRL_entry).grid(row = 3, column = 3, pady=(20,0), padx=(0,10))

        self.URL_entry = tk.StringVar()
        ttk.Label(self, text="Upper Rate Limit | 50-175 ppm").grid(row = 4, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.URL_entry).grid(row = 4, column = 3, pady=(20,0), padx=(0,10))

        self.AA_entry = tk.StringVar()
        ttk.Label(self, text="Atrial Amplitude | 0, 0.5-3.2V, 3.5-7.0 V").grid(row = 5, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.AA_entry).grid(row = 5, column = 3, pady=(20,0), padx=(0,10))

        self.APW_entry = tk.StringVar()
        ttk.Label(self, text="Atrial Pulse Width | 0.05 ns, 0.1-1.9 ms").grid(row = 6, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.APW_entry).grid(row = 6, column = 3, pady=(20,0), padx=(0,10))

        self.ARP_entry = tk.StringVar()
        ttk.Label(self, text="Atrial Refractory Period | 150-500 ms").grid(row = 7, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.ARP_entry).grid(row = 7, column = 3, pady=(20,0), padx=(0,10))

        self.MSR_entry = tk.StringVar()
        ttk.Label(self, text="Maximum Sensor Rate | 50-175 ppm").grid(row = 8, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.MSR_entry).grid(row = 8, column = 3, pady=(20,0), padx=(0,10))

        self.AT_entry = tk.StringVar()
        ttk.Label(self, text="Activity Threshold | V-Low, Low, Med-Low, Med, Med-High, High, V-High").grid(row = 9, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.AT_entry).grid(row = 9, column = 3, pady=(20,0), padx=(0,10))

        self.ReactTime_entry = tk.StringVar()
        ttk.Label(self, text="Reaction Time | 10-50 sec").grid(row = 10, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.ReactTime_entry).grid(row = 10, column = 3, pady=(20,0), padx=(0,10))

        self.RF_entry = tk.StringVar()
        ttk.Label(self, text="Response Factor | 1-16").grid(row = 11, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.RF_entry).grid(row = 11, column = 3, pady=(20,0), padx=(0,10))

        self.RecovTime_entry = tk.StringVar()
        ttk.Label(self, text="Recovery Time | 2-16 min").grid(row = 12, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.RecovTime_entry).grid(row = 12, column = 3, pady=(20,0), padx=(0,10))

        backButton = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage))
        backButton.grid(row = 13, column = 2,  pady=(30,20), padx=(10,10))

        setValuesBtn = ttk.Button(self, text="Set Values",
                            command=self.setValues)
        setValuesBtn.grid(row = 13, column = 3,  pady=(30,20), padx=(10,10))

    def setValues(self):
        userList = []
        correctVals = False

        with open(LogIn.dbFile) as json_file:
            data = json.load(json_file)
            userList = data['users']

        for user in userList:
            if (user['username'] == LogIn.currentUser):
                if (
                    checkLRL(self.LRL_entry.get()) and
                    checkURL(self.URL_entry.get()) and
                    checkAmp(self.AA_entry.get()) and
                    checkPW(self.APW_entry.get()) and
                    checkRP(self.ARP_entry.get()) and
                    checkMSR(self.MSR_entry.get()) and 
                    checkAT(self.AT_entry.get()) and
                    checkReactTime(self.ReactTime_entry.get()) and
                    checkRF(self.RF_entry.get()) and
                    checkRecovTime(self.RecovTime_entry.get())
                ):
                    user['LRL'] = self.LRL_entry.get() 
                    user['URL'] = self.URL_entry.get()
                    user['AA'] = self.AA_entry.get()
                    user['APW'] = self.APW_entry.get()
                    user['ARP'] = self.ARP_entry.get()
                    user['MSR'] = self.MSR_entry.get()
                    user['AT'] = self.AT_entry.get()
                    user['ReactTime'] = self.ReactTime_entry.get()
                    user['RF'] = self.RF_entry.get()
                    user['RecovTime'] = self.RecovTime_entry.get()
                    user['Mode'] = 'AAIR'

                    correctVals = True
                else:
                    messagebox.showerror('Error', 'Try again. Please enter a valid input that is within the specified range.')
                    break

                data['users'] = userList
                with open(LogIn.dbFile,'w') as outfile:
                    json.dump(data,outfile)

                with open(LogIn.dbFile) as json_file:
                    data = json.load(json_file)
                    userList = data['users']

                    for user in userList:
                        if (user['username'] == LogIn.currentUser and correctVals):
                            sendSerialInfo(33, LogIn.tempUserObject)
                            break
                
                messagebox.showinfo('Success', 'Successfully added values.')
                break

class ModeVVIR(tk.Frame):
    def __init__(self, parent, controller):
        #initialize widgets

        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="VVIR Mode", font="LARGE_FONT")
        label.grid(pady=20, padx=(300,0), row = 1, column = 2)

        self.LRL_entry = tk.StringVar()
        ttk.Label(self, text="Lower Rate Limit | 30-175 ppm").grid(row = 3, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.LRL_entry).grid(row = 3, column = 3, pady=(20,0), padx=(0,10))

        self.URL_entry = tk.StringVar()
        ttk.Label(self, text="Upper Rate Limit | 50-175 ppm").grid(row = 4, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.URL_entry).grid(row = 4, column = 3, pady=(20,0), padx=(0,10))

        self.VA_entry = tk.StringVar()
        ttk.Label(self, text="Ventricular Amplitude | 0, 0.5-3.2V, 3.5-7.0 V").grid(row = 5, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.VA_entry).grid(row = 5, column = 3, pady=(20,0), padx=(0,10))

        self.VPW_entry = tk.StringVar()
        ttk.Label(self, text="Ventricular Pulse Width | 0.05 ns, 0.1-1.9 ms").grid(row = 6, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.VPW_entry).grid(row = 6, column = 3, pady=(20,0), padx=(0,10))

        self.VRP_entry = tk.StringVar()
        ttk.Label(self, text="Ventricular Refractory Period | 150-500 ms").grid(row = 7, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.VRP_entry).grid(row = 7, column = 3, pady=(20,0), padx=(0,10))

        self.MSR_entry = tk.StringVar()
        ttk.Label(self, text="Maximum Sensor Rate | 50-175 ppm").grid(row = 8, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.MSR_entry).grid(row = 8, column = 3, pady=(20,0), padx=(0,10))

        self.AT_entry = tk.StringVar()
        ttk.Label(self, text="Activity Threshold | V-Low, Low, Med-Low, Med, Med-High, High, V-High").grid(row = 9, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.AT_entry).grid(row = 9, column = 3, pady=(20,0), padx=(0,10))

        self.ReactTime_entry = tk.StringVar()
        ttk.Label(self, text="Reaction Time | 10-50 sec").grid(row = 10, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.ReactTime_entry).grid(row = 10, column = 3, pady=(20,0), padx=(0,10))

        self.RF_entry = tk.StringVar()
        ttk.Label(self, text="Response Factor | 1-16").grid(row = 11, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.RF_entry).grid(row = 11, column = 3, pady=(20,0), padx=(0,10))

        self.RecovTime_entry = tk.StringVar()
        ttk.Label(self, text="Recovery Time | 2-16 min").grid(row = 12, column=2, pady=(20,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.RecovTime_entry).grid(row = 12, column = 3, pady=(20,0), padx=(0,10))

        backButton = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage))
        backButton.grid(row = 13, column = 2,  pady=(30,20), padx=(10,10))

        setValuesBtn = ttk.Button(self, text="Set Values",
                            command=self.setValues)
        setValuesBtn.grid(row = 13, column = 3,  pady=(30,20), padx=(10,10))

    def setValues(self):
        userList = []
        correctVals = False

        with open(LogIn.dbFile) as json_file:
            data = json.load(json_file)
            userList = data['users']

        for user in userList:
            if (user['username'] == LogIn.currentUser):
                if (
                    checkLRL(self.LRL_entry.get()) and
                    checkURL(self.URL_entry.get()) and
                    checkAmp(self.VA_entry.get()) and
                    checkPW(self.VPW_entry.get()) and
                    checkRP(self.VRP_entry.get()) and
                    checkMSR(self.MSR_entry.get()) and 
                    checkAT(self.AT_entry.get()) and
                    checkReactTime(self.ReactTime_entry.get()) and
                    checkRF(self.RF_entry.get()) and
                    checkRecovTime(self.RecovTime_entry.get())
                ):
                    user['LRL'] = self.LRL_entry.get() 
                    user['URL'] = self.URL_entry.get()
                    user['VA'] = self.VA_entry.get()
                    user['VPW'] = self.VPW_entry.get()
                    user['VRP'] = self.VRP_entry.get()
                    user['MSR'] = self.MSR_entry.get()
                    user['AT'] = self.AT_entry.get()
                    user['ReactTime'] = self.ReactTime_entry.get()
                    user['RF'] = self.RF_entry.get()
                    user['RecovTime'] = self.RecovTime_entry.get()
                    user['Mode'] = 'VVIR'

                    correctVals=True
                else:
                    messagebox.showerror('Error', 'Try again. Please enter a valid input that is within the specified range.')
                    break

                data['users'] = userList
                with open(LogIn.dbFile,'w') as outfile:
                    json.dump(data,outfile)

                with open(LogIn.dbFile) as json_file:
                    data = json.load(json_file)
                    userList = data['users']

                    for user in userList:
                        if (user['username'] == LogIn.currentUser and correctVals):
                            sendSerialInfo(33, LogIn.tempUserObject)
                            break
                
                messagebox.showinfo('Success', 'Successfully added values.')
                break

class ModeDOOR(tk.Frame):
    def __init__(self, parent, controller):
        #initialize widgets

        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="DOOR Mode", font="LARGE_FONT")
        label.grid(pady=20, padx=(300,0), row = 1, column = 2)

        self.LRL_entry = tk.StringVar()
        ttk.Label(self, text="Lower Rate Limit | 30-175 ppm").grid(row = 3, column=2, pady=(10,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.LRL_entry).grid(row = 3, column = 3, pady=(10,0), padx=(0,10))

        self.URL_entry = tk.StringVar()
        ttk.Label(self, text="Upper Rate Limit | 50-175 ppm").grid(row = 4, column=2, pady=(10,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.URL_entry).grid(row = 4, column = 3, pady=(10,0), padx=(0,10))

        self.AA_entry = tk.StringVar()
        ttk.Label(self, text="Atrial Amplitude | 0, 0.5-3.2V, 3.5-7.0 V").grid(row = 5, column=2, pady=(10,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.AA_entry).grid(row = 5, column = 3, pady=(10,0), padx=(0,10))

        self.VA_entry = tk.StringVar()
        ttk.Label(self, text="Ventricular Amplitude | 0, 0.5-3.2V, 3.5-7.0 V").grid(row = 6, column=2, pady=(10,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.VA_entry).grid(row = 6, column = 3, pady=(10,0), padx=(0,10))

        self.APW_entry = tk.StringVar()
        ttk.Label(self, text="Atrial Pulse Width | 0.05 ns, 0.1-1.9 ms").grid(row = 7, column=2, pady=(10,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.APW_entry).grid(row = 7, column = 3, pady=(10,0), padx=(0,10))

        self.VPW_entry = tk.StringVar()
        ttk.Label(self, text="Ventricular Pulse Width | 0.05 ns, 0.1-1.9 ms").grid(row = 8, column=2, pady=(10,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.VPW_entry).grid(row = 8, column = 3, pady=(10,0), padx=(0,10))

        self.ARP_entry = tk.StringVar()
        ttk.Label(self, text="Atrial Refractory Period | 150-500 ms").grid(row = 9, column=2, pady=(10,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.ARP_entry).grid(row = 9, column = 3, pady=(10,0), padx=(0,10))

        self.VRP_entry = tk.StringVar()
        ttk.Label(self, text="Ventricular Refractory Period | 150-500 ms").grid(row = 10, column=2, pady=(10,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.VRP_entry).grid(row = 10, column = 3, pady=(10,0), padx=(0,10))

        self.MSR_entry = tk.StringVar()
        ttk.Label(self, text="Maximum Sensor Rate | 50-175 ppm").grid(row = 11, column=2, pady=(10,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.MSR_entry).grid(row = 11, column = 3, pady=(10,0), padx=(0,10))

        self.FAVD_entry = tk.StringVar()
        ttk.Label(self, text="Fixed AV Delay | 70-300 ms").grid(row = 12, column=2, pady=(10,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.FAVD_entry).grid(row = 12, column = 3, pady=(10,0), padx=(0,10))

        self.AT_entry = tk.StringVar()
        ttk.Label(self, text="Activity Threshold | V-Low, Low, Med-Low, Med, Med-High, High, V-High").grid(row = 13, column=2, pady=(10,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.AT_entry).grid(row = 13, column = 3, pady=(10,0), padx=(0,10))

        self.ReactTime_entry = tk.StringVar()
        ttk.Label(self, text="Reaction Time | 10-50 sec").grid(row = 14, column=2, pady=(10,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.ReactTime_entry).grid(row = 14, column = 3, pady=(10,0), padx=(0,10))

        self.RF_entry = tk.StringVar()
        ttk.Label(self, text="Response Factor | 1-16").grid(row = 15, column=2, pady=(10,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.RF_entry).grid(row = 15, column = 3, pady=(10,0), padx=(0,10))

        self.RecovTime_entry = tk.StringVar()
        ttk.Label(self, text="Recovery Time | 2-16 min").grid(row = 16, column=2, pady=(10,0), padx=(0,10))
        ttk.Entry(self, width="7", textvariable=self.RecovTime_entry).grid(row = 16, column = 3, pady=(10,0), padx=(0,10))

        backButton = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage))
        backButton.grid(row = 17, column = 2,  pady=(30,20), padx=(10,10))

        setValuesBtn = ttk.Button(self, text="Set Values",
                            command=self.setValues)
        setValuesBtn.grid(row = 17, column = 3,  pady=(30,20), padx=(10,10))

    def setValues(self):
        userList = []
        correctVals = False

        with open(LogIn.dbFile) as json_file:
            data = json.load(json_file)
            userList = data['users']

        for user in userList:
            if (user['username'] == LogIn.currentUser):
                if (
                    checkLRL(self.LRL_entry.get()) and
                    checkURL(self.URL_entry.get()) and
                    checkAmp(self.AA_entry.get()) and
                    checkAmp(self.VA_entry.get()) and
                    checkPW(self.APW_entry.get()) and
                    checkPW(self.VPW_entry.get()) and
                    checkRP(self.ARP_entry.get()) and
                    checkRP(self.VRP_entry.get()) and
                    checkMSR(self.MSR_entry.get()) and
                    checkFAVD(self.FAVD_entry.get()) and 
                    checkAT(self.AT_entry.get()) and
                    checkReactTime(self.ReactTime_entry.get()) and
                    checkRF(self.RF_entry.get()) and
                    checkRecovTime(self.RecovTime_entry.get())
                ):
                    user['LRL'] = self.LRL_entry.get() 
                    user['URL'] = self.URL_entry.get()
                    user['AA'] = self.AA_entry.get()
                    user['VA'] = self.VA_entry.get()
                    user['APW'] = self.APW_entry.get()
                    user['VPW'] = self.VPW_entry.get()
                    user['ARP'] = self.ARP_entry.get()
                    user['VRP'] = self.VRP_entry.get()
                    user['MSR'] = self.MSR_entry.get()
                    user['FAVD'] = self.FAVD_entry.get()
                    user['AT'] = self.AT_entry.get()
                    user['ReactTime'] = self.ReactTime_entry.get()
                    user['RF'] = self.RF_entry.get()
                    user['RecovTime'] = self.RecovTime_entry.get()
                    user['Mode'] = 'DOOR'

                    correctVals = True
                else:
                    messagebox.showerror('Error', 'Try again. Please enter a valid input that is within the specified range.')
                    break

                data['users'] = userList
                with open(LogIn.dbFile,'w') as outfile:
                    json.dump(data,outfile)

                with open(LogIn.dbFile) as json_file:
                    data = json.load(json_file)
                    userList = data['users']

                    for user in userList:
                        if (user['username'] == LogIn.currentUser and correctVals):
                            sendSerialInfo(33, LogIn.tempUserObject)
                            break
                
                messagebox.showinfo('Success', 'Successfully added values.')
                break

if __name__ == "__main__":
    app = MainDCM()
    app.mainloop()
