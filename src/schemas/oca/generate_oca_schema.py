from src.metadata.models_metadata_result import MetadataResult
from src.extract.models_column_context import ColumnContext

def generate_oca_schema(
    metadata: MetadataResult,
    contexts: list[ColumnContext],
) -> dict:

    # Fast lookups by column name
    attributes_by_column = {
        item.column_name: item.attribute
        for item in metadata.attributes
    }

    datatypes_by_column = {
        item.column_name: item.datatype
        for item in metadata.datatypes
    }

    descriptions_by_column = {
        item.column_name: item.description
        for item in metadata.descriptions
    }

    units_by_column = {
        item.column_name: item.unit
        for item in metadata.units
    }

    schema = {}

    attributes = {}
    attribute_labels = {}
    attribute_information = {}
    attribute_unit = {}
    attribute_ordering = []

    ordered_contexts = sorted(
        contexts,
        key=lambda c: c.column_profile.source_position,
    )

    for context in ordered_contexts:
        column_name = context.column_profile.column_name

        attribute_name = attributes_by_column.get(column_name)
        if not attribute_name:
            continue

        attribute_ordering.append(attribute_name)

        attributes[attribute_name] = datatypes_by_column.get(
            column_name,
            "Text",
        )

        attribute_labels[attribute_name] = column_name

        if column_name in descriptions_by_column:
            attribute_information[attribute_name] = (
                descriptions_by_column[column_name]
            )

        unit = units_by_column.get(column_name)
        if unit:
            attribute_unit[attribute_name] = unit

    schema = {
        "d": "########",
        "type": "oca_package/1.0",
        "oca_bundle": {
            "bundle": {
                "v": "########",
                "d": "########",
                "capture_base": {
                    "d": "########",
                    "type": "spec/capture_base/1.1",
                    "attributes": attributes,
                    "classification": "",
                    "flagged_attributes": [],
                },
                "overlays": {
                    "information": [
                        {
                            "d": "########",
                            "capture_base": "########",
                            "type": "spec/overlays/information/1.1",
                            "language": "eng",
                            "attribute_information": attribute_information,
                        }
                    ],
                    "label": [
                        {
                            "d": "########",
                            "capture_base": "########",
                            "type": "spec/overlays/label/1.1",
                            "language": "eng",
                            "attribute_categories": [],
                            "attribute_labels": attribute_labels,
                            "category_labels": {},
                        }
                    ],
                    "meta": [
                        {
                            "d": "EG_72B4ZH_mNT9iNdrgBT4VERVoCUjuRaJDMm17GpJK5",
                            "capture_base": "ENIUkQ1erbhEshQzpB30F6cbUlLUqeBoMhcQMJ77-hm2",
                            "type": "spec/overlays/meta/1.1",
                            "language": "eng",
                            "description": metadata.schema_metadata.description,
                            "name": metadata.schema_metadata.title,
                        }
                    ],
                    "unit": {
                    "d": "EJh0C8T_vIy3WojjC_6ztJ_YBBS7BC3w4jrFrYu3Igdm",
                    "capture_base": "ENIUkQ1erbhEshQzpB30F6cbUlLUqeBoMhcQMJ77-hm2",
                    "type": "spec/overlays/unit/1.1",
                    "attribute_unit": attribute_unit,
                    }
                }
            },
            "dependencies": [],
        },
        "extensions": {
            "adc": {
                "########": {
                    "d": "########",
                    "type": "community/adc/extension/1.0",
                    "overlays": {
                        "ordering": {
                            "d": "########",
                            "capture_base": "########",
                            "type": "community/overlays/adc/ordering/1.0",
                            "attribute_ordering": attribute_ordering,
                            "entry_code_ordering": {},
                        }
                    }
                }
            }
        }
    }

    return schema