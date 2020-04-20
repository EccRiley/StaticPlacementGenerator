from util import reader_util, writer_util, data_util
import data, static_placement_finder
import pprint, logging

if __name__ == '__main__':
	data.init()

	logging.basicConfig(level=logging.INFO)
	
	time_range = '2015-2019'

	file_with_all_permutations_exists = True

	# ********** V2500-D5 ********** 2015-2018 done, 2015-2019 done
	# engine_subtype = 'V2500 - D5'
	# engine_subtype_filename = 'V2500-D5'
	# num_engines = 4
	# max_num_removals_to_iterate = 5
	# max_num_removals_to_find_cost = 5
	# subtype_aos_cost = 9072

	# ********** TRENT8-892-17 ********** 2015-2018 done
	engine_subtype = 'TRENT8 - 892-17'
	engine_subtype_filename = 'TRENT8-892-17'
	num_engines = 1
	max_num_removals_to_iterate = 1
	max_num_removals_to_find_cost = 1
	subtype_aos_cost = 20105

	# ********** PW4000-4168 ********** 2015-2018 done
	# engine_subtype = 'PW4000 - 4168'
	# engine_subtype_filename = 'PW4000-4168'
	# num_engines = 1
	# max_num_removals_to_iterate = 5
	# max_num_removals_to_find_cost = 5
	# subtype_aos_cost = 17556

	# ********** PW4000-4060 ********** 2015-2018 done
	# engine_subtype = 'PW4000 - 4060'
	# engine_subtype_filename = 'PW4000-4060'
	# num_engines = 2
	# max_num_removals_to_iterate = 2
	# max_num_removals_to_find_cost = 2
	# subtype_aos_cost = 9081

	# ********** PW2000-2040 ********** 2015-2018 done
	# engine_subtype = 'PW2000 - 2040'
	# engine_subtype_filename = 'PW2000-2040'
	# num_engines = 1
	# max_num_removals_to_iterate = 4
	# max_num_removals_to_find_cost = 4
	# subtype_aos_cost = 9134.5

	# ********** PW2000-2037 ********** 2015-2018 done
	# engine_subtype = 'PW2000 - 2037'
	# engine_subtype_filename = 'PW2000-2037'
	# num_engines = 3
	# max_num_removals_to_iterate = 5
	# max_num_removals_to_find_cost = 5
	# subtype_aos_cost = 9134.5

	# ********** JT8D-219 **********
	# ********** need to re-generate combinations
	# 10 in ATL, 5 CVG DTW MSP, 0 LAX SEA SLC, 2 non-hubs
	# engine_subtype = 'JT8D - 219'
	# engine_subtype_filename = 'JT8D-219'
	# num_engines = 4
	# max_num_removals_to_iterate = 17
	# max_num_removals_to_find_cost = 17
	# subtype_aos_cost = 9177

	# ********** CFM56-7B27E-B1F ********** 2015-2018 done
	# engine_subtype = 'CFM56 - 7B27E/B1F'
	# engine_subtype_filename = 'CFM56-7B27E-B1F'
	# num_engines = 1
	# max_num_removals_to_iterate = 2
	# max_num_removals_to_find_cost = 2
	# subtype_aos_cost = 7417

	# ********** CFM56-7B26 ********** 2015-2018 done
	# engine_subtype = 'CFM56 - 7B26'
	# engine_subtype_filename = 'CFM56-7B26'
	# num_engines = 3
	# max_num_removals_to_iterate = 3
	# max_num_removals_to_find_cost = 3
	# subtype_aos_cost = 5350.5

	# ********** CFM56-5B3-3 ********** 2015-2018 done
	# engine_subtype = 'CFM56 - 5B3/3'
	# engine_subtype_filename = 'CFM56-5B3-3'
	# num_engines = 1
	# max_num_removals_to_iterate = 1
	# max_num_removals_to_find_cost = 1
	# subtype_aos_cost = 8843

	# ********** CFM56-5A ********** 2015-2018 done
	# engine_subtype = 'CFM56 - 5A'
	# engine_subtype_filename = 'CFM56-5A'
	# num_engines = 5
	# max_num_removals_to_iterate = 7
	# max_num_removals_to_find_cost = 7
	# subtype_aos_cost = 5053.5

	# ********** CF6-80E1A4 ********** 2015-2018 done
	# engine_subtype = 'CF6 - 80E1A4'
	# engine_subtype_filename = 'CF6-80E1A4'
	# num_engines = 2
	# max_num_removals_to_iterate = 1
	# max_num_removals_to_find_cost = 1
	# subtype_aos_cost = 22403

	# ********** CF6-80C2B8F ********** 2015-2018 done
	# engine_subtype = 'CF6 - 80C2B8F'
	# engine_subtype_filename = 'CF6-80C2B8F'
	# num_engines = 1
	# max_num_removals_to_iterate = 4
	# max_num_removals_to_find_cost = 4
	# subtype_aos_cost = 8580

	# ********** CF6-80C2B6F ********** 2015-2018 done
	# engine_subtype = 'CF6 - 80C2B6F'
	# engine_subtype_filename = 'CF6-80C2B6F'
	# num_engines = 2
	# max_num_removals_to_iterate = 5
	# max_num_removals_to_find_cost = 5
	# subtype_aos_cost = 8200

	# ********** CF6-80C2B6 ********** 2015-2018 done
	# engine_subtype = 'CF6 - 80C2B6'
	# engine_subtype_filename = 'CF6-80C2B6'
	# num_engines = 1
	# max_num_removals_to_iterate = 2
	# max_num_removals_to_find_cost = 2
	# subtype_aos_cost = 13121

	# ********** BR700-715C1-30 ********** 2015-2018 done
	# engine_subtype = 'BR700 - 715C1-30'
	# engine_subtype_filename = 'BR700-715C1-30'
	# num_engines = 2
	# max_num_removals_to_iterate = 5
	# max_num_removals_to_find_cost = 5
	# subtype_aos_cost = 4525

	data.probabilities_of_engine_repair_within_month_by_num_broken = data_util.set_probabilities_of_engine_repair_within_month_by_num_broken(
		engine_subtypes_overall=data.all_engine_subtypes_overall,
		data_storage=data.probabilities_of_engine_repair_within_month_by_num_broken)
	data.expected_cost_to_transport_engine_from_hub_for_each_state_region = data_util.set_expected_cost_to_transport_engine_from_hub_for_each_state_region(
		engine_subtypes_overall=data.all_engine_subtypes_overall,
		hubs_and_state_regions=data.hubs_and_state_regions,
		hubs=data.current_delta_hubs,
		data_storage=data.expected_cost_to_transport_engine_from_hub_for_each_state_region)
	data.probabilities_of_num_removals_in_each_state_region = data_util.set_probabilities_of_num_removals_in_each_state_region(
		engine_subtypes_overall=data.all_engine_subtypes_overall,
		hubs_and_state_regions=data.hubs_and_state_regions,
		data_storage=data.probabilities_of_num_removals_in_each_state_region)
	data.all_possible_removal_situations_by_number_of_removals = data_util.set_all_possible_removal_situations_by_number_of_removals(
		max_num_removals=max_num_removals_to_find_cost,
		data_storage=data.all_possible_removal_situations_by_number_of_removals)

	# ********** READING FROM FILES **********

	data.probabilities_of_engine_repair_within_month_by_num_broken = reader_util.read_number_of_broken_engines_and_number_repaired_file(
		filename='data_to_read/' + engine_subtype_filename + '/' + engine_subtype_filename + '_number_of_broken_engines_and_number_repaired.csv', 
		engine_subtype=engine_subtype, 
		data_storage=data.probabilities_of_engine_repair_within_month_by_num_broken)
	data.expected_cost_to_transport_engine_from_hub_for_each_state_region = reader_util.read_expected_transport_cost_file(
		filename='data_to_read/' + engine_subtype_filename + '/' + engine_subtype_filename + '_expected_transport_cost.csv', 
		engine_subtype=engine_subtype,
		hubs=data.current_delta_hubs,
		data_storage=data.expected_cost_to_transport_engine_from_hub_for_each_state_region)
	data.probabilities_of_num_removals_in_each_state_region = reader_util.read_probabilities_of_num_removals_in_each_state_region_file(
		filename='data_to_read/' + engine_subtype_filename + '/' + engine_subtype_filename + '_' + time_range + '_probabilities_of_num_removals_in_each_state_region.csv', 
		engine_subtype=engine_subtype,
		data_storage=data.probabilities_of_num_removals_in_each_state_region)
	data.all_possible_removal_situations_by_number_of_removals = reader_util.read_num_removals_state_regions_and_hubs_file(
		max_num_removals=max_num_removals_to_find_cost,
		data_storage=data.all_possible_removal_situations_by_number_of_removals)

	# ********** DOING CALCULATIONS **********

	print("\n******************** Finding static placement for " + str(num_engines) + " total engines with up to " + str(max_num_removals_to_find_cost) + " removals total happening in the month. ********************\n")
	static_placement_finder.find_static_placement(engine_subtype=engine_subtype, engine_subtype_filename=engine_subtype_filename, num_engines=num_engines, max_num_removals_to_iterate=max_num_removals_to_iterate, max_num_removals_to_find_cost=max_num_removals_to_find_cost, subtype_aos_cost=subtype_aos_cost, time_range=time_range, file_with_all_permutations_exists=file_with_all_permutations_exists)















