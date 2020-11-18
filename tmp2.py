
import fnmatch

files_in_folder = ['checkpoint', 'graph.pbtxtgraph.pbtxt', 'graph.pbtxt', 'modeldsdsd.data-00000-of-00001', 'model222.data-00000-of-00001','model222.meta', 'model222.index', 'model222.index']

required_files = [ \
    'model*.meta', \
    'model*.index',\
    'model*.data-00000-of-00001' ]
#
cropped = []
for required_file in required_files:
	#
    tmp = fnmatch.filter(files_in_folder, required_file)
	#
    print('tmp : ', tmp)
    a, b = map(len, required_file.split('*'))
    print('a,b  : ', a, b)
    cropped.append( {t[a:-b] for t in tmp} ) 
	#

intersection = cropped[0] & cropped[1] & cropped[2] 
print(intersection)
print(len(intersection) > 0)
