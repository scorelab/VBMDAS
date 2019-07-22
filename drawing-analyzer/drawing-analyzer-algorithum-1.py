# USAGE
# python3 select_and_match1.py --image image.jpg

#User selects symbol using two mouse clicks (top-left and bottom-right corner of symbol)
#User press 'r' to reset if selection is wrong
#User press 'c' to crop if selection is ok
#Selection will be shown to the user
#User press 'space bar' to confirm
#Number of elements are counted
#Matching points wil be saved to the file 'r_matches.png'


# import the necessary packages
import argparse
import cv2
import numpy as np
from matplotlib import pyplot as plt

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
cropping = False

#functon definition-----------------------------------------------

def click_and_crop(event, x, y, flags, param):
	# grab references to the global variables
	global refPt, cropping

	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being
	# performed
	if event == cv2.EVENT_LBUTTONDOWN and cropping==False:
		refPt = [(x, y)]
		cropping = True
		print("Cropping Mode On")

	# elif event==cv2.EVENT_MOUSEMOVE and cropping==True:
	# 	cv2.rectangle(image, refPt[0], (x,y), (0, 0, 255), 2)
	# 	cv2.imshow("image", image)

		# check to see if the left mouse button was released
	# elif event == cv2.EVENT_LBUTTONUP:
	elif event == cv2.EVENT_LBUTTONDOWN and cropping==True:
		# record the ending (x, y) coordinates and indicate that
		# the cropping operation is finished
		refPt.append((x, y))
		cropping = False
		print("Cropping Mode Off")

		# draw a rectangle around the region of interest
		cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
		cv2.imshow("image", image)

#end of functon definition-----------------------------------------------


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

# load the image, clone it, and setup the mouse callback function
image = cv2.imread(args["image"])
clone = image.copy()


# cv2.namedWindow("image",cv2.WINDOW_KEEPRATIO)
cv2.namedWindow("image",cv2.WINDOW_KEEPRATIO)
cv2.setMouseCallback("image", click_and_crop)

# keep looping until the 'q' key is pressed
while True:
	# display the image and wait for a keypress
	cv2.imshow("image", image)
	key = cv2.waitKey(1) & 0xFF

	# if the 'r' key is pressed, reset the cropping region
	if key == ord("r"):
		image = clone.copy()

	# if the 'c' key is pressed, break from the loop
	elif key == ord("c"):
		break


image = clone.copy() #to clear the selection box before processing

# if there are two reference points, then crop the region of interest
# from the image and display it
if len(refPt) == 2:
	roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
	cv2.imshow("ROI", roi)
	cv2.waitKey(0)

'''
#to test code in ipython
image = cv2.imread('5main.png')
roi = cv2.imread('d1.png') #has 36 elements
'''


#match template
img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
template = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)


w, h = template.shape[::-1]
res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
res.shape
img_gray.shape

threshold = 0.82
loc = np.where( res >= threshold)
np.shape(loc)
type(loc)

for pt in zip(*loc[::-1]):#take all points and draw rectangles
    cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    #print(pt)

cv2.imwrite('r_matches.png',image)



#clustering

loc_x=loc[1][:]
loc_y=loc[0][:]

loc_x=loc_x.reshape(len(loc_x),1)
loc_y=loc_y.reshape(len(loc_y),1)

loc=np.hstack((loc_x,loc_y)) # x y creating a table of detections
zeros=np.zeros((len(loc_x),2))
loc=np.hstack((loc,zeros)) #x y d^2 group_number


# loc_a=np.asarray(loc_a) #convert tuple to an array
type(loc)
np.shape(loc)

grpno=1

for k in range(0,len(loc)): #Note:len(loc)-1 gives one less 0123|4=not included

	xk=loc[k][0] #take k th point
	yk=loc[k][1]

	if loc[k][3]==0:#check group number if no group assigned
		for n in range(0,len(loc)):
			loc[n][2]=(loc[n][0]-xk)**2+(loc[n][1]-yk)**2 #distance squared

		for n in range(0,len(loc)):#grouping
			if loc[n][2]<500:
				loc[n][3]=grpno
		grpno=grpno+1
	else:
		pass #do nothing

print("No of elements:",end = '')
print(grpno-1)



#averaging group clusters


x_avg=0
y_avg=0
# loc_new=np.ndarray()
loc_new=np.empty([grpno-1,3])#create empty ndarray x,y,group_no
type(loc_new)


for n in range(1,grpno):


	for k in range(0,len(loc)): #go through coordinate table
		if loc[k][3]==n :#if contains the group number
			x_avg=loc[k][0]+x_avg #this is only the sum
			y_avg=loc[k][1]+y_avg

	count=np.count_nonzero(loc[:,3] == n)
	x_avg=x_avg/count
	y_avg=y_avg/count

	loc_new[n-1][0]=x_avg
	loc_new[n-1][1]=y_avg
	loc_new[n-1][2]=n

	x_avg=0 #clear sum up values before moving into next group
	y_avg=0





'''
 this is old clustering algorithm- to delete
loc_new=[[x1,y1]] #this array contains the clustered element coordinates
# x=loc_new[0][0]
# y=loc_new[0][1]
np.shape(loc_new)
#type(loc_new)

for n in range(0,len(loc[0])-1):
	# print(n)

	# np.shape(loc)# 2 cols , 1759 rows
	x1=loc[1][n] #loc[row][col]
	y1=loc[0][n]

	x2=loc[1][n+1]
	y2=loc[0][n+1]

	d_sqrd=(x1-x2)**2 + (y1-y2)**2
	print(d_sqrd)

	if d_sqrd>50 :
		loc_new=loc_new+[[x2,y2]]


print(np.shape(loc_new))

# for pt in zip(*loc_new[::-1]):#take all points and draw rectangles
'''



for n in range(0,len(loc_new)):
	# print(n)
	x=int(round(loc_new[n][0]))
	y=int(round(loc_new[n][1]))
	cv2.rectangle(image, (x,y), (x + w, y + h), (255,0,0), 2)


cv2.imwrite('r_clusters.png',image)
print("No of elements:")
print(len(loc_new))


#clearing matching templates
mask=np.ones((h, w))*255 #create a white mask, with the size of the template
img_gray=img_gray.astype(float) #change data type to avoid overflow
'''
np.savetxt("img_gray.txt", template)
img_gray=255-img_gray #inverting the image
template=255-template#inverted template
'''
type(img_gray)
img_gray.shape

for n in range(0,len(loc_new)):
	x=int(round(loc_new[n][0]))
	y=int(round(loc_new[n][1]))

	# img_gray[y:h+y,x:w+x]=img_gray[y:h+y,x:w+x]-template
	img_gray[y:h+y,x:w+x]=img_gray[y:h+y,x:w+x]+mask # Warning may have values more than 255


#inverting back
# img_gray=255-img_gray
cv2.imwrite('r_cleaned.png', img_gray)
# np.savetxt("img_gray.txt", img_gray)
'''
img_gray[x:h,y:w].shape
#first try to clear one element
img_gray.shape
template.shape
img_gray[0:h,0:w].shape
img_gray[1:28,1:28].shape
type(img_gray)
# a=np.array([[2,3,4],[4,5,6],[6,7,9]])

# img_gray[0:4,0:4]=np.array([[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1]])

cv2.imshow('img_cleared',img_gray)
cv2.waitKey(2000)
'''




# close all open windows
cv2.destroyAllWindows()
