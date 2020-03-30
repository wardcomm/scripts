##################################################################################
# This script should be sourced from the Jenkins shell execution environment.
# It will set up the needed variables, use them to build the necessary
# configuration files *including* the ansible hosts file, and then execute the
# ansible playbook to do the install.
# It is included here so that it gets versioned and backed up in git.
##################################################################################
echo "Happy Friday !!"

set +x  # turn off debug output (mostly)
set -ue # errors are fatal; unset vars are errors

echo "STARTING $(date)"

echo "$Custom" > Custom.yml # save the vars file
src=/tmp/var.src            # single point of definition for tempfile name
sed 's/[	 ]*:[	 ]*/=/' < Custom.yml > $src # parse the vars file to something source-able
chmod 0600 $src # keep it secure
set -x  # debugging output while developing, comment this when done
. $src  # load the ansible vars to the environment for this script
rm $src # remove the tempfile (don't leave
set +x  # torn off the extra debug output again

echo "
Executing as $USER
Installing as $install_user

Putting ADMIN  on $NODE_1

Putting NODE_1 on $NODE_1
Putting NODE_2 on $NODE_2
Putting NODE_3 on $NODE_3

Using DB on $DB_HOST

"

>| hosts # empty exists
chmod 0600 hosts # keep secure

echo "
# this is the primary/admin machine
[admin]
$NODE_1

# these are application/managed nodes
[managed]
$NODE_2
$NODE_3

# a collective name for all
[fmw:children]
admin
managed

[db]
$DB_HOST

[fmw:vars]
ansible_ssh_user=$USER
ansible_ssh_pass=$PSWD
install_user=$install_user
install_group=$install_group
install_pswd=$install_pswd
ADMIN=$NODE_1
NODE_1=$NODE_1
NODE_2=$NODE_2
NODE_3=$NODE_3
DB_HOST=$DB_HOST

" >| hosts # truncates whatever was there before

ansible-playbook -i hosts -vv main.yml

echo "DONE $(date)"
