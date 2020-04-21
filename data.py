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
	
	global engine_subtypes
	engine_subtypes = []

	global all_possible_states
	all_possible_states = {}

	global removals_info
	removals_info = {}

	global need_to_update_removal_info
	need_to_update_removal_info = {}

	global engines_info
	engines_info = {}

	global aos_cost
	aos_cost = {}

	global expected_transport_cost
	expected_transport_cost = {}

	global probability_of_num_repair_given_num_broken
	probability_of_num_repair_given_num_broken = {}

	global probabilities_of_num_removals_in_each_state_region
	probabilities_of_num_removals_in_each_state_region = {}

	global all_possible_num_working_num_broken
	all_possible_num_working_num_broken = {}

	global all_possible_removal_situations
	all_possible_removal_situations = {}




