import stumpy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#import Rectanmgle
from matplotlib.patches import Rectangle
import plotly.graph_objects as go
import plotly.graph_objs as go
from plotly.subplots import make_subplots



class SimilarPattern:
    """
    Class to obtain the similar pattern of a given sequence. The sequence could be 2D or 1D.
    For 2D the columns are stacked to obtain a 1D sequence, ready to be used by stumpy.
    """
    def __init__(self,df, subsequence):
        if not isinstance(df, pd.DataFrame):
            df=df.to_frame()
            
        self.df = df
        self.subsequence = subsequence
        self.y = df.stack().reset_index(drop=True)
        self.x = df.stack().reset_index(drop=True).index
        self.m = subsequence*df.columns.size
        
    def get_matrix_profile(self):
        
        matrix_profile = stumpy.stump(self.y, self.m)
        self.matrix_profile_df = pd.DataFrame(matrix_profile, columns=['profile', 'profile index', 'left profile index', 'right profile index'])
        return self.matrix_profile_df
    
    def _get_values(self,df,columns,remove_):
        """
        Obtains the different values of a dataframe selecting the columns to seek
        
        Parameters
        ----------
        df: pandas.DataFrame
            Dataframe to obtain the values
        columns: list
            Columns to obtain the values

        Returns
        -------
        values: list
            List of the values of the columns

        """
        values=[]
        for col in columns:
            values.extend(df[col].unique())
        values=np.unique(values).tolist()
        values.remove(remove_)
        #make an array of int
        return np.array(values)

    def get_similar_pattern(self,date):
        """
        Obtains the similar date pattern to the given date
        
        Parameters
        ----------
        date: str
            Date to obtain the similar pattern

        Returns
        -------
        patron: str or tuple
            Date of the similar pattern

        """
        slice_index=self.df.index.get_loc(date)
        start_index=slice_index.start
        self.stumpy_index=start_index*self.df.columns.size

        matrix_profile_df=self.get_matrix_profile()
        matrix_profile_df_=matrix_profile_df[(matrix_profile_df['right profile index'] != -1) & (matrix_profile_df['left profile index'] != -1)]
        self.seek_motif=matrix_profile_df[matrix_profile_df['profile index'] == self.stumpy_index]
        close_values=self._get_values(self.seek_motif,['left profile index','right profile index'],self.stumpy_index.item())
        self.stumpy_close_values=close_values
        self.close_values=close_values/self.df.columns.size
        self.close_values=self.close_values.astype(int)
            

        patron= [self.df.iloc[int(i)].to_frame().T.index[0].strftime('%Y-%m-%d') for i in self.close_values]

        return patron
    
    def plot_similar_pattern(self,date):
        """
        Plot similar pattern of a given date

        Parameters
        ----------
        date : str
            Date to plot similar pattern
        """
        patron=self.get_similar_pattern(date)
        self.patron=patron
        height_adjuts= len(patron)
        try:
            patron_profile=[pat + ", " + str(round(self.seek_motif.reset_index().profile.iloc[i],3)) for i, pat in enumerate(patron)]
        except:
            
            patron_profile=patron

        fig = make_subplots(rows=len(patron), cols=1, vertical_spacing=0.1, subplot_titles= patron_profile )

        for i,idx in enumerate(self.stumpy_close_values):
            plot_y = self.y.iloc[idx:idx.item()+self.m].to_list()
            plot_base = self.y.iloc[self.stumpy_index:self.stumpy_index+self.m].to_list()
           
            fig.add_trace(go.Scatter(x=np.linspace(0,self.subsequence-1,len(list(range(len(plot_y))))), y=plot_y, name=patron[i] ), row=i+1, col=1)
            fig.add_trace(go.Scatter(x=np.linspace(0,self.subsequence-1,len(list(range(len(plot_base))))), y=plot_base, name=date, line={'color': '#000000'}), row=i+1, col=1)
            fig.update_yaxes(title_text="Serie {}".format(i+1), row=i+1, col=1)

        #indicate all int x values in the x axis
            fig.update_xaxes(tickmode = 'array', tickvals = np.linspace(0,self.subsequence-1,self.subsequence), row=i+1, col=1)
        fig.update_layout(title_text="Patrones similares para {}".format(date), title_x=0.5, height=800+height_adjuts*100)
        #x name as Hour
        fig.update_xaxes(title_text="Hour")
        fig.update_yaxes(title_text="Valor")
        #tight layout automatically adjusts subplot params so that the subplot(s) fits in to the figure area
        fig.update_layout(showlegend=True, title_x=0.5, title_font_size=20, title_font_color="black", title_font_family="Arial", title_xanchor="center", title_yanchor="top",
                          margin=dict(t=100, b=50, l=50, r=50))
        fig.show()
