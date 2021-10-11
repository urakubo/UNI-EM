##
##
##
import sys, os
import subprocess as s
import miscellaneous.Miscellaneous as m

from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
# exec_template = ['python', os.path.join(main_dir, 'plugins', 'Template', 'run_example.py')]

class LiftedMulticut():

	def _Run(self, parent, params, comm_title):
		##
		##
		print('')
		print(comm_title, 'was finished.')
		print('')

		return True

	def __init__(self, u_info):
		##
		self.u_info = u_info
		self.paramfile = os.path.join(u_info.parameters_path, "LiftedMulticut.pickle")

		self.title = 'Lifted Multicut'

		self.tips = [
		                'Membrane probability',
		                'Binarization threshold for boundary',
		                'Sigma in Gaussian smoothing',
		                'Minimal distance between seeds',
		                'Intermediate output folder',
		                'Output segmentation folder'
		                ]

		self.args = [
		                ['Membrane probability', 'SelectImageFolder', 'OpenImageFolder'],
		                ['Binarization threshold', 'SpinBox', [1, 128, 255]],
		                ['Sigma in Gaussian smoothing', 'SpinBox', [0, 2, 255]],
		                ['Minimal distance', 'SpinBox', [0, 10, 255]],
		                ['Intermediate output folder (2D Watershed, Empty)',  'SelectEmptyModelFolder', 'OpenEmptyModelFolder'],
		                ['Output segmentation folder (Empty)',  'SelectEmptyModelFolder', 'OpenEmptyModelFolder']
		    ]


