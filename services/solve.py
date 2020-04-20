from util import reader_util, writer_util, data_util
from itertools import permutations
import data
import copy, logging, pprint

class CostCalculator():

	def __init__(self, engine_subtype, current_state):
		self.engine_subtype = engine_subtype
		self.current_state = current_state

		self.aos_cost = data.aos_cost[self.engine_subtype]
		self.probability_of_repair = data.probability_of_num_repair_given_num_broken[self.engine_subtype]
		self.expected_transport_cost = data.expected_transport_cost[self.engine_subtype]
		self.num_working_engines = data.engines_info[self.engine_subtype]['NUM_WORKING_ENGINES']
		self.num_broken_engines_ATL = data.engines_info[self.engine_subtype]['NUM_BROKEN_ENGINES_ATL']
		self.num_broken_engines_MSP = data.engines_info[self.engine_subtype]['NUM_BROKEN_ENGINES_MSP']
		self.num_broken_engines_total = (self.num_broken_engines_ATL + self.num_broken_engines_MSP)
		self.all_possible_removal_situations = data.all_possible_removal_situations[self.engine_subtype]
		self.num_departures = data.num_departures_by_hub_monthly[self.engine_subtype]
		self.prob_of_num_removals_by_state_region = data.probabilities_of_num_removals_in_each_state_region[self.engine_subtype]
		self.departure_ground_time = data.total_departures_ground_time_by_state_region_monthly[self.engine_subtype]
		self.RONS_RADS_ground_time = data.total_RONSRADS_ground_time_by_hub_monthly[self.engine_subtype]
		self.regression = data.regression[self.engine_subtype]

		self.total_departure_ground_time = 0
		self.set_total_departure_ground_time_of_locations_without_regression_data()
		self.expected_cost_of_current_state = 0
		self.num_engines_available_at_hubs = {}
		self.set_num_engines_available_at_hubs()
		self.current_num_engines_repaired_ATL = 0 
		self.current_num_engines_repaired_MSP = 0  
		self.current_num_engines_repaired_total = 0
		self.probability_of_current_num_engines_repaired = 0
		self.current_num_removals = 0
		self.current_state_regions_of_removals_and_num_removals = {}
		self.current_state_regions_of_removals_and_removal_probabilities = {}
		self.probability_of_current_removal_situation = 0
		self.num_removals_left_in_iteration = 0
		self.num_engines_available_at_hubs_in_iteration = {}
		self.state_regions_of_removals_and_num_removals_to_edit = {}
		self.state_regions_of_removals_and_removal_probabilities_to_edit = {}
		self.there_are_removals_remaining = True 
		self.there_are_engines_remaining = True 

	def set_total_departure_ground_time_of_locations_without_regression_data(self):
		for location, ground_time in self.departure_ground_time.items():
			self.total_departure_ground_time += (sum(ground_time.values())/3)
		for location in self.regression.keys():
			if location != 'OTHER':
				self.total_departure_ground_time -= (sum(self.departure_ground_time[location].values())/3)

	def set_num_engines_available_at_hubs(self):
		for i in range(7):
			self.num_engines_available_at_hubs[data.hubs[i]] = self.current_state[i]

	def get_cost(self):
		logging.info('Currently finding expected cost associated with spare placement: ' + str(self.current_state))
		self.calculate_expected_cost_of_current_state()
		logging.info('Cost of removal situation found: ' + str(self.expected_cost_of_current_state))
		return self.expected_cost_of_current_state

	def calculate_expected_cost_of_current_state(self):
		# Iterate over the number of engines that could be repaired at ATL given the current number of engines broken at ATL
		for num_engines_repaired_ATL in range(self.num_broken_engines_ATL+1):
			# Iterate over the number of engines that could be repaired at MSP given the current number of engines broken at MSP
			for num_engines_repaired_MSP in range(self.num_broken_engines_MSP+1):
				self.set_current_engines_repaired_variables(num_engines_repaired_ATL, num_engines_repaired_MSP)
				self.get_current_probability_of_num_engines_repaired()
				self.consider_repaired_engines_as_working_engines_in_num_engines_available_at_hubs()
				self.look_at_all_possible_ways_in_which_removals_can_happen()
				self.reset_num_engines_available_at_hubs()

	def set_current_engines_repaired_variables(self, num_engines_repaired_ATL, num_engines_repaired_MSP):
		self.current_num_engines_repaired_ATL = num_engines_repaired_ATL
		self.current_num_engines_repaired_MSP = num_engines_repaired_MSP
		self.current_num_engines_repaired_total = (self.current_num_engines_repaired_ATL + self.current_num_engines_repaired_MSP)

	def get_current_probability_of_num_engines_repaired(self):
		# There's a probability associated with a possible repair only if engines are broken
		self.probability_of_current_num_engines_repaired = 0
		if self.num_broken_engines_total > 0:
			self.probability_of_current_num_engines_repaired = self.probability_of_repair[self.num_broken_engines_total][self.current_num_engines_repaired_total] 

	def consider_repaired_engines_as_working_engines_in_num_engines_available_at_hubs(self):
		self.num_engines_available_at_hubs['ATL'] += self.current_num_engines_repaired_ATL
		self.num_engines_available_at_hubs['MSP'] += self.current_num_engines_repaired_MSP

	def reset_num_engines_available_at_hubs(self):
		self.num_engines_available_at_hubs['ATL'] -= self.current_num_engines_repaired_ATL
		self.num_engines_available_at_hubs['MSP'] -= self.current_num_engines_repaired_MSP

	def look_at_all_possible_ways_in_which_removals_can_happen(self):
		# Iterate over ever possible removal situation given the current number of total removals
		for possible_removal_situation in self.all_possible_removal_situations:
			self.current_num_removals = sum(list(map(int, possible_removal_situation)))
			# Find the probability to multiply to the cost of this removal situation
			self.set_current_probability_of_removal_situation(possible_removal_situation)
			# Find total cost of all actions taken this month based on the current removal situation
			total_cost_of_current_removal_situation = 0
			if self.probability_of_current_removal_situation > 0:
				total_cost_of_current_removal_situation = self.get_total_cost_of_current_removal_situation()
			probability_to_multiply = self.probability_of_current_removal_situation
			if self.num_broken_engines_total > 0:
				probability_to_multiply = (self.probability_of_current_removal_situation * self.probability_of_current_num_engines_repaired)
			# Multiply the cost of this situation by the probability of it happening
			cost_of_possible_removal = (probability_to_multiply * total_cost_of_current_removal_situation)
			# Then add that value to the total expected cost for this spare engine placement
			self.expected_cost_of_current_state += cost_of_possible_removal

	def set_current_probability_of_removal_situation(self, removal_situation):
		self.probability_of_current_removal_situation = -1
		self.current_state_regions_of_removals_and_num_removals = {}
		self.current_state_regions_of_removals_and_removal_probabilities = {}
		for i in range(53):
			num_removals_in_state_region = int(removal_situation[i])
			if (num_removals_in_state_region > 0): # If at least 1 removal occurs in this state region
				state_region_of_removal = data.state_regions[i] 
				probability = self.prob_of_num_removals_by_state_region[state_region_of_removal][num_removals_in_state_region]
				self.current_state_regions_of_removals_and_num_removals[state_region_of_removal] = num_removals_in_state_region
				self.current_state_regions_of_removals_and_removal_probabilities[state_region_of_removal] = self.prob_of_num_removals_by_state_region[state_region_of_removal][1]
				if probability == 0:
					self.probability_of_current_removal_situation = 0
					break
				elif (self.probability_of_current_removal_situation == -1):
					self.probability_of_current_removal_situation = probability
				else:
					self.probability_of_current_removal_situation *= probability 
			else: # If no removals occur in this state region
				state_region = data.state_regions[i]
				probability = self.prob_of_num_removals_by_state_region[state_region_of_removal][0]
				if probability == 0:
					self.probability_of_current_removal_situation = 0
					break
				elif (self.probability_of_current_removal_situation == -1):
					self.probability_of_current_removal_situation = probability
				else:
					self.probability_of_current_removal_situation *= probability 

	def get_total_cost_of_current_removal_situation(self):
		self.there_are_removals_remaining = True 
		self.there_are_engines_remaining = True 
		# If there are no engines to place AND there are none that are being considered to be repaired during this month, then there are no engines remaining to allocate for any removals
		if (self.num_working_engines == 0) and (self.current_num_engines_repaired_total == 0):
			self.there_are_engines_remaining = False
		# Store data to change throughout iteration
		self.num_removals_left_in_iteration = self.current_num_removals
		self.num_engines_available_at_hubs_in_iteration = copy.deepcopy(self.num_engines_available_at_hubs)
		self.state_regions_of_removals_and_num_removals_to_edit = copy.deepcopy(self.current_state_regions_of_removals_and_num_removals)
		self.state_regions_of_removals_and_removal_probabilities_to_edit = copy.deepcopy(self.current_state_regions_of_removals_and_removal_probabilities)
		total_cost_of_current_removal_situation = 0 # sum up the total cost of all the actions taken in the month
		# While there are removals remaining to happen AND engines remaining to service those removals
		while self.there_are_removals_remaining and self.there_are_engines_remaining:
			cost_of_removal, location_of_removal, hub_to_service_removal = self.cost_to_service_removal_from_hub_with_min_transport_cost()
			total_cost_of_current_removal_situation += cost_of_removal
			self.reset_variables_to_reflect_action_for_this_removal(cost_of_removal, location_of_removal, hub_to_service_removal)
			if self.rest_of_removals_have_no_possibility_of_happening():
				self.there_are_removals_remaining = False
		if self.there_are_removals_remaining:
			# If there are removals remaining but no engines are available to service it, incure an AOS cost for the remaining removals
			total_cost_of_current_removal_situation += (self.num_removals_left_in_iteration * self.aos_cost)
		return total_cost_of_current_removal_situation

	def rest_of_removals_have_no_possibility_of_happening(self):
		if sum(self.state_regions_of_removals_and_removal_probabilities_to_edit.values()) == 0:
			return True 
		return False

	def cost_to_service_removal_from_hub_with_min_transport_cost(self):
		removal_probabilities = list(self.state_regions_of_removals_and_removal_probabilities_to_edit.values()) # List all probabilities of the remaining removals
		regions = list(self.state_regions_of_removals_and_removal_probabilities_to_edit.keys()) # List all state regions where removals are left to occur
		# Get state region of removal that has the highest probability of occurring
		state_region_of_next_removal = regions[removal_probabilities.index(max(removal_probabilities))]
		# Reset data for this removal
		cost_to_service_removal_from_hub_with_min_transport_cost = -1
		hub_with_min_cost = ''
		for hub_of_engine, num_engines_at_hub in self.num_engines_available_at_hubs_in_iteration.items(): # for every hub
			if num_engines_at_hub > 0: # If that hub has an engine available to service the removal
				# Find the cost to transport that engine from the hub to the state region
				cost_to_transport = self.expected_transport_cost[state_region_of_next_removal][hub_of_engine]
				if (cost_to_service_removal_from_hub_with_min_transport_cost == -1) or (cost_to_transport < cost_to_service_removal_from_hub_with_min_transport_cost):
					cost_to_service_removal_from_hub_with_min_transport_cost = cost_to_transport
					hub_with_min_cost = hub_of_engine
		return cost_to_service_removal_from_hub_with_min_transport_cost, state_region_of_next_removal, hub_with_min_cost

	def reset_variables_to_reflect_action_for_this_removal(self, cost_of_removal, location_of_removal, hub_to_service_removal):
		# Remove removal from dictionary being iterated
		self.state_regions_of_removals_and_num_removals_to_edit[location_of_removal] -= 1
		# True if there are no more removals remaining to occur for this state region, false otherwise
		if (self.state_regions_of_removals_and_num_removals_to_edit[location_of_removal] == 0):
			# Delete state region from both dictionaries 
			del self.state_regions_of_removals_and_num_removals_to_edit[location_of_removal]
			del self.state_regions_of_removals_and_removal_probabilities_to_edit[location_of_removal]
		else: # If there is a removal for this state region that still needs to happen
			# Find the number of removals that have already occurred for this region
			removals_that_have_occurred_in_this_region = (self.current_state_regions_of_removals_and_num_removals[location_of_removal] - self.state_regions_of_removals_and_num_removals_to_edit[location_of_removal])
			# Reset the probability associated with the next removal for this state region to match what number in sequence it will be
			self.state_regions_of_removals_and_removal_probabilities_to_edit[location_of_removal] = self.prob_of_num_removals_by_state_region[location_of_removal][removals_that_have_occurred_in_this_region+1]
		# Subtract 1 removal from the total number of removals currently iterating
		self.num_removals_left_in_iteration -= 1
		# True if there are NO removals remaining to occur in the current month, false otherwise
		if (self.num_removals_left_in_iteration == 0):
			self.there_are_removals_remaining = False
		# Remove this engine from dictionary being iterated because the engine has just been used for this removal
		self.num_engines_available_at_hubs_in_iteration[hub_to_service_removal] -= 1
		# Get number of engines still available
		engines_available = sum(self.num_engines_available_at_hubs_in_iteration.values()) 
		if (engines_available == 0): # True if there are NO engines available to service removals, false otherwise
			self.there_are_engines_remaining = False

# def setup_data_variables(engine_subtype, num_engines, aos_cost, max_num_removals):
# 	# store data from function arguments provided
# 	data.aos_cost = aos_cost
# 	data.max_num_removals = max_num_removals
	
# 	# store data for this subtype from data imported
# 	data.prob_of_repair_within_month_by_num_broken = data.probability_of_num_repair_given_num_broken[engine_subtype]
# 	data.prob_of_num_removals_by_state_region = data.probabilities_of_num_removals_in_each_state_region[engine_subtype]
# 	data.expected_cost_to_transport_engine_from_hub = data.expected_transport_cost[engine_subtype]
	
# 	# import and store data for this number of engines
# 	data.all_possible_engine_placements_by_spares_available = data_util.set_all_possible_engine_placements_by_spares_available(
# 		num_engines=num_engines,
# 		data_storage=data.all_possible_engine_placements_by_spares_available)
# 	data.all_possible_engine_placements_by_spares_available = reader_util.read_num_engines_placement_file(
# 		filename='data_to_read/permutations/' + str(num_engines) + '_engines_placement.csv',
# 		data_storage=data.all_possible_engine_placements_by_spares_available)
# 	data.all_possible_situations_of_available_and_broken_engines = reader_util.read_num_engines_num_to_place_file(
# 		filename='data_to_read/permutations/' + str(num_engines) + '_engines_num_to_place.csv',
# 		data_storage=data.all_possible_situations_of_available_and_broken_engines)

# def find_static_placement(engine_subtype, engine_subtype_filename, num_engines, max_num_removals_to_iterate, max_num_removals_to_find_cost, subtype_aos_cost, time_range, file_with_all_permutations_exists=False):
# 	logging.info('Finding static placement for the ' + engine_subtype + ' engine subtype with ' + str(num_engines) + ' total engines.')
# 	logging.info('The static placement and costs will be based on all possible removal situations from 1 removal up to ' + str(max_num_removals_to_iterate) + ' removals occurring in the month.')
# 	# generate all permutations if they don't exist for this number of engines
# 	if not file_with_all_permutations_exists:
# 		find_all_permutations(total_num_engines=num_engines)
	
# 	setup_data_variables(
# 		engine_subtype=engine_subtype, 
# 		num_engines=num_engines,
# 		aos_cost=subtype_aos_cost, 
# 		max_num_removals=max_num_removals_to_iterate)
	
# 	# find the best spare placement for every [NUM TO PLACE, NUM BROKEN-ATL, NUM BROKEN-MSP] combination possible given the total number of engines for this fleet
# 	for num_to_place_and_num_broken in data.all_possible_situations_of_available_and_broken_engines:
# 		# store data for this current iteration
# 		data.best_engine_placement_and_costs[str(num_to_place_and_num_broken)] = {'COST': -1, 'PLACEMENT': []}
# 		data.current_num_to_place = num_to_place_and_num_broken[0]
# 		data.current_num_broken_atl, data.current_num_broken_msp = num_to_place_and_num_broken[1:]
# 		data.current_total_broken = (data.current_num_broken_atl + data.current_num_broken_msp)

# 		logging.info('Currently finding the best spare placement if: ' 
# 			+ str(data.current_num_to_place) + ' engines are needing to be placed, ' 
# 			+ str(data.current_num_broken_atl) + ' are broken and being repaired in ATL, and ' 
# 			+ str(data.current_num_broken_msp) + ' are broken and being repaired in MSP.')
		
# 		find_best_engine_placement_and_associated_cost(num_to_place_and_num_broken=num_to_place_and_num_broken)		

# 	logging.info("ALL BEST PLACEMENTS ARE FOUND.")
# 	for num_to_place_and_num_broken, cost_and_static_placement in data.best_engine_placement_and_costs.items():
# 		logging.info('Situation: ' + str(num_to_place_and_num_broken) + '. Placement: ' + str(cost_and_static_placement['PLACEMENT']) + '. Cost: ' + str(cost_and_static_placement['COST']))
	
# 	if (max_num_removals_to_iterate == max_num_removals_to_find_cost):
# 		writer_util.export_static_placement(
# 			best_engine_placement_and_costs=data.best_engine_placement_and_costs, 
# 			engine_subtype=engine_subtype, 
# 			engine_subtype_filename=engine_subtype_filename,  
# 			num_engines=num_engines,
# 			max_num_removals=data.max_num_removals,
# 			hubs=data.current_delta_hubs,
# 			time_range=time_range)
# 	else:
# 		find_expected_cost_for_static_placement_given_max_num_removals(
# 			engine_subtype=engine_subtype, 
# 			engine_subtype_filename=engine_subtype_filename, 
# 			num_engines=num_engines, 
# 			subtype_aos_cost=data.aos_cost, 
# 			max_num_removals=max_num_removals_to_find_cost, 
# 			best_engine_placement=data.best_engine_placement_and_costs,
# 			time_range=time_range)

# def find_expected_cost_for_static_placement_given_max_num_removals(engine_subtype, engine_subtype_filename, num_engines, subtype_aos_cost, max_num_removals, best_engine_placement, time_range):
# 	setup_data_variables(
# 		engine_subtype=engine_subtype, 
# 		num_engines=num_engines,
# 		aos_cost=subtype_aos_cost, 
# 		max_num_removals=max_num_removals)

# 	# find cost associated with every spare placement that's considered the 'best' for every [NUM TO PLACE, NUM BROKEN-ATL, NUM BROKEN-MSP] situation
# 	for num_to_place_and_num_broken in data.all_possible_situations_of_available_and_broken_engines:
# 		static_placement = best_engine_placement[str(num_to_place_and_num_broken)]['PLACEMENT']
# 		# store data for this current iteration
# 		data.best_engine_placement_and_costs[str(num_to_place_and_num_broken)] = {'COST': -1, 'PLACEMENT': static_placement}
# 		data.current_num_to_place = num_to_place_and_num_broken[0]
# 		data.current_num_broken_atl, data.current_num_broken_msp = num_to_place_and_num_broken[1:]
# 		data.current_total_broken = (data.current_num_broken_atl + data.current_num_broken_msp)

# 		data.total_cost_of_current_spare_placement = 0 # reset total cost of current spare placement

# 		logging.info('Currently finding expected cost (with up to ' + str(max_num_removals) + ' total removals) associated with spare placement: ' + str(static_placement) + ', which is the best placement for: ' + str(num_to_place_and_num_broken))

# 		# store data (number of engines available at each hub) to match the current spare placement
# 		for i in range(7):
# 			data.num_engines_available_at_hubs[data.current_delta_hubs[i]] = static_placement[i]

# 		find_total_cost_of_all_possible_removal_situations_for_current_spare_placement()

# 		logging.info('Cost found: ' + str(data.total_cost_of_current_spare_placement))

# 		# store cost found
# 		data.best_engine_placement_and_costs[str(num_to_place_and_num_broken)]['COST'] = data.total_cost_of_current_spare_placement

# 	writer_util.export_static_placement(
# 		best_engine_placement_and_costs=data.best_engine_placement_and_costs, 
# 		engine_subtype=engine_subtype, 
# 		engine_subtype_filename=engine_subtype_filename,  
# 		num_engines=num_engines,
# 		max_num_removals=data.max_num_removals,
# 		hubs=data.current_delta_hubs,
# 		time_range=time_range)

# def find_best_engine_placement_and_associated_cost(num_to_place_and_num_broken):
# 	# iterate over every possible spare placement given the current [NUM TO PLACE, NUM BROKEN-ATL, NUM BROKEN-MSP]
# 	for possible_spare_placement in data.all_possible_engine_placements_by_spares_available[data.current_num_to_place]:
# 		data.total_cost_of_current_spare_placement = 0 # reset total cost of current spare placement

# 		logging.info('Currently finding expected cost associated with spare placement: ' + str(possible_spare_placement))
		
# 		# store data (number of engines available at each hub) to match the current spare placement
# 		for i in range(7):
# 			data.num_engines_available_at_hubs[data.current_delta_hubs[i]] = possible_spare_placement[i]
		
# 		find_total_cost_of_all_possible_removal_situations_for_current_spare_placement()
		
# 		if best_engine_placement_and_costs_needs_to_be_updated(num_to_place_and_num_broken=num_to_place_and_num_broken):
# 			logging.info('New best placement found. Placement: ' + str(possible_spare_placement) + '. Cost: ' + str(data.total_cost_of_current_spare_placement))
# 			data.best_engine_placement_and_costs[str(num_to_place_and_num_broken)]['COST'] = data.total_cost_of_current_spare_placement
# 			data.best_engine_placement_and_costs[str(num_to_place_and_num_broken)]['PLACEMENT'] = possible_spare_placement

# def best_engine_placement_and_costs_needs_to_be_updated(num_to_place_and_num_broken):
# 	# return true if the cost hasn't been set, then set these values to it OR the new cost is lower than the current cost that is set
# 	if (data.best_engine_placement_and_costs[str(num_to_place_and_num_broken)]['COST'] == -1) or (data.total_cost_of_current_spare_placement < data.best_engine_placement_and_costs[str(num_to_place_and_num_broken)]['COST']):
# 		return True 
# 	return False

# def find_total_cost_of_all_possible_removal_situations_for_current_spare_placement():
# 	# iterate over the number of engines that could be repaired at ATL given the current number of engines broken at ATL
# 	for num_engines_repaired_during_month_ATL in range(data.current_num_broken_atl + 1):
# 		# iterate over the number of engines that could be repaired at MSP given the current number of engines broken at MSP
# 		for num_engines_repaired_during_month_MSP in range(data.current_num_broken_msp + 1):
# 			data.current_total_repaired_during_month = (num_engines_repaired_during_month_ATL + num_engines_repaired_during_month_MSP)
			
# 			probability_of_repair = get_current_probability_of_repair()
			
# 			# consider current repaired engines as available engines
# 			data.num_engines_available_at_hubs['ATL'] += num_engines_repaired_during_month_ATL
# 			data.num_engines_available_at_hubs['MSP'] += num_engines_repaired_during_month_MSP

# 			iterate_over_every_possible_removal_location_given_the_max_number_of_removals_to_iterate_up_to(
# 				num_engines_repaired_during_month_ATL=num_engines_repaired_during_month_ATL,
# 				num_engines_repaired_during_month_MSP=num_engines_repaired_during_month_MSP,
# 				probability_of_repair=probability_of_repair)
			
# 			# reset engines available for the current iteration 
# 			data.num_engines_available_at_hubs['ATL'] -= num_engines_repaired_during_month_ATL
# 			data.num_engines_available_at_hubs['MSP'] -= num_engines_repaired_during_month_MSP

# def get_current_probability_of_repair():
# 	# there's a probability associated with a possible repair only if engines are broken
# 	probability_of_repair = 0
# 	if data.current_total_broken > 0:
# 		probability_of_repair = data.prob_of_repair_within_month_by_num_broken[data.current_total_broken][data.current_total_repaired_during_month] # P(Qm = qm)
# 	return probability_of_repair

# def iterate_over_every_possible_removal_location_given_the_max_number_of_removals_to_iterate_up_to(num_engines_repaired_during_month_ATL, num_engines_repaired_during_month_MSP, probability_of_repair):
# 	'''
# 	given the max number of removals, iterate over all possible removal locations with the following constraints:
# 	- no more than 2 removals can happen outside of hubs
# 	- no more than 4 removals can happen at one hub
# 	'''
# 	for num in range(1, data.max_num_removals + 1):
# 		data.current_num_removals = num # set the current number of total removals
# 		# iterate over ever possible removal situation given the current number of total removals
# 		for possible_removal_situation in data.all_possible_removal_situations_by_number_of_removals[data.current_num_removals]:
# 			# find the probability to multiply to the cost of this removal situation
# 			probability_of_removals = find_probability_of_current_removal_situation(
# 				possible_removal_situation=possible_removal_situation)

# 			# find total cost of all actions taken this month based on the current removal situation
# 			total_cost_of_all_actions_in_month = get_total_cost_of_current_removal_situation()
			
# 			if data.current_total_broken > 0:
# 				probability_to_multiply = (probability_of_removals * probability_of_repair)
# 			else:
# 				probability_to_multiply = probability_of_removals

# 			# multiply the cost of this situation by the probability of it happening
# 			cost_of_possible_removal = (probability_to_multiply * total_cost_of_all_actions_in_month)
# 			# then add that value to the total expected cost for this spare engine placement
# 			data.total_cost_of_current_spare_placement += cost_of_possible_removal

# def find_probability_of_current_removal_situation(possible_removal_situation):
# 	probability_of_removals = -1 # P(Xs = xs)

# 	data.state_regions_of_removals_and_num_removals = {}
# 	data.state_regions_removals_and_removal_prob = {}

# 	for i in range(53):
# 		num_removals_in_state_region = int(possible_removal_situation[i])
# 		if at_least_one_removal_occurs_in_this_state_region(num_removals_in_state_region=num_removals_in_state_region):
# 			state_region_of_removal = data.hubs_and_state_regions[i] 
# 			probability = data.prob_of_num_removals_by_state_region[state_region_of_removal][num_removals_in_state_region] # prob of this number of removals happening in this state region
# 			data.state_regions_of_removals_and_num_removals[state_region_of_removal] = num_removals_in_state_region
# 			data.state_regions_removals_and_removal_prob[state_region_of_removal] = data.prob_of_num_removals_by_state_region[state_region_of_removal][1]
# 			if probability_of_removals == -1:
# 				probability_of_removals = probability
# 			else:
# 				probability_of_removals *= probability 
# 		else: # if no removals occur in this state region
# 			state_region = data.hubs_and_state_regions[i]
# 			probability = data.prob_of_num_removals_by_state_region[state_region][0]
# 			if probability_of_removals == -1:
# 				probability_of_removals = probability
# 			else:
# 				probability_of_removals *= probability 
	
# 	return probability_of_removals

# def at_least_one_removal_occurs_in_this_state_region(num_removals_in_state_region):
# 	return (num_removals_in_state_region > 0)

# def get_total_cost_of_current_removal_situation():
# 	data.there_are_removals_remaining = True 
# 	data.there_are_engines_remaining = True 
	
# 	if there_are_no_engines_available_at_beginning_of_month():
# 		data.there_are_engines_remaining = False
	
# 	# store data to change throughout iteration
# 	data.current_num_removals_left = data.current_num_removals
# 	data.num_engines_available_at_hubs_to_edit = copy.deepcopy(data.num_engines_available_at_hubs)
# 	data.state_regions_of_removals_and_num_removals_to_edit = copy.deepcopy(data.state_regions_of_removals_and_num_removals)
# 	data.state_regions_removals_and_removal_prob_to_edit = copy.deepcopy(data.state_regions_removals_and_removal_prob)
	
# 	total_cost_of_all_actions_in_month = 0 # sum up the total cost of all the actions taken in the month

# 	# while there are removals remaining to happen AND engines remaining to service those removals
# 	while data.there_are_removals_remaining and data.there_are_engines_remaining:
# 		cost_of_removal = cost_to_service_removal_from_hub_with_min_transport_cost()
# 		total_cost_of_all_actions_in_month += cost_of_removal
# 		reset_variables_to_reflect_action_for_this_removal()
	
# 	if data.there_are_removals_remaining:
# 		# if there are removals remaining but no engines are available to service it, incure an AOS cost for the remaining removals
# 		total_cost_of_all_actions_in_month += aos_cost_for_remaining_removals()
	
# 	return total_cost_of_all_actions_in_month

# def there_are_no_engines_available_at_beginning_of_month():
# 	# if there are no engines to place AND there are none that are being considered to be repaired during this month, then there are no engines remaining to allocate for any removals
# 	if (data.current_num_to_place == 0) and (data.current_total_repaired_during_month == 0):
# 		return True 
# 	return False

# def cost_to_service_removal_from_hub_with_min_transport_cost():
# 	removal_probabilities = list(data.state_regions_removals_and_removal_prob_to_edit.values()) # list all probabilities of the remaining removals
# 	removal_probability_regions = list(data.state_regions_removals_and_removal_prob_to_edit.keys()) # list all state regions where removals are left to occur

# 	# get state region of removal that has the highest probability of occurring
# 	data.current_state_region_of_removal_with_highest_prob = removal_probability_regions[removal_probabilities.index(max(removal_probabilities))]
	
# 	# reset data for this removal
# 	cost_to_service_removal_from_hub_with_min_transport_cost = -1
# 	data.hub_with_min_cost = ''

# 	for hub_of_engine, num_engines_at_hub in data.num_engines_available_at_hubs_to_edit.items(): # for every hub
# 		if num_engines_at_hub > 0: # if that hub has an engine available to service the removal
# 			# find the cost to transport that engine from the hub to the state region
# 			cost_to_transport = data.expected_cost_to_transport_engine_from_hub[data.current_state_region_of_removal_with_highest_prob][hub_of_engine]
			
# 			if min_cost_to_service_removal_needs_to_be_updated(current_min_cost=cost_to_service_removal_from_hub_with_min_transport_cost, current_cost_to_transport=cost_to_transport):
# 				cost_to_service_removal_from_hub_with_min_transport_cost = cost_to_transport
# 				data.hub_with_min_cost = hub_of_engine
	
# 	return cost_to_service_removal_from_hub_with_min_transport_cost

# def aos_cost_for_remaining_removals():
# 	return (data.current_num_removals_left * data.aos_cost)

# def min_cost_to_service_removal_needs_to_be_updated(current_min_cost, current_cost_to_transport):
# 	if (current_min_cost == -1) or (current_cost_to_transport < current_min_cost):
# 		return True
# 	return False

# def reset_variables_to_reflect_action_for_this_removal():
# 	if there_are_no_more_removals_remaining_to_occur_for_this_state_region():
# 		delete_state_region_from_list_of_removals_remaining_and_probabilities_of_removals_remainining()
# 	else: # if there is a removal for this state region that still needs to happen
# 		update_probability_associated_with_state_region_to_be_the_probability_associated_with_the_next_removal_that_will_occur()
# 	if there_are_no_removals_remaining_to_occur():
# 		data.there_are_removals_remaining = False
# 	if there_are_no_engines_available_to_service_removals():
# 		data.there_are_engines_remaining  = False

# def delete_state_region_from_list_of_removals_remaining_and_probabilities_of_removals_remainining():
# 	# delete state region from both dictionaries 
# 	del data.state_regions_of_removals_and_num_removals_to_edit[data.current_state_region_of_removal_with_highest_prob]
# 	del data.state_regions_removals_and_removal_prob_to_edit[data.current_state_region_of_removal_with_highest_prob]

# def update_probability_associated_with_state_region_to_be_the_probability_associated_with_the_next_removal_that_will_occur():
# 	# find the number of removals that have already occurred for this region
# 	removals_that_have_occurred_in_this_region = (data.state_regions_of_removals_and_num_removals[data.current_state_region_of_removal_with_highest_prob] - data.state_regions_of_removals_and_num_removals_to_edit[data.current_state_region_of_removal_with_highest_prob])
# 	# reset the probability associated with the next removal for this state region to match what number in sequence it will be
# 	data.state_regions_removals_and_removal_prob_to_edit[data.current_state_region_of_removal_with_highest_prob] = data.prob_of_num_removals_by_state_region[data.current_state_region_of_removal_with_highest_prob][removals_that_have_occurred_in_this_region + 1]

# def there_are_no_more_removals_remaining_to_occur_for_this_state_region():
# 	# remove removal from dictionary being iterated
# 	data.state_regions_of_removals_and_num_removals_to_edit[data.current_state_region_of_removal_with_highest_prob] -= 1
# 	# true if there are no more removals remaining to occur for this state region, false otherwise
# 	return (data.state_regions_of_removals_and_num_removals_to_edit[data.current_state_region_of_removal_with_highest_prob] == 0)

# def there_are_no_removals_remaining_to_occur():
# 	# subtract 1 removal from the total number of removals
# 	data.current_num_removals_left -= 1
# 	return (data.current_num_removals_left == 0) # true if there are NO removals remaining to occur in the current month, false otherwise

# def there_are_no_engines_available_to_service_removals():
# 	# remove this engine from dictionary being iterated because the engine has just been used for this removal
# 	data.num_engines_available_at_hubs_to_edit[data.hub_with_min_cost] -= 1
# 	# get number of engines still available
# 	engines_available = sum(data.num_engines_available_at_hubs_to_edit.values()) 
# 	return (engines_available == 0) # true if there are NO engines available to service removals, false otherwise

# def find_all_permutations(total_num_engines):
# 	perms_of_num_engines = get_all_permutations_of_spare_and_repair_situations(total_num_engines=total_num_engines)
# 	perms_of_engine_placement = get_all_permutations_of_engine_placement(total_num_engines=total_num_engines)
# 	perms_of_engine_placement_by_num_to_place = sort_perms_by_num_engines_to_place(perms_of_engine_placement=perms_of_engine_placement, total_num_engines=total_num_engines)
# 	writer_util.export_permutations(
# 		total_num_engines=total_num_engines, 
# 		perms_of_num_engines=perms_of_num_engines, 
# 		perms_of_engine_placement_by_num_to_place=perms_of_engine_placement_by_num_to_place)

# def get_all_permutations_of_spare_and_repair_situations(total_num_engines):
# 	list_of_possible_values_for_num_engines = []
# 	for i in range(total_num_engines + 1):
# 		list_of_possible_values_for_num_engines += [i, i, i]
	
# 	possible_perms_of_num_engines = [list(unique_perm) for unique_perm in (set(perm for perm in list(permutations(list_of_possible_values_for_num_engines, 3))))]
	
# 	perms_of_num_engines = []
# 	for i in possible_perms_of_num_engines:
# 		if sum(i) == total_num_engines:
# 			perms_of_num_engines.append(i)
	
# 	return perms_of_num_engines

# def get_all_permutations_of_engine_placement(total_num_engines):
# 	list_of_possible_values_for_engine_placement = []
# 	current_list = []
# 	for num in range(total_num_engines + 1):
# 		current_sum = 0
# 		for i in range(7):
# 			current_sum += num
			
# 			if current_sum <= total_num_engines:
# 				current_list.append(num)
# 			else:
# 				continue
		
# 		list_of_possible_values_for_engine_placement.append(current_list[:])
	
# 	perms_of_engine_placement_for_hubs = []
# 	for current_list in list_of_possible_values_for_engine_placement:
# 		current_placements = [list(unique_perm) for unique_perm in (set(perm for perm in list(permutations(current_list, 7))))]
# 		for unique_placement in current_placements:
			
# 			if sum(unique_placement) <= total_num_engines:
# 				if unique_placement not in perms_of_engine_placement_for_hubs:
# 					perms_of_engine_placement_for_hubs.append(unique_placement)
	
# 	return perms_of_engine_placement_for_hubs

# def sort_perms_by_num_engines_to_place(perms_of_engine_placement, total_num_engines):
# 	perms_of_engine_placement_by_num_to_place = {}
	
# 	for num in range(total_num_engines + 1):
# 		perms_of_engine_placement_by_num_to_place[num] = []
	
# 	for perm in perms_of_engine_placement:
# 		num_engines = sum(perm)
# 		perms_of_engine_placement_by_num_to_place[num_engines].append(perm)
	
# 	return perms_of_engine_placement_by_num_to_place

# def get_values_from_perm(perm):
# 	return perm[0], perm[1], perm[2]






	

