from app.models.schema import (
    InputQuery,
    Operation_Hours,
    Day_Operation_Time,
    Crowd_Time,
    Crowd_Days,
    About_Validated,
    General_Information,
    Crowd_Level,
    Operation_Time,
    About,
    About_Entries,
    Crowd_Level_Entries,
    Operation_Time_Entries
 )
from app.scrapers.scrape import Scrape_Resto

from app.models.models import General_information, Operation_time, Crowd_level, About_Table

from app.models.database import get_session

import itertools

def get_param(parameter:InputQuery):
    parameter_dict=parameter.dict()
    kecamatan=parameter_dict['kecamatan']
    kota=parameter_dict['kota']
    provinsi=parameter_dict['provinsi']
    resto_id=parameter_dict['resto_id']
    return kecamatan, kota, provinsi, resto_id

def scrape_resto(parameter:InputQuery):
    kecamatan, kota, provinsi, resto_id=get_param(parameter)
    trial=Scrape_Resto(kecamatan=kecamatan,kota=kota,provinsi=provinsi,resto_id=resto_id)
    data=trial.scrape_resto_data()
    list_operation_time=[]
    list_crowd_level=[]
    list_general_information=[]
    list_about=[]

    for resto in data:
        if type(resto['operation_time']) == float:
            resto['operation_time']=None
        else:
            for days, hours in resto['operation_time'].items():
                hours_validated=Operation_Hours(**hours)
                resto['operation_time'][days]=hours_validated
            resto['operation_time']=Day_Operation_Time(**resto['operation_time'])

    for resto in data:
        if resto['crowd_level']== {}:
            resto['crowd_level']=None
        else:
            for days, hours in resto['crowd_level'].items():
                hours_validated=Crowd_Time(**hours)
                resto['crowd_level'][days]=hours_validated
            resto['crowd_level']=Crowd_Days(**resto['crowd_level'])

    for resto in data:
        if resto['rating_numbers']==0:
            resto['resto_rating']=0
        else:
            continue

    for resto in data:
        if resto['about']=={}:
            resto['about']=None
        else:
            resto['about']=About_Validated(**resto['about'])

    for resto in data:
        general_information_validated=General_Information(**resto)
        crowd_level_validated=Crowd_Level(**resto)
        operation_time_validated=Operation_Time(**resto)
        about_validated=About(**resto)
        list_operation_time.append(operation_time_validated)
        list_crowd_level.append(crowd_level_validated)
        list_general_information.append(general_information_validated)
        list_about.append(about_validated)
        
    list_gi_entries = store_general_information(list_general_information=list_general_information)
    list_new_ot_entries = store_operation_time_entries(list_operation_time=list_operation_time)
    list_new_cl_entries = store_crowd_level_entries(list_crowd_level=list_crowd_level)
    list_new_about_entries = store_about_entries(list_about=list_about)

    list_all_entries=list(itertools.chain(list_gi_entries,list_new_ot_entries,list_new_cl_entries,list_new_about_entries))
    with get_session(cleanup=False) as session:
        session.add_all(list_all_entries) 
        session.commit()

    number_of_record=len(list_general_information)
    last_resto_id=list_general_information[number_of_record-1].resto_id
    message=f'{number_of_record} resto has been scraped and store in database with last id{last_resto_id}'
    

def store_about_entries(list_about):
    list_new_about_entries=[]
    for abot in list_about:
        resto=abot.dict()
        if resto['about']:
            for title, content in resto['about'].items():
                for i,v in enumerate(content):
                    resto_id=resto['resto_id']
                    type_about=title
                    seq=i+1
                    about_values=v
                    entries=About_Entries(resto_id=resto_id,type_about=type_about,seq=seq,about_values=about_values)
                    new_entries=About_Table(**entries.dict())
                    list_new_about_entries.append(new_entries)
        else:
            continue
    return list_new_about_entries

def store_operation_time_entries(list_operation_time):
    list_new_ot_entries=[]
    for ops_time in list_operation_time:
        resto=ops_time.dict()
        if resto['operation_time']:
            for key, values in resto['operation_time'].items():
                resto_id=resto['resto_id']
                days = key
                open_hour = values['open_hour']
                close_hour = values['close_hour']
                entries=Operation_Time_Entries(resto_id=resto_id,days=days,open_hour=open_hour,close_hour=close_hour)
                new_entries=Operation_time(**entries.dict())
                list_new_ot_entries.append(new_entries)
        else:
            continue
    return list_new_ot_entries

def store_crowd_level_entries(list_crowd_level ):
    list_new_cl_entries=[]
    for crowd in list_crowd_level:
        resto=crowd.dict()
        if resto['crowd_level']:
            for days,hours in resto['crowd_level'].items():
                for jam, level in hours.items():
                    resto_id=resto['resto_id']
                    day=days
                    hour=jam
                    crowd_time_level=level
                    entries=Crowd_Level_Entries(resto_id=resto_id,day=day,hour=hour,crowd_time_level=crowd_time_level)
                    new_entries=Crowd_level(**entries.dict())
                    list_new_cl_entries.append(new_entries)
        else:
            continue
    return list_new_cl_entries

def store_general_information(list_general_information):
    list_gi_entries=[]
    for gi in list_general_information:
        new_entries=General_information(**gi.dict())
        list_gi_entries.append(new_entries)
    return list_gi_entries




 

    


