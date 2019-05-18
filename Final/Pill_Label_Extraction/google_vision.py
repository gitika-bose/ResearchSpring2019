from google.cloud import vision
from google.cloud.vision import types
import requests
import sys
import json
import re
from os.path import isfile

def menu():
    patient_names = []
    print('Please enter all the patient names one by one, that can be on the pill labels.')
    user = re.sub(r"[^a-zA-Z0-9]+", ' ', input('(Enter 0 or \'exit\' to exit) Please input Patient\'s first name: ').strip().lower())
    while user != '0' and user != 'exit':
        patient_names.append(user)
        user = re.sub(r"[^a-zA-Z0-9]+", ' ',input('(Enter 0 or \'exit\' to exit) Please input Patient\'s first name: ').strip().lower())
    path_to_pictures = []
    print('Please enter the path to images one by one. Relative path to this file is ok.')
    path = input('(Enter 0 or \'exit\' to exit) Please enter path to image: ').strip().lower()
    while path != '0' and path != 'exit':
        path_to_pictures.append(path)
        path = input('(Enter 0 or \'exit\' to exit) Please enter path to image: ').strip().lower()

    final = {}
    for path in path_to_pictures:
        if isfile(path):
            vals = text_processing(path,patient_names)
            if vals:
                for v in vals:
                    if v not in final:
                        final[v] = vals[v]
                    else:
                        if type(final[v])==dict:
                            for vv in vals[v]:
                                if vv not in final[v]:
                                    final[v][vv] = vals[v][vv]
                                elif final[v][vv].lower() == vals[v][vv].lower():
                                    pass
                                else:
                                    final[v][vv] += ","
                                    final[v][vv] += vals[v][vv]
                        else:
                            if vals[v].lower() == final[v].lower():
                                pass
                            else:
                                final[v] += ", "
                                final[v] += vals[v]

    for k,v in final.items():
        if type(v)==dict:
            print('{}:'.format(k))
            for k2,v2 in v.items(): print('\t{}: {}'.format(k2,v2))
        else: print('{}: {}'.format(k,v))

def text_processing(image_path, patient_names):
    final_values = {}
    client = vision.ImageAnnotatorClient.from_service_account_file('./research-pill-google_service_account_key.json')


    potential_patients = patient_names

    prefixes = ['ceph', 'tretin', 'pred', 'sulfa', 'cef']
    suffixes = ['setron', 'cycline', 'pramine', 'trel', 'asone', 'vir', 'tyline', 'zolam', 'profen', 'zepam', 'onide', 'tretin', 'nacin', 'gliptin', 'cillin', 'dronate', 'phylline', 'zosin', 'parin', 'glitazone', 'lamide', 'mab', 'oprazole', 'semide', 'sartan', 'dazole', 'bital', 'zodone', 'eprazole', 'tinib', 'statin', 'fenac', 'afil', 'caine', 'terol', 'floxacin', 'nazole', 'tadine', 'mustine', 'vudine', 'iramine', 'triptan', 'mycin', 'dipine', 'bicin', 'pril', 'ridone', 'olone', 'thiazide', 'olol']
    middles = ['cort', 'tretin', 'pred', 'parin', 'vir']

    pharmacies = ["cvs", "walgreens", "walmart", "rite", "aid", "kroger", "duane", "reade", "omnicare", "sears", "costco"]

    with open(image_path, 'rb') as image_file: content = image_file.read()

    image = vision.types.Image(content=content)

    text_response = client.text_detection(image=image)

    # print(text_response)
    # GETTING RESPONSE AND BOUNDING BOXES
    texts = [text.description for i, text in enumerate(text_response.text_annotations) if i != 0]
    boxes = [b.bounding_poly.vertices for i, b in enumerate(text_response.text_annotations) if i != 0]
    box_sizes = [((i[1].x-i[0].x)**2+(i[1].y-i[0].y)**2)**(1/2)*((i[2].x-i[1].x)**2+(i[2].y-i[1].y)**2)**(1/2) for i in boxes]

    complete_text = text_response.text_annotations[0].description
    sched = {}

    # ENUMERATE ALL WORDS TO CLASSIFY THEM
    potential = []
    check_dose = False
    schedule, start, diff = "", None, None
    for i, t in enumerate(texts):
        if t.lower() == "take" or t.lower() == "takes" or check_dose:
            check_dose = True
            if t.lower() == "take":
                start = boxes[i][0].y
                diff = boxes[i][2].y-boxes[i][0].y
            else:
                if boxes[i][0].y > start + 1.75*diff:
                    check_dose = False
                elif boxes[i][2].y < (start + (diff/4)):
                    pass
                else:
                    schedule += t + " "
        elif t.lower() == "every":
            reg = t + " (\w+)"
            m = re.search(reg, complete_text)
            sched['When'] = m.group(0)

        if t.lower() == 'tablet' or t.lower() == 'tablets':
            final_values['type'] = 'Tablet'
            continue
        elif t.lower() == 'capsule' or t.lower() == 'capsules':
            final_values['type'] = 'Capsule'
            continue
        elif 'mg' in t.lower() or 'mcg' in t.lower():
            reg = '(\S+)\s+' + t
            m = re.search(reg, complete_text)
            final_values['Dosage'] = m.group(0)
            continue

        URL = "https://rximage.nlm.nih.gov/api/rximage/1/rxnav?name=" + t
        r = requests.get(url = URL)
        r = r.json()
        if r['replyStatus']['imageCount'] != 0:
            potential.append((t, i))
        else:
            done = False
            for pat in potential_patients:
                if pat.lower() in t.lower():
                    final_values['Patient'] = pat
                    done = True
            if not done:
                for pharm in pharmacies:
                    if pharm.lower() in t.lower():
                        if pharm == "duane" or pharm == "reade": final_values['Pharmacy'] = "duane reade"
                        elif pharm == "rite" or pharm == "aid": final_values['Pharmacy'] = "rite aid"
                        else: final_values['Pharmacy'] = pharm



    # PARSE THROUGH SCHEDULE

    schedule = schedule.lower()
    words_in_sched = schedule.split()

    if "by" in schedule.lower():
        reg = "by (\w+)"
        m = re.search(reg, schedule)
        m2 = words_in_sched.index("by")
        if m2 < len(words_in_sched):
            words_in_sched[m2] = ""
        if m2+1 < len(words_in_sched):
            words_in_sched[m2+1] = ""
        if m:
            sched['How'] = m.group(0)

    if "tablet" in schedule.lower():
        reg = '(\w+)\s+tablet'
        m = re.search(reg, schedule)
        m2 = words_in_sched.index(m.group(1))
        if m2 < len(words_in_sched):
            words_in_sched[m2] = ""
        if m2+1 < len(words_in_sched):
            words_in_sched[m2+1] = ""
        if m:
            sched['No. of tablets'] = m.group(1)

    if "capsule" in schedule.lower():
        reg = '(\w+)\s+capsule'
        m = re.search(reg, schedule)
        m2 = words_in_sched.index(m.group(1))
        if m2 < len(words_in_sched):
            words_in_sched[m2] = ""
        if m2+1 < len(words_in_sched):
            words_in_sched[m2+1] = ""
        if m:
            sched['No. of tablets'] = m.group(1)

    if "meals" in schedule.lower():
        reg = '(\w+)\s+meals'
        m = re.search(reg, schedule)
        m2 = words_in_sched.index("meals")
        if m2 < len(words_in_sched):
            words_in_sched[m2] = ""
        if m2-1 < len(words_in_sched):
            words_in_sched[m2-1] = ""
        if m:
            sched['Meals'] = m.group(0)

    if "as" in schedule.lower():
        reg = "a (\w*)"
        m = re.search(reg, schedule)
        m2 = words_in_sched.index("meals")
        for i in range(m2, len(words_in_sched)):
            words_in_sched[m2] = ""
        if m:
            sched['Meals'] = m.group(0)

    if words_in_sched:
        when = " ".join(words_in_sched)
        if when.strip():
            if "When" in sched:
                sched["When"] += ", "
                sched["When"] += when.strip()
            else:
                sched["When"] = when.strip()
    if sched:
        final_values["Schedule"] = sched

    # print(potential)
    # MEDICINE NAME
    if potential:
        med_names = set()
        if len(potential) > 1:
            for s in suffixes:
                l = len(s)
                for p in potential:
                    m = p[0]
                    if m[len(m)-l:len(m)].lower() == s.lower():
                        med_names.add(p)
            for pr in prefixes:
                l = len(pr)
                for p in potential:
                    m = p[0]
                    if m[0:len(pr)].lower() == s.lower():
                        med_names.add(p)
            for mid in middles:
                for p in potential:
                    if mid in p:
                        med_names.add(p)

            if med_names:
                if len(med_names) > 1:
                    size = -1
                    med_name = None
                    for m in med_names:
                        if box_sizes[m[1]] > size:
                            size = box_sizes[m[1]]
                            med_name = m[0]
                            final_values['medicine_name'] = med_name
                else:
                    final_values['medicine_name'] = med_names.pop()[0]
            else:
                size = -1
                med_name = None
                for m in potential:
                    if box_sizes[m[1]] > size:
                        size = box_sizes[m[1]]
                        med_name = m[0]
                        final_values['medicine_name'] = med_name
        else:
            final_values['medicine_name'] = potential[0][0]

    return final_values


menu()



