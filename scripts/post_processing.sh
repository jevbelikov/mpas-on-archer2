#script to run after batch of model runs is completed:
shopt -s extglob

for directory in MPAS_* #change pattern if needed
do
	cd $directory
	if test -e atmosphere_model  #checking whether it has been cleaned up yet to avoid adding double outputs
	then
		elapsed_time=$( awk '/1 total time/{print $4}' log.atmosphere.0000.out )
		n=`echo $directory | awk -F'[_]' '{print $4}'`
		t=`echo $directory | awk -F'[_]' '{print $3}'`
		mesh=`echo $directory | awk -F'[_]' '{print $5}'`
		echo "$n,$t,$elapsed_time,$mesh" >> ../run_times.csv
		#removing all otherwise unnecessary files from working directory and returning to initial model directory:
		echo rm -v !(history*|log*|"namelist.atmosphere"|"job.slurm")
		cd ..
	else
		cd ..
	fi
done

