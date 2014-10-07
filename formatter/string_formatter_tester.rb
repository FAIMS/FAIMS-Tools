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

db.create_function('format', -1) do |func, *args|
  if args.empty? or args.size < 1
    func.result = nil
  else
    func.result = StringFormatter.new(args[0]).pre_compute.evaluate(args[1..-1])
  end
end


File.open(sql_file, 'r') do |file|
  sql = ""
  file.readlines.each do |line|
    sql += line.gsub(/--.*/, '')
    if line =~ /;/
      begin
      sql = sql.gsub(/(\n|\s|\t)+/, ' ').strip
      puts db.execute(sql) unless sql.nil? or sql == ''
      sql = ""
      rescue Exception => e
        puts e
        sql = ""
      end
    end
  end
end

