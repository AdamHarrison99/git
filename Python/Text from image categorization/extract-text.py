import sys, os, cv2, string, shutil
import pytesseract as pt
from PIL import Image

#need to install tesseract to run this program
pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

#arg parse
if len(sys.argv) < 1:
    print("Please input image directory")
    exit()

if len(sys.argv) > 2:
    print("Unknown argument:", sys.argv[2])
    exit()

directory = sys.argv[1]

#loop over dir
for root, dirs, files in os.walk(directory):
    for name in files:
        #ignore Thumbs.db
        if name == "Thumbs.db":
            exit()

        #filename
        print(name)

        #Create useable file path
        path = os.path.join(root, name)

        #take image, invert to black on white, and extract selection
        image = cv2.imread(path, 0)
        thresh = 255 - cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        #TODO get top slice of image rather than course selection. Needs to beable to work with varying resolutions
        x,y,w,h = 151,88,1172,218
        ROI = thresh[y:y+h,x:x+w]

        #image to string
        result = pt.image_to_string(ROI, config='--psm 7')

        #remove ' /' from result. Can be commented out if desired, or added to in order to remove starting characters
        if "/" in result:
            result = result[2:]

        #ensure no " " or new lines are present for folder naming
        result = result.replace(" ", "").replace("\n", "")

        #create our new path
        new_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),result)
        print("Found name:", result)

        #create our new folder if not exist
        if not os.path.exists(new_path):
            os.makedirs(new_path)
            print("Directory created:", new_path)

        #move file to correct folder
        if os.path.exists(new_path):
            shutil.move(path, new_path)
            print("Moving to:", new_path)
