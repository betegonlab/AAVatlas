import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_pdf_viewer import pdf_viewer
import kaleido
import AAVatlas_Class as aa

st.set_page_config(layout="wide")
st.set_page_config(page_title="PGH AAVatlas", page_icon="favicon.ico")

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
	st.image("PAA_Logo.png")
    st.sidebar.header("Pittsburgh AAV atlas")
    
    selected = option_menu("", ["By serotype", 'By cell type'],
        icons=['virus', 'vignette'], menu_icon="cast", default_index=0)

    st.text(' ')

    st.text("Funded by:")
    st.image("FNIH_logo.svg")
    st.text(' ')

    st.text('Developed by:')
    st.page_link('https://www.byrnelab.science/', label='The :blue[Byrne lab]')
    st.page_link('https://www.betegonlab.science/', label='The :blue[Betegon lab]')
    st.image("Pitt_logo.png")

    st.text("and")

    st.image("AvistaTX.png")
    st.page_link('https://www.avistatx.com', label=':blue[Avista Therapeutics]')

if selected == "By serotype":
	st.subheader("AAV serotype")
	col1, col2, col3 = st.columns(3)
	with col1:
		serotype_selected = st.selectbox(
		    "Select serotype",
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
			st.text("Data available soon")

		cellsPlot = atlas.cellsPlot(serotype)
		if cellsPlot != None:
			st.plotly_chart(cellsPlot, theme='streamlit', use_container_width=False)
			#st.text("(Click on a cell type name to show/hide. Double-click on a cell type name to show only that cell type/show all)")

# Infectivity tab
	with tab_infec:

		infectivityPlot = atlas.infectivityPlot(serotype)
		if infectivityPlot != None:
			st.plotly_chart(infectivityPlot, theme='streamlit', use_container_width=False)
		else:
			st.text("Data available soon")

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
			st.text("Data available soon")


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
			st.text("Data available soon")

# Data tab
	with tab_raw:
		st.text("Single-cell sequencing data is available at NCBI GEO:")
		st.link_button("Access raw data", "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSEXXXXXX")

# Immune response tab
	with tab_immuno:
		st.subheader("Immune response markers")
		try:
			st.image(atlas.dataPath+serotype+"/"+serotype+"_dotplot.jpg", width= 800)
			st.text(' ')
			st.image(atlas.dataPath+serotype+"/"+serotype+"_violin.jpg", width= 800)
			st.text(' ')
			st.image(atlas.dataPath+serotype+"/"+serotype+"_umap.jpg")
		except:
			st.text("Data available soon")


if selected == "By cell type":
	st.subheader("Cell type")
	col1, col2, col3 = st.columns(3)
	with col1:
		celltype_selected = st.selectbox(
		    '',
		    ("Rod","Cone","Retinal Ganglion Cell","Off-Bipolar","On-Bipolar","Horizontal Cell","Microglia","Muller Glia","Glia","Microglia","Amacrine Cell","Pericyte")
		)
		celltype = celltype_selected

	st.subheader(celltype_selected)
	st.text("Only serotypes and titers for which infected cells were detected are shown.")

	celltypePlot = atlas.celltypePlot(celltype_selected)
	if celltypePlot != None:
		st.plotly_chart(celltypePlot, theme='streamlit', use_container_width=False)
	else:
		st.text("Data available soon")
