
import matplotlib.pyplot as plt
import arviz as az
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime

class Plotter:
    
    def __init__(self, var="ÖVP"):
        self.var = var
    

    def scatter(self, df, save=False):
        df = df.copy()
        months = df.Date.dt.strftime("%b").unique()
        with plt.style.context('ggplot'):
            fig, ax = plt.subplots(figsize=(10,5))
            ax.scatter("Date", self.var, data=df[df["Treatment"]==1], 
                       label="Research Affairs", c='gray', s=25)
            ax.scatter("Date", self.var, data=df[df["Treatment"]==0], 
                       label="Other Institutes", c='black', s=25)
            ax.axvline(datetime(2017,5,10), c='lightgrey', ls="--", label="Leadership Change")
            ax.legend(fancybox=True)
            ax.set(xticklabels=months)  
            ax.set_ylabel("Estimated Voting % for " + str(self.var))
            ax.set_title("Descriptive Plot of Data")
            plt.show()
            
            if save is True:
                path = Path(__file__).parent.parent / "images" / "descriptive.csv"
                fig.savefig(path, dpi=300)
                
    
    def pre_trends(self, df):            
        df = df.copy() 
        df["group"] = np.where(df.Date < datetime(2017,3,10), 1,
                               np.where(df.Date < datetime(2017,5,10),2,
                                        np.where(df.Date < datetime(2017,7,10),3,4)))
        d1 = []
        d0 = []
        for treat, d in enumerate([d0,d1]):
            for group in df.group.unique():     
                d.append(df.loc[(df.Treatment==treat) & (df.group==group)][self.var].values)

        with plt.style.context('ggplot'):
            gap = 0.1
            fig, ax = plt.subplots(figsize=(10,5))
            ax.boxplot(d0,
                       positions=np.array(np.arange(len(d0)))*2.0-gap,
                       widths=0.2,
                       showbox=False,
                       showfliers=False,
                       showmeans=True,
                       medianprops={"color": "white", "linewidth": 0.0001},
                       meanprops=dict(marker='D', markeredgecolor='black',
                                      markerfacecolor='black'),
                       whiskerprops={"color": "black", "linewidth": 1},
                       capprops={"color": "white", "linewidth": 0.00001})
            ax.boxplot(d1,
                       positions=np.array(np.arange(len(d1)))*2.0+gap,
                       widths=0.2,
                       showbox=False,
                       showfliers=False,
                       showmeans=True,
                       medianprops={"color": "white", "linewidth": 0.0001},
                       whiskerprops={"color": "gray", "linewidth": 1},
                       meanprops=dict(marker='D', markeredgecolor='gray',
                                      markerfacecolor='gray'),
                       capprops={"color": "white", "linewidth": 0.00001})
            ax.plot(np.array(np.arange(len(d1)))*2.0+gap, df[df.Treatment==1].groupby("group")[self.var].mean().values,
                    color="gray",
                    linestyle='dashed',
                    label="Research Affairs")
            ax.plot(np.array(np.arange(len(d0)))*2.0-gap, df[df.Treatment==0].groupby("group")[self.var].mean().values,
                    color="black",
                    linestyle='dashed',
                    label="Other Institutes")
            ticks = ['Pre 2', 'Pre 1', 'Post 1', 'Post 2']
            plt.xticks(np.arange(0, len(ticks) * 2, 2), ticks)
            ax.legend(fancybox=True)
            ax.set_xlabel("Time periods of two Months")
            ax.set_ylabel("Estimated Voting % for " + str(self.var))
            ax.set_title("Pre-trends based on binning")
            plt.show()


    def compare_models(self, model1, model2, kind='forestplot'):
        # Rename Betas
        posterior1 = az.convert_to_inference_data(model1.fit)
        posterior2 = az.convert_to_inference_data(model2.fit)

        with az.style.context("arviz-whitegrid"):
            fig = plt.figure(figsize=(13, 5), constrained_layout=True)
            spec = fig.add_gridspec(2, 3)
            ax0 = fig.add_subplot(spec[0, :])
            az.plot_forest(
                [posterior1, posterior2], 
                model_names=["Imputation Model", "Naive Model"], 
                var_names=["beta"],
                kind=kind,
                combined=False,
                ridgeplot_overlap=1.1,
                figsize=(9, 4),
                ax=ax0
            )
            ax0.set_yticklabels([]) 
            ax0.set_title("99% Interval", fontsize=10)

            ax10 = fig.add_subplot(spec[1, 0])
            ax11 = fig.add_subplot(spec[1, 1])
            ax12 = fig.add_subplot(spec[1, 2]) 
            ax=[ax10,ax12,ax11] 
            az.plot_density([posterior1, posterior2], 
                data_labels=["Imputation Model", "Naive Model"], 
                var_names="beta",
                bw=.99,
                ax=ax
            )
            for axs, name in zip(ax, ["Group", "Time", "DiD"]):
                axs.set_title("")
                axs.set_xlabel(name)
            ax10.get_legend().remove()
            fig.suptitle("Overview over Results of Bayesian Regression Models", fontsize=20)
            plt.show()
            
            
    def plot_posterior(self, model):
        posterior = az.convert_to_inference_data(model.fit)
        with az.style.context("arviz-whitegrid"):
            az.plot_posterior(posterior, 
                              var_names="beta",
                              show=True,
                              ref_val=[-1.78, 13.92, 5.85]
                              )



    def plot_timeline(self):
        dates = [datetime(2019, 11, 12), datetime(2021, 10, 6), datetime(2021, 12, 2), datetime(2021, 12, 20), datetime(2022, 1, 20), datetime(2022, 2, 25)]
        min_date = datetime(np.min(dates).year - 2, np.min(dates).month, np.min(dates).day)
        max_date = datetime(np.max(dates).year + 2, np.max(dates).month, np.max(dates).day)
        labels = ['Elvis appears on\nthe Ed Sullivan Show', 'Buddy Holly dies', 'The Beatles appear\non the Ed Sullivan Show', 
          'Bob Dylan goes electric', 'The Beatles release\nSgt. Pepper', 'Woodstock']
        # labels with associated dates
        labels = ['{0:%d %b %Y}:\n{1}'.format(d, l) for l, d in zip (labels, dates)]
        with plt.style.context('ggplot'):
            fig, ax = plt.subplots(figsize=(15, 4), constrained_layout=True)
            _ = ax.set_ylim(-2, 1.75)
            _ = ax.set_xlim(min_date, max_date)
            _ = ax.axhline(0, xmin=0.05, xmax=0.95, c='deeppink', zorder=1)
            label_offsets = np.zeros(len(dates))
            label_offsets[::2] = 0.35
            label_offsets[1::2] = -0.7
            for i, (l, d) in enumerate(zip(labels, dates)):
                _ = ax.text(d, label_offsets[i], l, ha='center', fontfamily='serif', fontweight='bold', color='royalblue',fontsize=12)
            label_offsets = np.zeros(len(dates))
            label_offsets[::2] = 0.35
            label_offsets[1::2] = -0.7
            for i, (l, d) in enumerate(zip(labels, dates)):
                _ = ax.text(d, label_offsets[i], l, ha='center', fontfamily='serif', fontweight='bold', color='royalblue',fontsize=12)
            stems = np.zeros(len(dates))
            stems[::2] = 0.3
            stems[1::2] = -0.3   
            markerline, stemline, baseline = ax.stem(dates, stems, use_line_collection=True)
            _ = plt.setp(markerline, marker=',', color='darkmagenta')
            _ = plt.setp(stemline, color='darkmagenta')         
            # hide lines around chart
            for spine in ["left", "top", "right", "bottom"]:
                _ = ax.spines[spine].set_visible(False)
            
            # hide tick labels
            _ = ax.set_xticks([])
            _ = ax.set_yticks([])
            
            _ = ax.set_title('Important Milestones in Rock and Roll', fontweight="bold", fontfamily='serif', fontsize=16, 
                            color='royalblue')
            
            
if __name__ == "__main__":
    data = pd.read_csv("/Users/anton/Documents/University/Semester_7/Bachelor_Thesis/data/analysis/au_polls.csv")
    data["Date"] = pd.to_datetime(data.Date)
    plotter = Plotter()
    plotter.scatter(data)