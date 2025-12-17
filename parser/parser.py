# parser/parser.py

class Parser:
    def __init__(self, text):
        self.text = text
        self.i = 0

    def peek(self):
        return self.text[self.i] if self.i < len(self.text) else None

    def consume(self):
        ch = self.peek()
        self.i += 1
        return ch

    def skip_spaces(self):
        while self.peek() in [' ', '\n', '\t', '\r']:
            self.consume()

    def parse(self):
        self.skip_spaces()
        return self.parse_value()

    def parse_value(self):
        self.skip_spaces()
        ch = self.peek()
        if ch is None:
            return None
        if ch.isalpha() or ch == '_':
            return self.parse_object_or_literal()
        elif ch == '[':
            return self.parse_list()
        else:
            return self.parse_literal()

    def parse_list(self):
        items = []
        self.consume()  # [
        while True:
            self.skip_spaces()
            if self.peek() == ']':
                self.consume()
                break
            items.append(self.parse_value())
            self.skip_spaces()
            if self.peek() == ',':
                self.consume()
        return items

    def parse_object_or_literal(self):
        name = self.parse_identifier()
        self.skip_spaces()
        if self.peek() == '(':
            self.consume()
            obj = {}
            while True:
                self.skip_spaces()
                if self.peek() == ')':
                    self.consume()
                    break
                key = self.parse_identifier()
                self.skip_spaces()
                if self.peek() == '=':
                    self.consume()
                    value = self.parse_value()
                    if value is None:
                        value = ""
                    obj[key] = value
                self.skip_spaces()
                if self.peek() == ',':
                    self.consume()
            return {name: obj}
        else:
            return self.cast(name)

    def parse_identifier(self):
        s = ''
        while self.peek() and (self.peek().isalnum() or self.peek() in "_@."):
            s += self.consume()
        return s

    def parse_literal(self):
        s = ''
        while self.peek() and self.peek() not in [',', ')', ']']:
            s += self.consume()
        s = s.strip()
        return self.cast(s) if s else ""

    def cast(self, s):
        if s == 'null':
            return None
        if s == 'true':
            return True
        if s == 'false':
            return False
        if s.isdigit():
            return int(s)
        return s
