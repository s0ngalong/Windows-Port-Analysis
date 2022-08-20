import csv, math, multiprocessing, msvcrt, os, pprint, socket, subprocess, threading, webbrowser
#custom module
import IPValid

#from Textbook sockets port scan.
def Port_Scan(T, ADR, Ports, Connect_Type,Application_protocol=' ',Service_Name=' '):
    if Connect_Type == 'TCP':
        Socket_Type = socket.SOCK_STREAM
    elif Connect_Type == 'UDP':
        Socket_Type = socket.SOCK_DGRAM
    else:
        Socket_Type = socket.SOCK_STREAM
    
    
    try:
        #create a socket each time the function runs.
        sock = socket.socket(socket.AF_INET, Socket_Type)
        #socket.connect_ex is connecting to the address and port. but it only returns 1 if successful or 0 if failed.
        result = sock.connect_ex((ADR, Ports))
        if result == 0:
            T.acquire()
            print(f'Port {Ports} {Connect_Type}   :  Open   {Application_protocol}   {Service_Name}')
            T.release()
        else:
            T.acquire()
            print(f'Port {Ports} {Connect_Type}   :  Closed {Application_protocol}   {Service_Name}')
            T.release()
        sock.close()
    except socket.error as Error:
        print(str(Error)+'\nConnection Error')
    except socket.gaierror as GError:
        print(str(GError))

#get the cpu count. How many CPU Cores.
Perf = multiprocessing.cpu_count()*8


def Windows_Ports():
    Lock = threading.RLock()
    while True:
        IPAD = input('Please input a valid IPv4 Address: ')
        Validation = IPValid.ValidIP(IPAD)
        if Validation == IPAD:
            break
        else:
            print(Validation)
    try:
        with open('Windows ports.csv', 'r') as ReadPorts: #opening Windows ports.csv file
            ReadPortsCSV = csv.DictReader(ReadPorts) #Reading each line as a dictionary 
            #count variables
            Count = 0
            Multi = 1
            for Data in ReadPortsCSV: #Reading the dictionary line by line.
                try:
                    #Initiating a new thread with arguments passed through a function.
                    Scan = threading.Thread(target=Port_Scan, args=(Lock,IPAD, int(Data['Port']), Data['Protocol'], Data['Application_protocol'] , Data['System_Service_Name']))
                    Scan.start() #starting the thread.
                    Count +=1
                    if Count == Perf*Multi:
                        Scan.join() #Finishes current threads before moving past this code.
                        Multi+=1
                except ValueError:
                    pass
    except FileNotFoundError:
        print('no file found called Windows ports.csv\nPlease copy the Table from the browser about to open.\nSave as a csv file called Windows ports.csv')
        print('Please modify the first three rows with their respective Port number and type.')
        webbrowser.open_new('https://social.technet.microsoft.com/wiki/contents/articles/1772.windows-ports-protocols-and-system-services.aspx')
        print(f'Location to copy: {os.getcwd()}\\')
        print('Press space key to quit')
        msvcrt.getch()

def R(*Irrelevant):
    Lock = threading.RLock()
    while True:
        IPAD = input('Please input a valid IPv4 Address: ')
        Validation = IPValid.ValidIP(IPAD)
        if Validation == IPAD:
            break
        else:
            print(Validation)
    if Irrelevant != ():
        while True:
            Type = input('What protocal? (TCP or UDP): ')
            if Type.upper() == 'TCP' or Type.upper() == 'UDP':
                break
            else:
                print('you did not type the right Port-Type.. (TCP or UDP)')
        while True:
            try:
                PortRangeStart = int(input('Start port: '))
                PortRangeEnd = int(input('End Port: '))
                if PortRangeStart < 0:
                    PortRangeStart*-1
                if PortRangeEnd < 0:
                    PortRangeEnd*-1
                break
            except ValueError as NoNo:
                print(NoNo.args)
                print('Enter a Number...')
        if PortRangeStart > PortRangeEnd:
            X = PortRangeStart
            PortRangeStart = PortRangeEnd
            PortRangeEnd = X
            print('The starting port number was higher than the ending port number. so the, the number has been swapped.')
        if PortRangeEnd > 65535:
            PortRangeEnd = 65535
            print('You typed a number higher than the maximum port number.\nSo, the End port has been set to 65535.')
        if PortRangeEnd-PortRangeStart > Perf:
    #Dividing the range by performance
    #Taking apart pieces of the range
    #Keeping track of subsequent itterations
    #Checking for the last itteration to check the end of the range specified.
    #Itterating through each port

            for L in range(math.ceil((PortRangeEnd-PortRangeStart)/Perf)):
                if L == 0:
                    SmallRangeStart = PortRangeStart
                    SmallRangeEnd = PortRangeStart+Perf
                elif L == math.ceil((PortRangeEnd-PortRangeStart)/Perf)-1:
                    SmallRangeEnd = PortRangeEnd+1
                for P in range(SmallRangeStart,SmallRangeEnd):
                    Scan = threading.Thread(target=Port_Scan, args=(Lock,IPAD,P,Type))
                    Scan.start()
                Scan.join()
                SmallRangeStart = SmallRangeEnd
                SmallRangeEnd = SmallRangeEnd+Perf
        else:
            #If the range specified is smaller than the required target of perf it will run.
            for I in range(PortRangeStart,PortRangeEnd+1):
                Scan = threading.Thread(target=Port_Scan, args=(Lock, IPAD, I, Type))
                Scan.start()
            Scan.join()
    else:
        #If a specified range is not specified then it will open a file and loop through non Windows related ports (TCP).
        Holder,Multi = 0,4
        try:
            with open('Windows ports.csv', 'r') as ReadPorts: #opening Windows ports.csv file
                ReadPortsCSV = csv.DictReader(ReadPorts) #Reading each line as a dictionary 
                for Data in ReadPortsCSV: #Reading the dictionary line by line.
                    try:
                        for I in range(Holder+1,65536): #Itterating through port numbers
                            if Holder == int(Data['Port']): 
                                pass
                            elif I == int(Data['Port']): 
                                Holder = int(Data['Port'])
                            else:
                                #Initiating a new thread with arguments passed through a function.
                                Scan = threading.Thread(target=Port_Scan, args=(Lock, IPAD, I,'TCP'))
                                Scan.start() #starting the thread.
                                if I == Perf*Multi:
                                    Scan.join()
                                    Multi+=4
                    except ValueError:
                        pass
        except FileNotFoundError:
            print('no file found called Windows ports.csv\nPlease copy the Table from the browser about to open.\nSave as a csv file called Windows ports.csv')
            print('Please modify the first three rows with their respective Port number and type.')
            webbrowser.open('https://social.technet.microsoft.com/wiki/contents/articles/1772.windows-ports-protocols-and-system-services.aspx')
            print('Press space key to quit.')
            msvcrt.getch()
# This function is collecting data from the computer.
def Active_con():
    def ProcessInfo():
        subprocess.run(f'Powershell Get-Process|Select-Object ProcessName, Id, Path | Export-csv \'{os.getcwd()}\\Processes.csv\'')
    Collection = threading.Thread(target=ProcessInfo)
    subprocess.run(f'Powershell Get-NetTCPConnection|Select-Object OwningProcess, LocalAddress, LocalPort, State, RemoteAddress, RemotePort | Export-csv \'{os.getcwd()}\\TCPCon.csv\'')
    subprocess.run(f'Powershell Get-NetUDPEndpoint |Select-Object OwningProcess, LocalAddress, LocalPort|Export-csv \'{os.getcwd()}\\UDPCon.csv\'')
    Collection.start()
    Collection.join()


def DomainComputerTarget():
    InvalidDNSNameCh = ('`','~','!','@','#','$','%','^','&','(',')','=','+','_','[',']','{','}','\'',';','.',',','\\','/',':','*','?','\"','<','>','|')
    ComputerName = input('Please input a computer name.')
    NoSym = ''
    for Ch in InvalidDNSNameCh:
        if ComputerName.find(Ch) != -1:
            NoSym = NoSym+Ch
    if NoSym != '':
        print('A computer name cannot have these symbols ',NoSym,' in the name.\nRestart the program to try again.')
    else:
        print('You will be prompted twice for credentials...\nPlease press Space to continue')
        msvcrt.getch()
        subprocess.run(f'powershell $Access = get-credential; invoke-command {ComputerName} -credential $Access -ScriptBlock {{Get-process| Select-Object ProcessName, ID, Path| Export-csv RProcesses.csv; Get-NetTCPConnection| Select-Object OwningProcess, LocalAddress, LocalPort, State, RemoteAddress, RemotePort| Export-csv RTCPCon.csv; Get-NetUDPEndpoint| Select-Object OwningProcess, LocalAddress, LocalPort| Export-csv RUDPCon.csv; copy-item .\\RProcesses.csv,.\\RTCPCon.csv,.\\RUDPCon.csv -Destination \'{os.getcwd()}\' -ToSession (New-PsSession {socket.gethostname()} -credential $Access -EnableNetworkAccess) -ErrorAction silentlyContinue; Remove-item .\\RProcesses.csv,.\\RTCPCon.csv,.\\RUDPCon.csv}} -ErrorAction Stop')
        try:
            RProcesses = open('RProcesses.csv','r')
            RProcesses.close()
            RTCPCon = open('RTCPCon.csv','r')
            RTCPCon.close()
            RUDPCon = open('RUDPCon.csv','r')
            RUDPCon.close()
        except FileNotFoundError:
            exit('Something went wrong...\nEither Credentials were not correct or you do not have permission to complete the task.\nClosing the program.')

def ProcessID(Connections, ConnectionResult, Remote=''):
    with open(Connections,'r') as NCon: # Opening tcp or udp file that was created
        NConR = csv.DictReader(NCon)
        next(NCon)
        with open(f'{Remote}Processes.csv','r') as Processes: #Opening Processes.csv
            ProcessesR = csv.DictReader(Processes)
            next(Processes)
            with open(ConnectionResult,'w', newline='') as R: #Makes a new file 
                FName = NConR.fieldnames #top line of csv file
                FName.append('Path')
                RW = csv.DictWriter(R, FName) #initializing the csv filename and fieldname or header
                RW.writeheader() #Writing fieldnames to file 
                for Tag in NConR:
                    for PID in ProcessesR:
                        if Tag['OwningProcess'] == PID['Id']: #matching process id with the id of owning process
                            Tag['OwningProcess']  = PID['ProcessName']
                            Tag['Path'] = PID['Path']
                            RW.writerow(Tag) #this is writing the dictionary values to the row to the csv file
                    Processes.seek(0) #going back to top of processes.csv file and loop through this again
                    next(Processes)
        with open(ConnectionResult,'r') as ReadR: #opening another file which is the results file
            ReadRR = csv.DictReader(ReadR)
            for Line in ReadRR:
                pprint.pprint(Line)
                print('='*64)
            print('*'*128)
# This function is to delete the files.
def Clean(RVersion=''):
    os.remove(f'{RVersion}TCPCon.csv')
    os.remove('ConnectResultTCP.csv')
    os.remove(f'{RVersion}UDPCon.csv')
    os.remove('ConnectResultUDP.csv')
    os.remove(f'{RVersion}Processes.csv')



def options():
    def NoDomainVer():
        O = input('Range of ports, Windows based ports, Irrelevant ports, or Active Connections?\nType(Windows, range, irrelevant, or Active)\nType exit to leave the program: ')
        if O.lower() == 'windows':
            Windows_Ports()
        elif O.lower() == 'range':
            R('Everything Else!')
        elif O.lower() == 'irrelevant':
            R()
        elif O.lower() == 'active':
            Active_con()
            ProcessID('TCPCon.csv', 'ConnectResultTCP.csv')
            ProcessID('UDPCon.csv', 'ConnectResultUDP.csv')
            Clean()
        elif O.lower() == 'exit':
            exit('Bye! Bye!')
        else:
            NoDomainVer()
            exit()

    DomainStatusDict = {}
    print('Loading...')
    #Collecting computer information to check to see if it is part of a domain
    Domaininfo = subprocess.run('Powershell Get-ComputerInfo -Property csdomain,csdomainrole,CsPartOfDomain|Format-list', capture_output=True, text=True)
    DomainStatus = Domaininfo.stdout.strip().splitlines()
    for I in DomainStatus:
        Propertykey, PropertyValue = I.split(':')
        DomainStatusDict[Propertykey.strip()] = PropertyValue.strip()
    
    #asking if the user wants to run this program on another computer.
    if DomainStatusDict['CsDomainRole'] != 'StandaloneWorkstation' and DomainStatusDict['CsPartOfDomain'] == 'True':
        AdvancedDomainFeature = input(f'It appears that this computer is connected to a domain.\nWould you like to check up on another computer in %s? (y/n) '%(DomainStatusDict['CsDomain']))
        if AdvancedDomainFeature.lower() == 'y':
            DomainComputerTarget()  
            ProcessID('RTCPCon.csv', 'ConnectResultTCP.csv', 'R')
            ProcessID('RUDPCon.csv', 'ConnectResultUDP.csv', 'R')
            Clean('R')
            exit()
        elif AdvancedDomainFeature.lower() == 'n':
            print('OK')
            NoDomainVer()
            exit()
    NoDomainVer()
options()
