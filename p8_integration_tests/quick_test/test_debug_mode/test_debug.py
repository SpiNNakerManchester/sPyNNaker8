import os
import unittest
import pacman.operations.algorithm_reports.reports as reports_names
from pacman.operations.algorithm_reports.network_specification import \
    NetworkSpecification
from spinn_front_end_common.utilities import globals_variables
from spinn_front_end_common.utilities.report_functions.\
    routing_table_from_machine_report import _FOLDER_NAME as \
    routing_tables_from_machine_report
from spinn_front_end_common.utilities.report_functions.board_chip_report \
    import BoardChipReport
# from spinn_front_end_common.utility_models.\
#     data_speed_up_packet_gatherer_machine_vertex import \
#     DataSpeedUpPacketGatherMachineVertex
from p8_integration_tests.base_test_case import BaseTestCase
import spynnaker8 as sim


class TestDebug(BaseTestCase):
    """
    that it does not crash in debug mode. All reports on.
    """
    def test_debug(self):
        reports = [
            # write_energy_report
            "Detailed_energy_report.rpt",
            "energy_summary_report.rpt",
            # write_text_specs = False
            "data_spec_text_files",
            # write_router_reports
            reports_names._ROUTING_FILENAME,
            # write_partitioner_reports
            reports_names._PARTITIONING_FILENAME,
            # write_application_graph_placer_report
            reports_names._PLACEMENT_VTX_GRAPH_FILENAME,
            reports_names._PLACEMENT_CORE_GRAPH_FILENAME,
            reports_names._SDRAM_FILENAME,
            # write_machine_graph_placer_report
            reports_names._PLACEMENT_VTX_SIMPLE_FILENAME,
            reports_names._PLACEMENT_CORE_SIMPLE_FILENAME,
            # repeats reports_names._SDRAM_FILENAME,
            # write_router_info_report
            reports_names._VIRTKEY_FILENAME,
            # write_routing_table_reports
            reports_names._ROUTING_TABLE_DIR,
            reports_names._C_ROUTING_TABLE_DIR,
            reports_names._COMPARED_FILENAME,
            # write_routing_compression_checker_report
            "routing_compression_checker_report.rpt",
            # write_routing_tables_from_machine_report
            routing_tables_from_machine_report,
            # write_memory_map_report
            # ??? used by MachineExecuteDataSpecification but not called ???
            # write_network_specification_report
            NetworkSpecification._FILENAME,
            # write_provenance_data
            "provenance_data",
            # write_tag_allocation_reports
            reports_names._TAGS_FILENAME,
            # write_algorithm_timings
            # "provenance_data/pacman.xml"  = different test
            # write_board_chip_report
            BoardChipReport.AREA_CODE_REPORT_NAME,
            # write_data_speed_up_report
            # Appears to only work if you call get_data ???
            # DataSpeedUpPacketGatherMachineVertex.REPORT_NAME
            ]
        sim.setup(1.0)
        pop = sim.Population(1, sim.IF_curr_exp, {}, label="pop")
        inp = sim.Population(1, sim.SpikeSourceArray(
            spike_times=[0]), label="input")
        sim.Projection(inp, pop, sim.OneToOneConnector(),
                     synapse_type=sim.StaticSynapse(weight=5))
        sim.run(10)
        report_directory = globals_variables.get_simulator()._report_default_directory
        sim.end()

        found = os.listdir(report_directory)
        print(found)
        for report in reports:
            self.assertIn(report, found)


if __name__ == '__main__':
    unittest.main()
