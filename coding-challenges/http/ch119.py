import ringzer

sdmap = {
'''
 xxx 
x   x
x   x
x   x
 xxx ''' : '0',

'''
 xx  
x x  
  x  
  x  
xxxxx''' : '1',

'''
 xxx 
x   x 
  xx 
 x   
xxxxx''' : '2',

'''
 x   x
x    x
 xxxxx
     x
    x''' : '4',

'''
xxxxx
x    
 xxxx
    x
xxxxx''' : '5',

'''
 xxx 
x   x
  xx 
x   x
 xxx ''' : '3'}

def chall_func(message):
    rows = filter(lambda s: s, message.replace("&nbsp;", " ").split("<br />"))
    return ''.join([sdmap[('\n'+'\n'.join(rows[i:i+5]))] for i in range(0, 50, 5)])

ringzer.Challenge(119, chall_func)

