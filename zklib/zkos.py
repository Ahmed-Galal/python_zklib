def zkos(self):
    data_seq=[ self.data_recv.encode("hex")[4:6], self.data_recv.encode("hex")[6:8] ]
    #print data_seq
    self.data_seq1 = hex( int( data_seq[0], 16 ) + int( '66', 16 ) ).lstrip("0x")
    self.data_seq2 = hex( abs( int( data_seq[1], 16 ) - int( 'a', 16 ) ) ).lstrip("0x")
    
    if len(self.data_seq1) >= 3:
        self.data_seq2 = hex( int( self.data_seq2, 16 ) + int( self.data_seq1[:1], 16) ).lstrip("0x")
        self.data_seq1 = self.data_seq1[-2:]
        
    if len(self.data_seq2) >= 3:
        self.data_seq1 = hex( int( self.data_seq1, 16 ) + int( self.data_seq2[:1], 16) ).lstrip("0x")
        self.data_seq2 = self.data_seq2[-2:]
        

    if len(self.data_seq1) <= 1:
        self.data_seq1 = "0"+self.data_seq1
        
    if len(self.data_seq2) <= 1:
        self.data_seq2 = "0"+self.data_seq2
    
    
    counter = hex( self.counter ).lstrip("0x")
    if len(counter):
        counter = "0" + counter
    #print self.data_seq1+" "+self.data_seq2+": +66, -A"
    data = "0b00"+self.data_seq1+self.data_seq2+self.id_com+counter+"007e4f5300"
    self.zkclient.sendto(data.decode("hex"), self.address)
    #print data
    self.data_recv, addr = self.zkclient.recvfrom(1024)
    if len(self.data_recv) > 0:
        self.id_com = self.data_recv.encode("hex")[8:12]
        self.counter = self.counter+1
    #print self.data_recv.encode("hex")
    return self.data_recv[8:]
