import json
from configparser import ConfigParser

from layout_parser.table_merger.TableMerger import TableMerger

table_merger = TableMerger()

with open('pas_3_table_cells.json', 'r') as file:
    visual_cells = json.load(file)

merge_config = ConfigParser()
merge_config.read('../../configs/pas_3/table_merge.ini')

semantic_table_cells = table_merger.merge('FORMNO.PAS-3', visual_cells, merge_config)
print(semantic_table_cells)
