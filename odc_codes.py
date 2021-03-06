# -*- coding: utf-8 -*-
"""ODC Codes

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VAoF3Yf74z1t5NdoCYW1Zpo7-HW5WSyA

### PRE-PROCESSING

Price and Arrival
"""

import pandas as pd

df = pd.read_csv("/content/drive/My Drive/Open Data Conclave - Hackathon/Prices and Arrival/Prices_Arrival_2013-18.csv") 
df['Report Date'] = pd.to_datetime(df['Report Date'])
df.tail()

import re
df['Commodity'] = df['Commodity'].apply(lambda s: ' '.join(i.title() for i in re.split(r'[()|.-]',s) if i.strip()))
df['Commodity'] = df['Commodity'].apply(lambda s: re.sub(' +', ' ',s))
df['Commodity'] = df['Commodity'].apply(lambda s: s.rstrip())

useful_commodities = ['Arhar Dal Tur Dal','Arhar Tur Red Gram Whole','Bajra Pearl Millet Cumbu','Barley Jau','Cotton', 'Cotton Seed','Groundnut','Jowar Sorghum','Jute', 'Jute Seed','Maize','Masur Dal','Lentil Masur Whole','Green Gram Dal Moong Dal','Green Gram Moong Whole','Mustard','Niger Seed Ramtil','Onion','Paddy Dhan','Paddy Dhan Basmati','Paddy Dhan Common','Potato','Ragi Finger Millet','Safflower','Sesamum Sesame Gingelly Til','Soyabean','Sugarcane','Black Gram Dal Urd Dal','Black Gram Urd Beans Whole','Wheat','Wheat Atta']
df_filtered = df[df['Commodity'].isin(useful_commodities)]
df_filtered['Modal Prices'] = pd.to_numeric(df_filtered['Modal Prices'],errors = 'coerce')
df_filtered['Report Date Year'] = df_filtered['Report Date'].dt.year

commodity_to_crop_code = {'Arhar Dal Tur Dal': 202,
 'Arhar Tur Red Gram Whole': 202,
 'Bajra Pearl Millet Cumbu': 103,
 'Barley Jau': 107,
 'Black Gram Dal Urd Dal': 203,
 'Black Gram Urd Beans Whole': 203,
 'Cotton': 1101,
 'Cotton Seed': 1101,
 'Green Gram Dal Moong Dal': 204,
 'Green Gram Moong Whole': 204,
 'Groundnut': 1001,
 'Jowar Sorghum': 102,
 'Jute': 1102,
 'Jute Seed': 1102,
 'Lentil Masur Whole': 205,
 'Maize': 104,
 'Masur Dal': 205,
 'Mustard': 1004,
 'Niger Seed Ramtil': 1010,
 'Onion': 708,
 'Paddy Dhan': 101,
 'Paddy Dhan Basmati': 101,
 'Paddy Dhan Common': 101,
 'Potato': 701,
 'Ragi Finger Millet': 105,
 'Safflower': 1008,
 'Sesamum Sesame Gingelly Til': 1003,
 'Soyabean': 1009,
 'Sugarcane': 401,
 'Wheat': 106,
 'Wheat Atta': 106}

crop_code_to_crop = {101: 'Paddy',
 102: 'Jowar',
 103: 'Bajra',
 104: 'Maize',
 105: 'Ragi',
 106: 'Wheat',
 107: 'Barley',
 201: 'Gram',
 202: 'Arhar,Redgram',
 203: 'Urad,Blackgram',
 204: 'Moong,Greengram',
 205: 'Masur,Lentil',
 208: 'Peas',
 401: 'Sugarcane',
 701: 'Potato',
 708: 'Onion',
 1001: 'Groundnut',
 1003: 'Sesamum',
 1004: 'Rapeseed & Mustard',
 1006: 'Coconut-1',
 1007: 'Sunflower',
 1008: 'Safflower',
 1009: 'Soyabean',
 1010: 'Nigerseed',
 1101: 'Cotton',
 1102: 'Jute'}

df_filtered['crop_code'] = df_filtered['Commodity'].replace(commodity_to_crop_code)

df_filtered['crop'] = df_filtered['crop_code'].replace(crop_code_to_crop)

df_filtered = df_filtered.drop(['Market_Code','Origin','Origin_Derived_State','Origin_Derived_District/City','Commodity','Report Date Year'],axis = 1)

df_filtered.columns = ['date','state_name','state_code','dist_name','dist_code','Market Center','Latitude','Longitude','Arrivals','Unit of Arrivals','Variety','Minimum Prices','Maximum Prices','Modal Prices','Unit of Price','crop_code','crop']

df_filtered['year'] = pd.to_datetime(df_filtered['date']).dt.year

na_dict = {-999.0 : None}
df_filtered["Modal Prices"] = df_filtered["Modal Prices"].replace(na_dict)
df_filtered["Minimum Prices"] = df_filtered["Minimum Prices"].replace(na_dict)
df_filtered["Maximum Prices"] = df_filtered["Maximum Prices"].replace(na_dict)

df_filtered['Modal Prices'] = pd.to_numeric(df_filtered['Modal Prices'],errors = 'coerce')
df_filtered['Minimum Prices'] = pd.to_numeric(df_filtered['Minimum Prices'],errors = 'coerce')
df_filtered['Maximum Prices'] = pd.to_numeric(df_filtered['Maximum Prices'],errors = 'coerce')

df_new = df_filtered.groupby(["year","state_code","dist_code","crop_code","crop"],as_index=False)["Modal Prices","Minimum Prices",'Maximum Prices','Latitude','Longitude'].mean()

import numpy as np

df_new['Latitude_T'] = (np.floor(df_new['Latitude']) + np.ceil(df_new['Latitude']))/2 
df_new['Longitude_T'] = (np.floor(df_new['Longitude']) + np.ceil(df_new['Longitude']))/2 

df_new['Latitude_R'] = round(df_new['Latitude']*4)/4
df_new['Longitude_R'] = round(df_new['Longitude']*4)/4

df_new

"""COC"""

coc_codebook = pd.ExcelFile("/content/drive/My Drive/Open Data Conclave - Hackathon/Cost of Cultivation/coc_codebook.xlsx")
crops = pd.read_excel(coc_codebook,'Sheet2',index_col='crop_code')

#Remove uncommon crops
a = [201,1006]
df = df[(df['year'] >= 2013)] 
df = df[~df['crop_code'].isin(a)]

crops = crops['crop'].to_dict()
crops

area = df['croparea_ha']

#Main product and by product
df['mainprd_rs_per_hectare'] = df['mainprd_rs']/area
df['byprd_rs_per_hectare'] = df['byprd_rs']/area

#Labour
df['human_labour_per_hectare'] = (df['famlab_rs'] + df['atchdlab_rs'] + df['casuallab_rs'])/area
df['animal_labour_per_hectare'] = (df['hrdanimllab_rs'] + df['ownanimllab_rs'])/area
df['machine_labour_per_hectare'] = (df['hrdmchn_rs'] + df['ownmchn_rs'])/area

df['total_labour_per_hectare'] = df['human_labour_per_hectare'] + df['animal_labour_per_hectare'] + df['machine_labour_per_hectare']

#Fetrilizers and Manure
df['fert_man_per_hectare'] = (df['fertk_rs'] + df['fertn_rs'] + df['fertp_rs'] + df['manure_rs'])/area

#irrigation charges
df['irrigation_charges_per_hectare'] = (df['ownirrimchn_rs'] +  df['hrdirrimchn_rs'] + df['canalandothirri_rs'])/area

#Seed
df['seed_per_hectare'] = df['seed_rs']/area

#insecticides
df['insecticides_per_hectare'] = df['insecticide_rs']/area

#Miscelaneous
df['misc_per_hectare'] = df['misc_rs']/area

#Operational_cost
df['operational_cost_per_hectare'] = df['total_labour_per_hectare'] + df['fert_man_per_hectare'] +df['irrigation_charges_per_hectare']  +  df['seed_per_hectare'] + df['insecticides_per_hectare'] + df['misc_per_hectare']


#For FIxed Cost
df['land_revenue_per_hectare'] = df['landrevenue_rs']/area
df['leased_rent_per_hectare'] = df['rpll_rs']/area
df['imputed_rent_per_hectare'] = df['imputedrent_rs']/area
df['depriciation_per_hectare'] = df['totaldepre_rs']/area
df['total_capital_per_hectare'] = df['totalcapital_rs']/area

#Fixed cost
df['fixed_cost_per_hectare'] = df['land_revenue_per_hectare'] + df['leased_rent_per_hectare'] + df['imputed_rent_per_hectare'] + df['depriciation_per_hectare'] + df['total_capital_per_hectare']

#Total coc
df['coc_per_hectare'] = df['operational_cost_per_hectare'] + df['fixed_cost_per_hectare']

coc = df.sort_values(['year','season','state_code','dist_code','crop_code','farmerid'])
coc

"""APY"""

apy = pd.read_csv("/content/drive/My Drive/Open Data Conclave - Hackathon/APY/APY_13_14_to_17_18.csv")

apy['Season'][(apy['Season'] != 'Kharif') & (apy['Season'] != 'Rabi')] = 3
apy['Season'][apy['Season'] == 'Kharif'] = 1
apy['Season'][apy['Season'] == 'Rabi'] = 2

#Common crops from COC
keys = list(df['crop_code'].unique())

apy = apy[apy['Crop_code'].isin(keys)]

apy['Year'] = apy['Year'].apply(lambda x: x.split('-')[0].strip())

apy = apy[['Year','Season','State_code','District_code','Crop_code','Area','Production','Yield']]

apy.columns = ['year','season','state_code','dist_code','crop_code','Area','Production','Yield']

apy['year'] = np.int64(apy['year'])
apy['dist_code'] = np.int64(apy['dist_code'])

apy

"""Ground Water"""

gg = pd.read_excel("/content/drive/My Drive/Open Data Conclave - Hackathon/Ground Water_Well Monitoring/WRIS_groundwater_well_1994_2017.xlsx")

gg['MONSOON'][gg['MONSOON'] == "'0"] = 0
gg['POSTMONSOONKHARIF'][gg['POSTMONSOONKHARIF'] == "'0"] = 0
gg['POSTMONSOONRABI'][gg['POSTMONSOONRABI'] == "'0"] = 0
gg['PREMONSOON'][gg['PREMONSOON'] == "'0"] = 0

gg['MONSOON'] = gg['MONSOON'].astype('float')
gg['POSTMONSOONKHARIF'] = gg['POSTMONSOONKHARIF'].astype('float')
gg['POSTMONSOONRABI'] = gg['POSTMONSOONRABI'].astype('float')
gg['PREMONSOON'] = gg['PREMONSOON'].astype('float')

import numpy as np

gg['LAT'] = (np.floor(gg['LAT']) + np.ceil(gg['LAT']))/2 
gg['LON'] = (np.floor(gg['LON']) + np.ceil(gg['LON']))/2 
gg = gg.fillna(0)

well_grouped = gg.fillna(0).groupby(['YEAR_OBS','LAT','LON'],as_index = False).mean()

well_grouped = well_grouped.rename(columns = {'YEAR_OBS': 'year','LAT': 'Latitude', 'LON': 'Longitude'})

well_grouped = well_grouped[well_grouped['year'] >= 2013]

well_grouped

""".GRD TO TXT TO CSV """

import os
import pandas as pd
import numpy as np
from tqdm import tqdm
import sys
import subprocess

def year_days(year):
  if (year % 4) == 0:
    if (year % 100) == 0:
        if (year % 400) == 0:
            k = 366
            #print("{0} is a leap year".format(year))
        else:
            k = 365
            #print("{0} is not a leap year".format(year))
    else:
        k = 366
        #print("{0} is a leap year".format(year))
  else:
    k = 365
    #print("{0} is not a leap year".format(year))

  return k 


def get_file_paths(path):
    
    file_paths = []
    
    file_names = os.listdir(path)
    for file_name in file_names:
      #print(os.path.join(path,file_name))
      file_paths.append(os.path.join(path,file_name))

    return file_paths


averageT = file_paths("/content/drive/My Drive/Open Data Conclave - Hackathon/Temperature/AverageT/")


for file_path in averageT:
  base=os.path.basename(file_path)
  year = int(os.path.splitext(base)[0][-4:])

  days = year_days(year)
  print(days)

  for day in range(1,days):

    prog1 = r'''

        #include<stdio.h>

          main()
          {  float t[31][31];
        int i,j ,k;
            FILE *fin,*fout;

            fin = fopen("'''

    prog2 = r'''","rb");   // Input file
            fout = fopen("/content/AverageT_txt/'''

    prog3 = r'''.TXT","w");     // Output file

            fprintf(fout,"Daily Tempereture for 15 April 1980\n");
            if(fin == NULL)
            {  printf("Can't open file");
                return 0;
            }
            if(fout == NULL)
            {  printf("Can't open file");
                return 0;
            }
            for(k=0 ; k<366 ; k++)
            {  fread(&t,sizeof(t),1,fin) ;
                if(k == '''
 
    prog4= r''')
                {  for(i=0 ; i < 31 ; i++)
              {  fprintf(fout,"\n") ;
                  for(j=0 ; j < 31 ; j++)
                      fprintf(fout,"%6.2f",t[i][j]);
                  }
                }  
            }  
            fclose(fin);
            fclose(fout);
            return 0;
          } /* end of main */
          '''

    prog = prog1 + file_path + prog2 + os.path.splitext(base)[0] + r'''_''' + str(day) + prog3 + str(day) + prog4
    print(prog)

    if os.path.exists('foo'):
      os.remove("foo")
      os.remove("foo.c")   
      f = open('foo.c', 'w')
      f.write(prog)
      f.close()
      subprocess.call(["gcc", "foo.c", "-ofoo", "-std=c99", '-w', '-Ofast'])
      subprocess.call(["./foo"], stdin = sys.stdin)

    else:
      f = open('foo.c', 'w')
      f.write(prog)
      f.close()
      subprocess.call(["gcc", "foo.c", "-ofoo", "-std=c99", '-w', '-Ofast'])
      subprocess.call(["./foo"], stdin = sys.stdin)


longitudes = []
for i in range(0,31):
  longitudes.append(str(67.5 + i))


lattitudes = np.arange(7.5,38.5,1)


import pandas as pd
#longitudes = np.arange(67.5,98.5,1)
not_working_filepaths = []
years = range(2010,2018)
mean_t = pd.DataFrame()
for year in tqdm(years):
  for day in tqdm(range(0,365)):
    try:
      file_path = "/content/drive/My Drive/odc/temp/mean_t/MeanT_"+str(year)+"_"+str(day+1)+".TXT"
      d = pd.read_csv(file_path, sep=" ", header=None,names=list(range(0,71)))
      #d = d.drop(0,1)
      if d[70].isnull().values.sum() < 31:
        print("Didn't work for this file")
        not_working_filepaths.append(file_path)
        continue

      d = d.apply(lambda x: pd.Series(x.dropna().values),axis = 1) 

      print(d.shape)

      d.columns = longitudes
      d = d.set_index(lattitudes)
      d = d.unstack().reset_index()
      d['year'] = year
      d['day'] = day+1
      mean_t = pd.concat([mean_t,d])

    except:
      print(file_path+" did not work")
      not_working_filepaths.append(file_path)

print(not_working_filepaths)  


rainfall = file_paths("/content/drive/My Drive/Open Data Conclave - Hackathon/Rainfall/")
# /content/drive/My Drive/odc/rainfall

for file_path in tqdm(rainfall):

  prog1 = r'''
  #include<stdio.h>
  main()
  {   float rf[135][129],rainfall;
      float lo[135], la[129] ;
    int i, j, k, year, year1, month, date, nd ;
      FILE *fptr1,*fptr2;
      int	nd1[13] = {0,31,28,31,30,31,30,31,31,30,31,30,31} ;
    int nd2[13] = {0,31,29,31,30,31,30,31,31,30,31,30,31} ;

      year = 2013 ;
      printf("Year = %d",year) ;

      fptr1 = fopen("'''
      
  prog2=r'''","rb");   // input file
  fptr2 = fopen("/content/drive/My Drive/odc/rainfall/'''
  
  prog3=r'''.TXT","w");

  if(fptr1==NULL) {    printf("Can't open file");         return 0;    }
  if(fptr2==NULL) {    printf("Can't open file");         return 0;    }

  for(j=0 ; j < 135 ; j++) lo[j] = 66.5 + j * 0.25 ;
  for(j=0 ; j < 129 ; j++) la[j] =  6.5 + j * 0.25 ;

  year1 = year / 4 ;
  year1 = year1 * 4 ;

  for(month=1 ; month < 13 ; month++)
  {   nd = nd1[month] ;
      if(year == year1)nd = nd2[month] ;
      for(date=1 ; date <= nd ; date++)
  {   fprintf(fptr2,"\n%02d%02d%04d\n",date,month,year);
          for(i=0 ; i < 129 ; i++)
        {   fprintf(fptr2,"\n%8.2f,",la[i])  ;
              for(j=0 ; j < 135 ; j++)
            {   if(fread(&rainfall,sizeof(rainfall),1,fptr1) != 1) return 0 ;
                rf[j][i]  = rainfall ;
        fprintf(fptr2,"%7.1f,",rf[j][i] );
        }
          }
      printf("%4d %02d %02d \n",year,month,date);
      }
  }
  fclose(fptr1);
  fclose(fptr2);
  printf("Year = %d",year) ;
  return 0;
  }    /* end of main */

  '''

  base=os.path.basename(file_path)
  prog = prog1 + file_path + prog2 + os.path.splitext(base)[0] + prog3
  #print(prog)

  if os.path.exists('foo'):
    os.remove("foo")
    os.remove("foo.c")   
    f = open('foo.c', 'w')
    f.write(prog)
    f.close()
    subprocess.call(["gcc", "foo.c", "-ofoo", "-std=c99", '-w', '-Ofast'])
    subprocess.call(["./foo"], stdin = sys.stdin)

  else:
    f = open('foo.c', 'w')
    f.write(prog)
    f.close()
    subprocess.call(["gcc", "foo.c", "-ofoo", "-std=c99", '-w', '-Ofast'])
    subprocess.call(["./foo"], stdin = sys.stdin)



import numpy as np

rainfall_txts = get_file_paths("/content/drive/My Drive/odc/rainfall/")
longitudes = np.arange(66.5,100.25,0.25)
data = pd.DataFrame()

for file_path in tqdm(rainfall_txts[-9:-6]):
  if file_path.endswith('.TXT'):
    try:
      base=os.path.basename(file_path)
      #year = int(base.split('_')[0][3:])
      y = int(base.split('_')[0][3:])
      days = year_days(y)

      for i in tqdm(range(0,days)):
        

        df = pd.read_csv(file_path,nrows=129,skiprows=3 + 131 * i,header=None,index_col=0,engine='python')
        df = df.drop(136,1)
        df.columns = longitudes
        df = df.unstack()
        df = pd.DataFrame(df)
        df['year'] = y
        df['day'] = i+1
        data = pd.concat([data,df])
    except:
      print(file_path + " could not be read completely")

data

import pandas as pd
mean = pd.read_csv('/content/drive/My Drive/odc/mean_t_1990_2018.csv',index_col=[0])
mean.columns = ['long','lat','mean_t','year','day']
mean['date'] = pd.to_datetime(mean['year'] * 1000 + mean['day'], format='%Y%j')
seasons = [2, 2, 2, 3, 3, 3, 1, 1, 1, 1, 2, 2]
month_to_season = dict(zip(range(1,13), seasons))
mean['season'] = mean.date.dt.month.map(month_to_season)
mean = mean.groupby(['year','long','lat','season'],as_index=False)['mean_t'].mean()
mean.columns = ['year','Longitude','Latitude','season','mean_t']
mean = mean.sort_values(['Longitude','Latitude','season','year']).reset_index()  
import numpy as np
for j in range(1,7):
  mean['mean_t_'+str(j)] = np.zeros(len(mean))
  for i in range(0,len(mean)-j):
    if((mean['season'][i] == mean['season'][i+j])):
      mean['mean_t_'+str(j)][i+j] = mean['mean_t'][i]

mean = mean.drop('index',1)
mean.rename(columns = {'Longitude':'Longitude_T','Latitude':'Latitude_T'},inplace=True)


pa = pd.read_csv('/content/drive/My Drive/odc/Final/price_and_arrival_aggregated.csv')
coc_codebook = pd.ExcelFile("/content/drive/My Drive/Open Data Conclave - Hackathon/Cost of Cultivation/coc_codebook.xlsx")
crops = pd.read_excel(coc_codebook,'Sheet2',index_col='crop_code')
df = pd.read_csv('/content/drive/My Drive/Open Data Conclave - Hackathon/Cost of Cultivation/Cost of Cultivation_2005_2016 .csv')
#Remove uncommon crops
a = [201,1006]
#df = df[(df['year'] >= 2013)] 
df = df[~df['crop_code'].isin(a)]

crops = crops['crop'].to_dict()
crops

area = df['croparea_ha']

#Main product and by product
df['mainprd_rs_per_hectare'] = df['mainprd_rs']/area
df['byprd_rs_per_hectare'] = df['byprd_rs']/area

#Labour
df['human_labour_per_hectare'] = (df['famlab_rs'] + df['atchdlab_rs'] + df['casuallab_rs'])/area
df['animal_labour_per_hectare'] = (df['hrdanimllab_rs'] + df['ownanimllab_rs'])/area
df['machine_labour_per_hectare'] = (df['hrdmchn_rs'] + df['ownmchn_rs'])/area

df['total_labour_per_hectare'] = df['human_labour_per_hectare'] + df['animal_labour_per_hectare'] + df['machine_labour_per_hectare']

#Fetrilizers and Manure
df['fert_man_per_hectare'] = (df['fertk_rs'] + df['fertn_rs'] + df['fertp_rs'] + df['manure_rs'])/area

#irrigation charges
df['irrigation_charges_per_hectare'] = (df['ownirrimchn_rs'] +  df['hrdirrimchn_rs'] + df['canalandothirri_rs'])/area

#Seed
df['seed_per_hectare'] = df['seed_rs']/area

#insecticides
df['insecticides_per_hectare'] = df['insecticide_rs']/area

#Miscelaneous
df['misc_per_hectare'] = df['misc_rs']/area

#Operational_cost
df['operational_cost_per_hectare'] = df['total_labour_per_hectare'] + df['fert_man_per_hectare'] +df['irrigation_charges_per_hectare']  +  df['seed_per_hectare'] + df['insecticides_per_hectare'] + df['misc_per_hectare']


#For FIxed Cost
df['land_revenue_per_hectare'] = df['landrevenue_rs']/area
df['leased_rent_per_hectare'] = df['rpll_rs']/area
df['imputed_rent_per_hectare'] = df['imputedrent_rs']/area
df['depriciation_per_hectare'] = df['totaldepre_rs']/area
df['total_capital_per_hectare'] = df['totalcapital_rs']/area

#Fixed cost
df['fixed_cost_per_hectare'] = df['land_revenue_per_hectare'] +df['leased_rent_per_hectare'] +df['imputed_rent_per_hectare'] + df['depriciation_per_hectare'] +df['total_capital_per_hectare']

#Total coc
df['coc_per_hectare'] = df['operational_cost_per_hectare'] + df['fixed_cost_per_hectare']

coc = df.sort_values(['year','season','state_code','dist_code','crop_code','farmerid'])
coc


pa['dist_code'] = pa['dist_code'].astype(int)
latlon = pa[['dist_code','Latitude_T','Longitude_T']].drop_duplicates()
coc = pd.merge(coc,latlon,on = ['dist_code'],how = 'left')
coc = coc[coc['Latitude_T'] != 9.]
coc = coc[coc['Latitude_T'].isna() != True]

df = coc[['state_name','state_code','dist_code','dist_name','crop_code','block','year','total_labour_per_hectare','operational_cost_per_hectare','total_capital_per_hectare','fixed_cost_per_hectare','coc_per_hectare','Latitude_T','Longitude_T','season']]

final1 = pd.merge(df,mean,on = ['year','Longitude_T','Latitude_T','season'],how = 'left')

rainfall = pd.read_csv('/content/drive/My Drive/odc/Final/new_final.csv',index_col = [0])
rainfall1 = pd.read_csv('/content/drive/My Drive/odc/rainfall_combined.csv',index_col = [0])
rainfall2 = pd.read_csv('/content/drive/My Drive/odc/rainfall_2004_2009.csv',index_col = [0])
rainfall3 = pd.read_csv('/content/drive/My Drive/odc/rainfall_1999_2003.csv',index_col = [0])

rainfall = rainfall.reset_index()
rainfall3 = rainfall3.reset_index()
rainfall2 = rainfall2.reset_index()

rainfall.columns = ['long','lat','rainfall','year','day']
rainfall1.columns = ['long','lat','rainfall','year','day']
rainfall2.columns = ['long','lat','rainfall','year','day']
rainfall3.columns = ['long','lat','rainfall','year','day']

rainfall_full = pd.concat([rainfall,rainfall1,rainfall2,rainfall3])

rainfall_full = rainfall_full[rainfall_full['year'] > 1998]

rainfall_full.columns = ['long','lat','rainfall','year','day']
rainfall_full = rainfall_full[rainfall_full['rainfall'] != -999.0]
rainfall_full['date'] = pd.to_datetime(rainfall_full['year'] * 1000 + rainfall_full['day'], format='%Y%j')

seasons = [2, 2, 2, 3, 3, 3, 1, 1, 1, 1, 2, 2]
month_to_season = dict(zip(range(1,13), seasons))
rainfall_full['season'] = rainfall_full.date.dt.month.map(month_to_season)

rainfall_full = rainfall_full.groupby(['year','long','lat','season'],as_index=False)['rainfall'].mean()
rainfall_full.columns = ['year','Longitude','Latitude','season','rainfall']
rainfall_full = rainfall_full.sort_values(['Longitude','Latitude','season','year']).reset_index() 

for j in range(1,7):
  rainfall_full['rainfall_'+str(j)] = np.zeros(len(rainfall_full))
  for i in range(0,len(rainfall_full)-j):
    if((rainfall_full['season'][i] == rainfall_full['season'][i+j])):
      rainfall_full['rainfall_'+str(j)][i+j] = rainfall_full['rainfall'][i] 


pa['dist_code'] = pa['dist_code'].astype(int)
latlon_R = pa[['dist_code','Latitude_R','Longitude_R']].drop_duplicates()


final2 = pd.merge(final1,latlon_R,on = ['dist_code'],how = 'left')
#final2 = final2[final2['Latitude_T'] != 9.]
final2 = final2[final2['Latitude_R'].isna() != True]

rainfall_full = rainfall_full.rename(columns = {'Longitude':'Longitude_R','Latitude':'Latitude_R'})

coc_fullandfinal = pd.merge(final2,rainfall_full,on = ['year','Longitude_R','Latitude_R','season'])

"""### MODEL FITTING"""

import pandas as pd
df = pd.read_csv('/content/drive/My Drive/odc/Final/coc_fullandfinal_individual_predictions.csv',index_col = [0])

df = df[['state_name','dist_name','crop_code','year','season','total_labour_per_hectare','fert_man_per_hectare','irrigation_charges_per_hectare','seed_per_hectare','total_capital_per_hectare','']]
df = df.groupby(['state_name','dist_name','crop_code','block','year','season'],as_index=False).mean()

import numpy as np
df = df[df['total_capital_per_hectare'] != np.inf]

cols = ['state_name','dist_name','crop_code','season']
for i in cols:
  df = df.join(pd.get_dummies(df[i]))
  df.drop(i,1,inplace=True)

df['seed_fert_man_per_hectare'] = df['seed_per_hectare'] + df['fert_man_per_hectare']
df = df.drop(['seed_per_hectare','fert_man_per_hectare'],1)
columns = ['total_capital_per_hectare', 'total_labour_per_hectare', 'seed_fert_man_per_hectare', 'irrigation_charges_per_hectare']


x_train = df[df['year'] < 2015].drop(columns,1)
y_train = df[df['year'] < 2015][columns]

x_test = df[df['year'] > 2015].drop(columns,1)
y_test = df[df['year'] > 2015][columns]


from sklearn.ensemble import VotingRegressor
from lightgbm import LGBMRegressor
from sklearn.linear_model import LinearRegression
import xgboost as xgb
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import ExtraTreesRegressor

models = [LinearRegression(),
          LGBMRegressor(verbose = 1,n_estimators=1000),
          xgb.XGBRegressor(n_jobs = -1,verbose = 1,n_estimators=1000),
          RandomForestRegressor(n_jobs = -1,verbose = 1,n_estimators=1000),
          ExtraTreesRegressor(n_jobs = -1,verbose = 1,n_estimators=1000)]

models_ens = list(zip(['LR', 'lgbm', 'XGB','RF','XT'], models))
model_ens = VotingRegressor(estimators = models_ens,n_jobs = -1)
model_ens.fit(x_train, y_train['total_capital_per_hectare'])