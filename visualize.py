import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

def plot_quality_profile(avg_qualities,output_file ="quality_profile.png"):
    """
    Create per-base quality score plot.
    
    This is the MAIN quality control plot - shows quality at each position.
    High quality at start, may drop at end = normal sequencing pattern.
    
    Args:
        avg_qualities: list of average quality scores per position
        output_file: where to save the plot
    """
    positions =list(range(1,len(avg_qualities)+1))
    
    plt.figure(figsize=(12,6))

    #plot the quality line
    plt.plot(positions,avg_qualities, linewidth = 2.4, color = "#2c5282", label = 'Average Quality')

    #Add quality thresholds as horizontal lines
    plt.axhline(y=30, color='#48bb78', linestyle='--', linewidth=2, label='Q30 (Good - 99.9%)', alpha=0.7)
    plt.axhline(y=20, color='#ed8936', linestyle='--', linewidth=2, label='Q20 (Acceptable - 99%)', alpha=0.7)
    plt.axhline(y=10, color='#e53e3e', linestyle='--', linewidth=2, label='Q10 (Poor - 90%)', alpha=0.7)
    
     # Formatting
    plt.xlabel('Position in Read (bp)', fontsize=12, fontweight='bold')
    plt.ylabel('Quality Score (Phred)', fontsize=12, fontweight='bold')
    plt.title('Per-Base Quality Score Profile', fontsize=14, fontweight='bold')
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, alpha=0.3, linestyle=':')
    plt.tight_layout()

     # Save
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"✓ Quality profile plot saved: {output_file}")
    plt.close()

def plot_quality_distribution(fastq_file, output_file="quality_distribution.png"):
    """
    Create histogram of overall quality score distribution.
    
    Shows how many bases have each quality score.
    
    Args:
        fastq_file: path to FASTQ file
        output_file: where to save the plot
    """
    from fastq_parse import read_fastq
    from quality_calculator import phred_to_quality
    
    quality_counts = {}  # {quality_score: count}
    
    for header, seq, qual in read_fastq(fastq_file):
        qualities = phred_to_quality(qual)
        for q in qualities:
            quality_counts[q] = quality_counts.get(q, 0) + 1
    
    # Prepare data for histogram
    scores = sorted(quality_counts.keys())
    counts = [quality_counts[s] for s in scores]
    
    plt.figure(figsize=(12, 6))
    plt.bar(scores, counts, color='#4299e1', edgecolor='#2c5282', linewidth=1.5)
    
    # Add threshold lines
    plt.axvline(x=30, color='#48bb78', linestyle='--', linewidth=2, label='Q30 threshold', alpha=0.7)
    plt.axvline(x=20, color='#ed8936', linestyle='--', linewidth=2, label='Q20 threshold', alpha=0.7)
    
    plt.xlabel('Quality Score (Phred)', fontsize=12, fontweight='bold')
    plt.ylabel('Number of Bases', fontsize=12, fontweight='bold')
    plt.title('Quality Score Distribution', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3, axis='y', linestyle=':')
    plt.tight_layout()
    
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"✓ Quality distribution plot saved: {output_file}")
    plt.close()


def plot_read_length_distribution(fastq_file, output_file="read_lengths.png"):
    """
    Create histogram of read length distribution.
    
    Most reads should be same length (except quality trimming).
    
    Args:
        fastq_file: path to FASTQ file
        output_file: where to save the plot
    """
    from fastq_parse import read_fastq
    
    read_lengths = []
    
    for header, seq, qual in read_fastq(fastq_file):
        read_lengths.append(len(seq))
    
    plt.figure(figsize=(12, 6))
    plt.hist(read_lengths, bins=50, color='#9f7aea', edgecolor='#6b46c1', linewidth=1.5)
    
    plt.xlabel('Read Length (bp)', fontsize=12, fontweight='bold')
    plt.ylabel('Number of Reads', fontsize=12, fontweight='bold')
    plt.title('Read Length Distribution', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3, axis='y', linestyle=':')
    plt.tight_layout()
    
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"✓ Read length distribution plot saved: {output_file}")
    plt.close()


if __name__ == "__main__":
    import sys
    from quality_calculator import calculate_per_base_quality
    
    if len(sys.argv) < 2:
        print("Usage: python visualize.py <fastq_file>")
        sys.exit(1)
    
    fastq_file = sys.argv[1]
    
    print("Generating visualizations...")
    print()
    
    # Generate all plots
    avg_qual = calculate_per_base_quality(fastq_file)
    plot_quality_profile(avg_qual)
    
    plot_quality_distribution(fastq_file)
    plot_read_length_distribution(fastq_file)
    
    print()
    print("✓ All visualizations complete!")