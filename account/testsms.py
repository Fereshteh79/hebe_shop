import ghasedakpack

sms = ghasedakpack.Ghasedak("")
sms.verification({'receptor': '09332382883', 'type': '1', 'template': 'randcode', 'parm1': '1234', 'parm2': 'hi'})