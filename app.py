import streamlit as st
import scanpy as sc
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

@st.cache(allow_output_mutation=True, show_spinner=False)
def load_data():
	adata = sc.read("test_norm.h5ad")
	return adata
adata = load_data()

gene_list = list(adata.var_names)
st.set_option('deprecation.showPyplotGlobalUse', False)
st.title('UMAP')

user_input = st.sidebar.multiselect("gene",gene_list,['FAM138A'])
if len(user_input) >0:
	user_input = user_input[0]
else: user_input = 'FAM138A'
coord = adata.obsm['X_umap']
#cluster = pd.Categorical(adata.obs['leiden']).astype(int)
a = adata[: , user_input].X.toarray().astype('float')
a_min = np.round_(np.min(a), decimals=1)
a_max = np.round_(np.max(a), decimals=1)
x = st.slider("Scale", 0.0, 4.0, (float(a_min), float(a_max)), 0.1)
plt.rcParams.update({
    "figure.facecolor":  (0.0, 0.0, 0.0, 0.0),  # red   with alpha = 30%
    #"axes.facecolor":    (0.0, 0.0, 0.0, 0.0),  # green with alpha = 50%
})

@st.cache(allow_output_mutation=True, show_spinner=False)
def get_fig():
	fig,ax = plt.subplots(figsize=(15,6))
	sc = ax.scatter(coord[:, 0], coord[:, 1], c = a, cmap = 'magma', s = 3,alpha=0.65, vmin = x[0], vmax = x[1])
	cb = fig.colorbar(sc, ax=ax)
	ax.axis('off')
	ax.set_title(user_input,color='white')
	cb.ax.yaxis.set_tick_params(color='white')
	plt.setp(plt.getp(cb.ax.axes, 'yticklabels'), color='white')
	return fig

st.pyplot(get_fig())