__author__ = 'ssaar'

# This is an object to obtain information from a HELENA output file

import numpy as np
import os


class HelenaOutput:
	def get_data_from_line(self,line,ind):
		spl = line.split()
		try:
			output = float(spl[ind])
		except:
			output = 0.0
		return output

	def read_file(self):
		file = open(self.filename, 'r')
		self.crashed = True
		minpsi = 1.0 - max(self.delta_te, self.delta_ne)
		while True:
			line = file.readline()
			if line == '':
				break
			if 'NRMAP' in line:
				spl = line.split('NRMAP =')
				sp2=spl[1].split(',')
				npts = int(sp2[0])
			if 'NORM. BETA' in line:
				spl = line.split(':')
				self.betan = float(spl[1]) * 100
			if 'POLOIDAL BETA' in line:
				spl = line.split(':')
				self.betap = float(spl[1])
			if 'PED. BETAPOL' in line:
				spl = line.split(':')
				self.helenaBetap = float(spl[1])
			if 'VOLP' in line:
				self.area = np.zeros(npts)
				self.psi = np.zeros(npts)
				self.s = np.zeros(npts)
				self.vol = np.zeros(npts)
				line = file.readline()
				for i in range(npts - 1):
					line = file.readline()
					spl = line.split()
					self.psi[i + 1] = (float(spl[1]))
					self.area[i + 1] = (float(spl[-1]))
					self.s[i + 1] = (float(spl[2]))
					self.vol[i + 1] = (float(spl[-3]))
			if 'A,B,C' in line:
				spl = line.split(':')
				sp2 = spl[1].split()
				self.b_last_round = float(sp2[1])
			if 'I,     X,          PSI,          P,         Q' in line:
				line = file.readline()
				self.midplane_s = []
				self.midplane_psi = []
				while True:
					line = file.readline()
					if line.find('*****************') > -1:
						break
					sp = line.split()
					xnow = float(sp[1])
					if xnow > 0:
						self.midplane_psi.append(float(sp[2]))
						self.midplane_s.append(float(sp[1]))
				self.midplane_s = np.asarray(self.midplane_s)
				self.midplane_psi = np.asarray(self.midplane_psi)
			if 'ALPHA1' in line:
				self.crashed = False
				line = file.readline()
				q = []
				bal = []
				alpha = []
				shear = []
				psi_map = []
				while True:
					line = file.readline()
					if line.find('***************') > -1:
						break
					spl = line.split()
					try:
						psi_map.append(float(spl[1]))
					except:
						psi_map.append(0.0)
					try:
						bal.append(float(spl[8]))
					except:
						bal.append(0.0)
					if psi_map[-1] > 0.85:
						if bal[-1] < 1 and psi_map[-1] < self.balstart:
							self.balstart = psi_map[-1]
						if bal[-1] > 1 and psi_map[-1] > self.balstart and psi_map[-1] < self.balend:
							self.balend = psi_map[-1]
					try:
						alpha.append(float(spl[6]))
					except:
						alpha.append(0.0)
					try:
						shear.append(float(spl[5]))
					except:
						shear.append(1e3)
					try:
						q.append(float(spl[3]))
					except:
						q.append(0.0)
					if psi_map[-1] > minpsi:
						if alpha[-1] > self.max_alpha:
							self.max_alpha = alpha[-1]
						if shear[-1] < self.min_shear:
							self.min_shear = shear[-1]
				self.alpha = np.asarray(alpha)
				self.shear = np.asarray(shear)
				self.psi_map = np.asarray(psi_map)
				self.bal = np.asarray(bal)
				self.q = np.asarray(q)
			if 'RBPHI' in line:
				rbphi = []
				while True:
					line = file.readline()
					if line == ' \n':
						break
					spl = line.split()
					spl_float = [float(s) for s in spl]
					rbphi += spl_float

				self.rbphi = np.asarray(rbphi)
			if 'S,   P [Pa], Ne [10^19m^-3], Te [eV],  Ti [eV]' in line:
				line = file.readline()
				psi2 =[]
				te = []
				ti = []
				ne = []
				p = []
				jbs = []
				hjbt = [] # I don't know what it stands for
				jpar1 =[]
				jpar2 = []
				while True:
					line = file.readline()
					sp = line.split()
					if len(sp)<2:
						break
					psi2.append(self.get_data_from_line(line, 0) ** 2)
					p.append(self.get_data_from_line(line, 1))
					ne.append(self.get_data_from_line(line, 2))
					te.append(self.get_data_from_line(line, 3))
					ti.append(self.get_data_from_line(line, 4))
					jbs.append(self.get_data_from_line(line, 5))
					hjbt.append(self.get_data_from_line(line, 6))
					jpar1.append(self.get_data_from_line(line, 8))
					jpar2.append(self.get_data_from_line(line, 9))
				self.psi2 = np.asanyarray(psi2)
				self.p = np.asanyarray(p)
				self.ne = np.asanyarray(ne)
				self.te = np.asanyarray(te)
				self.ti = np.asanyarray(ti)
				self.jbs = np.asanyarray(jbs)
				self.hjbt = np.asanyarray(hjbt)
				self.jpar1 = np.asanyarray(jpar1)
				self.jpar2 = np.asanyarray(jpar2)
			if 'CIRCUMFRENCE' in line:
				line = file.readline()
				jz = []
				s_jz = []
				circ = []
				while True:
					line = file.readline()
					sp = line.split()
					if len(sp)<2:
						break
					s_jz.append(float(sp[0]))
					try:
						jz.append(float(sp[1]) / 1e6)
					except:
						jz.append(0.0)
					circ.append(float(sp[2]))
					if s_jz[-1] * s_jz[-1] > minpsi:
						if jz[-1] > self.max_j:
							self.max_j = jz[-1]
				self.s_jz = np.asarray(s_jz)
				self.jz = np.asarray(jz)
				self.circ = np.asarray(circ)
			if 'MERCIER' in line:
				self.crashed = False
			if 'INT. INDUCTANCE' in line:
				spl = line.split(':')
				self.li = float(spl[1])
			if '[kA]' in line:
				try:
					self.ip=float(line.split(':')[1].split()[0])/1e3
				except:
					print('Ip not read from the HELENA file')
			if '[T]' in line:
				self.bt=float(line.split(':')[1].split()[0])
			if 'ZEFF' in line:
				self.zeff=float(line.split(':')[1])
			if 'MAJOR RADIUS' in line:
				self.rgeo = float(line.split(':')[1].split()[0])
			if 'RADIUS (a)' in line:
				self.a = float(line.split(':')[1].split()[0])
			if 'PSI ON BOUNDARY' in line:
				self.psi_boundary = float(line.split(':')[1].split()[0])
			if 'MAGNETIC AXIS ' in line:
				self.rmag = float(line.split(':')[1].split()[0])
		file.close()
		self.rmag = self.rmag * self.a + self.rgeo
		self.midplane_r = self.midplane_s * self.a
		self.midplane_R = self.midplane_r + self.rgeo
		self.midplane_bp = np.gradient(self.midplane_psi * self.psi_boundary,self.midplane_r) / self.midplane_R

	def evaluate_q(self,psi):
		# Uses simple linear interpolation to evaluate q at give psi surface
		return(np.interp(psi,self.psi_map,self.q))

	def __init__(self, filename, delta_ne = 0.1, delta_te=0.1):
		self.crashed = False
		self.output_exist = True
		self.delta_ne = delta_ne
		self.delta_te = delta_te
		self.betan = 0.0
		self.betap = 0.0
		self.ip = 0.0
		self.bt = 0.0
		self.zeff = 0
		self.balstart = 1.0
		self.balend = 1.0
		self.max_alpha = 0
		self.min_shear = 1e3
		self.max_j = 0.0
		self.li = 0.0
		self.midplane_s = []
		self.midplane_r = []
		self.midplane_R = []
		self.midplane_psi = []
		self.midplane_bp = []
		self.a=0.0
		self.geo = 0.0
		self.psi_boundary = 0.0
		self.rmag = 0.0

		if not os.path.exists(filename):
			if os.path.exists(filename+'.out'):
				filename=filename+'.out'
				self.onlyout = True
			else:
				print(filename + ' does not exist')
				self.output_exist = False
				self.crashed = True
				return

		self.filename = filename
		self.read_file()
