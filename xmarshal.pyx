import re
import untangle
import inspect
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


to_snake_case_pattern = re.compile('(.)([A-Z][a-z]+)')
to_snake_case_pattern_2 = re.compile('([a-z0-9])([A-Z])')
cdef to_snake_case(str string):
    """
    Converts a name from PascalCase/"NotCamelCase" to snake_case.
    Importantly, maintains that acronyms are lowercased, not separated
    on each letter, and that colons (:) are replaced with underscores (_).
    From StackOverflow by @epost at:
    https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
    """

    string2 = re.sub(to_snake_case_pattern, r'\1_\2', string)
    return re.sub(to_snake_case_pattern_2, r'\1_\2', string2).lower()

cdef pluralize(str string):
    if string.endswith('y'):
        return string[:-1] + 'ies'
    elif string.endswith('s'):
        return string + 'es'
    else:
        return string + 's'

class Schema:
    def __init__(self):
        self.namespace = {}

    def define(self, schema_class):
        self.namespace[schema_class.__name__] = schema_class
        return schema_class

    def marshal(self, obj):
        if isinstance(obj, str):
            return obj

        elif isinstance(obj, list):
            return [self.marshal(el) for el in obj]

        elif obj is None:
            return None

        tag = obj._name
    
        if tag in self.namespace:
            scheme = self.namespace.get(tag)
        
            collected_attributes = {}
            valid_fields = set(inspect.getfullargspec(scheme.__init__).args[1:] + inspect.getfullargspec(scheme.__new__).args[1:])

            for attribute in obj._attributes:
                if to_snake_case(attribute) in valid_fields:
                    collected_attributes[to_snake_case(attribute)] = self.marshal(obj._attributes[attribute])

            for key in dir(obj):
                value = getattr(obj, key)
                parsed_key = to_snake_case(key)

                if pluralize(parsed_key) in valid_fields:
                    if isinstance(value, list):
                        collected_attributes[pluralize(parsed_key)] = [self.marshal(el) for el in value]
                    else:
                        collected_attributes[pluralize(parsed_key)] = [self.marshal(value)]
                elif parsed_key in valid_fields:
                    if isinstance(value, list):
                        collected_attributes[parsed_key] = self.marshal([el for el in value])
                    else:
                        collected_attributes[parsed_key] =  self.marshal(value)

            if 'cdata' in valid_fields:
                collected_attributes['cdata'] = obj.cdata

            return scheme(**collected_attributes)
        
        else:
            return None

    def parse(self, string):
        root = untangle.parse(string).children[0]
        return self.marshal(root)
