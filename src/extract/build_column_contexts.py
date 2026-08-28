from src.extract.models_column_context import ColumnContext
from src.extract.models_column_match import ColumnMatch
from src.extract.models_evidence import EvidenceRecord
from src.ingest.tabular_models import TabularProfile


def build_column_contexts(
    matches: list[ColumnMatch],
    evidence: list[EvidenceRecord],
    tabular_profile: TabularProfile,
) -> list[ColumnContext]:

    contexts = []

    for column in tabular_profile.columns:

        column_matches = [
            match
            for match in matches
            if match.column_name == column.column_name
        ]

        if not column_matches:
            continue

        column_evidence = []

        for match in column_matches:
            entity_evidence = [
                record
                for record in evidence
                if record.entity_name == match.entity_name
            ]

            column_evidence.extend(entity_evidence)

        contexts.append(
            ColumnContext(
                column_profile=column,
                matches=column_matches,
                evidence=column_evidence,
            )
        )

    return contexts