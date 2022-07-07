 New-SFTPSession -ComputerName mway.cnb.com -Credential (Get-Credential oldrepub ) -Verbose | fl
===========================================================
$UserName = "Intesasanpaolo"

#Define the Private Key file path
$KeyFile = "D:\Test1\TestKey"
$nopasswd = new-object System.Security.SecureString

#Set Credetials to connect to server
$Credential = New-Object System.Management.Automation.PSCredential ($UserName, $nopasswd)
$SFTPSession = New-SFTPSession -ComputerName $ComputerName -Credential $Credential -KeyFile $KeyFile