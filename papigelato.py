import json
import os
import tkinter
from tkinter import ttk
from tkinter.messagebox import showinfo, askyesno
import accounts_omac

defaultBonnetje = '''-=Chupapi Munyanyo=-
-----------------------------------------
Thanks for shopping, here is your receipt
-----------------------------------------'''


if os.path.isfile(f"papi.json"):
    with open(f"papi.json") as json_file_cardsCreation:
        dataString_cardsCreation = json.load(json_file_cardsCreation)
        #this makes it so if u use a json beautifier that makes it not being a string anymore, it would still work
        if type(dataString_cardsCreation) == dict:
            configData = dataString_cardsCreation
        else:
            configData = json.loads(dataString_cardsCreation)
    
    ######################## Basic JSON Creation ########################

else:
    configData = {'smaken':['Aardbei', 'Chocolade', 'Vanille', 'Banaan', 'Kaas', 'Goud'],
                    'prijs': {'liter': 9.8, 'bolletje': 0.95},
                    'extraPrijs': {'Goud': {'bolletje':60023, 
                                            'liter': 960368}, 
                                    'Oude kaas': {'bolletje':1, 
                                                    'liter': 10}},
                    'extraTypes':{'Kaas': ['Oude kaas', 'Jonge kaas']},
                    'opslag': {'Hoorntje': {'maximaal': 3, 
                                            'prijs': 1.25},
                                'Bakje': {'maximaal': 8, 
                                            'prijs': 0.75},
                                'Je handen':{'maximaal': 2, 
                                        'prijs': 0},
                                'Plastic vorkje':{'maximaal': 1, 
                                        'prijs': 0.25}},
                    'topping': {'Geen': {'typePrijs': 'totaal', 
                                            'prijs': {'Hoorntje': 0,
                                                        'Bakje': 0,
                                                        'Je handen': 0,
                                                        'Plastic vorkje':0}},
                                'ChocoladeSaus': {'typePrijs': 'totaal', 
                                                'prijs': {'Hoorntje': 1,
                                                            'Bakje': 1,
                                                            'Je handen': 1,
                                                            'Plastic vorkje':1}},
                                'Sprinkles': {'typePrijs': 'perBolletje', 
                                                'prijs': {'Hoorntje': 0.5,
                                                            'Bakje': 0.5,
                                                            'Je handen': 0.5,
                                                            'Plastic vorkje':0.5}},
                                'CaramelSaus': {'typePrijs': 'totaal', 
                                                'prijs': {'Hoorntje': 1,
                                                            'Bakje': 1.5,
                                                            'Je handen': 2,
                                                            'Plastic vorkje':2}}},
                    'maxBolletjes': 8,
                    'maxLiter':69,
                    'minLiter':5}

    json_string_configDat = json.dumps(configData)
    with open(f"papi.json", 'w') as outfile:
        json.dump(json_string_configDat, outfile)

typeOpslag = configData['opslag']
smaken = configData['smaken']
order = 0
orders = {}
extraTypes = configData['extraTypes']

#to not get those nasty index out of range errors, you try to get item 20 out of 19 items, this will return you item 0
def noIndexError(number, maxNumber, minNumber = 0):
    '''to not get those nasty index out of range errors, you try to get item 20 out of 19 items, this will return you item 0'''
    while number > maxNumber or number < minNumber:
        if number > maxNumber:
            number -= (maxNumber- minNumber)+1
        elif number < minNumber:
            number += (maxNumber - minNumber) + 1
    return number

def on_closing(windowTitles = 'Accounts_omac_lib'):
    if askyesno(windowTitles, f"Your program will be terminated\nShould we proceed?", icon ='warning'):
        exit()

def YNvraag(vraag, type = 'info'):
    if askyesno('<3', vraag, icon =type):
        return True

def selectOption(vraag,optionList):
    window = tkinter.Tk()
    def submit():
        window.destroy()
    selected = tkinter.StringVar()
    maximum = 4
    for x in range(len(optionList)):
        exec(f'radiobutton_{accounts_omac.removeCharacters(optionList[x])} = ttk.Radiobutton(window, text="{optionList[x]}", value="{optionList[x]}", variable=selected)')
        exec(f'radiobutton_{accounts_omac.removeCharacters(optionList[x])}.grid(column={x - (((x) // maximum)*maximum)}, row={(x // maximum)+1}, ipadx=20, ipady=10, sticky="EW")')
    tkinter.Label(window,text = vraag).grid(column=0, row=0, ipadx=20, ipady=10, sticky="EW", columnspan=4)
    ttk.Button(window,text='Next',command = submit).grid(column=0, row=(x // maximum)+2, ipadx=20, ipady=10, sticky="EW", columnspan=4)
    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.mainloop()
    return selected.get()

def aantalVraag(vraag,max = 1000,min = 1):
    def submit():
        window.destroy()  
    window = tkinter.Tk()
    tkinter.Label(window,text = vraag).grid(column=0, row=0, ipadx=20, ipady=10, sticky="EW")
    guessNumber = tkinter.IntVar()
    guessNumber.set(min)
    spinbox = ttk.Spinbox(window, from_=min,to=max,textvariable=guessNumber,wrap=True, state = 'readonly')
    spinbox.grid(column=0, row=1, ipadx=20, ipady=10, sticky="EW")
    ttk.Button(window,text='Next',command = submit).grid(column=0, row=2, ipadx=20, ipady=10, sticky="EW")
    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.mainloop()
    return guessNumber.get()

zakelijk = YNvraag(f"is dit een zakelijke bestelling?")

def smaakBestel(typeOfOrder, x):
    global orders
    temporarelySmaak = selectOption(f'voor {typeOfOrder} {x + 1}, welke smaak wil je?', smaken)
    while temporarelySmaak in extraTypes:
        temporarelySmaak = selectOption(f'voor {typeOfOrder} {x + 1}, welk type {temporarelySmaak} wil je?', extraTypes[temporarelySmaak])
    orders[f'order {order}'][f'{typeOfOrder} {x}'] = temporarelySmaak

def berekenBonnetje(orders):
    prijsVanIjs = 0
    literPrijs = 0
    extraKosten = 0
    if orders[list(orders.keys())[0]]['aantalLiter'] != 0:
        for x in range(orders[list(orders.keys())[0]]['aantalLiter']):
            prijsVanIjs += configData['prijs']['liter']
            literPrijs += configData['prijs']['liter']
            if orders[list(orders.keys())[0]][f'liter {x}'] in configData['extraPrijs']:
                prijsVanIjs += configData['extraPrijs'][orders[list(orders.keys())[0]][f'liter {x}']]['liter']
                extraKosten += configData['extraPrijs'][orders[list(orders.keys())[0]][f'liter {x}']]['liter']
            print(prijsVanIjs)
        receipt = f'{defaultBonnetje}\nLiter = {orders[list(orders.keys())[0]]["aantalLiter"]} x {configData["prijs"]["liter"]} = €{literPrijs}'


        if extraKosten > 0:
            receipt += f'\nIceType = €{round(extraKosten,2)}'
        
    else:
        bolletjes = 0
        bolletjePrijs = 0
        opslagPrijs = 0
        toppingPrijs = 0
        for y in range(len(list(orders.keys()))):
            for x in range(orders[list(orders.keys())[y]]['aantalBolletjes']):
                bolletjes += 1
                prijsVanIjs += configData['prijs']['bolletje']
                bolletjePrijs += configData['prijs']['bolletje']
                if orders[list(orders.keys())[y]][f'bolletje {x}'] in configData['extraPrijs']:
                    prijsVanIjs += configData['extraPrijs'][orders[list(orders.keys())[y]][f'bolletje {x}']]['bolletje']
                    extraKosten += configData['extraPrijs'][orders[list(orders.keys())[y]][f'bolletje {x}']]['bolletje']
            opslagPrijs += configData['opslag'][orders[list(orders.keys())[y]]['opslag']]['prijs']
            prijsVanIjs += configData['opslag'][orders[list(orders.keys())[y]]['opslag']]['prijs']
            if configData['topping'][orders[list(orders.keys())[y]]['topping']]['typePrijs'] == 'totaal':
                toppingPrijs += configData['topping'][orders[list(orders.keys())[y]]['topping']]['prijs'][orders[list(orders.keys())[y]]['opslag']]
                prijsVanIjs += configData['topping'][orders[list(orders.keys())[y]]['topping']]['prijs'][orders[list(orders.keys())[y]]['opslag']]
            elif configData['topping'][orders[list(orders.keys())[y]]['topping']]['typePrijs'] == 'perBolletje':
                toppingPrijs += (configData['topping'][orders[list(orders.keys())[y]]['topping']]['prijs'][orders[list(orders.keys())[y]]['opslag']]*orders[list(orders.keys())[y]]['aantalBolletjes'])
                prijsVanIjs += (configData['topping'][orders[list(orders.keys())[y]]['topping']]['prijs'][orders[list(orders.keys())[y]]['opslag']]*orders[list(orders.keys())[y]]['aantalBolletjes'])


        receipt = defaultBonnetje
        receipt += f'\nBolletjes = {bolletjes} x {configData["prijs"]["bolletje"]} = €{bolletjePrijs}'
        if extraKosten > 0:
            receipt += f'\nIceType = €{round(extraKosten,2)}'
        if opslagPrijs > 0:
            receipt += f'\nOpslag = €{round(opslagPrijs,2)}'
        if toppingPrijs > 0:
            receipt += f'\nTopping = €{round(toppingPrijs,2)}'     


    receipt += f'\nTotal = €{round(prijsVanIjs,2)}'
    showinfo('<3',receipt)





while True:
    if zakelijk:
        aantalLiter = aantalVraag('Hoeveel liter wilt u?',configData['maxLiter'],configData['minLiter'])
        orders[f'order {order}'] = {'aantalLiter':aantalLiter, 'aantalBolletjes':0}
        for x in range(aantalLiter):
            smaakBestel('liter', x)
        break
    else:
        aantalBolletjes = aantalVraag('Hoeveel bolletjes wilt u?',configData['maxBolletjes'],1)
        orders[f'order {order}'] = {'aantalLiter':0,'aantalBolletjes':aantalBolletjes}
        for x in range(aantalBolletjes):
            smaakBestel('bolletje', x)

        availableOpslag = []
        for x in range(len(configData['opslag'].keys())):
            keys = list(configData['opslag'].keys())
            if configData['opslag'][keys[x]]['maximaal'] >= aantalBolletjes:
                availableOpslag.append(keys[x])
        
        opslag = selectOption(f'Waarin/waarop wilt u de bolletjes?', availableOpslag)
        orders[f'order {order}'][f'opslag'] = opslag

        availableTopping = []
        for x in range(len(configData['topping'].keys())):
            keys = list(configData['topping'].keys())
            availableTopping.append(keys[x])
        topping = selectOption(f'Welke topping wilt u?', availableTopping)
        orders[f'order {order}'][f'topping'] = topping
        
        if not YNvraag(f"wilt u nog iets bestellen?"):
            break
        order += 1
print(orders)
berekenBonnetje(orders)