from __future__ import annotations 
from datetime import (
    datetime,
    date,
    time
)
from decimal import Decimal 
from enum import Enum 
import re
import sys
from typing import (
    Any,
    ClassVar,
    List,
    Literal,
    Dict,
    Optional,
    Union
)
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    field_validator
)
metamodel_version = "None"
version = "None"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )
    pass




class LinkMLMeta(RootModel):
    root: Dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta({'default_prefix': 'linkml_tutorial_2024',
     'default_range': 'string',
     'description': 'A repostitory that walks through schema generation.',
     'id': 'https://w3id.org/linkml/linkml-tutorial-2024',
     'imports': ['linkml:types'],
     'license': 'MIT',
     'name': 'linkml-tutorial-2024',
     'prefixes': {'ENVO': {'prefix_prefix': 'ENVO',
                           'prefix_reference': 'http://purl.obolibrary.org/obo/ENVO_'},
                  'KBase': {'prefix_prefix': 'KBase',
                            'prefix_reference': 'https://kbase.us/'},
                  'PATO': {'prefix_prefix': 'PATO',
                           'prefix_reference': 'http://purl.obolibrary.org/obo/PATO_'},
                  'SIO': {'prefix_prefix': 'SIO',
                          'prefix_reference': 'http://semanticscience.org/resource/'},
                  'biolink': {'prefix_prefix': 'biolink',
                              'prefix_reference': 'https://w3id.org/biolink/'},
                  'example': {'prefix_prefix': 'example',
                              'prefix_reference': 'https://example.org/'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'linkml_tutorial_2024': {'prefix_prefix': 'linkml_tutorial_2024',
                                           'prefix_reference': 'https://w3id.org/linkml/linkml-tutorial-2024/'},
                  'nmdc': {'prefix_prefix': 'nmdc',
                           'prefix_reference': 'https://w3id.org/nmdc/'},
                  'obo': {'prefix_prefix': 'obo',
                          'prefix_reference': 'http://purl.obolibrary.org/obo/'},
                  'schema': {'prefix_prefix': 'schema',
                             'prefix_reference': 'http://schema.org/'}},
     'see_also': ['https://linkml.github.io/linkml-tutorial-2024'],
     'source_file': 'src/linkml_tutorial_2024/schema/linkml_tutorial_2024.yaml',
     'title': 'linkml-tutorial-2024'} )

class BiomeTypeEnum(str, Enum):
    """
    The type of biome.
    """
    forest = "forest"
    lake = "lake"
    ocean = "ocean"
    desert = "desert"
    air = "air"


class SpeciesEnum(str):
    """
    The species of micro organisms collected in the sample.
    """
    pass



class SampleCollection(ConfiguredBaseModel):
    """
    A collection of samples.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/linkml-tutorial-2024',
         'tree_root': True})

    samples: Optional[Dict[str, Union[Sample,AirSample,SoilSample]]] = Field(None, description="""The samples in the collection.""", json_schema_extra = { "linkml_meta": {'alias': 'samples', 'domain_of': ['SampleCollection']} })


class Sample(ConfiguredBaseModel):
    """
    A sample is a limited quantity of something (e.g. an individual or set of individuals from a population,  or a portion of a substance) to be used for testing, analysis, inspection, investigation, demonstration,  or trial use.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Biosample', 'Environmental Sample'],
         'class_uri': 'SIO:001050',
         'exact_mappings': ['SIO:001050'],
         'from_schema': 'https://w3id.org/linkml/linkml-tutorial-2024',
         'id_prefixes': ['KBase', 'nmdc']})

    id: str = Field(..., description="""The unique identifier for the biosample.""", json_schema_extra = { "linkml_meta": {'alias': 'id', 'domain_of': ['Sample']} })
    latitude: Optional[float] = Field(None, description="""Latitude is a geographic coordinate which refers to the angle from a point on the Earth's surface to the  equatorial plane.""", ge=-90, le=90, json_schema_extra = { "linkml_meta": {'alias': 'latitude', 'domain_of': ['Sample'], 'slot_uri': 'schema:latitude'} })
    longitude: Optional[float] = Field(None, description="""Longitude is a geographic position that refers to the angle east or west of a reference meridian between the  two geographical poles to another meridian that passes through an arbitrary point.""", json_schema_extra = { "linkml_meta": {'alias': 'longitude', 'domain_of': ['Sample'], 'slot_uri': 'schema:longitude'} })
    species: Optional[List[SpeciesEnum]] = Field(None, description="""The species of micro organisms collected in the sample.""", json_schema_extra = { "linkml_meta": {'alias': 'species', 'domain_of': ['Sample']} })
    sample_biome: Optional[BiomeTypeEnum] = Field(None, description="""The biome type of the biosample""", json_schema_extra = { "linkml_meta": {'alias': 'sample_biome', 'domain_of': ['Sample']} })
    sample_type: Literal["Sample"] = Field("Sample", description="""The type of sample.""", json_schema_extra = { "linkml_meta": {'alias': 'sample_type', 'designates_type': True, 'domain_of': ['Sample']} })


class AirSample(Sample):
    """
    A sample of air
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/linkml-tutorial-2024',
         'slot_usage': {'id': {'name': 'id', 'pattern': '^airsample:\\d*'}}})

    altitude: Optional[float] = Field(None, description="""Altitude is the height of an object or point in relation to a specific reference point, such as the sea level.""", json_schema_extra = { "linkml_meta": {'alias': 'altitude', 'domain_of': ['AirSample']} })
    id: str = Field(..., description="""The unique identifier for the biosample.""", json_schema_extra = { "linkml_meta": {'alias': 'id', 'domain_of': ['Sample']} })
    latitude: Optional[float] = Field(None, description="""Latitude is a geographic coordinate which refers to the angle from a point on the Earth's surface to the  equatorial plane.""", ge=-90, le=90, json_schema_extra = { "linkml_meta": {'alias': 'latitude', 'domain_of': ['Sample'], 'slot_uri': 'schema:latitude'} })
    longitude: Optional[float] = Field(None, description="""Longitude is a geographic position that refers to the angle east or west of a reference meridian between the  two geographical poles to another meridian that passes through an arbitrary point.""", json_schema_extra = { "linkml_meta": {'alias': 'longitude', 'domain_of': ['Sample'], 'slot_uri': 'schema:longitude'} })
    species: Optional[List[SpeciesEnum]] = Field(None, description="""The species of micro organisms collected in the sample.""", json_schema_extra = { "linkml_meta": {'alias': 'species', 'domain_of': ['Sample']} })
    sample_biome: Optional[BiomeTypeEnum] = Field(None, description="""The biome type of the biosample""", json_schema_extra = { "linkml_meta": {'alias': 'sample_biome', 'domain_of': ['Sample']} })
    sample_type: Literal["AirSample"] = Field("AirSample", description="""The type of sample.""", json_schema_extra = { "linkml_meta": {'alias': 'sample_type', 'designates_type': True, 'domain_of': ['Sample']} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^airsample:\d*")
        if isinstance(v,list):
            for element in v:
                if not pattern.match(element):
                    raise ValueError(f"Invalid id format: {element}")
        elif isinstance(v,str):
            if not pattern.match(v):
                raise ValueError(f"Invalid id format: {v}")
        return v


class SoilSample(Sample):
    """
    A sample of soil
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/linkml-tutorial-2024',
         'slot_usage': {'id': {'name': 'id', 'pattern': '^soilsample:\\d*'}}})

    depth: Optional[int] = Field(None, description="""The depth in centimeters of the biosample.""", json_schema_extra = { "linkml_meta": {'alias': 'depth', 'domain_of': ['SoilSample']} })
    id: str = Field(..., description="""The unique identifier for the biosample.""", json_schema_extra = { "linkml_meta": {'alias': 'id', 'domain_of': ['Sample']} })
    latitude: Optional[float] = Field(None, description="""Latitude is a geographic coordinate which refers to the angle from a point on the Earth's surface to the  equatorial plane.""", ge=-90, le=90, json_schema_extra = { "linkml_meta": {'alias': 'latitude', 'domain_of': ['Sample'], 'slot_uri': 'schema:latitude'} })
    longitude: Optional[float] = Field(None, description="""Longitude is a geographic position that refers to the angle east or west of a reference meridian between the  two geographical poles to another meridian that passes through an arbitrary point.""", json_schema_extra = { "linkml_meta": {'alias': 'longitude', 'domain_of': ['Sample'], 'slot_uri': 'schema:longitude'} })
    species: Optional[List[SpeciesEnum]] = Field(None, description="""The species of micro organisms collected in the sample.""", json_schema_extra = { "linkml_meta": {'alias': 'species', 'domain_of': ['Sample']} })
    sample_biome: Optional[BiomeTypeEnum] = Field(None, description="""The biome type of the biosample""", json_schema_extra = { "linkml_meta": {'alias': 'sample_biome', 'domain_of': ['Sample']} })
    sample_type: Literal["SoilSample"] = Field("SoilSample", description="""The type of sample.""", json_schema_extra = { "linkml_meta": {'alias': 'sample_type', 'designates_type': True, 'domain_of': ['Sample']} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^soilsample:\d*")
        if isinstance(v,list):
            for element in v:
                if not pattern.match(element):
                    raise ValueError(f"Invalid id format: {element}")
        elif isinstance(v,str):
            if not pattern.match(v):
                raise ValueError(f"Invalid id format: {v}")
        return v


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
SampleCollection.model_rebuild()
Sample.model_rebuild()
AirSample.model_rebuild()
SoilSample.model_rebuild()

