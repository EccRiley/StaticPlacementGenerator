from util import reader_util, writer_util, data_util, config
from services import data_generator, solve
import data
import pprint, logging

if __name__ == '__main__':
	data.init()

	# Import engine information
	data.engines_info = reader_util.import_engine_info(
		filepath='data_to_read/engine_info.csv',
		data_storage=data.engines_info)

	# Import removal information
	data.removals_info, data.aos_cost = reader_util.import_removal_info(
		filepath='data_to_read/removal_info.csv',
		removals_data_storage=data.removals_info,
		aos_cost_data_storage=data.aos_cost)

	data_util.validate_removal_and_engine_info()

	if config.first_run:
		logging.info("FIRST_RUN is set to TRUE. All files needed for future runs are going to be generated. This may take awhile.")
		data_generator.generate_all_possible_states()
		data_generator.generate_all_possible_num_broken_num_working()
		logging.info("All files needed for future runs have been created. Please set FIRST_RUN to FALSE for any future runs on this machine.")
	else: 
		# Import engine subtype data
		reader_util.import_engine_subtype_data()

		data_util.validate_engine_subtype_data()

		# Generate all possible removal situations if removal info has been updated
		for engine_subtype in data.engine_subtypes:
			if data.need_to_update_removal_info[engine_subtype]:
				data_generator.generate_all_possible_removal_situations(
					engine_subtype=engine_subtype)

		# Import all possible states
		data.all_possible_states = reader_util.import_all_possible_states(
			filepath='data_to_read/all_possible_states.csv', 
			data_storage=data.all_possible_states)

		# Import all possible number of engines broken and number of engines working
		data.all_possible_num_working_num_broken = reader_util.import_all_possible_num_working_num_broken(
			filepath='data_to_read/all_possible_num_working_num_broken.csv',
			data_storage=data.all_possible_num_working_num_broken)

		# Import all possible removal situations
		data.all_possible_removal_situations = reader_util.import_all_possible_removal_situations(
			data_storage=data.all_possible_removal_situations)

		for engine_subtype in data.engine_subtypes:
			solve.static_placement_generator(engine_subtype)












