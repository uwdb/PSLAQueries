import os

output = open(os.path.expanduser("runtimes_12compute.txt"), 'w');
with open("./runtimes-sample100_12.txt") as f:
    lines = f.readlines()
    for line in lines:
        split = line.split(",")
        time = split[2]

        output.write(time)


output.flush()
output.close()
