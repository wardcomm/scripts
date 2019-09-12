<# This form was created using POSHGUI.com  a free online gui designer for PowerShell
.NAME
    Untitled
#>

Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.Application]::EnableVisualStyles()

$Form                            = New-Object system.Windows.Forms.Form
$Form.ClientSize                 = '400,400'
$Form.text                       = "Form"
$Form.TopMost                    = $false





#Write your logic code here

 
#Error Handling Functions
function Write-Error {
       Param ([string]$ErrorMsg, [System.IO.FileInfo]$logfile, [string]$Server)
       Write-Host "$ErrorMsg"
       Write-Output "$ErrorMsg"| Out-File $logfile -Append
       Rename-Item $logfile -NewName "$($Server)_FAILED.log"
}

function throw-error {
       Param ([string]$ErrorMsg, [System.IO.FileInfo]$logfile, [string]$serv)
       write-error -ErrorMsg $ErrorMsg -logfile $logfile -serv $serv
       Throw $ErrorMsg
}

Add-Type -Assembly System.Windows.Forms     ## Load the Windows Forms assembly
$Form = New-Object Windows.Forms.Form
$Form.FormBorderStyle = "FixedToolWindow"
$Form.Text = "Ansible Tower Manual Inventory - Production"
$Form.StartPosition = "CenterScreen"
$Form.Width = 350
$Form.Height = 260

$lblHost = New-Object System.Windows.Forms.Label  
$lblHost.Text = "Host Name:" 
$lblHost.Top = 23
$lblHost.Left = 5
$lblHost.Width = 120
$lblHost.AutoSize = $true
$Form.Controls.Add($lblHost)

$TxtBoxHost = New-Object Windows.Forms.TextBox 
$TxtBoxHost.TabIndex = 0 # set Tab Order
$TxtBoxHost.Top = 20
$TxtBoxHost.Left = 80
$TxtBoxHost.Width = 250 
$TxtBoxHost.Text = ".corp.chartercom.com"

$DCLabel = New-Object System.Windows.Forms.Label
$DCLabel.Text = "Data Center:"
$DCLabel.Top = 63
$DCLabel.Left = 5
$DCLabel.Autosize = $true 
$Form.Controls.Add($DCLabel)    # Add to Form

$DCCombo = New-Object Windows.Forms.ComboBox
$DCCombo.TabIndex = 1 # set Tab Order
$DCCombo.Top = 60
$DCCombo.Left = 100
$DCCombo.Width = 150
$ArrayImage = "NCE", "NCW", "CDP"
$DCCombo.DropDownStyle = [System.Windows.Forms.ComboBoxStyle]::DropDownList
$DCCombo.Items.AddRange($ArrayImage)
$DCCombo.SelectedIndex = 1
[void] $DCCombo.EndUpdate() 

$lblRITM = New-Object System.Windows.Forms.Label  
$lblRITM.Text = "RITM Ticket:" 
$lblRITM.Top = 103
$lblRITM.Left = 5
$lblRITM.Width = 120
$lblRITM.AutoSize = $true

$TxtBoxRITM = New-Object Windows.Forms.TextBox 
$TxtBoxRITM.TabIndex = 3 # set Tab Order
$TxtBoxRITM.Top = 100
$TxtBoxRITM.Left = 80
$TxtBoxRITM.Width = 250 
$TxtBoxRITM.Text = "RITM"

$chk_exch = New-Object Windows.Forms.CheckBox
$chk_exch.TabIndex = 4 # set Tab Order
$chk_exch.Top = 140
$chk_exch.Left = 10
$chk_exch.Width = 250 
$chk_exch.Text = "Exchange Server?"

$OK = New-Object Windows.Forms.Button
$OK.TabIndex = 5 # set Tab Order
$OK.Top = 190 
$OK.Left = 10
$OK.Text = "Submit Job"
$OK.DialogResult = "OK"

$Cancel = New-Object Windows.Forms.Button
$OK.TabIndex = 6 # set Tab Order
$Cancel.Top = 190  
$Cancel.Left = 250
$Cancel.Text = "Cancel"
$Cancel.DialogResult = "Cancel"

$Form.AcceptButton = $OK          
$Form.CancelButton = $Cancel      
$Form.Controls.Add($OK)
$Form.Controls.Add($Cancel)
$Form.Controls.Add($TxtBoxHost)
$Form.Controls.Add($DCCombo)
$Form.Controls.Add($lblRITM)
$Form.Controls.Add($TxtBoxRITM)
$Form.Controls.Add($chk_exch)

$Form.Add_Shown( { $Form.Activate(); $TxtBoxHost.Focus() } )
$TxtBoxHost.SelectionStart = 0
$result = $Form.ShowDialog()

If($result -eq "OK")
    {   # Copy variables and use them as you desire...
       $Server = $TxtBoxHost.Text.ToLower()
       $DataCenter = $DCCombo.SelectedItem
    $SNOWTicket = $TxtBoxRITM.Text
    Write-Host "Submitting the following data to tower..."
    Write-Host "`t - Hostname: $Server"
    Write-Host "`t - DataCenter: $DataCenter"
    Write-Host "`t - SNOW ticket: $SNOWTicket"
    $logfile = "$env:USERPROFILE\Desktop\$Server.txt"
}
else {
    Write-Host "Cancelled execution by user... Exiting."
    Exit
    }

$Error.Clear()
cls

#$AnsibleServer="ansible.corp.chartercom.com"
$AnsibleServer = "ncednanstra0001.corp.twcable.com"
#$AnsibleWindowsBuildTemplate= "OA/chtr-windows-standards-2019Q3 - provisioning"
$AnsibleWindowsBuildTemplate = "Users/TonyW/chtr-windows-standards-development-git"

# Create Authentication Credentials for Ansible API
$EncodedLogin="YXBpLXZtZGVwbG95OmFwaS12bWRlcGxveQ=="
$AuthHeader = "Basic " + $EncodedLogin
$Headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
$Headers.Add("Authorization",$AuthHeader)
$Headers.Add("Accept","application/json")
$Headers.Add("Content-Type","application/json")

# Force TLS 1.2
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

# Find the inventory for provisioning
$Uri = "https://$AnsibleServer/api/v2/inventories/?name=OA/Provisioning"

Try {
       $Response = Invoke-RestMethod -Uri $Uri -Headers $Headers -Method Get} 
Catch { 
       throw-error -ErrorMsg "Unable to query Ansible inventories" -logfile $logfile -Server $Server }
$Response.results | ForEach-Object -Process { if ($_.name -match "OA/Provisioning") {$ProvInventory = $_.id}}

# Create Ansible's variables
$Description = $SNOWTicket
$Environment = $Server.Substring(3,1).ToUpper()
$BuildDate = Get-Date -format "yyyyMMdd"


# Check if the host exists (Failure requiring rebuild)
$Uri = "https://$AnsibleServer/api/v2/inventories/$ProvInventory/hosts/?name=$Server"
Try {
    $Response = Invoke-RestMethod -Uri $uri -Headers $Headers -Method GET} 
Catch { 
    throw-error -ErrorMsg "Unable to check for preexisting host" -logfile $logfile -Server $Server }

    #Set the JSON for the if/else clause one time
    $Json = @{
           name="$Server"
           description="$Description"
           enabled="true"
           instance_id=""
           variables="{chtr_LegacyDomain: 'chtr', Vrm_DataCenter_Location: $DataCenter, chtr_Environment: $Environment, creation_date: $BuildDate, chtr_ProdReady: 'false'}"
    } | ConvertTo-Json

if ($Response.count -gt 0) {
       $HostID = $Response.results.id
       $Uri = "https://$AnsibleServer/api/v2/hosts/$HostID/"
       Try {
        $Response = Invoke-RestMethod -Uri $uri -Headers $Headers -Method PATCH -Body $Json} 
    Catch {
        throw-error -ErrorMsg "Unable to update existing host with Ansible" -logfile $logfile -Server $Server }
} 
else {
       # Register the host if it doesn't exist
       $Uri = "https://$AnsibleServer/api/v2/inventories/$ProvInventory/hosts/"
       Try {
        $Response = Invoke-RestMethod -Uri $uri -Headers $Headers -Method POST -Body $Json} 
    Catch {
        throw-error -ErrorMsg "Unable to register host with Ansible" -logfile $logfile -Server $Server }
       $HostID = $Response.id
}

# Find the configuration template
$Uri = "https://$AnsibleServer/api/v2/job_templates/?name=$AnsibleWindowsBuildTemplate"

Try {
    $Response = Invoke-RestMethod -Uri $Uri -Headers $Headers -Method Get} 
Catch {
    throw-error -ErrorMsg "Unable to locate configuration template" -logfile $logfile -Server $Server }

$Response.results | ForEach-Object -Process { if ($_.name -match $AnsibleWindowsBuildTemplate) {$ProvTemplate = $_.id}}

If($chk_exch.Checked)
{    # Launch the provisioning template
    $Json = @{
           inventory=$ProvInventory
           limit=$Server
           skip_tags="qualys"
    } | ConvertTo-Json
}
else
{    # Launch the provisioning template
    $Json = @{
           inventory=$ProvInventory
           limit=$Server
     } | ConvertTo-Json
}
$Uri = "https://$AnsibleServer/api/v2/job_templates/$ProvTemplate/launch/"

Try {
    $Response = Invoke-RestMethod -Uri $uri -Headers $Headers -Method POST -Body $Json} 
Catch {
    throw-error -ErrorMsg "Unable to launch provisioning template" -logfile $logfile -Server $Server }

$JobID = $Response.id

# Monitor provisioning
$loops=1
Write-Host -NoNewline "Invoking Ansible provisioning template (Timeout is 60 minutes) - "
While ($True) {
       $Uri = "https://$AnsibleServer/api/v2/jobs/$JobID/"
       Try {
        $Response = Invoke-RestMethod -Uri $Uri -Headers $Headers -Method Get} 
    Catch { 
        throw-error -ErrorMsg "Unable to query provisioning job status" -logfile $logfile -Server $Server }
       $loops = $loops + 1
       if ($loops -gt 120) {
              throw-error -ErrorMsg " Ansible provisioning timed out" -logfile $logfile -Server $Server
       }
       if ($Response.status -match "failed") {
              throw-error -ErrorMsg " Ansible provisioning failed" -logfile $logfile -Server $Server
       }
       if ($Response.status -match "successful") {
              Write-Host " Complete"
              Break
       }
       Write-Host -NoNewline "."
       Start-Sleep -Seconds 30
}

# Delete the host from ansible
$Uri = "https://$AnsibleServer/api/v2/hosts/$HostID/"
Try {
           $Response = Invoke-RestMethod -Uri $uri -Headers $Headers -Method DELETE
       } 
Catch {
           write-error -ErrorMsg "Unable to delete server from Ansible inventory - This is a non fatal error.  Continuing..." -logfile $logfile -Server $Server
       }

Write-Host "Complete!"
[void]$Form.ShowDialog()