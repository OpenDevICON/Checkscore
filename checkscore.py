from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from IPython.core.getipython import get_ipython
from .methods import get_score_addr, get_icon_service
import requests
import json

shell = get_ipython()
icon_service = IconService(HTTPProvider("https://bicon.net.solidwallet.io",3))

class Checkscore(object):

	def __init__(self, score_address, service: str = "yeouido"):
		super(Checkscore, self).__init__()
		get_score_addr(score_address)
		service_dict = {
			"yeouido": IconService(HTTPProvider("https://bicon.net.solidwallet.io",3)),
			"euljiro": IconService(HTTPProvider("https://test-ctz.solidwallet.io", 2)),
			"pagoda": IconService(HTTPProvider("https://zicon.net.solidwallet.io",80)),
			"mainnet": IconService(HTTPProvider("https://ctz.solidwallet.io", 3))
		}
		if service == "euljiro":
			icon_service = service_dict["euljiro"]
		elif service == "pagoda":
			icon_service = service_dict["pagoda"]
		elif service == "mainnet":
			icon_service = service_dict["mainnet"]
		else:
			icon_service = service_dict["yeouido"]

		get_icon_service(service)	
		self.score_apis = icon_service.get_score_api(score_address)

	def fill_methods(self):
		# remove fallback functions and eventlogs
		filtrd_fns = []
		for i in self.score_apis:
			if i['type'] == "function":
				filtrd_fns.append(i)

		# filter external, readonly and payable functions and reverse them 
		readonly_fns = reversed([d for i,d in enumerate(filtrd_fns) if 'readonly' in d])
		payable_fns = reversed([d for i,d in enumerate(filtrd_fns) if 'payable' in d])
		# for external, filter out payable functions, and then filter out readonly functions
		not_payable_fns = ([d for i,d in enumerate(filtrd_fns) if not 'payable' in d])
		external_fns = reversed([d for i,d in enumerate(not_payable_fns) if not 'readonly' in d])
        
		# loop through the functions, pass function name and input parameters
		for i in payable_fns:
			self.payable_function_content(i['name'],[(j['name'], j['type']) for j in i['inputs']])

		self.executable_markdown_cell("## Payable functions") 
		for i in external_fns:
			self.external_function_content(i['name'],[(j['name'], j['type']) for j in i['inputs']])

		self.executable_markdown_cell("## External Functions")
		for i in readonly_fns:
			self.readonly_function_content(i['name'],[(j['name'], j['type']) for j in i['inputs']])

		self.executable_markdown_cell("## Readonly functions")

	def external_function_content(self, fn_name:str, params:list):
		# no parameters
		parameters = ""
		fn = f"method = '{fn_name}'"  +"\n"
		wallet = "wallet = deployer_wallet" + "\n"
		# if there are parameters
		if params:
			attribs = {}
			for i in params:
				if i[1] == "int":
					attribs[i[0]] = 0
				else:
					attribs[i[0]] = ''
			parameters = (f'params = {str(attribs)}\n\n')

		self.create_new_cell(fn, wallet, parameters, None, "external")

	def payable_function_content(self,fn_name:str, params:list):
		fn = f"method = '{fn_name}'"  +"\n"
		wallet = "wallet = deployer_wallet" + "\n"
		parameters = ""
		val = "value = "
		if params:
			attribs = {}
			for i in params:
				if i[1] == "int":
					attribs[i[0]] = 0
				else:
					attribs[i[0]] = ''
			parameters = (f'params = {str(attribs)}\n\n')		

		self.create_new_cell(fn, wallet, parameters, val, "payable")

	def readonly_function_content(self,fn_name:str, params:list):
		fn = f"method = '{fn_name}'"  +"\n"
		parameters = ""
		if params:
			attribs = {}
			for i in params:
				if i[1] == "int":
					attribs[i[0]] = 0
				else:
					attribs[i[0]] = ''
			parameters = (f'params = {str(attribs)}\n\n')

		self.create_new_cell_readonly(fn, parameters)

	def create_new_cell_readonly(self, fn, parameters):
		if parameters != "":
			call = "readonly(method, params)"
		else:
			call = "readonly(method)"

		contents = parameters + fn  + '\n' + call
		payload = dict(
			source='set_next_input',
			text=contents,
			replace=False,
		)
		shell.payload_manager.write_payload(payload, single=False)

	def create_new_cell(self, fn, wallet, parameters, val:None, fn_type):
		if parameters != "":
			if fn_type == "external":
				call = "external(method, wallet, params)"
			if fn_type == "payable":
				call = "payable(method, wallet, value, params)"

			if val:
				contents = parameters + fn + wallet + val + "\n" + call
			else:
				contents = parameters + fn + wallet + "\n" + call
		else:
			if fn_type == "external":
				call = "external(method, wallet)"
			if fn_type == "payable":
				call = "payable(method, wallet, value)"

			if val:
				contents = fn + wallet + val + "\n" + call
			else:
				contents = fn + wallet + "\n" + call

		payload = dict(
			source='set_next_input',
			text=contents,
			replace=False,
		)
		shell.payload_manager.write_payload(payload, single=False)

	def executable_markdown_cell(self, contents):
		payload = dict(
			source='set_next_input',
			text=contents,
			replace=False,
		)
		shell.payload_manager.write_payload(payload, single=False)