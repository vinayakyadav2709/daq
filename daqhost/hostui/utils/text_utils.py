from datetime import datetime

def store(decoded_line):
    text_file = 'output.txt'

    with open(text_file, 'a') as file:
        # Get the current timestamp
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")
        
        formatted_data = ''.join(char for char in decoded_line if char in '01')
        file.write(f"{formatted_time}: {formatted_data}\n")
        return f"{formatted_time}: {formatted_data}\n"