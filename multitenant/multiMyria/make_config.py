#!/usr/bin/python
import os

T1_master = "ec2-23-22-177-26.compute-1.amazonaws.com:8001"
T2_master = "ec2-23-22-177-26.compute-1.amazonaws.com:8002"
T1_port = "8753"
T2_port = "8754"

workers = ["1 = ec2-50-17-109-10.compute-1.amazonaws.com:9001::myria",
"2 = ec2-54-226-90-27.compute-1.amazonaws.com:9001::myria",
"3 = ec2-54-91-171-130.compute-1.amazonaws.com:9001::myria",
"4 = ec2-54-144-66-9.compute-1.amazonaws.com:9001::myria",
"5 = ec2-54-159-50-183.compute-1.amazonaws.com:9001::myria",
"6 = ec2-54-226-95-27.compute-1.amazonaws.com:9001::myria",
"7 = ec2-54-160-155-124.compute-1.amazonaws.com:9001::myria",
"8 = ec2-50-19-39-233.compute-1.amazonaws.com:9001::myria",
"9 = ec2-54-87-28-154.compute-1.amazonaws.com:9001::myria",
"10 = ec2-54-160-190-205.compute-1.amazonaws.com:9001::myria",
"11 = ec2-54-160-183-207.compute-1.amazonaws.com:9001::myria",
"12 = ec2-54-144-88-110.compute-1.amazonaws.com:9001::myria",
"13 = ec2-54-226-118-196.compute-1.amazonaws.com:9001::myria",
"14 = ec2-54-145-13-151.compute-1.amazonaws.com:9001::myria",
"15 = ec2-54-226-186-7.compute-1.amazonaws.com:9001::myria",
"16 = ec2-107-21-172-238.compute-1.amazonaws.com:9001::myria",
"17 = ec2-54-90-224-9.compute-1.amazonaws.com:9001::myria",
"18 = ec2-54-159-16-84.compute-1.amazonaws.com:9001::myria",
"19 = ec2-107-20-117-216.compute-1.amazonaws.com:9001::myria",
"20 = ec2-54-91-105-124.compute-1.amazonaws.com:9001::myria",
"21 = ec2-54-146-218-167.compute-1.amazonaws.com:9001::myria",
"22 = ec2-54-221-167-105.compute-1.amazonaws.com:9001::myria"]

worker_map = []
for (i, worker) in enumerate(workers):
    worker_map.insert(i, worker)


with open("./preamble.txt", "r") as preamble_file:
    raw_preamble=preamble_file.readlines()
    T1_preamble=""
    T2_preamble=""

    for line in raw_preamble:
        line=line.replace("{MASTER}", T1_master)
        line=line.replace("{PORT}", T1_port)
        line=line.replace("{PATH}", "/mnt/myria_ec2_deployment_tenantA")
        line=line.replace("{NAME}", "MyriaEC2_tenantA")
        T1_preamble+=line

    for line in raw_preamble:
        line=line.replace("{MASTER}", T2_master)
        line=line.replace("{PORT}", T2_port)
        line=line.replace("{PATH}", "/mnt/myria_ec2_deployment_tenantB")
        line=line.replace("{NAME}", "MyriaEC2_tenantB")
        T2_preamble+=line

    # Always going to be the same
    T1_workers = [1,2,3,4,5,6,7,8,9,10,11,12]

    #T1: Data Nodes 1 through 12
    #T2: Data Nodes 11 through 22
    #2 Shared
    T1_2 = open(os.path.expanduser("configs/T1_2.ec2.cfg"), 'w');
    T2_2 = open(os.path.expanduser("configs/T2_2.ec2.cfg"), 'w');

    T1_2.write(T1_preamble)
    T2_2.write(T2_preamble)
    T2_2_workers = [11,12,13,14,15,16,17,18,19,20,21,22]
    for worker in T1_workers:
        T1_2.write(worker_map[worker-1]+"\n")
    for worker in T2_2_workers:
        T2_2.write(worker_map[worker-1]+"\n")

    #T1: Data Nodes 1 through 12
    #T2: Data Nodes 9 through 20
    #4 Shared
    T1_4 = open(os.path.expanduser("configs/T1_4.ec2.cfg"), 'w');
    T2_4 = open(os.path.expanduser("configs/T2_4.ec2.cfg"), 'w');

    T1_4.write(T1_preamble)
    T2_4.write(T2_preamble)
    T2_4_workers = [9,10,11,12,13,14,15,16,17,18,19,20]
    for worker in T1_workers:
        T1_4.write(worker_map[worker-1]+"\n")
    for worker in T2_4_workers:
        T2_4.write(worker_map[worker-1]+"\n")

    #T1: Data Nodes 1 through 12
    #T2: Data Nodes 7 through 18
    #6 Shared
    T1_6 = open(os.path.expanduser("configs/T1_6.ec2.cfg"), 'w');
    T2_6 = open(os.path.expanduser("configs/T2_6.ec2.cfg"), 'w');

    T1_6.write(T1_preamble)
    T2_6.write(T2_preamble)
    T2_6_workers = [7,8,9,10,11,12,13,14,15,16,17,18]
    for worker in T1_workers:
        T1_6.write(worker_map[worker-1]+"\n")
    for worker in T2_6_workers:
        T2_6.write(worker_map[worker-1]+"\n")

    #T1: Data Nodes 1 through 12
    #T2: Data Nodes 5 through 16
    #8 Shared
    T1_8 = open(os.path.expanduser("configs/T1_8.ec2.cfg"), 'w');
    T2_8 = open(os.path.expanduser("configs/T2_8.ec2.cfg"), 'w');

    T1_8.write(T1_preamble)
    T2_8.write(T2_preamble)
    T2_8_workers = [5,6,7,8,9,10,11,12,13,14,15,16]
    for worker in T1_workers:
        T1_8.write(worker_map[worker-1]+"\n")
    for worker in T2_8_workers:
        T2_8.write(worker_map[worker-1]+"\n")

    #T1: Data Nodes 1 through 12
    #T2: Data Nodes 3 through 14
    #10 Shared
    T1_10 = open(os.path.expanduser("configs/T1_10.ec2.cfg"), 'w');
    T2_10 = open(os.path.expanduser("configs/T2_10.ec2.cfg"), 'w');

    T1_10.write(T1_preamble)
    T2_10.write(T2_preamble)
    T2_10_workers = [3,4,5,6,7,8,9,10,11,12,13,14]
    for worker in T1_workers:
        T1_10.write(worker_map[worker-1]+"\n")
    for worker in T2_10_workers:
        T2_10.write(worker_map[worker-1]+"\n")

    #T1: Data Nodes 1 through 12
    #T2: Data Nodes 1 through 12
    #12 Shared
    T1_12 = open(os.path.expanduser("configs/T1_12.ec2.cfg"), 'w');
    T2_12 = open(os.path.expanduser("configs/T2_12.ec2.cfg"), 'w');

    T1_12.write(T1_preamble)
    T2_12.write(T2_preamble)
    T2_12_workers = [1,2,3,4,5,6,7,8,9,10,11,12]
    for worker in T1_workers:
        T1_12.write(worker_map[worker-1]+"\n")
    for worker in T2_12_workers:
        T2_12.write(worker_map[worker-1]+"\n")

    # Flush and close all files
    T1_2.flush()
    T1_2.close()
    T2_2.flush()
    T2_2.close()
    T1_4.flush()
    T1_4.close()
    T2_4.flush()
    T2_4.close()
    T1_6.flush()
    T1_6.close()
    T2_6.flush()
    T2_6.close()
    T1_8.flush()
    T1_8.close()
    T2_8.flush()
    T2_8.close()
    T1_10.flush()
    T1_10.close()
    T2_10.flush()
    T2_10.close()
    T1_12.flush()
    T1_12.close()
    T2_12.flush()
    T2_12.close()
