import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_csv('C:/Users/jonas/source/repos/SoHPC2021/MPAS_scalability_SoHPC2021/code snippets/Jonas/run_times.csv')
model_time = pd.unique(df['Run_time'])
node_count = pd.unique(df['Node_count'])
mesh_list = pd.unique(df['Mesh'])

#setting up multi_index to store final results for plotting
df_final = pd.DataFrame(columns=['Run_time', 'Node_count', 'Average_time', 'Speedup', 'Efficiency', 'Mesh', 'Time_per_hour'])
df_final = df_final.set_index(['Run_time', 'Mesh'])

#looping through each mesh type, model run time and node count used:
for m in mesh_list:
    for t in model_time:
        av_time = []
        av_std = []
        speedup = []
        efficiency = []
        time_per_hour = []
        for n in range(0,len(node_count)): #looping through number of nodes to calculate run time, speedup
            av_time.append(df.loc[(df['Run_time'] ==t) & (df['Node_count'] == node_count[n])]['Elapsed_time'].mean())
            av_std.append(df.loc[(df['Run_time'] ==t) & (df['Node_count'] == node_count[n])]['Elapsed_time'].std())
            speedup.append(av_time[0]/av_time[n]) #calculating relative speedup by Ln/L0
            efficiency.append(speedup[n]/node_count[n]) #calculating relative efficiency
            time_per_hour.append(av_time[n]/(int(model_time[n].split(':')[0])*(60**2))) #calculating elapsed time per modelled hour
        result_dict = {'Run_time': t, 'Node_count': node_count, 'Average_time': av_time, 'Speedup': speedup, 'Efficiency': efficiency, 'Mesh': m, 'Time_per_hour': time_per_hour}
        df_final = df_final.append(pd.DataFrame.from_dict(result_dict).set_index(['Run_time', 'Mesh']))
df_final.to_csv('MPAS_runtimes.csv')
 
print(df_final)

#plotting:
for m in mesh_list:
    for i in model_time:
        
        #setting up subplots
        fig,axs=plt.subplots(2,2)
        plt.subplots_adjust(left=0.125, right=0.9, bottom=0.1, top=0.9,wspace=0.6,hspace=0.5)
        fig.suptitle('Modelled time: ' + i)
        
        #setting up data
        av_time = df_final.loc[i].loc[m]['Average_time'].to_numpy()
        speedup = df_final.loc[i].loc[m]['Speedup'].to_numpy()
        efficiency = df_final.loc[i].loc[m]['Efficiency'].to_numpy()
        time_per_hour = df_final.loc[i].loc[m]['Time_per_hour'].to_numpy()

        #plotting data
        axs[0][0].plot(node_count,av_time,'--',color='blue')
        axs[0][0].plot(node_count,av_time,'^', color='orange')
        axs[0][0].set_title('Run time')
        axs[0][0].set_xticks(np.arange(0,max(node_count)+1))
        axs[0][0].set_aspect('auto')

        axs[0][1].plot(node_count,speedup, '--',color='blue')
        axs[0][1].plot(node_count,speedup,'^', color='orange')
        axs[0][1].set_title('Relative Speedup')
        axs[0][1].set_xticks(np.arange(0,max(node_count)+1))
        axs[0][1].set_aspect('auto')

        axs[1][1].plot(node_count, time_per_hour, '--', color='blue')
        axs[1][1].plot(node_count,time_per_hour,'^', color='orange')
        axs[1][1].set_title('Elapsed time per simulated hour')
        axs[1][1].set_xticks(np.arange(0,max(node_count)+1))
        axs[1][1].set_yscale('log')
        axs[1][1].set_aspect('auto')

        axs[1][0].plot(node_count, efficiency, '--', color='blue')
        axs[1][0].plot(node_count,efficiency,'^', color='orange')
        axs[1][0].set_title('Efficiency')
        axs[1][0].set_xticks(np.arange(0,max(node_count)+1))
        axs[1][0].set_yticks(np.arange(0,1,0.2))
        axs[1][0].set_aspect('auto')

        
        #saving figure:
        #plt.savefig('%s_%s_graphs.svg' % (m, i)) #uncomment to save plots

plt.show()