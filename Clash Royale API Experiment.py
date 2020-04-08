#!/usr/bin/env python
# coding: utf-8

# First we import requests module and json module to accomodate the file format.
import requests
import json
import time
from sklearn.preprocessing import StandardScaler
import pandas as pd
import folium
from IPython.display import display

def main(api):
	# Make request to server
	info = requests.get('https://api.clashroyale.com/v1/locations',headers={'Accept': "application/json",'Authorization': f'Bearer {api}'})

	# Cannot take literal value because in json false = False
	info = json.loads(info.text)

	# Put data into an array. Take a look at info if hard to see why it is needed.
	info_list = list(info['items']) 

	# My goal is to see the skill level of players in each continent/country. To do this, I take the sum of top 100 players' trophies and combine them

	df = pd.DataFrame([[],[]]).T
	df.columns = ['Country','Id']

	for country in enumerate(info_list):
		df.loc[country[0]]=country[1]['name'],int(country[1]['id'])

	df['Id'] = df['Id'].astype('int64')
	
	sum_list = []
	print('Please wait...')
	for ident in df['Id']:
		rank = requests.get(f'https://api.clashroyale.com/v1/locations/{ident}/rankings/players',
							headers={'Accept': "application/json",'Authorization': f'Bearer {api}'},
						    params={'limit':'100'}
							)
		
		content = json.loads(rank.text)
		try:
			content = content['items']
			print()
		except:
			print()
		
		n = 0
		for each in content:
			try:
				n += int(each['trophies'])
			except:
				print(f'Skipped {ident}')
		print(n)
		sum_list.append(n)
	

	# I would save this to a file

	# Create new row with sum
	df['Skill Count'] = sum_list

	# Remove regions without a ranking
	df_filtered = pd.DataFrame(df.values,columns=df.columns)

	for each in range(len(df_filtered['Skill Count'].values)):
		if df_filtered.loc[each][2]<50000:
			df_filtered.drop([each],inplace=True)

	df_filtered = df_filtered.reset_index(drop=True)



	# Optional
	choice = input('Scale? yes or no')
	
	if choice=='yes':
		to_be = df_filtered['Skill Count'].values.reshape(-1,1)

		ss = StandardScaler().fit(to_be)

		df_filtered['Skill Count'] = ss.transform(to_be)
	else:
		print('Wise Choice')

	# Now to visualise on map!

	mapp = folium.Map(location=[25,0],zoom_start=1.5)

	r = r'countries.geojson'

	folium.Choropleth(
		geo_data=r,
		data = df_filtered,
		key_on = 'feature.properties.ADMIN',
		columns=['Country','Skill Count'],
		fill_color='YlOrRd', 
		fill_opacity=0.7, 
		line_opacity=0.2,
		legend_name='Clash Royale "Skill" level',
		reset=True
	).add_to(mapp)

	display(mapp
	test = df_filtered['Skill Count']==62571

	for each in enumerate(test.values):
		if each[1]:
			print('Index:', each[0])
	print('Highest Country:', df_filtered['Country'].values[34])
	
main(input('Give API key'))

