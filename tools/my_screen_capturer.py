import cv2
import sys

# s=0
# if len(sys.argv) > 1:
#     s = sys.argv[1]
# source = cv2.VideoCapture(s)

# win_name = 'Camera Preview'
# cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)

# while cv2.waitKey(1) != 27: #escape key
#     has_frame, frame = source.read()
#     if not has_frame:
#         break
#     cv2.imshow(win_name, frame)

# source.release()
# cv2.destroyWindow(win_name)

class ScreenCapturer:

    def __init__(self):
        self.s = 1
        if len(sys.argv) > 1:
            s = sys.argv[1]
        self.source = cv2.VideoCapture(self.s)

    def previewScreenCapture(self):
        win_name = 'Camera Preview'
        cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)

        while cv2.waitKey(1) != 27: #escape key
            has_frame, frame = self.source.read()
            if not has_frame:
                break
            cv2.imshow(win_name, frame)

        self.source.release()
        cv2.destroyWindow(win_name)

    def take_printscreen(self, filename):
        has_frame, frame = self.source.read()
        if has_frame:
            cv2.imwrite("results\\printscreens\\" + filename + '.jpg',frame)
        else:
            print("video capture device not working")
        #self.source.release()
            
            
        
