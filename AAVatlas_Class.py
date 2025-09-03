import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

class AAVatlas():

    def __init__(self):
        self.dataPath = 'data/'
        self.serotypes = files_dir = [f for f in os.listdir(self.dataPath) if os.path.isdir(os.path.join(self.dataPath, f))]

    @st.cache_resource
    def cellsPlot(_self, serotype):
        try:
            cells_data = pd.read_csv(_self.dataPath+serotype+"/"+serotype+"_infected_cells.csv")
        except:
            return None

        cellsFig = px.histogram(cells_data, x="cell_type", y=["10E7", "10E8", "10E9", "10E10", "10E11", "10E12"],
            barmode='group',
            height=600,
            width=1200,
            log_y=True)
        cellsFig.update_layout(title=serotype + ' cell type infectivity')
        cellsFig.update_layout(legend_title='AAV titer')
        cellsFig.update_layout(legend_itemsizing='constant')
        cellsFig.update_layout(xaxis_title="", yaxis_title="Number of cells infected")
        cellsFig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
        cellsFig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)

        return cellsFig

    @st.cache_resource
    def celltypePlot(_self, celltypeName):
        availableSerotypes = []
        for serotype in _self.serotypes:
            if os.path.exists(_self.dataPath+serotype+"/"+serotype+"_infected_cells.csv"):
                availableSerotypes.append(serotype)

        if availableSerotypes == []:
            return None

        celltype_data = pd.concat((pd.read_csv(_self.dataPath+serotype+"/"+serotype+"_infected_cells.csv") for serotype in availableSerotypes), ignore_index=True)
        celltype_data = celltype_data.loc[celltype_data['cell_type'] == celltypeName]

        celltypeFig = px.histogram(celltype_data, x="serotype", y=["10E7", "10E8", "10E9", "10E10", "10E11", "10E12", "10E13"],
            text_auto='.0f',
            barmode='group',
            height=600,
            width=1200)
        celltypeFig.update_layout(title='AAV infectivity for ' + celltypeName + ' at increasing titers')
        celltypeFig.update_layout(legend_title='AAV titer')
        celltypeFig.update_layout(legend_itemsizing='constant')
        celltypeFig.update_layout(xaxis_title="", yaxis_title="Number of cells infected")
        celltypeFig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
        celltypeFig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)

        return celltypeFig

    @st.cache_resource
    def umapPlot(_self, serotype):
        try:
            umap_data = pd.read_csv(_self.dataPath+serotype+"/"+serotype+"_umap.csv")
        except:
            return None

        umapFig = px.scatter(
			umap_data,
			x='umap1',
			y='umap2',
			color='cell_type',
			width=1200,
			height=700,
			color_discrete_map={
				"Cells infected at AAV titer 10^7": "black",
				"Cells infected at AAV titer 10^8": "black",
				"Cells infected at AAV titer 10^9": "black",
				"Cells infected at AAV titer 10^10": "black",
				"Cells infected at AAV titer 10^11": "black",
				"Cells infected at AAV titer 10^12": "black",
				"Cells infected at AAV titer 10^13": "black"
			},
			hover_data={'umap1':False, 'umap2':False, 'cell_type':False, 'Cell type':umap_data['cell_type']}
		)
        umapFig.update_traces(marker_size=3)
        umapFig.update_traces(mode='markers')

		#umapFig.add_trace(umap_data['umap1'], umap_data['umap2'], umap_data['cells_with_BC2'].bool())

        umapFig.update_layout(title=serotype + ' UMAP')
        umapFig.update_layout(legend_title='Cell type')
        umapFig.update_layout(legend_itemsizing='constant')
        #umapFig.update_layout(
		#    xaxis_range=umapFig.full_figure_for_development(warn=False).layout.xaxis.range,
		#    yaxis_range=umapFig.full_figure_for_development(warn=False).layout.yaxis.range,
		#)
        umapFig.update_layout(plot_bgcolor='#ffffff')
        umapFig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
        umapFig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)

        return umapFig


    @st.cache_resource
    def loadPDF(_self, fileName):
        try:
            pdf = open(fileName, 'rb')
        except:
            return None
        return pdf

    @st.cache_resource
    def infectivityPlot(_self, serotype):
        dfs = {}
        infectivityFig = go.Figure()
        try:
            for i in range(13,6,-1):
                try:
                    dfs['1E'+str(i)] = pd.read_csv(_self.dataPath+serotype+"/"+serotype+'_subsample_cells_1e'+str(i)+'.txt', skiprows=0, header=None, names=["Sampled_cells", "Infected"])
                except:
                    continue
                infectivityFig.add_trace(go.Scatter(x=dfs['1E'+str(i)]["Sampled_cells"], y=dfs['1E'+str(i)]["Infected"], name='1E'+str(i)))
        except:
            return None

        infectivityFig.update_layout(
		    title=serotype + " infectivity",
		    xaxis_title="Number of cells sampled",
		    yaxis_title="Number of cells infected",
		    legend_title="AAV titer",
		    width=1000,
		    height=650
		)
        infectivityFig.update_layout(plot_bgcolor='#ffffff')
        infectivityFig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
        infectivityFig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
        infectivityFig.update_traces(mode='markers+lines')
        infectivityFig.update_traces(hovertemplate="<br>".join(["Cells sampled: %{x:,.2r}","Cells infected: %{y}"]))
        infectivityFig.update_traces(marker_size=8)

        return infectivityFig
