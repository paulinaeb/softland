# import serial
# import time
# f = source
# d = destiny
# c = command 
# p = list of params or variable with one param

class Resp:
    def __init__(self):
        self.f = self.d = self.c = None
        self.p = []
    def set_header(self, f, d, c):
        self.f = f 
        self.d = d 
        self.c = c
        self.p = []
    def set_values(self, f, d, c, p):
        self.set_header(f, d, c)
        self.p = p
    def add_p(self, param):
        self.p.append(param) 
        

def serialize(obj_resp):
    # num of params passed
    n_param = len(obj_resp.p) 
    # header of message
    msg = obj_resp.f + obj_resp.d + obj_resp.c 
    # size of params str with delimiter (/)
    size = n_param
    if (size > 0):
        # adds the size of each param
        for obj in obj_resp.p:
            size += len(obj)
        # define the number of spaces to be filled with '0'
        num_fill = 14 - size 
        # number of spaces that every param will have added to (if>0)
        n_each = num_fill / n_param 
        if num_fill >= 0: 
            if n_param >= 1: 
                for obj in obj_resp.p:
                    msg += obj + '/'
                    for i in range(int(n_each)):
                        msg += '0' 
            # if num to add is odd or there are less spaces to be filled than params 
            if ((n_each != int(n_each)) or (num_fill < n_param)):
                ex = 18 - len(msg)
                for i in range(ex):
                    msg += '0'
        else:
            print('El tamaño de los parámetros ingresados sobrepasa el limite permitido. Verifique e intente nuevamente.')
    # else:
    #     # no params needed 
    return msg

# obj_resp = Resp()
# obj_resp.set_values('0', 'F', 'II', ['1'])
# ser_msg = serialize(obj_resp)
# print(ser_msg)

# def time_as_int():
#     return int(round(time.time() * 100)) 

# ser_port = serial.Serial(port='COM3', baudrate=115200, timeout=0.01)  
# sent = time_as_int()
# ser_port.write(('ping,').encode())
# print('ping sent')
# while True:
#     read_val = ser_port.readline()
#     msg_read = read_val.decode()
#     if msg_read:
#         rec = time_as_int()
#         t = (rec - sent) 
#         t = '{:02d}.{:02d}'.format( (t // 100) % 60, t % 100)
#         print('diff time', t)
#         print('read ',msg_read)
#         break
        
# obj_req = Resp()

# msg = '01GP6.70/0ana/01/0';

def deserialize(msg, obj_req): 
    obj_req.set_header(msg[0], msg[1], msg[2] + msg[3])
    if len(msg) > 4:
        str_p = msg[4:]
        limit = str_p.count('/')
        if limit > 0:
            #  insert params into array
            index = 0
            aux = 0
            for i in range(limit):
                if i == 0: 
                    index = str_p.find('/') 
                    obj_req.add_p(str_p[:index])
                else:
                    index = str_p.find('/', index + 1)
                    obj_req.add_p(str_p[aux + 1:index])
                aux = index
                flag = 0 
                for char in range (len(obj_req.p[i])):
                    # checks if num or str for every char 
                    if not (((obj_req.p[i][char] >= '0') and (obj_req.p[i][char] <= '9')) or (obj_req.p[i][char] =='.')):
                        flag += 1
                # if the param is a str - remove 0
                if flag > 0:
                    obj_req.p[i] = obj_req.p[i].replace('0',''); 
    return 

# deserialize(msg)
