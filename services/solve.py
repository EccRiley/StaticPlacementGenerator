from util import reader_util, writer_util, data_util
from itertools import permutations
import data
import copy, logging, pprint

def static_placement_generator(engine_subtype):
	num_engines = data.engines_info[engine_subtype]
	possible_num_broken_num_working = data.all_possible_num_working_num_broken[num_engines]
	best_placements = {}
	logging.info("Finding best static placement for all scenarios for " + engine_subtype)
	for current_num_working_num_broken in possible_num_broken_num_working:
		best_placements[str(current_num_working_num_broken)] = {'PLACEMENT': [], 'COST': -1}
		num_working = current_num_working_num_broken[0]
		min_cost = -1
		best_placement = []
		logging.info("Current situation: " + str(num_working) + " engine(s) to place, " + str(current_num_working_num_broken[1]) + " engine(s) broken at ATL, and " + str(current_num_working_num_broken[2]) + " engine(s) broken at MSP.")
		for current_state in data.all_possible_states[num_working]:
			solver = CostCalculator(engine_subtype, current_state, current_num_working_num_broken)
			cost = solver.get_cost()
			if (min_cost == -1) or (cost < min_cost):
				min_cost = cost 
				best_placement = current_state
				logging.info("New best placement found! Placement: " + str(best_placement) + ", cost: " + str(min_cost))
		best_placements[str(current_num_working_num_broken)]['PLACEMENT'] = best_placement
		best_placements[str(current_num_working_num_broken)]['COST'] = min_cost
		logging.info("Best placement found for situation: " + str(current_num_working_num_broken))
		logging.info("Placement: " + str(best_placement) + ", cost: " + str(min_cost))
	writer_util.export_best_placements(engine_subtype, best_placements)


class CostCalculator():

	def __init__(self, engine_subtype, current_state, current_num_working_num_broken):
		self.engine_subtype = engine_subtype
		self.current_state = current_state

		self.aos_cost = data.aos_cost[self.engine_subtype]
		self.probability_of_repair = data.probability_of_num_repair_given_num_broken[self.engine_subtype]
		self.expected_transport_cost = data.expected_transport_cost[self.engine_subtype]
		self.num_working_engines = current_num_working_num_broken[0]
		self.num_broken_engines_ATL = current_num_working_num_broken[1]
		self.num_broken_engines_MSP = current_num_working_num_broken[2]
		self.num_broken_engines_total = (self.num_broken_engines_ATL + self.num_broken_engines_MSP)
		self.all_possible_removal_situations = data.all_possible_removal_situations[self.engine_subtype]
		self.prob_of_num_removals_by_state_region = data.probabilities_of_num_removals_in_each_state_region[self.engine_subtype]

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
				probability = self.prob_of_num_removals_by_state_region[state_region][0]
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




	

