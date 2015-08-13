machines = []

config_password = 'p47f8iqnct'
starting_machine_count = 8

#read machines list
with open('machines_to_add.txt') as f:
	machines = f.read().splitlines() 

#created files
file_change_passwords = open('./change_passwords.sh', 'w+')
file_passwordless_ssh = open('./passwordless_ssh.sh', 'w+')
machines_to_add_config = open('./config_to_add.txt', 'w+')

for m in machines:
	file_change_passwords.write('ssh ' + m + ' echo \"ALTER USER uwdb WITH PASSWORD \\\'' + config_password + '\\\'\" | sudo -u postgres psql myria' + '\n')
	file_passwordless_ssh.write('cat ~/.ssh/id_rsa.pub | ssh -i jortiz16Key.rsa root@' + m + ' \'cat >> .ssh/authorized_keys\'' + '\n')
	machines_to_add_config.write(str(starting_machine_count) + " = " + m + ":9001:myria" + '\n')
	starting_machine_count = starting_machine_count + 1
file_change_passwords.close()
file_passwordless_ssh.close()
machines_to_add_config.close()