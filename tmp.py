
import fnmatch

files_in_folder = ['checkpoint', 'graph.pbtxtgraph.pbtxt', 'graph.pbtxt', 'modeldsdsd.data-00000-of-00001']

files_required = [ \
	'checkpoint', \
	'events.out.tfevents.*', \
	'graph.pbtxt', \
	'model*.meta', \
	'model*.index',\
	'model*.data-00000-of-00001' ]

flags = []
for file_required in files_required:
	match_fname = [fnmatch.fnmatch(fn, file_required) for fn in files_in_folder]
	flags.append(any(match_fname))

