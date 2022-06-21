#remote
ls -t
pwd
!echo listing-start
export today_date=(`date +%m%d%y`)
export today_file=($today_date"_Lookup7500.csv")
!echo listing-end

put $today_file

#local
lpwd
lls -t
bye
