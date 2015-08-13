cat ~/.ssh/id_rsa.pub | ssh -i jortiz16Key.rsa root@machine-example-1@amazon.com'cat >> .ssh/authorized_keys'
cat ~/.ssh/id_rsa.pub | ssh -i jortiz16Key.rsa root@machine-example-2@amazon.com'cat >> .ssh/authorized_keys'
