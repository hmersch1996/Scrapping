from utils import *
from datetime import datetime
from sqlalchemy import create_engine
import pandas as pd

URL = 'https://www.bristol.com.py/82-celulares'
TODAY = datetime.today()

engine = create_engine("sqlite:///database.db")

driver = initChrome()
driver.get(URL)

items = driver.find_elements(By.CLASS_NAME,"item")


df = pd.DataFrame(columns=['nombre','contado','cant_cuotas','precio_cuotas','imagen','url','fecha'])


for item in items:
    if 'swiper-slide' in item.get_attribute("class"):
        continue
    title = item.find_element(By.CLASS_NAME,"product_name").text
    [price, fees] = [x.text for x in item.find_elements(By.CLASS_NAME,"product-price-and-shipping")]
    img = item.find_element(By.TAG_NAME,"img").get_attribute("data-src")
    link = item.find_element(By.TAG_NAME,"a").get_attribute("href")
    fee_price = fees.split('X')[1].strip().replace('.','')
    fees = '18'
    
    
    df.loc[len(df),:] = [title,price,fees,fee_price,img,link,TODAY]


print('Completada la obtencion de datos')
print(df.head())

df.to_sql('scrapping_temp',engine,index=False)

print('Se subió con éxito a la base de datos')
sleep(10)
driver.close()