   if [ $USER = "oracle" ]; then
            if [ $SHELL = "/bin/ksh" ]; then
                ulimit -u 16384
                ulimit -n 65536
            else
                ulimit -u 16384 -n 65536
            fi
umask 022
         fi
ulimit -u 16384
ulimit -n 65536
