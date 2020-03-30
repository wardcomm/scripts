# DBAAS-MSSQL
Ansible Repository for DBaaS playbooks for MSSQL servers

## Setting up a Windows Host

The setup that is required before Ansible can communicate with a Microsoft Windows host.

https://docs.ansible.com/ansible/2.5/user_guide/windows_setup.html

https://docs.ansible.com/ansible/2.5/user_guide/windows_winrm.html


#### Remote Machine
1.Run the "ConfigureRemotingForAnsible.ps1"
2.Run the below cmd
   Enable-WSManCredSSP -Role Server -Force

#### Local Machine(Ansible)
1.Install winrm
    pip install "pywinrm>=0.3.0"
2.Installing CredSSP Library
    pip install pywinrm[credssp]

## Roles
   The Script has following Ansible Roles

1. Physical 
   * Physical-Pre-Installation
   * Physical-Installation
   * Physical-Post-Installation

2. Virtual
   * Virtual-Post-Installation
   
3. AlwaysOn-setup
   * AlwaysOn-setup
        * CreateEmptyAvailabilityGroup-2-Node-with-DR
        * CreateEmptyAvailabilityGroup-2-Node
        * CreateEmptyAvailabilityGroup-3-Node

## Playbooks

1. Physcial 
    * Full Setup (Pre,installtion and Post)
        * Playbook: Physical-Full-Setup.yml

    * Splitup:
        * Physical-Pre-Installation Playbook: Physical-Pre-Installation.yml
        * Physical-installation Playbook: Physical-Installation.yml
        * Physical-Post-Installation Playbook: Physical-Post-Installation.yml

2. Virtual 
    * Post Installtion 
        * Playbook: Virtual-Post-installation.yml

3. AlwaysOn Setup
    * All Types
        * Playbook: AlwaysOn-Setup.yml

## Host Groups

Playbooks depend on host groups.

### Physical-Installation
#### Playbooks: 
* Physical-Pre-Installation.yml
* Physical-Installation.yml
* Physical-Post-Installation.yml
#### GroupName: 
* Physical-Windows #Need to Specify the hosts to run this setup

### Virtual-Installation
#### Playbook: 
* Virtual-Post-Installation.yml
#### GroupName: 
* Virtual-Windows #Need to Specify the hosts to run this setup

### AlwaysOn-Pre-Installation
#### Playbook: 
* AlwaysOn-Pre-Installation-2Node.yml
#### GroupName: 
* AlwaysOn-Pre-Installation-2Node #Need to Specify the 2 host to run this setup
#### Playbook: 
* AlwaysOn-Pre-Installation-3Node.yml
#### GroupName: 
* AlwaysOn-Pre-Installation-3Node #Need to Specify the 3 host to run this setup

### AlwaysOn-Setup
#### Playbooks: 
* AlwaysOn-2Node-With-DR.yml
* AlwaysOn-2Node.yml
* AlwaysOn-3Node.yml
#### GroupName: 
* AlwaysOn-Setup #Need to Specify only 1 host to run this setup

## Variables

#### Physical-Installation

    Physical-Pre-Installation and Physical-Installation
    #FTP Server Deatils
    unc: \\10.10.98.50\Charter_FileShare\CharterSQLInstallMedia
    unc_username: Administrator
    #Enter an Environment (LAB, DEV, UAT, TST, QA, SIT, DR, PRD)
    Env1: DEV
    #What Data Center is this being built in? (GVL, NCE, NCW)
    DC: GVL
    #What Domain is this being installed on? (CHTR, CORP, DEV, TWCCORP, TWZDMZ, UAT)
    Domain: CORP
    #Backup Path
    BuPath: E:\Backups
    #Data Path
    DataPath: E:\Data
    #Log Path
    LogPath: E:\Logs
    #System Path
    SystemPath: E:\System
    #Temdb Path
    TempdbPath: E:\Tempdb
    #Enter SQL Version (2012, 2014, 2016, 2017)
    SqlVersion: 2014

    Physical-Post-Installation (+ above Variables)

    #SQL MGT Server Details
    SQLInst: 10.10.98.50
    #Variables for SQLInst access Details
    database: master 
    username: admin
    # #  Enable TCP and Set port (enter "0" for Yes and "1" for No)
    resultTCP: 0 


#### Virtual-Post-Installation
    #FTP Server Details
    unc: \\10.10.98.50\Charter_FileShare\CharterSQLInstallMedia
    unc_username: Administrator
    # Env1 = "Enter an Environment (LAB, DEV, UAT, TST, QA, SIT, DR, PRD)"
    Env1: DEV
    #"Enter the Domain Name (CHTR, CORP, DEV, TWCCORP, TWZDMZ, UAT)"
    Domain: Corp
    #DC = "Enter the  Data Center is this being built in (GVL, NCE, NCW)"
    DC: GVL
    #Version = "What SQL Version is being installed? (2012, 2014, 2016)"
    SqlVersion: 2014
    #SQL MGT Server Details
    SQLInst: 10.10.98.50
    username: admin
    # #  Enable TCP and Set port (enter "0" for Yes and "1" for No)
    resultTCP: 0 

#### AlwaysOn-Pre-Installation

    AlwaysOn-Pre-Installation-2Node
    ipWSFC1: 10.10.98.150 # Cluster IP address
    nameWSFC: Charter-Cluster  
    node1: charter1.techlab.com
    node2: charter2.techlab.com

    AlwaysOn-Pre-Installation-2Node(+ above Variables)
    node3: charter3.techlab.com #DrReplica


#### AlwaysOn-Setup

    AlwaysOn-2Node
    #AAG-Security-Cleanup Need AD account
    Login: techlab\svc.sqladmin
    #CreateEmptyAvailabilityGroup-2-Node
    PrimaryReplica: charter1 #Specify the primary replica
    SecondaryReplica: charter2 #Specify the secondary replica
    EndPointPort: 5022 #Specify the port for the endpoints
    AvailabilityGroup: VS0 #Specify the name of the availability group
    Listener: VS0_VM0PWCYARADVS0 #Specify the name of the group listener
    IPListener: 10.10.98.157 #Specify the IP Address of the group listener
    ListenerPort: 1433 # Specify the listener port
    ListenerSubnet: 255.255.255.0 #Specify the subnet of the listeren IP Address
    
    AlwaysOn-2Node-With-DR(+ above Variables)
    #CreateEmptyAvailabilityGroup-2-Node-with-DR
    IPListener2: xxx #Specify the IP Address of the group listener
    ListenerSubnet2: xxx #Specify the subnet of the listeren IP Address
    

    AlwaysOn-3Node(+ above Variables)
    #CreateEmptyAvailabilityGroup-3-Node
    DrReplica: XXX #Specify the Dr replica
 


#### UPDATE THE ABOVE SECTION WITH THE VALUES NEEDED FOR YOU AVAILABLITY GROUP
#### REPLACE THE xxx WITH PROPER VALUES



 

