machines = []

config_password = 'p47f8iqnct'
starting_machine_count = 8

#read machines list
with open('machines_to_add.txt') as f:
	machines = f.read().splitlines() 

#write changing passwords script
file_change_passwords = open('./change_passwords.sh', 'w+')
for m in machines:
	#ssh and run command
	# this worked echo "ALTER USER uwdb WITH PASSWORD 'mpbl6or79s'" | sudo -u postgres psql myria
	file_change_passwords.write('ssh ' + m + ' echo \"ALTER USER uwdb WITH PASSWORD \\\'' + config_password + '\\\'\" | sudo -u postgres psql myria' + '\n')
file_change_passwords.close()

file_passwordless_ssh = open('./passwordless_ssh.sh', 'w+')
for m in machines:
	#passwordless ssh
	file_passwordless_ssh.write('cat ~/.ssh/id_rsa.pub | ssh -i jortiz16Key.rsa root@' + m + ' \'cat >> .ssh/authorized_keys\'' + '\n')
file_passwordless_ssh.close()

machines_to_add_config = open('./config_to_add.txt', 'w+')

for m in machines:
	#ssh and run postgres command
	machines_to_add_config.write(str(starting_machine_count) + " = " + m + ":9001:myria" + '\n')
	starting_machine_count = starting_machine_count + 1
machines_to_add_config.close()
