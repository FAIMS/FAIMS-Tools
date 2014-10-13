#!/home/faims/.rbenv/shims/ruby

require 'sqlite3'
require 'antlr3'
require_relative 'string_formatter'

def spatialite_library
  return 'libspatialite.dylib' if (/darwin/ =~ RUBY_PLATFORM) != nil
  return 'libspatialite.so'
end

db_file = ARGV.shift
sql_file = ARGV.shift

db = SQLite3::Database.new(db_file)
db.enable_load_extension(true)
db.execute("select load_extension('#{spatialite_library}')")

db.create_function('debug_format', -1) do |func, *args|
  $debug = true
  func.result = 'Format debugging on'
end

db.create_function('format', -1) do |func, *args|
  if args.empty? or args.size < 1
    func.result = nil
  else
    if args[0].nil?
      func.result = args[1..-1].select { |arg| !arg.nil? }.join(', ')
    else
      func.result = StringFormatter.new(args[0]).pre_compute.evaluate(args[1..-1])
    end
  end
end


File.open(sql_file, 'r') do |file|
  sql = ""
  file.readlines.each do |line|
    sql += line.gsub(/--.*/, '')
    if line =~ /;/
      begin
      sql = sql.gsub(/(\n|\s|\t)+/, ' ').strip
      unless sql.nil? or sql == ''
        result = db.execute(sql) 
        result.each do |r|
          puts r.join("\t")
        end
        puts ""
      end
      sql = ""
      rescue Exception => e
        $stderr.puts sql
        $stderr.puts e
        puts sql
        puts e
        sql = ""
      end
    end
  end
end

