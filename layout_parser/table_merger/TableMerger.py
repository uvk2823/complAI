from pprint import pprint

from layout_parser.Table import Table


class TableMerger:

    def merge(self, form_id: str, visual_table_cells: list, merge_config: dict):
        verbose_merge_config = self.detail_merge_config(visual_table_cells, merge_config)
        tables = {}
        for table_name, table_details in verbose_merge_config.items():
            table = Table(form_id, table_name, table_details)
            table_begin_index = self.get_table_index(visual_table_cells, table.begin_label,
                                                     table.begin_label_occurrence)
            table_end_index = self.get_table_index(visual_table_cells, table.end_label,
                                                   table.end_label_occurrence) - 1 if hasattr(table,
                                                                                              'end_label') and table.end_label is not None else \
                visual_table_cells[-1]['table_index']
            actual_table_data = list(
                filter(lambda data: table_begin_index <= data['table_index'] <= table_end_index, visual_table_cells))
            actual_table_data = self.update_cell_data(actual_table_data) if actual_table_data else actual_table_data
            table.set_cells(actual_table_data)
            tables[table_name] = table
        return tables

    def detail_merge_config(self, visual_table_cells: list, merge_config: dict):
        verbose_merge_config = {}
        for table_name, table_details in merge_config.items():
            modified_table_details = self.get_dynamic_table_details(visual_table_cells, table_name,
                                                                    table_details) if "consistency" in table_details.keys() else {
                table_name: table_details}
            verbose_merge_config.update(modified_table_details)
        return verbose_merge_config

    def get_dynamic_table_details(self, visual_table_cells: list, table_name: str, table_details: dict):
        number_of_tables = sum(1 for data in visual_table_cells if table_details['consistency_label'] in data['text'])
        dynamic_table_details = {}
        for table_index in range(1, number_of_tables + 1):
            table_name_with_index = f'{table_name}_{table_index}'
            dynamic_table_details[table_name_with_index] = {
                'begin_label': table_details['begin_label'],
                'begin_label_occurrence': table_index,
                'type': table_details['type'],
                'consistency': table_details['consistency']
            }
            if table_index == number_of_tables:
                dynamic_table_details[table_name_with_index]['end_label'] = table_details['end_label']
            else:
                dynamic_table_details[table_name_with_index]['end_label'] = table_details['begin_label']
                dynamic_table_details[table_name_with_index]['end_label_occurrence'] = table_index + 1
        return dynamic_table_details

    def get_table_index(self, cells: list, label: str, label_occurrence: int):
        matched_labels = [table_data for table_data in cells if label in table_data['text']]
        return matched_labels[label_occurrence - 1]['table_index'] if label_occurrence - 1 < len(
            matched_labels) else None

    def update_cell_data(self, actual_table_data):
        filtered_cells = self.get_filtered_cells(actual_table_data)
        row_count = 0
        for data in filtered_cells:
            if data['cell_ids'][0][1] == 1:
                row_count += 1
            data['cell_ids'] = [row_count, data['cell_ids'][0][1]]
        return filtered_cells

    def get_filtered_cells(self, actual_table_data):
        table_cells = []
        first_table_index = actual_table_data[0]['table_index']
        table_data_group_by_table_index = {}

        for data in actual_table_data:
            table_index = data['table_index']
            if table_index not in table_data_group_by_table_index:
                table_data_group_by_table_index[table_index] = []
            table_data_group_by_table_index[table_index].append(data)
        no_of_columns = table_data_group_by_table_index[first_table_index][-1]['cell_ids'][0][1]

        for table_index, data in table_data_group_by_table_index.items():
            if data[-1]['cell_ids'][0][1] == no_of_columns:
                table_cells.extend(data)

        return table_cells
