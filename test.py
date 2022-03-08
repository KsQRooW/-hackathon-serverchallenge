from modules.class_Supplier import Supplier
from pprint import pprint

supplier_browser = Supplier()
testData = (
    '4501099809',
    '7814493534',
    '2130045038',
    '0245014096',
    '7816658559',

)
for temp in testData:
    supplier_browser.inn = temp
    if supplier_browser.parse_supplier_data():
        pprint(supplier_browser.supplier_data)
