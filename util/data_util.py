import pprint

def set_probabilities_of_engine_repair_within_month_by_num_broken(engine_subtypes_overall, data_storage):
	for engine_subtype in engine_subtypes_overall:
		data_storage[engine_subtype] = {}
	return data_storage

def set_expected_cost_to_transport_engine_from_hub_for_each_state_region(engine_subtypes_overall, hubs_and_state_regions, hubs, data_storage):
	for engine_subtype in engine_subtypes_overall:
		data_storage[engine_subtype] = {}
		for state_region in hubs_and_state_regions:
			data_storage[engine_subtype][state_region] = {}
			for hub in hubs:
				data_storage[engine_subtype][state_region][hub] = 0
	return data_storage

def set_probabilities_of_num_removals_in_each_state_region(engine_subtypes_overall, hubs_and_state_regions, data_storage):
	for engine_subtype in engine_subtypes_overall:
		data_storage[engine_subtype] = {}
		for state_region in hubs_and_state_regions:
			data_storage[engine_subtype][state_region] = {}
			for num_removals in range(0, 11):
				data_storage[engine_subtype][state_region][num_removals] = 0
	return data_storage

def set_all_possible_removal_situations_by_number_of_removals(max_num_removals, data_storage):
	for i in range(1, max_num_removals + 1):
		data_storage[i] = []
	return data_storage

def set_all_possible_engine_placements_by_spares_available(num_engines, data_storage):
	for i in range(num_engines + 1):
		data_storage[i] = []
	return data_storage

