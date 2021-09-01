print("Hello Duggy!")
import board
import displayio
import terminalio
import busio
import time
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
from adafruit_st7789 import ST7789
import adafruit_sht31d

i2c = busio.I2C(board.GP21,board.GP20)
sensor = adafruit_sht31d.SHT31D(i2c)

displayio.release_displays()
tft_cs = board.GP17
tft_dc = board.GP16
spi_mosi = board.GP19
spi_clk = board.GP18
spi = busio.SPI(spi_clk, MOSI=spi_mosi)


display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)

display = ST7789(display_bus, width=240, height=240, rowstart=80)
display.rotation = 180

# Make the display context
splash = displayio.Group(max_size=10)
display.show(splash)

color_bitmap = displayio.Bitmap(240, 240, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x000066

font = bitmap_font.load_font("/firacode72.bdf")

bg_sprite = displayio.TileGrid(color_bitmap,
                               pixel_shader=color_palette,
                               x=0, y=0)
splash.append(bg_sprite)

text_group = displayio.Group(max_size=10, scale=1, x=20, y=10)
humidity_value = label.Label(font, text="100%", color=0xFFFFFF)
humidity_value.y = 100
text_group.append(humidity_value)

text1 = "Logs & Ducks"
text2 = "Ducks & Logs"
text_area = label.Label(terminalio.FONT, text=text1, color=0xFFFF00)
text_group.append(text_area) # Subgroup for text scaling
splash.append(text_group)

while True:
    text_area.text = text2
    humidity_value.text = str(round(sensor.relative_humidity)) + "%"
    time.sleep(0.5)
    text_area.text = text1
    time.sleep(0.5)