from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.exception import JSONRPCException
from iconsdk.builder.transaction_builder import CallTransactionBuilder, TransactionBuilder, DeployTransactionBuilder
from iconsdk.builder.call_builder import CallBuilder
from iconsdk.signed_transaction import SignedTransaction
from .repeater import retry


SCORE_ADDRESS = ''
icon_service = IconService(HTTPProvider("https://bicon.net.solidwallet.io",3))
RANDOM_ADDRESS = 'hx8b94a3792f336b71937709dae5487166c180c87a'

def get_score_addr(score_address):
	global SCORE_ADDRESS
	SCORE_ADDRESS = score_address

def get_icon_service(service):
	global icon_service
	service_dict = {
			"yeouido": IconService(HTTPProvider("https://bicon.net.solidwallet.io",3)),
			"euljiro": IconService(HTTPProvider("https://test-ctz.solidwallet.io", 2)),
			"pagoda": IconService(HTTPProvider("https://zicon.net.solidwallet.io",3)),
			"mainnet": IconService(HTTPProvider("https://ctz.solidwallet.io", 3))
		}
	icon_service = service_dict[service]

def external(fn_name: str, wallet, params=None):
	call_transaction = CallTransactionBuilder()\
			    .from_(wallet.get_address())\
			    .to(SCORE_ADDRESS)\
			    .nid(3)\
			    .nonce(100)\
			    .method(fn_name)\
			    .params(params)\
			    .build()
	transaction(call_transaction, wallet)


def payable(fn_name: str, wallet, value, params=None):
	call_transaction = CallTransactionBuilder()\
			    .from_(wallet.get_address())\
			    .to(SCORE_ADDRESS)\
			    .nid(3)\
			    .nonce(100)\
			    .value(value)\
			    .method(fn_name)\
			    .params(params)\
			    .build()
	transaction(call_transaction, wallet)


def readonly(fn_name: str, params=None):
	call = CallBuilder().from_(RANDOM_ADDRESS)\
	                    .to(SCORE_ADDRESS)\
	                    .method(fn_name)\
	                    .params(params)\
	                    .build()
	print(icon_service.call(call))


def transaction(call_transaction, wallet):
	estimate_step = icon_service.estimate_step(call_transaction)
	step_limit = estimate_step + 100000
	signed_transaction = SignedTransaction(call_transaction, wallet, step_limit)

	tx_hash = icon_service.send_transaction(signed_transaction)
	print(tx_hash)
	print(get_tx_result(tx_hash))


@retry(JSONRPCException, tries=10, delay=1, back_off=2)	
def get_tx_result(tx_hash):
  tx_result = icon_service.get_transaction_result(tx_hash)
  return tx_result