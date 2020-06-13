from xmarshal import Schema

schema = Schema()

# TODO: add attributes
@schema.define_tag
class ODM:
    def __init__(self,
                 studies,
                 admin_datas = [],
                 clinical_datas = [],
                 associations = [],
                 ds_signatures = []):
        self.studies = studies
        self.admin_datas = admin_datas
        self.clinical_datas = clinical_datas
        self.associations = associations
        self.ds_signatures = ds_signatures

@schema.define
class Study:
    def __init__(self, oid, global_variables, meta_data_versions):
        self.oid = oid
        self.global_variables = global_variables
        self.meta_data_versions = meta_data_versions

@schema.define
class GlobalVariables:
    def __init__(self, study_name, study_description, protocol_name):
        self.study_name = study_name
        self.study_description = study_description
        self.protocol_name = protocol_name

@schema.define
class StudyName(str):
    def __new__(self, cdata):
        return super().__new__(self, cdata)

@schema.define
class StudyDescription(str):
    def __new__(self, cdata):
        return super().__new__(self, cdata)
        
@schema.define
class ProtocolName(str):
    def __new__(self, cdata):
        return super().__new__(self, cdata)

@schema.define
class BasicDefinitions:
    def __init__(self, measurement_units=[]):
        self.measurement_units = measurement_units

@schema.define
class MeasurementUnit:
    def __init__(self, symbol, aliases):
        self.symbol = symbol
        self.aliases = aliases

@schema.define
class Symbol:
    def __init__(self, translated_texts):
        self.translated_texts = self.translated_texts

@schema.define
class TranslatedText:
    def __init__(self, cdata, xml_lang=None):
        self.text = cdata
        self.lang = xml_lang

@schema.define
class MetaDataVersion:
    def __init__(self,
                 oid, name, description=None,
                 include=None,
                 protocol=None,
                 study_event_defs=[],
                 form_defs=[],
                 item_group_defs=[],
                 item_defs=[],
                 code_lists=[],
                 presentations=[],
                 condition_defs=[],
                 method_defs=[]):
        self.oid = oid
        self.name = name
        self.include = include
        self.protocol = None
        self.description = description
        self.study_event_defs = study_event_defs
        self.form_defs = form_defs
        self.item_group_defs = item_group_defs
        self.item_defs = item_defs
        self.code_lists = code_lists
        self.presentations = presentations
        self.condition_defs = condition_defs
        self.method_defs = method_defs

@schema.define
class Include:
    def __init__(self,
                 study_oid,
                 meta_data_version_oid):
        self.study_oid = study_oid
        self.meta_data_version_oid = meta_data_version_oid

@schema.define
class Protocol:
    def __init__(self,
                 description=None,
                 study_event_refs=[],
                 aliases=[]):
        self.description = description
        self.study_event_refs = study_event_refs
        self.aliases = aliases

@schema.define
class Description:
    def __init__(self,
                 translated_texts):
        self.translated_texts = translated_texts

@schema.define
class StudyEventRef:
    def __init__(self,
                 study_event_oid,
                 mandatory,
                 order_number = None,
                 collection_exception_condition_oid = None):
        self.study_event_oid = study_event_oid
        self.order_number = order_number
        self.mandatory = mandatory
        self.collection_exception_condition_oid = collection_exception_condition_oid

@schema.define
class StudyEventDef:
    def __init__(self,
                 oid, name, repeating, type, category=None):
        self.oid = oid
        self.name = name
        self.repeating = repeating
        self.type = type
        self.category = category

@schema.define
class FormRef:
    def __init__(self,
                 form_oid, mandatory,
                 order_number=None,
                 collection_exception_condition_oid=None):
        self.form_oid = form_oid
        self.order_number = order_number
        self.collection_exception_condition_oid = collection_exception_condition_oid

@schema.define
class FormDef:
    def __init__(self,
                 oid,
                 name,
                 repeating,
                 description=None,
                 item_group_refs=[],
                 archive_layouts=[],
                 aliases=[]):
        self.oid = oid
        self.name = name
        self.repeating = repeating
        self.description = description
        self.item_group_refs = item_group_refs
        self.archive_layouts = archive_layouts
        self.aliases = aliases
        
@schema.define
class ItemGroupRef:
    def __init__(self,
                 item_group_oid,
                 mandatory,
                 order_number=None,
                 collection_exception_condition_oid=None):
        self.item_group_oid = item_group_oid
        self.order_number = order_number
        self.mandatory = mandatory
        self.collection_exception_condition_oid = collection_exception_condition_oid
                 
with open('example.xml') as f:
    odm = schema.parse(f.read())

print(odm)
