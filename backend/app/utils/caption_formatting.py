
import datetime

def process_timestamps(input_dict):
    # Step 1: Remove milliseconds from the keys and concatenate words
    processed_dict = {}
    for timestamp, word in input_dict.items():
        # Parse the timestamp and remove milliseconds
        time_obj = datetime.datetime.strptime(timestamp, '%H:%M:%S.%f')
        time_str = time_obj.strftime('%H:%M:%S')
        
        # Concatenate the words with a space if they are different
        if time_str in processed_dict:
            if word not in processed_dict[time_str].split():  # Avoid duplicate words
                processed_dict[time_str] += ' ' + word
        else:
            processed_dict[time_str] = word

    return processed_dict

def clean_repeated_words(input_dict):
    # Sort the input dictionary by timestamps
    sorted_keys = sorted(input_dict.keys())
    cleaned_dict = {}
    prev_word = None
    
    for key in sorted_keys:
        words = input_dict[key].split()
        
        # Check if the first word is the same as the last word of the previous entry
        if prev_word and words[0] == prev_word:
            words = words[1:]  # Remove the first word
        
        # Join the words back together
        cleaned_dict[key] = ' '.join(words)
        
        # Update prev_word to the last word of the current entry
        if words:
            prev_word = words[-1]
        else:
            prev_word = None
    
    return cleaned_dict