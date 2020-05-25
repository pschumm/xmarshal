import re
from typing import List
from xml.etree import ElementTree
from lxml import etree, objectify
import untangle
import inspect
from collections import namedtuple
from copy import deepcopy

class XMarshalElement(object):
    def __init__(self):
        self._tag = ''
        self._required_fields = []
        self._optional_fields = []
        self._fields = []
    
    def __call__(self, **kwargs):
        self = deepcopy(self)
        assert set(kwargs.keys()) == set(self._fields)
        self.__dict__.update(kwargs)
        return self

    def __repr__(self):
        return '<xmarshal ' + self._tag + '>'

def create_element(tag, attributes):
    element = XMarshalElement()
    
    for attribute in attributes:
        if attributes[attribute] == 'required':
            element._required_fields.append(attribute)
        elif attributes[attribute] == 'optional':
            element._optional_fields.append(attribute)
        element._tag = tag
        element._fields = element._required_fields + element._optional_fields

    return element

schema = {
    'MetadataVersion': create_element('MetadataVersion',
                                      {}),
    'GlobalVariables': create_element('GlobalVariables',
                                      {'study_name': 'required',
                                       'study_description': 'required',
                                       'protocol_name': 'required'}),
    'Study': create_element('Study',
                            {'oid': 'required',
                             'global_variables': 'required',
                             'meta_data_versions': 'required'}),
    'ODM': create_element('ODM',
                          {'studies': 'required'})
}

class InvalidODMException(Exception):
    pass

# from @Daveo on StackOverflow at:
# https://stackoverflow.com/questions/3809401/what-is-a-good-regular-expression-to-match-a-url
# TODO: make this a re.Pattern object
URI_REGEX = 'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'

class CustomElement(object):
    def __init__(self, element):
        self.element = element

def to_snake_case(string):
    """
    Converts a name from PascalCase/"NotCamelCase" to snake_case.
    Importantly, maintains that acronyms are lowercased, not separated
    on each letter, and that colons (:) are replaced with underscores (_).
    From StackOverflow by @epost at:
    https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
    """

    string = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', string).lower()

def remove_namespace(string):
    return re.sub('{' + URI_REGEX + '}', '', string, 1)

# from @YungGun on StackOverflow
# https://stackoverflow.com/questions/57829037/get-type-annotations-in-python-3-7
def get_type(function, param_name):
    return inspect.getmembers(function)[0][1][param_name]

def pluralize(string):
    if string.endswith('y'):
        return string[:-1] + 'ies'
    elif string.endswith('s'):
        return string + 'es'
    else:
        return string + 's'

def marshal(obj):
    if isinstance(obj, str):
        return obj

    elif isinstance(obj, list):
        return obj

    tag = obj._name

    if isinstance(obj, list):
        return [marshal(el) for el in obj]
    
    if tag in schema:
        scheme = schema.get(tag)
        
        collected_attributes = {}

        for attribute in obj._attributes:
            if to_snake_case(attribute) in scheme._fields:
                collected_attributes[to_snake_case(attribute)] = marshal(obj._attributes[attribute])

        for key in dir(obj):
            value = getattr(obj, key)
            parsed_key = to_snake_case(key)

            if pluralize(parsed_key) in scheme._fields:
                if isinstance(value, list):
                    collected_attributes[pluralize(parsed_key)] = [marshal(el) for el in value]
                else:
                    collected_attributes[pluralize(parsed_key)] = [marshal(value)]
            elif parsed_key in scheme._fields:
                if isinstance(value, list):
                    collected_attributes[parsed_key] = marshal([el for el in value])
                else:
                    collected_attributes[parsed_key] =  marshal(value)

        return schema.get(tag)(**collected_attributes)
        
    else:
        if obj.cdata.strip() != '':
            return obj.cdata.strip()
        
        el = XMarshalElement()

        collected_attributes = {}

        for attribute in obj._attributes:
            collected_attributes[to_snake_case(attribute)] = marshal(obj._attributes[attribute])

        for child in dir(obj):
            if isinstance(child, list):
                collected_attributes[pluralize(child)] = getattr(obj, child)
            else:
                collected_attributes[child] = getattr(obj, child)

        
        #if obj.cdata.strip() != "":
        #    return obj.cdata.strip()
        #el = CustomElement(tag)
        #el.__dict__.update(obj._fields)
        #for child in dir(obj):
        #    el.__dict__[to_snake_case(child)] = getattr(obj, child)
        
        
        return el

def parse(string):
    root = untangle.parse(string).ODM
    root = marshal(root)
    return root
