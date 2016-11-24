from magichome_wifi import MagicHomeLEDController

responses = MagicHomeLEDController.scan(30)
for r in responses:
    print(r)