import json, os
import boto3, pandas as pd, streamlit as st
st.set_page_config(page_title='FleetPulse • ISSE-05',layout='wide')
st.title('FleetPulse — Suivi de flotte')
st.caption('Projet ISSE-05 • Données GPS simulées • Zone autorisée : Casablanca')
s3=boto3.client('s3',endpoint_url='http://minio:9000',aws_access_key_id=os.getenv('MINIO_ROOT_USER','fleetadmin'),aws_secret_access_key=os.getenv('MINIO_ROOT_PASSWORD','fleetpassword123'))
def read(name):
    return json.loads(s3.get_object(Bucket='fleet',Key=f'exports/{name}.json')['Body'].read())
@st.fragment(run_every='30s')
def show():
    try:
        status=read('status'); daily=pd.DataFrame(read('daily')); latest=pd.DataFrame(read('latest'))
        incidents=pd.DataFrame(read('incidents')); zones=pd.DataFrame(read('zones'))
    except s3.exceptions.ClientError:
        st.info('En attente du premier traitement Spark. Premier rapport après environ 2 minutes.'); return
    st.caption(f"Dernier traitement : {status['updated_at']} • Actualisation Spark toutes les 2 minutes")
    a,b,c=st.columns(3)
    a.metric('Véhicules',len(latest)); b.metric('Distance échantillonnée (km)',round(daily.distance_km.sum(),2)); c.metric('Mesures en excès de vitesse',int(daily.speeding_samples.sum()))
    st.map(latest,latitude='latitude',longitude='longitude')
    st.subheader('Indicateurs quotidiens'); st.dataframe(daily,hide_index=True)
    st.subheader('Derniers incidents (200 mesures maximum)'); st.dataframe(incidents,hide_index=True)
    st.subheader("Centres des zones d’arrêt — KMeans")
    if len(zones): st.map(zones,latitude='latitude',longitude='longitude'); st.dataframe(zones)
    else: st.info("Pas encore assez de positions distinctes à l’arrêt (vitesse ≤ 5 km/h).")
    st.download_button('Télécharger le rapport CSV',daily.to_csv(index=False),'rapport_conduite.csv','text/csv')
show()
