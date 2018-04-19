import os 				# For env variables
import threading			# Enables use as module in slackbot
from time import sleep			# For sleep()
from datetime import datetime		# To get system time
from slackclient import SlackClient	# For Slack Client

Dante_Close_Hours = [1,9,17]

Dante_Open_Hours = [2,10,16]


'''	Class that defines a danteUpdater Thread
	This thread is responsible for updating the general channel
	5 minutes before Dantes Forest Closes, when Dante's Forest 
	closes, and when Dantes Forest opens again '''
class danteUpdater (threading.Thread):
	'''	Initializer for danteUpdater object
		Input:
			token: API token to commuicate with the slack team

		Output:
			danteUpdater object
	'''
	def __init__(self, token):
		threading.Thread.__init__(self)
		self.__sc = SlackClient(token)
		self.__lock = threading.Lock()
		self.__continue = True
		self.__send = True
		self.__longsleep = False
		self.__message = "Starting Dante's Updates"

	'''	Function that starts the updater in its own thread, called by start() SHOULD NOT
		BE CALLED BY ITSELF
		Input:
			N/A
		Output:
			N/A
	'''
	def run(self):
		print ("Starting Dantes Updater")
		self.start_loop()

	''' Main thread body, determines if a message needs to be sent, otherwise sleeps '''
	def start_loop (self):
		while True:
			self.__longSleep = False
			curTime = datetime.now()
			if curTime.hour in Dante_Close_Hours:
				if curTime.minute == 40:
					self.__message = "WARNING: Dante's Forest closes in 5 minutes"
					self.__send = True
				elif curTime.minute == 45:
					seelf.__message = "Dante's Forest is now closed"
					self.__send = True
			
			if curTime.hour in Dante_Open_Hours:
				if curTime.minute == 1:
					self.__message = "Dante's Forest is now open. Happy Hunting!"
					self.__send = True
					self.__longSleep = True
			if self.__send:
				self.__sc.api_call(
					"chat.postMessage",
					channel="#general",
					text=self.__message
					)
				self.__send = False
			
			if self.__longSleep:
				sleep(27000)
		
			sleep(60)

			self.__lock.acquire()
			if not self.__continue:
				self.__lock.release()
				break
			else:
				self.__lock.release()

	''' Function to  stop the updater thread, may take up to 7.5 hours to exit 
	    (will return immediately) '''
	def stop (self):
		self.__lock.aquire()
		self.__continue = False
		self.__lock.release()

# Run dantes updater if in main context
if __name__=='__main__':
	thing = os.environ['TESTING_TOKEN']
	manager = danteUpdater(thing)
	manager.start()
	input('Press any button to exit')
	manager.stop()
	print("Stopping thread (may take a long time)")
	manager.join()