host="mycluster-node001 mycluster-node002 mycluster-node003 mycluster-node004 mycluster-node005 mycluster-node006 mycluster-node007 mycluster-node008"

CMD="free && sync && echo \"echo 1 > /proc/sys/vm/drop_caches\" | sudo sh"
parallel -k --jobs +28 "/bin/echo -n '{} -- ' && ssh {} '$CMD'" ::: $host