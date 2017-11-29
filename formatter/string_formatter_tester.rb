#!/home/faims/.rbenv/shims/ruby

require 'sqlite3'
require 'antlr3'
require 'table_print'
require_relative 'string_formatter'
require 'arrayfields'

def spatialite_library
  return 'libspatialite.dylib' if (/darwin/ =~ RUBY_PLATFORM) != nil
  if `. /etc/lsb-release 2>/dev/null ; echo $DISTRIB_CODENAME`.strip == 'trusty'
    return 'libspatialite.so'
  else
    return 'mod_spatialite.so'
  end


end



class Hash
  # Returns a hash that includes everything but the given keys.
  #   hash = { a: true, b: false, c: nil}
  #   hash.except(:c) # => { a: true, b: false}
  #   hash # => { a: true, b: false, c: nil}
  #
  # This is useful for limiting a set of parameters to everything but a few known toggles:
  #   @person.update(params[:person].except(:admin))
  def except(*keys)
    dup.except!(*keys)
  end

  # Replaces the hash without the given keys.
  #   hash = { a: true, b: false, c: nil}
  #   hash.except!(:c) # => { a: true, b: false}
  #   hash # => { a: true, b: false }
  def except!(*keys)
    keys.each { |key| delete(key) }
    self
  end
end

db_file = ARGV.shift
sql_file = ARGV.shift

db = SQLite3::Database.new(db_file)
db.enable_load_extension(true)
db.execute("select load_extension('#{spatialite_library}')")
db.results_as_hash = true

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
        
        resultHash = []
        result.each do |r|
        #  puts r.join("\t")
          #puts r
          for i in 0..r.length/2-1
            r.delete(i)
          end

          
          resultHash << r
        end
        puts sql
        tp resultHash
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

