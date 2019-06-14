Import-Module ActiveDirectory
Get-ADObject -LDAPFilter "(&(&(&(uncName=*)(objectCategory=printQueue))))" -properties *|Sort-Object -Unique -Property servername |select servername

