import pprint
import data

def validate_removal_and_engine_info():
	for engine_subtype in data.engine_subtypes:
		assert (engine_subtype in data.aos_cost), "No AOS cost was provided for " + engine_subtype + " in the removal_info file. Please provide ALL info for this engine subtype in the removal_info file."
		assert (data.aos_cost[engine_subtype] > 0), "AOS cost for " + engine_subtype + " is not set to a positive value. Please provide a positive value indicating the expected AOS cost for this engine type in the removal_info file."
		assert (engine_subtype in data.engines_info), "No engine data was provided for " + engine_subtype + " in the engine_info file. Please provide ALL info for this engine subtype in the engine_info file."
		assert (data.engines_info[engine_subtype] <= 5), "The program is limited to running only for engine types with 5 or less total engines. The " + engine_subtype + " has more than 5 engines."

def validate_engine_subtype_data():
	pass