starcluster sshmaster $1 'mkdir /root/PSLAQueries'

starcluster put $1 --node $1-master read_chunks /root/PSLAQueries