import FonctionsBlob2 
import pandas as pd
import streamlit as st 
import openpyxl
import docx
import os 
import pdfplumber
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from tabulate import tabulate
import xlsxwriter


def EDA_excel_excel(fichier, repertoire):
    fichier.seek(0, os.SEEK_END)
    taille = fichier.tell()
    taille_ko = taille / 1024
    st.subheader("Taille du fichier :")
    st.write(f"{taille_ko:.2f} ko")  # en kilooctets
    if taille == 0:
        return st.error("Le fichier déposé est vide.")
    try:
        df = pd.read_excel(fichier, engine='openpyxl')
    except Exception as erreur:
        return st.error(str(erreur))
    if df.empty:
        return st.warning("Le fichier est vide, il n'est pas exploitable.")
    
    excel_filename = f"{fichier.name} - EDA.xlsx"
    
    workbook = xlsxwriter.Workbook(excel_filename)
    num_format = workbook.add_format({'num_format': '0.00'}) 
    
    worksheet = workbook.add_worksheet("EDA")
    worksheet.set_column(0, 1, 12)
    for col_num in range(2, df.shape[1] + 2):
        worksheet.set_column(col_num, col_num, 12)
    
    row_offset = 1
    
    # HEAD
    worksheet.write(row_offset, 0, "APERÇU", workbook.add_format({'color': 'blue', 'bold': True}))
    worksheet.write_row(row_offset + 1, 1, df.columns)
    for row_num, (index, row_data) in enumerate(df.head().iterrows()):
        worksheet.write(row_offset + row_num + 2, 0, index)
        row_values = [value if pd.notna(value) else "X" for value in row_data]
        worksheet.write_row(row_offset + row_num + 2, 1, row_values, num_format)
    
    row_offset += len(df.head()) + 4
    
    # DESCRIBE
    worksheet.write(row_offset, 0, "STATS", workbook.add_format({'color': 'blue', 'bold': True}))
    worksheet.write_row(row_offset + 1, 1, df.describe().columns,num_format)
    
    for row_num, (index, row_data) in enumerate(df.describe().iterrows()):
        worksheet.write(row_offset + row_num + 2, 0, index, num_format)
        worksheet.write_row(row_offset + row_num + 2, 1, row_data, num_format)
    
    row_offset += len(df.describe()) + 4
    
    # ISNA
    worksheet.write(row_offset, 0, "NaN", workbook.add_format({'color': 'blue', 'bold': True}))
    worksheet.write_row(row_offset + 1, 1, df.isna().columns)
    
    for row_num, (index, row_data) in enumerate(df.isna().iterrows()):
        worksheet.write(row_offset + row_num + 2, 0, index)
        worksheet.write_row(row_offset + row_num + 2, 1, row_data)
    
    row_offset += len(df.isna()) + 4
    
    # INFOS
    worksheet.write(row_offset, 0, "INFOS", workbook.add_format({'color': 'blue', 'bold': True}))
    worksheet.write(row_offset + 1, 0, "Shape")
    worksheet.write(row_offset + 1, 1, str(df.shape))
    worksheet.write(row_offset + 2, 0, "Size")
    worksheet.write(row_offset + 2, 1, str(df.size))
    worksheet.write(row_offset + 3, 0, "Taux NaN")
    worksheet.write(row_offset + 3, 1, str(df.isna().sum().sum() / df.size))
    if df.isna().sum().sum() / df.size >= 0.7:
        worksheet.write(row_offset + 4, 0, "Remarque:")
        worksheet.write(row_offset + 4, 1, "Le fichier contient 70% ou plus de valeurs manquantes. Faites attention avant de le manipuler.")
    
    workbook.close()
    
    st.subheader("Analyse des données : ")
    st.caption(f"Les résultats de l'EDA ont été enregistrés dans le fichier Excel : '{excel_filename}' et téléchargés sur notre base de données")
    FonctionsBlob2.upload_blob(open(excel_filename, 'rb'), excel_filename, repertoire)

def EDA_csv_excel(fichier, separateur,repertoire): #dans l'interface l'utilisateur précisera le séparateur
    if not fichier.name.endswith('.csv') or not fichier.name.endswith('.txt'): 
        return st.error("Une erreur s'est produite : Le fichier doit être un fichier CSV (.csv ou .txt)")  
    fichier.seek(0, os.SEEK_END)
    taille = fichier.tell()
    taille_ko = taille/1024
    st.subheader("Taille du fichier :")
    st.write(f"{taille_ko: .2f} ko ") # en kilooctets
    if taille == 0:
        return st.error("Le fichier déposé est vide.")   
    df = pd.read_csv(fichier,separateur) # conversion du csv en df
    if df.empty: # cas où df vide
        return st.warning("Le fichier est vide, il n'est pas exploitable.")
    
    excel_filename = f"{fichier.name} - EDA.xlsx"
    
    workbook = xlsxwriter.Workbook(excel_filename)
    num_format = workbook.add_format({'num_format': '0.00'}) 
    
    worksheet = workbook.add_worksheet("EDA")
    worksheet.set_column(0, 1, 12)
    for col_num in range(2, df.shape[1] + 2):
        worksheet.set_column(col_num, col_num, 12)
    
    row_offset = 1
    
    # HEAD
    worksheet.write(row_offset, 0, "APERÇU", workbook.add_format({'color': 'blue', 'bold': True}))
    worksheet.write_row(row_offset + 1, 1, df.columns)
    for row_num, (index, row_data) in enumerate(df.head().iterrows()):
        worksheet.write(row_offset + row_num + 2, 0, index)
        row_values = [value if pd.notna(value) else "X" for value in row_data]
        worksheet.write_row(row_offset + row_num + 2, 1, row_values, num_format)
    
    row_offset += len(df.head()) + 4
    
    # DESCRIBE
    worksheet.write(row_offset, 0, "STATS", workbook.add_format({'color': 'blue', 'bold': True}))
    worksheet.write_row(row_offset + 1, 1, df.describe().columns,num_format)
    
    for row_num, (index, row_data) in enumerate(df.describe().iterrows()):
        worksheet.write(row_offset + row_num + 2, 0, index, num_format)
        worksheet.write_row(row_offset + row_num + 2, 1, row_data, num_format)
    
    row_offset += len(df.describe()) + 4
    
    # ISNA
    worksheet.write(row_offset, 0, "NaN", workbook.add_format({'color': 'blue', 'bold': True}))
    worksheet.write_row(row_offset + 1, 1, df.isna().columns)
    
    for row_num, (index, row_data) in enumerate(df.isna().iterrows()):
        worksheet.write(row_offset + row_num + 2, 0, index)
        worksheet.write_row(row_offset + row_num + 2, 1, row_data)
    
    row_offset += len(df.isna()) + 4
    
    # INFOS
    worksheet.write(row_offset, 0, "INFOS", workbook.add_format({'color': 'blue', 'bold': True}))
    worksheet.write(row_offset + 1, 0, "Shape")
    worksheet.write(row_offset + 1, 1, str(df.shape))
    worksheet.write(row_offset + 2, 0, "Size")
    worksheet.write(row_offset + 2, 1, str(df.size))
    worksheet.write(row_offset + 3, 0, "Taux NaN")
    worksheet.write(row_offset + 3, 1, str(df.isna().sum().sum() / df.size))
    if df.isna().sum().sum() / df.size >= 0.7:
        worksheet.write(row_offset + 4, 0, "Remarque:")
        worksheet.write(row_offset + 4, 1, "Le fichier contient 70% ou plus de valeurs manquantes. Faites attention avant de le manipuler.")
    
    workbook.close()
    
    st.subheader("Analyse des données : ")
    st.caption(f"Les résultats de l'EDA ont été enregistrés dans le fichier Excel : '{excel_filename}' et téléchargés sur notre base de données.")
    FonctionsBlob2.upload_blob(open(excel_filename, 'rb'), excel_filename, repertoire)

def EDA_word(fichier):
    if not fichier.name.endswith(('.docx','.doc')):
        return st.error("Une erreur s'est produite : Le fichier doit être un fichier Word (.docx ou .doc)")
    document = docx.Document(fichier)
    fichier.seek(0, os.SEEK_END)
    taille = fichier.tell()
    taille_ko = taille/1024
    st.subheader("Taille du fichier :")
    st.write(f"{taille_ko: .2f} ko ") # en kilooctets
    if taille == 0:
        return st.error("Le fichier déposé est vide.")
    contenu = []
    for paragraph in document.paragraphs:
        contenu.append(paragraph.text)
    if not contenu : 
        return st.error("Le fichier déposé n'a pas de contenu.")
    else:
        st.subheader("Apercu du contenu:")
        with st.expander("Afficher le contenu du document"):
            st.write('\n'.join(contenu))        

def EDA_pdf(fichier):
    if not fichier.name.endswith('.pdf'):
        return st.error("Une erreur s'est produite : Le fichier doit être un fichier PDF (.pdf)")  
    fichier.seek(0, os.SEEK_END)
    taille = fichier.tell()
    taille_ko = taille/1024
    st.subheader("Taille du fichier :")
    st.write(f"{taille_ko: .2f} ko ") # en kilooctets
    if taille == 0:
        return st.error("Le fichier déposé est vide.")
    contenu=[]
    with pdfplumber.open(fichier) as pdf:
        #for page in pdf.pages:
        première_page= pdf.pages[0] #afficher la première page
        contenu.append(première_page.extract_text()) 
    if not contenu : 
        return st.error("Le fichier déposé n'a pas de contenu.")
    else:
        st.subheader("Apercu du contenu:")
        with st.expander("Afficher le contenu du document"):
            st.write((contenu[0]))  

def EDA_ziprar(fichier):
    if not fichier.name.endswith(('.zip', '.rar')):
        return st.error("Une erreur s'est produite : Le fichier doit être un fichier ZIP (.zip) ou RAR (.rar)")
    fichier.seek(0, os.SEEK_END)
    taille = fichier.tell()
    taille_ko = taille/1024
    st.subheader("Taille du fichier :")
    st.write(f"{taille_ko: .2f} ko") # en kilooctets
    if taille == 0:
        return st.error("Le fichier déposé est vide.")

# EDA sur un pdf pas esthétique 

def create_pdf(filename, titre, contenu):
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(300, 750, titre)
    text_object = c.beginText(72, 700)
    text_object.setFont("Helvetica", 12)
    text_object.textLines(contenu)
    c.drawText(text_object)
    c.save()

def EDA_excel_pdf(fichier,repertoire):
    fichier.seek(0, os.SEEK_END)
    taille = fichier.tell()
    taille_ko = taille/1024
    st.subheader("Taille du fichier :")
    st.write(f"{taille_ko: .2f} ko") # en kilooctets
    if taille == 0:
        return st.error("Le fichier déposé est vide.")    
    try:
        df = pd.read_excel(fichier, engine='openpyxl')
    except Exception as erreur:
        return st.error(str(erreur))
    if df.empty:
        return st.warning("Le fichier est vide, il n'est pas exploitable.")  
    
    pdf_title = f"Fiche notice de '{fichier.name}'" 
    pdf_filename = f"{fichier.name} - Fiche notice.pdf"

    df_head = tabulate(df.head(), headers="keys", tablefmt='simple_outline', numalign='center', showindex=False, colalign=["center",], floatfmt=".2f")
    df_describe = tabulate(df.describe(), headers='keys', tablefmt='simple_outline', numalign='center', showindex=False, colalign=["center",], floatfmt=".2f")
    df_isna = tabulate(df.isna(), headers='keys',tablefmt='simple_outline', numalign='center',showindex=False, colalign=["center",], floatfmt=".2f")

    pdf_content = f"""
    Aperçu des premières lignes:\n 
    {df_head}\n
    Statistiques descriptives:\n 
    {df_describe}\n
    Valeurs manquantes:\n 
    {df_isna}\n
    Taille du df:
    {df.shape}\n
    Nombre d'enregistrements:
    {df.size}\n
    Taux de NaN :
    {df.isna().sum().sum() / df.size}
    """
    if (df.isna().sum().sum() / df.size) >= 0.7:
        pdf_content += "Le fichier contient 70% ou plus de valeurs manquantes. Faites attention avant de le manipuler."
    
    create_pdf(pdf_filename, pdf_title, pdf_content)
    st.subheader("EDA : ")
    st.caption(f"Les résultats de l'EDA ont été enregistrés et uploadés dans le document PDF : {pdf_filename}")
    FonctionsBlob2.upload_blob(open(pdf_filename, 'rb'), pdf_filename,repertoire)

def EDA_csv_pdf(fichier, separateur,repertoire): #dans l'interface l'utilisateur précisera le séparateur
    if not fichier.name.endswith('.csv') or not fichier.name.endswith('.txt'): 
        return st.error("Une erreur s'est produite : Le fichier doit être un fichier CSV (.csv ou .txt)")  
    fichier.seek(0, os.SEEK_END)
    taille = fichier.tell()
    taille_ko = taille/1024
    st.subheader("Taille du fichier :")
    st.write(f"{taille_ko: .2f} ko ") # en kilooctets
    if taille == 0:
        return st.error("Le fichier déposé est vide.")   
    df = pd.read_csv(fichier,separateur) # conversion du csv en df
    if df.empty: # cas où df vide
        return st.warning("Le fichier est vide, il n'est pas exploitable.")
    
    pdf_title = f"Fiche notice de '{fichier.name}'" 
    pdf_filename = f"{fichier.name} - Fiche notice.pdf"

    df_head = tabulate(df.head(), headers="keys", tablefmt='simple', numalign='center', showindex=False, colalign=["center",], floatfmt=".2f")
    df_describe = tabulate(df.describe(), headers='keys', tablefmt='simple', numalign='center', showindex=False, colalign=["center"], floatfmt=".2f")
    df_isna = tabulate(df.isna(), headers='keys',tablefmt='simple', numalign='center',showindex=False, colalign=["center",], floatfmt=".2f")
#*len(df.columns)
    pdf_content = f"""
    Aperçu des premières lignes:\n 
    {df_head}\n
    Statistiques descriptives:\n 
    {df_describe}\n
    Valeurs manquantes:\n 
    {df_isna}\n
    Taille du df:
    {df.shape}\n
    Nombre d'enregistrements:
    {df.size}\n
    Taux de NaN :
    {df.isna().sum().sum() / df.size}
    """
    if (df.isna().sum().sum() / df.size) >= 0.7:
        pdf_content += "Le fichier contient 70% ou plus de valeurs manquantes. Faites attention avant de le manipuler."
    
    create_pdf(pdf_filename, pdf_title, pdf_content)

    st.subheader("EDA : ")
    st.caption(f"Les résultats de l'EDA ont été enregistrés et uploadés dans le document PDF : {pdf_filename}")
    FonctionsBlob2.upload_blob(open(pdf_filename, 'rb'), pdf_filename,repertoire)