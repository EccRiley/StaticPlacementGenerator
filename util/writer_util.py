import pprint, csv
import data


def export_all_possible_removal_situations(filepath, engine_subtype, all_possible_removal_situations):
	with open(filepath, 'w') as file:
		writer = csv.writer(file)
		rows_to_write = []
		for row in all_possible_removal_situations:
			rows_to_write.append(row)
		writer.writerows(rows_to_write)

def export_all_possible_states(all_states):
	with open('data_to_read/all_possible_states.csv', 'w') as file:
		writer = csv.writer(file)
		rows_to_write = []
		for num_engines, states in all_states.items():
			for state in states:
				row_to_write = [num_engines]
				row_to_write.extend(state)
				rows_to_write.append(row_to_write)
		writer.writerows(rows_to_write) 

def export_all_possible_num_working_num_broken(num_working_num_broken):
	with open('data_to_read/all_possible_num_working_num_broken.csv', 'w') as file:
		writer = csv.writer(file)
		rows_to_write = []
		for num_engines, all_situations in all_possible_num_working_num_broken.items():
			for situation in all_situations:
				row_to_write = [num_engines]
				row_to_write.extend(situation)
				rows_to_write.append(row_to_write)
		writer.writerows(rows_to_write)

def export_best_placements(engine_subtype, best_placements):
	with open('data_exported/' + engine_subtype + '_static_placement.csv', 'w') as file:
		writer = csv.writer(file)
		header = ['NUM_ENGINES_WORKING', 'NUM_ENGINES_BROKEN_ATL', 'NUM_ENGINES_BROKEN_MSP', 'ATL', 'CVG', 'DTW', 'LAX', 'MSP', 'SEA', 'SLC', 'COST']
		writer.writerow(header)
		rows_to_write = []
		num_engines = data.engines_info[engine_subtype]
		for num_working_num_broken in data.all_possible_num_working_num_broken[num_engines]:
			num_working, num_broken_ATL, num_broken_MSP = num_working_num_broken
			row_to_write = [num_working, num_broken_ATL, num_broken_MSP]
			row_to_write.extend(best_placements[str(num_working_num_broken)]['PLACEMENT'])
			row_to_write.append(best_placements[str(num_working_num_broken)]['COST'])
			rows_to_write.append(row_to_write)
		writer.writerows(rows_to_write)










