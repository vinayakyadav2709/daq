import csv
from datetime import datetime
    
def store(decoded_line):
    csv_file = 'output.csv'

    with open(csv_file, 'a', newline='') as file:
        csv_writer = csv.writer(file)

        result_list = []

        # Add current timestamp
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")
        result_list.append(formatted_time)
        
        # Convert the decoded line to a list of integers (0s and 1s)
        result_list.extend([int(char) if char in '01' else char for char in decoded_line.strip()])

        csv_writer.writerow(result_list)
        return result_list