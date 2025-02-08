import ghasedakpack

sms = ghasedakpack.Ghasedak("")
sms.verification({'receptor': '09332382883', 'type': '1', 'template': 'randcode', 'param1': '1234', 'param2': 'hi'})