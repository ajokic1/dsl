class Printer:
    def __init__(self, config):
        self.result = ""
        self._indent_level = 0
        self._tab_width = config.rules['tab_width']
        self._use_spaces = config.rules['use_spaces']

    def new_line_indent(self, num_tabs=1):
        self.append("\n" + self._spaces(num_tabs))

    def append(self, string):
        self.result += str(string)

    def increase_indent(self):
        self._indent_level += 1

    def decrease_indent(self):
        self._indent_level -= 1

    def write_to_file(self, filename):
        file = open(filename, 'w')
        file.write(self.result)
        file.close()

    def _spaces(self, num_tabs):
        if self._use_spaces:
            return " " * (self._indent_level - 1 + num_tabs) * self._tab_width
        else:
            return "\t" * (self._indent_level - 1 + num_tabs)