host="lbrendanlcluster-node001 lbrendanlcluster-node002 lbrendanlcluster-node003 lbrendanlcluster-node004 lbrendanlcluster-node005 lbrendanlcluster-node006 lbrendanlcluster-node007 lbrendanlcluster-node008 lbrendanlcluster-node009 lbrendanlcluster-node010 lbrendanlcluster-node011 lbrendanlcluster-node012 lbrendanlcluster-node013 lbrendanlcluster-node014 lbrendanlcluster-node015 lbrendanlcluster-node016 lbrendanlcluster-node017 lbrendanlcluster-node018 lbrendanlcluster-node019 lbrendanlcluster-node020"

CMD="sudo service postgresql restart"
parallel -k --jobs +28 "/bin/echo -n '{} -- ' && ssh {} '$CMD'" ::: $host
