#!/usr/bin/env python3
class main:
	def clear(self):
		self.headersOutput.delete('1.0', 'end')

	def copy(self):
		self.app.clipboard_clear()
		self.app.clipboard_append(f'self.headers = {self.convertedVal}\n\nself.cookies = {self.cookieVal}')
		self.app.update()

	def convert(self):
		curlVal = self.curlEntry.get('1.0', 'end')
		try:
			if '--data-raw' in curlVal:
				curlVal = curlVal.split(' --data-raw ')[0]
			mode = self.mode.get()
			match mode:
				case 'firefox':
					cookieHeader = "-H 'Cookie: "
					self.convertedVal = ast.literal_eval('{' + ',\n'.join(curlVal.split(' -H ')[1:]).replace(': ', "': '") + '}')
					if 'Cookie' in self.convertedVal:
						self.convertedVal.pop('Cookie')
				case 'chrome':
					cookieHeader = "-H 'cookie: "
					self.convertedVal = ast.literal_eval('{' + ',\n'.join(curlVal.split(' -H ')[1:]).replace(': ', "': '") + '}')
					if 'cookie' in self.convertedVal:
						self.convertedVal.pop('cookie')
				case _:
					self.convertedVal = 'WHAT??? N/AW AINT NO WAY FR FR ONG BRUH'

			self.cookieVal = json.dumps(ast.literal_eval("{'" + "',\n'".join(curlVal.split(cookieHeader)[1].split(' -H ')[0].split('; ')).replace('=', "': '") + "}"), indent='\t')
			self.convertedVal = json.dumps(self.convertedVal, indent='\t')
		except SyntaxError as syntaxError:
		 	self.convertedVal = 'Error!'
		 	self.cookieVal = 'Error!'

		self.headersOutput.delete('1.0', 'end')
		self.headersOutput.insert('end', self.convertedVal)
		self.cookiesOutput.delete('1.0', 'end')
		self.cookiesOutput.insert('end', self.cookieVal)

	def __init__(self):
		self.app = ttk.Window(themename = 'vapor')
		self.app.iconphoto(False, ttk.PhotoImage(file = '~/code/python/curl2Headers/jeff.png'))
		self.app.title('Convert dev tools copy as curl to headers and cookies dictionary to be used in a python program for web scrapping etc')
		self.app.geometry('1300x600')
		self.app.resizable(False, False)
		self.convertedVal = None

		labelFrame = ttk.Frame(self.app, padding=5, width=500)

		convertButton = ttk.Button(labelFrame, text='Convert', command=self.convert)
		convertButton.pack(padx = 5, side='left')
		copyButton = ttk.Button(labelFrame, text='Copy', command=self.copy)
		copyButton.pack(padx = 5, side='left')
		clearButton = ttk.Button(labelFrame, text='Clear', command=self.clear)
		clearButton.pack(padx = 5, side='left')

		modes = [
			'firefox',
			'firefox',
			'chrome',
		]

		self.mode = ttk.StringVar()
		# self.mode.set('firefox')

		modeSelect = ttk.OptionMenu(labelFrame, self.mode, *modes)
		modeSelect.pack(padx = 5, side='left')

		labelFrame.pack()

		curlEntry = ttk.Labelframe(self.app, text='Curl Input:', padding=1)
		headersOutput = ttk.Labelframe(self.app, text='Headers: ', padding=1)
		cookiesOutput = ttk.Labelframe(self.app, text='Cookies: ', padding=1)

		self.curlEntry = ttk.Text(curlEntry, width=50, height=30)
		self.curlEntry.pack(side='left', padx=10, pady=10)
		self.headersOutput = ttk.Text(headersOutput, width=50, height=30)
		self.headersOutput.pack(side='left', padx=10, pady=10)
		self.cookiesOutput = ttk.Text(cookiesOutput, width=50, height=30)
		self.cookiesOutput.pack(side='left', padx=10, pady=10)

		curlEntry.pack(side='left')
		headersOutput.pack(side='left')
		cookiesOutput.pack(side='left')



		self.app.mainloop()

if __name__ == '__main__':
	import ttkbootstrap as ttk
	import json, ast
	main()
