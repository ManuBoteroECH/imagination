# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 13:52:39 2023

IMAGINATION 2.0
@author: abisambra.d
"""

# Proyecto Imagination 2.0 P&G Colombia

#Importamos Paquetes
import numpy as np
import sys
import pandas as pd

from tkinter import *
from PIL import Image,ImageTk, ImageDraw, ImageFont
from PIL import ImageDraw, ImageFont
import tkinter as tk
from PIL import ImageGrab
from tkinter import filedialog

import io
import os
import subprocess

import streamlit
import streamlit as st
from streamlit.web import cli as stcli

from zipfile import ZipFile
from io import BytesIO
import base64

#Streamlit________________________________________________________________________________________

#Título Webpage
st.title("Imagination", anchor=None)

#Selecciono marca
opmarca = st.selectbox('Select Brand',('Herbal Essences' ,'Pantene' ,'HeadShoulders' ,'Ariel' ,'Rindex2en1' ,'Rindex10' ,'OldSpice' ,'GilletteDeos' ,'Gillette' ,'Venus' ,'Cebion' ,'Vick' ,'Neurobion' ,'OralB' ,'Pro', 'Secret', 'Multi' ))
st.write('You selected:', opmarca)

#Dimensiones
opancho=st.number_input("ancho en pixeles", step=1)
opalto=st.number_input("alto en pixeles", step=1)

#Selecciono si voy a subir un background
opback = st.selectbox('Select Background OPTIONAL',(TRUE ,FALSE))
st.write('You selected:', opback)

if opback==True:
    opbackgroundpic = st.file_uploader("Upload background image in png format, if not, the image will have the brand standard colors ", type = ['png'])
    opbackgroundpic = Image.open(opbackgroundpic)

#Modalidad de diseño dark/light
optone = st.selectbox('Select Design Tone (Dark/Light)',('Dark' ,'Light'))
st.write('You selected:', optone)

#Titlo, claim

optitle= st.text_input("Banner tittle", "tittle")
opclaim= st.text_input("Banner claim", "claim de marca")


#Call to action
opcta = st.selectbox('You need call to action?',(TRUE ,FALSE))
st.write('You selected:', opcta)

if opcta==True:
    opctatext= st.text_input("Banner cta", "claim cta")


#Agrego disclaimer
opdisc= st.text_input("Banner disclaimer", "*Descuento sólo para productos seleccionados")

#Productos
opprod1=st.number_input("EAN13 producto 1", step=1)
opprod2=st.number_input("EAN13 producto 2", step=1)
opprod3=st.number_input("EAN13 producto 3", step=1)
opprod4=st.number_input("EAN13 producto 4", step=1)

#Escalar producto
opscale=st.number_input("% product picture scaling", value=100, step=1,min_value=1, max_value=150)
opscale= opscale/100

#Agrego el Boton de generar    
resultado = st.button("Generar") #Devuleve True cuando el usuario hace click
zipObj = ZipFile("ImaginationResult.zip", "w")

if resultado == True:
    #Inputs____________________________________________________________________________________________

    #Inputfile
    #inputfile = pd.read_excel("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/InputFile.xlsx")
    inputfilefondos = pd.read_excel("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Background/RGB BACKGROUNDS.xlsx", header=0, index_col=0)
    inputfileletras = pd.read_excel("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Background/RGB TYPEFACES.xlsx", header=0, index_col=0)

    #Marca que se vaa generar
    #marca = inputfile.iloc[0,0]
    marca = opmarca

    #Dimensiones
    #ancho = inputfile.iloc[0,1]
    #alto = inputfile.iloc[0,2]
    #backgroundpic = inputfile.iloc[0,3]
    #backgroundtipo = inputfile.iloc[0,4]

    ancho = opancho
    alto = opalto
    backgroundpic = opback
    backgroundtipo = optone

    #Colores

    if backgroundtipo=="Dark":
        start_color= (inputfilefondos.loc[marca, inputfilefondos.columns[0]], inputfilefondos.loc[marca, inputfilefondos.columns[1]], inputfilefondos.loc[marca, inputfilefondos.columns[2]],255)
        end_color= (inputfilefondos.loc[marca, inputfilefondos.columns[3]], inputfilefondos.loc[marca, inputfilefondos.columns[4]], inputfilefondos.loc[marca, inputfilefondos.columns[5]],255)
        text_color = (inputfileletras.loc[marca, inputfileletras.columns[0]], inputfileletras.loc[marca, inputfileletras.columns[1]], inputfileletras.loc[marca, inputfileletras.columns[2]], 255)  # RGBA: White text (fully opaque)
        text_box_color = text_color
        buttonletter_color = (inputfileletras.loc[marca, inputfileletras.columns[3]], inputfileletras.loc[marca, inputfileletras.columns[4]], inputfileletras.loc[marca, inputfileletras.columns[5]], 255)
        transparent_color = (0, 0, 0, 0)

    if backgroundtipo=="Light":
        start_color= (inputfilefondos.loc[marca, inputfilefondos.columns[6]], inputfilefondos.loc[marca, inputfilefondos.columns[7]], inputfilefondos.loc[marca, inputfilefondos.columns[8]],255)
        end_color= (inputfilefondos.loc[marca, inputfilefondos.columns[9]], inputfilefondos.loc[marca, inputfilefondos.columns[10]], inputfilefondos.loc[marca, inputfilefondos.columns[11]],255)
        text_color = (inputfileletras.loc[marca, inputfileletras.columns[6]], inputfileletras.loc[marca, inputfileletras.columns[7]], inputfileletras.loc[marca, inputfileletras.columns[8]], 255)  # RGBA: White text (fully opaque)
        text_box_color = text_color
        buttonletter_color = (inputfileletras.loc[marca, inputfileletras.columns[9]], inputfileletras.loc[marca, inputfileletras.columns[10]], inputfileletras.loc[marca, inputfileletras.columns[11]], 255)
        transparent_color = (0, 0, 0, 0)


    font_title = ImageFont.truetype("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Font/" + marca +" Tittle.otf", int(30/400*min(ancho, alto)))
    font_claim = ImageFont.truetype("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Font/"+ marca +" Claim.otf", int(20/400*min(ancho, alto)))
    font_disclaimer = ImageFont.truetype("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Font/"+ marca +" Disclaimer.otf", int(10/400*min(ancho, alto)))



    callToAction = opcta

    #Texto a incluir (OJO con la longitud)

    img_title = Image.new("RGBA", (0, 0), transparent_color)
    draw = ImageDraw.Draw(img_title)

    titulo = optitle

    titulo_ancho, titulo_alto = draw.textsize(titulo, font=font_title)


    claim = opclaim
    claim_ancho, claim_alto = draw.textsize(claim, font=font_claim)


    cta = opctatext
    cta_ancho, cta_alto = draw.textsize(cta, font=font_claim)


    disclaimer = opdisc
    disc_ancho, disc_alto = draw.textsize(disclaimer, font=font_disclaimer)

    #Productos (Hasta 4)
    productos = 4


    producto4 = opprod4
    if pd.isna(producto4):
        productos =3
    if int(producto4)==0:
        productos =3

    producto3 = opprod3
    if pd.isna(producto3):
        productos = 2

    if int(producto3)==0:
        productos = 2

    producto2 = opprod2
    if pd.isna(producto2):
        productos =1
    
    if int(producto2)==0:
        productos =1


    producto1 = opprod1
    if pd.isna(producto1):
        productos = 0

    if int(producto1)==0:
        productos = 0
    

    #Carpeta Output____________________________________________________________________________________________

    output_folder = 'C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Output'



    # Funciones _____________________________________________________________________________________

    # Función para identificar primer pixel no transparente:
    def find_first_non_transparent_pixel(image):
        # Open the image
        #image = Image.open(image)
        #image = image.convert("RGBA")  # Ensure image is in RGBA mode
        
        width, height = image.size
        
        for x in range(width):
            for y in range(height):
                r, g, b, a = image.getpixel((x, y))
                if a != 0:  # Check if the pixel is not transparent
                    return x, y  # Return the coordinates of the first non-transparent pixel

        return None 

    # Función para identificar último pixel no transparente:
    def find_last_non_transparent_pixel(image):
        # Open the image
        #image = Image.open(image)
        #image = image.convert("RGBA")  # Ensure image is in RGBA mode
        
        width, height = image.size
        
        for x in range(width):
            for y in range(height):
                xfin= width-x-1
                r, g, b, a = image.getpixel((xfin, y))
                if a != 0:  # Check if the pixel is not transparent
                    return xfin, y  # Return the coordinates of the first non-transparent pixel

        return None

    # Función para identificar el piso de cada producto:
    def find_floor(image):

        width, height = image.size
        
        for y in range(height):
            for x in range(width):
                yfloor = height-y-1
                r, g, b, a = image.getpixel((x, yfloor ))
                if a != 0:  # Check if the pixel is not transparent
                    return y  # Return the coordinates of the first non-transparent pixel

        return None


    #Se identifica el tipo de imagen que se quiere generar

    ratiodim = ancho / alto
    tipo = ""

    if ratiodim >= 1.2:
        tipo = "H"

    elif ratiodim <= 0.8:
        tipo = "V"
        
    else: tipo = "C"


    #Inicia proceso de generación de imágenes______________________________________________________________________

    #Construir imagen tipo cuadrado:
    if tipo == "C":
        
        

        img_back = Image.new("RGBA", (ancho, alto), transparent_color)
        draw = ImageDraw.Draw(img_back)

        # Create a horizontal gradient from left to right
        for x in range(ancho):
            # Calculate the color at this position based on interpolation
            r = int(start_color[0] + (end_color[0] - start_color[0]) * (x / ancho))
            g = int(start_color[1] + (end_color[1] - start_color[1]) * (x / ancho))
            b = int(start_color[2] + (end_color[2] - start_color[2]) * (x / ancho))
            a = int(start_color[3] + (end_color[3] - start_color[3]) * (x / ancho))
            
            # Set the pixel color
            draw.line([(x, 0), (x, alto)], fill=(r, g, b, a))

        #Agrego Background (si hay)
        
        if backgroundpic == True:
            img_backg = Image.new("RGBA", (ancho, alto), transparent_color)
            #im_backg1 = Image.open("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Background/Herbal Essences.png")
            im_backg1= opbackgroundpic
            
            #im_backg2 = im_backg1.resize((int(ancho),int(alto)))
            im_backg2 = im_backg1.crop((0,0, int(ancho), int(alto)))
            
            
            img_backg.paste(im_backg2, (0, 0))
            
            composite_image = Image.alpha_composite(img_back, im_backg2)
        
        
        
        #Agrego las imágenes de producto
        



        #Productos
        
        multiplicador1 = 1*opscale
        multiplicador2= 0.78*opscale
        multiplicador3= 0.7*opscale
        multiplicador4 = 0.6*opscale
        locatorscale= (opscale-1)*0.5
        finalpegado = 0
        coordpegar	= 0
        padding = 20
        current_x = 0
        
        if productos ==1:
            img_prod10 = Image.new("RGBA", (ancho, alto), transparent_color)
            im_prod11 = Image.open("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Productos/"+ str(int(producto1)) +".png")
            im_prod12 = im_prod11.resize((int(min(ancho, alto)*0.7*multiplicador1),int(min(ancho,alto)*0.7*multiplicador1)))
            img_prod10.paste(im_prod12, (int(ancho*0.35-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador1))), int(alto*0.27-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador1)))))
        
        if productos ==2:
            img_prod10 = Image.new("RGBA", (ancho, alto), transparent_color)
            im_prod11 = Image.open("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Productos/"+ str(int(producto1)) +".png")
            im_prod12 = im_prod11.resize((int(min(ancho, alto)*0.7*multiplicador2),int(min(ancho, alto)*0.7*multiplicador2)))
            x1, y1 = find_first_non_transparent_pixel(im_prod12)
            xf1, yf1 = find_last_non_transparent_pixel(im_prod12)
            crop_im_prod12 = im_prod12.crop((x1, 0, xf1 + 1, im_prod12.height ))
            coordpegar = int(ancho*0.47-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador2)*2))
            finalpegado = coordpegar + crop_im_prod12.width
            img_prod10.paste(crop_im_prod12, (coordpegar, int(alto*0.37-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador2)))+find_floor(im_prod12)), crop_im_prod12)
            

            #img_prod20 = Image.new("RGBA", (ancho, alto), transparent_color)
            im_prod21 = Image.open("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Productos/"+ str(int(producto2)) +".png")
            im_prod22 = im_prod21.resize((int(min(ancho, alto)*0.7*multiplicador2),int(min(ancho, alto)*0.7*multiplicador2)))
            x2, y2 = find_first_non_transparent_pixel(im_prod22)
            xf2, yf2 = find_last_non_transparent_pixel(im_prod22)
            crop_im_prod22 = im_prod22.crop((x2, 0, xf2 + 1, im_prod22.height))
            coordpegar = finalpegado
            finalpegado = coordpegar + crop_im_prod22.width
            img_prod10.paste(crop_im_prod22, (coordpegar, int(alto*0.37-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador2)))+find_floor(im_prod22)), crop_im_prod22)
        
        if productos ==3:
            
            img_prod10 = Image.new("RGBA", (ancho, alto), transparent_color)
            im_prod11 = Image.open("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Productos/"+ str(int(producto1)) +".png")
            im_prod12 = im_prod11.resize((int(min(ancho, alto)*0.7*multiplicador3),int(min(ancho, alto)*0.7*multiplicador3)))
            x1, y1 = find_first_non_transparent_pixel(im_prod12)
            xf1, yf1 = find_last_non_transparent_pixel(im_prod12)
            crop_im_prod12 = im_prod12.crop((x1, 0, xf1 + 1, im_prod12.height ))
            coordpegar = int(ancho*0.3-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador3)*3))
            finalpegado = coordpegar + crop_im_prod12.width
            img_prod10.paste(crop_im_prod12, (coordpegar, int(alto*0.45-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador3)))+find_floor(im_prod12)), crop_im_prod12)
            

            #img_prod20 = Image.new("RGBA", (ancho, alto), transparent_color)
            im_prod21 = Image.open("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Productos/"+ str(int(producto2)) +".png")
            im_prod22 = im_prod21.resize((int(min(ancho, alto)*0.7*multiplicador3),int(min(ancho, alto)*0.7*multiplicador3)))
            x2, y2 = find_first_non_transparent_pixel(im_prod22)
            xf2, yf2 = find_last_non_transparent_pixel(im_prod22)
            crop_im_prod22 = im_prod22.crop((x2, 0, xf2 + 1, im_prod22.height))
            coordpegar = finalpegado
            finalpegado = coordpegar + crop_im_prod22.width
            img_prod10.paste(crop_im_prod22, (coordpegar, int(alto*0.45-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador3)))+find_floor(im_prod22)), crop_im_prod22)
        


            #img_prod30 = Image.new("RGBA", (ancho, alto), transparent_color)
            im_prod31 = Image.open("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Productos/"+ str(int(producto3)) +".png")
            im_prod32 = im_prod31.resize((int(min(ancho, alto)*0.7*multiplicador3),int(min(ancho, alto)*0.7*multiplicador3)))
            x3, y3 = find_first_non_transparent_pixel(im_prod32)
            xf3, yf3 = find_last_non_transparent_pixel(im_prod32)
            crop_im_prod32 = im_prod32.crop((x3, 0, xf3 + 1, im_prod32.height))
            coordpegar = finalpegado
            finalpegado = coordpegar + crop_im_prod32.width
            img_prod10.paste(crop_im_prod32, (coordpegar, int(alto*0.45-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador3)))+find_floor(im_prod32)), crop_im_prod32)
                                

        if productos ==4:
            img_prod10 = Image.new("RGBA", (ancho, alto), transparent_color)
            im_prod11 = Image.open("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Productos/"+ str(int(producto1)) +".png")
            im_prod12 = im_prod11.resize((int(min(ancho, alto)*0.7*multiplicador4),int(min(ancho, alto)*0.7*multiplicador4)))
            x1, y1 = find_first_non_transparent_pixel(im_prod12)
            xf1, yf1 = find_last_non_transparent_pixel(im_prod12)
            crop_im_prod12 = im_prod12.crop((x1, 0, xf1 + 1, im_prod12.height ))
            coordpegar = int(ancho*0.3-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador4)*4))
            finalpegado = coordpegar + crop_im_prod12.width
            img_prod10.paste(crop_im_prod12, (coordpegar, int(alto*0.45-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador4)))+find_floor(im_prod12)), crop_im_prod12)
            

            #img_prod20 = Image.new("RGBA", (ancho, alto), transparent_color)
            im_prod21 = Image.open("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Productos/"+ str(int(producto2)) +".png")
            im_prod22 = im_prod21.resize((int(min(ancho, alto)*0.7*multiplicador4),int(min(ancho, alto)*0.7*multiplicador4)))
            x2, y2 = find_first_non_transparent_pixel(im_prod22)
            xf2, yf2 = find_last_non_transparent_pixel(im_prod22)
            crop_im_prod22 = im_prod22.crop((x2, 0, xf2 + 1, im_prod22.height))
            coordpegar = finalpegado
            finalpegado = coordpegar + crop_im_prod22.width
            img_prod10.paste(crop_im_prod22, (coordpegar, int(alto*0.45-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador4)))+find_floor(im_prod22)), crop_im_prod22)
        


            #img_prod30 = Image.new("RGBA", (ancho, alto), transparent_color)
            im_prod31 = Image.open("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Productos/"+ str(int(producto3)) +".png")
            im_prod32 = im_prod31.resize((int(min(ancho, alto)*0.7*multiplicador4),int(min(ancho, alto)*0.7*multiplicador4)))
            x3, y3 = find_first_non_transparent_pixel(im_prod32)
            xf3, yf3 = find_last_non_transparent_pixel(im_prod32)
            crop_im_prod32 = im_prod32.crop((x3, 0, xf3 + 1, im_prod32.height))
            coordpegar = finalpegado
            finalpegado = coordpegar + crop_im_prod32.width
            img_prod10.paste(crop_im_prod32, (coordpegar, int(alto*0.45-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador4)))+find_floor(im_prod32)), crop_im_prod32)
                                
                    
            #img_prod40 = Image.new("RGBA", (ancho, alto), transparent_color)
            im_prod41 = Image.open("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Productos/"+ str(int(producto4)) +".png")
            im_prod42 = im_prod41.resize((int(min(ancho, alto)*0.7*multiplicador4),int(min(ancho, alto)*0.7*multiplicador4)))
            x4, y4 = find_first_non_transparent_pixel(im_prod42)
            xf4, yf4 = find_last_non_transparent_pixel(im_prod42)
            crop_im_prod42 = im_prod42.crop((x4, 0, xf4 + 1, im_prod42.height))
            coordpegar = finalpegado
            finalpegado = coordpegar + crop_im_prod42.width
            img_prod10.paste(crop_im_prod42, (coordpegar, int(alto*0.45-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador4)))+find_floor(im_prod42)), crop_im_prod42)
            

        
        if backgroundpic == True:
            composite_image = Image.alpha_composite(composite_image, img_prod10)
            
        else:
            composite_image = Image.alpha_composite(img_back, img_prod10)
            
        
        
        #Agrego Título


        if titulo_ancho >= ancho*0.95:
            middle_point = len(titulo) // 2
            split_point = titulo.rfind(" ", 0, middle_point+3)
            titulo = titulo[0:split_point] + "\n" + titulo[split_point+1 : middle_point*2 ]
        
            for k in range(100):
                titulo_ancho, titulo_alto = draw.textsize(titulo[0:split_point], font=font_title)
                if (titulo_ancho / ancho) >0.95:
                    font_title = ImageFont.truetype("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Font/" + marca +" Tittle.otf", int(font_title.size*0.9))
                    titulo_ancho, titulo_alto = draw.textsize(titulo[0:split_point], font=font_title) 

                else: 
                    break
        else:
            for k in range(100):
                titulo_ancho, titulo_alto = draw.textsize(titulo, font=font_title)
                if (titulo_ancho / ancho) >0.95:
                    font_title = ImageFont.truetype("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Font/" + marca +" Tittle.otf", int(font_title.size*0.9))
                    titulo_ancho, titulo_alto = draw.textsize(titulo, font=font_title) 

                else: 
                    break


        img_title = Image.new("RGBA", (ancho, alto), transparent_color)
        
        
        
        draw = ImageDraw.Draw(img_title)
        
        # Specify font settings
        text_position = (10, 10)  # Adjust the text position as needed
        
        # Draw the text
        text = titulo
        draw.text(text_position, text, fill=text_color, font=font_title)
        composite_image = Image.alpha_composite(composite_image, img_title)
        
        
    #Agrego Claim

        for k in range(100):
            claim_ancho, claim_alto = draw.textsize(claim, font=font_claim)
            if claim_ancho < 0.8*ancho:
                font_claim = ImageFont.truetype("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Font/" + marca +" Claim.otf", int(font_claim.size*1.2))
                claim_ancho, claim_alto = draw.textsize(claim, font=font_claim) 

        font_claim = ImageFont.truetype("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Font/" + marca +" Claim.otf", min( int(font_claim.size), int(font_title.size*0.8)))

        if claim_ancho >= ancho*0.95:
            middle_point = len(claim) // 2
            split_point = claim.rfind(" ", 0, middle_point+3)
            claim = claim[0:split_point] + "\n" + claim[split_point+1 : middle_point*2 ]
        
            for k in range(100):
                claim_ancho, claim_alto = draw.textsize(claim[0:split_point], font=font_claim)
                if (claim_ancho / ancho) >0.95:
                    font_claim = ImageFont.truetype("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Font/" + marca +" Claim.otf", int(font_claim.size*0.9))
                    claim_ancho, claim_alto = draw.textsize(claim[0:split_point], font=font_claim) 

                else: 
                    break
        else:
            for k in range(100):
                claim_ancho, claim_alto = draw.textsize(claim, font=font_claim)
                if (claim_ancho / ancho) >0.95:
                    font_claim = ImageFont.truetype("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Font/" + marca +" Claim.otf", int(font_claim.size*0.9))
                    claim_ancho, claim_alto = draw.textsize(claim, font=font_claim) 

                else: 
                    break
    
        img_claim = Image.new("RGBA", (ancho, alto), transparent_color)
        
        from PIL import ImageDraw, ImageFont
        
        draw = ImageDraw.Draw(img_claim)
        
        # Specify font settings
        text_position = (ancho*0.03, alto*0.20)  # Adjust the text position as needed
        
        # Draw the text
        text = claim
        draw.text(text_position, text, fill=text_color, font=font_claim)
        composite_image = Image.alpha_composite(composite_image, img_claim)
        
    #Agrego Call to action
        if callToAction == True:
            img_cta = Image.new("RGBA", (ancho, alto), transparent_color)
            
            from PIL import ImageDraw, ImageFont
            
            draw = ImageDraw.Draw(img_cta)
            
            # Specify font settings
            text_position = (ancho*0.05, alto*0.35)  # Adjust the text position as needed
            
            # Calculate the size of the text
            text = cta
            text_width, text_height = draw.textsize(text, font=font_claim)

            # Calculate the size of the text box based on the text size and padding
            padding = int(ancho*0.02)
            text_box_width = text_width + 2 * padding
            text_box_height = text_height + 2 * padding


            # Draw the filled rectangle (background) behind the text
            text_box_position = (text_position[0] - padding, text_position[1] - padding)
            text_box = (text_box_position[0], text_box_position[1], text_box_position[0] + text_box_width, text_box_position[1] + text_box_height)
            draw.rectangle(text_box, fill=text_box_color)
            
            # Draw the text
            draw.text(text_position, text, fill=buttonletter_color, font=font_claim)
            composite_image = Image.alpha_composite(composite_image, img_cta)
        
        #Agrego Disclaimer
        posy_disc= 0.95
        if disc_ancho >= ancho*0.95:
            middle_point = len(disclaimer) // 2
            split_point = disclaimer.rfind(" ", 0, middle_point+3)
            disclaimer = disclaimer[0:split_point] + "\n" + disclaimer[split_point+1 : middle_point*2 ]
            posy_disc= 0.93
            
        img_disclaimer = Image.new("RGBA", (ancho, alto), transparent_color)
        
        from PIL import ImageDraw, ImageFont
        
        draw = ImageDraw.Draw(img_disclaimer)
        
        # Specify font settings
        text_position = (ancho*0.03, alto*posy_disc)  # Adjust the text position as needed
        
        # Draw the text
        text = disclaimer
        draw.text(text_position, text, fill=text_color, font=font_disclaimer)
        composite_image = Image.alpha_composite(composite_image, img_disclaimer)


    #Construir imagen tipo cuadrado:
    if tipo == "H":
        
        font_title = ImageFont.truetype("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Font/" + marca +" Tittle.otf", int(50/400*min(ancho, alto)))
        font_claim = ImageFont.truetype("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Font/"+ marca +" Claim.otf", int(37/400*min(ancho, alto)))
        font_disclaimer = ImageFont.truetype("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Font/"+ marca +" Disclaimer.otf", int(10/400*min(ancho, alto)))
        
        titulo_ancho, titulo_alto = draw.textsize(titulo, font=font_title)

        img_back = Image.new("RGBA", (ancho, alto), transparent_color)
        draw = ImageDraw.Draw(img_back)

        # Create a horizontal gradient from left to right
        for x in range(ancho):
            # Calculate the color at this position based on interpolation
            r = int(start_color[0] + (end_color[0] - start_color[0]) * (x / ancho))
            g = int(start_color[1] + (end_color[1] - start_color[1]) * (x / ancho))
            b = int(start_color[2] + (end_color[2] - start_color[2]) * (x / ancho))
            a = int(start_color[3] + (end_color[3] - start_color[3]) * (x / ancho))
            
            # Set the pixel color
            draw.line([(x, 0), (x, alto)], fill=(r, g, b, a))

        #Agrego Background (si hay)
        
        if backgroundpic == True:
            img_backg = Image.new("RGBA", (ancho, alto), transparent_color)
            #im_backg1 = Image.open("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Background/Herbal Essences.png")
            im_backg1 = opbackgroundpic
            
            #im_backg2 = im_backg1.resize((int(ancho),int(alto)))
            im_backg2 = im_backg1.crop((0,0, int(ancho), int(alto)))
            
            
            img_backg.paste(im_backg2, (0, 0))
            
            composite_image = Image.alpha_composite(img_back, im_backg2)
        
        
        
        #Agrego las imágenes de producto
        #Productos
        
        multiplicador1 = 1.1*opscale
        multiplicador2= 0.9*opscale
        multiplicador3= 0.8*opscale
        multiplicador4 = 0.7*opscale
        locatorscale= (opscale-1)*0.5
        finalpegado = 0
        coordpegar	= 0
        padding = 20
        current_x = 0
        
        if productos ==1:
            img_prod10 = Image.new("RGBA", (ancho, alto), transparent_color)
            im_prod11 = Image.open("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Productos/"+ str(int(producto1)) +".png")
            im_prod12 = im_prod11.resize((int(min(ancho, alto)*0.7*multiplicador1),int(min(ancho,alto)*0.7*multiplicador1)))
            img_prod10.paste(im_prod12, (int(ancho*0.6-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador1))), int(alto*0.2-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador1)))))
        
        if productos ==2:
            img_prod10 = Image.new("RGBA", (ancho, alto), transparent_color)
            im_prod11 = Image.open("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Productos/"+ str(int(producto1)) +".png")
            im_prod12 = im_prod11.resize((int(min(ancho, alto)*0.7*multiplicador2),int(min(ancho, alto)*0.7*multiplicador2)))
            x1, y1 = find_first_non_transparent_pixel(im_prod12)
            xf1, yf1 = find_last_non_transparent_pixel(im_prod12)
            crop_im_prod12 = im_prod12.crop((x1, 0, xf1 + 1, im_prod12.height ))
            coordpegar = int(ancho*0.6-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador2)*2))
            finalpegado = coordpegar + crop_im_prod12.width
            img_prod10.paste(crop_im_prod12, (coordpegar, int(alto*0.3-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador2)))+find_floor(im_prod12)), crop_im_prod12)
            

            im_prod21 = Image.open("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Productos/"+ str(int(producto2)) +".png")
            im_prod22 = im_prod21.resize((int(min(ancho, alto)*0.7*multiplicador2),int(min(ancho, alto)*0.7*multiplicador2)))
            x2, y2 = find_first_non_transparent_pixel(im_prod22)
            xf2, yf2 = find_last_non_transparent_pixel(im_prod22)
            crop_im_prod22 = im_prod22.crop((x2, 0, xf2 + 1, im_prod22.height))
            coordpegar = finalpegado
            finalpegado = coordpegar + crop_im_prod22.width
            img_prod10.paste(crop_im_prod22, (coordpegar, int(alto*0.3-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador2)))+find_floor(im_prod22)), crop_im_prod22)
        
        if productos ==3:
            
            img_prod10 = Image.new("RGBA", (ancho, alto), transparent_color)
            im_prod11 = Image.open("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Productos/"+ str(int(producto1)) +".png")
            im_prod12 = im_prod11.resize((int(min(ancho, alto)*0.7*multiplicador3),int(min(ancho, alto)*0.7*multiplicador3)))
            x1, y1 = find_first_non_transparent_pixel(im_prod12)
            xf1, yf1 = find_last_non_transparent_pixel(im_prod12)
            crop_im_prod12 = im_prod12.crop((x1, 0, xf1 + 1, im_prod12.height ))
            coordpegar = int(ancho*0.6-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador3)*3))
            finalpegado = coordpegar + crop_im_prod12.width
            img_prod10.paste(crop_im_prod12, (coordpegar, int(alto*0.3-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador3)))+find_floor(im_prod12)), crop_im_prod12)
            

            im_prod21 = Image.open("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Productos/"+ str(int(producto2)) +".png")
            im_prod22 = im_prod21.resize((int(min(ancho, alto)*0.7*multiplicador3),int(min(ancho, alto)*0.7*multiplicador3)))
            x2, y2 = find_first_non_transparent_pixel(im_prod22)
            xf2, yf2 = find_last_non_transparent_pixel(im_prod22)
            crop_im_prod22 = im_prod22.crop((x2, 0, xf2 + 1, im_prod22.height))
            coordpegar = finalpegado
            finalpegado = coordpegar + crop_im_prod22.width
            img_prod10.paste(crop_im_prod22, (coordpegar, int(alto*0.3-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador3)))+find_floor(im_prod22)), crop_im_prod22)
        


            im_prod31 = Image.open("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Productos/"+ str(int(producto3)) +".png")
            im_prod32 = im_prod31.resize((int(min(ancho, alto)*0.7*multiplicador3),int(min(ancho, alto)*0.7*multiplicador3)))
            x3, y3 = find_first_non_transparent_pixel(im_prod32)
            xf3, yf3 = find_last_non_transparent_pixel(im_prod32)
            crop_im_prod32 = im_prod32.crop((x3, 0, xf3 + 1, im_prod32.height))
            coordpegar = finalpegado
            finalpegado = coordpegar + crop_im_prod32.width
            img_prod10.paste(crop_im_prod32, (coordpegar, int(alto*0.3-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador3)))+find_floor(im_prod32)), crop_im_prod32)
                                

        if productos ==4:
            img_prod10 = Image.new("RGBA", (ancho, alto), transparent_color)
            im_prod11 = Image.open("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Productos/"+ str(int(producto1)) +".png")
            im_prod12 = im_prod11.resize((int(min(ancho, alto)*0.7*multiplicador4),int(min(ancho, alto)*0.7*multiplicador4)))
            x1, y1 = find_first_non_transparent_pixel(im_prod12)
            xf1, yf1 = find_last_non_transparent_pixel(im_prod12)
            crop_im_prod12 = im_prod12.crop((x1, 0, xf1 + 1, im_prod12.height ))
            coordpegar = int(ancho*0.5-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador4)*4))
            finalpegado = coordpegar + crop_im_prod12.width
            img_prod10.paste(crop_im_prod12, (coordpegar, int(alto*0.3-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador4)))+find_floor(im_prod12)), crop_im_prod12)
            

            im_prod21 = Image.open("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Productos/"+ str(int(producto2)) +".png")
            im_prod22 = im_prod21.resize((int(min(ancho, alto)*0.7*multiplicador4),int(min(ancho, alto)*0.7*multiplicador4)))
            x2, y2 = find_first_non_transparent_pixel(im_prod22)
            xf2, yf2 = find_last_non_transparent_pixel(im_prod22)
            crop_im_prod22 = im_prod22.crop((x2, 0, xf2 + 1, im_prod22.height))
            coordpegar = finalpegado
            finalpegado = coordpegar + crop_im_prod22.width
            img_prod10.paste(crop_im_prod22, (coordpegar, int(alto*0.3-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador4)))+find_floor(im_prod22)), crop_im_prod22)
        


            im_prod31 = Image.open("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Productos/"+ str(int(producto3)) +".png")
            im_prod32 = im_prod31.resize((int(min(ancho, alto)*0.7*multiplicador4),int(min(ancho, alto)*0.7*multiplicador4)))
            x3, y3 = find_first_non_transparent_pixel(im_prod32)
            xf3, yf3 = find_last_non_transparent_pixel(im_prod32)
            crop_im_prod32 = im_prod32.crop((x3, 0, xf3 + 1, im_prod32.height))
            coordpegar = finalpegado
            finalpegado = coordpegar + crop_im_prod32.width
            img_prod10.paste(crop_im_prod32, (coordpegar, int(alto*0.3-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador4)))+find_floor(im_prod32)), crop_im_prod32)
                                

            im_prod41 = Image.open("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Productos/"+ str(int(producto4)) +".png")
            im_prod42 = im_prod41.resize((int(min(ancho, alto)*0.7*multiplicador4),int(min(ancho, alto)*0.7*multiplicador4)))
            x4, y4 = find_first_non_transparent_pixel(im_prod42)
            xf4, yf4 = find_last_non_transparent_pixel(im_prod42)
            crop_im_prod42 = im_prod42.crop((x4, 0, xf4 + 1, im_prod42.height))
            coordpegar = finalpegado
            finalpegado = coordpegar + crop_im_prod42.width
            img_prod10.paste(crop_im_prod42, (coordpegar, int(alto*0.3-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador4)))+find_floor(im_prod42)), crop_im_prod42)
            

        
        if backgroundpic == True:
            composite_image = Image.alpha_composite(composite_image, img_prod10)
            
        else:
            composite_image = Image.alpha_composite(img_back, img_prod10)
            
        
        
        #Agrego Título
        
        if titulo_ancho >= ancho*0.5:
            middle_point = len(titulo) // 2
            split_point = titulo.rfind(" ", 0, middle_point+3)
            titulo = titulo[0:split_point] + "\n" + titulo[split_point+1 : middle_point*2 ]
        
            for k in range(100):
                titulo_ancho, titulo_alto = draw.textsize(titulo[0:split_point], font=font_title)
                if (titulo_ancho / ancho) >0.95:
                    font_title = ImageFont.truetype("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Font/" + marca +" Tittle.otf", int(font_title.size*0.9))
                    titulo_ancho, titulo_alto = draw.textsize(titulo[0:split_point], font=font_title) 

                else: 
                    break
        for k in range(100):
            titulo_ancho, titulo_alto = draw.textsize(titulo, font=font_title)
            if (titulo_ancho / ancho) >0.95:
                font_title = ImageFont.truetype("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Font/" + marca +" Tittle.otf", int(font_title.size*0.9))
                titulo_ancho, titulo_alto = draw.textsize(titulo, font=font_title) 

            else: 
                break

    

        img_title = Image.new("RGBA", (ancho, alto), transparent_color)
        
        
        
        draw = ImageDraw.Draw(img_title)
        
        # Specify font settings
        text_position = (10, 10)  # Adjust the text position as needed
        
        # Draw the text
        text = titulo
        draw.text(text_position, text, fill=text_color, font=font_title)
        composite_image = Image.alpha_composite(composite_image, img_title)
        
        
    #Agrego Claim
        
        for k in range(100):
            claim_ancho, claim_alto = draw.textsize(claim, font=font_claim)
            if claim_ancho < 0.8*ancho:
                font_claim = ImageFont.truetype("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Font/" + marca +" Claim.otf", int(font_claim.size*1.2))
                claim_ancho, claim_alto = draw.textsize(claim, font=font_claim) 
        
        font_claim = ImageFont.truetype("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Font/" + marca +" Claim.otf", min( int(font_claim.size), int(font_title.size*0.8)))


        if claim_ancho >= ancho*0.95:
            middle_point = len(claim) // 2
            split_point = claim.rfind(" ", 0, middle_point+3)
            claim = claim[0:split_point] + "\n" + claim[split_point+1 : middle_point*2 ]
        
        
            for k in range(100):
                claim_ancho, claim_alto = draw.textsize(claim[0:split_point], font=font_claim)
                if (claim_ancho / ancho) >0.95:
                    font_claim = ImageFont.truetype("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Font/" + marca +" Claim.otf", int(font_claim.size*0.9))
                    claim_ancho, claim_alto = draw.textsize(claim[0:split_point], font=font_claim) 

                else: 
                    break

        for k in range(100):
                claim_ancho, claim_alto = draw.textsize(claim, font=font_claim)
                if (claim_ancho / ancho) >0.95:
                    font_claim = ImageFont.truetype("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Font/" + marca +" Claim.otf", int(font_claim.size*0.9))
                    claim_ancho, claim_alto = draw.textsize(claim, font=font_claim) 

                else: 
                    break
        
            

        img_claim = Image.new("RGBA", (ancho, alto), transparent_color)
        
        from PIL import ImageDraw, ImageFont
        
        draw = ImageDraw.Draw(img_claim)
        
        # Specify font settings
        text_position = (ancho*0.03, alto*0.3)  # Adjust the text position as needed
        
        # Draw the text
        text = claim
        draw.text(text_position, text, fill=text_color, font=font_claim)
        composite_image = Image.alpha_composite(composite_image, img_claim)
        
    #Agrego Call to action
        if callToAction == True:
            img_cta = Image.new("RGBA", (ancho, alto), transparent_color)
            
            from PIL import ImageDraw, ImageFont
            
            draw = ImageDraw.Draw(img_cta)
            
            # Specify font settings
            text_position = (ancho*0.05, alto*0.65)  # Adjust the text position as needed
            
            # Calculate the size of the text
            text = cta
            text_width, text_height = draw.textsize(text, font=font_claim)

            # Calculate the size of the text box based on the text size and padding
            padding = int(ancho*0.02)
            text_box_width = text_width + 2 * padding
            text_box_height = text_height + 2 * padding


            # Draw the filled rectangle (background) behind the text
            text_box_position = (text_position[0] - padding, text_position[1] - padding)
            text_box = (text_box_position[0], text_box_position[1], text_box_position[0] + text_box_width, text_box_position[1] + text_box_height)
            draw.rectangle(text_box, fill=text_box_color)
            
            # Draw the text
            draw.text(text_position, text, fill=buttonletter_color, font=font_claim)
            composite_image = Image.alpha_composite(composite_image, img_cta)
        
        #Agrego Disclaimer
        posy_disc= 0.95
        if disc_ancho >= ancho*0.95:
            middle_point = len(disclaimer) // 2
            split_point = disclaimer.rfind(" ", 0, middle_point+3)
            disclaimer = disclaimer[0:split_point] + "\n" + disclaimer[split_point+1 : middle_point*2 ]
            posy_disc= 0.93
            
        img_disclaimer = Image.new("RGBA", (ancho, alto), transparent_color)
        
        from PIL import ImageDraw, ImageFont
        
        draw = ImageDraw.Draw(img_disclaimer)
        
        # Specify font settings
        text_position = (ancho*0.03, alto*posy_disc)  # Adjust the text position as needed
        
        # Draw the text
        text = disclaimer
        draw.text(text_position, text, fill=text_color, font=font_disclaimer)
        composite_image = Image.alpha_composite(composite_image, img_disclaimer)

    if tipo == "V":
        
        font_title = ImageFont.truetype("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Font/" + marca +" Tittle.otf", int(50/400*min(ancho, alto)))
        font_claim = ImageFont.truetype("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Font/"+ marca +" Claim.otf", int(20/400*min(ancho, alto)))
        font_disclaimer = ImageFont.truetype("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Font/"+ marca +" Disclaimer.otf", int(10/400*min(ancho, alto)))

        titulo_ancho, titulo_alto = draw.textsize(titulo, font=font_title)

        img_back = Image.new("RGBA", (ancho, alto), transparent_color)
        draw = ImageDraw.Draw(img_back)

        # Create a horizontal gradient from left to right
        for x in range(ancho):
            # Calculate the color at this position based on interpolation
            r = int(start_color[0] + (end_color[0] - start_color[0]) * (x / ancho))
            g = int(start_color[1] + (end_color[1] - start_color[1]) * (x / ancho))
            b = int(start_color[2] + (end_color[2] - start_color[2]) * (x / ancho))
            a = int(start_color[3] + (end_color[3] - start_color[3]) * (x / ancho))
            
            # Set the pixel color
            draw.line([(x, 0), (x, alto)], fill=(r, g, b, a))

        #Agrego Background (si hay)
        
        if backgroundpic == True:
            img_backg = Image.new("RGBA", (ancho, alto), transparent_color)
            #im_backg1 = Image.open("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Background/Herbal Essences.png")
            im_backg1= opbackgroundpic
            
            #im_backg2 = im_backg1.resize((int(ancho),int(alto)))
            im_backg2 = im_backg1.crop((0,0, int(ancho), int(alto)))
            
            
            img_backg.paste(im_backg2, (0, 0))
            
            composite_image = Image.alpha_composite(img_back, im_backg2)
        
        
        
        #Agrego las imágenes de producto
        #Productos
        
        multiplicador1 = 1.1*opscale
        multiplicador2= 0.9*opscale
        multiplicador3= 0.8*opscale
        multiplicador4 = 0.7*opscale
        locatorscale= (opscale-1)*0.5
        finalpegado = 0
        coordpegar	= 0
        padding = 20
        current_x = 0
        
        if productos ==1:
            img_prod10 = Image.new("RGBA", (ancho, alto), transparent_color)
            im_prod11 = Image.open("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Productos/"+ str(int(producto1)) +".png")
            im_prod12 = im_prod11.resize((int(min(ancho, alto)*0.7*multiplicador1),int(min(ancho,alto)*0.7*multiplicador1)))
            img_prod10.paste(im_prod12, (int(ancho*0.1-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador1))), int(alto*0.6-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador1)))))
        
        if productos ==2:
            img_prod10 = Image.new("RGBA", (ancho, alto), transparent_color)
            im_prod11 = Image.open("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Productos/"+ str(int(producto1)) +".png")
            im_prod12 = im_prod11.resize((int(min(ancho, alto)*0.7*multiplicador2),int(min(ancho, alto)*0.7*multiplicador2)))
            x1, y1 = find_first_non_transparent_pixel(im_prod12)
            xf1, yf1 = find_last_non_transparent_pixel(im_prod12)
            crop_im_prod12 = im_prod12.crop((x1, 0, xf1 + 1, im_prod12.height ))
            coordpegar = int(ancho*0.1-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador2)*2))
            finalpegado = coordpegar + crop_im_prod12.width
            img_prod10.paste(crop_im_prod12, (coordpegar, int(alto*0.6-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador2)))+find_floor(im_prod12)), crop_im_prod12)
            

            im_prod21 = Image.open("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Productos/"+ str(int(producto2)) +".png")
            im_prod22 = im_prod21.resize((int(min(ancho, alto)*0.7*multiplicador2),int(min(ancho, alto)*0.7*multiplicador2)))
            x2, y2 = find_first_non_transparent_pixel(im_prod22)
            xf2, yf2 = find_last_non_transparent_pixel(im_prod22)
            crop_im_prod22 = im_prod22.crop((x2, 0, xf2 + 1, im_prod22.height))
            coordpegar = finalpegado-int(ancho*0.02)
            finalpegado = coordpegar + crop_im_prod22.width
            img_prod10.paste(crop_im_prod22, (coordpegar, int(alto*0.6-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador2)))+find_floor(im_prod22)), crop_im_prod22)
        
        if productos ==3:
            
            img_prod10 = Image.new("RGBA", (ancho, alto), transparent_color)
            im_prod11 = Image.open("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Productos/"+ str(int(producto1)) +".png")
            im_prod12 = im_prod11.resize((int(min(ancho, alto)*0.7*multiplicador3),int(min(ancho, alto)*0.7*multiplicador3)))
            x1, y1 = find_first_non_transparent_pixel(im_prod12)
            xf1, yf1 = find_last_non_transparent_pixel(im_prod12)
            crop_im_prod12 = im_prod12.crop((x1, 0, xf1 + 1, im_prod12.height ))
            coordpegar = int(ancho*0.1-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador3)*3))
            finalpegado = coordpegar + crop_im_prod12.width
            img_prod10.paste(crop_im_prod12, (coordpegar, int(alto*0.6-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador3)))+find_floor(im_prod12)), crop_im_prod12)
            

            im_prod21 = Image.open("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Productos/"+ str(int(producto2)) +".png")
            im_prod22 = im_prod21.resize((int(min(ancho, alto)*0.7*multiplicador3),int(min(ancho, alto)*0.7*multiplicador3)))
            x2, y2 = find_first_non_transparent_pixel(im_prod22)
            xf2, yf2 = find_last_non_transparent_pixel(im_prod22)
            crop_im_prod22 = im_prod22.crop((x2, 0, xf2 + 1, im_prod22.height))
            coordpegar = finalpegado-int(ancho*0.01)
            finalpegado = coordpegar + crop_im_prod22.width
            img_prod10.paste(crop_im_prod22, (coordpegar, int(alto*0.6-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador3)))+find_floor(im_prod22)), crop_im_prod22)
        


            im_prod31 = Image.open("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Productos/"+ str(int(producto3)) +".png")
            im_prod32 = im_prod31.resize((int(min(ancho, alto)*0.7*multiplicador3),int(min(ancho, alto)*0.7*multiplicador3)))
            x3, y3 = find_first_non_transparent_pixel(im_prod32)
            xf3, yf3 = find_last_non_transparent_pixel(im_prod32)
            crop_im_prod32 = im_prod32.crop((x3, 0, xf3 + 1, im_prod32.height))
            coordpegar = finalpegado-int(ancho*0.01)
            finalpegado = coordpegar + crop_im_prod32.width
            img_prod10.paste(crop_im_prod32, (coordpegar, int(alto*0.6-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador3)))+find_floor(im_prod32)), crop_im_prod32)
                                

        if productos ==4:
            img_prod10 = Image.new("RGBA", (ancho, alto), transparent_color)
            im_prod11 = Image.open("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Productos/"+ str(int(producto1)) +".png")
            im_prod12 = im_prod11.resize((int(min(ancho, alto)*0.7*multiplicador4),int(min(ancho, alto)*0.7*multiplicador4)))
            x1, y1 = find_first_non_transparent_pixel(im_prod12)
            xf1, yf1 = find_last_non_transparent_pixel(im_prod12)
            crop_im_prod12 = im_prod12.crop((x1, 0, xf1 + 1, im_prod12.height ))
            coordpegar = int(ancho*0.1-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador4)*4))
            finalpegado = coordpegar + crop_im_prod12.width
            img_prod10.paste(crop_im_prod12, (coordpegar, int(alto*0.6-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador4)))+find_floor(im_prod12)), crop_im_prod12)
            

            im_prod21 = Image.open("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Productos/"+ str(int(producto2)) +".png")
            im_prod22 = im_prod21.resize((int(min(ancho, alto)*0.7*multiplicador4),int(min(ancho, alto)*0.7*multiplicador4)))
            x2, y2 = find_first_non_transparent_pixel(im_prod22)
            xf2, yf2 = find_last_non_transparent_pixel(im_prod22)
            crop_im_prod22 = im_prod22.crop((x2, 0, xf2 + 1, im_prod22.height))
            coordpegar = finalpegado-int(ancho*0.01)
            finalpegado = coordpegar + crop_im_prod22.width
            img_prod10.paste(crop_im_prod22, (coordpegar, int(alto*0.6-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador4)))+find_floor(im_prod22)), crop_im_prod22)
        


            im_prod31 = Image.open("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Productos/"+ str(int(producto3)) +".png")
            im_prod32 = im_prod31.resize((int(min(ancho, alto)*0.7*multiplicador4),int(min(ancho, alto)*0.7*multiplicador4)))
            x3, y3 = find_first_non_transparent_pixel(im_prod32)
            xf3, yf3 = find_last_non_transparent_pixel(im_prod32)
            crop_im_prod32 = im_prod32.crop((x3, 0, xf3 + 1, im_prod32.height))
            coordpegar = finalpegado-int(ancho*0.01)
            finalpegado = coordpegar + crop_im_prod32.width
            img_prod10.paste(crop_im_prod32, (coordpegar, int(alto*0.6-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador4)))+find_floor(im_prod32)), crop_im_prod32)
                                

            im_prod41 = Image.open("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Productos/"+ str(int(producto4)) +".png")
            im_prod42 = im_prod41.resize((int(min(ancho, alto)*0.7*multiplicador4),int(min(ancho, alto)*0.7*multiplicador4)))
            x4, y4 = find_first_non_transparent_pixel(im_prod42)
            xf4, yf4 = find_last_non_transparent_pixel(im_prod42)
            crop_im_prod42 = im_prod42.crop((x4, 0, xf4 + 1, im_prod42.height))
            coordpegar = finalpegado-int(ancho*0.01)
            finalpegado = coordpegar + crop_im_prod42.width
            img_prod10.paste(crop_im_prod42, (coordpegar, int(alto*0.6-max(0,locatorscale*int(min(ancho, alto)*0.7*multiplicador4)))+find_floor(im_prod42)), crop_im_prod42)
            

        
        if backgroundpic == True:
            composite_image = Image.alpha_composite(composite_image, img_prod10)
            
        else:
            composite_image = Image.alpha_composite(img_back, img_prod10)
            
        
        
        #Agrego Título

        if titulo_ancho >= ancho*0.5:
            middle_point = len(titulo) // 2
            split_point = titulo.rfind(" ", 0, middle_point+3)
            titulo = titulo[0:split_point] + "\n" + titulo[split_point+1 : middle_point*2 ]
        
            for k in range(100):
                titulo_ancho, titulo_alto = draw.textsize(titulo[0:split_point], font=font_title)
                if (titulo_ancho / ancho) >0.95:
                    font_title = ImageFont.truetype("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Font/" + marca +" Tittle.otf", int(font_title.size*0.9))
                    titulo_ancho, titulo_alto = draw.textsize(titulo[0:split_point], font=font_title) 

                else: 
                    break
        
        for k in range(100):
                titulo_ancho, titulo_alto = draw.textsize(titulo, font=font_title)
                if (titulo_ancho / ancho) >0.95:
                    font_title = ImageFont.truetype("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Font/" + marca +" Tittle.otf", int(font_title.size*0.9))
                    titulo_ancho, titulo_alto = draw.textsize(titulo, font=font_title) 

                else: 
                    break



        img_title = Image.new("RGBA", (ancho, alto), transparent_color)
        
        
        
        draw = ImageDraw.Draw(img_title)
        
        # Specify font settings
        text_position = (ancho*0.04, alto*0.1)  # Adjust the text position as needed
        
        # Draw the text
        text = titulo
        draw.text(text_position, text, fill=text_color, font=font_title)
        composite_image = Image.alpha_composite(composite_image, img_title)
        
        
    #Agrego Claim

        for k in range(100):
            claim_ancho, claim_alto = draw.textsize(claim, font=font_claim)
            if claim_ancho < 0.8*ancho:
                font_claim = ImageFont.truetype("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Font/" + marca +" Claim.otf", int(font_claim.size*1.2))
                claim_ancho, claim_alto = draw.textsize(claim, font=font_claim) 
        
        font_claim = ImageFont.truetype("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Font/" + marca +" Claim.otf", min( int(font_claim.size), int(font_title.size*0.8)))


        if claim_ancho >= ancho*0.95:
            middle_point = len(claim) // 2
            split_point = claim.rfind(" ", 0, middle_point+3)
            claim = claim[0:split_point] + "\n" + claim[split_point+1 : middle_point*2 ]
        
        
            for k in range(100):
                claim_ancho, claim_alto = draw.textsize(claim[0:split_point], font=font_claim)
                if (claim_ancho / ancho) >0.95:
                    font_claim = ImageFont.truetype("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Font/" + marca +" Claim.otf", int(font_claim.size*0.9))
                    claim_ancho, claim_alto = draw.textsize(claim[0:split_point], font=font_claim) 

                else: 
                    break

            for k in range(100):
                claim_ancho, claim_alto = draw.textsize(claim, font=font_claim)
                if (claim_ancho / ancho) >0.95:
                    font_claim = ImageFont.truetype("C:/Users/abisambra.d/Procter and Gamble/Emerging Channels Colombia - Documents/E-commerce/Imagination/Imagination 2.0/Input/Font/" + marca +" Claim.otf", int(font_claim.size*0.9))
                    claim_ancho, claim_alto = draw.textsize(claim, font=font_claim) 

                else: 
                    break

        img_claim = Image.new("RGBA", (ancho, alto), transparent_color)
        
        from PIL import ImageDraw, ImageFont
        
        draw = ImageDraw.Draw(img_claim)
        
        # Specify font settings
        text_position = (ancho*0.03, alto*0.23)  # Adjust the text position as needed
        
        # Draw the text
        text = claim
        draw.text(text_position, text, fill=text_color, font=font_claim)
        composite_image = Image.alpha_composite(composite_image, img_claim)
        
    #Agrego Call to action
        if callToAction == True:
            img_cta = Image.new("RGBA", (ancho, alto), transparent_color)
            
            from PIL import ImageDraw, ImageFont
            
            draw = ImageDraw.Draw(img_cta)
            
            # Specify font settings
            text_position = (ancho*0.05, alto*0.45)  # Adjust the text position as needed
            
            # Calculate the size of the text
            text = cta
            text_width, text_height = draw.textsize(text, font=font_claim)

            # Calculate the size of the text box based on the text size and padding
            padding = int(ancho*0.02)
            text_box_width = text_width + 2 * padding
            text_box_height = text_height + 2 * padding


            # Draw the filled rectangle (background) behind the text
            text_box_position = (text_position[0] - padding, text_position[1] - padding)
            text_box = (text_box_position[0], text_box_position[1], text_box_position[0] + text_box_width, text_box_position[1] + text_box_height)
            draw.rectangle(text_box, fill=text_box_color)
            
            # Draw the text
            draw.text(text_position, text, fill=buttonletter_color, font=font_claim)
            composite_image = Image.alpha_composite(composite_image, img_cta)
        
        #Agrego Disclaimer
        posy_disc= 0.95
        if disc_ancho >= ancho*0.95:
            middle_point = len(disclaimer) // 2
            split_point = disclaimer.rfind(" ", 0, middle_point+3)
            disclaimer = disclaimer[0:split_point] + "\n" + disclaimer[split_point+1 : middle_point*2 ]
            posy_disc= 0.93
            
        img_disclaimer = Image.new("RGBA", (ancho, alto), transparent_color)
        
        from PIL import ImageDraw, ImageFont
        
        draw = ImageDraw.Draw(img_disclaimer)
        
        # Specify font settings
        text_position = (ancho*0.03, alto*posy_disc)  # Adjust the text position as needed
        
        # Draw the text
        text = disclaimer
        draw.text(text_position, text, fill=text_color, font=font_disclaimer)
        composite_image = Image.alpha_composite(composite_image, img_disclaimer)

    # Save or display the image
    #composite_image.save("gradient_background.png")  # Save the image
    #composite_image.show()  # Display the image
        
    image_bytes = BytesIO()
    composite_image.save(image_bytes, format="PNG")
    image_bytes.seek(0)

# Convert BytesIO to base64
    b64_image = base64.b64encode(image_bytes.read()).decode()

# Create a download link for the image
    href = f"<a href=\"data:image/png;base64,{b64_image}\" download='banner.png'>\
    Download Image\
    </a>"

# Display the download link
    st.sidebar.markdown(href, unsafe_allow_html=True)

#Publish Streamlit
#Correr en command prompt:
#cd-> incluir directorio
# Correr: streamlit run Imaginationstreamlit.py
#Local URL: http://localhost:8501
#Network URL: http://143.3.120.77:8501









