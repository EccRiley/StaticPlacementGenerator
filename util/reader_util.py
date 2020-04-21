import csv, pprint, logging
import data

def import_all_possible_states(filepath, data_storage):
	logging.info("Importing all states...")
	with open(filepath, 'rt') as file:
		data_from_file = csv.reader(file)
		all_states = list(data_from_file)
		for row in all_states:
			num_working_engines = int(row[0])
			state = list(map(int, row[1:]))
			if num_working_engines not in data_storage:
				data_storage[num_working_engines] = []
			data_storage[num_working_engines].append(state)
	logging.info("All states have been imported.")
	return data_storage

def import_removal_info(filepath, removals_data_storage, aos_cost_data_storage):
	logging.info("Importing all removal information...")
	with open(filepath, 'rt') as file:
		data_from_file = csv.reader(file)
		data_as_list = list(data_from_file)
		header = data_as_list[0]
		all_rows = data_as_list[1:]
		for row in all_rows:
			assert ('' not in row[:12]), "There are empty cells in the removal_info file. All information for each fleet must be inputted. Values may be zero, but they may not be blank."
			try:
				engine_subtype = row[0]
				removals_data_storage[engine_subtype] = {
					'MAX_NUM_REMOVALS_MONTHLY_TOTAL': int(row[1]),
					'MAX_NUM_REMOVALS_MONTHLY_ATL': int(row[2]),
					'MAX_NUM_REMOVALS_MONTHLY_CVG': int(row[3]),
					'MAX_NUM_REMOVALS_MONTHLY_DTW': int(row[4]),
					'MAX_NUM_REMOVALS_MONTHLY_LAX': int(row[5]),
					'MAX_NUM_REMOVALS_MONTHLY_MSP': int(row[6]),
					'MAX_NUM_REMOVALS_MONTHLY_SEA': int(row[7]),
					'MAX_NUM_REMOVALS_MONTHLY_SLC': int(row[8]),
					'MAX_NUM_REMOVALS_MONTHLY_NON_HUBS': int(row[9])}
				aos_cost_data_storage[engine_subtype] = float(row[10])
				if row[11].upper() == 'TRUE':
					data.need_to_update_removal_info[engine_subtype] = True
				elif row[11].upper() == 'FALSE':
					data.need_to_update_removal_info[engine_subtype] = False 
				assert (row[11].upper() in ['TRUE', 'FALSE']), "The value in column 10 of the removal_info file must either be TRUE, indicating the information in the file has been changed since the previous run, or FALSE, indicating the information in the file is the same as the previous run."
			except Exception as e:
				logging.error("An exception has occurred: " + e)
				raise Exception("POSSIBLE SOLUTION: Make sure you are inputting integer values into the removal_info file for columns 2 through 9. String values cannot be accepted.")
	logging.info("All removal information has been imported.")
	return removals_data_storage, aos_cost_data_storage

def import_engine_info(filepath, data_storage):
	logging.info("This program can generate a default best spare placement for the following engine subtypes:")
	with open(filepath, 'rt') as file:
		data_from_file = csv.reader(file)
		data_as_list = list(data_from_file)
		header = data_as_list[0]
		all_rows = data_as_list[1:]
		for row in all_rows:
			assert ('' not in row[:2]), "There are empty cells in the engine_info file. Total number of engines for each fleet must be inputted."
			try:
				engine_subtype = row[0]
				data.engine_subtypes.append(engine_subtype)
				logging.info(engine_subtype)
				data_storage[engine_subtype] = int(row[1])
			except Exception as e:
				logging.error("An exception has occurred: " + str(e))
				raise Exception("POSSIBLE SOLUTION: Make sure you are inputting integer values for column 2. String values cannot be accepted.")
	logging.info("All engine information has been imported.")
	return data_storage

def import_engine_subtype_data():
	logging.info("Importing expected transportation costs, probabilities of engines repaired, and probabilities of removals...")
	for engine_subtype in data.engine_subtypes:
		path = 'data_to_read/' + engine_subtype + '/' + engine_subtype
		data.expected_transport_cost = import_expected_transport_cost(
			filepath=path + '_expected_transport_cost.csv', 
			engine_subtype=engine_subtype, 
			data_storage=data.expected_transport_cost)
		data.probability_of_num_repair_given_num_broken = import_number_of_broken_engines_and_number_repaired(
			filepath=path + '_number_of_broken_engines_and_number_repaired.csv', 
			engine_subtype=engine_subtype, 
			data_storage=data.probability_of_num_repair_given_num_broken)
		data.probabilities_of_num_removals_in_each_state_region = import_probabilities_of_num_removals_in_each_state_region(
			filename=path + '_2015-2019_probabilities_of_num_removals_in_each_state_region.csv', 
			engine_subtype=engine_subtype, 
			data_storage=data.probabilities_of_num_removals_in_each_state_region)
		logging.info(engine_subtype + " data has been imported.")

def import_expected_transport_cost(filepath, engine_subtype, data_storage):
	data_storage[engine_subtype] = {}
	with open(filepath, 'rt') as file:
		data_from_file = csv.reader(file)
		data_as_list = list(data_from_file)
		hubs_header = data_as_list[0][1:]
		all_costs = data_as_list[1:]
		for row in all_costs:
			state_region = row[0]
			costs = row[1:]
			data_storage[engine_subtype][state_region] = {}
			for i in range(7):
				data_storage[engine_subtype][state_region][hubs_header[i]] = float(costs[i])
	return data_storage

def import_number_of_broken_engines_and_number_repaired(filepath, engine_subtype, data_storage):
	data_storage[engine_subtype] = {}
	with open(filepath, 'rt') as file:
		data_from_file = csv.reader(file)
		data_as_list = list(data_from_file)
		num_broken_header = data_as_list[0][1:]
		for num in num_broken_header:
			data_storage[engine_subtype][int(num)] = {}
		all_repair_probabilities = data_as_list[1:]
		for row in all_repair_probabilities:
			num_repaired = int(row[0])
			probabilities = row[1:]
			index_count = 0
			for num in num_broken_header:
				if (int(num) >= num_repaired):
					data_storage[engine_subtype][int(num)][num_repaired] = float(probabilities[index_count])
				index_count += 1
	return data_storage

def import_probabilities_of_num_removals_in_each_state_region(filename, engine_subtype, data_storage):
	data_storage[engine_subtype] = {}
	with open(filename, 'rt') as file:
		data_from_file = csv.reader(file)
		data_as_list = list(data_from_file)
		num_removals_header = data_as_list[0]	
		all_rows = data_as_list[1:]
		for row in all_rows:
			state_region  = row[0]
			if state_region == '':
				break
			data_storage[engine_subtype][state_region] = {}
			for num_removals in range(0, 11):
				data_storage[engine_subtype][state_region][num_removals] = float(row[num_removals + 1])
	return data_storage

def import_all_possible_removal_situations(data_storage):
	logging.info("Importing all possible removal situations...")
	for engine_subtype in data.engine_subtypes:
		data_storage = import_removal_situations(
			filepath='data_to_read/' + engine_subtype + '/' + engine_subtype + '_all_possible_removal_situations.csv',
			engine_subtype=engine_subtype,
			data_storage=data_storage)
	logging.info("All possible removal situations have been imported.")
	return data_storage

def import_removal_situations(filepath, engine_subtype, data_storage):
	data_storage[engine_subtype] = []
	with open(filepath, 'rt') as file:
		data_from_file = csv.reader(file)
		data_as_list = list(data_from_file)
		for row in data_as_list:
			data_storage[engine_subtype].append(row)
	return data_storage

def import_all_possible_num_working_num_broken(filepath, data_storage):
	logging.info("Importing all possible ways in which engines can be working and broken...")
	with open(filepath, 'rt') as file:
		data_from_file = csv.reader(file)
		all_situations = list(data_from_file)
		for row in all_situations:
			num_engines = int(row[0])
			situation = list(map(int, row[1:]))
			if num_engines not in data_storage:
				data_storage[num_engines] = []
			if int(row[1]) > 0:
	 			data_storage[num_engines].append(situation)
	logging.info("All situations have been imported.")
	return data_storage













