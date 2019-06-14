#!/bin/bash
wget  https://github.com/wata727/tflint/releases/download/v0.8.2/tflint_linux_amd64.zip -P /tmp
mkdir -p /usr/local/tflint/bin
unzip /tmp/tflint_linux_amd64.zip -d /usr/local/tflint/bin
export PATH=/usr/local/tflint/bin:$PATH
# install tflint /usr/local/tflint/bin
tflint -v
# brew tap wata727/tflint
# brew install tflint
rm -rf /tmp/tflint*

# #!/bin/bash -e

# processor=$(uname -m)

# if [ "$processor" == "x86_64" ]; then
#   arch="amd64"
# else
#   arch="386"
# fi

# case "$(uname -s)" in
#   Darwin*)
#     os="darwin_${arch}"
#     ;;
#   MINGW64*)
#     os="windows_${arch}"
#     ;;
#   MSYS_NT*)
#     os="windows_${arch}"
#     ;;
#   *)
#     os="linux_${arch}"
#     ;;
# esac

# echo "os=$os"

# echo -e "\n\n===================================================="

# get_latest_release() {
#   curl --silent "https://api.github.com/repos/wata727/tflint/releases/latest" | # Get latest release from GitHub api
#     grep '"tag_name":' |                                            # Get tag line
#     sed -E 's/.*"([^"]+)".*/\1/'                                    # Pluck JSON value
# }

# echo "Looking up the latest version ..."
# latest_version=$(get_latest_release)
# echo "Downloading latest version of tflint which is $latest_version"
# curl -L -o /tmp/tflint.zip "https://github.com/wata727/tflint/releases/download/${latest_version}/tflint_${os}.zip"
# retVal=$?
# if [ $retVal -ne 0 ]; then
#   echo "Failed to download tflint_${os}.zip"
#   exit $retVal
# else
#   echo "Download was successfully"
# fi

# echo -e "\n\n===================================================="
# echo "Unpacking /tmp/tflint.zip ..."
# unzip -u /tmp/tflint.zip -d /tmp/
# echo "Installing /tmp/tflint to /usr/local/bin..."
# sudo mkdir -p /usr/local/bin
# sudo install -b -C -v /tmp/tflint /usr/local/bin/
# retVal=$?
# if [ $retVal -ne 0 ]; then
#   echo "Failed to install tflint"
#   exit $retVal
# else
#   echo "tflint installed at /usr/local/bin/ successfully"
# fi

# echo -e "\n\n===================================================="
# echo "Current tflint version"
# tflint -v

