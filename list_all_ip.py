def convert_to_binary(inp):
	inp = int(inp)
	ret = str('')
	
	while inp:
		temp = inp % 2
		ret += str(temp)
		inp /= 2

	ret = reversed(ret)
	return ret

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

# TEST-CASE
	# a = list_all_ip('10.220.64.0/18')

	# for ip in a:
	# 	print ip
