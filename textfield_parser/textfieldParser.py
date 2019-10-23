import json
import re


class TextFieldParser() :

    _modifier_list_not = ['!','~','not','Not','NOT']
    _separator = ','
    _formula_map = {'!=':'!','==':'=','>=':'≥','=>':'≥','<=':'≤','=<':'≤'}
    def __init__(self):
        pass

    def read_list(self,text,value_list=None):

        text = text.strip()

        negation = False
        # Test for Not
        if len(text) > 1 and text[0] in self._modifier_list_not :
            text = text[1:-1]
            negation = True
        elif len(text) > 3 and text[:3] in self._modifier_list_not :
            text = text[4:-1].strip()
            negation = True

        result_list = [x.strip().strip("'").strip('"') for x in text.split(self._separator)]

        if negation :
            if not value_list :
                raise ValueError("Negation needs a value list to exclude items")
            result_list = [x for x in value_list if x not in result_list]

        return result_list

    def read_map(self,text):
        list_maps = [x.strip() for x in text.split(self._separator)]
        return  {cm.split(':')[0].strip().strip("'").strip('"'): \
                       cm.split(':')[1].strip().strip("'").strip('"') for cm in list_maps}


    def read_json(self,text) :
        j = json.loads(text)
        return j

    def read_comparisons(self,text):

        for key,value in self._formula_map.items() :
            text = text.replace(key,value)
        text_list = text.split(',')

        print (text_list)

        comparison_list = list()
        for selection in text_list:
            m = re.match(u'(.+)\s*([<>!≤≥]+)\s*(.+)', selection)
            if m:
                left = m.group(1).strip().strip('"').strip("'")
                right = float(m.group(3).strip())
                comparison = m.group(2).strip()
                comparison_list.append([left,comparison,right])
            else:
                raise ValueError('Could not parse comparison statement: ' + selection)
        return comparison_list

tf_parser = TextFieldParser()

##############################
### MAIN
##############################
if __name__ == '__main__':

    ### list
    text = "'Hello', 'a list', separated by , me"
    not_text = "Not Mercedes, Renault, Citroen, Peugeaut, 'Rolls Royce'"
    list2 = ['Mercedes', 'Audi', 'VW', 'Skoda', 'Renault', 'Citroen', 'Peugeot', 'Rolls Royce']
    print('Not: ' + str(tf_parser.read_list(not_text, list2)))
    print('All :' + str(tf_parser.read_list('All', list2)))
    print('List: ' + str(tf_parser.read_list(text)))

    ### map
    maplist = "'Mercedes':expensive, Audi:'sportiv', VW : 'people', Citroen:cool, 'Rolls Rocye': royal"
    print('Map :' + str(tf_parser.read_map(maplist)))


    ### json
    json_text = "{\"Luxury Class\": {\"Mercedes\":\"expensive\",\"Rolls Rocye\": \"royal\"}, \"High Middle Class\":{\"Audi\":\"sportiv\"}, \"Middle Class\": {}, \
                \"Middle Class\" : {\"Citroen\":\"cool\",\"VW\" : \"people\" }}"
    print('JSON: ' + str(tf_parser.read_json(json_text)))


    ### comparison
    comparison = ' anna > 1.70, norbert != 900, cindy <= 1.65'
    print('Comparison: ' + str(tf_parser.read_comparisons(comparison)))