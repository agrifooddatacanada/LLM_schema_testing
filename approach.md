# **Approach: Evidence-Driven Metadata Extraction**

## **Purpose**

This project explores the extraction of structured metadata from tabular research datasets and associated documentation.

Current inputs:

* Tabular data (CSV, TSV, Excel)  
* README or documentation files

Long-term outputs:

* OCA overlays  
* OCA package schemas

Current focus:

* Collect documentation evidence  
* Match documentation concepts to dataset columns  
* Extract metadata from that evidence  
* Support prompt experimentation and human review

---

# **Core Principles**

## **Evidence First**

The system collects evidence before attempting metadata extraction.

```text
README
    ↓
Evidence
    ↓
Metadata
    ↓
OCA Overlays
```

Every metadata assertion should be traceable to source documentation.

## **Column-Centric Design**

The primary object is the dataset column.

The goal is to determine:

* what each column represents  
* what evidence supports it  
* what metadata can be extracted

## **Incremental Processing**

The workflow is divided into small steps that are suitable for local LLMs.

```text
Profile Data
    ↓
Discover Entities
    ↓
Collect Evidence
    ↓
Match Columns
    ↓
Extract Metadata
```

## **Separation of Concerns**

```text
src/
    Extraction pipeline

prompts/
    Prompt sets

evaluation/
    Experimentation and reporting
```

The pipeline remains stable while prompts and datasets vary.

---

# **Current Workflow**

```text
README
    ↓
ReadmeProfile

Dataset
    ↓
TabularProfile

ReadmeProfile
+
TabularProfile
    ↓
Entity Discovery
    ↓
DiscoveredEntity

DiscoveredEntity
+
ReadmeProfile
    ↓
Evidence Collection
    ↓
EvidenceRecord

EvidenceRecord
+
TabularProfile
    ↓
Column Matching
    ↓
ColumnMatch

ColumnMatch
+
EvidenceRecord
+
ColumnContext
    ↓
Metadata Extraction
    ↓
MetadataResult
```
---

# **Experiment Framework**

Experiments compare prompt sets across multiple datasets.

```text
Experiment Config
+
Prompt Set
+
Dataset
    ↓
run_pipeline()
    ↓
PipelineResult
    ↓
run_metadata_pipeline()
    ↓
MetadataResult
    ↓
ExperimentResult
    ↓
Reports
```

The experiment runner:

* discovers datasets  
* discovers prompt sets  
* discovers experiment configurations for the llm
* executes the pipeline  
* stores artifacts  
* generates reports

Each run creates a timestamped directory.

```text
evaluation/runs/
    2026-08-28_10-00-00/
```

Outputs include:

* intermediate JSON artifacts  
* per-run reports  
* comparison reports  
* CSV summaries

Datasets beginning with `_` are ignored.

---

# **Key Data Models**

```text
ExperimentResult
├── Dataset Name
├── Prompt Set
├── ExperimentConfig
│   ├── Name
│   ├── Model
│   └── Temperature
│
└── MetadataResult
        ├── SchemaMetadata
        │ ├── Title
        │ └── Description
        |
        ├── Descriptions
        │   └── DescriptionMetadata
        │       ├── Column Name
        │       └── Description
        │
        ├── Units
        │   └── UnitMetadata
        │       ├── Column Name
        │       └── Unit
        │
        ├── Attributes
        │   └── AttributeMetadata
        │       ├── Column Name
        │       └── Attribute
        │
        └── Datatypes
            └── DatatypeMetadata
                ├── Column Name
                └── Datatype
```

```text
PipelineResult
├── ReadmeProfile
│   ├── Source File
│   ├── Content
│   ├── Character Count
│   └── Line Count
│
├── Entities
│   └── DiscoveredEntity
│       └── Name
│
├── Evidence
│   └── EvidenceRecord
│       ├── Entity Name
│       ├── Evidence Text
│       ├── Source Section
│       └── Source File
│
├── Matches
│   └── ColumnMatch
│       ├── Entity Name
│       ├── Column Name
│       ├── LLM Rationale
│       └── Evidence Used
│
└── Contexts
    └── ColumnContext
        ├── ColumnProfile
        │   ├── Column Name
        │   ├── Source Position
        │   ├── Sample Values
        │   ├── Missing Count
        │   ├── Unique Count
        │   └── Inferred Datatypes
        │
        ├── Matches
        └── Evidence
```

```text
Dataset
├── Name
├── Tabular File
└── README File
```

```text
TabularProfile
├── Source File
└── Columns
    └── ColumnProfile
        ├── Column Name
        ├── Source Position
        ├── Sample Values
        ├── Missing Count
        ├── Unique Count
        └── Inferred Datatypes
```

```text
ReadmeProfile
├── Source File
├── Content
├── Character Count
└── Line Count
```

## **DiscoveredEntity**

A documentation concept identified from the README.

Examples:

```text
date
sst_degc
vp_count_cfu
```
   
Show more lines

## **EvidenceRecord**

Documentation evidence associated with an entity.

Evidence is preserved without interpretation.

## **ColumnMatch**

A mapping between a documentation concept and a dataset column.

Includes rationale and supporting evidence.

## **PipelineResult**

The complete output of a pipeline run.

```text
PipelineResult
├── entities
├── evidence
├── matches
└── metadata
```

## **ExperimentResult**

The complete result of an experiment run. 

```text 
ExperimentResult 
├── dataset_name 
├── prompt_set 
├── experiment_config 
└── metadata
```

This object is the interface between the pipeline and the experiment framework.

## ExperimentConfig

Defines the settings used for a metadata extraction experiment.

Examples:

```text
model = Qwen2.5-Omni-7B-Q4_K_M
temperature = 0.0

---

# **Current Status**

Implemented:

* Data profiling
* Entity discovery
* Evidence collection
* Entity-to-column matching
* Description extraction
* Unit extraction
* Datatype extraction
* Metadata pipeline
* Experiment configurations
* Experiment runner
* Markdown reporting
* CSV reporting

Next priorities:

* Datatype extraction  
* Code list extraction  
* Ontology extraction  
* Evaluation metrics

Research question:

> Can heterogeneous README documentation be transformed into structured, traceable metadata suitable for downstream OCA generation?