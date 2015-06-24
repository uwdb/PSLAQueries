host="mycluster-node001 mycluster-node002 mycluster-node003 mycluster-node004 mycluster-node005 mycluster-node006 mycluster-node007 mycluster-node008 mycluster-node009 mycluster-node010 mycluster-node011 mycluster-node012 mycluster-node013 mycluster-node014 mycluster-node015 mycluster-node016 mycluster-node017 mycluster-node018 mycluster-node019 mycluster-node020 mycluster-node021 mycluster-node022"

CMD="sudo service postgresql restart"
parallel -k --jobs +28 "/bin/echo -n '{} -- ' && starcluster sshnode mycluster {} '$CMD'" ::: $host
