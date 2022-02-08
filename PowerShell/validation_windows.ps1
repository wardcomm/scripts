#######################################################################
# Charter Windows validation script
#
# version: 3.0.0.0
#
# copyright Charter Communications
#
# desc This script provides information about whether a
#       a server is in compliance with Charter Standards
#
#   The default report will output to:
#       C:\Windows\Temp\<hostname>_validation.log
#
# You can run it using:
#   PowerShell ISE
#   PowerShell Command Line
#   WMI
#
#   > validation_windows.ps1 cam.newton@charter.com
#   > validation_window.ps1 <any_other_email>
#
#   If you don't provide an email it will ask for one.
#
#######################################################################
param(
[string]$EmailIn,
[string]$LegacyIn
)
#############################
### Imports               ###
#############################
Clear-Host
Import-Module -Name ServerManager, ActiveDirectory, NetTCPIP

##############################
## Pre-Setup               ###
##############################

if ([string]::IsNullOrEmpty($EmailIn)) {
    $EmailIn = Read-Host -Prompt "Please provide an Email Address to receive report. Or press Enter to skip."
}
Clear-Host
Write-Host "Validation in progress. Please wait...."

#####################################
### Global Variables              ###
#####################################

# Result Array
$Global:ValidationResult = @()

# Logs, Registry, Email, etc
$Global:RemoteRegistry = [microsoft.win32.registrykey]::OpenRemoteBaseKey('Localmachine',$env:COMPUTERNAME)
$Global:LogFile = $env:COMPUTERNAME + "_" +  (Get-Date -Format "MM-dd-yyyy_HH-mm-ss").ToString() + ".log"
$Global:LogPath = "C:\Windows\Temp\"
New-Item "$LogPath$LogFile" -Force  | Out-Null
$Global:EmailAddress=$EmailIn

Write-Host "Gathering information..."
$Global:Apps = Get-WmiObject -Class Win32_Product

# Keys are stored 'SubBranch' = @("Keyname", "Value")
$NonPciRegKeys = @(
    @("SOFTWARE\Microsoft\Active Setup\Installed Components\{A509B1A8-37EF-4b3f-8CFC-4F3A74704073}", "IsInstalled", "0"),
    @("SOFTWARE\Microsoft\Active Setup\Installed Components\{A509B1A7-37EF-4b3f-8CFC-4F3A74704073}", "IsInstalled" , "0"),
    @("SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer", "NoDriveTypeAutoRun", "0xff"),
    @("SYSTEM\CurrentControlSet\Control\FileSystem", "NtfsDisable8dot3NameCreation","1"),
    @("SYSTEM\CurrentControlSet\Control\CrashControl", "AutoReboot", "1"),
    @("SYSTEM\CurrentControlSet\Control\CrashControl", "CrashDumpEnabled", "2"),
    @("SYSTEM\CurrentControlSet\Control\CrashControl", "Dumpfile", "C:\MEMORY.DMP"),
    @("SYSTEM\CurrentControlSet\Control\CrashControl", "LogEvent", "1"),
    @("SYSTEM\CurrentControlSet\Control\CrashControl", "Overwrite", "1"),
    @("SYSTEM\CurrentControlSet\Control\CrashControl", "SendAlert", "1"),
    @("SYSTEM\CurrentControlSet\Services\kbdhid\Parameters", "CrashOnCtrlScroll", "1"),
    @("SYSTEM\CurrentControlSet\Services\Tcpip6\Parameters", "DisabledComponents", "0x20"),
    @("SYSTEM\CurrentControlSet\Control\Terminal Server", "fDenyTSConnections", "0"),
    @("SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp", "UserAuthentication", "1"),
    @("Software\Microsoft\Windows\CurrentVersion\Policies\System","legalnoticecaption","Charter Communications Legal Notice"),
    @("Software\Policies\Microsoft\Windows\LLTD", "ProhibitLLTDIOOnPrivateNet", "0"),
    @("Software\Policies\Microsoft\Windows\LLTD", "EnableLLTDIO", "0"),
    @("Software\Policies\Microsoft\Windows\LLTD", "AllowLLTDIOOnPublicNet", "0"),
    @("Software\Policies\Microsoft\Windows\LLTD", "AllowLLTDIOOnDomain", "0"),
    @("Software\Policies\Microsoft\Windows\LLTD", "AllowRspndrOndomain", "0"),
    @("Software\Policies\Microsoft\Windows\LLTD", "AllowRspndrOnPublicNet", "0"),
    @("Software\Policies\Microsoft\Windows\LLTD", "EnableRspndr", "0"),
    @("Software\Policies\Microsoft\Windows\LLTD", "ProhibitRspndrOnPrivateNet", "0"),
    @("SOFTWARE\Microsoft\Windows NT\CurrentVersion\Setup\RecoveryConsole", "SecurityLevel", "0"),
    @("SOFTWARE\Microsoft\Windows NT\CurrentVersion\Setup\RecoveryConsole", "SetCommand", "0"),
    @("SOFTWARE\Policies\Microsoft\Windows\Network Connections", "NC_AllowNetBridge_NLA", "0"),
    @("SOFTWARE\Policies\Microsoft\Windows\Network Connections", "NC_ShowSharedAccessUI" , "0"),
    @("SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU", "NoAutoUpdate", "1"),
    @("SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System", "LocalAccountTokenFilterPolicy", "1"),
    @("SOFTWARE\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging", "EnableScriptBlockLogging", "1"),
    @("SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate","SetAutoRestartNotificationDisable", "1"),
    @("SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update","UpdatesAvailableForInstallLogon", "0"),
    @("SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update","UpdatesAvailableForDownloadLogon" , "0"),
    @("SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update","UpdatesAvailableWithUiLogon","0"),
    @("SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update", "UpdatesAvailableWithUiOrEulaLogon", "0")
)

# Keys are stored 'SubBranch' = @("Keyname", "Value")
$PciRegKeys = @(
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\Multi-Protocol Unified Hello\Client", "Enabled", "0"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\Multi-Protocol Unified Hello\Client", "DisabledByDefault", "1"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\Multi-Protocol Unified Hello\Server", "Enabled", "0"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\Multi-Protocol Unified Hello\Server", "DisabledByDefault", "1"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\PCT 1.0\Client", "Enabled", "0"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\PCT 1.0\Client", "DisabledByDefault", "1"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\PCT 1.0\Server", "Enabled", "0"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\PCT 1.0\Server", "DisabledByDefault", "1"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 2.0\Client", "Enabled", "0"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 2.0\Client", "DisabledByDefault", "1"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 2.0\Server", "Enabled", "0"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 2.0\Server", "DisabledByDefault", "1"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 3.0\Client", "Enabled", "0"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 3.0\Client", "DisabledByDefault", "1"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 3.0\Server", "Enabled", "0"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 3.0\Server", "DisabledByDefault", "1"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.0\Client", "Enabled", "0"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.0\Client", "DisabledByDefault", "1"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.0\Server", "Enabled", "0"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.0\Server", "DisabledByDefault", "1"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.1\Client", "Enabled", "0"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.1\Client", "DisabledByDefault", "1"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.1\Server", "Enabled", "0"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.1\Server", "DisabledByDefault", "1"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.2\Client", "Enabled", "1"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.2\Client", "DisabledByDefault", "0"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.2\Server", "Enabled", "1"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.2\Server", "DisabledByDefault", "0"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\AES 128/128", "Enabled", "0xffffffff"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\AES 256/256", "Enabled", "0xffffffff"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\DES 56/56", "Enabled" , "0"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\NULL", "Enabled", "0"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\RC2 128/128", "Enabled", "0"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\RC2 40/128", "Enabled", "0"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\RC2 56/128", "Enabled", "0"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\RC4 128/128", "Enabled", "0"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\RC4 40/128", "Enabled", "0"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\RC4 56/128", "Enabled", "0"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\RC4 64/128", "Enabled", "0"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\Triple DES 168", "Enabled", "0"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\","EventLogging","5"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Hashes\MD5","Enabled", "0"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Hashes\SHA","Enabled", "0"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Hashes\SHA256","Enabled", "0xffffffff"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Hashes\SHA384","Enabled", "0xffffffff"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Hashes\SHA512","Enabled", "0xffffffff"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\KeyExchangeAlgorithms\ECDH","Enabled", "0xffffffff"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\KeyExchangeAlgorithms\PKCS","Enabled", "0xffffffff"),
    @("SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\KeyExchangeAlgorithms\Diffie-Hellman","ServerMinKeyBitLength", "2048")
    @("SYSTEM\CurrentControlSet\Control\Cryptography\Configuration\Local\SSL", "Flags", "1"),
    @("SYSTEM\CurrentControlSet\Control\Cryptography\Configuration\Local\SSL\00010002", "", "NCRYPT_SCHANNEL_INTERFACE"),
    @("SYSTEM\CurrentControlSet\Control\Cryptography\Configuration\Local\SSL\00010003", "", "NCRYPT_SCHANNEL_SIGNATURE_INTERFACE")
)

# Determine which OS to compare ciphers for
Switch (((Get-WmiObject -Class Win32_OperatingSystem).Caption).Split(" ")[3]){
    2012{
        $OSCiphers = @("TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384_P256",
        "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256_P256",
        "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA_P256",
        "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA_P256",
        "TLS_DHE_RSA_WITH_AES_256_GCM_SHA384",
        "TLS_DHE_RSA_WITH_AES_128_GCM_SHA256",
        "TLS_DHE_RSA_WITH_AES_256_CBC_SHA",
        "TLS_DHE_RSA_WITH_AES_128_CBC_SHA",
        "TLS_RSA_WITH_AES_256_GCM_SHA384")
    }
# Default currently is anything not 2012R2, but is intended to  mean 2016 and 2019
    Default{
        $OSCurves = @("curve25519",
        "NistP256",
        "NistP384")
        $OSCiphers = @("TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
        "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
        "TLS_DHE_RSA_WITH_AES_256_GCM_SHA384",
        "TLS_DHE_RSA_WITH_AES_128_GCM_SHA256",
        "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384",
        "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256",
        "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA",
        "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA",
        "TLS_DHE_RSA_WITH_AES_256_CBC_SHA",
        "TLS_DHE_RSA_WITH_AES_128_CBC_SHA"
        "TLS_RSA_WITH_AES_256_GCM_SHA384")
        $OSFunctions = @("RSA/SHA256",
        "RSA/SHA384",
        "RSA/SHA1",
        "ECDSA/SHA256",
        "ECDSA/SHA384",
        "ECDSA/SHA1",
        "DSA/SHA1",
        "RSA/SHA512",
        "ECDSA/SHA512")
    }
}

# Added check to verify "order" of items denoting precedence
$Ciphers = [Array](Get-TlsCipherSuite).Name
$Curves = (Get-ItemProperty -Path "HKLM:SYSTEM\CurrentControlSet\Control\Cryptography\Configuration\Local\SSL\00010002" -ErrorAction Ignore).EccCurves
$Functions = (Get-ItemProperty -Path "HKLM:SYSTEM\CurrentControlSet\Control\Cryptography\Configuration\Local\SSL\00010003" -ErrorAction Ignore).Functions

# Windows Features and Roles that need to be present on the Server
$WindowsFeatures = @(
    "FileAndStorage-Services",
    "File-Services",
    "FS-FileServer",
    "Storage-Services",
    "NET-Framework-45-Core",
    "NET-WCF-Services45",
    "NET-WCF-TCP-PortSharing45", #.NET Framework TCP Sharing
	"Server-Media-Foundation",
	"RDC", #Remote Differential Compression
    "RSAT",
    "RSAT-AD-Tools",
    "RSAT-AD-PowerShell",
    "RSAT-ADDS",
    "RSAT-AD-AdminCenter",
    "RSAT-ADDS-Tools",
    "RSAT-ADLDS",
	"Telnet-Client",
    "PowerShell",
	"PowerShell-ISE",
	"WoW64-Support"
)

##June 2019
#Windows Features and Roles that need to be disabled
$DisabledWindowsFeatures = @(
    "(Get-SmbServerConfiguration).EnableSMB1Protocol",
    "File-Services",
    "FS-FileServer",
	"WoW64-Support"
)

#If the Windows Server Version is 2016 we need to check to make
#sure that windows defenders features are enabled.
$WinVer = (Get-WMIObject 'win32_operatingsystem').caption + " " + [environment]::OSVersion.Version
if ($WinVer -like "*Windows Server 2016*" ) {
    $WindowsFeatures += "Windows-Defender-Features"
    $WindowsFeatures += "Windows-Defender"
    $WindowsFeatures += "Windows-Defender-Gui"
}

#Manufactuerer is Dell - assumption for bare metal deployments - April 2019
if ( $HostInfo.Manufactuerer -match "Dell") {
    $WindowsFeatures += "SNMP-WMI-Provider"
}

######################################
### End System Variables           ###
######################################


######################################
### Host Information               ###
######################################

# System Generated Info for parsing.
Write-Host "Gathering system information..."
$sysinfo = systeminfo

# Get current site DC
$DC = (nltest /dsgetdc:corp.chartercom.com)[0]
$DC = $DC.Substring($DC.LastIndexOf("\\") + 2)

# Information gathered from the host.
$HostInfo = [ordered]@{
    'Hostname:' = $env:COMPUTERNAME
    'OS:' = (Get-WMIObject 'win32_operatingsystem').caption + " " + [environment]::OSVersion.Version
    'License Status' = ((cscript c:\windows\system32\slmgr.vbs /dli | find "License Status").split(':')[1]).Trim()
    'Manufacturer' = (Get-CimInstance CIM_ComputerSystem).Manufacturer
    'Serial Number:' = (Get-CimInstance CIM_BIOSElement).SerialNumber
    'Model:' = (Get-CimInstance CIM_ComputerSystem).Model
    'CPU Model' = (Get-CimInstance CIM_Processor).Name
    'CPUs:'=[string](Get-WMIObject win32_ComputerSystem | Select-Object "NumberOfLogicalProcessors").NumberOfLogicalProcessors
    'Memory:'=[string]([math]::round((Get-WmiObject Win32_OperatingSystem | ForEach-Object {$_.TotalVisibleMemorySize}) / 1KB, 0)) + " MB"
    'IPv4 Address' = (Get-NetIPConfiguration | Where-Object { $_.IPv4DefaultGateway -ne $null -and  $_.NetAdapter.Status -ne "Disconnected" }).IPv4Address.IPAddress
    'NTP:' = ((w32tm /query /peers | find "Peer: ").split(':')[1]).Trim()
    'Domain:'= (Get-CimInstance CIM_ComputerSystem).Domain
    'Domain Controller:'=$DC
    'Active Directory Site:'= (nltest /dsgetsite)[0]
    'Time Zone:' = (Get-WmiObject -Query "Select Caption from win32_timezone").Caption
}

# IP Address Info
$ipaddresses = Get-WmiObject -Query "SELECT * FROM Win32_NetworkAdapterConfiguration WHERE IPEnabled = True"
# Format for display
$ipaddresses = $ipaddresses | Format-Table @{ Label = "Metric"; Expression={$_.IPConnectionMetric}}, @{ Label = "IP Addresses"; Expression={$_.IPAddress[0]}}, Description, @{ Label = "Gateway"; Expression={$_.DefaultIPGateway}}

# Network Adapter Info
$adapter = Get-NetAdapter

######################################
### End of Host Information        ###
######################################

######################################
### Variable Declarations for CHTR ###
######################################

# An array for application information, This used to check against the applications installed on the system.
# Structure ([string]"Application Name",[string]Version)
$ChtrApplications = [ordered]@{
    'DTC' = @("ManageEngine Desktop Central - Agent","")
    'Netbackup' = @("Veritas NetBackup Client","")
    'Splunk' = @("UniversalForwarder","")
    'FireEye Endpoint Agent' = @("FireEye Endpoint Agent","")
    'Tripwire Agent' = @("Axon Agent","")
    'HP SA Agent' = @("HP SA Agent","")
    'Snow Inventory Agent' = @("Snow Inventory Agent", "")
    'Symantec Endpoint Protection' = @("Symantec Endpoint Protection","")
    'Centrify Agent for Windows 3.6.0.171' = @("Centrify Agent for Windows 3.6.0.171","")
    }

# Hash of Agent names, console servers and ports the host should be able to connect to
$LogonServer = $DC

# Attempt to determine AD site
If($NDC -eq ""){
    $NDC = (nltest /dsgetsite)[0].SubString(0,3)
    }

$DTC1 = @("Desktop Central Agent -10.64.170.47-135"),
    @("Desktop Central Agent -10.64.170.47-445"),
    @("Desktop Central Agent -10.64.170.47-8020"),
    @("Desktop Central Agent -10.64.170.47-8027"),
    @("Desktop Central Agent -10.64.170.47-8383")

$DTC2 = @("Desktop Central Agent -142.136.184.210-135"),
    @("Desktop Central Agent -142.136.184.210-445"),
    @("Desktop Central Agent -142.136.184.210-8020"),
    @("Desktop Central Agent -142.136.184.210-8027"),
    @("Desktop Central Agent -142.136.184.210-8383")

$TCPServerPorts = @(@("FireEye Agent -142.136.230.158-443"),
    @("FireEye Agent -142.136.230.158-80")
    @("SNOW Agent -agents.snow.chartercom.com-443"),
    @("Active Directory -$LogonServer-53"),
    @("Active Directory -$LogonServer-88"),
    @("Active Directory -$LogonServer-135"),
    @("Active Directory -$LogonServer-139"),
    @("Active Directory -$LogonServer-389"),
    @("Active Directory -$LogonServer-445"),
    @("Active Directory -$LogonServer-464"),
    @("Active Directory -$LogonServer-636"),
    @("Active Directory -$LogonServer-3268"),
    @("Active Directory -$LogonServer-3269")
  )

# Add environment specific servers - Default to UAT/Non-Prod
Switch($env:COMPUTERNAME.Substring(3,1)){
    P {
        $Tripwire = @("Tripwire Axon Agent -vm0pwtripwa0002.corp.chartercom.com-5670"),
        @("Tripwire Axon Agent -vm0pwtripwa0002.corp.chartercom.com-8080")
    }
    Default{
        $Tripwire = @("Tripwire Axon Agent -vm0uwtripwa0003.corp.chartercom.com-5670"),
        @("Tripwire Axon Agent -vm0uwtripwa0003.corp.chartercom.com-8080")
    }
}

# Add HPSA site specific servers - Default to NCE servers
Switch($NDC){
    "CDP" {
        $HPSA = @("HPSA Agent -165.237.179.115-3001"),
            @("HPSA Agent -165.237.179.116-3001")
        }
    "NCW" {
        $SEP = @("Symantec Agent -vm0pwsymepa0003.corp.chartercom.com-443"),
            @("Symantec Agent -vm0pwsymepw0004.corp.chartercom.com-443"),
            @("Symantec Agent -vm0pwsymepw0005.corp.chartercom.com-443"),
            @("Symantec Agent -vm0pwsymepw0006.corp.chartercom.com-443"),
            @("Symantec Agent -vm0pwsymepa0005.corp.chartercom.com-443")
        $HPSA = @("HPSA Agent -142.136.236.85-3001"),
            @("HPSA Agent -142.136.236.86-3001"),
            @("HPSA Agent -142.136.236.87-3001"),
            @("HPSA Agent -142.136.236.88-3001"),
            @("HPSA Agent -142.136.236.91-3001")
        $Splunk = @("Splunk Forwarder Agent -142.136.236.140-9997"),
            @("Splunk Forwarder Agent -142.136.236.141-9997"),
            @("Splunk Forwarder Agent -142.136.236.143-9997"),
            @("Splunk Forwarder Agent -142.136.236.144-9997"),
            @("Splunk Forwarder Agent -142.136.236.145-9997"),
            @("Splunk Forwarder Agent -142.136.236.146-9997"),
            @("Splunk Forwarder Agent -142.136.236.147-9997"),
            @("Splunk Forwarder Agent -142.136.236.148-9997"),
            @("Splunk Forwarder Agent -142.136.236.149-9997"),
            @("Splunk Forwarder Agent -142.136.236.150-9997"),
            @("Splunk Forwarder Agent -142.136.236.152-9997"),
            @("Splunk Forwarder Agent -142.136.236.157-9997"),
            @("Splunk Forwarder Agent -142.136.236.158-9997"),
            @("Splunk Forwarder Agent -142.136.236.161-9997"),
            @("Splunk Forwarder Agent -142.136.236.163-9997"),
            @("Splunk Forwarder Agent -142.136.236.164-9997"),
            @("Splunk Forwarder Agent -142.136.236.165-9997"),
            @("Splunk Forwarder Agent -142.136.236.166-9997"),
            @("Splunk Forwarder Agent -142.136.236.167-9997"),
            @("Splunk Forwarder Agent -142.136.236.168-9997"),
            @("Splunk Forwarder Agent -142.136.236.169-9997"),
            @("Splunk Forwarder Agent -142.136.236.170-9997"),
            @("Splunk Forwarder Agent -142.136.236.171-9997"),
            @("Splunk Forwarder Agent -142.136.236.172-9997"),
            @("Splunk Forwarder Agent -142.136.236.173-9997"),
            @("Splunk Forwarder Agent -142.136.236.174-9997"),
            @("Splunk Forwarder Agent -142.136.236.175-9997"),
            @("Splunk Forwarder Agent -142.136.236.176-9997"),
            @("Splunk Forwarder Agent -142.136.236.177-9997"),
            @("Splunk Forwarder Agent -142.136.236.178-9997"),
            @("Splunk Forwarder Agent -142.136.236.179-9997"),
            @("Splunk Forwarder Agent -142.136.236.180-9997"),
            @("Splunk Forwarder Agent -142.136.236.181-9997"),
            @("Splunk Forwarder Agent -142.136.236.182-9997"),
            @("Splunk Forwarder Agent -142.136.236.183-9997"),
            @("Splunk Forwarder Agent -142.136.236.184-9997"),
            @("Splunk Forwarder Agent -142.136.236.185-9997"),
            @("Splunk Forwarder Agent -142.136.236.187-9997"),
            @("Splunk Forwarder Agent -142.136.236.189-9997"),
            @("Splunk Forwarder Agent -142.136.236.190-9997"),
            @("Splunk Forwarder Agent -142.136.236.191-9997"),
            @("Splunk Forwarder Agent -142.136.236.192-9997"),
            @("Splunk Forwarder Agent -142.136.236.193-9997"),
            @("Splunk Forwarder Agent -142.136.236.194-9997"),
            @("Splunk Forwarder Agent -142.136.236.195-9997"),
            @("Splunk Forwarder Agent -142.136.236.196-9997"),
            @("Splunk Forwarder Agent -142.136.236.197-9997"),
            @("Splunk Forwarder Agent -142.136.236.198-9997"),
            @("Splunk Forwarder Agent -142.136.236.199-9997"),
            @("Splunk Forwarder Agent -142.136.236.200-9997")
        }
    "GVL" {
        $HPSA = @("HPSA Agent -172.24.209.126-3001"),
            @("HPSA Agent -172.24.209.127-3001"),
            @("HPSA Agent -172.24.209.128-3001"),
            @("HPSA Agent -172.24.209.129-3001"),
            @("HPSA Agent -172.24.209.130-3001")
        }
    # NCE is NOT specified as it is the "default" NDC
    Default {
        $SEP_NCE = @("Symantec Agent -vm0pwsymepw0013.corp.chartercom.com-443"),
            @("Symantec Agent -vm0pwsymepw0014.corp.chartercom.com-443"),
            @("Symantec Agent -vm0pwsymepw0015.corp.chartercom.com-443"),
            @("Symantec Agent -vm0pwsymepa0001.corp.chartercom.com-443"),
            @("Symantec Agent -vm0pwsymepa0002.corp.chartercom.com-443")
        $HPSA = @("HPSA Agent -142.136.251.47-3001"),
            @("HPSA Agent -142.136.251.48-3001"),
            @("HPSA Agent -142.136.251.49-3001")
        $Splunk = @("Splunk Forwarder Agent -142.136.251.140-9997"),
            @("Splunk Forwarder Agent -142.136.251.141-9997"),
            @("Splunk Forwarder Agent -142.136.251.142-9997"),
            @("Splunk Forwarder Agent -142.136.251.143-9997"),
            @("Splunk Forwarder Agent -142.136.251.145-9997"),
            @("Splunk Forwarder Agent -142.136.251.146-9997"),
            @("Splunk Forwarder Agent -142.136.251.147-9997"),
            @("Splunk Forwarder Agent -142.136.251.148-9997"),
            @("Splunk Forwarder Agent -142.136.251.149-9997"),
            @("Splunk Forwarder Agent -142.136.251.156-9997"),
            @("Splunk Forwarder Agent -142.136.251.157-9997"),
            @("Splunk Forwarder Agent -142.136.251.158-9997"),
            @("Splunk Forwarder Agent -142.136.251.159-9997"),
            @("Splunk Forwarder Agent -142.136.251.160-9997"),
            @("Splunk Forwarder Agent -142.136.251.161-9997"),
            @("Splunk Forwarder Agent -142.136.251.162-9997"),
            @("Splunk Forwarder Agent -142.136.251.163-9997"),
            @("Splunk Forwarder Agent -142.136.251.164-9997"),
            @("Splunk Forwarder Agent -142.136.251.165-9997"),
            @("Splunk Forwarder Agent -142.136.251.166-9997"),
            @("Splunk Forwarder Agent -142.136.251.167-9997"),
            @("Splunk Forwarder Agent -142.136.251.168-9997"),
            @("Splunk Forwarder Agent -142.136.251.170-9997"),
            @("Splunk Forwarder Agent -142.136.251.171-9997"),
            @("Splunk Forwarder Agent -142.136.251.172-9997"),
            @("Splunk Forwarder Agent -142.136.251.173-9997"),
            @("Splunk Forwarder Agent -142.136.251.174-9997"),
            @("Splunk Forwarder Agent -142.136.251.175-9997"),
            @("Splunk Forwarder Agent -142.136.251.176-9997"),
            @("Splunk Forwarder Agent -142.136.251.177-9997"),
            @("Splunk Forwarder Agent -142.136.251.178-9997"),
            @("Splunk Forwarder Agent -142.136.251.179-9997"),
            @("Splunk Forwarder Agent -142.136.251.180-9997"),
            @("Splunk Forwarder Agent -142.136.251.181-9997"),
            @("Splunk Forwarder Agent -142.136.251.182-9997"),
            @("Splunk Forwarder Agent -142.136.251.183-9997"),
            @("Splunk Forwarder Agent -142.136.251.184-9997"),
            @("Splunk Forwarder Agent -142.136.251.185-9997"),
            @("Splunk Forwarder Agent -142.136.251.186-9997"),
            @("Splunk Forwarder Agent -142.136.251.188-9997"),
            @("Splunk Forwarder Agent -142.136.251.189-9997"),
            @("Splunk Forwarder Agent -142.136.251.190-9997"),
            @("Splunk Forwarder Agent -142.136.251.191-9997"),
            @("Splunk Forwarder Agent -142.136.251.192-9997"),
            @("Splunk Forwarder Agent -142.136.251.193-9997"),
            @("Splunk Forwarder Agent -142.136.251.194-9997"),
            @("Splunk Forwarder Agent -142.136.251.195-9997"),
            @("Splunk Forwarder Agent -142.136.251.196-9997"),
            @("Splunk Forwarder Agent -142.136.251.197-9997"),
            @("Splunk Forwarder Agent -142.136.251.198-9997"),
            @("Splunk Forwarder Agent -142.136.251.199-9997"),
            @("Splunk Forwarder Agent -142.136.251.200-9997"),
            @("Splunk Forwarder Agent -142.136.236.140-9997"),
            @("Splunk Forwarder Agent -142.136.236.141-9997"),
            @("Splunk Forwarder Agent -142.136.236.143-9997"),
            @("Splunk Forwarder Agent -142.136.236.144-9997"),
            @("Splunk Forwarder Agent -142.136.236.145-9997"),
            @("Splunk Forwarder Agent -142.136.236.146-9997"),
            @("Splunk Forwarder Agent -142.136.236.147-9997"),
            @("Splunk Forwarder Agent -142.136.236.148-9997"),
            @("Splunk Forwarder Agent -142.136.236.149-9997"),
            @("Splunk Forwarder Agent -142.136.236.150-9997"),
            @("Splunk Forwarder Agent -142.136.236.152-9997"),
            @("Splunk Forwarder Agent -142.136.236.157-9997"),
            @("Splunk Forwarder Agent -142.136.236.158-9997"),
            @("Splunk Forwarder Agent -142.136.236.161-9997"),
            @("Splunk Forwarder Agent -142.136.236.163-9997"),
            @("Splunk Forwarder Agent -142.136.236.164-9997"),
            @("Splunk Forwarder Agent -142.136.236.165-9997"),
            @("Splunk Forwarder Agent -142.136.236.166-9997"),
            @("Splunk Forwarder Agent -142.136.236.167-9997"),
            @("Splunk Forwarder Agent -142.136.236.168-9997"),
            @("Splunk Forwarder Agent -142.136.236.169-9997"),
            @("Splunk Forwarder Agent -142.136.236.170-9997"),
            @("Splunk Forwarder Agent -142.136.236.171-9997"),
            @("Splunk Forwarder Agent -142.136.236.172-9997"),
            @("Splunk Forwarder Agent -142.136.236.173-9997"),
            @("Splunk Forwarder Agent -142.136.236.174-9997"),
            @("Splunk Forwarder Agent -142.136.236.175-9997"),
            @("Splunk Forwarder Agent -142.136.236.176-9997"),
            @("Splunk Forwarder Agent -142.136.236.177-9997"),
            @("Splunk Forwarder Agent -142.136.236.178-9997"),
            @("Splunk Forwarder Agent -142.136.236.179-9997"),
            @("Splunk Forwarder Agent -142.136.236.180-9997"),
            @("Splunk Forwarder Agent -142.136.236.181-9997"),
            @("Splunk Forwarder Agent -142.136.236.182-9997"),
            @("Splunk Forwarder Agent -142.136.236.183-9997"),
            @("Splunk Forwarder Agent -142.136.236.184-9997"),
            @("Splunk Forwarder Agent -142.136.236.185-9997"),
            @("Splunk Forwarder Agent -142.136.236.187-9997"),
            @("Splunk Forwarder Agent -142.136.236.189-9997"),
            @("Splunk Forwarder Agent -142.136.236.190-9997"),
            @("Splunk Forwarder Agent -142.136.236.191-9997"),
            @("Splunk Forwarder Agent -142.136.236.192-9997"),
            @("Splunk Forwarder Agent -142.136.236.193-9997"),
            @("Splunk Forwarder Agent -142.136.236.194-9997"),
            @("Splunk Forwarder Agent -142.136.236.195-9997"),
            @("Splunk Forwarder Agent -142.136.236.196-9997"),
            @("Splunk Forwarder Agent -142.136.236.197-9997"),
            @("Splunk Forwarder Agent -142.136.236.198-9997"),
            @("Splunk Forwarder Agent -142.136.236.199-9997"),
            @("Splunk Forwarder Agent -142.136.236.200-9997"),
            @("Splunk Forwarder Agent -142.136.236.140-9997"),
            @("Splunk Forwarder Agent -142.136.236.141-9997"),
            @("Splunk Forwarder Agent -142.136.236.143-9997"),
            @("Splunk Forwarder Agent -142.136.236.144-9997"),
            @("Splunk Forwarder Agent -142.136.236.145-9997"),
            @("Splunk Forwarder Agent -142.136.236.146-9997"),
            @("Splunk Forwarder Agent -142.136.236.147-9997"),
            @("Splunk Forwarder Agent -142.136.236.148-9997"),
            @("Splunk Forwarder Agent -142.136.236.149-9997"),
            @("Splunk Forwarder Agent -142.136.236.150-9997"),
            @("Splunk Forwarder Agent -142.136.236.152-9997"),
            @("Splunk Forwarder Agent -142.136.236.157-9997"),
            @("Splunk Forwarder Agent -142.136.236.158-9997"),
            @("Splunk Forwarder Agent -142.136.236.161-9997"),
            @("Splunk Forwarder Agent -142.136.236.163-9997"),
            @("Splunk Forwarder Agent -142.136.236.164-9997"),
            @("Splunk Forwarder Agent -142.136.236.165-9997"),
            @("Splunk Forwarder Agent -142.136.236.166-9997"),
            @("Splunk Forwarder Agent -142.136.236.167-9997"),
            @("Splunk Forwarder Agent -142.136.236.168-9997"),
            @("Splunk Forwarder Agent -142.136.236.169-9997"),
            @("Splunk Forwarder Agent -142.136.236.170-9997"),
            @("Splunk Forwarder Agent -142.136.236.171-9997"),
            @("Splunk Forwarder Agent -142.136.236.172-9997"),
            @("Splunk Forwarder Agent -142.136.236.173-9997"),
            @("Splunk Forwarder Agent -142.136.236.174-9997"),
            @("Splunk Forwarder Agent -142.136.236.175-9997"),
            @("Splunk Forwarder Agent -142.136.236.176-9997"),
            @("Splunk Forwarder Agent -142.136.236.177-9997"),
            @("Splunk Forwarder Agent -142.136.236.178-9997"),
            @("Splunk Forwarder Agent -142.136.236.179-9997"),
            @("Splunk Forwarder Agent -142.136.236.180-9997"),
            @("Splunk Forwarder Agent -142.136.236.181-9997"),
            @("Splunk Forwarder Agent -142.136.236.182-9997"),
            @("Splunk Forwarder Agent -142.136.236.183-9997"),
            @("Splunk Forwarder Agent -142.136.236.184-9997"),
            @("Splunk Forwarder Agent -142.136.236.185-9997"),
            @("Splunk Forwarder Agent -142.136.236.187-9997"),
            @("Splunk Forwarder Agent -142.136.236.189-9997"),
            @("Splunk Forwarder Agent -142.136.236.190-9997"),
            @("Splunk Forwarder Agent -142.136.236.191-9997"),
            @("Splunk Forwarder Agent -142.136.236.192-9997"),
            @("Splunk Forwarder Agent -142.136.236.193-9997"),
            @("Splunk Forwarder Agent -142.136.236.194-9997"),
            @("Splunk Forwarder Agent -142.136.236.195-9997"),
            @("Splunk Forwarder Agent -142.136.236.196-9997"),
            @("Splunk Forwarder Agent -142.136.236.197-9997"),
            @("Splunk Forwarder Agent -142.136.236.198-9997"),
            @("Splunk Forwarder Agent -142.136.236.199-9997"),
            @("Splunk Forwarder Agent -142.136.236.200-9997")
        }
    }

$TCPServerPorts += $Tripwire
$TCPServerPorts += $HPSA

# HashMap for services that need to be checked.
$ChtrServices = [ordered]@{
    'DTC' = "manageengine desktop central - agent"
    'Netbackup' = "NetBackup Client Service"
    'Splunk' = "SplunkForwarder Service"
    'FireEye Endpoint Agent' = "xagt"
    'Tripwire Agent' = "Tripwire Axon Agent"
    'HP SA Agent' = "OpswareAgent"
    'Symantec Endpoint Protection' = "Symantec Endpoint Protection"
    'Qualys Cloud Agent' = "Qualys Cloud Agent"
    'Centrify Agent Logger Service' = "Centrify Agent Logger"
}

# Array of  services that need to be disabled.
$ChtrDisabledServices = @(
    "AudioEndpointBuilder",
    "Audiosrv",
    "bthserv",
    "CDPUserSvc",
    "FrameServer",
    "icssvc",
    "lfsvc",
    "MapsBroker",
    "NcbService",
    "NgcCtnrSvc",
    "NgcSvc",
    "OneSyncSvc",
    "PcaSvc",
    "PimIndexMaintenanceSvc",
    "QWAVE",
    "RmSvc",
    "RasAuto",
    "RasMan",
    "Spooler",
    "SensorDataService",
    "SensorService",
    "SensrSvc",
    "SharedAccess",
    "ShellHWDetection",
    "SSDPSRV",
    "stisvc",
    "TabletInputService",
    "UnistoreSvc",
    "upnphost",
    "UserDataSvc",
    "WalletService",
    "WiaRpc",
    "wisvc",
    "wlidsvc",
    "WpnService",
    "WpnUserService",
    "XblAuthManager",
    "XblGameSave"
)

$ChtrDisabledTasks = @(
    "XblGameSaveTask",
    "XblGameSaveTaskLogon"
)

if ($sysinfo -match "VMware") {
   $ChtrServices.Add('VMware Tools', "vmware tools")
}

# Admin Users/Groups that should be present on the server
$ChtrAdminGroup = @(
    "RG-DC-WINDOWS-OPS-ADM",
    "WinAdmin",
    "itops.admin",
    "ADM-IT-Infrastructure-SvrBuild",
    "ADM-ITS-Corp-EDC-Standards",
    "ADM-IT-Infrastructure-WinSvcAccounts"
)

# PerfMon Users/Groups that should be present on the server
$ChtrPerfGroup = @(
    "svc_solarwinds"
)

# OU that the computer object should reside in
$ChtrOrgUnit = "OU=Production,OU=DC_Operations,OU=Enterprise,DC=CORP,DC=CHARTERCOM,DC"

############################################
### End of Variable Declaration for CHTR ###
############################################


#########################
### Functions        ####
#########################

 <#
    Create-BigSeparator

    .SYNOPSIS
        Creates a separator for text output in the console.
    .DESCRIPTION
       Creates a separator to divide section of text. It is written to stdout of the current console this script
       is run on.
    .PARAMETERS
        $SeparatorName{string} - The name that will appear in the separator.
    .EXAMPLE
        Create-BigSeparator "Host Validation"
#>

Function Create-BigSeperator($SeparatorName ) {
    $Sep_out = "#################################
$SeparatorName
#################################"
    $Sep_out | Out-File -FilePath "$Global:LogPath$Global:LogFile" -Append
}

 <#
    Create-TimeStamp

    .SYNOPSIS
        Creates a Time Stamp
    .DESCRIPTION
       Create a time stamp using the current date on the machine and writes it to stdout.
    .PARAMETER
        None
    .EXAMPLE
        Create-TimeStamp
#>

Function Create-TimeStamp() {
    $time =  "Timestamp:" + " " + (Get-Date).ToString()
    Write-Host $time
    $time | Out-File -FilePath "$Global:LogPath$Global:LogFile" -Append
}

 <#
    Export-Env

    .SYNOPSIS
        Dumps envirnment information
    .DESCRIPTION
       Exports certain powershell environmental information to the output log
    .PARAMETER
        None
    .EXAMPLE
        Export-Env
#>

Function Export-Env() {
    $UEnv =  "**********************`r`n"
    $UEnv += "Start time: " + (Get-Date).DateTime + "`r`n"
    $UEnv += "Username: " + [System.Security.Principal.WindowsIdentity]::GetCurrent().Name + "`r`n"
    $UEnv += "Machine: $env:COMPUTERNAME (" + [environment]::OSVersion.VersionString +")" + "`r`n"
    $UEnv += "Process ID: " + $PID + "`r`n"
    ForEach($item in $PSVersionTable.Keys) {
        $UEnv += $item + ": " + $($PSVersionTable.$($item)) + "`r`n"
        }
    $UEnv +=  "**********************"
    $UEnv | Out-File -FilePath "$Global:LogPath$Global:LogFile" -Append
}


<#
    Check-Value

    .SYNOPSIS
        This function act as an if then gateway for simple if then functions it reduces
        the necesity to retype simple if/then functions to perform simple logic
    .DESCRIPTION
        The function accepts $VariableIn and uses a switch case on $Operator to create
        conditional statement that compares $VariableIn and Value based on the $Operator.
         If the result of the conditional is true the function will load a validation object
        with "PASS" $Message $Config. If the result of the conditional is false the function
        will load a validation object with "FAIL" $Message $Config
    .PARAMETERS
        $VariableIn{pointer} - The variable you wish to check
        $Operator{string} - The logical operator you wish to use right now it only supports(-like,-match,-contains,-eq)
        $Value{any} - The value you wish to check againts $VariableIn using $Operator
        $Message{string} - The Message you wish to provide for validation based on the results of the check.
        $Config{string} - The particular configuration filter you wish to use for the check.
    .EXAMPLE
        $NetAdapter = Get-NetAdapter
        Check-Value $NetAdapter.LinkSpeed "eq" "10 Gbs" "Check that the link speed is 10 Gbs" "CONFIG"
#>

Function Check-Value($VariableIn, $Operator, $Value, $Message, $Config) {
    switch ($Operator) {
        like {
            if ($VariableIn -like $Value) {
                Load-ValidationObject "PASS" $Message $Config
            } else {
                Load-ValidationObject "FAIL" $Message $Config
            }
        }
        notlike {
            if ($VariableIn -notlike $Value) {
                Load-ValidationObject "PASS" $Message $Config
            } else {
                Load-ValidationObject "FAIL" $Message $Config
            }
        }
        match {
            if ($VariableIn -match $Value) {
                Load-ValidationObject "PASS" $Message $Config
            } else {
                Load-ValidationObject "FAIL" $Message $Config
            }
        }
        notmatch {
            if ($VariableIn -notmatch $Value) {
                Load-ValidationObject "PASS" $Message $Config
            } else {
                Load-ValidationObject "FAIL" $Message $Config
            }
        }
        contains {
            if ($VariableIn -contains $Value) {
                Load-ValidationObject "PASS" $Message $Config
            } else {
                Load-ValidationObject "FAIL" $Message $Config
            }
        }
        notcontains {
            if ($VariableIn -notcontains $Value) {
                Load-ValidationObject "PASS" $Message $Config
            } else {
                Load-ValidationObject "FAIL" $Message $Config
            }
        }
        eq {
            if ($VariableIn -eq $Value) {
                Load-ValidationObject "PASS" $Message $Config
            } else {
                Load-ValidationObject "FAIL" $Message $Config
            }
        }
        ne {
            if ($VariableIn -ne $Value) {
                Load-ValidationObject "PASS" $Message $Config
            } else {
                Load-ValidationObject "FAIL" $Message $Config
            }
        }
        ge {
            if ($VariableIn -ge $Value) {
                Load-ValidationObject "PASS" $Message $Config
            } else {
                Load-ValidationObject "FAIL" $Message $Config
            }
        }
        le {
            if ($VariableIn -le $Value) {
                Load-ValidationObject "PASS" $Message $Config
            } else {
                Load-ValidationObject "FAIL" $Message $Config
            }
        }
    }
}

<#
    Check-PCIArray

    .SYNOPSIS
        This function will compare array contents for not only a match but also to verify
        the corresponing element's position in that array.
    .DESCRIPTION
        This function was primarily intended to be used against ciphers as their order also
        denotes their preference in connectivity.
    .PARAMETER
        $test = @("string", "string", "string") - The array you wish to test
        $required = @("string", "string", "string") - The array items required to pass
    .EXAMPLE
        $required = @("myvalue1",
            "myvalue2",
            "myvalue3")
            )
        $found = (Get-ItemProperty -Path <<location whose value is an array or object>>).SomeProperty
        Check-PCIArray -Required $required -Found $found
#>

Function Check-PCIArray($Required, $Found){
    For($idx = 0; $idx -lt $Required.Count ; $idx++){
        If(!$Found[$idx] -eq $Required[$idx]){
            $msg = "Missing item: " + $Required[$idx] + "."
            Load-ValidationObject "FAIL" $msg "PCI"
        }
        Else{
            $msg = "PASS - Required item: " + $Required[$idx] + " was found."
            Load-ValidationObject "PASS" $msg "PCI"
        }
    }
}

 <#
    Lookup-RegKeys

    .SYNOPSIS
        This function will lookup a key in the registry hive and compare it to the
        corresponing key that is provided.
    .DESCRIPTION
        This function accepts an array of Registry branches, keys, value and checks to make
        sure that the value provided is present in the registry.
    .PARAMETER
        $RegArray{array}{"string", "string", "string"} - The array of keys you wish to lookup,
    .EXAMPLE
        $Keys = @(
            @("Key1\Location", "Enabled", "0")
            @("Key2\Location", "Enabled", "0")
        )
        Lookup-RegKeys $Keys
#>

Function Lookup-RegKeys($RegArray) {
    Foreach ($item in $RegArray) {
        $SubBranch = $item[0]
        $Key = $item[1]
        $Value = $item[2]
        $RegistryKey=$RemoteRegistry.OpenSubKey($SubBranch)
        $KeyValue=$RegistryKey.GetValue($Key)

        if ($KeyValue -eq $Value) {
            $msg = "HKLM:$SubBranch\$Key is correct." # (Desired=$Value vs Current=$KeyValue)"
            Load-ValidationObject "PASS" $msg "REG"
        }
        else {
            if ($KeyValue -eq $null) {
                $KeyValue = "Null"
            }
            $msg = "HKLM:$SubBranch\$Key has the incorrect value. (Desired=$Value vs Current=$KeyValue)"
            Load-ValidationObject "FAIL" $msg  "REG"
        }
    }
}

<#
    Check-WindowsFeature

    .SYNOPSIS
        This will check to make sure Windows Features are installed.
    .DESCRIPTION
        This wwill return the value of a registry key at the location specified.
    .PARAMETER
        $WindowsFeature{array} - The array features that you wish to check.
    .EXAMPLE
        $WinFeature = @(
            "Feature1",
            "Feature2"
        )
        Check-WindowsFeature $WinFeature
#>

Function Check-WindowsFeature($WindowsFeatures) {
    Foreach ($item in $WindowsFeatures) {
       $Feature =  Get-WindowsFeature -Name $item -ErrorAction SilentlyContinue
       if ($Feature.InstallState -eq "Installed") {
            $msg = $item + " is installed on the server."
            Load-ValidationObject "PASS" $msg "FEA"
       } else {
            $msg = $item + " is not installed on the server."
            Load-ValidationObject "FAIL" $msg "FEA"
       }
    }
}

# Check SMB
Function Check-DisabledWindowsFeature(){
    $SMB =  (Get-SmbServerConfiguration).EnableSMB1Protocol
    if ($SMB -eq $false) {
        $msg = "SMB1Protocol is disabled on this server"
        Load-ValidationObject "PASS" $msg "FEA"
    } else {
        $msg = "SMB1Protocol is enabled on this server"
    Load-ValidationObject "FAIL" $msg "FEA"
    }
}

<#
    Check-ScheduledTaskState

    .SYNOPSIS
        Check an array of Task and make sure they match the provided state.
    .DESCRIPTION
       This funciton accepts and array of Strings (Task names I.E.) and will
       check make sure theu match the state passed to the function.
    .PARAMETER
        $ScheduledTasks{array} - The tasks that will be checked
        $State{string} - The state you wish to check the task for.
    .EXAMPLE
        $Tasks = @(
            "WinTask1",
            "WinTask2"
        )
        $State = "Disabled"
        Check-ScheduledTaskState $Tasks $State
#>

Function Check-ScheduledTaskState($ScheduledTasks, $State) {
    Foreach ($item in $ScheduledTasks) {
        $TaskState = (Get-ScheduledTask -TaskName $item -ErrorAction SilentlyContinue).State
        if ($TaskState -eq $State) {
            Load-ValidationObject "PASS" "Task $item should be $state" "TASK"
        } elseif ($TaskState -eq $null) {
            Load-ValidationObject "INFO" "Task $item was not found in scheduled Tasks." "TASK"
        } else {
            Load-ValidationObject "FAIL" "Task $item should be $State" "TASK"
        }
    }
}

<#
    Load-ValidationObject

    .SYNOPSIS
        Allows results from validation to be load into an object array
    .DESCRIPTION
        This method will add new Powershell Objects to the Validation array based on specification. You can load text
        in as and object by running the function i.e. Load-ValidationObject "PASS" "This is was a test for something" "HOST"
    .PARAMETERS
        $Result{string} - The result of the Validation check
        $Description{string} - The description of the check that was performed.
        $Type{string} - The type of check. (This is used more as a filter to sort the objects.)
    .EXAMPLE
        Load-ValidationObject "PASS" "This was something I was validating" "HOST"
#>

Function Load-ValidationObject($Result, $Description, $Type) {
    $ValidationResultProperty =  [ordered]@{
        Result = $Result
        Description = $Description
        Type = $Type
    }
    $ValidationObject = New-Object -TypeName PSObject -Property $ValidationResultProperty
    $Global:ValidationResult += $ValidationObject
}

 <#
    Parse-HostName

    .SYNOPSIS
        Will parse the characters of a host name to determine what kind of server it is.
    .DESCRIPTION
        For cases when the hostname is larger or smaller than 15 characters this function
        will return with a fail and will not parse any further.
    .PARAMETERS
        None
    .EXAMPLE
        Parse-HostName
#>

Function Parse-HostName() {
    $SwtichResult=""

    # Check the hostname length to make sure it is 15 characters.
    If ($env:COMPUTERNAME.Length -ne 15) {
        If (($env:COMPUTERNAME).StartsWith("TEST")){
            Load-ValidationObject "PASS" "$ENV:ComputerName appears to be a 'test' server. Hostname checks will be skipped."  "HOST"
        }
    Else{
        Load-ValidationObject "WARN" "Hostname is not 15 characters. Please check the hostname!"  "HOST"
        }
    Return
    }

    # Determine the Hardware (if any)
    switch ( $env:COMPUTERNAME.Substring(0,3) )
    {
        vm0 { $Hardware = "Server is a Virtual Machine"; $SwitchResult="INFO"  }
        default { $Hardware = "Server is a physical server." ; $SwitchResult="INFO"  }
    }
    Load-ValidationObject $SwitchResult $Hardware "HOST"

    # Determine the environment
    switch ( $env:COMPUTERNAME.Substring(3,1) )
    {
        P { $Environment = "Environment is Production"; $SwitchResult="INFO" }
        U { $Environment = "Environment is UAT"; $SwitchResult="INFO" }
        L { $Environment = "Environment is Lab"; $SwitchResult="INFO" }
        D { $Environment = "Environment is Dev, QA, Test"; $SwitchResult="INFO" }
        R { $Environment = "Environment is DR"; $SwitchResult="INFO" }
        default {
            If( $env:COMPUTERNAME.Substring(0,4) -like "test"){
                $Environment = "Environment is Dev, QA, Test"; $SwitchResult="INFO" 
                }
            Else{
                $Environment = "WARN - Environment could not be determined from host name."; $SwitchResult="WARN" 
                }
            }
    }
    Load-ValidationObject $SwitchResult $Environment "HOST"

    # Determine the operating system.
    switch ( $env:COMPUTERNAME.Substring(4,1) )
    {
        W { $OS = "This is a Windows System"; $SwitchResult="INFO" }
        A { $OS = "This is an Appliance"; $SwitchResult="INFO" }
        default { $OS = "OS should be Windows, but hostname says otherwise."; $SwitchResult="WARN" }
    }
    Load-ValidationObject $SwitchResult $OS "HOST"

    # Determine the type of server
    switch ( $env:COMPUTERNAME.Substring(10,1) )
    {
        A { $Type = "Application Server"; $SwitchResult="INFO" }
        W { $Type = "Web Server"; $SwitchResult="INFO" }
        D { $Type =  "Database Server"; $SwitchResult="INFO" }
        default { $Type = "Could not determine server type from hostname."; $SwitchResult="WARN" }
    }
    Load-ValidationObject $SwitchResult $Type "HOST"
}

 <#
    Check-Services

    .SYNOPSIS
        Checks the services on a system to confirm if they are running or not.
    .DESCRIPTION
        This function accepts an array of applications, which contain strings used for validating
        whether services are running or not
    .PARAMETERS
        $Services{hashmap} - The services that you wish to check that are running
    .EXAMPLE
        $Services = [ordered]@(
            'Service1' = "A service",
            'Service2' = "Another service"
        )
        Check-Services $Services
#>

Function Check-Services($Services) {
    $Services.Keys | % {
        $srv = Get-Service $Services.Item($_) -ErrorAction SilentlyContinue
        if ($srv.Name -ne $null -and $srv.Status -eq "Running") {
            $msg = $_ + " is currently running."
            Load-ValidationObject "PASS" $msg "SRV"
        } else {
            $msg = $_  + " is currently not running."
            Load-ValidationObject "FAIL" $msg "SRV"
        }
    }
}

<#
    Check-ServiceStartMode

    .SYNOPSIS
        Checks an array of services to determine if they are in the user
        Provided Mode.
    .DESCRIPTION
        This function will check the win32_services to determine if the desired start
        mode for the services sent in the array are equal.
    .PARAMETERS
        $Services{array}- An array of Service Names that will checked.
        $DesiredStartMode{string} - The state to compare each of service in the array to.
    .EXAMPLE
        $Services = @(
            "WinService1",
            "WinService2"
        )
        $StartMode = "Disabled"
        Check-ServiceStartMode $Services $StartMode
#>

Function Check-ServiceStartMode ($Services, $DesiredStartMode) {
    Foreach ($item in $Services) {
        $ServiceStartMode = (Get-WMIObject win32_service -filter "name='$item'" -computer $env:ComputerName).StartMode
        if ($ServiceStartMode -eq $DesiredStartMode) {
            $msg = "$item service start mode is $DesiredStartMode"
            Load-ValidationObject "PASS" $msg "DSRV"
        } elseif ($ServiceStartMode -eq $null) {
            $msg ="$item service was not found."
            Load-ValidationObject "INFO" $msg "DSRV"
        } else {
            $msg = "$item service start mode is not $DesiredStartMode"
            Load-ValidationObject "FAIL" $msg "DSRV"
        }
    }
}

 <#
    Check-DNS

    .SYNOPSIS
    Checks DNS for the record passed.
    .DESCRIPTION
        This function will check the if the provided record exist in DNS. It will try to resolve the name or IP
        If it cannot it will throw an exception and output as a FAIL.
    .PARAMETER
        $Record{string} - The Record you wish to check
        $Type{string} - The type of record "Forward" "Reverse". It is just for display purposes.
    .EXAMPLE
        Check-DNS "172.24.120.7" "Reverse"
        Check-DNS "corp.chartercom.com" "Forward"
#>

Function Check-DNS($Record, $Type) {
    try {
        $DNS = [System.Net.Dns]::GetHostAddresses($Record)
        $msg =  $Type + " lookup works for " + $Record
        Load-ValidationObject "PASS" $msg "CONFIG"
    }
    catch {
        $msg =  $Type + " lookup fails for " + $Record
        Load-ValidationObject "FAIL" $msg "CONFIG"
    }
}

 <#
    Check-LogicalDisks

    .SYNOPSIS
        Check the disk on the system and shows their size
    .DESCRIPTION
        This function will output all of the disks on the system and will show the sizes
        in GB.
    .PARAMETERS
        None
    .EXAMPLE
        Check-LogicalDisks
#>

Function Check-LogicalDisks() {
    $Disks = Get-WmiObject -Class Win32_LogicalDisk -Filter "DriveType=3" | Sort-Object -Property Name
    $Global:Log += "Logical Disk Info:"
	ForEach ($LDisk in $Disks)
	{
		$Size = ($LDisk.Size/1GB).ToString(".00")
		$Free = "(" + ($LDisk.FreeSpace/1GB).ToString(".00") + " GB Free)"
		$LDrive = $LDisk.DeviceID
		$Global:Log +=  " - $LDrive $Size GB $Free"
	}
}

<#
    Check-PhysicalDisks

    .SYNOPSIS
        Check the disks on the system to show if any unextended partitions exist.
    .DESCRIPTION
        This function will output all of the disks on the system and will show if there
        any partitions that are unextended.
    .PARAMETERS
        None
    .EXAMPLE
        Check-PhysicalDisks
#>

Function Check-PhysicalDisks() {
    $PDisks = Get-WmiObject -Class Win32_DiskDrive | Sort-Object -Property Index
    ForEach ($PDisk in $PDisks) {
	    [long]$DiskPartSize = 0
	    $PDiskSize = $PDisk.Size
	    If ($PDisk.Partitions -gt 1) {
		    ForEach($Partition in $PDisk.GetRelated("Win32_DiskPartition")) {
			    $DiskPartSize = ($DiskPartSize + $Partition.Size)
		    }
	    } Else {
		    $Partition = $PDisk.GetRelated("Win32_DiskPartition")
		    $DiskPartSize = $Partition.Size
	    }
	    If (($PDiskSize - $DiskPartSize)/1GB -ge 4) {
		    $msg = ($PDisk.Name).replace('\\.\',"") + "' has one or more unextended partitions."
            Load-ValidationObject "FAIL" $msg "CONFIG"
	    } Else {
		    $msg = ($PDisk.Name).replace('\\.\',"") + "' has no unextended partitions."
            Load-ValidationObject "PASS" $msg "CONFIG"
        }
    }
}

 <#
    Check-Applications

    .SYNOPSIS
    Checks the applications on a system to determine if they are installed
    .DESCRIPTION
        This function will check to ensure that the application passed to the function
        are found in Add/Remove programs (Win32_Product). This will not check the version
        passed. You will have to add that functionality if you need it.
    .PARAMETERS
        $SystemApplications{hashmap} - The systems application you wish to check.
    .EXAMPLE
        $Applications = [ordered]@(
            'WinApp1' = @("Windows Application 1","Version 1.0")
            'WinApp2' = @("Windows Application 2","Version 5.6")
        )
        Check-Applications $Applications
#>

Function Check-Applications($SystemApplications) {
    $SystemApplications.Keys | % {
        if ($Global:Apps -match $SystemApplications[$_].GetValue(0)) {
            $msg =  $_ + " is currently installed."
            Load-ValidationObject "PASS" $msg "APP"
        } else {
            $msg = $_  + " is not currently installed."
            Load-ValidationObject "FAIL" $msg "APP"
        }
    }
}

<#
    Check-NBUPort

    .SYNOPSIS
        This function attempts to verify that the NetBackup master is set and
        can be reached over the appropriate network adapter and TCP port
    .DESCRIPTION
        The function is hardcoded for the NBU Agent connectivity only but may be modified to check
        for other connectiivty over a specified adapter or TCP (or UDP) port.
    .EXAMPLE
        Check-NBPort
#>

#Function Check-NBUPort($RemoteHost, $Port, $Proto){
Function Check-NBUPort(){
    $Adapters = Get-WmiObject Win32_NetworkAdapterConfiguration -Filter {IPEnabled = True}# -ErrorAction SilentlyContinue

    # If the Orange/back net adapter is present, use it. Otherwise, use the front net adapter for comms check.
    If ($Adapters.Count -eq 2){
        ForEach($Adapter in $Adapters){
            if (!$Adapter.DefaultIPGateway){
                $SourceAdapter = $Adapter
            }
        }
    }
    Else{
    # No Orange or back net adapter detected, using front net adapter for NBU master communications check/
        $SourceAdapter = $Adapters
    }
    # Set the local Source IP to the first IP bound to the selected adapter.
    $SourceIP = $SourceAdapter.IPAddress[0]
    $MyAdapter = (Get-NetAdapter -InterfaceIndex $SourceAdapter.InterfaceIndex).Name

    If($SourceIP){
        Try{
            # Attempt to retrieve the master server (first item in array if present) set by successful NetBackup agent installation.
            $Master = (Get-ItemProperty HKLM:\SOFTWARE\Veritas\NetBackup\CurrentVersion\Config -ErrorAction SilentlyContinue).Server[0]
        }
        Catch{
            $msg =  "FAILED to determine NetBackup Master server from the registry!"
            Load-ValidationObject "FAIL" $msg "COMM"
            Return
        }
        $MasterIP = ([System.Net.Dns]::GetHostAddresses($Master)).IPAddresstoString
        $SourceIP = [IPAddress]$SourceIP
        $MasterIP = [IPAddress]$MasterIP
        # NBU Agent comm port to over TCP
        $MasterIPPort = 1556

        # get an unused local port, used in local IP endpoint creation
        $UsedLocalPorts = ([System.Net.NetworkInformation.IPGlobalProperties]::GetIPGlobalProperties()).GetActiveTcpListeners() |
                                Where-Object -FilterScript {$PSitem.AddressFamily -eq 'Internetwork'} |
                                Select-Object -ExpandProperty Port
        Do {
            $localport = $(Get-Random -Minimum 49152 -Maximum 65535 )
            }
        Until ( $UsedLocalPorts -notcontains $localport)
        # Create the local IP endpoint using specified adapter for making the connection test.
        $LocalIPEndPoint = New-Object -TypeName System.Net.IPEndPoint -ArgumentList  $SourceIP,$localport

        # Create the TCP client and specify the local IP endpoint to be used.
        # By "default" the protocol uses TCP, but UDP could be specified too.
        $TCPClient = New-Object -Typename System.Net.Sockets.TcpClient -ArgumentList $LocaIPEndPoint

        Try{
            # Connect to the MasterIP on the required port.
            $TCPClient.Connect($MasterIP, $MasterIPPort)
            $msg = "NetBackup connects to: $Master over: $MyAdapter - $SourceIP."
            Load-ValidationObject "PASS" $msg "COMM"
            $Error.Clear()
            Return
        }
        Catch{
            $msg = "NetBackup cannot connect to: $Master-$MasterIPPort using $MyAdapter - $SourceIP! $Error[0]"
            Load-ValidationObject "FAIL" $msg "COMM"
            $Error.Clear()
            Return
        }
    }
    Else{
        $msg = "NetBackup failed to determine the adapter for communications!"
        Load-ValidationObject "FAIL" $msg "COMM"
        Return
    }
}

Function Check-SinglePort($TCPServerPorts) {
    $count = $TCPServerPorts.Count
    Foreach ($item in $TCPServerPorts){
        $SlItem = $item.split("-")
        $loop += 1
        If(Test-NetConnection -ComputerName $SlItem[1] -port $SlItem[2] -WarningAction SilentlyContinue -ErrorAction SilentlyContinue -InformationLevel Quiet){
            $msg = $SlItem[0] + "connection to server " + $SlItem[1] + " on port " + $SlItem[2] + " was successful."
            Load-ValidationObject "PASS" $msg "COMM"
            $Error.Clear()
            Return
        }
        If ($loop -ge $count){
            $msg = $SlItem[0] + "connection to " + $SlItem[1] + " on port " + $SlItem[2] + " FAILED!"
            Load-ValidationObject "FAIL" $msg "COMM"
            $Error.Clear()
        }
    }
}


Function Check-AllPorts($TCPServerPorts) {
    Foreach ($item in $TCPServerPorts){
        $SlItem = $item.split("-")
        If(Test-NetConnection -ComputerName $SlItem[1] -port $SlItem[2] -WarningAction SilentlyContinue -ErrorAction SilentlyContinue -InformationLevel Quiet){
            $msg = $SlItem[0] + "connection to " + $SlItem[1] + " on port " + $SlItem[2] + " was successful."
            Load-ValidationObject "PASS" $msg "COMM"
            $Error.Clear()
        }
        Else{
            $counter_fail += 1
            $msg = $SlItem[0] + "connection to " + $SlItem[1] + " on port " + $SlItem[2] + " FAILED!"
            Load-ValidationObject "FAIL" $msg "COMM"
            $Error.Clear()
        }
    }
}

 <#
    Check-SystemConfig

    .SYNOPSIS
        Checks the system to make sure the configurations confirm to Charter standards.
    .DESCRIPTION
        This will check a system to ensure that the configurations are correct. There are
        a variety of checks that this function will perform.
    .PARAMETERS
        None
    .EXAMPLE
        Check-SystemConfig
#>

Function Check-SystemConfig() {
    #Check to make sure that the time zone is set to Central
    $TimeZone = (Get-WmiObject -Query "Select Caption from win32_timezone").Caption
    Check-Value $TimeZone "like" "*Central*" "Time Zone should be set to Central Time" "HOST"

    #If disk size is not 80GB fail server
    $PrimaryDisk = Get-WmiObject Win32_LogicalDisk -Filter "DeviceID='C:'" | Foreach-Object {$_.Size}
    $PrimaryDiskGB = $PrimaryDisk / 1GB
    if ($PrimaryDiskGB -ge 79 -and $PrimaryDiskGB -lt 81) {
        Load-ValidationObject "PASS" "OS disk size is correct." "CONFIG"
    }
    else {
        Load-ValidationObject "FAIL" "OS disk size should be 80GB (Current Size: $PrimaryDiskGB)" "CONFIG"
    }
    #Check PageFile size, it must be 8GB
    $PageFile = Get-WmiObject Win32_PageFileusage | Select-Object Name,AllocatedBaseSize,PeakUsage
    $Disk = $PageFile.AllocatedBaseSize/1024
    if ($PageFile.AllocatedBaseSize -eq 8192){
        Load-ValidationObject "PASS" "PageFile should be 8GB and it's $Disk GB" "CONFIG"
    }
    else{
        Load-ValidationObject "FAIL" "PageFile should be 8GB and it's $Disk GB" "CONFIG"
    }
    #Check BGInfo
    $BgInfo = Test-Path "C:\Program Files\sysinternals\BgInfo.exe"
    Check-Value $BgInfo "eq" "True" "BgInfo should be installed on the system." "CONFIG"
    #Check to make sure that Server is using the DNS VIPs for Charter
    $Dns = ipconfig /all
    ##Dec 2019
    Check-Value "$Dns" "match" "142.136.252.85" "DNS VIP 142.136.252.85 in the NCE should be present in configuration" "CONFIG" 
    Check-Value "$Dns" "match" "142.136.253.85" "DNS VIP 142.136.253.85 in the NCW should be present in configuration" "CONFIG" 
    #Check Nic Speed for each adapter.
    $NetAdapters = Get-NetAdapter
    Foreach ( $item in $NetAdapters) {
        $Speed = $item.LinkSpeed.Substring(0,2)
        Check-Value $Speed "ge" "10" "Network Adapter LinkSpeed should be greater or equal to 10 Gbs for $($item.Name)" "CONFIG"
    }
    # Check that IPv6 transitional protocols have been defeated
    $NetIsatapAdapter = Get-NetIsatapConfiguration | Where-Object {$_.State -eq "Enabled" -or $_.State -eq "Default" }
    $Net6to4Configuration = Get-Net6to4Configuration | Where-Object {$_.State -eq "Enabled" -or $_.State -eq "Default" }
    $NetTereConfiguration = Get-NetTeredoConfiguration | Where-Object {$_.Type -eq "Enabled" -or $_.Type -eq "Default" }
    Check-Value $NetIsatapAdapter.State "eq" "Default" "ISATAP network adaptor should be enabled and State should be 'Default'" "CONFIG"
    Check-Value $Net6to4Configuration.State "eq" "Default" "6to4 network adaptor should be enabled and State should be 'Default'" "CONFIG"
    Check-Value $NetTereConfiguration.Type "eq" "Default" "Teredo network adaptor should be enabled and Type should be 'Default'" "CONFIG" 

    #Check Network Direct, Chimney, and ReceiveSideScalling
    $NetOffloadGlobalSettings = Get-NetOffloadGlobalSetting

    Check-Value $NetOffloadGlobalSettings.ReceiveSideScaling "eq" "Enabled" "Receive Side Scalling should be enabled in Network Offload Settings" "CONFIG"
    Check-Value $NetOffloadGlobalSettings.Chimney "eq" "Disabled" "Chimney should be DISabled in Network Offload Settings" "CONFIG"
    Check-Value $NetOffloadGlobalSettings.NetworkDirect "eq" "Enabled" "Network Direct should be enabled in Network Offload Settings" "CONFIG"

    #Check Nic Bonding if physical
    $Bonding = get-netlbfoteam
    if ($null -ne $Bonding -and $env:COMPUTERNAME.Substring(0,3) -ne "vm0" ) {
    Check-Value $Bonding.TeamingMode "eq" "Lacp" "Nic Teaming should be configured for LACP if found" "CONFIG"
    }

    #Check if Licensed
    $LicenseStatus = ((cscript c:\windows\system32\slmgr.vbs /dli | find "License Status").split(':')[1]).Trim()
    Check-Value $LicenseStatus "eq" "Licensed" "Windows should be Licensed and Activated." "CONFIG"

    #Check to make sure the Windows Firewall is turned OFF for all profiles
    $Firewall = netsh advfirewall show all state | Select-String "state"
    Check-Value $Firewall "notcontains" "ON" "Windows Firewall should be turned off for all profiles." "CONFIG"

    #Check to make sure that the server has a site in AD Site and Services
    $Site = nltest /dsgetsite | cmd /q /v:on /c "set/p .=&echo(!.!"
    Check-Value $Site "notlike" "*ERROR*" "Server should be in an Active Directory Site!"

    #Check to make sure that the server is in the correct OU
    $Org = gpresult /R | select-String "OU="
    Check-Value $Org "match" $OrgUnit "Computer Object should be in OU=Production,OU=DC_Operations,OU=Enterprise,DC=CORP,DC=CHARTERCOM,DC" "CONFIG"

    #This must be run and pass
    $GroupPolicyUpdate = gpupdate
    Check-Value $GroupPolicyUpdate "match" "Computer Policy update has completed successfully" "Group policy manual refresh should succeed." "CONFIG"

    #Test the secure channel
    $SChannel = Test-ComputerSecureChannel
    Check-Value $SChannel "match" "True" "Test-ComputerSecureChannel test should work." "CONFIG"

    #Check Version Control File
    $VerFile = Test-Path "C:\Program Files\build\IERBReleaseNotes.txt"
    Check-Value $VerFile "eq" "True" "Version Control File C:\Program Files\build\IERBReleaseNotes.txt is on this server" "CONFIG"
}

 <#
    Send-Email

    .SYNOPSIS
        Sends an email using an SMTP server
    .DESCRIPTION
        Sends an email to the requested address provided from the start of the script
    .PARAMETERS
        None
    .EXAMPLE
        Send-Email
#>

Function Send-Email() {
    $SMTPServer = "mailrelay.chartercom.com"
    $From = "Build-Validations@charter.com"
    $To = $Global:EmailAddress
    $Subject = $env:COMPUTERNAME + " Validation Report"
    $Body = "Validation Completed. Please see attachment for Report."
    $Attachment = $Global:LogPath + $Global:LogFile
    Write-Output $Attachment
    Send-MailMessage -To $To -From $From -Subject $Subject -Body $body -Attachments $Attachment -SmtpServer $SMTPServer
}

<#
    Check-Groups

    .SYNOPSIS
        Check a group on the host to ensure that it contains requested groups.
    .DESCRIPTION
        This will perform a check against the array provided and the group you wish
        to check. If all groups are found it will return an array with true and an empty string
        others it will return false and an array with the groups/users not found.
    .PARAMETERS
        $Group{array} - The group members you wish to check.
        $GroupName{string} - The name of the group you wish to check.
    .EXAMPLE
        $Groups = @(
            "WinGroup1",
            "WinGroup2"
        )
        $GroupName = "Administrators"
        Check-Groups $Groups $GroupsName
#>

Function Check-Groups($Group, $GroupName) {
    $Flag = @($true,"")
    $SystemGroups = net localgroup $GroupName.toString()
    Foreach ($g in $Group) {
        If ([string]::IsNullOrEmpty($SystemGroups -like "*$g*")){
            $Flag[0] = $false
            $Flag[1] =  $Flag[1] + $g + " "
        }
     }
    #return $Flag
    if ($Flag[0] -eq $true) {
        $msg = "All required Users/Groups found in " + $GroupName
        Load-ValidationObject "PASS" $msg "CONFIG"
    }
    else {
        $msg =  "Users/Groups Missing from " +  $GroupName + " (" + $Flag[1].ToString() +")"
        Load-ValidationObject "FAIL" $msg "CONFIG"
    }
}

###############################
### End of helper functions ###
###############################


#################
# Main Program  #
#################
Function Main() {
    # Let the user know we are in progress
    Write-Host "Validation underway, please wait or press CTRL+C to cancel..."
    
    # Get PS environement info and send to log file
    Export-Env

    # Stamp the version
    Create-BigSeperator "Charter Windows Validation. Script version 3.0.0.0"
    Create-TimeStamp

    #Get Infos about the host
    Create-BigSeperator "Host Information"
    $HostInfo | Format-Table Name,Value -AutoSize -HideTableHeaders | Out-File -FilePath "$Global:LogPath$Global:LogFile" -Append
    Check-LogicalDisks

    Create-BigSeperator "Adapter Information"
    $adapter | Format-Table Name,InterfaceDescription,ifIndex,Status,LinkSpeed,MacAddress -AutoSize -Wrap | Out-File -FilePath "$Global:LogPath$Global:LogFile" -Append
    $ipaddresses | Out-File -FilePath "$Global:LogPath$Global:LogFile" -Append

    #Hostname check
    Create-BigSeperator "Host Validation"
    Parse-Hostname
    $Global:ValidationResult | Where-Object {$_.Type -eq "HOST"} |Format-Table Result, Description -AutoSize | Out-File -FilePath "$Global:LogPath$Global:LogFile" -Append

    #Checks to ensure that the appropriate Registry Key were set up
    Write-Host "Checking registry and PCI settings..."
    Create-BigSeperator "Windows Registry"
    Lookup-RegKeys $NonPciRegKeys
    Lookup-RegKeys $PciRegKeys
    Check-PCIArray -Required $OSCiphers -Found $Ciphers
    Check-PCIArray -Required $OSCurves -Found $Curves
    Check-PCIArray -Required $OSFunctions -Found $Functions
    $Global:ValidationResult | Where-Object {$_.Type -eq "REG"} |Format-Table Result, Description -AutoSize -Wrap | Out-File -FilePath "$Global:LogPath$Global:LogFile" -Append

    #Check to ensure require features are installed on the server.
    Write-Host "Checking Windows features..."
    Create-BigSeperator "Windows Features"
    Check-WindowsFeature $WindowsFeatures
    Check-DisabledWindowsFeature
    $Global:ValidationResult | Where-Object {$_.Type -eq "FEA"} |Format-Table Result, Description -AutoSize | Out-File -FilePath "$Global:LogPath$Global:LogFile" -Append

    #Checks to ensure the correct application are install on the box
    Write-Host "Writing application information..."
    Create-BigSeperator "Application Information"
    Check-Applications $ChtrApplications
    $Global:ValidationResult | Where-Object {$_.Type -eq "APP"} |Format-Table Result, Description -AutoSize | Out-File -FilePath "$Global:LogPath$Global:LogFile" -Append

    #Checks Agent TCP connections
    Write-Host "Checking application communications, this will take several minutes..."
    Create-BigSeperator "Communication Checks (TCP)"
    Check-AllPorts($TCPServerPorts)
    Check-AllPorts($DTC1)
    If(($Global:ValidationResult | Where-Object {$_.Description -match "Desktop Central" -and $_.result -match "FAIL"} | Measure-Object).Count){
        Check-AllPorts($DTC2)
    }
    Check-SinglePort($Splunk)
    Check-SinglePort($SEP)
    Check-NBUPort    
    
    $Global:ValidationResult | Where-Object {$_.Type -eq "COMM"} |Format-Table Result, Description -AutoSize | Out-File -FilePath "$Global:LogPath$Global:LogFile" -Append
    #Checks to ensure the correcy services are running.
    Write-Host "Checking services and status..."
    Create-BigSeperator "Service Information"
    Check-Services $ChtrServices
    $Global:ValidationResult | Where-Object {$_.Type -eq "SRV"} |Format-Table Result, Description -AutoSize | Out-File -FilePath "$Global:LogPath$Global:LogFile" -Append

    #Checks to ensure the correcy services start mode is disabled. (Windows 2016 Only)
    if ($WinVer -like "*Windows Server 2016*" ) {
        Create-BigSeperator "Disabled Service Information"
        #Start-Sleep -m 500
        Check-ServiceStartMode $ChtrDisabledServices "Disabled"
        $Global:ValidationResult | Where-Object {$_.Type -eq "DSRV"} |Format-Table Result, Description -AutoSize | Out-File -FilePath "$Global:LogPath$Global:LogFile" -Append
    }

    #Checks to ensure the correct services start mode is disabled.
    Create-BigSeperator "Disabled Task Information"
    Write-Host "Checking tasks..."
    Check-ScheduledTaskState $ChtrDisabledTasks "Disabled"
    $Global:ValidationResult | Where-Object {$_.Type -eq "TASK"} |Format-Table Result, Description -AutoSize | Out-File -FilePath "$Global:LogPath$Global:LogFile" -Append

    #Host configuration that need to be checked.
    Write-Host "Checking host configuration..."
    Create-BigSeperator "Host Configurations"
    Check-PhysicalDisks
    Check-DNS "corp.chartercom.com" "Forward"
    Check-DNS $env:COMPUTERNAME "Forward"
    Check-DNS $HostInfo['IPv4 Address'] "Reverse"
    Check-SystemConfig
    Check-Groups $ChtrAdminGroup "Administrators"
    Check-Groups $ChtrPerfGroup "Performance Monitor Users"

    #Backnet and Database checks need to occur if the adapter is present
    If ($env:COMPUTERNAME.Substring(10,1) -like "d" -or $env:COMPUTERNAME.Substring(0,3) -ne "vm0") {
        Write-Host "If this is Coudersport Virtual Machine you may ignore backnet Failures." 
        $backnet = $env:COMPUTERNAME + "-BN"
        $backnetip = (Get-NetIPConfiguration | Where-Object { $_.IPv4DefaultGateway -eq $null -and  $_.NetAdapter.Status -ne "Disconnected" }).IPv4Address.IPAddress
        Check-DNS $backnet "Forward"
        Check-DNS $backnetip "Reverse"
        $route = route print
        If ($route -Match "10.222.56.0") {
            Load-ValidationObject "PASS" "Correct route for backnet found." "CONFIG"
        }
        ElseIf ($route -Match "10.222.59.0 ") {
            Load-ValidationObject "PASS" "Correct route for backnet found." "CONFIG"
        }
        Else {
            Load-ValidationObject "FAIL" "Route for backnet was not found." "CONFIG"
        }
    }

    #Check-Groups $PerfGroup "Performance Monitor Users"
    $Global:ValidationResult | Where-Object {$_.Type -eq "CONFIG"} | Format-Table Result, Description -AutoSize | Out-File -FilePath "$Global:LogPath$Global:LogFile" -Append

    #If there are any failures print them out at the bottom of the log.
    $Failures = $Global:ValidationResult | Where-Object {$_.Result -eq "FAIL"}
    If ($Failures) {
        Create-BigSeperator "FAILED ITEMS"
        $Global:ValidationResult | Where-Object {$_.Result -eq "FAIL"} |Format-Table Result, Description -AutoSize -Wrap | Out-File -FilePath "$Global:LogPath$Global:LogFile" -Append
    }
    Write-Host "Finalizing validation..."
    Create-BigSeperator "End of Validation"

    If (!([string]::IsNullOrEmpty($Global:EmailAddress))) {
        Send-Email
        Write-Host "Validation finished. Please check you email for the results."
    }
    Else {
        Write-Host "Validation finished. Please check $Global:LogPath$Global:LogFile for the results."
    }
    Create-TimeStamp
}

Main