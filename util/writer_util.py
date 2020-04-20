import pprint, csv

def export_permutations(total_num_engines, perms_of_num_engines, perms_of_engine_placement_by_num_to_place):
	export_all_possible_situations_of_available_and_broken_engines(
		total_num_engines=total_num_engines,
		perms_of_num_engines=perms_of_num_engines)
	export_perms_of_engine_placement(
		total_num_engines=total_num_engines, 
		perms_of_engine_placement_by_num_to_place=perms_of_engine_placement_by_num_to_place)

def export_all_possible_situations_of_available_and_broken_engines(total_num_engines, perms_of_num_engines):
	with open('data_to_read/permutations/' + str(total_num_engines) + '_engines_num_to_place.csv', 'w') as file:
		writer = csv.writer(file)
		header = ['SPARES AVAILABLE', 'BEING REPAIRED-ATL', 'BEING REPAIRED-MSP']
		writer.writerow(header)
		rows_to_write = []
		for perm in perms_of_num_engines:
			rows_to_write.append(perm)
		writer.writerows(rows_to_write)

def export_perms_of_engine_placement(total_num_engines, perms_of_engine_placement_by_num_to_place):
	with open('data_to_read/permutations/' + str(total_num_engines) + '_engines_placement.csv', 'w') as file:
		writer = csv.writer(file)
		header = ['SPARES AVAILABLE', 'BEING REPAIRED', 'ATL', 'CVG', 'DTW', 'MSP', 'SLC', 'SEA', 'LAX']
		writer.writerow(header)
		rows_to_write = []
		for spares_available, perms in perms_of_engine_placement_by_num_to_place.items():
			being_repaired = total_num_engines - spares_available
			for perm in perms:
				row_to_write = [spares_available, being_repaired]
				row_to_write += perm
				rows_to_write.append(row_to_write[:])
		writer.writerows(rows_to_write)

def export_static_placement(best_engine_placement_and_costs, engine_subtype, engine_subtype_filename, num_engines, max_num_removals, hubs, time_range):
	filepath = 'data_exported/' + engine_subtype_filename + '_' + time_range + '_' + str(num_engines) + '_engines_static_placement.csv'
	with open(filepath, 'w') as file:
		writer = csv.writer(file)
		header = ['TOTAL SPARES', 'TO PLACE', 'BEING REPAIRED AT ATL', 'BEING REPAIRED AT MSP'] + hubs + ['COST']
		writer.writerow(header)
		rows_to_write = []
		for situation, cost_and_placement in best_engine_placement_and_costs.items():
			current_situation = situation[1:-1]
			to_place, being_repaired_atl, being_repaired_msp = current_situation.split(", ")
			row_to_write = [num_engines, int(to_place), int(being_repaired_atl), int(being_repaired_msp)]
			for placement in cost_and_placement['PLACEMENT']:
				row_to_write.append(placement)
			row_to_write.append(cost_and_placement['COST'])
			rows_to_write.append(row_to_write)
		writer.writerows(rows_to_write)







