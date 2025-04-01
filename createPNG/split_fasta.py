import os
import argparse
from pathlib import Path
def split_fasta_to_files(input_fasta, output_directory):

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
  
    current_header = None
    current_sequence = []
    
 
    with open(input_fasta, 'r') as infile:
        for line in infile:
            line = line.strip()
            if line.startswith(">"): 
             
                if current_header:
                    save_sequence(current_header, current_sequence, output_directory)
                    current_sequence = []  
                current_header = line 
            else:
                current_sequence.append(line) 
     
        if current_header:
            save_sequence(current_header, current_sequence, output_directory)

def save_sequence(header, sequence, output_directory):
   
    filename = header.lstrip(">").split()[0][:100] + ".fa"
    filepath = os.path.join(output_directory, filename)
    

    with open(filepath, 'w') as outfile:
        outfile.write(header + "\n") 
        outfile.write("\n".join(sequence) + "\n") 
    print(f"Saved: {filepath}")

def main():
    parser = argparse.ArgumentParser(description="Split a FASTA collection file into individual FASTA files.")
    parser.add_argument("input_fasta", type=str, help="Path to the input FASTA collection file.")
    args = parser.parse_args()

    input_path = Path(args.input_fasta)

    if not input_path.exists():
        print(f"Error: Input file {args.input_fasta} does not exist.")
        return


    input_dir = input_path.parent
    input_filename = input_path.stem


    output_dir = input_dir / input_filename
    output_dir.mkdir(parents=True, exist_ok=True)

    split_fasta_to_files(str(input_path), str(output_dir))
if __name__ == "__main__":
    main()
