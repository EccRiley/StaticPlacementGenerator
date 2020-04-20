import csv, pprint


def read_number_of_broken_engines_and_number_repaired_file(filename, engine_subtype, data_storage):
	with open(filename, 'rt') as file:
		data = csv.reader(file)
		data_as_list = list(data)
		number_of_broken_engines = data_as_list[0][1:]
		for num in number_of_broken_engines:
			data_storage[engine_subtype][int(num)] = {}
		data_as_list_without_header = data_as_list[1:]
		for row in data_as_list_without_header:
			num_repaired = int(row[0])
			probabilities = row[1:]
			num_broken = 1
			for prob in probabilities:
				if prob != '':
					data_storage[engine_subtype][num_broken][num_repaired] = float(prob)
				num_broken += 1
	return data_storage

def read_expected_transport_cost_file(filename, engine_subtype, hubs, data_storage):
	with open(filename, 'rt') as file:
		data = csv.reader(file)
		data_as_list = list(data)
		data_as_list_without_header = data_as_list[1:]
		for row in data_as_list_without_header:
			state_region = row[0]
			costs = row[1:]
			for i in range(7):
				data_storage[engine_subtype][state_region][hubs[i]] = float(costs[i])
	return data_storage

def read_probabilities_of_num_removals_in_each_state_region_file(filename, engine_subtype, data_storage):
	with open(filename, 'rt') as file:
		data = csv.reader(file)
		data_as_list = list(data)
		header = data_as_list[0]	
		data_as_list_without_header = data_as_list[1:]
		for row in data_as_list_without_header:
			state_region  = row[0]
			if state_region == '':
				break
			for num_removals in range(0, 11):
				data_storage[engine_subtype][state_region][num_removals] = float(row[num_removals + 1])
	return data_storage

def read_num_removals_state_regions_and_hubs_file(max_num_removals, data_storage):
	for num_removals in range(1, max_num_removals + 1):
		filepath = 'data_to_read/permutations/removals/' + str(num_removals) + '_removals_state_regions_and_hubs.csv'
		with open(filepath, 'rt') as file:
			data = csv.reader(file)
			data_as_list = list(data)
			data_as_list_without_header = data_as_list[1:]
			for row in data_as_list_without_header:
				data_storage[num_removals].append(row)
	return data_storage

def read_num_engines_placement_file(filename, data_storage):
	with open(filename, 'rt') as file:
		data = csv.reader(file)
		data_as_list = list(data)
		data_as_list_without_header = data_as_list[1:]
		for row in data_as_list_without_header:
			perm = []
			for i in row[2:]:
				perm.append(int(i))
			data_storage[int(row[0])].append(perm)
	return data_storage

def read_num_engines_num_to_place_file(filename, data_storage):
	with open(filename, 'rt') as file:
		data = csv.reader(file)
		data_as_list = list(data)
		data_as_list_without_header = data_as_list[1:]
		for row in data_as_list_without_header:
			perm = []
			for i in row:
				perm.append(int(i))
			data_storage.append(perm)
	return data_storage











