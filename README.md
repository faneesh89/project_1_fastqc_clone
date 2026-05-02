# FASTQC Clone

A Python quality control tool for FASTQ sequencing files.

## Features

✓ Parse FASTQ files (gzip support)
✓ Calculate per-base quality scores
✓ Generate 3 professional QC plots
✓ Detect bad quality cycles
✓ Create comprehensive HTML reports
✓ Command-line interface

## Quick Start

```bash
python fastqc_clone.py input.fastq.gz
```

## Usage

```bash
# Basic usage
python fastqc_clone.py data.fastq.gz

# Custom output
python fastqc_clone.py data.fastq.gz -o my_report.html

# Help
python fastqc_clone.py -h
```

## Output

Generates `quality_report.html` containing:
- Overall quality statistics
- Per-base quality score profile
- Quality score distribution histogram
- Read length distribution
- Bad cycle detection results
- Quality assessment & recommendations

## Project Structure
fastqc_clone/
├── fastq_parser.py        # FASTQ file parsing
├── quality_calculator.py  # Quality metrics
├── visualize.py           # Plot generation
├── report_generator.py    # HTML report creation
├── fastqc_clone.py        # Main CLI tool
└── README.md              # This file

## Example

```bash
# Analyze real FASTQ data
python fastqc_clone.py data/real_data.fastq.gz

# View report
# Open quality_report.html in web browser
```

## Author

Faneesh Kumar - Genomics Data Analyst