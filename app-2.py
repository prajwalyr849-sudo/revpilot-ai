import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title='RevPilot AI — Revenue Intelligence', page_icon='🚀', layout='wide')

@st.cache_data
def demo_data():
    rows=[
    ['C001',8500,'GROWTH',4,4200,'Email'],['C002',12500,'LOYAL',8,6800,'WhatsApp'],['C003',3200,'STANDARD',2,1800,'Email'],['C004',18500,'HIGH VALUE',10,9200,'Email + WhatsApp'],['C005',7600,'GROWTH',5,3900,'WhatsApp'],['C006',4100,'STANDARD',3,2200,'Email'],['C007',22400,'HIGH VALUE',12,11600,'Email + WhatsApp'],['C008',9800,'LOYAL',7,5100,'WhatsApp'],['C009',2900,'STANDARD',2,1500,'Email'],['C010',14300,'GROWTH',6,7300,'Email'],
    ['C011',5200,'STANDARD',3,2700,'Email'],['C012',16700,'LOYAL',9,8500,'Email + WhatsApp'],['C013',3800,'STANDARD',2,1900,'WhatsApp'],['C014',21100,'HIGH VALUE',11,10900,'Email + WhatsApp'],['C015',6900,'GROWTH',4,3500,'Email'],['C016',4700,'STANDARD',3,2400,'WhatsApp'],['C017',13200,'LOYAL',8,6900,'Email + WhatsApp'],['C018',28700,'HIGH VALUE',13,14200,'Email + WhatsApp'],['C019',34100,'HIGH VALUE',14,16900,'Email + WhatsApp'],['C020',6100,'GROWTH',4,3100,'Email'],
    ['C021',5300,'STANDARD',3,2600,'Email'],['C022',25600,'HIGH VALUE',10,12800,'Email + WhatsApp'],['C023',11800,'LOYAL',7,6200,'WhatsApp'],['C024',7300,'GROWTH',5,3700,'Email'],['C025',4500,'STANDARD',2,2100,'Email'],['C026',15600,'LOYAL',9,7900,'Email + WhatsApp'],['C027',8200,'GROWTH',5,4100,'WhatsApp'],['C028',3600,'STANDARD',2,1750,'Email'],['C029',19800,'HIGH VALUE',11,10100,'Email + WhatsApp'],['C030',9200,'LOYAL',6,4700,'WhatsApp'],
    ['C031',5100,'STANDARD',3,2500,'Email'],['C032',17600,'LOYAL',9,8800,'Email + WhatsApp'],['C033',6600,'GROWTH',4,3300,'Email'],['C034',3900,'STANDARD',2,1900,'WhatsApp'],['C035',23900,'HIGH VALUE',12,12100,'Email + WhatsApp'],['C036',10700,'LOYAL',7,5400,'WhatsApp'],['C037',5800,'STANDARD',3,2900,'Email'],['C038',14900,'GROWTH',6,7600,'Email'],['C039',4300,'STANDARD',2,2050,'WhatsApp'],['C040',312200,'HIGH VALUE',15,156000,'Email + WhatsApp'],
    ['C041',8700,'GROWTH',5,4400,'Email'],['C042',12700,'LOYAL',8,6400,'WhatsApp'],['C043',3400,'STANDARD',2,1650,'Email'],['C044',19300,'HIGH VALUE',10,9800,'Email + WhatsApp'],['C045',7400,'GROWTH',4,3600,'Email'],['C046',4900,'STANDARD',3,2400,'WhatsApp'],['C047',13800,'LOYAL',8,7000,'Email + WhatsApp'],['C048',6800,'GROWTH',4,3400,'Email'],['C049',5500,'STANDARD',3,2700,'WhatsApp'],['C050',59400,'HIGH VALUE',13,30200,'Email + WhatsApp']]
    return pd.DataFrame(rows,columns=['Customer','Customer Value','Segment','Purchases','Total Spend','Channel'])

def normalize(df):
    df=df.copy()
    aliases={'customer':'Customer','customer_id':'Customer','id':'Customer','customer_value':'Customer Value','value':'Customer Value','revenue':'Customer Value','segment':'Segment','purchases':'Purchases','purchase_count':'Purchases','total_spend':'Total Spend','spend':'Total Spend','channel':'Channel'}
    df=df.rename(columns={c:aliases.get(str(c).strip().lower(),c) for c in df.columns})
    if 'Customer' not in df: df['Customer']=[f'C{i:03d}' for i in range(1,len(df)+1)]
    if 'Customer Value' not in df: df['Customer Value']=0.0
    if 'Purchases' not in df: df['Purchases']=1
    if 'Total Spend' not in df: df['Total Spend']=df['Customer Value']*.5
    if 'Segment' not in df:
        q1,q2,q3=df['Customer Value'].quantile([.25,.5,.75]).values
        df['Segment']=df['Customer Value'].apply(lambda x:'HIGH VALUE' if x>=q3 else 'LOYAL' if x>=q2 else 'GROWTH' if x>=q1 else 'STANDARD')
    if 'Channel' not in df: df['Channel']=np.where(df['Purchases']>=8,'Email + WhatsApp','Email')
    for c in ['Customer Value','Purchases','Total Spend']: df[c]=pd.to_numeric(df[c],errors='coerce').fillna(0)
    df['Customer']=df['Customer'].astype(str); df['Segment']=df['Segment'].astype(str).str.upper().str.strip(); df['Channel']=df['Channel'].astype(str)
    df['Avg Order Value']=np.where(df['Purchases']>0,df['Total Spend']/df['Purchases'],0)
    df['Spend Ratio']=np.where(df['Customer Value']>0,df['Total Spend']/df['Customer Value'],0)
    return df

if 'dataset' not in st.session_state: st.session_state.dataset=demo_data()
customers=normalize(st.session_state.dataset)

st.markdown('''<style>
.stApp{background:linear-gradient(180deg,#060912,#080d18,#060a12)}
.block-container{max-width:1480px;padding:2rem 2.4rem 3rem}
.hero{padding:2.5rem;border-radius:28px;border:1px solid rgba(139,92,246,.35);background:linear-gradient(135deg,rgba(39,20,79,.92),rgba(10,18,34,.96));margin-bottom:1.5rem}.hero h1{font-size:clamp(2.4rem,5vw,4.5rem);margin:0;color:white}.hero p{color:#b4c0d2;max-width:800px;font-size:1rem;line-height:1.65}.badge{display:inline-block;padding:.45rem .7rem;border-radius:999px;background:rgba(52,211,153,.08);color:#6ee7b7;border:1px solid rgba(52,211,153,.25);font-weight:700}
</style>''',unsafe_allow_html=True)

st.sidebar.markdown('''<div style="padding:18px;border-radius:20px;background:linear-gradient(145deg,rgba(124,58,237,.18),rgba(7,15,29,.82));border:1px solid rgba(139,92,246,.3)"><div style="font-size:28px">🚀</div><h2 style="color:white;margin:5px 0">RevPilot AI</h2><p style="color:#91a1b8;margin:0">Revenue Intelligence OS</p><p style="color:#6ee7b7">● Internship portfolio demo</p><p style="color:#a9b7ca;font-size:12px">Built & Designed by <b style="color:white">Prajwal Y R</b><br>Creator & Developer • Razorpay Internship Portfolio Demo</p></div>''',unsafe_allow_html=True)
page=st.sidebar.radio('WORKSPACE',['🏠 Executive Dashboard','👥 Customer Intelligence','🎯 AI Target Customers','🔮 Campaign Prediction','📊 Revenue Analytics','⚙️ Data & Settings'])

if page=='🏠 Executive Dashboard':
    st.markdown('<div class="hero"><div style="color:#a78bfa;font-weight:800;letter-spacing:.18em">AI REVENUE INTELLIGENCE</div><h1>RevPilot AI 🚀</h1><p>Turn customer data into revenue opportunities using segmentation, priority scoring and campaign performance prediction.</p><span class="badge">● System ready</span></div>',unsafe_allow_html=True)
    a,b,c,d=st.columns(4); a.metric('Customers',f'{len(customers):,}'); b.metric('Customer Value',f'₹{customers["Customer Value"].sum():,.0f}'); c.metric('Avg Customer Value',f'₹{customers["Customer Value"].mean():,.0f}'); d.metric('High-Value Customers',int((customers.Segment=='HIGH VALUE').sum()))
    x,y=st.columns(2)
    with x: st.plotly_chart(px.bar(customers.groupby('Segment',as_index=False)['Customer Value'].sum(),x='Segment',y='Customer Value',title='Value by Customer Segment'),use_container_width=True)
    with y: st.plotly_chart(px.pie(customers.groupby('Channel',as_index=False)['Total Spend'].sum(),names='Channel',values='Total Spend',title='Spend by Campaign Channel'),use_container_width=True)
    st.subheader('Top Revenue Customers'); st.dataframe(customers.sort_values('Customer Value',ascending=False).head(10),use_container_width=True,hide_index=True)

elif page=='👥 Customer Intelligence':
    st.title('👥 Customer Intelligence'); st.caption('Explore customer value, purchase behaviour and segments.')
    options=sorted(customers.Segment.unique().tolist())
    selected=st.multiselect('Target segments',options=options,default=options)  # FIXED: defaults are valid options
    f=customers[customers.Segment.isin(selected)]; a,b,c=st.columns(3); a.metric('Customers',len(f)); b.metric('Total Value',f'₹{f["Customer Value"].sum():,.0f}'); c.metric('Total Spend',f'₹{f["Total Spend"].sum():,.0f}'); st.dataframe(f,use_container_width=True,hide_index=True)

elif page=='🎯 AI Target Customers':
    st.title('🎯 AI Target Customers'); st.caption('Prioritize customers using a transparent revenue opportunity score.')
    w=customers.copy(); v=w['Customer Value']/max(w['Customer Value'].max(),1); p=w['Purchases']/max(w['Purchases'].max(),1); s=w['Spend Ratio'].clip(0,1); bonus=w.Segment.map({'HIGH VALUE':1,'LOYAL':.85,'GROWTH':.65,'STANDARD':.4}).fillna(.4); w['Strategy Score']=(v*.45+p*.25+s*.1+bonus*.2)*100
    n=st.slider('Priority customers to show',5,len(w),min(10,len(w))); t=w.sort_values('Strategy Score',ascending=False).head(n); a,b,c,d=st.columns(4); a.metric('Targets',len(t)); b.metric('Target Value',f'₹{t["Customer Value"].sum():,.0f}'); c.metric('Avg Value',f'₹{t["Customer Value"].mean():,.0f}'); d.metric('Avg Purchases',f'{t.Purchases.mean():.1f}'); st.dataframe(t[['Customer','Segment','Customer Value','Purchases','Total Spend','Channel','Strategy Score']],use_container_width=True,hide_index=True); st.plotly_chart(px.bar(t.sort_values('Strategy Score'),x='Strategy Score',y='Customer',color='Segment',orientation='h',title='AI Priority Score'),use_container_width=True)

elif page=='🔮 Campaign Prediction':
    st.title('🔮 Campaign Performance Prediction'); st.caption('Estimate response and expected revenue from a selected campaign.')
    w=customers.copy(); w['Priority Score']=(w['Customer Value'].rank(pct=True)*.65+w['Purchases'].rank(pct=True)*.35)*100; n=st.slider('Priority customers to forecast',5,len(w),min(10,len(w))); t=w.sort_values('Priority Score',ascending=False).head(n).copy(); boost=st.slider('Campaign quality adjustment',0.0,1.0,.2,.05); revenue_rate=st.slider('Revenue realization rate',.05,1.,.4,.05); cost_rate=st.slider('Variable campaign cost rate',0.,.2,.03,.01)
    base=t['Priority Score']/100*.7+t['Purchases'].rank(pct=True)*.2+(t.Segment=='HIGH VALUE')*.1; t['Blended Response']=np.clip((base*100+boost*25)*.85+boost*15,0,100); t['Expected Revenue']=t['Customer Value']*t['Blended Response']/100*revenue_rate; t['Campaign Cost']=t['Expected Revenue']*cost_rate; t['Expected ROI']=np.where(t['Campaign Cost']>0,(t['Expected Revenue']-t['Campaign Cost'])/t['Campaign Cost'],0)
    a,b,c,d=st.columns(4); a.metric('Forecast Revenue',f'₹{t["Expected Revenue"].sum():,.0f}'); b.metric('Campaign Cost',f'₹{t["Campaign Cost"].sum():,.0f}'); c.metric('Avg Response',f'{t["Blended Response"].mean():.1f}%'); d.metric('Avg ROI',f'{t["Expected ROI"].mean():.1f}x'); st.dataframe(t[['Customer','Segment','Customer Value','Blended Response','Expected Revenue','Campaign Cost','Expected ROI']],use_container_width=True,hide_index=True)

elif page=='📊 Revenue Analytics':
    st.title('📊 Revenue Analytics'); metric=st.selectbox('Choose metric',['Customer Value','Total Spend','Purchases','Avg Order Value']); st.plotly_chart(px.histogram(customers,x=metric,color='Segment',marginal='box',title=f'{metric} Distribution'),use_container_width=True); st.plotly_chart(px.scatter(customers,x='Purchases',y='Customer Value',size='Total Spend',color='Segment',hover_name='Customer',title='Customer Value vs Purchases'),use_container_width=True)

else:
    st.title('⚙️ Data & Settings'); st.write('Upload a CSV to replace the demo dataset.'); uploaded=st.file_uploader('Upload customer CSV',type=['csv'])
    if uploaded is not None:
        try: st.session_state.dataset=pd.read_csv(uploaded); st.success('Dataset uploaded successfully.'); st.rerun()
        except Exception as e: st.error(f'Could not read CSV: {e}')
    if st.button('Restore demo dataset'): st.session_state.dataset=demo_data(); st.success('Demo dataset restored.'); st.rerun()
    st.dataframe(customers.head(20),use_container_width=True,hide_index=True)
