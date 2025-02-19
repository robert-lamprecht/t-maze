import numpy as np
import cv2
import os
import pickle
from tqdm import tqdm
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilenames


# user selects video files
Tk().withdraw()
videoFiles = askopenfilenames(initialdir=r'N:\TMAZE\TMAZE_REFIND_VID_NEW',defaultextension='.mp4',filetypes=[('Video Files', '*.mp4')])

initial_coords = {} ### default locations for door centers
initial_coords['door1'] = [14, 36] # Floor Left
initial_coords['door2'] = [13, 125] # Floor Right
initial_coords['door3'] = [217, 183] # End Zone Top
initial_coords['door4'] = [223, 16]  # End Zone Bottom

global BLUE, RED

BLUE = [255,0,0]
RED = [0,0,255]


def mouse(event,x,y,flags,params): ## defining the callback for the door selection
    global move_rectangle, BLUE, fg, bg, bgCopy, final_coords, door, rows, cols
    #draw rectangle where x,y is rectangle center
    if event == cv2.EVENT_LBUTTONDOWN:
        move_rectangle = True

    elif event == cv2.EVENT_MOUSEMOVE:
        try:
            if move_rectangle:
                bg = bgCopy.copy() #!! your image is reinitialized with initial one
                cv2.rectangle(bg,(x-int(0.5*cols),y-int(0.5*rows)),
                (x+int(0.5*cols),y+int(0.5*rows)),BLUE, -1)
        except UnboundLocalError:
            pass

    elif event == cv2.EVENT_LBUTTONUP:
        move_rectangle = False
        cv2.rectangle(bg,(x-int(0.5*cols),y-int(0.5*rows)),
        (x+int(0.5*cols),y+int(0.5*rows)),BLUE, -1)
        final_coords[door] = [x,y]

def crop_video(video_path):
    """Crop video to region of interest using mouse dragging"""
    vid = cv2.VideoCapture(video_path)
    length = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    vid.set(cv2.CAP_PROP_POS_FRAMES, int(length/2))  # set to middle frame
    ret, frame = vid.read()
    
    # Create window
    cv2.namedWindow('Crop Video')
    
    # Initial crop rectangle (start with center 50% of frame)
    height, width = frame.shape[:2]
    rect = [width//4, height//4, 3*width//4, 3*height//4]  # [x1, y1, x2, y2]
    
    # Mouse interaction states
    dragging = False
    drag_corner = None
    drag_start = None
    
    def mouse_callback(event, x, y, flags, param):
        nonlocal dragging, drag_corner, drag_start, rect
        
        # Corner detection radius
        corner_radius = 20
        
        # Define corners
        corners = {
            'topleft': (rect[0], rect[1]),
            'topright': (rect[2], rect[1]),
            'bottomleft': (rect[0], rect[3]),
            'bottomright': (rect[2], rect[3])
        }
        
        if event == cv2.EVENT_LBUTTONDOWN:
            # Check if clicking near a corner
            for corner_name, (cx, cy) in corners.items():
                if ((x - cx)**2 + (y - cy)**2) < corner_radius**2:
                    dragging = True
                    drag_corner = corner_name
                    drag_start = (x, y)
                    return
                    
            # Check if clicking inside rectangle for moving entire box
            if (rect[0] < x < rect[2] and rect[1] < y < rect[3]):
                dragging = True
                drag_corner = 'move'
                drag_start = (x, y)
        
        elif event == cv2.EVENT_MOUSEMOVE and dragging:
            dx = x - drag_start[0]
            dy = y - drag_start[1]
            
            if drag_corner == 'move':
                # Move entire rectangle while keeping it within frame
                new_rect = rect.copy()
                new_rect[0] = max(0, min(width - 10, rect[0] + dx))
                new_rect[2] = max(10, min(width, rect[2] + dx))
                new_rect[1] = max(0, min(height - 10, rect[1] + dy))
                new_rect[3] = max(10, min(height, rect[3] + dy))
                if new_rect[2] - new_rect[0] >= 10 and new_rect[3] - new_rect[1] >= 10:
                    rect = new_rect
                drag_start = (x, y)
            
            else:
                # Update corner positions
                if drag_corner == 'topleft':
                    rect[0] = max(0, min(rect[2] - 10, x))
                    rect[1] = max(0, min(rect[3] - 10, y))
                elif drag_corner == 'topright':
                    rect[2] = max(rect[0] + 10, min(width, x))
                    rect[1] = max(0, min(rect[3] - 10, y))
                elif drag_corner == 'bottomleft':
                    rect[0] = max(0, min(rect[2] - 10, x))
                    rect[3] = max(rect[1] + 10, min(height, y))
                elif drag_corner == 'bottomright':
                    rect[2] = max(rect[0] + 10, min(width, x))
                    rect[3] = max(rect[1] + 10, min(height, y))
        
        elif event == cv2.EVENT_LBUTTONUP:
            dragging = False
            drag_corner = None
            drag_start = None
    
    cv2.setMouseCallback('Crop Video', mouse_callback)
    
    while True:
        display = frame.copy()
        
        # Draw the crop rectangle
        cv2.rectangle(display, (int(rect[0]), int(rect[1])), 
                     (int(rect[2]), int(rect[3])), (0, 255, 0), 2)
        
        # Draw corner handles
        for cx, cy in [(rect[0], rect[1]), (rect[2], rect[1]), 
                      (rect[0], rect[3]), (rect[2], rect[3])]:
            cv2.circle(display, (int(cx), int(cy)), 5, (0, 0, 255), -1)
        
        # Add instructions
        cv2.putText(display, "Drag corners to resize", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(display, "Drag inside to move entire box", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(display, "Press ENTER when done", (10, 90), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        cv2.imshow('Crop Video', display)
        
        if cv2.waitKey(1) & 0xFF == 13:  # Enter key
            break
    
    cv2.destroyAllWindows()
    vid.release()
    
    # Return crop coordinates in (top, bottom, left, right) format
    return (int(rect[1]), int(rect[3]), int(rect[0]), int(rect[2]))

def selectDoorCoords(video, initial_coords=initial_coords):
    print('On video {}'.format(video))
    vid = cv2.VideoCapture(video)
    length = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    vid.set(cv2.CAP_PROP_POS_FRAMES, int(length/2))
    ret, frame = vid.read()
    
    # Get crop region
    top, bottom, left, right = crop_regions[video]
    frame = frame[top:bottom, left:right]
    
    global fg, bg, bgCopy, move_rectangle, BLUE, RED, final_coords, door, rows, cols
    
    # Adjust initial coordinates based on crop region
    adjusted_coords = initial_coords.copy()
    for key in adjusted_coords:
        adjusted_coords[key] = [
            initial_coords[key][0] - left,  # Adjust x coordinate
            initial_coords[key][1] - top    # Adjust y coordinate
        ]
    
    # Display names mapping (only for GUI display)
    display_names = {
        'door1': 'Floor Left',
        'door2': 'Floor Right',
        'door3': 'Endzone Top',
        'door4': 'Endzone Bottom'
    }
    
    fg = frame[:14,:14] ## door size is about 15x15 pixels
    bg = frame ## middle frame of video
    bgCopy = bg.copy()
    move_rectangle = False
    final_coords = {}
    
    def draw_initial_coord(k, display_img):
        cv2.rectangle(display_img,
                     (adjusted_coords[k][0]-int(0.5*cols), adjusted_coords[k][1]-int(0.5*rows)),
                     (adjusted_coords[k][0]+int(0.5*cols), adjusted_coords[k][1]+int(0.5*rows)),
                     RED, -1)
    
    rows, cols = fg.shape[:2]
    
    for door in initial_coords.keys():
        window_name = f'Draw {display_names[door]} and press ENTER'
        cv2.namedWindow(window_name)
        cv2.setMouseCallback(window_name, mouse)
        while True:
            display_img = bg.copy()
            draw_initial_coord(door, display_img)
            cv2.imshow(window_name, display_img)
            k = cv2.waitKey(1)
            if k == 13 & 0xFF: ## enter key
                break
        cv2.destroyAllWindows()

    for door in initial_coords:
        try:
            print(f"{display_names[door]}: {final_coords[door]}")
        except KeyError:
            final_coords[door] = adjusted_coords[door]  # Use adjusted coordinates for defaults
            print(f"{display_names[door]}: {final_coords[door]}")

    return final_coords

def select_frame_range(video_path):
    """Select start and end frames for video analysis with playback controls"""
    vid = cv2.VideoCapture(video_path)
    total_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = vid.get(cv2.CAP_PROP_FPS)
    
    # Create window and trackbars
    cv2.namedWindow('Select Frame Range')
    
    def nothing(x):
        pass
    
    # Create trackbars for frame selection
    cv2.createTrackbar('Start Frame', 'Select Frame Range', 0, total_frames-1, nothing)
    cv2.createTrackbar('End Frame', 'Select Frame Range', total_frames-1, total_frames-1, nothing)
    cv2.createTrackbar('Current Frame', 'Select Frame Range', 0, total_frames-1, nothing)
    
    playing = False
    current_frame = 0
    
    while True:
        # Get current positions of trackbars
        start_frame = cv2.getTrackbarPos('Start Frame', 'Select Frame Range')
        end_frame = cv2.getTrackbarPos('End Frame', 'Select Frame Range')
        
        # Ensure end frame is after start frame
        if end_frame <= start_frame:
            end_frame = start_frame + 1
            cv2.setTrackbarPos('End Frame', 'Select Frame Range', end_frame)
        
        # If playing, increment current_frame
        if playing:
            current_frame += 1
            if current_frame >= end_frame:
                current_frame = start_frame
            cv2.setTrackbarPos('Current Frame', 'Select Frame Range', current_frame)
        else:
            current_frame = cv2.getTrackbarPos('Current Frame', 'Select Frame Range')
            
        # Show frame at current position
        vid.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
        ret, frame = vid.read()
        if ret:
            # Calculate times
            total_duration = total_frames / fps
            selected_duration = (end_frame - start_frame) / fps
            current_time = current_frame / fps
            
            # Format durations as MM:SS
            def format_time(seconds):
                minutes = int(seconds // 60)
                seconds = int(seconds % 60)
                return f"{minutes:02d}:{seconds:02d}"
            
            # Add text overlay
            info_text = [
                f'Start: Frame {start_frame} ({format_time(start_frame/fps)})',
                f'Current: Frame {current_frame} ({format_time(current_time)})',
                f'End: Frame {end_frame} ({format_time(end_frame/fps)})',
                f'Selected Duration: {format_time(selected_duration)}',
                f'Total Duration: {format_time(total_duration)}',
                '',
                'Controls:',
                'SPACE - Play/Pause',
                'ENTER - Confirm Selection',
                'ESC - Reset Selection'
            ]
            
            # Add each line of text
            y_position = 30
            for text in info_text:
                cv2.putText(frame, text, (10, y_position), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                y_position += 25
            
            # Draw progress bar (now safe from division by zero)
            frame_height, frame_width = frame.shape[:2]
            bar_y = frame_height - 50
            bar_width = int(((current_frame - start_frame) / max(1, end_frame - start_frame)) * frame_width)
            cv2.rectangle(frame, (0, bar_y), (frame_width, bar_y + 20), (0, 0, 255), -1)  # background
            cv2.rectangle(frame, (0, bar_y), (bar_width, bar_y + 20), (0, 255, 0), -1)  # progress
            
            cv2.imshow('Select Frame Range', frame)
        
        # Handle keyboard input
        key = cv2.waitKey(int(1000/fps)) & 0xFF  # Control playback speed using fps
        if key == 13:  # Enter key - confirm selection
            break
        elif key == 27:  # Esc key - reset selection
            cv2.setTrackbarPos('Start Frame', 'Select Frame Range', 0)
            cv2.setTrackbarPos('End Frame', 'Select Frame Range', total_frames-1)
        elif key == 32:  # Space key - toggle play/pause
            playing = not playing
    
    cv2.destroyAllWindows()
    vid.release()
    
    return (start_frame, end_frame)

def extractDoorTraces(video, door_coords):
    print('On video {}'.format(video))
    vid = cv2.VideoCapture(video)
    start_frame, end_frame = frame_ranges[video]
    
    # Set video to start frame
    vid.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    ret, frame = vid.read()
    
    # Get crop region
    top, bottom, left, right = crop_regions[video]
    frame = frame[top:bottom, left:right]
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    dc = door_coords[video]
    
    frameCounter = start_frame

    doorTraces = {}
    for door in range(4):
        doorkey = 'door{}'.format(door+1)
        doorTraces[doorkey] = []

    # Convert the first frame to grayscale
    gray1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    for frameCounter in tqdm(range(start_frame, end_frame)):
        # Read the next frame
        ret, frame2 = vid.read()
        if not ret:
            break

        # Crop the frame before processing
        frame2 = frame2[top:bottom, left:right]
        
        # Convert the current frame to grayscale
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    
        # Compute the absolute difference between the current frame and the previous frame
        diff = cv2.absdiff(gray1, gray2) 

        # Apply a threshold to get the binary image
        _, thresh = cv2.threshold(diff, 7, 255, cv2.THRESH_BINARY)
        
        
        doorImages = {}
        for door in range(4):
            doorkey = 'door{}'.format(door+1)
            doorImages[doorkey] = thresh[dc[doorkey][1]-7:dc[doorkey][1]+7, dc[doorkey][0]-7:dc[doorkey][0]+7]  ## PARAMETERIZE IN FUTURE
        # cv2.imshow('door1',doorImages['door1'])
        # Optional: Apply some morphological operations to reduce noise
        # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        # thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        # Highlight the motion areas in the original frame
        #motion_areas = cv2.bitwise_and(frame2, frame2, mask=thresh)

        # # Display the original frame and the thresholded difference
        # cv2.imshow('Original', frame2)
        # cv2.imshow('Motion Detection', motion_areas)
        
        
        
        for door in range(4):
            doorkey = 'door{}'.format(door+1)
            doorTraces[doorkey].append(np.sum(doorImages[doorkey]))
    

        # Update the previous frame
        gray1 = gray2
        
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    # Release the video capture object and close all OpenCV windows
    vid.release()
    cv2.destroyAllWindows()
    
    
    ### save doorTraces
    with open(video.split('.')[0]+'_doorTraces.pkl', 'wb') as f:
        pickle.dump(doorTraces, f, protocol=pickle.HIGHEST_PROTOCOL)

door_coords = {}
crop_regions = {}  # Store crop coordinates for each video
frame_ranges = {}  # Store frame ranges for each video

for file in videoFiles:
    print(f"Select crop region for {file}")
    crop_regions[file] = crop_video(file)
    print(f"Select frame range for {file}")
    frame_ranges[file] = select_frame_range(file)
    print(f"Select feature locations for {file}")
    door_coords[file] = selectDoorCoords(file, initial_coords=initial_coords)

for file in videoFiles:
    if os.path.exists(file.split('.')[0]+'_doorTraces.pkl'):
        print('Door traces already extracted for {}'.format(file))
        print('Skipping...')
    else:
        extractDoorTraces(file, door_coords=door_coords)