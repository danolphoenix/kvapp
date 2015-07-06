if __name__=='__main__':    
 

    import sys
    import pycurl
    import StringIO
    import time

    import web as kvapp

   

    sys.stderr.write("Testing %s\n" % pycurl.version)

    #test POST
    b = StringIO.StringIO()
    urlpost = 'http://localhost:8080/keys'
    testkey =  "hello"+str(int(time.time()))
    testdict= '{"'+ str(testkey) +'":"world"} '     
    c = pycurl.Curl()
    c.setopt(c.URL, urlpost)
    c.setopt(c.HTTPHEADER,['Content-Type: application/json'])
    c.setopt(c.CUSTOMREQUEST,"POST")    
    c.setopt(c.POSTFIELDS,testdict)
    c.setopt(c.WRITEFUNCTION, b.write)
    c.perform() 
    print "test POST"
    print c.getinfo(pycurl.HTTP_CODE), b.getvalue()
    c.close()
    b.close()


    #test GET
    b = StringIO.StringIO()
    urlget = 'http://localhost:8080/keys/'+ testkey
    c = pycurl.Curl()
    c.setopt(c.URL, urlget)
    c.setopt(c.HTTPHEADER,['Content-Type: application/json'])
    c.setopt(c.CUSTOMREQUEST,"GET")       
    c.setopt(c.WRITEFUNCTION, b.write)
    c.perform() 
    print "test GET"
    print c.getinfo(pycurl.HTTP_CODE),
    print b.getvalue()
    c.close()
    b.close()

    with kvapp.get_session() as session:
        session.query(kvapp.KVpair).filter(kvapp.KVpair.key == testkey).delete()
        session.commit()

    #test GET,the key doesn't exist
    b = StringIO.StringIO()
    urlget = 'http://localhost:8080/keys/'+ 'notexistkey'
    c = pycurl.Curl()
    c.setopt(c.URL, urlget)
    c.setopt(c.HTTPHEADER,['Content-Type: application/json'])
    c.setopt(c.CUSTOMREQUEST,"GET")       
    c.setopt(c.WRITEFUNCTION, b.write)
    c.perform() 
    print "test GET not exited key"
    print c.getinfo(pycurl.HTTP_CODE)
    c.close()
    b.close()
          


        
            

