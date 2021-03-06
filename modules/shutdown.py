# This file is part of photoframe (https://github.com/mrworf/photoframe).
#
# photoframe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# photoframe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with photoframe.  If not, see <http://www.gnu.org/licenses/>.
#
from threading import Thread
import select
import time
import subprocess

class shutdown(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.daemon = True
		self.gpio = 26
		self.start()


	def run(self):
		# Shutdown can be initated from GPIO26
		poller = select.poll()
		try:
			with open('/sys/class/gpio/export', 'wb') as f:
				f.write('%d' % self.gpio)
		except:
			# Usually it means we ran this before
			pass
		with open('/sys/class/gpio/gpio%d/direction' % self.gpio, 'wb') as f:
			f.write('in')
		with open('/sys/class/gpio/gpio%d/edge' % self.gpio, 'wb') as f:
			f.write('both')
		with open('/sys/class/gpio/gpio%d/value' % self.gpio, 'rb') as f:
			data = f.read()
			poller.register(f, select.POLLPRI)
			i = poller.poll(None)
			subprocess.call(['/sbin/poweroff'], stderr=DEVNULL);
			logging.debug('Shutdown GPIO triggered')
