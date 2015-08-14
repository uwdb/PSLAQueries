host="mycluster-node001 mycluster-node002 mycluster-node003 mycluster-node004 mycluster-node005 mycluster-node006 mycluster-node007 mycluster-node008 mycluster-node009 mycluster-node010 mycluster-node011  mycluster-node012"

CMD="sudo service postgresql restart"
parallel -k --jobs +28 "/bin/echo -n '{} -- ' && ssh {} '$CMD'" ::: $host
