

sudo apt-get update
sudo apt-get install mininet
sudo apt-get install openvswitch-switch
sudo apt-get install openvswitch-testcontroller

# starts ovs service
sudo service openvswitch-switch start

sudo pip3 install mininet

# cleans env
sudo mn -c