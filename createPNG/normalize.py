import os
import argparse

def pad_sequence(sequence, target_length, padding_char='N'):

    if len(sequence) < target_length:
        padding_length = target_length - len(sequence)
        left_padding = padding_char * (padding_length // 2)
        right_padding = padding_char * (padding_length - len(left_padding))
        return left_padding + sequence + right_padding
    else:
        return sequence

def process_fa_file(input_file):

    with open(input_file, 'r') as file:
        content = file.read().strip()
    
    lines = content.split('\n')
    header = lines[0].strip()
    sequence = ''.join(lines[1:])

    if len(sequence) < 100:
        print(f"Skipping {os.path.basename(input_file)} (sequence length < 100)")
        os.remove(input_file)  # 删除小于 100 的文件
        return

    if 100 <= len(sequence) < 10000:
        # 补齐序列到 10K，文件名和 header 保持不变
        processed_sequence = pad_sequence(sequence, 10000)
        with open(input_file, 'w') as new_file:
            new_file.write(f"{header}\n")
            for k in range(0, len(processed_sequence), 60):
                new_file.write(processed_sequence[k:k+60] + '\n')
        print(f"Processed {os.path.basename(input_file)} (length: {len(sequence)})")

    elif len(sequence) >= 10000:
        # 大于 10K 的序列，分割并生成多个文件
        split_sequences = [sequence[j:j+10000] for j in range(0, len(sequence), 10000)]
        for j, split_sequence in enumerate(split_sequences):
            if len(split_sequence) < 10000:
                split_sequence = pad_sequence(split_sequence, 10000)
            part_header = f"{header}_part{j+1}"
            part_filename = f"{header.replace('>', '')}_part{j+1}.fa"
            part_filepath = os.path.join(os.path.dirname(input_file), part_filename)
            with open(part_filepath, 'w') as new_file:
                new_file.write(f"{part_header}\n")
                for k in range(0, len(split_sequence), 60):
                    new_file.write(split_sequence[k:k+60] + '\n')
        print(f"Processed {os.path.basename(input_file)} into {len(split_sequences)} parts")
        os.remove(input_file)
        
def normalize_fa_files(input_folder):

    for filename in os.listdir(input_folder):
        if filename.endswith('.fa'):
            input_file = os.path.join(input_folder, filename)
            process_fa_file(input_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Normalize and process FASTA files in a folder.")
    parser.add_argument("input_folder", type=str, help="Path to the input folder containing FA files.")
    args = parser.parse_args()

    normalize_fa_files(args.input_folder)
