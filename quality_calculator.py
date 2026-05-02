"""
Calculate quality scores from FASTQ quality strings
"""

def phred_to_quality(quality_string):
    """
    Convert ASCII quality string to Phred scores.
    
    Phred+33 encoding (standard for Illumina 1.8+):
    ASCII character - 33 = Phred score
    
    Args:
        quality_string: ASCII quality string from FASTQ
    
    Returns:
        list: Phred quality scores (integers)
    
    Example:
        >>> phred_to_quality("IIIII")
        [40, 40, 40, 40, 40]
    """
    return [ord(char) - 33 for char in quality_string]


def calculate_per_base_quality(fastq_file):
    """
    Calculate average quality score at each base position.
    
    Args:
        fastq_file: Path to FASTQ file
    
    Returns:
        list: Average quality score for each position
    """
    from fastq_parse import read_fastq
    
    position_qualities = {}  # {position: [list of quality scores]}
    
    for header, seq, qual in read_fastq(fastq_file):
        qualities = phred_to_quality(qual)
        
        for pos, q in enumerate(qualities):
            if pos not in position_qualities:
                position_qualities[pos] = []
            position_qualities[pos].append(q)
    
    # Calculate average for each position
    avg_qualities = []
    for pos in sorted(position_qualities.keys()):
        avg = sum(position_qualities[pos]) / len(position_qualities[pos])
        avg_qualities.append(avg)
    
    return avg_qualities


def get_overall_stats(fastq_file):
    """
    Get overall quality statistics.
    
    Returns:
        dict: Statistics including total reads, average quality, etc.
    """
    from fastq_parse import read_fastq
    
    total_reads = 0
    total_bases = 0
    total_quality = 0
    
    for header, seq, qual in read_fastq(fastq_file):
        total_reads += 1
        qualities = phred_to_quality(qual)
        total_bases += len(qualities)
        total_quality += sum(qualities)
    
    return {
        'total_reads': total_reads,
        'total_bases': total_bases,
        'average_quality': total_quality / total_bases if total_bases > 0 else 0,
        'average_read_length': total_bases / total_reads if total_reads > 0 else 0
    }



def detect_bad_cycles(avg_qualities, threshold=20):
    """
    Detect positions with low average quality.
    
    Bad cycles = positions where average quality < threshold
    Common causes:
    - Sequencing errors at specific positions
    - Chemical degradation during sequencing
    - Optical issues on the sequencer
    
    Args:
        avg_qualities: list of average quality scores per position
        threshold: quality threshold (default Q20 = 99% accuracy)
    
    Returns:
        list: tuples of (position, quality) for positions below threshold
    
    Example:
        >>> avg_qual = [35, 38, 37, 15, 36, 38]  # Position 4 is bad
        >>> detect_bad_cycles(avg_qual, threshold=20)
        [(4, 15)]  # Returns position 4 with quality 15
    """
    bad_cycles = []
    
    for pos, qual in enumerate(avg_qualities):
        if qual < threshold:
            bad_cycles.append((pos + 1, qual))
    
    return bad_cycles


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python quality_calculator.py <fastq_file>")
        sys.exit(1)
    
    fastq_file = sys.argv[1]
    print("Calculating statistics...")
    print()
    
    # Get overall stats
    stats = get_overall_stats(fastq_file)
    
    print(f"Overall Statistics:")
    print(f"  Total reads: {stats['total_reads']:,}")
    print(f"  Total bases: {stats['total_bases']:,}")
    print(f"  Average quality: {stats['average_quality']:.2f}")
    print(f"  Average read length: {stats['average_read_length']:.1f} bp")
    
    # Calculate per-base quality
    print("\nCalculating per-base quality...")
    avg_qual = calculate_per_base_quality(fastq_file)
    
    print(f"\nFirst 10 positions:")
    for i, q in enumerate(avg_qual[:10]):
        print(f"  Position {i+1}: Q{q:.1f}")
    
    #Detect bad cycles
    print("\nDetecting bad cycles...")
    bad_cycles = detect_bad_cycles(avg_qual, threshold=20)
    
    if bad_cycles:
        print(f"\nBad cycles detected: {len(bad_cycles)} positions with Q < 20")
        print(f"\nFirst 10 bad cycles:")
        for pos, qual in bad_cycles[:10]:
            print(f"  Position {pos}: Q{qual:.1f}")
    else:
        print(f"\n✓ No bad cycles detected! All positions have Q >= 20")
        print(f"  Your sequencing data is EXCELLENT quality!")
    
    # Quality assessment
    if stats['average_quality'] >= 30:
        quality_rating = "EXCELLENT (Q30+)"
    elif stats['average_quality'] >= 20:
        quality_rating = "GOOD (Q20-Q30)"
    else:
        quality_rating = "POOR (Q<20 - consider trimming)"
    
    print(f"\nOverall Quality Assessment: {quality_rating}")
    print(f"\nAnalysis complete!")