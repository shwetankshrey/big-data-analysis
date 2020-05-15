import random
import time
import tweepy

auth = tweepy.OAuthHandler('XXXX', 'XXXX')
auth.set_access_token('XXXX', 'XXXX')
api = tweepy.API(auth)

class CovidStreamListener(tweepy.StreamListener):

	def __init__(self):
		self.start_time = time.time()
		self.time_for_running = [600, 1200, 1800, 2400]
		self.current_time = 0
		self.iteration_count = 0
		self.user_id_count = 0
		self.user_id_values = {}
		super().__init__()

	def update_moment(self, user_id):
		if user_id not in self.user_id_values:
			self.user_id_count += 1
			if self.user_id_count > 10000:
				user_to_replace = random.randrange(self.user_id_count)
				if user_to_replace < 10000:
					user_id_to_replace = list(self.user_id_values.keys())[user_to_replace]
					self.user_id_values.pop(user_id_to_replace)
					self.user_id_values[user_id] = 0
			else:
				self.user_id_values[user_id] = 0
		if user_id in self.user_id_values:
			self.user_id_values[user_id] += 1

	def print_status(self, save):
		print("minuted", self.time_for_running[self.current_time])
		print("time elapsed:", time.time() - self.start_time)
		print("number of users:", self.user_id_count)
		print("moment:", int(self.user_id_count * sum((2 * value - 1) for value in self.user_id_values.values()) / len(self.user_id_values)))
		if save:
			f = open(str(self.time_for_running[self.current_time]) + "_results.txt", "a")
			f.write("\n\n\n")
			f.write("time elapsed:" + str(time.time() - self.start_time) + "\n")
			f.write("number of users:" + str(self.user_id_count) + "\n")
			f.write("moment:" + str(int(self.user_id_count * sum((2 * value - 1) for value in self.user_id_values.values()) / len(self.user_id_values))) + "\n")
			f.close()

	def on_status(self, status):
		self.update_moment(status.user.id_str)
		running_time = time.time()
		if (int(running_time - self.start_time) > self.time_for_running[self.current_time]):
			self.print_status(save = True)
			self.start_time = time.time()
			self.iteration_count += 1
			if self.iteration_count == 15:
				self.current_time += 1
				if self.current_time == 4:
					return False
			self.user_id_count = 0
			self.user_id_values = {}

def crawl_tweets_for_custom_time():
	my_covid_stream = tweepy.Stream(auth=api.auth, listener=CovidStreamListener())
	my_covid_stream.filter(track=['#Covid19','#Coronavirus'], is_async=True)

crawl_tweets_for_custom_time()