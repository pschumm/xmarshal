from xmarshal import Schema

schema = Schema()

@schema.define
class MetadataVersion:
    def __init__(self):
        pass

@schema.define
class GlobalVariables:
    def __init__(self, study_name, study_description, protocol_name):
        self.study_name = study_name
        self.study_description = study_description
        self.protocol_name = protocol_name

@schema.define
class Study:
    def __init__(self, oid, global_variables, meta_data_versions):
        self.oid = oid
        self.global_variables = global_variables
        self.meta_data_versions = meta_data_versions

@schema.define
class ODM:
    def __init__(self, studies):
        self.studies = studies

with open('example.xml') as f:
    root = schema.parse(f.read())
