from PIL import Image, ImageGrab
import pytesseract
import numpy as np
import time

# Test from a file
# filename = 'data/new-world-1.png'
# img = np.array(Image.open(filename))
# text = pytesseract.image_to_string(img)
# print(text)
# exit()

go = True
itor = 0
while go:
    # Allow time to position windows, get focus, etc.
    time.sleep(5)

    bbox = [2800,200,3456,300]
    img = ImageGrab.grab(bbox=bbox, all_screens=False)
    location_raw = pytesseract.image_to_string(img)

    # Optionally show image for testing.
    img.show()

    starting_bracket_pos = location_raw.find('[')
    ending_bracket_pos = location_raw.find(']')
    not_found_pos = location_raw.find('*')

    print("Starting Bracket: " + str(starting_bracket_pos))
    print("Ending Bracket: " + str(ending_bracket_pos))

    # Skip this iteration if start/end brackets not recognized or if distance doesn't seem right.
    if(starting_bracket_pos == -1 or ending_bracket_pos == -1 or (ending_bracket_pos - starting_bracket_pos) < 20):
        print("Skipping iteration due to unreadable picture. The data returned by the ocr unit was \"" + location_raw + "\"")
        continue

    trimmed_location = location_raw[starting_bracket_pos+1:ending_bracket_pos-1]

    print("Trimmed String: " + trimmed_location)

    itor = itor + 1
    
    if itor > 10:
        go = False