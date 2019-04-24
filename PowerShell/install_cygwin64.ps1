$url = "http://www.cygwin.com/setup-x86_64.exe"
$output = "C:\Users\ncah61\Downloads\setup-x86_64.exe"

Invoke-WebRequest -Uri $url -OutFile $output
cmd.exe /c "c:\setup-x86_64.exe --no-admin -q -P binutils,openssl,openssl-devel,gcc-core,make,python,python-setuptools,libtool,libuuid-devel,libffi-dev,libcrypt-devel,gmp,gmp-devel,libgmp-devel,libmysqlclient-devel,python-devel,python-cffi,python-crypto,openssh,curl,wget,nano"
Set-ExecutionPolicy AllSigned; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
