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
		print(refPt)

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


def locate_mouse(event, x, y, flags, param):
	global loc_new #asking function to use global varible
	if event == cv2.EVENT_LBUTTONDOWN: #left button used to add new points
		refPt = [(x, y)]
		print('addding')
		print(refPt)
		image=clone.copy()

		loc_new=np.append(loc_new,[[x,y,(1+len(loc_new[:,0]))]],axis=0)#add new values to the array



		print(np.shape(loc_new))

		for n in range(0,len(loc_new)):#loc_new includes clustered matches. Here it will draw squares around them
			# print(n)
			x=int(round(loc_new[n][0]))
			y=int(round(loc_new[n][1]))
			cv2.rectangle(image, (x,y), (x + w, y + h), (0,0,255), 2)
		cv2.imshow("Modify",image)


	elif event == cv2.EVENT_RBUTTONDOWN:#right button used to remove existing points
		print('removing')
		image=clone.copy()
		refPt = [(x, y)]
		print(refPt)

		# x=3280
		# y=2826
		#
		# x=loc_new[39][0]
		# y=loc_new[39][1]

		d_selected=x**2+y**2 #get Euclidean distance to the selected point

		distances=np.ones([len(loc_new[:,0]),1]) # will add distances from the origin of every detected point

		for n in range(0,len(loc_new[:,0])):#calculate and add Euclidean distances to the distance array
			distances[n][0]=(loc_new[n][0])**2+(loc_new[n][1])**2

		d_array=np.ones([len(loc_new[:,0]),1])*d_selected #create an array of same elements of d_selected
		subs=abs(distances-d_array)#substract the array and get the arugument

		min_val=np.nanmin(subs)#find min value
		min_idx=int(np.where(subs==min_val)[0]) #get iundex of the minimum value

		loc_new=np.delete(loc_new,min_idx,0)#delete row related to the picked point from the list

		for n in range(0,len(loc_new)):#loc_new includes clustered matches. Here it will draw squares around them
			# print(n)
			x=int(round(loc_new[n][0]))
			y=int(round(loc_new[n][1]))
			cv2.rectangle(image, (x,y), (x + w, y + h), (0,0,255), 2)
		cv2.imshow("Modify",image)



def mouseTrack_calibrate(event, x, y, flags, param):
	global x1,y1,x2,y2
	global first_coordinate
	if event == cv2.EVENT_LBUTTONDOWN and first_coordinate==False:
		print([(x, y)])
		x1=x
		y1=y
	elif event == cv2.EVENT_LBUTTONDOWN and first_coordinate==True:
		print([(x, y)])
		x2=x
		y2=y




#end of functon definition-----------------------------------------------


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

# load the image, clone it, and setup the mouse callback function
image = cv2.imread(args["image"])

'''
#to test code in ipython
image = cv2.imread('5main.png')
roi = cv2.imread('d1.png') #has 36 elements
roi = cv2.imread('a2.png') #has 18 elements
'''
clone = image.copy() #to reset the selection when 'r' pressed

# cv2.namedWindow("results",cv2.WINDOW_KEEPRATIO)
# cv2.namedWindow("results")
fileno=1 # to name the saved results
calibration=True # to run calibration code only once

# ==================Infinite loop from here=================
while True:  #infinite loop, this will go until user selects all elements
# While loop enabled

	refPt = [] #reset things
	cropping = False
	first_coordinate=False

	if calibration==True:
		#Let user do the px/mm calibration initially
		cv2.namedWindow("calibration",cv2.WINDOW_KEEPRATIO)
		cv2.setMouseCallback("calibration", mouseTrack_calibrate)

		while True:
			cv2.imshow("calibration", image)

			print("==========Calibration ==========")
			print("*You have to select two known points on the drawing in this step. Please make sure two points are not in same row or column*")
			print("")
			print("-Click the first point and press the space bar")
			cv2.waitKey(0)

			print("-Enter the coordinates of the point (mm)")
			x1_coord = input("x coordinate? ") #this is mm value
			y1_coord = input("y coordinate? ")

			first_coordinate=True
			print("Click the second point and press the space bar")
			cv2.waitKey(0)

			print("-Enter the coordinates of the point (mm)")
			x2_coord = input("x coordinate? ")
			y2_coord = input("y coordinate? ")

			print("If finish, press 'space bar', or to restart calibration process press 'r'")
			key = cv2.waitKey(0) & 0xFF


			x1_coord=float(x1_coord)
			x2_coord=float(x2_coord)
			y1_coord=float(y1_coord)
			y2_coord=float(y2_coord)

			if key == ord(" "):


				x_ratio=abs(x1_coord-x2_coord)/abs(x1-x2)
				y_ratio=abs(y1_coord-y2_coord)/abs(y1-y2)
				print(x_ratio)
				print(y_ratio)
				mmTopx_ratio=(x_ratio+y_ratio)*0.5 #take average

				if(x_ratio-y_ratio>1):
					print("x-ratio and y-ratio differs a lot. Please check!")
				else:
					print("Calibration done")
					print("mm to px ratio is")
					print(mmTopx_ratio)
					cv2.destroyWindow("calibration")
					calibration=False

				break
			else:
				pass


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
			print("Image reset")

		# if the 'c' key is pressed, break from the loop
		elif key == ord("c"):
			print("Cropping done")
			break


	image = clone.copy() #to clear the drawn selection boxes before processing

	# if there are two reference points, then crop the region of interest
	# from the image and display it
	if len(refPt) == 2:
		roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
		cv2.imshow("ROI", roi)
		cv2.waitKey(0)#wait until any key press




	#match template
	# cv2.imwrite('a2.png',roi) #if need to save a template from image
	img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	template = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)



	w, h = template.shape[::-1]
	res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
	res.shape
	img_gray.shape

	threshold = 0.8 #0.82
	loc = np.where( res >= threshold)
	np.shape(loc)
	type(loc)

	for pt in zip(*loc[::-1]):#take all points and draw rectangles
	    cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
	    #print(pt)

	# cv2.imwrite('results/r_detections.png',image)

	print("Matching done")

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

	for k in range(0,len(loc)): #Note:len(loc) gives one less 0123|4=not included

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

	#to display the selections before user modification
	'''
	for n in range(0,len(loc_new)):#loc_new includes clustered matches. Here it will draw squares around them
		# print(n)
		x=int(round(loc_new[n][0]))
		y=int(round(loc_new[n][1]))
		cv2.rectangle(image, (x,y), (x + w, y + h), (0,0,255), 2)
	'''

	#let  user select the matched points and edit them manually
	cv2.namedWindow("Modify",cv2.WINDOW_KEEPRATIO)
	cv2.setMouseCallback("Modify", locate_mouse)
	cv2.imshow("Modify",image) #show marked
	cv2.waitKey(0)

	image=clone.copy()
	for n in range(0,len(loc_new)):#loc_new includes clustered matches. Here it will draw squares around them
		# print(n)
		x=int(round(loc_new[n][0]))
		y=int(round(loc_new[n][1]))
		cv2.rectangle(image, (x,y), (x + w, y + h), (0,0,255), 2)

	#---------Distance calculation for time estimation. (loc_new =x ,y ,cluster number)-----------

	loc_new_copy=loc_new #take a copy ; leave loc_new unmodified for image clean
	distance=np.empty([len(loc_new[:,0]),3])#create empty ndarray x,y,distancefromreferencepoint

	xr=0 # n=0 is the first attempt we use the origin as the reference
	yr=0

	grpno=len(loc_new[:,0])+1 #this is number of elements +1. Was wrriten like this as previous code modified

	for n in range(0,grpno-1):

		xr_col=np.ones([grpno-1-n,1])*xr
		yr_col=np.ones([grpno-1-n,1])*yr

		x_diff=np.subtract(xr_col,loc_new_copy[:,0:1]) #xrColumn-xValueColumn
		y_diff=np.subtract(yr_col,loc_new_copy[:,1:2]) #yrColumn-yValueColumn

		d_sqrd=np.power(x_diff,2)+np.power(y_diff,2)
		min_val=np.nanmin(d_sqrd) #Note: if there is a Nan, it will be detected as the min number, to resolve use np.nanmin() instead of np.amin()
		# print(min_val)
		min_idx=int(np.where(d_sqrd==min_val)[0]) #get min value index

		distance[n][0]=loc_new_copy[min_idx][0] #x coordinate nth row
		distance[n][1]=loc_new_copy[min_idx][1] #y coordinate nth row
		distance[n][2]=int(np.sqrt(d_sqrd[min_idx])) #distance from reference point
		# following error happens if np.sqrt(d_sqrd[min_idx]) is empty
		# TypeError: only size-1 arrays can be converted to Python scalars


		loc_new_copy=np.delete(loc_new_copy,min_idx,0)#delete row related to the picked point from the list

		xr=distance[n][0] #update reference point (from picked point)
		yr=distance[n][1]

	np.shape(loc_new_copy)
	np.shape(distance)


	#next lets draw the machine head movement
	# x1=y1=x2=y2=int() #OverflowError: signed integer is less than minimum

	x2=(distance[0][0]).astype(int)
	y2=(distance[0][1]).astype(int)
	# print(distance)
	cv2.arrowedLine(image, (0,0), (x2,y2), (0,0,255), thickness=2, line_type=8, shift=0, tipLength=0)#from origin to 1st point

	for n in range(0,len(distance)-1):

		x1=(distance[n][0]).astype(int)
		y1=(distance[n][1]).astype(int)
		x2=(distance[n+1][0]).astype(int)
		y2=(distance[n+1][1]).astype(int)
		# cv2.line(image, (x1,y1), (x2,y2), (0,255,0), thickness=2, lineType=8, shift=0)
		cv2.arrowedLine(image, (x1,y1), (x2,y2), (0,0,255), thickness=2, line_type=8, shift=0, tipLength=0)
		# cv2.imwrite(imagename,image)
	# cv2.imshow("img",image)
	# cv2.waitKey(0)

	count_str='count = '+str(grpno-1)
	cv2.putText(image,count_str,(200,400),cv2.FONT_HERSHEY_SIMPLEX,5,(0,255,0),2)
	dist_str='distance(mm) = '+ str((np.sum(distance[:,2]))*mmTopx_ratio) #now distance is in mm
	cv2.putText(image,dist_str,(200,600),cv2.FONT_HERSHEY_SIMPLEX,5,(0,255,0),2)
	# cv2.putText(img,'Hello World!',bottomLeftCornerOfText,font,fontScale,fontColor,lineType)
	imagename='results/'+str(fileno)+'_matches.png'
	cv2.imwrite(imagename,image)
	filename='results/'+str(fileno)+'_coordinates.csv'
	np.savetxt(filename,distance,delimiter=',')
	print("Clustering finished")
	# print("No of elements:")
	# print(len(loc_new))

	#adding ROI and number of detections to a table
	result=np.ndarray([])
	result=template
	type(template)
	np.shape(result)
	cv2.imshow("results",roi)



	#clearing matching templates
	image = clone.copy() #load image again to avoid detection marks
	mask=np.ones((h, w))*255 #create a white mask, with the size of the template
	# img_gray=img_gray.astype(float) #change data type to avoid overflow
	image=image.astype(float)

	'''
	np.savetxt("img_gray.txt", template)
	img_gray=255-img_gray #inverting the image
	template=255-template#inverted template
	'''
	type(img_gray)
	img_gray.shape
	image.shape


	for n in range(0,len(loc_new)):
		x=int(round(loc_new[n][0]))
		y=int(round(loc_new[n][1]))

		# img_gray[y:h+y,x:w+x]=img_gray[y:h+y,x:w+x]-template

		# img_gray[y:h+y,x:w+x]=img_gray[y:h+y,x:w+x]+mask # Warning may have values more than 255

		#clear all 3 layers RGB (Using colored image to ,aintain image quality)
		image[y:h+y,x:w+x,0]=image[y:h+y,x:w+x,0]+mask # Warning may have values more than 255 : FIXED
		image[y:h+y,x:w+x,1]=image[y:h+y,x:w+x,1]+mask
		image[y:h+y,x:w+x,2]=image[y:h+y,x:w+x,2]+mask


	image[image > 255] = 255 #change values more than 255 to 255
	# print(image.dtype)
	image=np.uint8(image) # converting back to CV_8F to use COLOR_BGR2GRAY
	# print(image.dtype)


	#inverting back
	# img_gray=255-img_gray
	# cv2.imwrite('r_cleaned.png', img_gray)
	#cv2.imwrite('results/r_cleaned.png', image)
	print("Cleared")
	# np.savetxt("img_gray.txt", img_gray)
	# image=img_gray.copy() #new image is the cleaned image
	clone = image.copy()#clone is the new cleared image which is used in the next stage

	img_gray[x:h,y:w].shape
	#first try to clear one element
	img_gray.shape
	template.shape
	img_gray[0:h,0:w].shape
	img_gray[1:28,1:28].shape
	type(img_gray)
	# a=np.array([[2,3,4],[4,5,6],[6,7,9]])

	# img_gray[0:4,0:4]=np.array([[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1]])

	# cv2.imshow('img_cleared',img_gray)
	# cv2.waitKey(2000)





	# close all open windows
	# cv2.destroyAllWindows()

	#Close only image and ROI windows
	cv2.destroyWindow("image")
	cv2.destroyWindow("ROI")

	fileno=fileno+1
