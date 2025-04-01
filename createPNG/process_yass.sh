#!/bin/bash

# 检查参数数量
if [ $# -ne 3 ]; then
    echo "Usage: bash process_yass.sh folderA folderB folderC"
    exit 1
fi


folderA="$1"
folderB="$2"
folderC="$3"


mkdir -p "$folderC"


for fileA in "$folderA"/*.fa; do

    filenameA=$(basename "$fileA")
    headerA="${filenameA%.fa}"


    if [[ "$headerA" == *_part* ]]; then
        baseA="${headerA%_part*}"
        partA="${headerA##*_part}"
    else
        baseA="$headerA"
        partA=""
    fi

    if [ -n "$partA" ]; then
        filesB=("$folderB"/"${baseA}"*.fa)
    else
        filesB=("$folderB"/*.fa)
    fi


    for fileB in "${filesB[@]}"; do

        if [ -f "$fileB" ]; then

            filenameB=$(basename "$fileB")
            headerB="${filenameB%.fa}"


            if [[ "$headerB" == *_part* ]]; then
                baseB="${headerB%_part*}"
                partB="${headerB##*_part}"
            else
                baseB="$headerB"
                partB=""
            fi

            # 只有当 baseA 和 baseB 相同时才进行比较
            if [ "$baseA" = "$baseB" ]; then
                # 构造输出文件名
                if [ -n "$partA" ] && [ -n "$partB" ]; then
                    # 文件A和文件B都有 _partX
                    output_filename="${headerA}_${headerB}.yop"
                elif [ -n "$partA" ]; then
                    # 文件A有 _partX，文件B没有
                    output_filename="${headerA}_${baseB}.yop"
                elif [ -n "$partB" ]; then
                    # 文件A没有 _partX，文件B有
                    output_filename="${baseA}_${headerB}.yop"
                else
                    # 文件A和文件B都没有 _partX
                    output_filename="${baseA}_${baseB}.yop"
                fi


                output_file="$folderC/$output_filename"

                ./yass-MacOSX64-4threads.bin -M 3 -C 5,-4,-3,-4 -G -16,-4 -E 10 -X 30 -r 2 -d 1 -s 70 -o "$output_file" "$fileA" "$fileB"

                echo "Processed: $fileA and $fileB -> $output_file"
            fi
        fi
    done
done

echo "All files have been processed."
