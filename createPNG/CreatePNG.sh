#!/bin/bash

# 检查参数数量
if [ $# -ne 4 ]; then
    echo "Usage: bash CreatePNG.sh {input1.all.fa} {input2.all.fa} {Yass-master/src路径}"
    exit 1
fi


input1="$1"
input2="$2"
yass_src_path="$3"


if [ ! -d "$yass_src_path" ]; then
    echo "Error: Yass-master/src path does not exist."
    exit 1
fi


yass_executable=$(ls "$yass_src_path" | grep "^yass$")
if [ -z "$yass_executable" ]; then
    echo "Error: 'yass' executable not found in $yass_src_path. Please compile YASS first."
    exit 1
fi


php_version=$(php -v 2>/dev/null)
if [ $? -ne 0 ]; then
    echo "Error: PHP is not installed. Please install PHP first."
    exit 1
fi
echo "PHP version: $php_version"



script_dir=$(dirname "$0")
process_yass_script="$script_dir/process_yass.sh"
yass2dotplot_script="$script_dir/yass2dotplot.php"

if [ ! -f "$process_yass_script" ] || [ ! -f "$yass2dotplot_script" ]; then
    echo "Error: process_yass.sh or yass2dotplot.php not found in the same directory as this script."
    exit 1
fi

cp "$process_yass_script" "$yass_src_path/"
cp "$yass2dotplot_script" "$yass_src_path/"
echo "Copied process_yass.sh and yass2dotplot.php to $yass_src_path."



sed -i.bak "s|./yass-MacOSX64-4threads.bin|./yass|g" "$yass_src_path/process_yass.sh"
echo "Updated yass executable path in process_yass.sh."


input1_dir=$(dirname "$input1")
input1_name=$(basename "$input1" .fa)
input2_dir=$(dirname "$input2")
input2_name=$(basename "$input2" .fa)

input1_folder="$input1_dir/$input1_name"
input2_folder="$input2_dir/$input2_name"


echo "Step 1: Splitting FASTA files..."
python split_fasta.py "$input1"
python split_fasta.py "$input2"


if [ ! -d "$input1_folder" ] || [ ! -d "$input2_folder" ]; then
    echo "Error: Splitting failed. One or both output folders do not exist."
    exit 1
fi

echo "Step 2: Comparing and cleaning folders..."
python compareAndclean.py "$input1_folder" "$input2_folder"

echo "Step 3: Normalizing files..."
python normalize.py "$input1_folder"
python normalize.py "$input2_folder"


echo "Step 4: Processing with YASS and generating PNGs..."
cd "$yass_src_path"
bash process_yass.sh "$input1_folder" "$input2_folder"

echo "Pipeline completed successfully!"
