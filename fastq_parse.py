import gzip
import sys

def read_fastq(file_path):
    """
    Parse FASTQ file and yield records.
    
    Args:
        file_path: Path to FASTQ file (.fastq or .fastq.gz)
    
    Yields:
        tuple: (header, sequence, quality) for each read
    """
    try:
        open_func = gzip.open if file_path.endswith(".gz") else open
        with open_func(file_path, "rt") as f:
            while True:
                header = f.readline().rstrip()
                if not header:
                    break
                
                sequence = f.readline().rstrip()
                plus = f.readline().rstrip()
                quality = f.readline().rstrip()
                
                # Basic validation
                if not header.startswith('@'):
                    print(f"Warning: Invalid header line: {header}")
                    continue
                
                if not plus.startswith('+'):
                    print(f"Warning: Invalid plus line: {plus}")
                    continue
                
                yield header, sequence, quality
    
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found!")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    file_path = "data/real_data.fastq.gz"
    count = 0
    for header, seq, qual in read_fastq(file_path):
        if count < 10:
            print(f"Read {count + 1}:")
            print(f"  ID: {header}")
            print(f"  Seq: {seq[:50]}...")
            print(f"  Qual: {qual[:50]}...")
            print()
        count += 1
    
    print(f"Total reads: {count:,}")