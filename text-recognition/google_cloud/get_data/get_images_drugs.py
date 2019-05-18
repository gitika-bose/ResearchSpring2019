from bs4 import BeautifulSoup
import requests

shapes_all = {"1": "Barrel", "2": "Biconcave", "3": "Biconvex", "4": "Bowtie", "5": "Capsule", "6": "Character",
          "7": "Diamond", "8": "D", "9": "Egg", "10": "Octagon", "11": "Oval", "12": "Octagon", "13": "Pentagon",
          "14": "Rectangle", "15": "Gear", "16": "Heart", "17": "Hourglass", "18": "Kidney", "19": "Oblong",
          "20": "Oval", "21": "Ovoid-rectangular", "22": "Peanut", "23": "Rectangle", "24": "Round", "25": "Heptagon",
          "26": "Shield", "27": "Hexagon", "28": "Square", "29": "Spherical", "30": "Teardrop", "32": "Triangle", "33": "U"}
colors_all = {"1":['Blue'], "2":['Brown'], "3":['Clear'], "4":['Gold'], "5":['Gray'], "6":['Green'], "7":['Orange'],
              "8":['Pink'], "9":['Purple'], "10": ['Red'], "11": ['Tan'], "12": ['White'], "13": ['Yellow'],
              "14": ['Beige'], "15": ['Pink', 'Purple'], "16": ['Brown', 'Red'], "17": ['Red', 'Turquoise'],
              "18": ['Peach', 'White'], "19": ['Blue', 'White'], "20": ['Red', 'Yellow'], "21": ['Blue', 'Yellow'],
              "22": ['Green', 'Yellow'], "23": ['Orange', 'Yellow'], "24": ['Turquoise', 'Yellow'], "25": ['Pink', 'White'],
              "26": ['Blue', 'White Specks'], "27": ['Brown', 'Yellow'], "28": ['Brown', 'Peach'], "29": ['Pink', 'Turquoise'],
              "30": ['Green', 'White'], "31": ['Yellow', 'Gray'], "32": ['White', 'Blue Specks'], "33": ['Tan', 'White'],
              "34": ['Blue', 'Pink'], "35": ['Red', 'White'], "36": ['Yellow', 'White'], "37": ['Pink', 'Red Specks'],
              "38": ['White', 'Yellow'], "39": ['Gray', 'Pink'], "40": ['Maroon', 'Pink'], "41": ['White', 'Red Specks'],
              "42": ['Lavender', 'White'], "43": ['Green', 'Purple'], "44": ['Maroon'], "45": ['Blue', 'Gray'],
              "46": ['Dark', 'Light Green'], "47": ['Brown', 'Clear'], "48": ['Black', 'Yellow'], "49": ['Clear', 'Green'],
              "50": ['Orange', 'Turquoise'], "51": ['Gold', 'White'], "52": ['Blue', 'Brown'], "53": ['Blue', 'Peach'],
              "54": ['Brown', 'Orange'], "55": ['Black', 'Green'], "56": ['Green', 'Pink'], "57": ['Brown', 'White'],
              "58": ['Gray', 'Red'], "59": ['Turquoise', 'White'], "60": ['Peach', 'Purple'], "61": ['Gray', 'Peach'],
              "62": ['Green', 'Turquoise'], "63": ['Green', 'Peach'], "64": ['Orange', 'White'], "65": ['Green', 'Orange'],
              "66": ['Peach', 'Red'], "67": ['Gray', 'White'], "68": ['Gray', 'Yellow'], "69": ['Beige', 'Red'],
              "70": ['Black', 'Teal'], "71": ['Blue', 'Orange'], "72": ['Pink', 'Yellow'], "73": ['Black'], "74": ['Peach']}

shapes =  {"1": "Barrel", "5": "Capsule", "6": "Character", "9": "Egg", "10": "Octagon", "11": "Oval", "12": "Octagon",
           "13": "Pentagon", "14": "Rectangle", "15": "Gear", "16": "Heart", "18": "Kidney", "20": "Oval", "23": "Rectangle",
           "24": "Round", "25": "Heptagon", "27": "Hexagon", "32": "Triangle", "33": "U"}
colors = {"1":['Blue'], "2":['Brown'], "3":['Clear'], "4":['Gold'], "5":['Gray'], "6":['Green'], "7":['Orange'],
              "8":['Pink'], "9":['Purple'], "10": ['Red'], "11": ['Tan'], "12": ['White'], "13": ['Yellow'],
              "14": ['Beige'], "15": ['Pink', 'Purple'], "16": ['Brown', 'Red'], "17": ['Red', 'Turquoise'],
              "18": ['Peach', 'White'], "19": ['Blue', 'White'], "20": ['Red', 'Yellow'], "21": ['Blue', 'Yellow'],
              "22": ['Green', 'Yellow'], "23": ['Orange', 'Yellow'], "25": ['Pink', 'White'],
              "26": ['Blue', 'White Specks'], "27": ['Brown', 'Yellow'], "28": ['Brown', 'Peach'], "29": ['Pink', 'Turquoise'],
              "30": ['Green', 'White'], "31": ['Yellow', 'Gray'], "32": ['White', 'Blue Specks'], "33": ['Tan', 'White'],
              "34": ['Blue', 'Pink'], "35": ['Red', 'White'], "36": ['Yellow', 'White'], "37": ['Pink', 'Red Specks'],
              "38": ['White', 'Yellow'], "39": ['Gray', 'Pink'], "40": ['Maroon', 'Pink'], "41": ['White', 'Red Specks'],
              "42": ['Lavender', 'White'], "43": ['Green', 'Purple'], "44": ['Maroon'], "45": ['Blue', 'Gray'],
              "46": ['Dark', 'Light Green'], "47": ['Brown', 'Clear'], "48": ['Black', 'Yellow'], "49": ['Clear', 'Green'],
              "50": ['Orange', 'Turquoise'], "51": ['Gold', 'White'], "52": ['Blue', 'Brown'], "53": ['Blue', 'Peach'],
              "54": ['Brown', 'Orange'], "55": ['Black', 'Green'], "56": ['Green', 'Pink'], "57": ['Brown', 'White'],
              "58": ['Gray', 'Red'], "59": ['Turquoise', 'White'], "60": ['Peach', 'Purple'], "61": ['Gray', 'Peach'],
              "62": ['Green', 'Turquoise'], "63": ['Green', 'Peach'], "64": ['Orange', 'White'], "65": ['Green', 'Orange'],
              "67": ['Gray', 'White'], "68": ['Gray', 'Yellow'], "69": ['Beige', 'Red'],
              "70": ['Black', 'Teal'], "71": ['Blue', 'Orange'], "72": ['Pink', 'Yellow'], "73": ['Black'], "74": ['Peach']}

base_url = 'https://www.drugs.com/imprints.php?maxrows=100'

def get_shapes_code():
    site = 'https://www.drugs.com/imprints.php'
    for i in range(1,34):
        url = site + '?shape='+str(i)
        html = requests.get(url)
        html = html.text
        soup = BeautifulSoup(html, 'html.parser')
        for s in soup.find_all('h1'):
            if s.string:
                if 'no' in s.string or 'No' in s.string:
                    print('"'+str(i)+'"', s.string.split()[-1])
            # if 'image' in s.lower(): print(s)

def get_colors_code():
    site = 'https://www.drugs.com/imprints.php'
    for i in range(1,75):
        url = site + '?color='+str(i)
        html = requests.get(url)
        html = html.text
        soup = BeautifulSoup(html, 'html.parser')
        for s in soup.find_all('h1'):
            if s.string:
                l = [ss.strip() for ss in s.string.split('"')[-2].split('&')]
                print('"' + str(i) + '"', l)
                # if 'no' in s.string or 'No' in s.string:
                #     l = [ss.strip() for ss in s.string.split('"')[-2].split('&')]
                #     print('"' + str(i) + '"', l)
            # if 'image' in s.lower(): print(s)

def get_result(imprint, color, shape):
    # main_url = base_url + '&imprint='+imprint+'&color='+color+'&shape='+shape
    # for start in range(0,10000,100):
    #     url = main_url + '&start='+start
    #     html = requests.get(url).text
    #     soup = BeautifulSoup(html, 'html.parser')
    #     for s in soup.find_all('div'):
    #         if s['class'] ==
    pass

imprint, color, shape = '', '', ''
get_result(imprint, color, shape)
# site = 'https://www.drugs.com/imprints.php'
#
# shapes = {'round': '24', 'capsule': '5',  }
# imprint = ''
# color = ''
# shape = ''
# url = site + '?imprint='+imprint+'&color='+color+'14&shape=24&sort=rel&maxrows=50'