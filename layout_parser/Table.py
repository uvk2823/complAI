class Table:
    """
    A class representing a table with associated metadata and cells.
    """

    def __init__(
            self, document_type: str, name: str, table_details: dict, cells: list = None
    ):
        """
        Initialize a Table instance.

        Args:
            document_type (str): The form identifier.
            name (str): The table name.
            table_details (dict): The table details.
            cells (list, optional): The list of cells associated with the table.
        """
        self.document_type = document_type
        self.name = name
        self.begin_label = table_details['begin_label']
        self.begin_label_occurrence = table_details.get('begin_label_occurrence', 1)
        self.end_label = table_details.get('end_label')
        self.end_label_occurrence = table_details.get('end_label_occurrence', 1)
        self.consistency = table_details.get('consistency', 'static')
        self.type = table_details['type']
        self.cells = cells or []

    def set_cells(self, cells: list):
        """
        Set the cells associated with the table.

        Args:
            cells (list): The list of cells to associate with the table.
        """
        self.cells = cells

    def __str__(self):
        """
        Return a string representation of the Table.

        Returns:
            str: A string describing the table.
        """
        return (
            f"Table(document_type='{self.document_type}', name='{self.name}', type='{self.type}', "
            f"begin_label='{self.begin_label}', end_label='{self.end_label}', "
            f"cells_count={len(self.cells)})"
        )
