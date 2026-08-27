# Approach: Evidence-Driven Metadata Extraction for Tabular Research Data

## Purpose

This project is a prototype for extracting structured metadata from heterogeneous research datasets.

The primary inputs are:

- Tabular data files (CSV, TSV, Excel, etc.)
- Associated README or documentation files

The long-term objective is to generate structured metadata that can later be transformed into an OCA Package schema.

Schema generation is not the current focus.

The current focus is the reliable collection, organization, and preservation of documentation evidence that may later support the creation of OCA overlays and schemas.

The project is designed around the principle that every metadata assertion should be traceable back to source documentation.

The project includes an experimentation framework designed to support prompt iteration and human review.

The goal of the experimentation framework is not yet automated scoring.

The immediate goal is to:

- run multiple datasets through the pipeline
- compare prompt sets
- preserve experiment outputs
- generate human-readable review reports
- support future evaluation and benchmarking efforts

---

# Design Principles

## Evidence First

The system separates evidence collection from metadata interpretation.

Rather than immediately generating metadata descriptions, datatypes, units, or ontology mappings, the system first builds a collection of evidence records extracted from documentation.

Conceptually:

```text
README
    ↓
Evidence Records
    ↓
Metadata Interpretation
    ↓
OCA Overlays
    ↓
OCA Package Schema
```

This approach provides:

- traceability
- auditability
- easier debugging
- easier reprocessing
- easier testing
- reduced dependence on a specific LLM implementation

Evidence becomes the durable artifact within the pipeline.

---

## Evidence Before Classification

A key architectural decision is that evidence collection should not classify information.

Evidence extraction should answer:

> What documentation exists about this entity?

It should not attempt to determine:

- descriptions
- units
- datatypes
- code lists
- ontologies
- constraints

Those interpretations are deferred to later stages.

For example:

```text
sst_degc: Associated sea surface temperature in degrees Celsius.
```

should initially be preserved as evidence:

```text
Associated sea surface temperature in degrees Celsius.
```

A later extraction stage may identify:

```text
Description:
Associated sea surface temperature

Unit:
degrees Celsius
```

This separation keeps evidence collection simple and model-independent.

---

## Column-Centric Design

The fundamental object in the system is the dataset column.

The final output will describe columns and their meaning.

Documentation may describe concepts using many different names, but the goal of the system is ultimately to determine:

- which concepts correspond to columns
- what those columns represent
- what supporting documentation exists

Because the final target is column-level metadata, extraction and reasoning should ultimately be organized around dataset columns rather than abstract concepts.

---

## Incremental Reasoning

The project is designed for use with small local language models.

Small models often struggle with:

- large context windows
- long structured outputs
- large JSON responses
- multi-step reasoning
- classification-heavy tasks

To improve reliability, the workflow is decomposed into smaller stages.

Instead of asking a model to:

```text
Read README
+
Discover entities
+
Find evidence
+
Classify datatypes
+
Identify units
+
Produce schema
```

the system performs many focused extraction tasks with small outputs.

The objective is to minimize the information processed during any single model invocation.

---

## Separation of Concerns

The project distingishes between:

```text
src/
    Pipeline implementation

prompts/
    Experimental prompt variants

evaluation/
    Benchmark datasets
    Experiment execution
    Human review artifacts
```

The pipeline itself should remain unchanged regardless of the experiment being run.

Experiments vary Dataset and Prompt Set.

### Prompt Sets
Prompts are organized into versioned prompt sets.

Example:

```text
prompts/
│
├── baseline/
│   ├── discover_entities.txt
│   ├── extract_evidence.txt
│   └── matching_entities.txt
│
├── entity_v2/
│   ├── discover_entities.txt
│   ├── extract_evidence.txt
│   └── matching_entities.txt
│
└── entity_v3/
    ├── discover_entities.txt
    ├── extract_evidence.txt
    └── matching_entities.txt
```
Each prompt set must contain the same prompt filenames.

This allows experimentation to change prompt wording while keeping pipeline logic unchanged.

### Evaluation Datasets
Benchmark datasets are stored separately from normal pipeline inputs.

Example:
```text
evaluation/
└── datasets/
    ├── vibrio/
    │   ├── data.csv
    │   └── README.txt
    │
    └── dairy/
        ├── data.csv
        └── README.txt
```
Each dataset follows a standard structure:
```text
dataset/
├── data.csv
└── README.txt
```

Datasets whose folder names begin with an underscore ```_``` are ignored by the experiment runner. e.g _vibrio.

---

## Experiment Runner

Experiments are executed using: ```evaluation/run_experiment.py```
The runner automatically:
```text
Discover Prompt Sets
        ↓
Discover Datasets
        ↓
Execute Pipeline
        ↓
Store Artifacts
        ↓
Generate Reports
```

---
## Pipeline 
The orchestrator now returns a structured result object.
```text
@dataclass
class PipelineResult:
    entities: list[DiscoveredEntity]
    evidence: list[EvidenceRecord]
    matches: list[ColumnMatch]
```
Purpose:

- simplify review reporting
- support future evaluation metrics
- expose pipeline outputs directly to experiment tooling

## Experiment Output Structure
Each experiment execution creates a timestamped run directory.

Example:

```text
evaluation/
└── runs/
└── 2026-08-26_15-30-00/
```

All outputs generated during an experiment are stored beneath this run directory.

Example:

```text
evaluation/
└── runs/
    └── 2026-08-26_15-30-00/
        ├── baseline_vibrio.md
        ├── entity_v2_vibrio.md
        │
        ├── baseline/
        │   └── vibrio/
        │       ├── readme_profile.json
        │       ├── tabular_profile.json
        │       ├── entities.json
        │       ├── evidence.json
        │       └── matches.json
        │
        └── entity_v2/
            └── vibrio/
                ├── readme_profile.json
                ├── tabular_profile.json
                ├── entities.json
                ├── evidence.json
                └── matches.json

```
---
## Human Review Reports

Each dataset/prompt combination generates a Markdown report.

Reports are intended for manual review and prompt comparison.

Current report contents include:

```text
Dataset Information
Prompt Set
Summary Counts

Entities

Entity-to-Column Matches

Unmatched Entities

LLM Match Rationales

Evidence Records
```
Purpose:

- allow comparison of prompt versions
- avoid direct inspection of JSON artifacts
- support future scoring and benchmark development

---
# Current Data Models

## ReadmeProfile

Represents a README or documentation file.

```python
from dataclasses import dataclass

@dataclass
class ReadmeProfile:
    source_file: str
    content: str
    character_count: int
    line_count: int
```

Purpose:

- preserve README content
- provide source metadata
- serve as input to extraction processes

---
## ColumnProfile

Represents an observed column in a tabular dataset.

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class ColumnProfile:
    column_name: str
    source_position: int
    sample_values: List[str] = field(default_factory=list)
    missing_count: int = 0
    unique_count: int = 0
    inferred_datatypes: List[str] = field(default_factory=list)
```

Purpose:

- preserve observed structure from source data
- expose existing column names
- provide information useful for future matching and interpretation

---
## TabularProfile

Represents a tabular dataset.

```python
from dataclasses import dataclass

@dataclass
class TabularProfile:
    source_file: str
    columns: list[ColumnProfile]
```

Purpose:

- provide a complete description of dataset structure
- support future metadata extraction and harmonization workflows

---
## DiscoveredEntity

Represents a metadata concept discovered from documentation.

```python
from dataclasses import dataclass

@dataclass
class DiscoveredEntity:
    name: str
```

Purpose:

- represent concepts discovered within README documentation
- act as the focus of downstream evidence collection

Examples:

```text
date
vp_count_cfu
sst_degc
```

---
## EvidenceRecord

Represents documentation evidence associated with an entity.

```python
from dataclasses import dataclass

@dataclass
class EvidenceRecord:
    entity_name: str
    evidence_text: str
    source_section: str
    source_file: str
```

Purpose:

- preserve source documentation
- maintain traceability
- avoid premature interpretation
- support future overlay generation

At this stage, evidence records intentionally avoid metadata classification.

---
## ColumnMatch

Represents the association between a discovered entity and a dataset column.

Purpose:

- connect documentation concepts to dataset columns
- preserve LLM reasoning
- preserve supporting evidence
- create a bridge between documentation and column-level metadata extraction

```python
@dataclass
class ColumnMatch:
    entity_name: str
    column_name: str | None
    llm_rationale: str
    evidence_used: list[str]
)
```

This model is now part of the active pipeline.

---
## DescriptionMetadata

Represents a human-readable description associated with a matched dataset column. 
This hasn't been implemented yet.

```python
@dataclass 
class DescriptionMetadata: 
    column_name: str 
    description: str
```

Purpose:

- represent extracted field descriptions
- support future Description Overlay generation
- maintain separation between evidence collection and metadata interpretation

Example:

```text
DescriptionMetadata(
    column_name="sst_degc",
    description="Associated sea surface temperature"
)
```

---
## HarmonizedEntity

Represents a canonicalized metadata concept.

```python
from dataclasses import dataclass

@dataclass
class HarmonizedEntity:
    canonical_name: str
    source_terms: list[str]
```

Purpose:

- group related source terms
- support future metadata standardization
- provide a canonical identifier for later processing

Example:

```text
DATE
date
SampleDate
COL_DT
```

may become:

```python
HarmonizedEntity(
    canonical_name="sample_date",
    source_terms=[
        "DATE",
        "date",
        "SampleDate",
        "COL_DT"
    ]
)
```

This model exists but is not currently used in the active pipeline.

---
## PipelineResult

Represents the complete output of a pipeline execution.

```python
from dataclasses import dataclass

@dataclass
class PipelineResult:
    entities: list[DiscoveredEntity]
    evidence: list[EvidenceRecord]
    matches: list[ColumnMatch]
```
Purpose:

- expose pipeline outputs to downstream tooling
- support experiment reporting
- support future evaluation workflows
- avoid rereading intermediate artifacts from disk

The object is returned by the orchestrator after a successful run and serves as the primary interface between the pipeline and experimentation framework.


---
# Current Pipeline



## Stage 1: Data Profiling

The ingestion layer produces two independent representations.

### Documentation

```text
README
    ↓
ReadmeProfile
```



### Tabular Data

```text
CSV / TSV / Excel
    ↓
TabularProfile
```

At this stage the system only captures information directly observable from source files.

No semantic interpretation occurs.

---



## Stage 2: Entity Discovery

README content is analyzed to identify concepts that appear relevant to dataset metadata.

Conceptually:

```text
ReadmeProfile
+
TabularProfile
    ↓
Entity Discovery
    ↓
DiscoveredEntity List
```

Current implementation:

```python
collect_entities()
```

Example output:

```python
[
    DiscoveredEntity("date"),
    DiscoveredEntity("vp_count_cfu"),
    DiscoveredEntity("sst_degc")
]
```

---



## Stage 3: Evidence Collection

Evidence is collected separately for each discovered entity.

Conceptually:

```text
DiscoveredEntity
    ↓
Evidence Extraction
    ↓
EvidenceRecord List
```

The objective is to find documentation passages that explicitly describe the entity.

The extraction stage should:

- preserve wording
- avoid inference
- avoid interpretation
- return the smallest relevant excerpt possible

Example:

```text
README

date: ISO-formatted date object; date Vp test was taken
```

Produces:

```python
EvidenceRecord(
    entity_name="date",
    evidence_text="date: ISO-formatted date object; date Vp test was taken",
    source_section="Metadata",
    source_file="README.txt"
)
```

---



# Current Workflow

```text
CSV
    ↓
profile_tabular()
    ↓
TabularProfile


README
    ↓
profile_readme()
    ↓
ReadmeProfile


ReadmeProfile
+
TabularProfile
    ↓
collect_entities()
    ↓
DiscoveredEntity List


DiscoveredEntity List
+
ReadmeProfile
    ↓
collect_evidence()
    ↓
EvidenceRecord List


DiscoveredEntity List 
+ 
EvidenceRecord List 
+ 
TabularProfile 
    ↓ 
match_entities() 
    ↓ 
ColumnMatch List
```

---



# Planned Overlay-Oriented Workflow

The architecture is evolving toward an evidence-driven OCA overlay generation approach.

Rather than classifying evidence during extraction, specialized processing stages will operate on the evidence itself.

Conceptually:

```text
README
    ↓
Entity Discovery
    ↓
Evidence Collection
    ↓
Evidence Records
```

Then:

```text
Evidence Records
    ↓
Description Extraction
    ↓
Description Overlay
```

```text
Evidence Records
    ↓
Unit Extraction
    ↓
Unit Overlay
```

```text
Evidence Records
    ↓
Datatype Extraction
    ↓
Datatype Overlay
```

```text
Evidence Records
    ↓
Code List Extraction
    ↓
Code Overlay
```

```text
Evidence Records
    ↓
Ontology Extraction
    ↓
Ontology Overlay
```

Each overlay can be generated independently using focused prompts and specialized logic.

---

# Experimentation Framework (Planned)

## Purpose

Before introducing formal evaluation metrics and ground-truth datasets, the project should support structured experimentation and human review.

The initial goal is not to determine whether outputs are correct.

The initial goal is to make it easy to:

- run multiple datasets through the pipeline
- compare different prompt versions
- preserve outputs from each run
- support manual inspection and review

This creates a foundation for later automated evaluation.

Later:
```text
Dataset
    ↓
Pipeline Run
    ↓
Human Review
    ↓
Ground Truth
    ↓
Automated Evaluation
```
At the current stage, human review is sufficient.

## Experiment Structure
```text
evaluation/
│
├── datasets/
│   ├── vibrio/
│   ├── dairy/
│   └── ...
│
├── configs/
│
├── runs/
│
└── run_experiment.py
```
Purpose:
```text
datasets/
    benchmark datasets used for comparison

runs/
    preserved experiment outputs

configs/
    experiment definitions
```
## Datasets
Each dataset should contain all files required by the pipeline.

Example:
```text
evaluation/
└── datasets/
    └── vibrio/
        ├── data.csv
        └── README.txt
```
The experiment runner should automatically discover available datasets.

## Prompt focussed Experiments
The first experimentation focus should be prompt comparison rather than model comparison.

Example questions:
Does entity prompt v2 discover more useful entities?
Does evidence prompt v3 extract cleaner evidence?
Does a shorter prompt perform better than a longer prompt?

Initially, the model remains fixed.

Only prompts vary.

## Prompt sets
Prompts should be grouped into versioned prompt sets.

Example:
```text
prompts/
│
├── baseline/
│   ├── discover_entities.txt
│   ├── extract_evidence.txt
│   └── match_entities.txt
│
├── entity_v2/
│   ├── discover_entities.txt
│   ├── extract_evidence.txt
│   └── match_entities.txt
```
This allows an experiment to specify:

Use baseline prompts
or
Use entity_v2 prompts

without changing pipeline code.

## Experiment Configuration
An experiment should completely describe a run.

Conceptually:

```YAML
name: entity_v2
prompt_set: entity_v2
```

Future versions may also include:

```YAML
model: qwen3:8b
temperature: 0.0
```

but model experimentation is not the current priority.

## Experiment Runs
Running an experiment should automatically
```text
Load experiment configuration
    ↓
Find datasets
    ↓
Run orchestrator
    ↓
Save outputs
    ↓
Generate summary report
```

Example:
```text
runs/

2026-08-25_entity_v2/

    vibrio/
        entities.json
        evidence.json
        matches.json

    dairy/
        entities.json
        evidence.json
        matches.json

    summary.md
```
Each run becomes a permanent artifact that can be inspected later.

## Human Review Reports

Each experiment run should generate a simple review report.

Example:

```markdown
# Vibrio

## Entities

- date
- sst_degc
- vp_count_cfu

## Matches

date → date

sea surface temperature → sst_degc

## Evidence Counts

date: 2

sst_degc: 1

vp_count_cfu: 3
```
The objective is to allow reviewers to inspect results without reading JSON files.

## Future Expansion

Once prompt experimentation is stable, the same framework can support:

- model comparison
- temperature comparison
- parameter tuning
- automated scoring
- benchmark datasets
- ground truth comparisons

The pipeline itself should remain unchanged.

Experiments should vary:
```text
Dataset
Prompt Set
Model
Parameters
```
while the orchestrator continues to execute the same workflow.

---

# Experiment Before Evaluation

The project should progress through three stages:

```text
Dataset
    ↓
Pipeline Run
    ↓
Human Review
```


---

# Next Stage: Metadata Extraction

With entity matching now implemented, the pipeline can transition from evidence collection to metadata extraction.

The system now knows:

```text
Documentation Concept
        ↓
Evidence
        ↓
Dataset Column
```

The next question becomes: What metadata can be extracted from the evidence associated with this column?

The next planned processing stage is Description Extraction.

Conceptually:

```text
ColumnMatch
+
EvidenceRecord
    ↓
Description Extraction
    ↓
DescriptionMetadata
```

Example:

Evidence:

```text
sst_degc: Associated sea surface temperature in degrees Celsius.
```

Output:

```python
DescriptionMetadata(
column_name="sst_degc",
description="Associated sea surface temperature"
)
```

Once description extraction is working reliably, the same pattern can be applied to:

- units
- datatypes
- code lists
- ontologies

Each metadata type should be extracted independently from the same evidence records.

---



# Column Harmonization

Column names found in source datasets are often inconsistent.

Researchers may use:

```text
DATE
DATE1
COL_DT
SAMPLEDATE
dt
```

to represent the same concept.

Future processing stages will introduce harmonization.

Conceptually:

```text
Source Terms
    ↓
Canonical Concept
```

Example:

```text
DATE
SAMPLEDATE
COL_DT
    ↓
sample_date
```

The canonical identifier becomes the preferred representation for downstream processing.

The original source terms must always be preserved for traceability.

---



# Architectural Goals

The architecture should remain:

- simple
- inspectable
- modular
- testable
- model-agnostic

Each stage should produce explicit artifacts that can be:

- inspected
- serialized
- reused
- independently tested

Whenever possible, downstream stages should operate on structured intermediate representations rather than raw README content.

---



# Project Structure

```text
project/
│
├── data/
│   ├── input/
│   │   └── test_data/
│   │       ├── cfia_vibrio_data_public.csv
│   │       └── READMEvib.txt
│   │
│   ├── intermediate/
│   │   ├── entities.json
│   │   ├── evidence.json
│   │   ├── readme_profile.json
│   │   ├── tabular_profile.json
│   │   └── failed_column_responses.txt
│   │
│   └── output/
│
├── prompts/
│   ├── discover_entities.txt
│   ├── extract_evidence.txt
│   ├── matching_entities.txt
│   ├── extract_descriptions.txt
│   └── ...
│
├── src/
│   │
│   ├── orchestrator.py
│   │
│   ├── ingest/
│   │   ├── readme.py
│   │   ├── readme_models.py
│   │   ├── tabular.py
│   │   └── tabular_models.py
│   │
│   ├── extract/
│   │   ├── collect_entities.py
│   │   ├── collect_evidence.py
│   │   ├── match_entities.py
│   │   ├── extract_descriptions.py
│   │   │
│   │   ├── models_entities.py
│   │   ├── models_evidence.py
│   │   ├── models_column_match.py
│   │   ├── models_description.py
│   │   │
│   │   ├── save_entities.py
│   │   ├── save_evidence.py
│   │   ├── save_readme_profile.py
│   │   └── save_tabular_profile.py
│   │
│   ├── llm/
│   │   ├── client.py
│   │   └── load_prompt.py
│   │
│   └── utils/
│       └── json_utils.py
│
├── .env
├── requirements.txt
└── README.md
```

---



# Known Limitations



## Documentation Quality

README files vary significantly in quality.

Documentation may be:

- incomplete
- inconsistent
- ambiguous
- outdated
- written for humans rather than machines

Metadata quality will always be constrained by available documentation.

---



## Small Local LLM Constraints

The workflow assumes use of relatively small local language models.

These models may:

- generate malformed JSON
- struggle with context length
- miss evidence
- fail to classify consistently
- produce inconsistent outputs

The architecture therefore favors small focused tasks over large multi-purpose prompts.

---



## Imperfect Documentation-to-Column Mapping

Documentation does not always explicitly reference column names.

Many README files describe concepts without clearly identifying fields.

As a result, entity discovery, evidence collection, and later harmonization will remain probabilistic processes.

---



# Prototype Status

The project is currently focused on building a reliable evidence-driven metadata extraction pipeline. 

Completed stages: 

1. Data profiling
2. Entity discovery
3. Evidence collection
4. Entity-to-column matching

The current development priority is: 
5. Description extraction Planned near-term stages: 
6. Unit extraction 
7. Datatype extraction 
8. Code list extraction 
9. Ontology extraction 

Future stages: 

- harmonization 
- overlay generation 
- OCA Package generation

The primary research question is: 

> Can heterogeneous README documentation be transformed into structured, traceable evidence that can later support automated OCA overlay generation and schema construction? 

The current architectural hypothesis is: 

> Metadata extraction becomes significantly more reliable when documentation evidence is collected first, then linked to dataset columns, before any attempt is made to generate overlays or schemas.

