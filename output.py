import os

def process_yolo_labels(input_folder, output_file):


    detections = []
    for filename in os.listdir(input_folder):
        if filename.endswith(".yop.txt"):
 
            sequence_name = filename[:-8]
            file_path = os.path.join(input_folder, filename)
  
            with open(file_path, 'r') as file:
                for line in file:
        
                    data = line.strip().split()
                    if len(data) >= 6:
                        confidence = float(data[1])
                        x1 = float(data[2])
                        y1 = float(data[3])
                        x2 = float(data[4])
                        y2 = float(data[5])

                        width = x2 - x1
                        height = y1 - y2
                        aspect_ratio = width / height if height != 0 else 0
                        
                        detections.append((sequence_name, confidence, aspect_ratio))
    

    detections.sort(key=lambda x: x[1], reverse=True)
    

    with open(output_file, 'w') as file:
        for detection in detections:
            file.write(f"{detection[0]}\n{detection[1]}\n{detection[2]}\n\n")



input_folder = "/Users/diana/yass+yolo/labels"
output_file = "/Users/diana/yass+yolo/320list.txt"
process_yolo_labels(input_folder, output_file)



