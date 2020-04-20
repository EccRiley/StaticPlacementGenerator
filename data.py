def init():

	global hubs
	hubs = ['ATL', 'CVG', 'DTW', 'LAX', 'MSP', 'SEA', 'SLC']

	global state_regions_without_hubs
	state_regions_without_hubs = ['AL', 'AR-LA', 'AR-OK', 'CT-RI-MA', 'DE-NJ-PA', 'GA', 'IA-IL', 'ID', 
		'ID-MT', 'IL', 'IL-IN-MI', 'IN', 'KS-MO', 'KY-OH', 'LA', 'MD-VA-PA', 'MI', 'MN', 'MO-AR', 'MS', 
		'MT', 'NC', 'NCA', 'ND', 'NFL', 'NH-VT-ME', 'NM-CO', 'NNY', 'NV-AZ-TX', 'NV-UT', 'OH', 'OR', 
		'PA', 'SC', 'SCA', 'SD-NE', 'SFL', 'SNY', 'TN', 'TX', 'VA', 'WA', 'WI', 'WI-MI', 'WV-VA', 'WY']

	global state_regions
	state_regions = ['ATL', 'CVG', 'DTW', 'LAX', 'MSP', 'SEA', 'SLC', 'AL', 'AR-LA', 'AR-OK', 
		'CT-RI-MA', 'DE-NJ-PA', 'GA', 'IA-IL', 'ID', 'ID-MT', 'IL', 'IL-IN-MI', 'IN', 'KS-MO', 'KY-OH', 
		'LA', 'MD-VA-PA', 'MI', 'MN', 'MO-AR', 'MS', 'MT', 'NC', 'NCA', 'ND', 'NFL', 'NH-VT-ME', 
		'NM-CO', 'NNY', 'NV-AZ-TX', 'NV-UT', 'OH', 'OR', 'PA', 'SC', 'SCA', 'SD-NE', 'SFL', 'SNY', 
		'TN', 'TX', 'VA', 'WA', 'WI', 'WI-MI', 'WV-VA', 'WY']
	
	global probability_of_num_repair_given_num_broken
	probability_of_num_repair_given_num_broken = {}

	global expected_transport_cost
	expected_transport_cost = {}

	global probabilities_of_num_removals_in_each_state_region
	probabilities_of_num_removals_in_each_state_region = {}

	global all_possible_engine_placements_by_spares_available
	all_possible_engine_placements_by_spares_available = {}

	global all_possible_situations_of_available_and_broken_engines
	all_possible_situations_of_available_and_broken_engines = []

	# ******************** SET VARIABLES ********************

	global all_engine_subtypes_overall
	all_engine_subtypes_overall = ['BR700 - 715C1-30', 'CF6 - 80C2B8F', 'CF6 - 80C2B6F', 'CF6 - 80C2B6', 
		'CF6 - 80A2', 'CFM56 - 5A', 'CFM56 - 7B26', 'CFM56 - 5B3/3', 'CFM56 - 7B27E/B1F', 'JT8D - 219', 
		'PW2000 - 2037', 'PW2000 - 2040', 'PW4000 - 4168', 'PW4000 - 4056', 'PW4000 - 4060', 'TRENT8 - 892-17', 
		'V2500 - D5', 'CF6 - 80E1A4']

	global current_delta_hubs
	current_delta_hubs = ['ATL', 'CVG', 'DTW', 'LAX', 'MSP', 'SEA', 'SLC']

	global state_regions
	state_regions = ['AL', 'AR-LA', 'AR-OK', 'CT-RI-MA', 'DE-NJ-PA', 'GA', 'IA-IL', 'ID', 'ID-MT', 
		'IL', 'IL-IN-MI', 'IN', 'KS-MO', 'KY-OH', 'LA', 'MD-VA-PA', 'MI', 'MN', 'MO-AR', 'MS', 'MT', 
		'NC', 'NCA', 'ND', 'NFL', 'NH-VT-ME', 'NM-CO', 'NNY', 'NV-AZ-TX', 'NV-UT', 'OH', 'OR', 'PA', 
		'SC', 'SCA', 'SD-NE', 'SFL', 'SNY', 'TN', 'TX', 'VA', 'WA', 'WI', 'WI-MI', 'WV-VA', 'WY']

	global hubs_and_state_regions
	hubs_and_state_regions = current_delta_hubs[:]
	hubs_and_state_regions.extend(state_regions[:])

	global prob_of_repair_within_month_by_num_broken 
	prob_of_repair_within_month_by_num_broken = {}

	global prob_of_num_removals_by_state_region 
	prob_of_num_removals_by_state_region = {}

	global expected_cost_to_transport_engine_from_hub 
	expected_cost_to_transport_engine_from_hub = {}

	# ******************** VARIABLES THAT CHANGE THROUGHOUT ITERATION ********************

	global best_engine_placement_and_costs 
	best_engine_placement_and_costs = {}

	global total_cost_of_current_spare_placement 
	total_cost_of_current_spare_placement = 'NOT SET'

	# the number of engines available at each hub for that iteration
	global num_engines_available_at_hubs 
	num_engines_available_at_hubs = {}

	for hub in current_delta_hubs:
		num_engines_available_at_hubs[hub] = 0

	global num_engines_available_at_hubs_to_edit
	num_engines_available_at_hubs_to_edit = {}

	# holds number of removals for each state region that one occurs in for the current possible removal situation iteration
	global state_regions_of_removals_and_num_removals
	state_regions_of_removals_and_num_removals = {}

	global state_regions_of_removals_and_num_removals_to_edit
	state_regions_of_removals_and_num_removals_to_edit = {}

	# holds probability of next removal for each state region that one occurs in for the current possible removal situation iteration
	global state_regions_removals_and_removal_prob
	state_regions_removals_and_removal_prob = {}

	global state_regions_removals_and_removal_prob_to_edit
	state_regions_removals_and_removal_prob_to_edit = {}

	global max_num_removals 
	max_num_removals = 'NOT SET'

	global current_num_removals 
	current_num_removals = 'NOT SET'

	global current_num_removals_left
	current_num_removals_left = 'NOT SET'

	global aos_cost 
	aos_cost = 'NOT SET'

	global current_num_to_place 
	current_num_to_place = 'NOT SET'

	global current_num_broken_atl 
	current_num_broken_atl = 'NOT SET'

	global current_num_broken_msp 
	current_num_broken_msp = 'NOT SET'

	global current_total_broken 
	current_total_broken = 'NOT SET'

	global current_total_repaired_during_month 
	current_total_repaired_during_month = 'NOT SET'

	global current_state_region_of_removal_with_highest_prob
	current_state_region_of_removal_with_highest_prob = 'NOT SET'

	global there_are_removals_remaining
	there_are_removals_remaining = 'NOT SET'

	global there_are_engines_remaining
	there_are_engines_remaining = 'NOT SET'

	global hub_with_min_cost
	hub_with_min_cost = 'NOT SET'



