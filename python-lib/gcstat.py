class gcstat:
	def __init__(self, n, st, dur, type, beforeMem, afterMem, totalMem, used, gc):
		self.gc = gc
		self.id = n
		self.starttime = st
		self.duration = dur
		self.endtime = float(self.starttime) + float(self.duration)
		self.type = type
		self.beforeMem = beforeMem
		self.afterMem = afterMem
		self.totalMem = totalMem
		self.used = used

