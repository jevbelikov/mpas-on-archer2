shopt -s extglob

#setting variables to loop through
run_time='01:00:00'
no_nodes='1'
no_runs=1
count=0
mesh=`echo *graph* | awk -F'.' '{print $1"."$2}'`

#select whether to check namelist before submitting job:
echo "check each job before running? (y/n)"
read verb

#looping through changes made:
while [ $count -lt $no_runs ]
do
	for t in $run_time
	do
		for n in $no_nodes
		do
			echo "running $n"
		#copying model into new directory: Directory is named MPAS_modeltime.nodes_month_day_hour_minutes to ensure uniquness
			now=`date +'%m-%d-%H-%M'`
			mkdir ../'MPAS_'$now'_'$t'_'$n'_'$mesh'_'$count
			cp * ../'MPAS_'$now'_'$t'_'$n'_'$mesh'_'$count
			cd ../'MPAS_'$now'_'$t'_'$n'_'$mesh'_'$count #moving into working directory

		#setting variables as needed in namelist and job form:
			sed -i 's/MODEL_RUNTIME/'$t'/' namelist.atmosphere
			sed -i 's/RUN_NODE_COUNT/'$n'/' job.slurm

		#print changed lines and verify correctness: (if selected earlier)
			if [[ "$verb" == "y" ]]
			then
				awk '$1 == "config_run_duration" {print}' namelist.atmosphere
				awk '$1 == "#SBATCH" {print}' job.slurm

				echo "Namelist changes correct? (y/n)"
				read check
	
		#run job.slurm with current parameters: (currently echoed to not run but show what would happen)
		
				if [[ "$check" == "y" ]]
				then
					echo "sbatch job.slurm"
				else
					echo "skipped"
				fi
			else
				echo "sbatch job.slurm"
			fi
			cd ../Jonas/ #change to path to MPAS on ARCHER2
		done
	done
	let count=count+1 #update run counter
	
done
