from bs4 import BeautifulSoup
import sys
import requests


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
    print('The top result is: ')
    info = {}
    url = result[0]
    drug_page = requests.get(url)
    drug_soup = BeautifulSoup(drug_page.content, 'html.parser')
    drug_info = drug_soup.findAll('div', class_='drug-information')
    name = drug_info[0].find('h1').string
    brands,generic_name = '',''
    for p_tags in drug_info[0].findAll('p'):
        if 'COMMON' in p_tags.string or 'common' in p_tags.string.lower(): brands = p_tags.string.split(':')[1].strip()
        if 'GENERIC' in p_tags.string or 'generic' in p_tags.string.lower(): generic_name = p_tags.string.split(':')[1].strip()
    content = drug_soup.findAll('div', class_='tab-content-container')
    uses,side_effects,precautions,interactions,overdose,images = {},{},{},{},{},{}
    tabs = {'tab-1':uses,'tab-2':side_effects,'tab-3':precautions,'tab-4':interactions,'tab-5':overdose,'tab-6':images}
    for div_tags in content[0].findAll('div'):
        if div_tags.get('id')=='tab-1':
            content2 = div_tags.find(class_='inner-content')
            use = content2.p.get_text()
            content = div_tags.find(class_='monograph-drug-use')
            how = content2.p.get_text()
            print(how)

else: print('No Match Found')
