import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_pdf_viewer import pdf_viewer

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


@st.cache_data
def load_data(data_path):
    data = pd.read_csv(data_path)
    return data

@st.cache_data
def load_data_umap(data_path):
    umap_data = pd.read_csv(data_path)
    infected_data = pd.DataFrame()
    umap_data.drop('full_cell_id', inplace=True, axis=1)
    return umap_data

@st.cache_resource
def plot_umap(serotype_name):
	fig = px.scatter(
		umap_data,
		x='umap1',
		y='umap2',
		color='cell_type',
		width=1200,
		height=700,
		color_discrete_map={"Cells infected": "black"},
		hover_data={'umap1':False, 'umap2':False, 'cell_type':False, 'Cell type':umap_data['cell_type']}
	)
	fig.update_traces(marker_size=3)
	fig.update_traces(mode='markers')

	#fig.add_trace(umap_data['umap1'], umap_data['umap2'], umap_data['cells_with_BC2'].bool())

	fig.update_layout(title=serotype_name + ' UMAP')
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
	    dfs['1E'+str(i)] = pd.read_csv(serotype_name+'_subsample_cells_1e'+str(i)+'.txt', delimiter='\t', header=None, names=["Sampled_cells", "Infected"])
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
	fig2.update_traces(hovertemplate="<br>".join(["Cells sampled: %{x:,.2r}","Cells infected: %{y}"]))
	fig2.update_traces(marker_size=8)

	return st.plotly_chart(fig2, theme='streamlit', use_container_width=False)

tab_umap, tab_infec, tab_immuno, tab_qc, tab_imaging, tab_raw = st.tabs(["Infectivity UMAP", "Dose infectivity", "Immune response", "AAV QC", "NHP imaging", "Raw data"])

with tab_umap:
	umap_file = 'proc_'+serotype+"_dilution_curve_umap_cell_type_aav_binary.csv"
	umap_data = load_data_umap(umap_file)
	plot_umap(serotype)

with tab_infec:
	import plotly.graph_objects as go
	import plotly.io as pio
	plot_infectivity(serotype)

with tab_qc:
	pdf_viewer(serotype+"_qc.pdf", height=800)

with tab_imaging:
	st.write("Imaging was performed on a Heidelberg Spectralis OCT imaging system, under sedation, following dilation with tropicamide.")
	pdf_viewer(serotype+"_imaging.pdf", height=800)
	st.subheader("Pre-OP OCT imaging")
	st.image(serotype+"_OCT_pre.png", width=600)
	st.subheader("30 days post-injection OCT imaging")
	st.image(serotype+"_OCT_post.png", width=600)

