import operator
def convert_to_binary(inp):
	inp = int(inp)
	ret = str('')

	while inp:
		temp = inp % 2
		ret += str(temp)
		inp /= 2

	siz = len(ret)
	
	for i in range(0,8-siz):
		ret += '0'
	ret = (ret[::-1])

	return str(ret)

def to_dec(inp):
	inp = str(inp)
	ret = int(0)

	for i in range(0,8):
		ret += (1 << (7-i)) * int(inp[i])

	return str(ret)

def next(inp):
	numbers = inp.split('.')
	for i in range(3, 0, -1):
		if int(numbers[i]) < 255:
			numbers[i] = str(int(numbers[i]) + int(1))
			break
		else:
			numbers[i] = 0

	# what if no IP possible?

	ret = ''

	for i in numbers:
		ret += str(i)
		ret += '.'

	return ret[:-1]

def first(inp, right):
	numbers = inp.split('.')
	in_binary = ''
	ret = ''
	for i in range(0, 4):
		in_binary += convert_to_binary(numbers[i])

	in_binary2 = ''
	for i in range(0, 32):
		if (i < int(right)):
			in_binary2 += in_binary[i]
		else:
			in_binary2 += '0'

	for i in range(0,32,8):
		send = ''
		for j in range(i,i+8):
			send += in_binary2[j]
		ret += to_dec(send) + '.'
	return ret[:-1]

def list_all_ip(subnet):
	left = subnet.split('/')[0]
	right = subnet.split('/')[1]

	num_possible = 2 ** (int(32) - int(right))

	ret = []

	first_ip = left
	ret.append(first_ip)
	prev = first_ip
	count = 1

	while count < num_possible:
		ip = next(prev)
		ret.append(ip)
		prev = ip
		count += 1

	return ret

def get_ip_list(cidr, num):
	left = cidr.split('/')[0]
	ret = []
	ret.append(left)

	for i in range(int(num) - 1):
		temp = next(left)
		ret.append(temp)
		left = temp

	return ret

def allot(cidr, alloted_yet, to_be_alloted):
	two_powers = []
	right = int(-1)
	for i in range(32):
		if (1 << int(i)) >= to_be_alloted:
			right = int(32) - i
			break

	ip = cidr.split('/')[0]
	for i in range(alloted_yet):
		ip = next(ip)

	ret = ip + '/' + str(right)
	return (ret, 2 ** (int(32) - right))

def allot_cidr(cidr, data):
	ret = []
	alloted_yet = int(0)
	total_alloted = int(0)

	print 'before = ' + cidr
	cidr = first(cidr.split('/')[0], cidr.split('/')[1]) + '/' + cidr.split('/')[1]
	print 'after = ' + cidr

	for lab in data:
		lab_name = lab[0]
		num_machine = lab[1]

		for i in range(32):
			if (1 << int(i)) >= num_machine:
				total_alloted += (1 << int(i))
				break

	# end mein +2 nai kia
	temp = (1 << (32 - int(cidr.split('/')[1]))) - total_alloted
	for i in range(32):
		if (1 << int(i)) > temp and i > 0:
			temp = (1 << int(i-1))
			break
	data.append(['Other', temp])
	data.sort(key=operator.itemgetter(1),reverse=True)

	for lab in data:
		lab_name = lab[0]
		num_machine = lab[1]

		temp = allot(cidr, alloted_yet, num_machine)

		given_cidr = temp[0]
		alloted_yet += int(temp[1])

		ip_list = get_ip_list(given_cidr, temp[1])

		struct = []
		struct.append(lab_name)
		struct.append(given_cidr)
		struct.append(ip_list)

		print lab_name, "alloted", given_cidr, 'required:', num_machine, 'list :'
		for i in ip_list:
			print i

		ret.append(struct)

	return ret

# TEST-CASE
allot_cidr('10.4.5.8/23', [
	['a', 76],
	['b', 54],
	['c', 30],
	['d', 4],
	['e', 4],
	['f', 4]
])
