import numpy as np
import pandas as pd
import datetime as dt
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Online Store Analysis",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/mfadlili',
        'Report a bug': "https://github.com/mfadlili",
        'About': "# This is hacktiv8 Data Science Talent Fair project."
    }
)
selected = st.sidebar.selectbox('Select Page: ', ['Business Overview', 'Cohort & RFM Analysis'])

@st.cache(allow_output_mutation=True)
def load_data1():
    data1 = pd.read_csv('user-events1.csv')
    data2 = pd.read_csv('user-events2.csv')
    data = pd.concat([data1, data2])
    return data

@st.cache(allow_output_mutation=True)
def load_data2():
    data = pd.read_csv('rfm.csv')
    return data

df = load_data1()
df['month'] = pd.to_datetime(df['event_time']).dt.month
df['month'] = df['month'].map({9:1, 10:2, 11:3, 12:4, 1:5, 2:6})
df['event_time'] = pd.to_datetime(df['event_time'])
rfm = load_data2()

if selected == 'Business Overview':
    st.title('Business Review')
    st.title('')
    col1, col2, col3 = st.columns(3)

    def total_sales():
        total_sales = df[df.event_type=='purchase'].price.sum()
        st.metric(label="Total Penjualan", value='$'+str(total_sales))

    def quantity():
        total_quantity_sold = len(df[df.event_type=='purchase'])
        st.metric(label="Total Barang Terjual", value=str(total_quantity_sold)+' unit')

    def customer():
        total_active_customer = df[df.event_type=='purchase'].user_id.nunique()
        st.metric(label="Total Pelanggan Aktif", value=str(total_active_customer)+' orang')

    with col1:
        total_sales()

    with col2:
        quantity()

    with col3:
        customer()
    
    st.title(' ')
    st.title(' ')
    st.title(' ')

    col4, col5 = st.columns(2)

    with col4:
        st.markdown("<h2 style='text-align: center; color: black;'>Aktivitas Pengunjung</h2>", unsafe_allow_html=True)
        bulan = st.selectbox('Pilih bulan:', ['Semua', 1, 2, 3, 4, 5, 6])
        if bulan=='Semua':
            buat_pie = df["event_type"].value_counts().reset_index()
            fig = px.pie(buat_pie,values='event_type',names='index',title=' ',hole=.4,height=600,width=500)
            fig.update_traces(textposition='outside', textinfo='percent+label')
            fig.update_layout(title='Aktivitas pengunjung di bulan 1 sampai 6')
            st.plotly_chart(fig)
        else:
            buat_pie = df[df.month==bulan]["event_type"].value_counts().reset_index()
            fig = px.pie(buat_pie,values='event_type',names='index',title=' ',hole=.4,height=600,width=500)
            fig.update_traces(textposition='outside', textinfo='percent+label')
            fig.update_layout(title='Aktivitas pengunjung di bulan '+str(bulan))
            st.plotly_chart(fig)            
    
    with col5:
        st.markdown("<h2 style='text-align: center; color: black;'>Distribusi Aktivitas Pengunjung Tiap Bulan</h2>", unsafe_allow_html=True)
        aktivitas = st.selectbox('Pilih aktivitas:', ['view', 'cart', 'purchase'])
        st.subheader(' ')
        lihat0 = df[df.event_type==aktivitas].groupby('month')[['product_id']].count().reset_index()
        fig2 = px.bar(lihat0,x='month',y='product_id',height=500,width=700, text_auto=True)
        fig2.update_traces(marker_color='#0000FF')
        fig2.update_layout(title = 'Jumlah '+ aktivitas+' per bulan',xaxis_title='Bulan', yaxis_title=' ')
        st.plotly_chart(fig2) 
    
    col4, col5 = st.columns(2)
    with col4:
        st.markdown("<h2 style='text-align: center; color: black;'>Overview Per Bulan</h2>", unsafe_allow_html=True)
        pilih = st.selectbox('Pilih parameter:', ['Pelanggan aktif', 'Produk terjual', 'Pendapatan kotor'])
        st.title(' ')
        st.title(' ')
        st.subheader(' ')
        if pilih == 'Pelanggan aktif':
            lihat = df[df.event_type=='purchase'].groupby('month')[['user_id']].nunique().reset_index()
            fig2 = px.bar(lihat,x='month',y='user_id',height=500,width=700, text_auto=True)
            fig2.update_traces(marker_color='#5aa17f')
            fig2.update_layout(xaxis_title='Bulan',title='Jumlah pelanggan aktif per bulan', yaxis_title=' ')
            st.plotly_chart(fig2)
        elif pilih ==  'Produk terjual':
            lihat2 = df[df.event_type=='purchase'].groupby('month')[['product_id']].count().reset_index()
            fig2 = px.bar(lihat2,x='month',y='product_id',height=500,width=700, text_auto=True)
            fig2.update_traces(marker_color='#5aa17f')
            fig2.update_layout(xaxis_title='Bulan',title='Jumlah produk terjual per bulan', yaxis_title=' ')
            st.plotly_chart(fig2)            
        else:
            lihat3 = df[df.event_type=='purchase'].groupby('month')[['price']].sum().reset_index()
            fig2 = px.bar(lihat3,x='month',y='price',height=500,width=700, text_auto=True)
            fig2.update_traces(marker_color='#5aa17f')
            fig2.update_layout(xaxis_title='Bulan',yaxis_title='Jumlah Pendapatan Kotor ($)')
            st.plotly_chart(fig2)                     

    with col5:
        st.markdown("<h2 style='text-align: center; color: black;'>Top 10 Kategori/Produk</h2>", unsafe_allow_html=True)
        a = st.selectbox('Pilih aktivitas: ', ['view', 'cart', 'purchase'])
        b = st.selectbox('Category/Product:', ['category', 'product'])
        df_dist_event = pd.crosstab(df[b], df.event_type).sort_values('cart', ascending=False).head(10).reset_index()
        fig = px.bar(df_dist_event,y=b,x=a,color=b,color_discrete_sequence=['indianred'],height=500,width=700, text_auto='.2s')
        fig.update_layout(xaxis_title='Qty '+a,yaxis_title='Category',title='Top 10 '+b+' '+a, showlegend = False)
        st.plotly_chart(fig)

if selected == 'Cohort & RFM Analysis':
    st.title('Customer Analysis')
    st.title('')   
    st.markdown("<h2 style='text-align: left; color: black;'>1. Cohort Analysis</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        i = st.selectbox('Pilih aktivitas:  ', ['view', 'cart', 'purchase'])
        df_cohort = df[df.event_type==i][['user_id', 'event_time', 'price']]
        def get_month(x) : return dt.datetime(x.year,x.month,1)
        df_cohort['invoice_month'] = df_cohort['event_time'].apply(get_month)
        df_cohort2 = df_cohort.groupby('user_id').invoice_month.min().reset_index()
        df_cohort2.columns = ['user_id', 'cohort_month']
        hasil = df_cohort.merge(df_cohort2, left_on = 'user_id', right_on = 'user_id')
        hasil['month'] = (hasil['invoice_month'] - hasil['cohort_month'])
        hasil['month'] = round(hasil['month'].dt.days/30) +1
        hasil['cohort_month'] = hasil['cohort_month'].dt.to_period('M')
        cross_tab = pd.crosstab(hasil.cohort_month, hasil.month)
        cross_tab = cross_tab.divide(cross_tab.iloc[:, 0], axis=0).round(4)*100
        cross_tab.reset_index(inplace=True, drop=True)
        cross_tab.index = cross_tab.index.map({0:'Sep-20', 1:'Oct-20', 2:'Nov-20', 3:'Dec-20', 4:'Jan-21', 5:'Feb-21'})
        fig = px.imshow(cross_tab, text_auto=True, color_continuous_scale='Blues',height=500,width=650)
        fig.update_layout(yaxis_title='Bulan', xaxis_title='Cohort Index', title='Retention rates')
        st.plotly_chart(fig)
    
    st.markdown("<h2 style='text-align: left; color: black;'>2. RFM Analysis</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        l = st.selectbox('Pilih scoring:  ', ['Recency', 'Frequency', 'Monetary'])
        if l=='Recency':
            lihat1 = rfm.groupby('R').Recency.mean().reset_index()
            fig2 = px.bar(lihat1,x='R',y='Recency',height=500,width=700, text_auto=True)
            fig2.update_traces(marker_color='#5aa17f')
            fig2.update_layout(xaxis_title='R score',title='Rata-rata recency untuk tiap-tiap R score', yaxis_title='Rata-rata recency (hari)')
            st.plotly_chart(fig2)
        elif l=='Frequency':
            lihat1 = rfm.groupby('F').Frequency.mean().reset_index()
            fig2 = px.bar(lihat1,x='F',y='Frequency',height=500,width=700, text_auto=True)
            fig2.update_traces(marker_color='#5aa17f')
            fig2.update_layout(xaxis_title='F score',title='Rata-rata frequency untuk tiap-tiap F score', yaxis_title='Rata-rata frequency')
            st.plotly_chart(fig2)
        else:
            lihat1 = rfm.groupby('M').Monetary.mean().reset_index()
            fig2 = px.bar(lihat1,x='M',y='Monetary',height=500,width=700, text_auto=True)
            fig2.update_traces(marker_color='#5aa17f')
            fig2.update_layout(xaxis_title='M score',title='Rata-rata monetary untuk tiap-tiap M score', yaxis_title='Rata-rata monetary (dollar)')
            st.plotly_chart(fig2)
    with col2:
        st.title(' ')
        st.title(' ')
        st.subheader(' ')
        b = rfm.groupby('RFM_Score').user_id.count().reset_index()
        fig2 = px.bar(b,x='RFM_Score',y='user_id',height=500,width=700, text_auto=True,color_discrete_sequence=['indianred'])
        fig2.update_layout(xaxis_title='RFM_Score',title='Distribusi pengguna berdasarkan RFM score', yaxis_title='Jumlah pengguna')
        st.plotly_chart(fig2)
