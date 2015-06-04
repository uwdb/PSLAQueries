host="mycluster-training-node001 mycluster-training-node002 mycluster-training-node003 mycluster-training-node004 mycluster-training-node005 mycluster-training-node006 mycluster-training-node007 mycluster-training-node008"

CMD="free && sync && echo \"echo 1 > /proc/sys/vm/drop_caches\" | sudo sh"
parallel -k --jobs +28 "/bin/echo -n '{} -- ' && starcluster sshnode mycluster-training {} '$CMD'" ::: $host