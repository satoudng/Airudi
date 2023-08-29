import pandas as pd
import streamlit as st
from azure.storage.blob import BlobServiceClient, ContainerClient
import io 

# définition des 4 paramètres nous permettant d'atteindre le compte et container de stockage (keys access et containers sur Azure) : 

storage_account_name="airudidatalake"
container_name="stage-aissatou"
storage_account_key="8fHYfL5HB9WTFx98kDnG+L6TvlNmp24rwOlLeRZQ9QwZl+0zsnqGe0WfL92UbsKEBokqDxCmU6T++AStrBts0g=="
connection_string="DefaultEndpointsProtocol=https;AccountName=airudidatalake;AccountKey=8fHYfL5HB9WTFx98kDnG+L6TvlNmp24rwOlLeRZQ9QwZl+0zsnqGe0WfL92UbsKEBokqDxCmU6T++AStrBts0g==;EndpointSuffix=core.windows.net"

# création d'une fonction vérifiant l'existance d'un blob dans le storage 
def existence_blob(connection_string, container_name,file_name):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(file_name)
    blob_exists = blob_client.exists() # existance du blob ou non 
    return blob_exists # retourne un bool (T ou F)
 
# création d'une fonction nous permettant d'upload nos blobs dans un répertoire :
def upload_blob (fichier,file_name,repertoire): # avec file_path le chemin du fichier et file-name le nom qu'on lui donne dans le blobstorage
    blob_service_client = BlobServiceClient.from_connection_string(connection_string) #chaine de connection permet d'accéder au storage
    blob_client = blob_service_client.get_blob_client(container=container_name,blob=repertoire+"/"+file_name) #permet de manipuler les blobs
    #with open (file_path,"rb") as data : #rb pour mode de lecture binaire, définition du contenu du blob
    with st.spinner("Téléchargement en cours"): 
        blob_client.upload_blob(fichier) #(data) #stockage du blob #.getvalue()) 
    return existence_blob(connection_string, container_name, file_name)

# téléchargement de blobs : 
def telecharger_blob(connection_string, container_name, file_name, destination_path):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(file_name)
    if not blob_client.exists():
        st.warning(f"Le fichier '{file_name}' n'existe pas.")
        return
    with open(destination_path, "wb") as new_file: # 'w' pour mode d'écriture- Ouvre le fichier en écriture. Si le fichier existe déjà, son contenu sera écrasé. Si le fichier n'existe pas, il sera créé.
        blob_data = blob_client.download_blob()
        blob_data.readinto(new_file)
    st.success(f"Le fichier '{file_name}' a été téléchargé vers '{destination_path}'.")