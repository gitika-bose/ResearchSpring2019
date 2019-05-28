from bs4 import BeautifulSoup
import sys
import requests
import json

root = 'https://www.webmd.com'
drug = [s.lower() for s in sys.argv[1:]]
drug_name = ' '.join(drug)
drug_url = '%20'.join(drug)
page = requests.get("{}/drugs/2/search?type=drugs&query={}".format(root,drug_url))
soup =  BeautifulSoup(page.content, 'html.parser')

exact_match,partial_match = [],[]
for ul_tag in soup.findAll('ul'):
    if ul_tag.get('class') == ['exact-match']:
        for a in ul_tag.findAll('a'): exact_match.append('{}{}'.format(root,a.get('href')))
    if ul_tag.get('class') == ['partial-match']:
        for a in ul_tag.findAll('a'): partial_match.append('{}{}'.format(root, a.get('href')))
result = exact_match + partial_match
if len(result)>0:
    drug = {}
    url = result[0]
    drug_page = requests.get(url)
    drug_soup = BeautifulSoup(drug_page.content, 'html.parser')
    drug_info = drug_soup.findAll('div', class_='drug-information')
    name = drug_info[0].find('h1').string
    brands,generic_name = '',''
    for p_tags in drug_info[0].findAll('p'):
        if 'COMMON' in p_tags.string or 'common' in p_tags.string.lower(): brands = p_tags.string.split(':')[1].strip()
        if 'GENERIC' in p_tags.string or 'generic' in p_tags.string.lower(): generic_name = p_tags.string.split(':')[1].strip()
    content2 = drug_soup.findAll('div', class_='tab-content-container')
    info = {}
    if content2:
        tabs = {'tab-1': None, 'tab-2': None, 'tab-3': None, 'tab-4': None, 'tab-5': None, 'tab-6': None}
        for div_tags in content2[0].findAll('div'):
            if div_tags.get('id')=='tab-1':
                content = div_tags.find(class_='inner-content')
                if content:
                    use, how = '', ''
                    for c in content.children:
                        if c.name=='p': use += c.get_text() + '\n'
                    # content = div_tags.find(class_='monograph-drug-use')
                    for h in content.find(class_='monograph-drug-use'):
                        if h.name == 'p': how += h.get_text() + '\n'
                    tabs['tab-1'] = {'use': use, 'how': how}
            elif div_tags.get('id')=='tab-2':
                content = div_tags.find(class_='inner-content')
                if content:
                    side_effects = ''
                    for c in content.children:
                        if c.name=='p': side_effects += c.get_text() + '\n'
                    tabs['tab-2'] = {'side-effects': side_effects}
            elif div_tags.get('id')=='tab-3':
                content = div_tags.find(class_='inner-content')
                if content:
                    precautions = ''
                    for c in content.children:
                        if c.name == 'p': precautions += c.get_text() + '\n'
                    tabs['tab-3'] = {'precautions': precautions}
            elif div_tags.get('id')=='tab-4':
                content = div_tags.find(class_='inner-content')
                if content:
                    interactions = ''
                    for c in content.children:
                        if c.name == 'p': interactions += c.get_text() + '\n'
                    tabs['tab-4'] = {'interactions': interactions}
            elif div_tags.get('id')=='tab-5':
                content = div_tags.find(class_='inner-content')
                if content:
                    overdose_dict, key = {}, ''
                    for c in content.children:
                        if c.name == 'h2' or c.name == 'h3':
                            key = c.get_text().lower()
                            overdose_dict[key] = ''
                        if c.name == 'p': overdose_dict[key] += c.get_text()
                    tabs['tab-5'] = overdose_dict
            elif div_tags.get('id')=='tab-6':
                content = div_tags.find(class_='inner-content')
                if content:
                    drug_image_dict, count = {}, 1
                    for c in content.find_all(class_='drug-image-large'):
                        link = c.find('img')['src']
                        id = c.find(class_='identification')
                        if id:
                            dl = id.find('dl')
                            dl_dict, key = {}, ''
                            for d in dl:
                                if d.name == 'dt':
                                    key = d.get_text().lower()
                                    dl_dict[key] = ''
                                if d.name == 'dd': dl_dict[key] += d.get_text()
                            drug_image_dict['image_'+str(count)] = {'link': link, 'info': dl_dict}
                            count += 1
                    tabs['tab-6'] = drug_image_dict
        info = {'uses':tabs['tab-1'],'side_effects':tabs['tab-2'],'precautions':tabs['tab-3'],
                'interactions':tabs['tab-4'],'overdose':tabs['tab-5'],'images':tabs['tab-6']}
    drug = {'name': name, 'brands': brands, 'generic-name': generic_name, 'info': info}
    json.dump(drug, open('output2.json', 'w'), indent=2)
else: print('No Match Found')


