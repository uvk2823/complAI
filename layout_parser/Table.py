class Table:

    def __init__(self, form_id: str, name: str, table_details: dict, cells: list = None):
        self.form_id = form_id
        self.name = name
        self.begin_label = table_details['begin_label']
        self.begin_label_occurrence = table_details.get('begin_label_occurrence', 1)
        self.end_label = table_details.get('end_label', None)
        self.end_label_occurrence = table_details.get('end_label_occurrence', 1)
        self.consistency = table_details.get('consistency', 'static')
        self.type = table_details['type']
        self.cells = cells

    def set_cells(self, cells: list):
        self.cells = cells

    def __str__(self):
        return f"form_id:'{self.form_id}', name:'{self.name}', type:'{self.type}', begin_label:'{self.begin_label}', end_label:'{self.end_label}', cells:'{self.cells}'"
