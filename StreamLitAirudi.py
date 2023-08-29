import streamlit as st
import pandas as pd
from azure.storage.blob import BlobServiceClient, ContainerClient
import FonctionsEDA2 
import FonctionsBlob2 



storage_account_name="airudidatalake"
container_name="stage-aissatou"
storage_account_key="8fHYfL5HB9WTFx98kDnG+L6TvlNmp24rwOlLeRZQ9QwZl+0zsnqGe0WfL92UbsKEBokqDxCmU6T++AStrBts0g=="
connection_string="DefaultEndpointsProtocol=https;AccountName=airudidatalake;AccountKey=8fHYfL5HB9WTFx98kDnG+L6TvlNmp24rwOlLeRZQ9QwZl+0zsnqGe0WfL92UbsKEBokqDxCmU6T++AStrBts0g==;EndpointSuffix=core.windows.net"

st.set_page_config(page_title="Airudi - Ingestion des données",page_icon=":chart_with_upwards_trend:",layout="wide",initial_sidebar_state="collapsed")

st.sidebar.title("AIRUDI")
selected_category = st.sidebar.selectbox("Catégories", ["Accueil", "Dépôt de données"])
st.title("AIRUDI")

if selected_category == "Accueil":
    st.header("Bienvenue !")
    st.write("Sélectionnez une catégorie dans la barre latérale gauche pour commencer.")

if selected_category== "Dépôt de données":
    repertoire1 = st.text_input("Entrez le nom de votre entreprise : ")
    repertoire = repertoire1.upper()
    if repertoire is None :
        st.header("Dépôt de données") 
        st.warning("Veuillez entrer le nom de votre entreprise, avant de pouvoir télécharger vos fichiers sur la plateforme.")
    else :
        st.header("Dépôt de données")

        fichiers = st.file_uploader("Veuillez déposer ci-dessous votre ou vos fichier(s) : ",accept_multiple_files=True)
        for fichier in fichiers :
            st.header(f"Fichier {fichier.name} :")

            if fichier is not None:
                if fichier.name.endswith(('.csv', '.txt')):
                    st.success('Le fichier a bien été téléchargé.')

                    st.caption("Attention, si vous déposez un fichier de type CSV ou TXT, veuillez précisez le séparateur utilisé :")
                    separateur = st.text_input('Séparateur')
                    if not separateur:
                        st.caption("Veuillez indiquer le séparateur du fichier.")
                    else : 
                        st.caption(f"Le séparateur du fichier est : {separateur}")

                    if st.button(f"Déposer le fichier - {fichier.name}"):
                        FonctionsEDA2.EDA_csv_excel(fichier,separateur,repertoire)
                        st.subheader("Transfert vers la base de données")
                        if FonctionsBlob2.existence_blob(connection_string, container_name,repertoire+"/"+fichier.name) is True:
                            st.warning("Ce fichier existe déjà dans notre base de données.")
                        else:
                            FonctionsBlob2.upload_blob(fichier.getvalue(), fichier.name,repertoire)
                            if FonctionsBlob2.existence_blob(connection_string, container_name,repertoire+"/"+fichier.name) is True:
                                st.success(f"Le fichier '{fichier.name}' a bien été téléchargé dans votre dossier client sous le nom '{repertoire}/{fichier.name}'.")
                            else:
                                st.error(f"Erreur lors du téléchargement, veuillez réessayer.")

                elif fichier.name.endswith(('.docx','.doc')):
                    if st.button(f"Déposer le fichier - {fichier.name}"):
                        FonctionsEDA2.EDA_word(fichier)
                        st.subheader("Transfert vers la base de données")
                        if FonctionsBlob2.existence_blob(connection_string, container_name,repertoire+"/"+fichier.name) is True:
                            st.warning("Ce fichier existe déjà dans notre base de données.")
                        else:
                            FonctionsBlob2.upload_blob(fichier.getvalue(), fichier.name,repertoire)
                            if FonctionsBlob2.existence_blob(connection_string, container_name,repertoire+"/"+fichier.name) is True:
                                st.success(f"Le fichier '{fichier.name}' a bien été téléchargé dans votre dossier client sous le nom '{repertoire}/{fichier.name}'.")
                            else:
                                st.error(f"Erreur lors du téléchargement, veuillez réessayer.")

                elif fichier.name.endswith('.pdf'):
                    if st.button(f"Déposer le fichier - {fichier.name}"):            
                        FonctionsEDA2.EDA_pdf(fichier)
                        st.subheader("Transfert vers la base de données")
                        if FonctionsBlob2.existence_blob(connection_string, container_name,repertoire+"/"+fichier.name) is True:
                            st.warning("Ce fichier existe déjà dans notre base de données.")
                        else:
                            FonctionsBlob2.upload_blob(fichier.getvalue(), fichier.name,repertoire)
                            if FonctionsBlob2.existence_blob(connection_string, container_name, repertoire+"/"+fichier.name) is True:
                                st.success(f"Le fichier '{fichier.name}' a bien été téléchargé dans votre dossier client sous le nom '{repertoire}/{fichier.name}'.")
                            else:
                                st.error(f"Erreur lors du téléchargement, veuillez réessayer.")

                elif fichier.name.endswith(('.zip','.rar')):
                    if st.button(f"Déposer le fichier - {fichier.name}"): 
                        FonctionsEDA2.EDA_ziprar(fichier)
                        st.subheader("Transfert vers la base de données")
                        if FonctionsBlob2.existence_blob(connection_string, container_name, repertoire+"/"+fichier.name) is True:
                            st.warning("Ce fichier existe déjà dans notre base de données.")
                        else:
                            FonctionsBlob2.upload_blob(fichier.getvalue(), fichier.name,repertoire)
                            if FonctionsBlob2.existence_blob(connection_string, container_name, repertoire+"/"+fichier.name) is True:
                                st.success(f"Le fichier '{fichier.name}' a bien été téléchargé dans votre dossier client sous le nom '{repertoire}/{fichier.name}'.")
                            else:
                                st.error(f"Erreur lors du téléchargement, veuillez réessayer.")

                elif fichier.name.endswith(('.xls','.xlsx')):
                    if st.button(f"Déposer le fichier - {fichier.name}"):
                        FonctionsEDA2.EDA_excel_excel(fichier,repertoire)
                        st.subheader("Transfert vers la base de données")
                        if FonctionsBlob2.existence_blob(connection_string, container_name, repertoire+"/"+fichier.name) is True:
                            st.warning("Ce fichier existe déjà dans notre base de données.")
                        else:
                            FonctionsBlob2.upload_blob(fichier.getvalue(), fichier.name,repertoire)
                            if FonctionsBlob2.existence_blob(connection_string, container_name, repertoire+"/"+fichier.name) is True:
                                st.success(f"Le blob '{fichier.name}' a bien été téléchargé dans votre dossier client sous le nom '{repertoire}/{fichier.name}'.")
                            else:
                                st.error(f"Erreur lors du téléchargement, veuillez réessayer.")
      
            else:
                st.error("Il y a eu une erreur lors du téléchargement, veuillez vérifier que le (les) fichier(s) a (ont) été correctement déposé(s).")
                st.stop()
