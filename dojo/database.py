
import numpy as np
import time
import sqlite3

MAX_SEGMENTS = 100000000

class Database(object):

  def __init__(self, file):
    '''
    '''
    self.__connection = sqlite3.connect(file)
    self.__cursor = self.__connection.cursor()

    print('Largest ID', self.get_largest_id())

    self._merge_table = None
    self._lock_table = None


  def get_segment_info(self):
    '''
    '''
    self.__cursor.execute('SELECT * FROM segmentInfo')

    result = self.__cursor.fetchall()

    output = [None] * (len(result) + 1)

    for r in result:
      output[r[0]] = r[1:]

    return output

  def get_lock_table(self):

    try:
      self.__cursor.execute('SELECT * FROM segmentInfo WHERE confidence=100')

      result = self.__cursor.fetchall()

      output = {'0':True}

      for r in result:
        output[r[0]] = True
      print('Locks:', len(result))
    except:
      output = {'0':True}

    return output

  def get_largest_id(self):

    self.__cursor.execute('SELECT * FROM segmentInfo ORDER BY id DESC')

    result = self.__cursor.fetchone()[0]

    try:
      self.__cursor.execute('SELECT * FROM relabelMap ORDER BY fromId DESC')

      result2 = self.__cursor.fetchone()
      if result2:
        result2 = result2[0]
      else:
        result2 = -1

    except:
      return result

    # output = [None] * (len(result) + 1)

    # for r in result:
    #   output[r[0]] = r[1:]

    if result > result2:
      return result

    if result2 > result:
      return result2

    return result 



  def get_id_tile_index(self,tile_id):
    '''
    '''
    self.__cursor.execute('SELECT * FROM idTileIndex WHERE id='+tile_id)

    result = self.__cursor.fetchall()

    output = []

    for r in result:
      output.append(r[1:])

    # w, z, y, x
    return output

  def lookup_label(self, lut, label):
    if lut[label] != label:
      lut[label] = self.lookup_label(lut, lut[label])
    return lut[label]

  def get_merge_table(self):

    lut = np.arange(MAX_SEGMENTS, dtype=np.uint64)

    try:
      self.__cursor.execute('SELECT * FROM relabelMap')
      result_list = self.__cursor.fetchall()

      print('Creating lookup table buffer..')

      # All results stored as index:value in lookup table
      lut[[r[0] for r in result_list]] = [r[1] for r in result_list]

      print('Start hardening the lookup table..')
      max_lut = len(result_list)
      steps = np.arange(0,max(max_lut,1),max(1,max_lut//10))
      percents = 100*(np.arange(len(steps)) + 1)//len(steps)
      step_index = 0
      st = time.time()
      for i, r in enumerate(result_list):
        if i >= steps[step_index]:
          print("{}% DONE, {} seconds".format(percents[step_index], int(time.time() - st)))
          step_index += 1
        lut[r[0]] = self.lookup_label(lut, r[0])
      print('Merges:', len(result_list))

    except:
      return lut

    return lut

  def insert_lock(self, id):

    try:
      self.__connection.execute('SELECT * FROM segmentInfo WHERE id='+str(id))
      result = self.__cursor.fetchone()
      if result:
        self.__connection.execute('UPDATE segmentInfo SET confidence=100 WHERE id='+str(id))
      else:
        self.__connection.execute('INSERT INTO segmentInfo VALUES (?,?,?,?,?,?)', (id, 'newone', 0, 100, 'None', 'None'))
    
    except:
      print('ERROR WHEN LOCKING', id)

  def remove_lock(self, id):

    try:
      self.__connection.execute('SELECT * FROM segmentInfo WHERE id='+str(id))
      result = self.__cursor.fetchone()
      if result:
        self.__connection.execute('UPDATE segmentInfo SET confidence=0 WHERE id='+str(id))
      else:
        self.__connection.execute('INSERT INTO segmentInfo VALUES (?,?,?,?,?,?)', (id, 'newone', 0, 0, 'None', 'None'))
    
    except:
      print('ERROR WHEN UNLOCKING', id)

  def insert_merge(self, id1, id2):

    try:
      self.__connection.execute('INSERT INTO relabelMap VALUES (?,?)', (id1, id2))
    

    except:
      print('ERROR WHEN MERGING', id1, id2)

  def store(self):

    self.__connection.commit()


