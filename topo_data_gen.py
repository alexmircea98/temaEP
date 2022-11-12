import hashlib
import sys

if (len(sys.argv) != 2):
    print("no argument found, ai uitat sa bagi username-ul boss")
    exit()
hash = hashlib.sha256(sys.argv[1].encode('utf-8')).hexdigest()
print(hash)

values =[]
for i in range(32):
    values.append(str(int(hash[i:i+2], 16)%100))

print("Server-Switch links:  bw=" + values[0] + ", delay=\'" + values[1] + "ms\'")
print("Switch-Routers links: bw=" + values[2] + ", delay=\'" + values[3] + "ms\'")
print("Router-Switch link:   bw=" + values[4] + ", delay=\'" + values[5] + "ms\'")
print("Switch-Client link:   bw=" + values[6] + ", delay=\'" + values[7] + "ms\'")

# OPTIONAL
print("\n") 
print("Servers cpu values:") 
for i in range(1,6):
    print("h" + str(i) + ": " + str(float(int(values[i+7])%20)/10))