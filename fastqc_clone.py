"""
FASTQC Clone - Quality control for FASTQ files
Main CLI tool
"""

import sys
import argparse
from report_generator import generate_html_report


def main():
    """Main entry point"""
    
    parser = argparse.ArgumentParser(
        description='FASTQC Clone - Quality control for FASTQ files',
        epilog='Example: python fastqc_clone.py data.fastq.gz'
    )
    
    parser.add_argument('input', help='Input FASTQ file')
    parser.add_argument('-o', '--output', default='quality_report.html',
                       help='Output HTML report filename')
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("  FASTQC Clone - Quality Control Analysis")
    print("="*60)
    print(f"Input: {args.input}")
    print(f"Output: {args.output}\n")
    
    try:
        generate_html_report(args.input, args.output)
        print("\n✓ Analysis complete!")
        print(f"✓ Report saved: {args.output}")
        print("="*60 + "\n")
    except FileNotFoundError:
        print(f"✗ Error: File '{args.input}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()