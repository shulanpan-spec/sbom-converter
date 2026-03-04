# SBOM Excel → SPDX 2.3 JSON Converter

Converts automotive **Software Bill of Materials (SBOM)** from Excel format to
[SPDX 2.3](https://spdx.github.io/spdx-spec/v2.3/) compliant JSON — the
industry-standard format required by EU Cyber Resilience Act and automotive
supply-chain compliance workflows.

Built for the automotive industry: handles VBF part numbers, CONTAINS /
DEPENDS_ON relationships, and multi-value cells out of the box.

## Why This Project

- Solves a real compliance workflow used in automotive software delivery
- Converts manual Excel-to-SPDX work from hours to seconds
- Handles real-world SBOM edge cases (multi-value cells, duplicate relationships)
- Produces clean, machine-readable SPDX 2.3 JSON for downstream tooling

---

## Features

- Reads structured SBOM data from Excel files (`Cover` + `SBOM` sheets)
- Outputs valid SPDX 2.3 JSON with correct package relationships
- Automatically establishes `VBF CONTAINS <all-other-packages>` relationships
- Handles `DEPENDS_ON` relationships between software components
- Batch processing: converts an entire folder in one command
- Clean output filenames based on VBF part numbers (e.g. `70049413BB.sbom.json`)
- Fast duplicate-relationship detection using hash sets (O(1) lookup)

---

## Motivation

In automotive software development, SBOM documentation is required for:

- **ISO 26262** functional safety case evidence
- **UNECE WP.29 / UN R155** cybersecurity compliance
- **EU Cyber Resilience Act** supply chain transparency

This tool automates the conversion step that is otherwise done manually,
reducing effort from hours to seconds per project.

---

## Getting Started

### Requirements

- Python 3.8+
- pip

### Installation

```bash
git clone https://github.com/shulanpan-spec/sbom-converter.git
cd sbom-converter
pip install -r requirements.txt
```

### Usage

```bash
# Convert all Excel files in current directory
python sbom_converter.py .

# Convert a single file
python sbom_converter.py SBOM-APP.xlsx

# Specify input folder and output directory
python sbom_converter.py ./input -o ./output

# Use a custom file pattern
python sbom_converter.py ./input -p "SBOM_*.xlsx" -o ./output
```

### Quick Run (30 seconds)

```bash
pip install -r requirements.txt
python sbom_converter.py ./input -o ./output
```

If `./input` contains `SBOM-70049413BB.xlsx`, output will be generated as
`./output/70049413BB.sbom.json`.

### Expected Excel Structure

| Sheet  | Required columns |
|--------|-----------------|
| Cover  | `VBF-part_number`, `spdxVersion`, `dataLicense`, `Organization` |
| SBOM   | `SPDXID`, `name`, `versionInfo`, `supplier`, `downloadLocation`, `licenseDeclared`, `copyrightText`, `relationshipType`, `relatedSpdxElement` |

---

## Output Example

```
Processing: SBOM-70049413BB.xlsx
  VBF part number: 70049413BB
  VBF CONTAINS relationships: 8
  Extracted: 9 packages, 18 relationships
  Saved: output/70049413BB.sbom.json (4.2 KB)

==============================
Done!
Total : 3  |  OK: 3  |  Failed: 0
```

Generated JSON follows the SPDX 2.3 schema:

```json
{
  "spdxVersion": "SPDX-2.3",
  "dataLicense": "CC0-1.0",
  "SPDXID": "SPDXRef-DOCUMENT",
  "packages": [ ... ],
  "relationships": [
    { "spdxElementId": "SPDXRef-Package-VBF",
      "relationshipType": "CONTAINS",
      "relatedSpdxElement": "SPDXRef-Package-APP" },
    ...
  ]
}
```

---

## Background

This project grew out of real work in the automotive embedded software
industry, where SBOM data is maintained in Excel by engineering teams but
needs to be submitted in SPDX format to OEM customers (VW, JLR, Volvo, etc.).

---

## Author

**Shulan Pan** — E/E Systems Engineer & Project Manager  
15+ years in automotive embedded software (GKN Driveline, Bosch Engineering)  
[LinkedIn](https://www.linkedin.com/in/shulan-pan-57063759/) · [GitHub](https://github.com/shulanpan-spec)

---

## License

MIT License — see [LICENSE](LICENSE) for details.
