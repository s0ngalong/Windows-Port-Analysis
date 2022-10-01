# Windows-Port-Analysis
Scans local network ports and service identification

## About the project
With all the services and active connections on a computer, It can be difficult identifying what they are and what process is tied to them. This small application is designed to help metigate some of the most common ports within windows.<br>
Features include:<br>
- Scan known Windows ports
- - Scan a range of ports
- Scan all other non-assigned ports
- - Scan active ports
- - intigration with local domain environment


### Scan known windows ports
By comparing the table of known windows ports to open ports on the computer, a user is able to see what windows based ports are active and their respective services.
![output on a windows 10 machine after scanning windows based ports](/./Scanned%20windows%20ports.png)

#### Scan a range of ports
Just as it says. The program will scan a range of ports specified by the user.
![Output after scanning a range of ports](./Scanned%20range%20of%20ports.png)

##### Scanns irrelevant ports.
Scanns ports outside of the Windows Ports.csv table
![Output of irrelevant ports](./SCANNED%20IRRELEVANT.png)

###### Scan active ports
Collecting the open ports on a windows machine, the program will proceed to match them with their respective process ID.
![Output after scanning active ports on a windows 10 machine](./Scanned%20active.png)

####### Domain environment
In a Local Active Directory Domain enviornment, this program will prompt for the feature to start. Than a administrator can scan for active ports on a remote machine connected to the domain.
