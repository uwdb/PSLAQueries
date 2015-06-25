starcluster sshmaster $1 'mkdir /root/PSLAQueries'

starcluster put $1 --node $1-master queries /root/PSLAQueries
starcluster put $1 --node $1-master data /root/PSLAQueries
starcluster put $1 --node $1-master raco /root/PSLAQueries
starcluster put $1 --node $1-master schema.py /root/PSLAQueries
starcluster put $1 --node $1-master buildingQueries.py /root/PSLAQueries
starcluster put $1 --node $1-master ganglia /root/PSLAQueries

echo "finished moving files"

echo "installing myria-python"
starcluster sshmaster $1 "pip install myria-python"

echo "installing aws"
starcluster sshmaster $1 "sudo pip install awscli"

echo "installing raco"
starcluster sshmaster $1 "/root/PSLAQueries/raco/python setup.py install"

echo "installing gnu parallel"
starcluster sshmaster $1 "(wget -O - pi.dk/3 || curl pi.dk/3/ || fetch -o - http://pi.dk/3) | bash"