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
#from PIL import Image


def main():
	"""A Simple NLP app with Spacy-Streamlit"""

	st.title("Natural Language Processing Dashboard")
    # our_image = Image.open(os.path.join('SpaCy_logo.svg.png'))
	# st.image(our_image)

	menu = ["Home","NER"]
	st.sidebar.subheader('Select the functions to display')
	choice = st.sidebar.selectbox("Menu",menu)
	

	if choice == "Home":
		st.header("Tokenization")
		raw_text = st.text_area("Your Text","Enter Text Here")
		docx = nlp(raw_text)
		if st.button("Tokenize"):
			spacy_streamlit.visualize_tokens(docx,attrs=['text','pos_','dep_','ent_type_'])

	elif choice == "NER":
		st.subheader("Named Entity Recognition and GeoCoding")
		raw_text = st.text_area("Your Text","Enter Text Here")
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
			#Convert JSON into Python Object 
			data = json.loads(resp.content)

			location_coordinates = []
			location_names = []
			length = data['found']

			maximum = 5
			if length > 0 and length < 5:
				maximum	= length
			if length > 0:
				for i in range(maximum):
					results = data['results'][i]
					location_coordinates.append([results['LATITUDE'],results['LONGITUDE']])
					location_names.append(results['SEARCHVAL'])

				m = folium.Map(location=location_coordinates[0], zoom_start=16)

				# add marker
				for point in range(0, maximum):
					folium.Marker(location_coordinates[point], popup=location_names[point]).add_to(m)
				# call to render Folium map in Streamlit
				folium_static(m)





if __name__ == '__main__':
	main()