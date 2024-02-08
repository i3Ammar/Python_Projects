import requests
from bs4 import BeautifulSoup
import csv 
import datetime as dt 
import pandas as pd 
from os.path import join,expanduser,exists



desktop_dir = join(expanduser('~'),"Desktop")
file_path = join (desktop_dir,"yallakora_matches_details.csv")
today = dt.date.today()
print (f"Today date is : {today}")
print (f"Your desktop path is '{file_path}'\n")


def core_date():
    core = int(input("Choose 1 for today matches: \nChoose 2 for any date matches :\n"))

    try:
        if core != 2 and core != 1 : 
            print("Please select the right number : ")
            core_date()
        elif core == 1:
            page = requests.get(f'https://www.yallakora.com/Match-Center?date={today}')
        elif core == 2 : 
            date = input ("please enter a date in the following format: MM/DD/YYYY : " )
            page = requests.get(f'https://www.yallakora.com/Match-Center?date={date}')
        return page  
    except requests.exceptions.RequestException as e: 
        raise e


def get_match_info(championships)  :
    champion_title = championships.contents[1].find('h2').text.strip()
    all_matches = championships.contents[3].find_all('div', {"class" :"liItem"})
    number_of_matches = len(all_matches)

    for i in range (number_of_matches) :
        #get teams names
        team_A = all_matches[i].find("div",{"class" : "teamA"}).text.strip()
        team_B = all_matches[i].find("div",{"class" : "teamB"}).text.strip()
        
        #get score 
        match_result = all_matches[i].find("div",{"class":"MResult"}).find_all("span",{"class":"score"})
        score = f"{match_result[0].text.strip()} - {match_result[1].text.strip()}"
        
        #Get match time 
        match_time = all_matches[i].find("div",{"class":"MResult"}).find("span",{"class":"time"}).text.strip()
        
        #add match information to matches_details 
        matches_details.append({"نوع البطولة ":champion_title , "الفريق الاول":team_A,"الفريق الثاني":
                            team_B ,"ميعاد المباراة":match_time, "النتيجة": score})
if __name__ == '__main__': 
    src = core_date().content
    soup = BeautifulSoup(src , "lxml")
    matches_details = []
    championships =soup.find_all('div', {'class': 'matchCard'})
    
    for i in range(len(championships)):
        get_match_info(championships[i])
        
    keys = matches_details[0].keys()

    with open(file_path,"w",encoding="utf-8" )   as output_file :
            dict_writer = csv.DictWriter(output_file , keys) 
            dict_writer.writeheader()
            dict_writer.writerows(matches_details)    
            print("file created successfully")   
    df=pd.read_csv(file_path)
    df.to_excel("Matches.xlsx",index = False )