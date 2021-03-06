machines = []

config_password = 'p47f8iqnct'
total_machines = 12
starting_machine_count = 7
key_name = 'jortiz16Key.rsa '

#read machines list
with open('machines_to_add.txt') as f:
	machines = f.read().splitlines() 

#created files
file_change_passwords = open('./change_passwords.sh', 'w+')
file_passwordless_ssh = open('./passwordless_ssh.sh', 'w+')
machines_to_add_config = open('./config_to_add.txt', 'w+')

for m in machines:
	file_change_passwords.write('ssh ' + m + ' "sudo -u postgres psql -c \\\"ALTER USER uwdb WITH PASSWORD \'' + config_password  + '\'\\\""' + '\n')
	file_passwordless_ssh.write('cat ~/.ssh/id_rsa.pub | ssh -i ' + key_name + ' root@' + m + ' \'cat >> .ssh/authorized_keys\'' + '\n')
	machines_to_add_config.write(str(starting_machine_count) + " = " + m + ":9001::myria" + '\n')
	starting_machine_count = starting_machine_count + 1

#max heap sizes
machines_to_add_config.write('\n')
machines_to_add_config.write('[maxheapsizes]' + '\n')
current_machine_count = 1

for m in range(total_machines):
	machines_to_add_config.write(str(current_machine_count) + ' = ' + '-Xmx?g' + '\n')
	current_machine_count = current_machine_count + 1

file_change_passwords.close()
file_passwordless_ssh.close()
machines_to_add_config.close()