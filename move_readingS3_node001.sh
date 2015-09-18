starcluster sshmaster $1 'mkdir /root/PSLAQueries'

starcluster put $1 --node $1-node001 readingS3 /root/PSLAQueries

starcluster sshnode $1 $1-node001 "sudo apt-get install openjdk-7-jdk"
starcluster sshnode $1 $1-node001 "export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64"
starcluster sshnode $1 $1-node001 "wget http://www.motorlogy.com/apache/maven/maven-3/3.3.3/binaries/apache-maven-3.3.3-bin.tar.gz;tar -zxvf apache-maven-3.3.3-bin.tar.gz;export PATH=/root/apache-maven-3.3.3/bin:$PATH"
