# Multi-sized Font for Raspberry Pi Pico LCD/OLED Displays
# Existing framebuf library only supports 8*8 font size
# lcd_write method has been implemented in the LCD_1inch3
# class inside the lcd_lib.py file

from lcd_lib import LCD_1inch3
import network
import urequests
import secrets
import time

LCD = LCD_1inch3()

LCD.fill(LCD.black)

# Connect to WLAN
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.SSID, secrets.PASSWORD)
while not wlan.isconnected():
    pass
print('Connected to WLAN')

while True:
    # Make GivEnergy API call to get Inverter data
    url = "https://api.givenergy.cloud/v1/inverter/"+secrets.INVERTER+"/system-data/latest"
    headers = {
      'Authorization': 'Bearer '+ secrets.API_KEY,
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }

    response = urequests.request('GET',url,headers=headers)
    data = response.json()
    batt_lvl = data['data']['battery']['percent']
    pwr_lvl = data['data']['battery']['power']
    print(batt_lvl)
    print(pwr_lvl) 
    LCD.fill(LCD.black)
    LCD.write_text('Battery',x=10,y=10,size=4,color=LCD.white)
    if (batt_lvl <= 10):
        LCD.write_text(str(batt_lvl)+"%",x=10,y=50,size=7,color=LCD.red)
    elif (batt_lvl > 10):
        LCD.write_text(str(batt_lvl)+"%",x=10,y=50,size=7,color=LCD.green)
    LCD.write_text(str(pwr_lvl)+"W",x=10,y=105,size=4,color=LCD.blue)
    LCD.show()
    time.sleep(30)







        
