from pathlib import Path
import json

from src.metadata.models_metadata_result import MetadataResult
from src.metadata.models_schema_metadata import SchemaMetadata
from src.metadata.models_attribute import AttributeMetadata
from src.metadata.models_datatype import DatatypeMetadata
from src.metadata.models_description import DescriptionMetadata
from src.metadata.models_unit import UnitMetadata

def load_reference_metadata(
    reference_schema_file: Path,
) -> MetadataResult:

    with open(
        reference_schema_file,
        encoding="utf-8",
    ) as f:
        package = json.load(f)

    bundle = (
        package
        .get("oca_bundle", {})
        .get("bundle", {})
    )

    capture_base = bundle.get(
        "capture_base",
        {}
    )

    overlays = bundle.get(
        "overlays",
        {}
    )

    # ------------------------------------------------------------------
    # Meta Overlay
    #
    # Load schema title and description.
    # For now, use English only.
    # ------------------------------------------------------------------

    schema_metadata = None

    meta_overlays = overlays.get("meta", [])

    english_meta = next(
        (
            overlay
            for overlay in meta_overlays
            if overlay.get("language") == "eng"
        ),
        None,
    )

    if english_meta:
        schema_metadata = SchemaMetadata(
            title=english_meta.get("name", ""),
            description=english_meta.get("description", ""),
        )

    print(
        "REFERENCE TITLE:",
        schema_metadata.title
    )

    print(
        "REFERENCE DESCRIPTION:",
        schema_metadata.description[:100]
    )

    # ------------------------------------------------------------------
    # Label Overlay
    #
    # Build a lookup from:
    #
    #     attribute name -> column label
    #
    # Example:
    #
    #     call -> Call
    #     source -> Source
    #
    # We reuse these labels throughout the loader so that all metadata
    # uses the same column_name values.
    #
    # For now, use English only.
    # ------------------------------------------------------------------

    attribute_labels = {}

    label_overlays = overlays.get(
        "label",
        []
    )

    english_labels = next(
        (
            overlay
            for overlay in label_overlays
            if overlay.get("language") == "eng"
        ),
        None,
    )

    if english_labels:
        attribute_labels = english_labels.get(
            "attribute_labels",
            {}
        )


    # ------------------------------------------------------------------
    # Capture Base
    #
    # Build:
    #
    # - AttributeMetadata
    # - DatatypeMetadata
    #
    # Datatypes come directly from capture base.
    # Column names come from the label overlay.
    # ------------------------------------------------------------------

    attributes = []
    datatypes = []

    capture_attributes = capture_base.get(
        "attributes",
        {}
    )

    for attribute_name, datatype in (
        capture_attributes.items()
    ):

        column_name = attribute_labels.get(
            attribute_name,
            attribute_name,
        )

        attributes.append(
            AttributeMetadata(
                column_name=column_name,
                attribute=attribute_name,
            )
        )

        datatypes.append(
            DatatypeMetadata(
                column_name=column_name,
                datatype=datatype,
            )
        )


    # ------------------------------------------------------------------
    # Information Overlay
    #
    # Build:
    #
    # - DescriptionMetadata
    #
    # Descriptions come from:
    #
    #     attribute_information
    #
    # Keys are attribute names, so we translate them to the same
    # column_name used everywhere else.
    # ------------------------------------------------------------------

    descriptions = []

    information_overlays = overlays.get(
        "information",
        []
    )

    english_information = next(
        (
            overlay
            for overlay in information_overlays
            if overlay.get("language") == "eng"
        ),
        None,
    )

    if english_information:

        attribute_information = english_information.get(
            "attribute_information",
            {}
        )

        for attribute_name, description in (
            attribute_information.items()
        ):

            column_name = attribute_labels.get(
                attribute_name,
                attribute_name,
            )

            descriptions.append(
                DescriptionMetadata(
                    column_name=column_name,
                    description=description,
                )
            )

    # ------------------------------------------------------------------
    # Unit Overlay
    #
    # Build:
    #
    # - UnitMetadata
    #
    # Units come from:
    #
    #     attribute_unit
    #
    # As with descriptions, keys are attribute names and must be
    # translated to column names.
    # ------------------------------------------------------------------

    units = []

    unit_overlay = overlays.get(
        "unit",
        {}
    )

    attribute_units = unit_overlay.get(
        "attribute_unit",
        {}
    )

    for attribute_name, unit in (
        attribute_units.items()
    ):

        column_name = attribute_labels.get(
            attribute_name,
            attribute_name,
        )

        units.append(
            UnitMetadata(
                column_name=column_name,
                unit=unit,
            )
        )

    return MetadataResult(
        schema_metadata=schema_metadata,
        descriptions=descriptions,
        units=units,
        attributes=attributes,
        datatypes=datatypes,
    )