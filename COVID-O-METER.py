from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import time
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import pandas as pd 
from difflib import get_close_matches

#DATA EXTRACTION BY WEB SCRAPING USING BEAUTIFUL SOUP
#-------------------------------------------------------------------------------------------------------------------------------#

page_link=requests.get('https://www.worldometers.info/coronavirus/')
soup_object=BeautifulSoup(page_link.content, 'html.parser')
soup_object2=soup_object.find(id='main_table_countries_today')
rows=soup_object2.find_all('tr')

column=[v.get_text() for v in rows[0].find_all('th')]

covid_list=[]
country_list=[]

for i in range(1,len(rows)):
    row_data=[x.get_text().replace("\n", "") for x in rows[i].find_all('td')] 
    individual_dic={}
    country_list.append(row_data[1]) 
    individual_dic['Country']=row_data[1].rstrip()
    individual_dic['Total Cases']=row_data[2].rstrip()
    individual_dic['New Cases']=row_data[3].rstrip()
    individual_dic['Total Deaths']=row_data[4].rstrip()
    individual_dic['Total Recovered']=row_data[6].rstrip()
    covid_list.append(individual_dic)
    
covid_df=pd.DataFrame(covid_list, columns=['Country', 'Total Cases','New Cases','Total Deaths','Total Recovered'], index=country_list)

page_link_india=requests.get('https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_India')
soup_object=BeautifulSoup(page_link_india.content, 'html.parser') 
my_table=soup_object.find(id='covid19-container')
rows=my_table.find_all('tr')
list1=[]
for x in rows:
    list1.append(x.get_text())

states_list=[]
india_covid_list=[]

for i in range(2,len(rows)-2):
    row_heading=[x.get_text() for x in rows[i].find_all('th')]
    states_list.append(row_heading)

total_stats=states_list[0] 
states_list.pop(0)

data=[]
for i in range(2,len(rows)-2):
    row_data=[x.get_text() for x in rows[i].find_all('td')]
    data.append(row_data)

data.pop(0)

for i in range(0,36):
    state_dic={}
    state_dic['State']=states_list[i][0].replace("\n","").rstrip()
    state_dic['Total Cases']=data[i][0].replace("\n","").rstrip().replace("[a]","").replace("[b]","")
    state_dic['Deaths']=data[i][1].replace("\n","").rstrip().replace("[a]","").replace("[b]","")
    state_dic['Total Recovered']=data[i][2].replace("\n","").rstrip().replace("[a]","").replace("[b]","")
    state_dic['Active Cases']=data[i][3].replace("\n","").rstrip().replace("[a]","").replace("[b]","")
    india_covid_list.append(state_dic)

state_dic1={}
state_dic1['State']="India"
state_dic1['Total Cases']=total_stats[1].replace("\n","").rstrip().replace("*","")
state_dic1['Deaths']=total_stats[2].replace("\n","").rstrip()
state_dic1['Total Recovered']=total_stats[3].replace("\n","").rstrip()
state_dic1['Active Cases']=total_stats[4].replace("\n","").rstrip()
india_covid_list.append(state_dic1)

india_covid_df=pd.DataFrame(india_covid_list, columns=['State', 'Total Cases','Deaths','Total Recovered','Active Cases'])
india_covid_df=india_covid_df.set_index('State')

#GUI
#------------------------------------------------------------------------------------------------------------------------------------#

root=Tk()
root.title("COVID-O-METER")
root.geometry("1000x1000")
root.iconbitmap(r"C:\Users\riyan\OneDrive\Desktop\COVID-O-METER\virus.ico")

covid_notebook=ttk.Notebook(root)
covid_notebook.pack()

live_updates_frame=Frame(covid_notebook, width=1000, height=1000, bg="#e3fdfd" )
live_updates_frame.pack(fill="both", expand=1)
local_frame=Frame(covid_notebook, width=1000, height=1000, bg="#e3fdfd")
local_frame.pack(fill="both", expand=1)
search_frame=Frame(covid_notebook, width=1000, height=1000, bg="#e3fdfd")
search_frame.pack(fill="both", expand=1)
answer_frame=Frame(covid_notebook, height=1000, width=1000, bg="#e3fdfd")
answer_frame.pack(fill="both", expand=1)
faq_frame=Frame(covid_notebook,height=1000, width=1000, bg="#e3fdfd")
faq_frame.pack(fill="both", expand=1)

covid_notebook.add(live_updates_frame, text="COVID-19 Live Updates")
covid_notebook.add(local_frame, text="COVID-19 India")
covid_notebook.add(faq_frame, text="Frequently Asked Questions")
covid_notebook.add(search_frame, text="Search")
covid_notebook.add(answer_frame, text="Search Results")
covid_notebook.hide(4)

#All continent windows

def north_america():
    north_america1=Tk()
    north_america1.geometry("400x400")
    north_america1.iconbitmap(r"C:\Users\riyan\Downloads\favicon (2).ico")
    north_america1.title("North America")
    north_america1.config(bg="#d3f4ff")

    north_america_updates_canvas=Canvas(north_america1, height=200, width=400, bg="#d3f4ff", bd=0, highlightthickness=0, relief='ridge')
    north_america_updates_canvas.grid()
    north_america_updates_canvas.create_rectangle(10,20,390,193, fill="#d3f4ff",outline="black", width=3)
    
    north_america_total_cases=covid_df.loc['North America','Total Cases']
    north_america_total_recovered=covid_df.loc['North America', 'Total Recovered']
    north_america_total_deaths=covid_df.loc['North America' ,'Total Deaths']
    north_america_new_cases=covid_df.loc['North America', 'New Cases']

    north_america_updates_canvas.create_text(200,40, text="Total Cases: " + str(north_america_total_cases), font=('Helvetica', 18, 'bold'), fill="black", tag="delete_text")
    north_america_updates_canvas.create_text(200,80, text="Total Recovered: " + str(north_america_total_recovered), font=('Helvetica', 18, 'bold'), fill="green", tag="delete_text")
    north_america_updates_canvas.create_text(200,120, text="Total Deaths: " + str(north_america_total_deaths), font=('Helvetica', 18, 'bold'), fill="black", tag="delete_text")
    north_america_updates_canvas.create_text(200,160, text="New Cases: " + str(north_america_new_cases), font=('Helvetica', 18, 'bold'), fill="red",tag="delete_text")
    
    def selected_option_north_america(event):
        option_selected=north_america_combo.get()
        north_america_updates_canvas.delete("delete_text")

        selected_country_total_cases=covid_df.loc[option_selected, 'Total Cases']
        selected_country_total_recovered=covid_df.loc[option_selected, 'Total Recovered']
        selected_country_total_deaths=covid_df.loc[option_selected, 'Total Deaths']
        selected_country_new_cases=covid_df.loc[option_selected,'New Cases']

        north_america_updates_canvas.create_text(200,50, text="Total Cases: " + str(selected_country_total_cases), font=('Helvetica', 18, 'bold'), fill="black", tag="delete_text")
        north_america_updates_canvas.create_text(200,90, text="Total Recovered: " + str(selected_country_total_recovered), font=('Helvetica', 18, 'bold'), fill="green", tag="delete_text")
        north_america_updates_canvas.create_text(200,130, text="Total Deaths: " + str(selected_country_total_deaths), font=('Helvetica', 18, 'bold'), fill="black", tag="delete_text")
        north_america_updates_canvas.create_text(200,170, text="New Cases: " + str(selected_country_new_cases), font=('Helvetica', 18, 'bold'), fill="red",tag="delete_text")


    north_america_countries_list=["North America","USA","Mexico","Canada","Dominican Republic","Panama","Guatemala", "Honduras","Haiti","El Salvador","Cuba","Costa Rica",
    "Nicaragua","Jamaica","Martinique","Guadeloupe","Cayman Islands","Bermuda","Trinidad and Tobago","Bahamas","Aruba","Barbados","Sint Maarten","Saint Martin",
    "St. Vincent Grenadines","Antigua and Barbuda","Grenada","Curaçao","Belize","Saint Lucia","Dominica","Saint Kitts and Nevis","Greenland","Turks and Caicos",
    "Montserrat","British Virgin Islands","Caribbean Netherlands","St. Barth","Anguilla","Saint Pierre Miquelon"]

    select_country_label=Label(north_america1, text="Select Country", bg="#d3f4ff", font=('Helvetica',12,'bold','underline'), fg="#084177")
    select_country_label.grid(pady=20)

    north_america_combo=ttk.Combobox(north_america1, value=north_america_countries_list, state='readonly', width=30, height=6)
    north_america_combo.current(0)
    north_america_combo.bind("<<ComboboxSelected>>", selected_option_north_america)
    north_america_combo.grid()

    
    north_america1.mainloop()

def south_america():
    south_america1=Tk()
    south_america1.geometry("400x400")
    south_america1.iconbitmap(r"C:\Users\riyan\Downloads\favicon (2).ico")
    south_america1.title("South America")
    south_america1.config(bg="#d3f4ff")

    south_america_updates_canvas=Canvas(south_america1, height=200, width=400, bg="#d3f4ff",bd=0, highlightthickness=0, relief='ridge')
    south_america_updates_canvas.grid()
    south_america_updates_canvas.create_rectangle(10,20,390,193, fill="#d3f4ff",outline="black", width=3)
    
    south_america_total_cases=covid_df.loc['South America','Total Cases']
    south_america_total_recovered=covid_df.loc['South America', 'Total Recovered']
    south_america_total_deaths=covid_df.loc['South America' ,'Total Deaths']
    south_america_new_cases=covid_df.loc['South America', 'New Cases']

    south_america_updates_canvas.create_text(200,50, text="Total Cases: " + str(south_america_total_cases), font=('Helvetica', 18, 'bold'), fill="black", tag="delete_text")
    south_america_updates_canvas.create_text(200,90, text="Total Recovered: " + str(south_america_total_recovered), font=('Helvetica', 18, 'bold'), fill="green", tag="delete_text")
    south_america_updates_canvas.create_text(200,130, text="Total Deaths: " + str(south_america_total_deaths), font=('Helvetica', 18, 'bold'), fill="black", tag="delete_text")
    south_america_updates_canvas.create_text(200,170, text="New Cases: " + str(south_america_new_cases), font=('Helvetica', 18, 'bold'), fill="red",tag="delete_text")
    
    def selected_option_south_america(event):
        option_selected=south_america_combo.get()
        south_america_updates_canvas.delete("delete_text")

        selected_country_total_cases=covid_df.loc[option_selected, 'Total Cases']
        selected_country_total_recovered=covid_df.loc[option_selected, 'Total Recovered']
        selected_country_total_deaths=covid_df.loc[option_selected, 'Total Deaths']
        selected_country_new_cases=covid_df.loc[option_selected,'New Cases']

        south_america_updates_canvas.create_text(200,50, text="Total Cases: " + str(selected_country_total_cases), font=('Helvetica', 18, 'bold'), fill="black", tag="delete_text")
        south_america_updates_canvas.create_text(200,90, text="Total Recovered: " + str(selected_country_total_recovered), font=('Helvetica', 18, 'bold'), fill="green", tag="delete_text")
        south_america_updates_canvas.create_text(200,130, text="Total Deaths: " + str(selected_country_total_deaths), font=('Helvetica', 18, 'bold'), fill="black", tag="delete_text")
        south_america_updates_canvas.create_text(200,170, text="New Cases: " + str(selected_country_new_cases), font=('Helvetica', 18, 'bold'), fill="red",tag="delete_text")


    south_america_countries_list=["South America","Brazil","Peru","Chile","Ecuador","Colombia","Argentina","Bolivia","Venezuela","Paraguay","Uruguay","French Guiana","Guyana","Suriname","Falkland Islands"]

    select_country_label=Label(south_america1, text="Select Country", bg="#d3f4ff", font=('Helvetica',12,'bold','underline'), fg="#084177")
    select_country_label.grid(pady=20)
    
    south_america_combo=ttk.Combobox(south_america1, value=south_america_countries_list, state='readonly',width=30,height=6)
    south_america_combo.current(0)
    south_america_combo.bind("<<ComboboxSelected>>", selected_option_south_america)
    south_america_combo.grid()

    south_america1.mainloop()

def asia():
    asia1=Tk()
    asia1.geometry("400x400")
    asia1.iconbitmap(r"C:\Users\riyan\Downloads\favicon (2).ico")
    asia1.title("Asia")
    asia1.config(bg="#d3f4ff")

    asia_updates_canvas=Canvas(asia1, height=200, width=400, bg="#d3f4ff",bd=0, highlightthickness=0, relief='ridge')
    asia_updates_canvas.grid()
    asia_updates_canvas.create_rectangle(10,20,390,193, fill="#d3f4ff",outline="black", width=3)
    
    asia_total_cases=covid_df.loc['Asia','Total Cases']
    asia_total_recovered=covid_df.loc['Asia', 'Total Recovered']
    asia_total_deaths=covid_df.loc['Asia' ,'Total Deaths']
    asia_new_cases=covid_df.loc['Asia', 'New Cases']

    asia_updates_canvas.create_text(200,50, text="Total Cases: " + str(asia_total_cases), font=('Helvetica', 18, 'bold'), fill="black", tag="delete_text")
    asia_updates_canvas.create_text(200,90, text="Total Recovered: " + str(asia_total_recovered), font=('Helvetica', 18, 'bold'), fill="green", tag="delete_text")
    asia_updates_canvas.create_text(200,130, text="Total Deaths: " + str(asia_total_deaths), font=('Helvetica', 18, 'bold'), fill="black", tag="delete_text")
    asia_updates_canvas.create_text(200,170, text="New Cases: " + str(asia_new_cases), font=('Helvetica', 18, 'bold'), fill="red",tag="delete_text")
    
    def selected_option_asia(event):
        option_selected=asia_combo.get()
        asia_updates_canvas.delete("delete_text")

        selected_country_total_cases=covid_df.loc[option_selected, 'Total Cases']
        selected_country_total_recovered=covid_df.loc[option_selected, 'Total Recovered']
        selected_country_total_deaths=covid_df.loc[option_selected, 'Total Deaths']
        selected_country_new_cases=covid_df.loc[option_selected,'New Cases']

        asia_updates_canvas.create_text(200,50, text="Total Cases: " + str(selected_country_total_cases), font=('Helvetica', 18, 'bold'), fill="black", tag="delete_text")
        asia_updates_canvas.create_text(200,90, text="Total Recovered: " + str(selected_country_total_recovered), font=('Helvetica', 18, 'bold'), fill="green", tag="delete_text")
        asia_updates_canvas.create_text(200,130, text="Total Deaths: " + str(selected_country_total_deaths), font=('Helvetica', 18, 'bold'), fill="black", tag="delete_text")
        asia_updates_canvas.create_text(200,170, text="New Cases: " + str(selected_country_new_cases), font=('Helvetica', 18, 'bold'), fill="red",tag="delete_text")


    asia_countries_list=["Asia","India","Iran","Turkey","Saudi Arabia","Pakistan","China","Qatar","Bangladesh","UAE","Singapore","Kuwait","Indonesia","Philippines","Afghanistan","Israel",
    "Oman","Japan","Bahrain","Iraq","Armenia","Kazakhstan","S. Korea","Malaysia","Azerbaijan","Tajikistan","Uzbekistan","Nepal","Thailand","Kyrgyzstan","Maldives","Sri Lanka","Lebanon",
    "Hong Kong","Cyprus","Jordan","Georgia","Yemen","Palestine","Taiwan","Vietnam","Myanmar","Mongolia","Syria","Brunei ","Cambodia","Bhutan","Macao","Timor-Leste","Laos"]

    select_country_label=Label(asia1, text="Select Country", bg="#d3f4ff", font=('Helvetica',12,'bold','underline'), fg="#084177")
    select_country_label.grid(pady=20)
    
    asia_combo=ttk.Combobox(asia1, value=asia_countries_list, state='readonly', width=30, height=6)
    asia_combo.current(0)
    asia_combo.bind("<<ComboboxSelected>>", selected_option_asia)
    asia_combo.grid()

    asia1.mainloop()


def oceania():
    oceania1=Tk()
    oceania1.geometry("400x400")
    oceania1.iconbitmap(r"C:\Users\riyan\Downloads\favicon (2).ico")
    oceania1.title("Oceania")
    oceania1.config(bg="#d3f4ff")

    oceania_updates_canvas=Canvas(oceania1, height=200, width=400, bg="#d3f4ff",bd=0, highlightthickness=0, relief='ridge')
    oceania_updates_canvas.grid()
    oceania_updates_canvas.create_rectangle(10,20,390,193, fill="#d3f4ff",outline="black", width=3)
    
    oceania_total_cases=covid_df.loc['Oceania','Total Cases']
    oceania_total_recovered=covid_df.loc['Oceania', 'Total Recovered']
    oceania_total_deaths=covid_df.loc['Oceania' ,'Total Deaths']
    oceania_new_cases=covid_df.loc['Oceania', 'New Cases']

    oceania_updates_canvas.create_text(200,50, text="Total Cases: " + str(oceania_total_cases), font=('Helvetica', 18, 'bold'), fill="black", tag="delete_text")
    oceania_updates_canvas.create_text(200,90, text="Total Recovered: " + str(oceania_total_recovered), font=('Helvetica', 18, 'bold'), fill="green", tag="delete_text")
    oceania_updates_canvas.create_text(200,130, text="Total Deaths: " + str(oceania_total_deaths), font=('Helvetica', 18, 'bold'), fill="black", tag="delete_text")
    oceania_updates_canvas.create_text(200,170, text="New Cases: " + str(oceania_new_cases), font=('Helvetica', 18, 'bold'), fill="red",tag="delete_text")
    
    def selected_option_oceania(event):
        option_selected=oceania_combo.get()
        oceania_updates_canvas.delete("delete_text")

        selected_country_total_cases=covid_df.loc[option_selected, 'Total Cases']
        selected_country_total_recovered=covid_df.loc[option_selected, 'Total Recovered']
        selected_country_total_deaths=covid_df.loc[option_selected, 'Total Deaths']
        selected_country_new_cases=covid_df.loc[option_selected,'New Cases']

        oceania_updates_canvas.create_text(200,50, text="Total Cases: " + str(selected_country_total_cases), font=('Helvetica', 18, 'bold'), fill="black", tag="delete_text")
        oceania_updates_canvas.create_text(200,90, text="Total Recovered: " + str(selected_country_total_recovered), font=('Helvetica', 18, 'bold'), fill="green", tag="delete_text")
        oceania_updates_canvas.create_text(200,130, text="Total Deaths: " + str(selected_country_total_deaths), font=('Helvetica', 18, 'bold'), fill="black", tag="delete_text")
        oceania_updates_canvas.create_text(200,170, text="New Cases: " + str(selected_country_new_cases), font=('Helvetica', 18, 'bold'), fill="red",tag="delete_text")


    oceania_countries_list=["Oceania","Australia","New Zealand","French Polynesia","New Caledonia","Fiji","Papua New Guinea"]

    select_country_label=Label(oceania1, text="Select Country", bg="#d3f4ff", font=('Helvetica',12,'bold','underline'), fg="#084177")
    select_country_label.grid(pady=20)

    oceania_combo=ttk.Combobox(oceania1, value=oceania_countries_list, state='readonly', width=30, height=6)
    oceania_combo.current(0)
    oceania_combo.bind("<<ComboboxSelected>>", selected_option_oceania)
    oceania_combo.grid()

    
    oceania1.mainloop()


def europe():
    europe1=Tk()
    europe1.geometry("400x400")
    europe1.iconbitmap(r"C:\Users\riyan\Downloads\favicon (2).ico")
    europe1.title("Europe")
    europe1.config(bg="#d3f4ff")

    europe_updates_canvas=Canvas(europe1, height=200, width=400, bg="#d3f4ff",bd=0, highlightthickness=0, relief='ridge')
    europe_updates_canvas.grid()
    europe_updates_canvas.create_rectangle(10,20,390,193, fill="#d3f4ff",outline="black", width=3)
    
    europe_total_cases=covid_df.loc['Europe','Total Cases']
    europe_total_recovered=covid_df.loc['Europe', 'Total Recovered']
    europe_total_deaths=covid_df.loc['Europe' ,'Total Deaths']
    europe_new_cases=covid_df.loc['Europe', 'New Cases']

    europe_updates_canvas.create_text(200,50, text="Total Cases: " + str(europe_total_cases), font=('Helvetica', 18, 'bold'), fill="black", tag="delete_text")
    europe_updates_canvas.create_text(200,90, text="Total Recovered: " + str(europe_total_recovered), font=('Helvetica', 18, 'bold'), fill="green", tag="delete_text")
    europe_updates_canvas.create_text(200,130, text="Total Deaths: " + str(europe_total_deaths), font=('Helvetica', 18, 'bold'), fill="black", tag="delete_text")
    europe_updates_canvas.create_text(200,170, text="New Cases: " + str(europe_new_cases), font=('Helvetica', 18, 'bold'), fill="red",tag="delete_text")
    
    def selected_option_europe(event):
        option_selected=europe_combo.get()
        europe_updates_canvas.delete("delete_text")

        selected_country_total_cases=covid_df.loc[option_selected, 'Total Cases']
        selected_country_total_recovered=covid_df.loc[option_selected, 'Total Recovered']
        selected_country_total_deaths=covid_df.loc[option_selected, 'Total Deaths']
        selected_country_new_cases=covid_df.loc[option_selected,'New Cases']

        europe_updates_canvas.create_text(200,50, text="Total Cases: " + str(selected_country_total_cases), font=('Helvetica', 18, 'bold'), fill="black", tag="delete_text")
        europe_updates_canvas.create_text(200,90, text="Total Recovered: " + str(selected_country_total_recovered), font=('Helvetica', 18, 'bold'), fill="green", tag="delete_text")
        europe_updates_canvas.create_text(200,130, text="Total Deaths: " + str(selected_country_total_deaths), font=('Helvetica', 18, 'bold'), fill="black", tag="delete_text")
        europe_updates_canvas.create_text(200,170, text="New Cases: " + str(selected_country_new_cases), font=('Helvetica', 18, 'bold'), fill="red",tag="delete_text")


    europe_countries_list=["Europe","Russia","Spain","UK","Italy","Germany","France","Belgium","Belarus","Netherlands","Sweden","Portugal","Switzerland","Ukraine",
    "Poland","Ireland","Romania","Austria","Denmark","Serbia","Moldova","Czechia","Norway","Finland","Luxembourg","Hungary","North Macedonia","Greece","Bulgaria",
    "Bosnia and Herzegovina","Croatia","Estonia","Iceland","Lithuania","Slovakia","Slovenia","Albania","Latvia","Andorra","San Marino","Malta","Channel Islands",
    "Isle of Man","Montenegro","Faeroe Islands","Gibraltar","Monaco","Liechtenstein","Vatican City"]

    select_country_label=Label(europe1, text="Select Country", bg="#d3f4ff", font=('Helvetica',12,'bold','underline'), fg="#084177")
    select_country_label.grid(pady=20)
    
    europe_combo=ttk.Combobox(europe1, value=europe_countries_list, state='readonly', width=30, height=6)
    europe_combo.current(0)
    europe_combo.bind("<<ComboboxSelected>>", selected_option_europe)
    europe_combo.grid()


    europe1.mainloop()

def africa():
    africa1=Tk()
    africa1.geometry("400x400")
    africa1.iconbitmap(r"C:\Users\riyan\Downloads\favicon (2).ico")
    africa1.title("Africa")
    africa1.config(bg="#d3f4ff")

    africa_updates_canvas=Canvas(africa1, height=200, width=400, bg="#d3f4ff",bd=0, highlightthickness=0, relief='ridge')
    africa_updates_canvas.grid()
    africa_updates_canvas.create_rectangle(10,20,390,193, fill="#d3f4ff",outline="black", width=3)
        
    africa_total_cases=covid_df.loc['Africa','Total Cases']
    africa_total_recovered=covid_df.loc['Africa', 'Total Recovered']
    africa_total_deaths=covid_df.loc['Africa' ,'Total Deaths']
    africa_new_cases=covid_df.loc['Africa', 'New Cases']

    africa_updates_canvas.create_text(200,50, text="Total Cases: " + str(africa_total_cases), font=('Helvetica', 18, 'bold'), fill="black", tag="delete_text")
    africa_updates_canvas.create_text(200,90, text="Total Recovered: " + str(africa_total_recovered), font=('Helvetica', 18, 'bold'), fill="green", tag="delete_text")
    africa_updates_canvas.create_text(200,130, text="Total Deaths: " + str(africa_total_deaths), font=('Helvetica', 18, 'bold'), fill="black", tag="delete_text")       
    africa_updates_canvas.create_text(200,170, text="New Cases: " + str(africa_new_cases), font=('Helvetica', 18, 'bold'), fill="red",tag="delete_text")
        
    def selected_option_africa(event):
        option_selected=africa_combo.get()
        africa_updates_canvas.delete("delete_text")

        selected_country_total_cases=covid_df.loc[option_selected, 'Total Cases']
        selected_country_total_recovered=covid_df.loc[option_selected, 'Total Recovered']
        selected_country_total_deaths=covid_df.loc[option_selected, 'Total Deaths']
        selected_country_new_cases=covid_df.loc[option_selected,'New Cases']

        africa_updates_canvas.create_text(200,50, text="Total Cases: " + str(selected_country_total_cases), font=('Helvetica', 18, 'bold'), fill="black", tag="delete_text")
        africa_updates_canvas.create_text(200,90, text="Total Recovered: " + str(selected_country_total_recovered), font=('Helvetica', 18, 'bold'), fill="green", tag="delete_text")
        africa_updates_canvas.create_text(200,130, text="Total Deaths: " + str(selected_country_total_deaths), font=('Helvetica', 18, 'bold'), fill="black", tag="delete_text")
        africa_updates_canvas.create_text(200,170, text="New Cases: " + str(selected_country_new_cases), font=('Helvetica', 18, 'bold'), fill="red",tag="delete_text")


    africa_countries_list=["Africa","South Africa","Egypt","Nigeria","Algeria","Ghana","Morocco","Cameroon","Sudan","Senegal","Djibouti","Guinea","DRC","Ivory Coast","Gabon","Kenya","Somalia",
    "Ethiopia","Mayotte","CAR","South Sudan","Mali","Guinea-Bissau","Equatorial Guinea","Zambia","Madagascar","Tunisia","Mauritania","Sierra Leone","Niger","Burkina Faso","Chad",
    "Congo","Uganda","Cabo Verde","Sao Tome and Principe","Tanzania","Togo","Réunion","Rwanda","Malawi","Mozambique","Liberia","Mauritius","Eswatini","Benin","Zimbabwe","Libya",
    "Comoros","Angola","Burundi","Botswana","Eritrea","Namibia","Gambia","Seychelles","Western Sahara","Lesotho"]

    select_country_label=Label(africa1, text="Select Country", bg="#d3f4ff", font=('Helvetica',12,'bold','underline'), fg="#084177")
    select_country_label.grid(pady=20)
    
    africa_combo=ttk.Combobox(africa1, value=africa_countries_list, state='readonly', width=30, height=6)
    africa_combo.current(0)
    africa_combo.bind("<<ComboboxSelected>>", selected_option_africa)
    africa_combo.grid()


    africa1.mainloop()


#world_canvas
world_canvas=Canvas(live_updates_frame, height=200, width=1000)
world_canvas.grid(row=0, column=0, columnspan=3, pady=15)
world_image=Image.open(r"C:\Users\riyan\OneDrive\Desktop\gui python(tkinter)\world-map.jpg")
world_image_resize=world_image.resize((1000,300), Image.ANTIALIAS)
final_world_image=ImageTk.PhotoImage(world_image_resize)
world_canvas.create_image(500,100,image=final_world_image)
world_canvas.create_text(500,25, text="WORLD", font=('Helvetica', 24, 'bold', 'underline'), fill="#1f4068")
total_cases_world=covid_df.loc['World', 'Total Cases']
new_cases_world=covid_df.loc['World','New Cases']
total_deaths_world=covid_df.loc['World', 'Total Deaths']
total_recovered_world=covid_df.loc['World','Total Recovered']
world_canvas.create_text(325, 90, text="Total Cases: " + str(total_cases_world), font=('Helvetica',18,'bold'), fill='black')
world_canvas.create_text(325, 140, text="New Cases: " + str(new_cases_world), font=('Helvetica',18,'bold'), fill='red')
world_canvas.create_text(700, 90, text="Total Deaths: " + str(total_deaths_world), font=('Helvetica',18,'bold'), fill='black')
world_canvas.create_text(700, 140, text="Total Recovered: " + str(total_recovered_world), font=('Helvetica',18,'bold'), fill='green')


#north america canvas
north_america_canvas=Canvas(live_updates_frame, height=250, width=200, bg="#e3fdfd")
north_america_canvas.grid(row=1, column=0, padx=0)

north_america_image=Image.open(r"C:\Users\riyan\OneDrive\Desktop\gui python(tkinter)\north-america.png")
north_america_resize_image=north_america_image.resize((220,200), Image.ANTIALIAS)
final_north_america_image=ImageTk.PhotoImage(north_america_resize_image)
north_america_canvas.create_image(0,0, anchor=NW , image=final_north_america_image)

def on_enter_north_america(event):
    north_america_button['foreground']='blue'

def on_leave_north_america(event):
    north_america_button['foreground']='black'

north_america_button=Button(live_updates_frame, text="North America", borderwidth=0, font=('Helvetica', 16, 'bold', 'underline'), bg="#e3fdfd" , command=north_america )
north_america_button_window=north_america_canvas.create_window(100, 225 , window=north_america_button)
north_america_button.bind("<Enter>", on_enter_north_america)
north_america_button.bind("<Leave>", on_leave_north_america)

#South America canvas
south_america_canvas=Canvas(live_updates_frame, height=250, width=200, bg="#e3fdfd")
south_america_canvas.grid(row=1, column=1, padx=0)

south_america_image=Image.open(r"C:\Users\riyan\OneDrive\Desktop\gui python(tkinter)\south-america.png")
south_america_resize_image=south_america_image.resize((220,200), Image.ANTIALIAS)
final_south_america_image=ImageTk.PhotoImage(south_america_resize_image)
south_america_canvas.create_image(0,0, anchor=NW , image=final_south_america_image)

def on_enter_south_america(event):
    south_america_button['foreground']='blue'

def on_leave_south_america(event):
    south_america_button['foreground']='black'

south_america_button=Button(live_updates_frame, text="South America", borderwidth=0, font=('Helvetica', 16, 'bold', 'underline'), bg="#e3fdfd", command=south_america )
south_america_button_window=south_america_canvas.create_window(100, 225 , window=south_america_button)
south_america_button.bind("<Enter>", on_enter_south_america)
south_america_button.bind("<Leave>", on_leave_south_america)

#Asia Canvas
asia_canvas=Canvas(live_updates_frame, height=250, width=200, bg="#e3fdfd")
asia_canvas.grid(row=1, column=2, padx=0)

asia_image=Image.open(r"C:\Users\riyan\OneDrive\Desktop\gui python(tkinter)\asia.png")
asia_resize_image=asia_image.resize((220,190), Image.ANTIALIAS)
final_asia_image=ImageTk.PhotoImage(asia_resize_image)
asia_canvas.create_image(0,0, anchor=NW , image=final_asia_image)

def on_enter_asia(event):
    asia_button['foreground']='blue'

def on_leave_asia(event):
    asia_button['foreground']='black'

asia_button=Button(live_updates_frame, text="Asia", borderwidth=0, font=('Helvetica', 16, 'bold', 'underline'), bg="#e3fdfd", command=asia )
asia_button_window=asia_canvas.create_window(100, 225 , window=asia_button)
asia_button.bind("<Enter>", on_enter_asia)
asia_button.bind("<Leave>", on_leave_asia)

#Africa Canvas
africa_canvas=Canvas(live_updates_frame, height=250, width=200, bg="#e3fdfd")
africa_canvas.grid(row=2, column=0, padx=0, pady=15)

africa_image=Image.open(r"C:\Users\riyan\Downloads\africa.png")
africa_resize_image=africa_image.resize((200,200), Image.ANTIALIAS)
final_africa_image=ImageTk.PhotoImage(africa_resize_image)
africa_canvas.create_image(0,0, anchor=NW , image=final_africa_image)

def on_enter_africa(event):
    africa_button['foreground']='blue'

def on_leave_africa(event):
    africa_button['foreground']='black'

africa_button=Button(live_updates_frame, text="Africa", borderwidth=0, font=('Helvetica', 16, 'bold', 'underline'), bg="#e3fdfd", command=africa)
africa_button_window=africa_canvas.create_window(100, 225 , window=africa_button)
africa_button.bind("<Enter>", on_enter_africa)
africa_button.bind("<Leave>", on_leave_africa)

#oceania Canvas
oceania_canvas=Canvas(live_updates_frame, height=250, width=200, bg="#e3fdfd")
oceania_canvas.grid(row=2, column=1, padx=0, pady=15)

oceania_image=Image.open(r"C:\Users\riyan\OneDrive\Desktop\gui python(tkinter)\australia.jpg")
oceania_resize_image=oceania_image.resize((220,200), Image.ANTIALIAS)
final_oceania_image=ImageTk.PhotoImage(oceania_resize_image)
oceania_canvas.create_image(0,0, anchor=NW , image=final_oceania_image)

def on_enter_oceania(event):
    oceania_button['foreground']='blue'

def on_leave_oceania(event):
    oceania_button['foreground']='black'

oceania_button=Button(live_updates_frame, text="Oceania", borderwidth=0, font=('Helvetica', 16, 'bold', 'underline'), bg="#e3fdfd",command=oceania )
oceania_button_window=oceania_canvas.create_window(100, 225 , window=oceania_button)
oceania_button.bind("<Enter>", on_enter_oceania)
oceania_button.bind("<Leave>", on_leave_oceania)

#Europe Canvas
europe_canvas=Canvas(live_updates_frame, height=250, width=200, bg="#e3fdfd")
europe_canvas.grid(row=2, column=2,  padx=0, pady=15)

europe_image=Image.open(r"C:\Users\riyan\OneDrive\Desktop\gui python(tkinter)\europe.png")
europe_resize_image=europe_image.resize((210,200), Image.ANTIALIAS)
final_europe_image=ImageTk.PhotoImage(europe_resize_image)
europe_canvas.create_image(0,0, anchor=NW , image=final_europe_image)

def on_enter_europe(event):
    europe_button['foreground']='blue'

def on_leave_europe(event):
    europe_button['foreground']='black'

europe_button=Button(live_updates_frame, text="Europe", borderwidth=0, font=('Helvetica', 16, 'bold', 'underline'), bg="#e3fdfd", command=europe)
europe_button_window=europe_canvas.create_window(100, 225 , window=europe_button)
europe_button.bind("<Enter>", on_enter_europe)
europe_button.bind("<Leave>", on_leave_europe)

#COVID-19 INDIA 

def goa():
    blue_bullet()
    india_canvas.delete("delete")
    goa_button=Button(local_frame, image=red_small_bullet_image, bg="#e3fdfd", command=goa, borderwidth=0)
    india_canvas.create_window(300,580, window=goa_button)
    total_cases=india_covid_df.loc['Goa', 'Total Cases']
    deaths=india_covid_df.loc['Goa','Deaths']
    recovered=india_covid_df.loc['Goa','Total Recovered']
    active_cases=india_covid_df.loc['Goa','Active Cases']
    india_canvas.create_text(800,30, text="State: Goa", font=('Helvetica', 16,'underline', 'bold'), tag="delete")
    india_canvas.create_text(800, 70, text="Total Cases: " + total_cases, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 110, text="Total Deaths: " + deaths, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 150, text="Total Recovered: " + recovered, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 190, text="Active Cases: " + active_cases, font=('Helvetica', 16),tag="delete")

def himachal():
    blue_bullet()
    india_canvas.delete("delete")
    hp_button=Button(local_frame, image=red_final_bullet_image, borderwidth=0, bg="#e3fdfd", command=himachal)
    india_canvas.create_window(375,145, window=hp_button)
    total_cases=india_covid_df.loc['Himachal Pradesh', 'Total Cases']
    deaths=india_covid_df.loc['Himachal Pradesh','Deaths']
    recovered=india_covid_df.loc['Himachal Pradesh','Total Recovered']
    active_cases=india_covid_df.loc['Himachal Pradesh','Active Cases']
    india_canvas.create_text(800,30, text="State: Himachal Pradesh", font=('Helvetica', 16,'underline', 'bold'), tag="delete")
    india_canvas.create_text(800, 70, text="Total Cases: " + total_cases, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 110, text="Total Deaths: " + deaths, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 150, text="Total Recovered: " + recovered, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 190, text="Active Cases: " + active_cases, font=('Helvetica', 16),tag="delete")


def punjab():
    blue_bullet()
    india_canvas.delete("delete")
    punjab_button=Button(local_frame, image=red_final_bullet_image, borderwidth=0, bg="#e3fdfd", command=punjab)
    india_canvas.create_window(335,180, window=punjab_button)
    total_cases=india_covid_df.loc['Punjab', 'Total Cases']
    deaths=india_covid_df.loc['Punjab','Deaths']
    recovered=india_covid_df.loc['Punjab','Total Recovered']
    active_cases=india_covid_df.loc['Punjab','Active Cases']
    india_canvas.create_text(800,30, text="State: Punjab", font=('Helvetica', 16,'underline', 'bold'), tag="delete")
    india_canvas.create_text(800, 70, text="Total Cases: " + total_cases, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 110, text="Total Deaths: " + deaths, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 150, text="Total Recovered: " + recovered, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 190, text="Active Cases: " + active_cases, font=('Helvetica', 16),tag="delete")


def haryana():
    blue_bullet()
    india_canvas.delete("delete")
    haryana_button=Button(local_frame, image=red_final_bullet_image, borderwidth=0, bg="#e3fdfd", command=haryana)
    india_canvas.create_window(355,230, window=haryana_button)
    total_cases=india_covid_df.loc['Haryana', 'Total Cases']
    deaths=india_covid_df.loc['Haryana','Deaths']
    recovered=india_covid_df.loc['Haryana','Total Recovered']
    active_cases=india_covid_df.loc['Haryana','Active Cases']
    india_canvas.create_text(800,30, text="State: Haryana", font=('Helvetica', 16,'underline', 'bold'), tag="delete")
    india_canvas.create_text(800, 70, text="Total Cases: " + total_cases, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 110, text="Total Deaths: " + deaths, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 150, text="Total Recovered: " + recovered, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 190, text="Active Cases: " + active_cases, font=('Helvetica', 16),tag="delete")


def uttarakhand():
    blue_bullet()
    india_canvas.delete("delete")
    uttarakhand_button=Button(local_frame, image=red_final_bullet_image, borderwidth=0, bg="#e3fdfd", command=uttarakhand)
    india_canvas.create_window(420,190, window=uttarakhand_button)
    total_cases=india_covid_df.loc['Uttarakhand', 'Total Cases']
    deaths=india_covid_df.loc['Uttarakhand','Deaths']
    recovered=india_covid_df.loc['Uttarakhand','Total Recovered']
    active_cases=india_covid_df.loc['Uttarakhand','Active Cases']
    india_canvas.create_text(800,30, text="State: Uttarakhand", font=('Helvetica', 16,'underline', 'bold'), tag="delete")
    india_canvas.create_text(800, 70, text="Total Cases: " + total_cases, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 110, text="Total Deaths: " + deaths, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 150, text="Total Recovered: " + recovered, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 190, text="Active Cases: " + active_cases, font=('Helvetica', 16),tag="delete")


def uttar_pradesh():
    blue_bullet()
    india_canvas.delete("delete")
    up_button=Button(local_frame, image=red_final_bullet_image, borderwidth=0, bg="#e3fdfd", command=uttar_pradesh)
    india_canvas.create_window(450,280, window=up_button)
    total_cases=india_covid_df.loc['Uttar Pradesh', 'Total Cases']
    deaths=india_covid_df.loc['Uttar Pradesh','Deaths']
    recovered=india_covid_df.loc['Uttar Pradesh','Total Recovered']
    active_cases=india_covid_df.loc['Uttar Pradesh','Active Cases']
    india_canvas.create_text(800,30, text="State: Uttar Pradesh", font=('Helvetica', 16,'underline', 'bold'), tag="delete")
    india_canvas.create_text(800, 70, text="Total Cases: " + total_cases, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 110, text="Total Deaths: " + deaths, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 150, text="Total Recovered: " + recovered, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 190, text="Active Cases: " + active_cases, font=('Helvetica', 16),tag="delete")

def rajasthan():
    blue_bullet()
    india_canvas.delete("delete")
    raja_button=Button(local_frame, image=red_final_bullet_image, borderwidth=0, bg="#e3fdfd", command=rajasthan)
    india_canvas.create_window(290,290, window=raja_button)
    total_cases=india_covid_df.loc['Rajasthan', 'Total Cases']
    deaths=india_covid_df.loc['Rajasthan','Deaths']
    recovered=india_covid_df.loc['Rajasthan','Total Recovered']
    active_cases=india_covid_df.loc['Rajasthan','Active Cases']
    india_canvas.create_text(800,30, text="State: Rajasthan", font=('Helvetica', 16,'underline', 'bold'), tag="delete")
    india_canvas.create_text(800, 70, text="Total Cases: " + total_cases, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 110, text="Total Deaths: " + deaths, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 150, text="Total Recovered: " + recovered, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 190, text="Active Cases: " + active_cases, font=('Helvetica', 16),tag="delete")


def bihar():
    blue_bullet()
    india_canvas.delete("delete")
    bihar_button=Button(local_frame, image=red_final_bullet_image, borderwidth=0, bg="#e3fdfd", command=bihar)
    india_canvas.create_window(570,320, window=bihar_button)
    total_cases=india_covid_df.loc['Bihar', 'Total Cases']
    deaths=india_covid_df.loc['Bihar','Deaths']
    recovered=india_covid_df.loc['Bihar','Total Recovered']
    active_cases=india_covid_df.loc['Bihar','Active Cases']
    india_canvas.create_text(800,30, text="State: Bihar", font=('Helvetica', 16,'underline', 'bold'), tag="delete")
    india_canvas.create_text(800, 70, text="Total Cases: " + total_cases, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 110, text="Total Deaths: " + deaths, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 150, text="Total Recovered: " + recovered, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 190, text="Active Cases: " + active_cases, font=('Helvetica', 16),tag="delete")

def sikkim():
    blue_bullet()
    india_canvas.delete("delete")
    sikkim_button=Button(local_frame, image=red_small_bullet_image, borderwidth=0, bg="#e3fdfd", command=sikkim)
    india_canvas.create_window(627,265, window=sikkim_button)
    total_cases=india_covid_df.loc['Sikkim', 'Total Cases']
    deaths=india_covid_df.loc['Sikkim','Deaths']
    recovered=india_covid_df.loc['Sikkim','Total Recovered']
    active_cases=india_covid_df.loc['Sikkim','Active Cases']
    india_canvas.create_text(800,30, text="State: Sikkim", font=('Helvetica', 16,'underline', 'bold'), tag="delete")
    india_canvas.create_text(800, 70, text="Total Cases: " + total_cases, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 110, text="Total Deaths: " + deaths, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 150, text="Total Recovered: " + recovered, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 190, text="Active Cases: " + active_cases, font=('Helvetica', 16),tag="delete")


def arunachal_pradesh():
    blue_bullet()
    india_canvas.delete("delete")
    arunachal_button=Button(local_frame, image=red_final_bullet_image, borderwidth=0, bg="#e3fdfd", command=arunachal_pradesh)
    india_canvas.create_window(760,250, window=arunachal_button)
    total_cases=india_covid_df.loc['Arunachal Pradesh', 'Total Cases']
    deaths=india_covid_df.loc['Arunachal Pradesh','Deaths']
    recovered=india_covid_df.loc['Arunachal Pradesh','Total Recovered']
    active_cases=india_covid_df.loc['Arunachal Pradesh','Active Cases']
    india_canvas.create_text(800,30, text="State: Arunachal Pradesh", font=('Helvetica', 16,'underline', 'bold'), tag="delete")
    india_canvas.create_text(800, 70, text="Total Cases: " + total_cases, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 110, text="Total Deaths: " + deaths, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 150, text="Total Recovered: " + recovered, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 190, text="Active Cases: " + active_cases, font=('Helvetica', 16),tag="delete")


def assam():
    blue_bullet()
    india_canvas.delete("delete")
    assam_button=Button(local_frame, image=red_final_bullet_image, borderwidth=0, bg="#e3fdfd", command=assam)
    india_canvas.create_window(730,300, window=assam_button)
    total_cases=india_covid_df.loc['Assam', 'Total Cases']
    deaths=india_covid_df.loc['Assam','Deaths']
    recovered=india_covid_df.loc['Assam','Total Recovered']
    active_cases=india_covid_df.loc['Assam','Active Cases']
    india_canvas.create_text(800,30, text="State: Assam", font=('Helvetica', 16,'underline', 'bold'), tag="delete")
    india_canvas.create_text(800, 70, text="Total Cases: " + total_cases, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 110, text="Total Deaths: " + deaths, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 150, text="Total Recovered: " + recovered, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 190, text="Active Cases: " + active_cases, font=('Helvetica', 16),tag="delete")


def nagaland():
    blue_bullet()
    india_canvas.delete("delete")
    nagaland_button=Button(local_frame, image=red_medium_bullet_image, borderwidth=0, bg="#e3fdfd", command=nagaland)
    india_canvas.create_window(766,305, window=nagaland_button)
    total_cases=india_covid_df.loc['Nagaland', 'Total Cases']
    deaths=india_covid_df.loc['Nagaland','Deaths']
    recovered=india_covid_df.loc['Nagaland','Total Recovered']
    active_cases=india_covid_df.loc['Nagaland','Active Cases']
    india_canvas.create_text(800,30, text="State: Nagaland", font=('Helvetica', 16,'underline', 'bold'), tag="delete")
    india_canvas.create_text(800, 70, text="Total Cases: " + total_cases, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 110, text="Total Deaths: " + deaths, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 150, text="Total Recovered: " + recovered, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 190, text="Active Cases: " + active_cases, font=('Helvetica', 16),tag="delete")


def manipur():
    blue_bullet()
    india_canvas.delete("delete")
    manipur_button=Button(local_frame, image=red_medium_bullet_image, borderwidth=0, bg="#e3fdfd", command=manipur)
    india_canvas.create_window(750,340, window=manipur_button)
    total_cases=india_covid_df.loc['Manipur', 'Total Cases']
    deaths=india_covid_df.loc['Manipur','Deaths']
    recovered=india_covid_df.loc['Manipur','Total Recovered']
    active_cases=india_covid_df.loc['Manipur','Active Cases']
    india_canvas.create_text(800,30, text="State: Manipur", font=('Helvetica', 16,'underline', 'bold'), tag="delete")
    india_canvas.create_text(800, 70, text="Total Cases: " + total_cases, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 110, text="Total Deaths: " + deaths, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 150, text="Total Recovered: " + recovered, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 190, text="Active Cases: " + active_cases, font=('Helvetica', 16),tag="delete")


def mizoram():
    blue_bullet()
    india_canvas.delete("delete")
    mizoram_button=Button(local_frame, image=red_medium_bullet_image, borderwidth=0, bg="#e3fdfd", command=mizoram)
    india_canvas.create_window(725,375, window=mizoram_button)
    total_cases=india_covid_df.loc['Mizoram', 'Total Cases']
    deaths=india_covid_df.loc['Mizoram','Deaths']
    recovered=india_covid_df.loc['Mizoram','Total Recovered']
    active_cases=india_covid_df.loc['Mizoram','Active Cases']
    india_canvas.create_text(800,30, text="State: Mizoram", font=('Helvetica', 16,'underline', 'bold'), tag="delete")
    india_canvas.create_text(800, 70, text="Total Cases: " + total_cases, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 110, text="Total Deaths: " + deaths, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 150, text="Total Recovered: " + recovered, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 190, text="Active Cases: " + active_cases, font=('Helvetica', 16),tag="delete")


def tripura():
    blue_bullet()
    india_canvas.delete("delete")
    tripura_button=Button(local_frame, image=red_small_bullet_image, borderwidth=0, bg="#e3fdfd", command=tripura)
    india_canvas.create_window(696,370, window=tripura_button)
    total_cases=india_covid_df.loc['Tripura', 'Total Cases']
    deaths=india_covid_df.loc['Tripura','Deaths']
    recovered=india_covid_df.loc['Tripura','Total Recovered']
    active_cases=india_covid_df.loc['Tripura','Active Cases']
    india_canvas.create_text(800,30, text="State: Tripura", font=('Helvetica', 16,'underline', 'bold'), tag="delete")
    india_canvas.create_text(800, 70, text="Total Cases: " + total_cases, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 110, text="Total Deaths: " + deaths, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 150, text="Total Recovered: " + recovered, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 190, text="Active Cases: " + active_cases, font=('Helvetica', 16),tag="delete")

def meghalaya():
    blue_bullet()
    india_canvas.delete("delete")
    meghalaya_button=Button(local_frame, image=red_medium_bullet_image, borderwidth=0, bg="#e3fdfd", command=meghalaya)
    india_canvas.create_window(680,322, window=meghalaya_button)
    total_cases=india_covid_df.loc['Meghalaya', 'Total Cases']
    deaths=india_covid_df.loc['Meghalaya','Deaths']
    recovered=india_covid_df.loc['Meghalaya','Total Recovered']
    active_cases=india_covid_df.loc['Meghalaya','Active Cases']
    india_canvas.create_text(800,30, text="State: Meghalaya", font=('Helvetica', 16,'underline', 'bold'), tag="delete")
    india_canvas.create_text(800, 70, text="Total Cases: " + total_cases, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 110, text="Total Deaths: " + deaths, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 150, text="Total Recovered: " + recovered, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 190, text="Active Cases: " + active_cases, font=('Helvetica', 16),tag="delete")

def maharashtra():
    blue_bullet()
    india_canvas.delete("delete")
    maharashtra_button=Button(local_frame, image=red_final_bullet_image, borderwidth=0, bg="#e3fdfd", command=maharashtra)
    india_canvas.create_window(350,470, window=maharashtra_button)
    total_cases=india_covid_df.loc['Maharashtra', 'Total Cases']
    deaths=india_covid_df.loc['Maharashtra','Deaths']
    recovered=india_covid_df.loc['Maharashtra','Total Recovered']
    active_cases=india_covid_df.loc['Maharashtra','Active Cases']
    india_canvas.create_text(800,30, text="State: Maharashtra", font=('Helvetica', 16,'underline', 'bold'), tag="delete")
    india_canvas.create_text(800, 70, text="Total Cases: " + total_cases, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 110, text="Total Deaths: " + deaths, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 150, text="Total Recovered: " + recovered, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 190, text="Active Cases: " + active_cases, font=('Helvetica', 16),tag="delete")


def gujarat():
    blue_bullet()
    india_canvas.delete("delete")
    gujarat_button=Button(local_frame, image=red_final_bullet_image, borderwidth=0, bg="#e3fdfd", command=gujarat)
    india_canvas.create_window(250,390, window=gujarat_button)
    total_cases=india_covid_df.loc['Gujarat', 'Total Cases']
    deaths=india_covid_df.loc['Gujarat','Deaths']
    recovered=india_covid_df.loc['Gujarat','Total Recovered']
    active_cases=india_covid_df.loc['Gujarat','Active Cases']
    india_canvas.create_text(800,30, text="State: Gujarat", font=('Helvetica', 16,'underline', 'bold'), tag="delete")
    india_canvas.create_text(800, 70, text="Total Cases: " + total_cases, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 110, text="Total Deaths: " + deaths, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 150, text="Total Recovered: " + recovered, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 190, text="Active Cases: " + active_cases, font=('Helvetica', 16),tag="delete")


def madhya_pradesh():
    blue_bullet()
    india_canvas.delete("delete")
    mp_button=Button(local_frame, image=red_final_bullet_image, borderwidth=0, bg="#e3fdfd", command=madhya_pradesh)
    india_canvas.create_window(400,380, window=mp_button)
    total_cases=india_covid_df.loc['Madhya Pradesh', 'Total Cases']
    deaths=india_covid_df.loc['Madhya Pradesh','Deaths']
    recovered=india_covid_df.loc['Madhya Pradesh','Total Recovered']
    active_cases=india_covid_df.loc['Madhya Pradesh','Active Cases']
    india_canvas.create_text(800,30, text="State: Madhya Pradesh", font=('Helvetica', 16,'underline', 'bold'), tag="delete")
    india_canvas.create_text(800, 70, text="Total Cases: " + total_cases, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 110, text="Total Deaths: " + deaths, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 150, text="Total Recovered: " + recovered, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 190, text="Active Cases: " + active_cases, font=('Helvetica', 16),tag="delete")


def chhattisgarh():
    blue_bullet()
    india_canvas.delete("delete")
    chhattisgarh_button=Button(local_frame, image=red_final_bullet_image, borderwidth=0, bg="#e3fdfd", command=chhattisgarh)
    india_canvas.create_window(480,430, window=chhattisgarh_button)
    total_cases=india_covid_df.loc['Chhattisgarh', 'Total Cases']
    deaths=india_covid_df.loc['Chhattisgarh','Deaths']
    recovered=india_covid_df.loc['Chhattisgarh','Total Recovered']
    active_cases=india_covid_df.loc['Chhattisgarh','Active Cases']
    india_canvas.create_text(800,30, text="State: Chhattisgarh", font=('Helvetica', 16,'underline', 'bold'), tag="delete")
    india_canvas.create_text(800, 70, text="Total Cases: " + total_cases, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 110, text="Total Deaths: " + deaths, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 150, text="Total Recovered: " + recovered, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 190, text="Active Cases: " + active_cases, font=('Helvetica', 16),tag="delete")

def jharkhand():
    blue_bullet()
    india_canvas.delete("delete")
    jharkhand_button=Button(local_frame, image=red_final_bullet_image, borderwidth=0, bg="#e3fdfd", command=jharkhand)
    india_canvas.create_window(555,380, window=jharkhand_button)
    total_cases=india_covid_df.loc['Jharkhand', 'Total Cases']
    deaths=india_covid_df.loc['Jharkhand','Deaths']
    recovered=india_covid_df.loc['Jharkhand','Total Recovered']
    active_cases=india_covid_df.loc['Jharkhand','Active Cases']
    india_canvas.create_text(800,30, text="State: Jharkhand", font=('Helvetica', 16,'underline', 'bold'), tag="delete")
    india_canvas.create_text(800, 70, text="Total Cases: " + total_cases, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 110, text="Total Deaths: " + deaths, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 150, text="Total Recovered: " + recovered, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 190, text="Active Cases: " + active_cases, font=('Helvetica', 16),tag="delete")

def west_bengal():
    blue_bullet()
    india_canvas.delete("delete")
    wb_button=Button(local_frame, image=red_final_bullet_image, borderwidth=0, bg="#e3fdfd", command=west_bengal)
    india_canvas.create_window(610,380, window=wb_button)
    total_cases=india_covid_df.loc['West Bengal', 'Total Cases']
    deaths=india_covid_df.loc['West Bengal','Deaths']
    recovered=india_covid_df.loc['West Bengal','Total Recovered']
    active_cases=india_covid_df.loc['West Bengal','Active Cases']
    india_canvas.create_text(800,30, text="State: West Bengal", font=('Helvetica', 16,'underline', 'bold'), tag="delete")
    india_canvas.create_text(800, 70, text="Total Cases: " + total_cases, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 110, text="Total Deaths: " + deaths, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 150, text="Total Recovered: " + recovered, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 190, text="Active Cases: " + active_cases, font=('Helvetica', 16),tag="delete")
    

def odisha():
    blue_bullet()
    india_canvas.delete("delete")
    odisha_button=Button(local_frame, image=red_final_bullet_image, borderwidth=0, bg="#e3fdfd", command=odisha)
    india_canvas.create_window(550,440, window=odisha_button)
    total_cases=india_covid_df.loc['Odisha', 'Total Cases']
    deaths=india_covid_df.loc['Odisha','Deaths']
    recovered=india_covid_df.loc['Odisha','Total Recovered']
    active_cases=india_covid_df.loc['Odisha','Active Cases']
    india_canvas.create_text(800,30, text="State: Odisha", font=('Helvetica', 16,'underline', 'bold'), tag="delete")
    india_canvas.create_text(800, 70, text="Total Cases: " + total_cases, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 110, text="Total Deaths: " + deaths, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 150, text="Total Recovered: " + recovered, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 190, text="Active Cases: " + active_cases, font=('Helvetica', 16),tag="delete")

def karnatka():
    blue_bullet()
    india_canvas.delete("delete")
    karnatka_button=Button(local_frame, image=red_final_bullet_image, borderwidth=0, bg="#e3fdfd", command=karnatka)
    india_canvas.create_window(340,600, window=karnatka_button)
    total_cases=india_covid_df.loc['Karnataka', 'Total Cases']
    deaths=india_covid_df.loc['Karnataka','Deaths']
    recovered=india_covid_df.loc['Karnataka','Total Recovered']
    active_cases=india_covid_df.loc['Karnataka','Active Cases']
    india_canvas.create_text(800,30, text="State: Karnataka", font=('Helvetica', 16,'underline', 'bold'), tag="delete")
    india_canvas.create_text(800, 70, text="Total Cases: " + total_cases, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 110, text="Total Deaths: " + deaths, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 150, text="Total Recovered: " + recovered, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 190, text="Active Cases: " + active_cases, font=('Helvetica', 16),tag="delete")

def telangana():
    blue_bullet()
    india_canvas.delete("delete") 
    telangana_button=Button(local_frame, image=red_final_bullet_image, borderwidth=0, bg="#e3fdfd", command=telangana)
    india_canvas.create_window(410,520, window=telangana_button)
    total_cases=india_covid_df.loc['Telangana', 'Total Cases']
    deaths=india_covid_df.loc['Telangana','Deaths']
    recovered=india_covid_df.loc['Telangana','Total Recovered']
    active_cases=india_covid_df.loc['Telangana','Active Cases']
    india_canvas.create_text(800,30, text="State: Telangana", font=('Helvetica', 16,'underline', 'bold'), tag="delete")
    india_canvas.create_text(800, 70, text="Total Cases: " + total_cases, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 110, text="Total Deaths: " + deaths, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 150, text="Total Recovered: " + recovered, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 190, text="Active Cases: " + active_cases, font=('Helvetica', 16),tag="delete")

def andhra_pradesh():
    blue_bullet()
    india_canvas.delete("delete")
    ap_button=Button(local_frame, image=red_final_bullet_image, borderwidth=0, bg="#e3fdfd", command=andhra_pradesh)
    india_canvas.create_window(415,580, window=ap_button)
    total_cases=india_covid_df.loc['Andhra Pradesh', 'Total Cases']
    deaths=india_covid_df.loc['Andhra Pradesh','Deaths']
    recovered=india_covid_df.loc['Andhra Pradesh','Total Recovered']
    active_cases=india_covid_df.loc['Andhra Pradesh','Active Cases']
    india_canvas.create_text(800,30, text="State: Andhra Pradesh", font=('Helvetica', 16,'underline', 'bold'), tag="delete")
    india_canvas.create_text(800, 70, text="Total Cases: " + total_cases, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 110, text="Total Deaths: " + deaths, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 150, text="Total Recovered: " + recovered, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 190, text="Active Cases: " + active_cases, font=('Helvetica', 16),tag="delete")

def kerala():
    blue_bullet()
    india_canvas.delete("delete")
    kerala_button=Button(local_frame, image=red_small_bullet_image, borderwidth=0, bg="#e3fdfd", command=kerala)
    india_canvas.create_window(358,695, window=kerala_button)
    total_cases=india_covid_df.loc['Kerala', 'Total Cases']
    deaths=india_covid_df.loc['Kerala','Deaths']
    recovered=india_covid_df.loc['Kerala','Total Recovered']
    active_cases=india_covid_df.loc['Kerala','Active Cases']
    india_canvas.create_text(800,30, text="State: Kerala", font=('Helvetica', 16,'underline', 'bold'), tag="delete")
    india_canvas.create_text(800, 70, text="Total Cases: " + total_cases, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 110, text="Total Deaths: " + deaths, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 150, text="Total Recovered: " + recovered, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 190, text="Active Cases: " + active_cases, font=('Helvetica', 16),tag="delete")

def tamil_nadu():
    blue_bullet()
    india_canvas.delete("delete")
    tn_button=Button(local_frame, image=red_final_bullet_image, borderwidth=0, bg="#e3fdfd", command=tamil_nadu)
    india_canvas.create_window(410,680, window=tn_button)
    total_cases=india_covid_df.loc['Tamil Nadu', 'Total Cases']
    deaths=india_covid_df.loc['Tamil Nadu','Deaths']
    recovered=india_covid_df.loc['Tamil Nadu','Total Recovered']
    active_cases=india_covid_df.loc['Tamil Nadu','Active Cases']
    india_canvas.create_text(800,30, text="State: Tamil Nadu", font=('Helvetica', 16,'underline', 'bold'), tag="delete")
    india_canvas.create_text(800, 70, text="Total Cases: " + total_cases, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 110, text="Total Deaths: " + deaths, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 150, text="Total Recovered: " + recovered, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 190, text="Active Cases: " + active_cases, font=('Helvetica', 16),tag="delete")

def delhi():
    blue_bullet()
    india_canvas.delete("delete")
    total_cases=india_covid_df.loc['Delhi', 'Total Cases']
    deaths=india_covid_df.loc['Delhi','Deaths']
    recovered=india_covid_df.loc['Delhi','Total Recovered']
    active_cases=india_covid_df.loc['Delhi','Active Cases']
    india_canvas.create_text(800,30, text="Delhi", font=('Helvetica', 16,'underline', 'bold'), tag="delete")
    india_canvas.create_text(800, 70, text="Total Cases: " + total_cases, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 110, text="Total Deaths: " + deaths, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 150, text="Total Recovered: " + recovered, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 190, text="Active Cases: " + active_cases, font=('Helvetica', 16),tag="delete")

def jk():
    blue_bullet()
    india_canvas.delete("delete")
    total_cases=india_covid_df.loc['Jammu and Kashmir', 'Total Cases']
    deaths=india_covid_df.loc['Jammu and Kashmir','Deaths']
    recovered=india_covid_df.loc['Jammu and Kashmir','Total Recovered']
    active_cases=india_covid_df.loc['Jammu and Kashmir','Active Cases']
    india_canvas.create_text(800,30, text="Jammu & Kashmir", font=('Helvetica', 16,'underline', 'bold'), tag="delete")
    india_canvas.create_text(800, 70, text="Total Cases: " + total_cases, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 110, text="Total Deaths: " + deaths, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 150, text="Total Recovered: " + recovered, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 190, text="Active Cases: " + active_cases, font=('Helvetica', 16),tag="delete")


def puducherry():
    blue_bullet()
    india_canvas.delete("delete")
    total_cases=india_covid_df.loc['Puducherry', 'Total Cases']
    deaths=india_covid_df.loc['Puducherry','Deaths']
    recovered=india_covid_df.loc['Puducherry','Total Recovered']
    active_cases=india_covid_df.loc['Puducherry','Active Cases']
    india_canvas.create_text(800,30, text="Puducherry", font=('Helvetica', 16,'underline', 'bold'), tag="delete")
    india_canvas.create_text(800, 70, text="Total Cases: " + total_cases, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 110, text="Total Deaths: " + deaths, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 150, text="Total Recovered: " + recovered, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 190, text="Active Cases: " + active_cases, font=('Helvetica', 16),tag="delete")

def andaman_nicobar():
    blue_bullet()
    india_canvas.delete("delete")
    total_cases=india_covid_df.loc['Andaman and Nicobar Islands', 'Total Cases']
    deaths=india_covid_df.loc['Andaman and Nicobar Islands','Deaths']
    recovered=india_covid_df.loc['Andaman and Nicobar Islands','Total Recovered']
    active_cases=india_covid_df.loc['Andaman and Nicobar Islands','Active Cases']
    india_canvas.create_text(800,30, text="Andaman & Nicobar ", font=('Helvetica', 16,'underline', 'bold'), tag="delete")
    india_canvas.create_text(800, 70, text="Total Cases: " + total_cases, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 110, text="Total Deaths: " + deaths, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 150, text="Total Recovered: " + recovered, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 190, text="Active Cases: " + active_cases, font=('Helvetica', 16),tag="delete")


def chandigarh():
    blue_bullet()
    india_canvas.delete("delete")
    total_cases=india_covid_df.loc['Chandigarh', 'Total Cases']
    deaths=india_covid_df.loc['Chandigarh','Deaths']
    recovered=india_covid_df.loc['Chandigarh','Total Recovered']
    active_cases=india_covid_df.loc['Chandigarh','Active Cases']
    india_canvas.create_text(800,30, text="Chandigarh", font=('Helvetica', 16,'underline', 'bold'), tag="delete")
    india_canvas.create_text(800, 70, text="Total Cases: " + total_cases, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 110, text="Total Deaths: " + deaths, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 150, text="Total Recovered: " + recovered, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 190, text="Active Cases: " + active_cases, font=('Helvetica', 16),tag="delete")


def lakshadweep():
    blue_bullet()
    india_canvas.delete("delete")
    total_cases=india_covid_df.loc['Lakshadweep', 'Total Cases']
    deaths=india_covid_df.loc['Lakshadweep','Deaths']
    recovered=india_covid_df.loc['Lakshadweep','Total Recovered']
    active_cases=india_covid_df.loc['Lakshadweep','Active Cases']
    india_canvas.create_text(800,30, text="Lakshadweep", font=('Helvetica', 16,'underline', 'bold'), tag="delete")
    india_canvas.create_text(800, 70, text="Total Cases: " + total_cases, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 110, text="Total Deaths: " + deaths, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 150, text="Total Recovered: " + recovered, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 190, text="Active Cases: " + active_cases, font=('Helvetica', 16),tag="delete")


def ladakh():
    blue_bullet()
    india_canvas.delete("delete")
    total_cases=india_covid_df.loc['Ladakh', 'Total Cases']
    deaths=india_covid_df.loc['Ladakh','Deaths']
    recovered=india_covid_df.loc['Ladakh','Total Recovered']
    active_cases=india_covid_df.loc['Ladakh','Active Cases']
    india_canvas.create_text(800,30, text="Ladakh", font=('Helvetica', 16,'underline', 'bold'), tag="delete")
    india_canvas.create_text(800, 70, text="Total Cases: " + total_cases, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 110, text="Total Deaths: " + deaths, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 150, text="Total Recovered: " + recovered, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 190, text="Active Cases: " + active_cases, font=('Helvetica', 16),tag="delete")


def dadra_nagarhaveli_daman_diu():
    blue_bullet()
    india_canvas.delete("delete")
    total_cases=india_covid_df.loc['Dadra and Nagar Haveli and Daman and Diu', 'Total Cases']
    deaths=india_covid_df.loc['Dadra and Nagar Haveli and Daman and Diu','Deaths']
    recovered=india_covid_df.loc['Dadra and Nagar Haveli and Daman and Diu','Total Recovered']
    active_cases=india_covid_df.loc['Dadra and Nagar Haveli and Daman and Diu','Active Cases']
    india_canvas.create_text(800,30, text="Dadra-Nagar Haveli & Daman-Diu", font=('Helvetica', 16,'underline', 'bold'), tag="delete")
    india_canvas.create_text(800, 70, text="Total Cases: " + total_cases, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 110, text="Total Deaths: " + deaths, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 150, text="Total Recovered: " + recovered, font=('Helvetica', 16),tag="delete")
    india_canvas.create_text(800, 190, text="Active Cases: " + active_cases, font=('Helvetica', 16),tag="delete")


def union_territory():
    blue_bullet()	

    delhi_button=Button(local_frame, image=black_final_bullet_image, borderwidth=0, bg="#e3fdfd", command=delhi)
    india_canvas.create_window(375,238, window=delhi_button)

    jk_button=Button(local_frame, image=black_final_bullet_image, borderwidth=0, bg="#e3fdfd", command=jk)
    india_canvas.create_window(360,80, window=jk_button)

    puducherry_button=Button(local_frame, image=black_final_bullet_image, bg="#e3fdfd", command=puducherry, borderwidth=0)
    india_canvas.create_window(430,668, window=puducherry_button)

    andaman_button=Button(local_frame, image=black_final_bullet_image, bg="#e3fdfd", command=andaman_nicobar, borderwidth=0)
    india_canvas.create_window(700,600, window=andaman_button)

    chandigarh_button=Button(local_frame, image=black_final_bullet_image, bg="#e3fdfd", command=chandigarh, borderwidth=0)
    india_canvas.create_window(362,180, window=chandigarh_button)

    lakshwadeep_button=Button(local_frame, image=black_final_bullet_image, bg="#e3fdfd", command=lakshadweep, borderwidth=0)
    india_canvas.create_window(220,650, window=lakshwadeep_button)

    ladakh_button=Button(local_frame, image=black_final_bullet_image, bg="#e3fdfd", command=ladakh, borderwidth=0)
    india_canvas.create_window(300,580, window=ladakh_button)

    daman_button=Button(local_frame, image=black_final_bullet_image, bg="#e3fdfd", command=dadra_nagarhaveli_daman_diu, borderwidth=0)
    india_canvas.create_window(282,455, window=daman_button)

    daman_button2=Button(local_frame, image=black_final_bullet_image, bg="#e3fdfd", command=dadra_nagarhaveli_daman_diu, borderwidth=0)
    india_canvas.create_window(250,445, window=daman_button2)

india_canvas=Canvas(local_frame, height=1000, width=1000, bg="#e3fdfd")
india_canvas.grid()

india_image=Image.open(r"C:\Users\riyan\Downloads\india-removebg-preview (1).png")
india_image_resize=india_image.resize((1000,800), Image.ANTIALIAS)
final_india_image=ImageTk.PhotoImage(india_image_resize)
india_canvas.create_image(0,0, anchor=NW, image=final_india_image)

bullet_image=Image.open(r"C:\Users\riyan\Downloads\circle-cropped (7).png")
bullet_image_resize=bullet_image.resize((20,20), Image.ANTIALIAS)
final_bullet_image=ImageTk.PhotoImage(bullet_image_resize)

medium_bullet_resize=bullet_image.resize((14,14), Image.ANTIALIAS)
medium_bullet_image=ImageTk.PhotoImage(medium_bullet_resize)

small_bullet_resize=bullet_image.resize((11,11), Image.ANTIALIAS)
small_bullet_image=ImageTk.PhotoImage(small_bullet_resize)

black_bullet_image=Image.open(r"C:\Users\riyan\OneDrive\Desktop\gui python(tkinter)\redtri.png")
black_bullet_image_resize=black_bullet_image.resize((15,15), Image.ANTIALIAS)
black_final_bullet_image=ImageTk.PhotoImage(black_bullet_image_resize)

red_bullet_image=Image.open(r"C:\Users\riyan\Downloads\circle-cropped (8).png")
red_bullet_image_resize=red_bullet_image.resize((20,20), Image.ANTIALIAS)
red_final_bullet_image=ImageTk.PhotoImage(red_bullet_image_resize)

red_medium_bullet_resize=red_bullet_image.resize((14,14), Image.ANTIALIAS)
red_medium_bullet_image=ImageTk.PhotoImage(red_medium_bullet_resize)

red_small_bullet_resize=red_bullet_image.resize((11,11), Image.ANTIALIAS)
red_small_bullet_image=ImageTk.PhotoImage(red_small_bullet_resize)


def on_enter(event):
    union_button['foreground']='blue'

def on_leave(event):
    union_button['foreground']='black'

union_button=Button(local_frame, text="View Union Territories", borderwidth=0 , bg="#e3fdfd", command=union_territory, fg="black", font=('Helvetica',14,'bold','underline'),highlightthickness=0, relief='ridge')
india_canvas.create_window(120,50, window=union_button)
union_button.bind("<Enter>", on_enter)
union_button.bind("<Leave>", on_leave)

def normal_text():
    india_canvas.create_text(900,680, text="TOTAL",font=('Helvetica',14,'bold','underline'), fill="black")
    local_frame.after(500, animate_text)

def animate_text():
    india_canvas.create_text(900,680, text="TOTAL",font=('Helvetica',14,'bold','underline'), fill="blue")
    local_frame.after(500, normal_text)

india_canvas.create_oval(850,650,950,750,fill="white")
india_canvas.create_text(900,680, text="TOTAL",font=('Helvetica',14,'bold','underline') )
local_frame.after(500, animate_text)
total=india_covid_df.loc['India','Total Cases']
india_canvas.create_text(900,715, text=total, font=('Helvetica',14,'bold'), fill="red")

def blue_bullet():
    goa_button=Button(local_frame, image=small_bullet_image, bg="#e3fdfd", command=goa, borderwidth=0)
    india_canvas.create_window(300,580, window=goa_button)

    hp_button=Button(local_frame, image=final_bullet_image, borderwidth=0, bg="#e3fdfd", command=himachal)
    india_canvas.create_window(375,145, window=hp_button)

    punjab_button=Button(local_frame, image=final_bullet_image, borderwidth=0, bg="#e3fdfd", command=punjab)
    india_canvas.create_window(335,180, window=punjab_button)

    uttarakhand_button=Button(local_frame, image=final_bullet_image, borderwidth=0, bg="#e3fdfd", command=uttarakhand)
    india_canvas.create_window(420,190, window=uttarakhand_button)

    haryana_button=Button(local_frame, image=final_bullet_image, borderwidth=0, bg="#e3fdfd", command=haryana)
    india_canvas.create_window(355,230, window=haryana_button)

    raja_button=Button(local_frame, image=final_bullet_image, borderwidth=0, bg="#e3fdfd", command=rajasthan)
    india_canvas.create_window(290,290, window=raja_button)

    up_button=Button(local_frame, image=final_bullet_image, borderwidth=0, bg="#e3fdfd", command=uttar_pradesh)
    india_canvas.create_window(450,280, window=up_button)

    bihar_button=Button(local_frame, image=final_bullet_image, borderwidth=0, bg="#e3fdfd", command=bihar)
    india_canvas.create_window(570,320, window=bihar_button)

    sikkim_button=Button(local_frame, image=small_bullet_image, borderwidth=0, bg="#e3fdfd", command=sikkim)
    india_canvas.create_window(627,265, window=sikkim_button)

    arunachal_button=Button(local_frame, image=final_bullet_image, borderwidth=0, bg="#e3fdfd", command=arunachal_pradesh)
    india_canvas.create_window(760,250, window=arunachal_button)

    assam_button=Button(local_frame, image=final_bullet_image, borderwidth=0, bg="#e3fdfd", command=assam)
    india_canvas.create_window(730,300, window=assam_button)

    nagaland_button=Button(local_frame, image=medium_bullet_image, borderwidth=0, bg="#e3fdfd", command=nagaland)
    india_canvas.create_window(766,305, window=nagaland_button)

    manipur_button=Button(local_frame, image=medium_bullet_image, borderwidth=0, bg="#e3fdfd", command=manipur)
    india_canvas.create_window(750,340, window=manipur_button)

    mizoram_button=Button(local_frame, image=medium_bullet_image, borderwidth=0, bg="#e3fdfd", command=mizoram)
    india_canvas.create_window(725,375, window=mizoram_button)

    tripura_button=Button(local_frame, image=small_bullet_image, borderwidth=0, bg="#e3fdfd", command=tripura)
    india_canvas.create_window(696,370, window=tripura_button)

    meghalaya_button=Button(local_frame, image=medium_bullet_image, borderwidth=0, bg="#e3fdfd", command=meghalaya)
    india_canvas.create_window(680,322, window=meghalaya_button)

    maharashtra_button=Button(local_frame, image=final_bullet_image, borderwidth=0, bg="#e3fdfd", command=maharashtra)
    india_canvas.create_window(350,470, window=maharashtra_button)

    gujarat_button=Button(local_frame, image=final_bullet_image, borderwidth=0, bg="#e3fdfd", command=gujarat)
    india_canvas.create_window(250,390, window=gujarat_button)

    mp_button=Button(local_frame, image=final_bullet_image, borderwidth=0, bg="#e3fdfd", command=madhya_pradesh)
    india_canvas.create_window(400,380, window=mp_button)

    chhattisgarh_button=Button(local_frame, image=final_bullet_image, borderwidth=0, bg="#e3fdfd", command=chhattisgarh)
    india_canvas.create_window(480,430, window=chhattisgarh_button)

    jharkhand_button=Button(local_frame, image=final_bullet_image, borderwidth=0, bg="#e3fdfd", command=jharkhand)
    india_canvas.create_window(555,380, window=jharkhand_button)

    wb_button=Button(local_frame, image=final_bullet_image, borderwidth=0, bg="#e3fdfd", command=west_bengal)
    india_canvas.create_window(610,380, window=wb_button)

    odisha_button=Button(local_frame, image=final_bullet_image, borderwidth=0, bg="#e3fdfd", command=odisha)
    india_canvas.create_window(550,440, window=odisha_button)

    karnatka_button=Button(local_frame, image=final_bullet_image, borderwidth=0, bg="#e3fdfd", command=karnatka)
    india_canvas.create_window(340,600, window=karnatka_button)

    telangana_button=Button(local_frame, image=final_bullet_image, borderwidth=0, bg="#e3fdfd", command=telangana)
    india_canvas.create_window(410,520, window=telangana_button)

    ap_button=Button(local_frame, image=final_bullet_image, borderwidth=0, bg="#e3fdfd", command=andhra_pradesh)
    india_canvas.create_window(415,580, window=ap_button)

    tn_button=Button(local_frame, image=final_bullet_image, borderwidth=0, bg="#e3fdfd", command=tamil_nadu)
    india_canvas.create_window(410,680, window=tn_button)

    kerala_button=Button(local_frame, image=small_bullet_image, borderwidth=0, bg="#e3fdfd", command=kerala)
    india_canvas.create_window(358,695, window=kerala_button)

blue_bullet()


def pressed_enter_key(event):
    question_asked=search_box.get().title().rstrip()
    if question_asked=="Usa" or question_asked=="Us":
        question_asked="USA"
    elif question_asked=="Uae":
        question_asked=question_asked.upper()
    elif question_asked=="Uk":
        question_asked=question_asked.upper()
    question_asked1=get_close_matches(question_asked, country_list, n=1, cutoff=0.7)

    if (len(question_asked1)!=0):
        try:
            question_asked=question_asked1[0]
            total_cases=covid_df.loc[question_asked, 'Total Cases']
            new_cases=covid_df.loc[question_asked,'New Cases']
            deaths=covid_df.loc[question_asked,'Total Deaths']
            total_recovered=covid_df.loc[question_asked,'Total Recovered']
            search_box.delete(0,END)
            covid_notebook.add(answer_frame, text="Search Results")
            covid_notebook.hide(3)
            answer_frame_canvas.grid(padx=200, pady=125)
            answer_frame_canvas.delete("delete_answer")
            answer_frame_canvas.create_rectangle(5,5,600,500,fill="#f2d6eb",outline="black", width=5, tag="delete_answer")
            answer_frame_canvas.create_text(300, 100, text= question_asked, font=('Roboto',20, 'bold','underline'), tag="delete_answer")
            answer_frame_canvas.create_text(300, 150, text="Total Cases: " + total_cases, font=('Roboto',18, 'bold'), tag="delete_answer")
            answer_frame_canvas.create_text(300, 200, text="New Cases : " + new_cases, font=('Roboto',18, 'bold'), tag="delete_answer", fill="red")
            answer_frame_canvas.create_text(300, 250, text="Total Deaths: " + deaths, font=('Roboto',18, 'bold'), tag="delete_answer")
            answer_frame_canvas.create_text(300, 300, text="Total Recovered: " + total_recovered, font=('Roboto',18, 'bold'),fill="green" ,tag="delete_answer")
            answer_frame_canvas.create_window(300, 400, window=back_button)

        except KeyError:
            covid_notebook.add(answer_frame, text="Search Results")
            covid_notebook.hide(3)
            answer_frame_canvas.grid(padx=200, pady=125)
            answer_frame_canvas.delete("delete_answer")
            answer_frame_canvas.create_rectangle(5,5,600,500,fill="#f2d6eb",outline="black", width=5, tag="delete_answer")
            search_box.delete(0,END)
            answer_frame_canvas.create_image(300, 200, image=error_final_image)
            messagebox.showerror("Not Found","Please enter a valid country/continent.")
            choose_search_frame()
    else:
        covid_notebook.add(answer_frame, text="Search Results")
        covid_notebook.hide(3)
        answer_frame_canvas.grid(padx=200, pady=125)
        answer_frame_canvas.delete("delete_answer")
        answer_frame_canvas.create_rectangle(5,5,600,500,fill="#f2d6eb",outline="black", width=5, tag="delete_answer")
        search_box.delete(0,END)
        answer_frame_canvas.create_image(300, 200, image=error_final_image)
        messagebox.showerror("Not Found","Please enter a valid country/continent.")
        choose_search_frame()



def choose_search_frame():
    covid_notebook.add(search_frame, text="Search")
    covid_notebook.hide(4)

search_image=Image.open(r"C:\Users\riyan\Downloads\mag-glass-removebg-preview-removebg-preview (1).png")
search_image_resize=search_image.resize((30,30), Image.ANTIALIAS)
search_final_image=ImageTk.PhotoImage(search_image_resize)

error_image=Image.open(r"C:\Users\riyan\Downloads\circle-cropped (9).png")
error_image_resize=error_image.resize((250,250), Image.ANTIALIAS)
error_final_image=ImageTk.PhotoImage(error_image_resize)

search_canvas=Canvas(search_frame, height=1000, width=1000, bg="#e3fdfd")
search_canvas.grid()

search_label1=Label(search_frame, text="S", font=('Roboto',45,'bold'), bg="#e3fdfd", fg="#4285F4")
search_canvas.create_window(430, 250, window=search_label1)

search_label2=Label(search_frame, text="e", font=('Roboto',45,'bold'), bg="#e3fdfd", fg="#DB4437")
search_canvas.create_window(470, 250, window=search_label2)

search_label3=Label(search_frame, text="a", font=('Roboto',45,'bold'), bg="#e3fdfd", fg="#F4B400")
search_canvas.create_window(510, 250, window=search_label3)

search_label4=Label(search_frame, text="r", font=('Roboto',45,'bold'), bg="#e3fdfd", fg="#4285F4")
search_canvas.create_window(545, 250, window=search_label4)

search_label5=Label(search_frame, text="c", font=('Roboto',45,'bold'), bg="#e3fdfd", fg="#0F9D58")
search_canvas.create_window(580 ,250, window=search_label5)

search_label6=Label(search_frame, text="h", font=('Roboto',45,'bold'), bg="#e3fdfd", fg="#DB4437")
search_canvas.create_window(615, 250, window=search_label6)

search_box=Entry(search_frame, font=('Helvetica','18'),width=40)
search_canvas.create_window(500, 340, window=search_box)
question_asked=search_box.get()
search_box.bind('<Return>', pressed_enter_key)

search_button=Button(search_frame, image=search_final_image, bg="white", borderwidth=0, command=lambda : pressed_enter_key(1))
search_canvas.create_window(758,340, window=search_button)

info_label=Label(search_frame, text="Enter a Country or Continent", font=('Roboto', 16, 'bold','underline'), bg="#e3fdfd", fg="black")
search_canvas.create_window(500, 400, window=info_label )

def navigate_first_tab():
    covid_notebook.select(0)

def search_normal_text():
    all_updates_button=Button(text="COVID-19 LIVE-UPDATES HERE",font=('Times New Roman', 30, 'bold', 'underline'),fg="#142850", bg="#e3fdfd", borderwidth=0,command=navigate_first_tab)
    search_canvas.create_window(510, 670, window=all_updates_button )
    search_frame.after(500, search_animate_text)

def search_animate_text():
    all_updates_button=Button(text="COVID-19 LIVE-UPDATES HERE",font=('Times New Roman', 30, 'bold', 'underline'),fg="#fe346e", bg="#e3fdfd",command=navigate_first_tab, borderwidth=0)
    search_canvas.create_window(510, 670, window=all_updates_button )
    search_frame.after(500, search_normal_text)

all_updates_button=Button(text="COVID-19 LIVE-UPDATES HERE",font=('Times New Roman', 30, 'bold', 'underline'),fg="#142850", bg="#e3fdfd", command=navigate_first_tab, borderwidth=0)
search_canvas.create_window(510, 670, window=all_updates_button )
search_frame.after(500, search_animate_text)


answer_frame_canvas=Canvas(answer_frame, height=500,width=600, bg="#f2d6eb")
back_button=Button(answer_frame, text="Back to Search", command=choose_search_frame, bg="white", fg="black", font=('Roboto',20,'bold'), borderwidth=1)


faq_frame_canvas=Canvas(faq_frame, height=600, width=600, bg="#f2d6eb")
faq_frame_canvas.grid(padx=200, pady=100)
faq_frame_canvas.create_rectangle(5,5,600,600,fill="#f2d6eb",outline="black", width=5)
faq_frame_canvas.create_text(300,75, text="COVID-19 FAQ", font=('Balsamiq Sans', 30, 'bold', 'underline'))
question_list=['What is the source of the virus?','How does the virus spread?','How can I protect myself?',
'What are the symptoms of COVID-19','What is the recovery time of the virus?', 'Can the virus spread through food?']

answer_list=['It is caused by a coronavirus called SARS-CoV-2, which are originated in bats. However the exact source is unknown.',
'Spreads mainly through respiratory droplets produced when an infected person coughs or sneezes. Spread is more likely when people are in close contact (within about 6 feet).',
'Wash hands often, avoid close contact, cover your mouth when areound people,clean and disinfect.',
'Fever, cough, shortness of breath, nausea, headache, sore throat, fatigue are some of the common symptoms.',
'They found that for people with mild disease, recovery time is about two weeks, while people with severe or critical disease recover within three to six weeks.',
'It is highly unlikely that people can contract COVID-19 from food or food packaging.']


def selected_question(event):
    option=faq_combo.get()
    faq_frame_canvas.delete("ans")
    for i in range(0,len(question_list)):
        if option==question_list[i]:
            index=i
            break
        
    answer=answer_list[index].split()
    one=""
    two=""
    three=""
    four=""
    if index==1 or index==4:
        for i in range(0,5):
            one=one + " " + answer[i]
        for i in range(5,10):
            two=two + " " + answer[i]
        for i in range(10,15):
            three=three + " " + answer[i]
        for i in range(15, len(answer)):
            four=four + " " + answer[i]
        faq_frame_canvas.create_text(300,150, text=one, font=('Helvetica',18,'bold'), tag="ans")
        faq_frame_canvas.create_text(300,200, text=two, font=('Helvetica',18,'bold'), tag="ans")
        faq_frame_canvas.create_text(300,250, text=three, font=('Helvetica',18,'bold'), tag="ans")
        faq_frame_canvas.create_text(300,300, text=three, font=('Helvetica',18,'bold'), tag="ans")
    else:
        for i in range(0,6):
            one=one + " " + answer[i]
        for i in range(6,12):
            two=two + " " + answer[i]
        for i in range(12,len(answer)):
            three=three + " " + answer[i]
        faq_frame_canvas.create_text(300,200, text=one, font=('Helvetica',18,'bold'), tag="ans")
        faq_frame_canvas.create_text(300,250, text=two, font=('Helvetica',18,'bold'), tag="ans")
        faq_frame_canvas.create_text(300,300, text=three, font=('Helvetica',18,'bold'), tag="ans")

    

faq_combo=ttk.Combobox(value=question_list, width=60, height=6, state='readonly')
faq_combo.bind("<<ComboboxSelected>>", selected_question)
faq_frame_canvas.create_window(300, 400, window=faq_combo)


root.mainloop()