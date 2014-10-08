require_relative 'StatementLexer'
require_relative 'StatementParser'

$lexer_cache = {}
$expression_cache = {}
$debug = false

class StringFormatter

  def initialize(format_string)
    @format_string = format_string
  end

  def pre_compute
    create_expressions
    self
  end

  def evaluate(arguments = nil)
    argument_mapper = ArgumentMap.new(arguments)
    formatted_value = ''
    @expressions.each do |expression|
      formatted_value += expression.evaluate(argument_mapper)
    end
    formatted_value
  end

  class << self

    def find_or_create(format_string, arguments)
      StringFormatter.new(format_string).pre_compute.evaluate(arguments)
    end

  end

  private

  def create_expressions
    if $expression_cache[@format_string]
      @expressions = $expression_cache[@format_string]
    else
      @expressions = []

      index = 0
      str = @format_string
      loop do
        data = str.match(/{{(?<statement>([^}]||}(?!}))*)}}/)
        if data
          index += data.begin(:statement)
          @expressions << Expression.new(data.pre_match, data[:statement], index)
          str = data.post_match
        else
          @expressions << Expression.new(str, nil, index)
          break
        end
      end

      $expression_cache[@format_string] = @expressions
    end
  end

end

class ArgumentMap

  def initialize(arguments)
    @arguments = arguments
  end

  def apply(value)
    return value unless value
    return value unless @arguments
    @arguments.each_with_index do |argument, index|
      value = value.to_s.gsub(/\$#{index + 1}/, argument.to_s)
    end
    value
  end

  def get_value(argument)
    index = argument[1..-1].to_i - 1
    $stderr.puts "parse error #{argument} not found" if $debug and @arguments.size <= index
    @arguments[index]
  end

end

class Expression

  def initialize(pre_match, statement, index)
    @pre_match = pre_match
    @statement = statement
    @index = index
  end

  def evaluate(argument_mapper)
    $argument_mapper = argument_mapper

    parsed_statement = @statement

    unless parsed_statement.nil? || parsed_statement.strip.nil?
      $stderr.puts "parse #{@index}:#{@index + parsed_statement.size}" if $debug

      lexer = create_or_find_lexer(parsed_statement)
      parser = Statement::Parser.new(lexer)
      parsed_statement = parser.program.value
    end

    "#{argument_mapper.apply(@pre_match)}#{argument_mapper.apply(parsed_statement)}"
  end

  private

  def create_or_find_lexer(statement)
    if $lexer_cache[statement]
      lexer = $lexer_cache[statement]
    else
      lexer = Statement::Lexer.new(statement)
      $lexer_cache[statement] = lexer
    end
    lexer.reset
    lexer
  end

end
