from pydantic import BaseModel,validator, Field
from datetime import time
from typing import Optional, Union

#Input Parameter
class InputQuery(BaseModel):
    kecamatan: str 
    kota: str 
    provinsi: str 
    resto_id: int 
        
class General_Information(BaseModel):
    resto_id: int 
    resto_name: str
    resto_type: str
    resto_address: str
    resto_rating: Optional[Union[float, None]]
    rating_numbers: int
    resto_link:str

class Operation_Hours(BaseModel):
    open_hour: time
    close_hour: time
        
    @validator('open_hour')
    def validate_opem_time(cls, value):
        if isinstance(value, time):
            return value
        try:
            parsed_time = time.fromisoformat(value)
            return parsed_time
        except ValueError:
            raise ValueError("Invalid time format. Must be in HH:MM format.")
            
    @validator('close_hour')
    def validate_close_time(cls, value):
        if isinstance(value, time):
            return value
        try:
            parsed_time = time.fromisoformat(value)
            return parsed_time
        except ValueError:
            raise ValueError("Invalid time format. Must be in HH:MM format.")
        
class Day_Operation_Time(BaseModel):
    senin: Operation_Hours
    selasa: Operation_Hours
    rabu: Operation_Hours
    kamis: Operation_Hours
    jumat: Operation_Hours
    sabtu: Operation_Hours
    minggu: Operation_Hours
        
class Operation_Time(BaseModel):
    resto_id: int
    operation_time: Optional[Day_Operation_Time]
        
class Crowd_Time(BaseModel):
    am0: Optional[int]
    am1: Optional[int]
    am2: Optional[int]
    am3: Optional[int] 
    am4: Optional[int] 
    am5: Optional[int] 
    am6: Optional[int]
    am7: Optional[int]
    am8: Optional[int]
    am9: Optional[int]
    am10: Optional[int]
    am11: Optional[int]
    pm12: Optional[int]
    pm13: Optional[int]
    pm14: Optional[int]
    pm15: Optional[int]
    pm16: Optional[int] 
    pm17: Optional[int]
    pm18: Optional[int] 
    pm19: Optional[int]
    pm20: Optional[int]
    pm21: Optional[int] 
    pm22: Optional[int]
    pm23: Optional[int] 

class Crowd_Days(BaseModel):
    senin: Optional[Crowd_Time]=Field(default_factory=dict)
    selasa: Optional[Crowd_Time]=Field(default_factory=dict)
    rabu: Optional[Crowd_Time]=Field(default_factory=dict)
    kamis: Optional[Crowd_Time]=Field(default_factory=dict)
    jumat: Optional[Crowd_Time]=Field(default_factory=dict)
    sabtu: Optional[Crowd_Time]=Field(default_factory=dict)
    minggu: Optional[Crowd_Time]=Field(default_factory=dict)
    
class Crowd_Level(BaseModel):
    resto_id:int
    crowd_level:Optional[Union[Crowd_Days, None]]
        
class About_Validated(BaseModel):
    opsi_layanan: Optional[list[str]]=Field(default_factory=list)
    penawaran: Optional[list[str]]=Field(default_factory=list)
    pilihan_makan:Optional[list[str]]=Field(default_factory=list)
    fasilitas: Optional[list[str]]=Field(default_factory=list)
    suasana: Optional[list[str]]=Field(default_factory=list)
    tipe_pengunjung: Optional[list[str]]=Field(default_factory=list)
    perencanaan: Optional[list[str]]=Field(default_factory=list)
    pembayaran: Optional[list[str]]=Field(default_factory=list)

class About(BaseModel):
    resto_id: int
    about: Optional[Union[About_Validated, None]] 

class Operation_Time_Entries(BaseModel):
    resto_id: int
    days: str
    open_hour: time
    close_hour: time
        
class Crowd_Level_Entries(BaseModel):
    resto_id: int
    day: str
    hour: str
    crowd_time_level: Optional[Union[float, None]]

class About_Entries(BaseModel):
    resto_id: int
    type_about: str
    seq: int
    about_values: str