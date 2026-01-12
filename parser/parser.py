# parser/parser.py

class Parser:
    def __init__(self, text):
        self.text = text
        self.i = 0

    def peek(self, offset=0):
        """Look ahead at character without consuming."""
        pos = self.i + offset
        return self.text[pos] if pos < len(self.text) else None

    def consume(self):
        """Read and advance past current character."""
        ch = self.peek()
        self.i += 1
        return ch

    def skip_spaces(self):
        """Skip whitespace characters."""
        while self.peek() in [' ', '\n', '\t', '\r']:
            self.consume()

    def parse(self):
        """Main entry point for parsing."""
        self.skip_spaces()
        return self.parse_value()

    def parse_value(self):
        """Parse any value (object, list, or literal)."""
        self.skip_spaces()
        ch = self.peek()
        
        if ch is None:
            return None
        elif ch == '[':
            return self.parse_list()
        elif ch == '"':
            return self.parse_quoted_string()
        elif ch.isalpha() or ch == '_':
            # Could be an object with parens, or just a literal string
            # We need to look ahead to decide
            return self.parse_identifier_or_literal()
        else:
            # number or special case
            return self.parse_literal()

    def parse_identifier_or_literal(self):
        """Parse identifier - could be:
        - ClassName(...)  -> object
        - keyword=value   -> literal (handled elsewhere)
        - just_text       -> literal
        """
        start_pos = self.i
        name = ''
        
        # Read identifier characters
        while self.peek() and (self.peek().isalnum() or self.peek() in "_@."):
            name += self.consume()
        
        self.skip_spaces()
        
        if self.peek() == '(':
            # It's definitely an object: ClassName(...)
            self.consume()  # consume '('
            obj = {}
            
            while True:
                self.skip_spaces()
                if self.peek() == ')':
                    self.consume()
                    break
                
                # Parse key
                key = ''
                while self.peek() and (self.peek().isalnum() or self.peek() in "_"):
                    key += self.consume()
                
                self.skip_spaces()
                
                if self.peek() == '=':
                    self.consume()
                    value = self.parse_value()
                    obj[key] = value if value is not None else ""
                
                self.skip_spaces()
                
                if self.peek() == ',':
                    self.consume()
                elif self.peek() == ')':
                    pass
            
            return {name: obj}
        else:
            # It's a literal value that starts with letters/underscore
            # Reset and parse as full literal including what we already read
            self.i = start_pos
            return self.parse_literal()

    def parse_list(self):
        """Parse a list [...]. """
        items = []
        self.consume()  # consume '['
        
        while True:
            self.skip_spaces()
            
            if self.peek() == ']':
                self.consume()
                break
            
            value = self.parse_value()
            items.append(value)
            
            self.skip_spaces()
            
            if self.peek() == ',':
                self.consume()
            elif self.peek() != ']':
                # Separator expected
                pass
        
        return items

    def parse_quoted_string(self):
        """Parse a quoted string."""
        self.consume()  # consume opening quote
        s = ''
        while self.peek() and self.peek() != '"':
            s += self.consume()
        if self.peek() == '"':
            self.consume()  # consume closing quote
        return s

    def parse_literal(self):
        """Parse an unquoted literal value until we hit a delimiter."""
        s = ''
        
        # Read everything until we hit a hard delimiter
        while self.peek() and self.peek() not in [',', ')', ']']:
            s += self.consume()
        
        # The value might have trailing spaces, so we need to trim
        # but keep internal spaces (like "Tue Jan 06")
        s = s.rstrip()  # Only strip from right
        
        return self.cast(s) if s else ""

    def cast(self, s):
        """Convert string to appropriate type."""
        if not s:
            return ""
        if s == 'null':
            return None
        if s == 'true':
            return True
        if s == 'false':
            return False
        # Try to parse as integer
        try:
            if '.' not in s:  # Don't convert floats to int
                return int(s)
        except ValueError:
            pass
        return s
