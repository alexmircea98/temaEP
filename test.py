import time

def test(net):
    # on first server start the listener
    net.get("h1").sendCmd("python3 -m http.server 9000 &")
    
    # Start the client
    net.get("c1").sendCmd("python3 client.py -p http 10.10.101.2:9000 &")

    print("Running base test with only one server")

    time.sleep(4)
    
    net.get("c1").monitor()
    print("Done")
    return