import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_pdf_viewer import pdf_viewer
import AAVatlas_Class as aa

st.set_page_config(layout="wide")

serotype = "K912"

atlas = aa.AAVatlas()

from streamlit_option_menu import option_menu

with st.sidebar:
    selected = option_menu("Pittsburgh AAV atlas", ["By serotype", 'By cell type'], 
        icons=['virus', 'vignette'], menu_icon="cast", default_index=0)

if selected == "By serotype":
	col1, col2, col3 = st.columns(3)
	with col1:
		serotype_selected = st.selectbox(
		    "Select an AAV serotype:",
		    atlas.serotypes
		)
		serotype = serotype_selected
	
	st.subheader(serotype)
	
	
	@st.cache_data
	def load_data(data_path):
		data = pd.read_csv(data_path)
		return data
	
	
	tab_umap, tab_infec, tab_immuno, tab_qc, tab_imaging, tab_raw = st.tabs(["Infectivity UMAP", "Dose infectivity", "Immune response", "AAV QC", "NHP imaging", "Raw data"])
	
	with tab_umap:
		umapPlot = atlas.umapPlot(serotype)
		if umapPlot != None:
			st.plotly_chart(umapPlot, theme='streamlit', use_container_width=False)
			#st.text("(Click on a cell type name to show/hide. Double-click on a cell type name to show only that cell type/show all)")
		else:
			st.text("No data found")

	with tab_infec:
		infectivityPlot = atlas.infectivityPlot(serotype)
		if infectivityPlot != None:
			st.plotly_chart(infectivityPlot, theme='streamlit', use_container_width=False)
		else:
			st.text("No data found")
	
	with tab_qc:
		try:
			f_qc = open(serotype+"_qc.pdf", 'rb')
			st.download_button(
				label="Download "+serotype+" QC PDF",
				file_name=atlas.dataPath+serotype+"/"+serotype+"_qc.pdf",
				data=f_qc,
				mime="application/pdf",
				icon=":material/download:",
			)
			pdf_viewer(atlas.dataPath+serotype+"/"+serotype+"_qc.pdf") #, height=800, width=1000)\
		except:
			st.text("No data found")
	
	with tab_imaging:
		try:
			f_img = open(serotype+"_imaging.pdf", 'rb')
			st.download_button(
		    	label="Download "+serotype+" imaging PDF",
		    	file_name=atlas.dataPath+serotype+"/"+serotype+"_imaging.pdf",
				data=f_img,
		    	mime="application/pdf",
		    	icon=":material/download:",
			)
			pdf_viewer(atlas.dataPath+serotype+"/"+serotype+"_imaging.pdf") #, height=800, width=1000)
		except:
			st.text("No data found")
	
if selected == "By cell type":
	col1, col2, col3 = st.columns(3)
	with col1:
		celltype_selected = st.selectbox(
		    "Select a cell type:",
		    ("Rods","Cones","RGCs")
		)
		celltype = celltype_selected
	
	st.subheader(celltype_selected)
