from layout_parser.Table import Table


class TableMerger:
    """
    A class to merge visual table cells into semantic cells based on a merge configuration.
    """

    def merge(self, document_type: str, visual_cells: list, merge_config: dict) -> dict:
        """
        Merge visual table cells based on the provided merge configuration.

        Args:
            document_type (str): The document identifier.
            visual_cells (list): A list of visual table cells.
            merge_config (dict): The merge configuration dictionary.

        Returns:
            dict: A dictionary of merged tables.
        """
        detailed_config = self._expand_merge_config(visual_cells, merge_config)
        tables = {}

        for table_name, table_details in detailed_config.items():
            table = Table(document_type, table_name, table_details)

            table_begin_index = self._get_table_index(
                visual_cells, table.begin_label, table.begin_label_occurrence
            )

            if table.end_label:
                table_end_index = self._get_table_index(
                    visual_cells, table.end_label, table.end_label_occurrence
                ) - 1
            else:
                table_end_index = visual_cells[-1]['table_index']

            semantic_table_data = [] if table_begin_index < 0 or table_end_index < 0 else [
                cell for cell in visual_cells
                if table_begin_index <= cell['table_index'] <= table_end_index]

            if semantic_table_data:
                semantic_table_data = self._update_cell_data(semantic_table_data)

            table.set_cells(semantic_table_data)
            tables[table_name] = table

        return tables

    def _expand_merge_config(self, visual_cells: list, merge_config: dict) -> dict:
        """
        Expand the merge configuration for dynamic tables.

        Args:
            visual_cells (list): A list of visual table cells.
            merge_config (dict): The merge configuration dictionary.

        Returns:
            dict: An expanded merge configuration dictionary.
        """
        detailed_config = {}

        for table_name, table_details in merge_config.items():
            if 'consistency' in table_details:
                dynamic_details = self._get_dynamic_table_details(
                    visual_cells, table_name, table_details
                )
                detailed_config.update(dynamic_details)
            else:
                detailed_config[table_name] = table_details

        return detailed_config

    def _get_dynamic_table_details(
            self, visual_cells: list, table_name: str, table_details: dict
    ) -> dict:
        """
        Generate dynamic table details based on the number of occurrences.

        Args:
            visual_cells (list): A list of visual table cells.
            table_name (str): The base name of the table.
            table_details (dict): The base table details.

        Returns:
            dict: A dictionary containing dynamic table details.
        """
        label = table_details['consistency_label']
        num_tables = sum(1 for cell in visual_cells if label in cell['text'])
        dynamic_details = {}

        for index in range(1, num_tables + 1):
            indexed_table_name = f"{table_name}_{index}"
            dynamic_details[indexed_table_name] = {
                'begin_label': table_details['begin_label'],
                'begin_label_occurrence': index,
                'type': table_details['type'],
                'consistency': table_details['consistency'],
            }

            if index == num_tables:
                dynamic_details[indexed_table_name]['end_label'] = table_details.get('end_label')
                dynamic_details[indexed_table_name]['end_label_occurrence'] = table_details.get(
                    'end_label_occurrence', 1
                )
            else:
                dynamic_details[indexed_table_name]['end_label'] = table_details['begin_label']
                dynamic_details[indexed_table_name]['end_label_occurrence'] = index + 1

        return dynamic_details

    def _get_table_index(self, cells: list, label: str, occurrence: int) -> int:
        """
        Get the index of the table based on the label occurrence.

        Args:
            cells (list): A list of table cells.
            label (str): The label to search for.
            occurrence (int): The occurrence number of the label.

        Returns:
            int: The table index if found; otherwise, None.
        """
        matched_cells = [cell for cell in cells if label in cell['text']]
        index = occurrence - 1

        if index < len(matched_cells):
            return matched_cells[index]['table_index']
        else:
            return -1

    def _update_cell_data(self, table_data: list) -> list:
        """
        Update cell data by adjusting row counts.

        Args:
            table_data (list): The list of table data to update.

        Returns:
            list: The updated table data.
        """
        filtered_cells = self._filter_cells(table_data)
        row_count = 0

        for cell in filtered_cells:
            if cell['cell_ids'][0][1] == 1:
                row_count += 1
            cell['cell_ids'] = [row_count, cell['cell_ids'][0][1]]

        return filtered_cells

    def _filter_cells(self, table_data: list) -> list:
        """
        Filter cells to include only those with a consistent number of columns.

        Args:
            table_data (list): The list of table data to filter.

        Returns:
            list: The filtered list of table cells.
        """
        grouped_cells = {}
        first_table_index = table_data[0]['table_index']

        # Group cells by table index
        for cell in table_data:
            table_index = cell['table_index']
            grouped_cells.setdefault(table_index, []).append(cell)

        # Determine the expected number of columns
        first_group = grouped_cells[first_table_index]
        expected_columns = first_group[-1]['cell_ids'][0][1]

        # Collect cells from groups matching the expected number of columns
        filtered_cells = []
        for group in grouped_cells.values():
            if group[-1]['cell_ids'][0][1] == expected_columns:
                filtered_cells.extend(group)

        return filtered_cells
