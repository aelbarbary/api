class Scorer:
    def __init__(self, document):
        self.document = document
        self.score = 0

    def check_structure(self):
        headers = self.count_headers()
        sections = self.count_sections()
        print(f"Headers: {headers}, Sections: {sections}")
        # Criteria for scoring structure
        if headers >= 3 and sections >= 2:
            self.score += 15  # Full points for structure
        elif headers >= 2 and sections >= 1:
            self.score += 10  # Partial points for structure
        elif headers == 1 and sections == 1:
            self.score += 5   # Minimal structure
        else:
            self.score += 0   # No structure

    def count_headers(self):
        # Count headers based on specific markers (e.g., # for Markdown)
        return self.document.count("#")  # Example for Markdown headers

    def count_sections(self):
        # Count sections based on double line breaks
        return self.document.count("\n\n")  # Example for section breaks

    def evaluate(self):
        self.check_structure()
        return self.score  # Return the score instead of printing
