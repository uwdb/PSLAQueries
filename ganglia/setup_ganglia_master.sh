# View README.txt
# Configure gmond and gmetad on master
sudo apt-get install ganglia-monitor rrdtool gmetad
tar -xvf ganglia-web-3.7.0.tar
make install -C ganglia-web-3.7.0/
sudo cp /etc/ganglia-webfrontend/apache.conf /etc/apache2/sites-enabled/ganglia.conf
cp ./masterGangliaFiles/gmond.conf /etc/ganglia/
cp ./masterGangliaFiles/gmetad.conf /etc/ganglia/
cp ./masterGangliaFiles/apache2.conf /etc/apache2/
cp ./masterGangliaFiles/ports.conf /etc/apache2/
cp ./masterGangliaFiles/000-default /etc/apache2/sites-enabled/

sudo service gmetad start
sudo service ganglia-monitor start
chown -R nobody /var/lib/ganglia/rrds

# Restart all services
sudo service ganglia-monitor restart && sudo service gmetad restart && sudo service apache2 restart