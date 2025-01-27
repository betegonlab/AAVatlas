import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(layout="wide")


serotype = "K912"
#serotype = st.query_params["sero"]

from streamlit_option_menu import option_menu

with st.sidebar:
    selected = option_menu("Pittsburgh AAV atlas", ["By serotype", 'By cell type'], 
        icons=['virus', 'vignette'], menu_icon="cast", default_index=0)

col1, col2, col3 = st.columns(3)
with col1:
	add_selectbox = st.selectbox(
	    "Select an AAV serotype:",
	    ("K912",)
	)

st.subheader(serotype)

DATA_PATH = "K912_dilution_curve_umap_cell_type_aav_binary.csv"

@st.cache_data
def load_data(data_path):
    data = pd.read_csv(data_path)
    return data

@st.cache_resource
def plot_umap(serotype_name):
	fig = px.scatter(
		umap_data,
		x='umap1',
		y='umap2',
		color='cell_type',
		width=1200,
		height=700,
		hover_data={'umap1':False, 'umap2':False, 'cell_type':False, 'Cell type':umap_data['cell_type']}
	)
	fig.update_traces(marker_size=2)
	fig.update_traces(mode='markers')

	#fig.add_trace(umap_data['umap1'], umap_data['umap2'], umap_data['cells_with_BC2'].bool())

	fig.update_layout(title=serotype + ' UMAP')
	fig.update_layout(legend_title='Cell type')
	fig.update_layout(legend_itemsizing='constant')
	fig.update_layout(
	    xaxis_range=fig.full_figure_for_development(warn=False).layout.xaxis.range,
	    yaxis_range=fig.full_figure_for_development(warn=False).layout.yaxis.range,
	)
	fig.update_layout(plot_bgcolor='#ffffff')
	fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
	fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
	
	return st.plotly_chart(fig, theme='streamlit', use_container_width=False)

@st.cache_resource
def plot_infectivity(serotype_name):
	dfs = {}
	fig2 = go.Figure()
	for i in range(12,6,-1):
	    dfs['1E'+str(i)] = pd.read_csv('K912_subsample_cells_1e'+str(i)+'.txt', delimiter='\t', header=None, names=["Sampled_cells", "Infected"])
	    fig2.add_trace(go.Scatter(x=dfs['1E'+str(i)]["Sampled_cells"], y=dfs['1E'+str(i)]["Infected"], name='1E'+str(i)))

	fig2.update_layout(
	    title=serotype + " infectivity",
	    xaxis_title="Number of cells sampled",
	    yaxis_title="Number of cells infected",
	    legend_title="AAV titer",
	    width=1000,
	    height=650
	)
	fig2.update_layout(plot_bgcolor='#ffffff')
	fig2.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
	fig2.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
	fig2.update_traces(mode='markers+lines')
	fig2.update_traces(hovertemplate="<br>".join(["Cells sampled: %{x:,.2r}","Cells infected: %{y}", "% infected: %{y/x}"]))
	fig2.update_traces(marker_size=8)

	return st.plotly_chart(fig2, theme='streamlit', use_container_width=False)

tab_umap, tab_infec, tab_immuno, tab_qc, tab_imaging, tab_raw = st.tabs(["Infectivity UMAP", "Dose infectivity", "Immune response", "AAV QC", "NHP imaging", "Raw data"])

with tab_umap:
	umap_data = load_data(DATA_PATH)
	umap_data.drop('full_cell_id', inplace=True, axis=1)
	plot_umap(serotype)

with tab_infec:
	import plotly.graph_objects as go
	import plotly.io as pio
	plot_infectivity(serotype)

with tab_qc:
	col1, col2, col3 = st.columns(3)
	with col1:
		st.subheader("AAV Quality Control:")
		qc_data = load_data("K912_QC.csv")
		qc_data.set_index('Test', inplace=True)
		st.table(qc_data)

with tab_imaging:
	st.write("Imaging was performed on a Heidelberg Spectralis OCT imaging system, under sedation, following dilation with tropicamide.")
	st.subheader("Pre-OP OCT imaging")
	st.image("K912_OCT_pre.png", width=600)
	st.subheader("30 days post-injection OCT imaging")
	st.image("K912_OCT_post.png", width=600)

