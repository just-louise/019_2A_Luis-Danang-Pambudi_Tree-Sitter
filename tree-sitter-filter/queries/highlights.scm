["and" "or" "not" "in" "contains"] @keyword
["=" "!=" ">" "<" ">=" "<="] @operator
["(" ")"] @punctuation.bracket
"," @punctuation.delimiter

(string) @string
(number) @number
(boolean) @constant.builtin

(comparison
  field: (identifier) @property)

(in_expression
  field: (identifier) @property)
