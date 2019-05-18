"""
Before start:
export GOOGLE_APPLICATION_CREDENTIALS=/Users/tejitpabari/Desktop/ResearchSpring2019/text-recognition/research-pill-google_service_account_key.json
export PROJECT_ID=research-pill
"""
import sys
import json
from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2

imprint_json, data_json, color_json, shape_json = open('imprints.json'), open('data.json'), open('colors.json'), open('shapes.json')
imprints, colors, shapes = json.load(imprint_json), json.load(color_json), json.load(shape_json)
# imprints = {k:set(v) for k,v in imprints_list.items()}
data = json.load(data_json)
links = open('links.txt','w')

shape,color = 'round','yellow'
pills_shapes = set(shapes[shape])
pills_color = set(colors[color])

def get_prediction(content, project_id, model_id):
    prediction_client = automl_v1beta1.PredictionServiceClient()
    name = 'projects/{}/locations/us-central1/models/{}'.format(project_id, model_id)
    payload = {'image': {'image_bytes': content }}
    params = {}
    request = prediction_client.predict(name, payload, params)
    return request  # waits till request is returned

def resolve_y(res):
    result = {}
    bounds = []
    count = 0
    for r in res:
        ytop,ybot = r[2],r[4]
        check = True
        for b in bounds:
            s5 = 75*(b[1]-b[0])/100
            if b[0] <= ybot <= b[1] and b[0] <= ytop <= b[1] and (ybot-ytop) >= s5:
                result[b[2]].append(r)
                check = False
                break
            elif ybot >= b[1] and b[0] >= ytop and (ybot-ytop) >= s5:
                result[b[2]].append(r)
                b[0] = ytop
                b[1] = ybot
                check = False
                break
            elif b[0] <= ybot <= b[1] and (ybot-b[0]) >= s5:
                result[b[2]].append(r)
                b[0] = ytop
                check = False
                break
            elif b[0] <= ytop <= b[1] and (b[1]-ytop) >= s5:
                result[b[2]].append(r)
                b[1] = ybot
                check = False
                break
        if check:
            bounds.append([ytop, ybot, count])
            result[count] = [r]
            count += 1
    return [sorted(v,key=lambda x:x[1]) for k,v in result.items()]

def resolve_x(res):
    result = []
    for rr in res:
        bounds = []
        for r in rr:
            n, x1, x2 = r[0], r[1], r[3]
            check = True
            for b in bounds:
                b_n, b_x1, b_x2 = b[0], b[1], b[2]
                if abs(x1-b_x2) <= 0.05:
                    b[0] += n
                    b[2] = x2
                    check=False
                    break
            if check:
                bounds.append([r[0],r[1],r[3]])
        for b in bounds: result.append(b[0])
    return result

image_paths = sys.argv[1:]
project_id_letters, model_id_letters = 'research-pill', 'IOD8510123241962995712'
project_id_numbers, model_id_numbers = 'research-pill', 'IOD9124864591099068416'
pills_imprint, names2 = None, None
for image_path in image_paths:
    content = open(image_path, 'rb').read()
    letters = get_prediction(content, project_id_letters, model_id_letters)
    numbers = get_prediction(content, project_id_numbers, model_id_numbers)
    names,res = [], []
    for n in numbers.payload:
        boxes = n.image_object_detection.bounding_box.normalized_vertices
        res.append((n.display_name,boxes[0].x,boxes[0].y,boxes[1].x,boxes[1].y))
        names.append(n.display_name)
    for l in letters.payload:
        boxes = l.image_object_detection.bounding_box.normalized_vertices
        res.append((l.display_name,boxes[0].x,boxes[0].y,boxes[1].x,boxes[1].y))
        names.append(l.display_name)
    res = resolve_y(res)
    print(res)
    names2 = resolve_x(res)
    print(names2)
    for name in names:
        if not pills_imprint: pills_imprint = set(imprints[name])
        else: pills_imprint=pills_imprint.intersection(set(imprints[name]))

pills = pills_imprint.intersection(pills_color,pills_shapes)
print(pills)
for pill in pills:
    shape = pill[4:]
    shape_data = data[shape]['data'][pill]
    imprint = shape_data.get('imprint_list', None)
    if not imprint: imprint = [shape_data.get('imprint', None)]
    check = False
    for name in names2:
        for i in imprint:
            if name in i:
                check = True
                break
    if check: links.write(shape_data['imageUrl'] + '\n')
