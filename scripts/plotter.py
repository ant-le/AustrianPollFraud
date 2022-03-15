
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import arviz as az
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import timedelta


class Plotter:
    
    def __init__(self):
        pass


    def rawDifferences(self, df, kind='mean'):
        df = df.copy()
        with plt.style.context('ggplot'):
            fig,ax = plt.subplots(3,1, figsize=(10,8), sharex=True, sharey=True)
            for idx, y in enumerate(['ÖVP', 'Grüne', 'SPÖ']):
                if kind == 'mean':
                    fig.suptitle('Differences of Means between bins')
                    tg = df.groupby('bins')[y].mean().reset_index()
                    cg = df[df.Treatment==0]
                    cg = cg.groupby('bins')[y].mean().reset_index()
                elif kind == 'std':
                    fig.suptitle('Differences of Standard Deviations between bins')
                    tg = df.groupby('bins')[y].std().reset_index()
                    cg = df[df.Treatment==0]
                    cg = cg.groupby('bins')[y].std().reset_index()
                else:
                    fig.suptitle('Differences of Variances between bins')
                    tg = df.groupby('bins')[y].var().reset_index()
                    cg = df[df.Treatment==0]
                    cg = cg.groupby('bins')[y].var().reset_index()
                diff = tg[y] - cg[y]
                ax[idx].scatter(df.bins.unique(), diff, s=25, c='olive', alpha=.6)
                ax[idx].set_title(f'{y}')
            fig.contrained_layout=True


    def scatter(self, df, save=False, var='ÖVP', binning=True):
        df = df.copy()        
        with plt.style.context('ggplot'):
            fig, ax = plt.subplots(figsize=(14,5))
            ax.scatter("Date", var, data=df[df["Treatment"]==1], 
                       label="Research Affairs", 
                       s=25,
                       c='olive',
                       alpha=.6
            )
            ax.scatter("Date", var, data=df[df["Treatment"]==0], 
                       label="Other Institutes",
                       s=25,
                       c='silver',
                       alpha=.6
            )
            if binning:
                # Create Lines seperating bins
                upper = df.groupby('bins')['Date'].max()[:-1].reset_index(drop=True)
                lower = df.groupby('bins')['Date'].min()[1:].reset_index(drop=True)
                bins = lower + (upper - lower)/2              
                ax.vlines(bins, ymin=df[var].min()-1, ymax=df[var].max()+1, color='black',lw=.5)
                
                # Plotting mean value of each bin with fixed distances
                pos = []
                pos.append(df.Date.min()-timedelta(5))
                pos[1:len(bins)] = bins
                pos.append(df.Date.max()+timedelta(5))
                for b in df.bins.unique():
                    ax.hlines(df.loc[(df.bins==b) & (df.Treatment==1), var].mean(),
                              xmin=pos[b-1]+timedelta(7),
                              xmax=pos[b]-timedelta(7),
                              color="olive",
                    )
                    ax.hlines(df.loc[(df.bins==b) & (df.Treatment==0), var].mean(),
                              xmin=pos[b-1]+timedelta(5),
                              xmax=pos[b]-timedelta(5),
                              color='silver',
                    )
            ax.set_xlim([df.Date.min()-timedelta(20), df.Date.max()+timedelta(20)])
            ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7)))
            ax.xaxis.set_minor_locator(mdates.MonthLocator())
            ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
            ax.set_ylim(df[var].min()-2, df[var].max()+2)    
            ax.set_ylabel("Estimated Voting % for " + str(var))
            ax.legend(fancybox=True)
            plt.show()
            if save is True:
                path = Path(__file__).parent.parent / "images" / "descriptive.csv"
                fig.savefig(path, dpi=300)
    
    
    def trends(self, df, var='ÖVP', diff=.1):            
        df = df.copy() 
        with plt.style.context('ggplot'):  
            if 'all' in var:
                fig, ax = plt.subplots(2,2,figsize=(15,8), sharex=True, sharey=True, constrained_layout=True)
                var = [['ÖVP', 'SPÖ'],['FPÖ', 'Grüne']]
                for row in range(2):
                    ax[row,0].errorbar(df.bins.unique()+diff,
                                df[df.Treatment==1].groupby('bins')[var[0][row]].mean().values, 
                                df[df.Treatment==1].groupby('bins')[var[0][row]].std().values,
                                elinewidth=.7,
                                color='olive',
                                #alpha=.6,
                                fmt='o',
                                capsize=6,
                                label='Research Affairs'
                    )
                    ax[row,0].errorbar(df.bins.unique()-diff,
                                df[df.Treatment==0].groupby('bins')[var[0][row]].mean().values, 
                                df[df.Treatment==0].groupby('bins')[var[0][row]].std().values,
                                elinewidth=.7,
                                color='silver',
                                fmt='o',
                                capsize=6,
                                label='Other Institutes'
                    )
                    ax[row,1].errorbar(df.bins.unique()+diff,
                                df[df.Treatment==1].groupby('bins')[var[1][row]].mean().values, 
                                df[df.Treatment==1].groupby('bins')[var[1][row]].std().values,
                                elinewidth=.7,
                                color='olive',
                                #alpha=.6,
                                fmt='o',
                                capsize=6,
                                label='Research Affairs'
                    )
                    ax[row,1].errorbar(df.bins.unique()-diff,
                                df[df.Treatment==0].groupby('bins')[var[1][row]].mean().values   , 
                                df[df.Treatment==0].groupby('bins')[var[1][row]].std().values,
                                elinewidth=.7,
                                color='silver',
                                fmt='o',
                                capsize=6,
                                label='Other Institutes'
                    )         
                    ax[0,1].set_title(f"{var[1][row]}",fontsize='small')
                    ax[row,0].set_title(f'{var[0][row]}',fontsize='small')                    
                ax[1,1].set_title(f"FPÖ (values for 2020 are not comparable)",fontsize='small')
                ax[0,0].legend(fancybox=True)
                # ticks = ['-3', '-2', '-1', '0', '1', '2', '3', '4', '5']
                # plt.xticks(np.r_[1:10], ticks)
                fig.suptitle('Binned Differences for major parties in Austria')
                fig.supxlabel('Time')
                fig.supylabel('Estimated Voting %')
            else:          
                _, ax = plt.subplots(figsize=(10,4))
                tg = df[df.Treatment==1].groupby('bins')[var].mean().values   
                cg = df[df.Treatment==0].groupby('bins')[var].mean().values   
                ax.errorbar(df.bins.unique()+diff,
                            tg, 
                            df[df.Treatment==1].groupby('bins')[var].std().values,
                            elinewidth=.7,
                            color='olive',
                            #alpha=.6,
                            fmt='o',
                            capsize=6,
                            label='Research Affairs'
                )
                ax.errorbar(df.bins.unique()-diff,
                            cg, 
                            df[df.Treatment==0].groupby('bins')[var].std().values,
                            elinewidth=.7,
                            color='silver',
                            fmt='o',
                            capsize=6,
                            label='Other Institutes'
                )
                ax.legend(fancybox=True)
                # ticks = ['-3', '-2', '-1', '0', '1', '2', '3', '4', '5']
                # plt.xticks(np.r_[1:10], ticks)
                ax.set_ylabel(f"Estimated Voting % for {var}")
                ax.set_title("Pre-trends based on binning")
            plt.show()


    def posterior(self, model, interval=.89):
        df = az.summary(model.post.posterior[["beta"]],
                            hdi_prob=interval
                        ).iloc[:,:4]        
        bounds = df.iloc[:,2:].to_numpy()
        bounds[:,0] -= df.iloc[:,0].to_numpy()
        bounds[:,1] -= df.iloc[:,0].to_numpy()
        with plt.style.context('seaborn-white'):
            _,ax = plt.subplots(figsize=(10,4))
            ax.set_xlim([-.5, len(df.index)-.5])
            ax.errorbar(x=df.index,
                         y=df.iloc[:,0].values,
                         yerr=abs(bounds.T),
                         elinewidth=.5,
                         fmt='ok',
                         capsize=4,
                         markerfacecolor="white",
            )
            ax.hlines(0, 
                      xmin=-.5,
                      xmax=len(df.index)-.5,
                      colors='black', 
                      linestyles='--',
                      linewidth=.8)
                        
            label = []
            for i in range(len(model.post.posterior.beta_dim_0)):
                label.append(f'Group {i}')
            ax.set_xticks(df.index)
            ax.set_xticklabels(label)
            ax.set_ylabel('Coefficient', fontsize=12)
            ax.set_title("Posterior Distributions with 89% Intervals", fontsize=14)
            plt.show()


    def trace(self, model):
        with plt.style.context('seaborn-whitegrid'):
            fig = plt.figure(figsize=(14, 4), constrained_layout=True)
            spec = fig.add_gridspec(2, 3)
            ax0 = fig.add_subplot(spec[:, 2])
            az.plot_energy(model.post, ax=ax0, fill_alpha=[.6,.6])
            ax0.set_title("Energy Function of Model", fontsize=12)
            ax10 = fig.add_subplot(spec[0, 0])
            ax11 = fig.add_subplot(spec[0, 1])
            ax20 = fig.add_subplot(spec[1, 0])
            ax21 = fig.add_subplot(spec[1, 1])
            ax=np.array([[ax10,ax11], [ax20, ax21]])
            az.plot_trace(model.post,
                          var_names=['beta', 'sigma'],
                          axes=ax)
            ax10.set_title("Posterior Distribution of betas", fontsize=12)
            ax11.set_title("Trace of betas", fontsize=12)
            ax20.set_title("Posterior Distribution of sigma", fontsize=12)
            ax21.set_title("Trace of simga", fontsize=12)
            fig.suptitle('Model Checking based on Energy and Trace', fontsize=17)
            plt.show()


if __name__ == "__main__":
    df = pd.read_csv("/Users/anton/Documents/University/Semester_7/Bachelor_Thesis/data/analysis/polls.csv")
    df.rename(columns={'datum':'Date'}, inplace=True)
    df["Date"] = pd.to_datetime(df.Date)
    plotter = Plotter()
    plotter.trends(df)