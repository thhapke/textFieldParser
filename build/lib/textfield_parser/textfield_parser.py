import json
import re


#### READ LIST
def read_list(text,value_list=None,sep = ',',modifier_list_not=None):

    if not modifier_list_not:
        modifier_list_not = ['!', '~', 'not', 'Not', 'NOT']

    text = text.strip()

    negation = False
    # Test for Not
    if len(text) > 1 and text[0] in modifier_list_not :
        text = text[1:-1]
        negation = True
    elif len(text) > 3 and text[:3] in modifier_list_not :
        text = text[4:-1].strip()
        negation = True

    result_list = [x.strip().strip("'").strip('"') for x in text.split(sep)]

    if negation :
        if not value_list :
            raise ValueError("Negation needs a value list to exclude items")
        result_list = [x for x in value_list if x not in result_list]

    return result_list

#### READ VALUE LIST
def read_value_lists(text,inner_sep = ',',outer_sep = ';',map_sep=':'):

    text = text.strip()

    vo_lists = [x.strip().strip("'").strip('"') for x in text.split(outer_sep)]

    value_list_dict = dict()
    for vo in vo_lists :
        key, vi_str = vo.split(map_sep)
        key = key.strip().strip("'").strip('"')
        value_list_dict[key] = [x.strip().strip("'").strip('"') for x in vi_str.split(inner_sep)]

    return value_list_dict


#### READ MAP
def read_maps(text,sep = ',',):
    list_maps = [x.strip() for x in text.split(sep)]
    return  {cm.split(':')[0].strip().strip("'").strip('"'): \
                   cm.split(':')[1].strip().strip("'").strip('"') for cm in list_maps}

#### READ JSON
def read_json(text) :
    j = json.loads(text)
    return j

#### READ Relation
def read_relations(text,sep=',',relation_map=None):

    if not relation_map :
        relation_map = {'!=': '!', '~':'!', '==': '=', '>=': '≥', '=>': '≥', '<=': '≤', '=<': '≤'}

    for key,value in relation_map.items() :
        text = text.replace(key,value)
    text_list = text.split(sep)

    print (text_list)

    relation_list = list()
    for selection in text_list:
        m = re.match(u'(.+)\s*([<>!≤≥]+)\s*(.+)', selection)
        if m:
            left = m.group(1).strip().strip('"').strip("'")
            right = float(m.group(3).strip())
            relation = m.group(2).strip()
            relation_list.append([left,relation,right])
        else:
            raise ValueError('Could not parse relation statement: ' + selection)
    return relation_list

##############################
### MAIN
##############################
if __name__ == '__main__':

    ### list
    text = "'Hello', 'a list', separated by , me"
    not_text = "Not Mercedes, Renault, Citroen, Peugeaut, 'Rolls Royce'"
    list2 = ['Mercedes', 'Audi', 'VW', 'Skoda', 'Renault', 'Citroen', 'Peugeot', 'Rolls Royce']
    print('Not: ' + str(read_list(not_text, list2)))
    print('All :' + str(read_list('All', list2)))
    print('List: ' + str(read_list(text)))

    ### value lists
    value_str = "'Mercedes':expensive, German, respectable; Audi:'sportive, German, technology-advanced'; \
                    VW : 'people', 'solid', No1; Citroen:cool, Fantomas, CV2, elastic ; 'Rolls Rocye': royal,  \
                    British, 'very expensive', black"

    print('Value lists: ' + str(read_value_lists(value_str)))


    ### map
    maplist = "'Mercedes':expensive, Audi:'sportive', VW : 'people', Citroen:cool, 'Rolls Rocye': royal"
    print('Map :' + str(read_maps(maplist)))


    ### json
    json_text = "{\"Luxury Class\": {\"Mercedes\":\"expensive\",\"Rolls Rocye\": \"royal\"}, \"High Middle Class\":{\"Audi\":\"sportiv\"}, \"Middle Class\": {}, \
                \"Middle Class\" : {\"Citroen\":\"cool\",\"VW\" : \"people\" }}"
    print('JSON: ' + str(read_json(json_text)))


    ### comparison
    comparison = ' anna > 1.70, norbert != 900, cindy <= 1.65'
    print('Comparison: ' + str(read_relations(comparison)))