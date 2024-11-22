import json
from configparser import ConfigParser

from layout_parser.table_merger.TableMerger import TableMerger

table_merger = TableMerger()

with open('pas_3_table_cells.json', 'r') as file:
    visual_cells = json.load(file)

merge_config_parser = ConfigParser()
merge_config_parser.read('../../configs/pas_3/table_merge.ini')

merge_config = dict(
    map(lambda section: (section, dict(merge_config_parser.items(section))), merge_config_parser.sections()))

semantic_table_cells = table_merger.merge('FORMNO.PAS-3', visual_cells, merge_config)
for table_name, table_details in semantic_table_cells.items():
    print(f'Table Name - {table_name}')
    print(f'Table details - {table_details}')
# print(semantic_table_cells)
