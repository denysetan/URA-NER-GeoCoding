# Core Pkgs
import streamlit as st 
from streamlit_folium import folium_static
import folium

# NLP Pkgs
import spacy_streamlit
import spacy
nlp = spacy.load('en_core_web_sm')

import os
import json
import requests


def main():
	"""A Simple NLP app with Spacy-Streamlit"""

	st.title("Named-Entity Recognition for SG Locations")

	menu = ["Home","NER"]
	st.sidebar.subheader('Select the functions to display')
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.image('cover_photo.jpg')
		st.header("Project Background")
		''' Often, when a feedback comes in to URA, it would include references to place names, roads, addresses, etc. 
		These references to locations would be **useful to planners** reviewing each case, as it provides a **spatial context**.
 		'''
		st.image('image1.png')
		st.header("Value of Project")
		'''Previously, identifying the locations tagged to each text message and generating geospatial coordinates were **manual and time consuming**.
		\nThe project therefore aims to utilise **Natural Language Processing Techniques** to automate the process, providing time savings for planners.
		\n**The model has 2 parts:**
		'''
		st.image('image2.png')

	elif choice == "NER":
		st.header("Named Entity Recognition and GeoCoding")
		raw_text = st.text_area("","Enter Text Here")
		
		# perform NER and visualise output
		docx = nlp(raw_text)
		spacy_streamlit.visualize_ner(docx,labels=nlp.get_pipe('ner').labels)

		locations = []
		for ent in docx.ents:
			if ent.label_ in ['LOC','GPE', 'ORG']:
				locations.append(ent.text)

		if locations:
			# get geocoordinates from onemap API
			query_address = locations[0]
			query_string='https://developers.onemap.sg/commonapi/search?searchVal='+str(query_address)+'&returnGeom=Y&getAddrDetails=Y'
			resp = requests.get(query_string)
			data = json.loads(resp.content) #Convert JSON into Python Object 

			location_coordinates = []
			location_names = []
			length = data['found'] # number of locations detected by onemap

			maximum = 5
			if length > 0 and length < 5:
				maximum	= length
			if length > 0:
				# store location infos - names and coordinates
				for i in range(maximum):
					results = data['results'][i]
					location_coordinates.append([results['LATITUDE'],results['LONGITUDE']])
					location_names.append(results['SEARCHVAL'])

				st.header("GeoCoded Map")
				m = folium.Map(location=location_coordinates[0], zoom_start=16)
				# add markers
				for point in range(0, maximum):
					folium.Marker(location_coordinates[point], popup=location_names[point]).add_to(m)
				# call to render Folium map in Streamlit
				folium_static(m)





if __name__ == '__main__':
	main()