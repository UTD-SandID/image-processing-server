
def get_error_message(code):
    if code == 1:
        return "Image needs to be taken from closer"
    elif code == 2:
        return "Object was not detected properly / no coin in frame"
    