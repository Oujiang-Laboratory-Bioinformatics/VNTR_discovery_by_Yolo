# VNTR_discovery_by_Yolo
Discover VNTRs in the CDS extracted from the mouse genome with machine-learning-based tools.

## Concepts
Variable number tandem repeats (VNTRs) are important genome variations neglected in much of the previous research. Many of them, especially VNTRs in the coding sequence (CDS) of the genome, play important roles in biological processes. The discovery of VNTRs is difficult because these regions are difficult to assemble, and the annotation of genomes is not always reliable.
Here, we extract full CDS from _de novo_ assembly of 17 mouse strains and transfer alleles/orthologues from each gene into dot plots. Repeats with adiquit area (i.e. total length of VNTR) and density (i.e. length of each repeat unit) are selected by YOLO object detection algorithm. More than 300 protein-coding genes in the mouse genome have been detected to contain VNTRs, and most of them have not been reported before. 

## Usage

1. Preparation

Install YASS and YOLOv10, refer to the official documentation of the tools used.
Whole genome CDS are extracted with Subread Gffread https://subread.sourceforge.net/

2. Generating PNG Dot Plots

Use the `CreatePNG.sh` script to batch-generate PNG-format dot plots
 **Usage**:
   bash CreatePNG.sh {input1.all.fa} {input2.all.fa} {path/to/Yass-master/src}

3. Using YOLO for Prediction
Use the pre-trained weights for object detection
 **Usage**:
   yolo detect predict model=/dataset/best.pt source=Path_to_PNG_Folder_Generated_In_Previous_Step save_txt save_conf conf=0.25 iou=0.45

4. Post-processing Tools

4.1 Confidence Sorting and Filtering

 Traverse YOLO label files, sort them by confidence, and generate a list file.
 **Usage**:
   python output.py --input_folder {Path_to_YOLO_Label_Files} --output_file {Path_to_Output_List_File}


4.2 Aspect Ratio Filtering

 Filter detection results based on aspect ratio and save the results to a new file.
 **Usage**:

   python clean_rectangle.py--input_file {Path_to_Detection_Results_File} --output_file {Path_to_Output_Filtered_File} --min_ratio 0.9 --max_ratio 1.1

## An Example with GRCm39 v.s. PWK/PhJ

1. Mus_musculus.GRCm39.cds.all_SymbolOnly.fa and PWK3.5_S.fa in /dataset using the `CreatePNG/CreatePNG.sh` script to batch-generate PNG-format dot plots as raw data.
 
2. Labeled using `labelimg` for YOLO detection training and validation, located at `/dataset/yolov_set`.

3. Pre-trained Weights located at `/dataset/best.pt`, with Yolov10s Model and Pytorch 2.1 framework.
