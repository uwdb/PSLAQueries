host="mycluster-training-node001 mycluster-training-node002 mycluster-training-node003 mycluster-training-node004 mycluster-training-node005 mycluster-training-node006 mycluster-training-node007 mycluster-training-node008"

CMD="sudo service postgresql restart"
parallel -k --jobs +28 "/bin/echo -n '{} -- ' && starcluster sshnode mycluster-training {} '$CMD'" ::: $host
