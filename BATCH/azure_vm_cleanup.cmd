REM *********************
REM Stop appvolume service
REM *********************
sc stop svservice
REM *********************
REM Stop and disable Windows update service
REM *********************
sc stop wuauserv
sc config wuauserv start= disabled
REM *********************
REM Delete any existing shadow copies
REM *********************
vssadmin delete shadows /All /Quiet
REM *********************
REM delete files in c:\Windows\SoftwareDistribution\Download\
REM *********************
del c:\Windows\SoftwareDistribution\Download\*.* /f /s /q
REM *********************
REM delete hidden install files
REM *********************
del %windir%\$NT* /f /s /q /a:h
REM *********************
REM delete prefetch files
REM *********************
del c:\Windows\Prefetch\*.* /f /s /q
REM *********************
REM Run Disk Cleanup to remove temp files, empty recycle bin
REM and remove other unneeded files
REM Note: Makes sure to run c:\windows\system32\cleanmgr /sageset:1 command on your initially created parent image and check all the boxes of items you want to delete 
REM *********************
c:\windows\system32\cleanmgr /sagerun:1
REM ********************
REM Execute queued compilation jobs for .NET Framework
REM ********************
cd c:\Windows\Microsoft.NET\Framework\v4.0.30319
ngen executequeueditems
REM ********************
REM Cleanup Image with DISM
REM ********************
dism.exe /online /cleanup-image /startcomponentcleanup /resetbase
REM ********************
REM CompactOS
REM ********************
compact /compactos:always
REM ********************
REM Defragment the VM disk
REM ********************
sc config defragsvc start= auto
net start defragsvc
defrag c: /U /V
net stop defragsvc
sc config defragsvc start= disabled
REM *********************
REM Clear all event logs
REM *********************
wevtutil el 1>cleaneventlog.txt
for /f %%x in (cleaneventlog.txt) do wevtutil cl %%x
del cleaneventlog.txt
REM *********************
REM release IP address
REM *********************
ipconfig /release
REM *********************
REM Flush DNS
REM *********************
ipconfig /flushdns
REM *********************
REM Shutdown VM
REM *********************
shutdown /s /t 0