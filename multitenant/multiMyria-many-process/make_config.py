#!/usr/bin/python
import os

#for master
master_name = "mycluster-large-master"
master_ports = ["8001", "8002", "8003", "8004", "8005", "8006", "8007", "8008", "8009" ,"8010"] 
master_rest_ports = ["9001", "9002", "9003", "9004", "9005", "9006", "9007", "9008", "9009" ,"9010"] 

config_tenant_mapper = []
num_tenants = 10
num_workers = 12

#for each tenant, have the preamble prepared
for t in range(0,num_tenants):
    current_preamble = ""
    with open("./preamble.txt", "r") as preamble_file:
        raw_preamble=preamble_file.readlines()
        for line in raw_preamble:
            line=line.replace("{MASTER}", master_name + ":" +  master_ports[t])
            line=line.replace("{REST_PORT}", master_rest_ports[t])
            line=line.replace("{PATH}", "/mnt/myria_ec2_deployment_tenant" + str(t))
            line=line.replace("{NAME}", "MyriaEC2_tenant" + str(t))
            current_preamble+=line
        config_tenant_mapper.insert(t, current_preamble) 
    preamble_file.close()

#2shared configure
shared_nodes = ["mycluster-large-node001","mycluster-large-node002"]
marker = len(shared_nodes) + 1

for t in range(0,num_tenants):
    current_config = open(os.path.expanduser("configs/2_shared/t" + str(t) + "ec2.cfg"), 'w+')
    current_config.write(config_tenant_mapper[t])

    for w in range(1,num_workers+1):
        worker_port = "8" + str(t+1) + ("0" + str(w) if w < 10 else str(w))

        if w <= len(shared_nodes):
            w_num = str(w)
            n_name = shared_nodes[w-1]
            n_port = worker_port
            d_name =  "myria"
        else:
            w_num = str(w)
            n_name = "mycluster-large-node0" + ("0" + str(marker) if marker < 10 else str(marker))
            n_port = worker_port
            d_name =  "myria"
            marker = marker + 1

        current_config.write(w_num + " = " + n_name + ":"+  n_port + "::" + d_name + "\n" )
        
    current_config.close()

#4shared configure
shared_nodes = ["mycluster-large-node001","mycluster-large-node002", "mycluster-large-node003", "mycluster-large-node004"]
marker = len(shared_nodes) + 1

for t in range(0,num_tenants):
    current_config = open(os.path.expanduser("configs/4_shared/t" + str(t) + "ec2.cfg"), 'w+')
    current_config.write(config_tenant_mapper[t])

    for w in range(1,num_workers+1):
        worker_port = "8" + str(t+1) + ("0" + str(w) if w < 10 else str(w))

        if w <= len(shared_nodes):
            w_num = str(w)
            n_name = shared_nodes[w-1]
            n_port = worker_port
            d_name =  "myria"
        else:
            w_num = str(w)
            n_name = "mycluster-large-node0" + ("0" + str(marker) if marker < 10 else str(marker))
            n_port = worker_port
            d_name =  "myria"
            marker = marker + 1

        current_config.write(w_num + " = " + n_name + ":"+  n_port + "::" + d_name + "\n" )
        
    current_config.close()

#6shared configure
shared_nodes = ["mycluster-large-node001","mycluster-large-node002", "mycluster-large-node003", "mycluster-large-node004", "mycluster-large-node005", "mycluster-large-node006"]
marker = len(shared_nodes) + 1

for t in range(0,num_tenants):
    current_config = open(os.path.expanduser("configs/6_shared/t" + str(t) + "ec2.cfg"), 'w+')
    current_config.write(config_tenant_mapper[t])

    for w in range(1,num_workers+1):
        worker_port = "8" + str(t+1) + ("0" + str(w) if w < 10 else str(w))

        if w <= len(shared_nodes):
            w_num = str(w)
            n_name = shared_nodes[w-1]
            n_port = worker_port
            d_name =  "myria"
        else:
            w_num = str(w)
            n_name = "mycluster-large-node0" + ("0" + str(marker) if marker < 10 else str(marker))
            n_port = worker_port
            d_name =  "myria"
            marker = marker + 1

        current_config.write(w_num + " = " + n_name + ":"+  n_port + "::" + d_name + "\n" )
        
    current_config.close()

#8shared configure
shared_nodes = ["mycluster-large-node001","mycluster-large-node002", "mycluster-large-node003", "mycluster-large-node004", "mycluster-large-node005", "mycluster-large-node006", "mycluster-large-node007",  "mycluster-large-node008"]
marker = len(shared_nodes) + 1

for t in range(0,num_tenants):
    current_config = open(os.path.expanduser("configs/8_shared/t" + str(t) + "ec2.cfg"), 'w+')
    current_config.write(config_tenant_mapper[t])

    for w in range(1,num_workers+1):
        worker_port = "8" + str(t+1) + ("0" + str(w) if w < 10 else str(w))

        if w <= len(shared_nodes):
            w_num = str(w)
            n_name = shared_nodes[w-1]
            n_port = worker_port
            d_name =  "myria"
        else:
            w_num = str(w)
            n_name = "mycluster-large-node0" + ("0" + str(marker) if marker < 10 else str(marker))
            n_port = worker_port
            d_name =  "myria"
            marker = marker + 1

        current_config.write(w_num + " = " + n_name + ":"+  n_port + "::" + d_name + "\n" )
        
    current_config.close()