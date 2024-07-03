#speedtest Nizenkovskiy

import customtkinter
import speedtest
import os
import pathlib
import requests
import time
from threading import Thread
from PIL import Image, ImageTk

version = '1.0.0'

customtkinter.set_appearance_mode('light')

app = customtkinter.CTk()
app.resizable(False, False)
app.iconbitmap(os.path.join(pathlib.Path(__file__).parent.resolve(), 'icon.ico'))

def humansize(nbytes):

	suffixes = ['Бит', 'Кбит', 'Мбит', 'Гбит', 'Тбит']

	i = 0

	while nbytes >= 1024 and i < len(suffixes)-1:
		nbytes /= 1024.
		i += 1

	f = ('%.2f' % nbytes).rstrip('0').rstrip('.')

	return f"{f} {suffixes[i]}"

class TritelSpeedtest:

	def __init__(self):
		self.st = speedtest.Speedtest()

	def download_speed(self):
		return humansize(self.st.download())

	def upload_speed(self):
		return humansize(self.st.upload())

	def latency(self):

		latency_list = []

		for _ in range(5):

			try:

				t0 = time.time()

				requests.get("https://vk.com/", timeout=1)

				t1 = time.time()

				latency_list.append( round((t1-t0) * 100) )

			except:
				pass

		return str(round(sum(latency_list) / len(latency_list))) + " мс" if latency_list else "Ошибка"

class Menu:

	def __init__(self):

		self.buildTitle()

		app.title(f"Tritel Speedtest v{version}")
		app.geometry("600x500")

		self.buildStartButton()

	def destroyAll(self):

		for widget in app.winfo_children():
			widget.destroy()

	def buildTitle(self):

		self.appname_label = customtkinter.CTkLabel(app, text='Tritel Speedtest', font=("Courier", 20), text_color="red")
		self.appname_label.place(x=200, y=10)

		self.version_label = customtkinter.CTkLabel(app, text=f'v{version}', font=("Courier", 20))
		self.version_label.place(x=260, y=35)

	def buildStartButton(self):

		self.button_img = customtkinter.CTkImage(Image.open(os.path.join(pathlib.Path(__file__).parent.resolve(), 'start_button.png')), size=(193, 197))

		self.start_button = customtkinter.CTkButton(app, image=self.button_img, text="", fg_color="gray92", hover=False, command=lambda: Thread(target=self.buildSpeedtest).start())
		self.start_button.place(x=200, y=225)

	def buildSpeedtest(self):

		self.destroyAll()
		self.buildTitle()

		self.label1 = customtkinter.CTkLabel(app, text="Скорость скачивания:", font=("Courier", 16))
		self.label1.place(x=10, y=80)

		self.label2 = customtkinter.CTkLabel(app, text="Скорость загрузки:", font=("Courier", 16))
		self.label2.place(x=400, y=80)

		self.label3 = customtkinter.CTkLabel(app, text="Время задержки:", font=("Courier", 16))
		self.label3.place(x=225, y=100)

		self.latency_label = customtkinter.CTkLabel(app, text="Вычисление...", font=("Courier", 20))
		self.latency_label.place(x=225, y=120)

		self.download_speed_label = customtkinter.CTkLabel(app, text="", font=("Courier", 20))
		self.download_speed_label.place(x=10, y=100)

		self.upload_speed_label = customtkinter.CTkLabel(app, text="", font=("Courier", 20))
		self.upload_speed_label.place(x=400, y=100)

		self.tritel = TritelSpeedtest()

		self.latency = self.tritel.latency()
		self.latency_label.configure(text=self.latency)

		self.download_speed_label.configure(text="Вычисление...")
		self.download_speed = self.tritel.download_speed()
		self.download_speed_label.configure(text=self.download_speed)

		self.upload_speed_label.configure(text="Вычисление...")
		self.upload_speed = self.tritel.upload_speed()
		self.upload_speed_label.configure(text=self.upload_speed)

		self.buildStartButton()

menu = Menu()

app.mainloop()
