
def test(net):
    # on first server start the listener
    net.get("h1").sendCmd("python server.py &")
    
    # Start the client
    net.get("c1").sendCmd("python client.py -p http 10.10.101.2:8080")

    print("Running base test with only one server")

    time.sleep(4)
    
    net.get("c1").monitor()
    print("Done")
    return