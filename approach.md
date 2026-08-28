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
    ↓
Metadata Extraction
```
---

# **Experiment Framework**

Experiments compare prompt sets across multiple datasets.

```text
Prompt Set
+
Dataset
    ↓
run_pipeline()
    ↓
PipelineResult
    ↓
Reports
```

The experiment runner:

* discovers datasets  
* discovers prompt sets  
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

This object is the interface between the pipeline and the experiment framework.

---

# **Current Status**

Implemented:

* Data profiling  
* Entity discovery  
* Evidence collection  
* Entity-to-column matching  
* Description extraction  
* Unit extraction  
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

This is probably closer to 3-5 pages instead of 25+, and future contributors are much more likely to read it.

