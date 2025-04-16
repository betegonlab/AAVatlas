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

st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 250px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.sidebar.header("Pittsburgh AAV atlas")
    st.image("PAA_Logo.png")
    selected = option_menu("", ["By serotype", 'By cell type'], 
        icons=['virus', 'vignette'], menu_icon="cast", default_index=0)

    st.text(' ')
    st.text(' ')
    st.text(' ')
    st.text(' ')
    st.text(' ')
    st.text("Funded by:")
    st.image("FNIH_logo.svg")
    st.text(' ')
    st.text(' ')
    st.text(' ')
    st.text(' ')
    st.text(' ')
    st.text('Developed by:')
    st.page_link('https://www.byrnelab.science/', label='The :blue[Byrne lab]')
    st.page_link('https://www.betegonlab.science/', label='The :blue[Betegon lab]')
    st.image("Pitt_logo.png")

if selected == "By serotype":
	st.subheader("AAV serotype")
	col1, col2, col3 = st.columns(3)
	with col1:
		serotype_selected = st.selectbox(
		    "",
		    atlas.serotypes
		)
		serotype = serotype_selected
	
	st.subheader(serotype)
	
	
	tab_umap, tab_infec, tab_immuno, tab_qc, tab_imaging, tab_raw = st.tabs(["Infectivity UMAP", "Dose infectivity", "Immune response", "AAV QC", "NHP information", "Raw data"])

# umap tab	
	with tab_umap:

		umapPlot = atlas.umapPlot(serotype)
		if umapPlot != None:
			st.text("Click on a cell type name to show/hide. Double-click on a cell type name to show only that cell type/show all.")
			st.plotly_chart(umapPlot, theme='streamlit', use_container_width=False)
		else:
			st.text("No data found")

		cellsPlot = atlas.cellsPlot(serotype)
		if cellsPlot != None:
			st.plotly_chart(cellsPlot, theme='streamlit', use_container_width=False)
			#st.text("(Click on a cell type name to show/hide. Double-click on a cell type name to show only that cell type/show all)")
		else:
			st.text("No data found")

# Infectivity tab
	with tab_infec:

		infectivityPlot = atlas.infectivityPlot(serotype)
		if infectivityPlot != None:
			st.plotly_chart(infectivityPlot, theme='streamlit', use_container_width=False)
		else:
			st.text("No data found")

# AAV QC tab	
	with tab_qc:

		try:
			pdf = atlas.loadPDF(atlas.dataPath+serotype+"/"+serotype+"_qc.pdf")
			st.download_button(
	    		label="Download "+serotype+" QC pdf",
	    		file_name=serotype+"_qc.pdf",
				data=pdf,
	    		mime="application/pdf",
	    		icon=":material/download:",
			)
			#st.link_button("Download "+serotype+" QC pdf", atlas.dataPath+serotype+"/"+serotype+"_qc.pdf")
			pdf_viewer(atlas.dataPath+serotype+"/"+serotype+"_qc.pdf", width=1200)
			
		except:
			st.text("No data found")
	

# NHP info tab
	with tab_imaging:

		try:
			pdf = atlas.loadPDF(atlas.dataPath+serotype+"/"+serotype+"_imaging.pdf")
			st.download_button(
	    		label="Download "+serotype+" imaging pdf",
	    		file_name=serotype+"_imaging.pdf",
				data=pdf,
	    		mime="application/pdf",
	    		icon=":material/download:",
			)
			#st.link_button("Download "+serotype+" imaging pdf", atlas.dataPath+serotype+"/"+serotype+"_imaging.pdf")
			pdf_viewer(atlas.dataPath+serotype+"/"+serotype+"_imaging.pdf", width=1200) #, height=800, width=1000)
		
		except:
			st.text("No data found")

# Data tab
	with tab_raw:
		st.text("Single-cell sequencing data is available at NCBI GEO:")
		st.link_button("Access raw data", "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSEXXXXXX")
		
	
if selected == "By cell type":
	st.subheader("Cell type")
	col1, col2, col3 = st.columns(3)
	with col1:
		celltype_selected = st.selectbox(
		    '',
		    ("Rod","Cone","Retinal Ganglion Cell","Horizontal Cell","Microglia","Muller Glia","Off-Bipolar","On-Bipolar", "Retinal pigment epithelium", "Amacrine Cell")
		)
		celltype = celltype_selected
	
	st.subheader(celltype_selected)

	celltypePlot = atlas.celltypePlot(celltype_selected)
	if celltypePlot != None:
		st.plotly_chart(celltypePlot, theme='streamlit', use_container_width=False)
	else:
		st.text("No data found")

