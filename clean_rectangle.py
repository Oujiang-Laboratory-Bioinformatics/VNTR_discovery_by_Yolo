def filter_detections_by_aspect_ratio(input_file, output_file, min_ratio=0.9, max_ratio=1.1):
  

    filtered_detections = []
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    i = 0
    while i < len(lines):
        
        if lines[i].strip() == "":
            i += 1
            continue
        sequence_name = lines[i].strip()
        i += 1
        confidence = lines[i].strip()
        i += 1
        aspect_ratio = float(lines[i].strip())
        i += 1
        if aspect_ratio <= min_ratio or aspect_ratio >= max_ratio:
            filtered_detections.append((sequence_name, confidence, aspect_ratio))

    with open(output_file, 'w') as file:
        for detection in filtered_detections:
            file.write(f"{detection[0]}\n{detection[1]}\n{detection[2]}\n\n")

input_file = "/Users/diana/yass+yolo/320list.txt" 
output_file = "/Users/diana/yass+yolo/320list_final.txt"

filter_detections_by_aspect_ratio(input_file, output_file)
