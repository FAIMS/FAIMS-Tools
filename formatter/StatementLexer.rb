#!/usr/bin/env ruby
#
# Statement.g
# --
# Generated using ANTLR version: 3.5
# Ruby runtime library version: 1.10.0
# Input grammar file: Statement.g
# Generated at: 2014-10-07 12:11:50
#

# ~~~> start load path setup
this_directory = File.expand_path( File.dirname( __FILE__ ) )
$LOAD_PATH.unshift( this_directory ) unless $LOAD_PATH.include?( this_directory )

antlr_load_failed = proc do
  load_path = $LOAD_PATH.map { |dir| '  - ' << dir }.join( $/ )
  raise LoadError, <<-END.strip!

Failed to load the ANTLR3 runtime library (version 1.10.0):

Ensure the library has been installed on your system and is available
on the load path. If rubygems is available on your system, this can
be done with the command:

  gem install antlr3

Current load path:
#{ load_path }

  END
end

defined?( ANTLR3 ) or begin

  # 1: try to load the ruby antlr3 runtime library from the system path
  require 'antlr3'

rescue LoadError

  # 2: try to load rubygems if it isn't already loaded
  defined?( Gem ) or begin
    require 'rubygems'
  rescue LoadError
    antlr_load_failed.call
  end

  # 3: try to activate the antlr3 gem
  begin
    defined?( gem ) and gem( 'antlr3', '~> 1.10.0' )
  rescue Gem::LoadError
    antlr_load_failed.call
  end

  require 'antlr3'

end
# <~~~ end load path setup

module Statement
  # TokenData defines all of the token type integer values
  # as constants, which will be included in all
  # ANTLR-generated recognizers.
  const_defined?( :TokenData ) or TokenData = ANTLR3::TokenScheme.new

  module TokenData

    # define the token constants
    define_tokens( :EOF => -1, :T__11 => 11, :T__12 => 12, :T__13 => 13, 
                   :T__14 => 14, :T__15 => 15, :T__16 => 16, :T__17 => 17, 
                   :T__18 => 18, :T__19 => 19, :T__20 => 20, :T__21 => 21, 
                   :T__22 => 22, :T__23 => 23, :T__24 => 24, :T__25 => 25, 
                   :T__26 => 26, :T__27 => 27, :T__28 => 28, :DIGIT => 4, 
                   :INT => 5, :NEWLINE => 6, :NUMBER => 7, :SPACE => 8, 
                   :STRING => 9, :VARIABLE => 10 )

  end


  class Lexer < ANTLR3::Lexer
    @grammar_home = Statement
    include TokenData

    begin
      generated_using( "Statement.g", "3.5", "1.10.0" )
    rescue NoMethodError => error
      # ignore
    end

    RULE_NAMES   = [ "T__11", "T__12", "T__13", "T__14", "T__15", "T__16", 
                     "T__17", "T__18", "T__19", "T__20", "T__21", "T__22", 
                     "T__23", "T__24", "T__25", "T__26", "T__27", "T__28", 
                     "NEWLINE", "SPACE", "STRING", "NUMBER", "INT", "VARIABLE", 
                     "DIGIT" ].freeze
    RULE_METHODS = [ :t__11!, :t__12!, :t__13!, :t__14!, :t__15!, :t__16!, 
                     :t__17!, :t__18!, :t__19!, :t__20!, :t__21!, :t__22!, 
                     :t__23!, :t__24!, :t__25!, :t__26!, :t__27!, :t__28!, 
                     :newline!, :space!, :string!, :number!, :int!, :variable!, 
                     :digit! ].freeze

    def initialize( input=nil, options = {} )
      super( input, options )
    end


    # - - - - - - - - - - - lexer rules - - - - - - - - - - - -
    # lexer rule t__11! (T__11)
    # (in Statement.g)
    def t__11!
      # -> uncomment the next line to manually enable rule tracing
      # trace_in( __method__, 1 )



      type = T__11
      channel = ANTLR3::DEFAULT_CHANNEL
    # - - - - label initialization - - - -


      # - - - - main rule block - - - -
      # at line 7:9: ')'
      match( 0x29 )


      @state.type = type
      @state.channel = channel
    ensure
      # -> uncomment the next line to manually enable rule tracing
      # trace_out( __method__, 1 )


    end

    # lexer rule t__12! (T__12)
    # (in Statement.g)
    def t__12!
      # -> uncomment the next line to manually enable rule tracing
      # trace_in( __method__, 2 )



      type = T__12
      channel = ANTLR3::DEFAULT_CHANNEL
    # - - - - label initialization - - - -


      # - - - - main rule block - - - -
      # at line 8:9: ','
      match( 0x2c )


      @state.type = type
      @state.channel = channel
    ensure
      # -> uncomment the next line to manually enable rule tracing
      # trace_out( __method__, 2 )


    end

    # lexer rule t__13! (T__13)
    # (in Statement.g)
    def t__13!
      # -> uncomment the next line to manually enable rule tracing
      # trace_in( __method__, 3 )



      type = T__13
      channel = ANTLR3::DEFAULT_CHANNEL
    # - - - - label initialization - - - -


      # - - - - main rule block - - - -
      # at line 9:9: '['
      match( 0x5b )


      @state.type = type
      @state.channel = channel
    ensure
      # -> uncomment the next line to manually enable rule tracing
      # trace_out( __method__, 3 )


    end

    # lexer rule t__14! (T__14)
    # (in Statement.g)
    def t__14!
      # -> uncomment the next line to manually enable rule tracing
      # trace_in( __method__, 4 )



      type = T__14
      channel = ANTLR3::DEFAULT_CHANNEL
    # - - - - label initialization - - - -


      # - - - - main rule block - - - -
      # at line 10:9: ']'
      match( 0x5d )


      @state.type = type
      @state.channel = channel
    ensure
      # -> uncomment the next line to manually enable rule tracing
      # trace_out( __method__, 4 )


    end

    # lexer rule t__15! (T__15)
    # (in Statement.g)
    def t__15!
      # -> uncomment the next line to manually enable rule tracing
      # trace_in( __method__, 5 )



      type = T__15
      channel = ANTLR3::DEFAULT_CHANNEL
    # - - - - label initialization - - - -


      # - - - - main rule block - - - -
      # at line 11:9: 'and('
      match( "and(" )



      @state.type = type
      @state.channel = channel
    ensure
      # -> uncomment the next line to manually enable rule tracing
      # trace_out( __method__, 5 )


    end

    # lexer rule t__16! (T__16)
    # (in Statement.g)
    def t__16!
      # -> uncomment the next line to manually enable rule tracing
      # trace_in( __method__, 6 )



      type = T__16
      channel = ANTLR3::DEFAULT_CHANNEL
    # - - - - label initialization - - - -


      # - - - - main rule block - - - -
      # at line 12:9: 'between('
      match( "between(" )



      @state.type = type
      @state.channel = channel
    ensure
      # -> uncomment the next line to manually enable rule tracing
      # trace_out( __method__, 6 )


    end

    # lexer rule t__17! (T__17)
    # (in Statement.g)
    def t__17!
      # -> uncomment the next line to manually enable rule tracing
      # trace_in( __method__, 7 )



      type = T__17
      channel = ANTLR3::DEFAULT_CHANNEL
    # - - - - label initialization - - - -


      # - - - - main rule block - - - -
      # at line 13:9: 'else'
      match( "else" )



      @state.type = type
      @state.channel = channel
    ensure
      # -> uncomment the next line to manually enable rule tracing
      # trace_out( __method__, 7 )


    end

    # lexer rule t__18! (T__18)
    # (in Statement.g)
    def t__18!
      # -> uncomment the next line to manually enable rule tracing
      # trace_in( __method__, 8 )



      type = T__18
      channel = ANTLR3::DEFAULT_CHANNEL
    # - - - - label initialization - - - -


      # - - - - main rule block - - - -
      # at line 14:9: 'elsif'
      match( "elsif" )



      @state.type = type
      @state.channel = channel
    ensure
      # -> uncomment the next line to manually enable rule tracing
      # trace_out( __method__, 8 )


    end

    # lexer rule t__19! (T__19)
    # (in Statement.g)
    def t__19!
      # -> uncomment the next line to manually enable rule tracing
      # trace_in( __method__, 9 )



      type = T__19
      channel = ANTLR3::DEFAULT_CHANNEL
    # - - - - label initialization - - - -


      # - - - - main rule block - - - -
      # at line 15:9: 'equal('
      match( "equal(" )



      @state.type = type
      @state.channel = channel
    ensure
      # -> uncomment the next line to manually enable rule tracing
      # trace_out( __method__, 9 )


    end

    # lexer rule t__20! (T__20)
    # (in Statement.g)
    def t__20!
      # -> uncomment the next line to manually enable rule tracing
      # trace_in( __method__, 10 )



      type = T__20
      channel = ANTLR3::DEFAULT_CHANNEL
    # - - - - label initialization - - - -


      # - - - - main rule block - - - -
      # at line 16:9: 'greaterThan('
      match( "greaterThan(" )



      @state.type = type
      @state.channel = channel
    ensure
      # -> uncomment the next line to manually enable rule tracing
      # trace_out( __method__, 10 )


    end

    # lexer rule t__21! (T__21)
    # (in Statement.g)
    def t__21!
      # -> uncomment the next line to manually enable rule tracing
      # trace_in( __method__, 11 )



      type = T__21
      channel = ANTLR3::DEFAULT_CHANNEL
    # - - - - label initialization - - - -


      # - - - - main rule block - - - -
      # at line 17:9: 'greaterThanEqual('
      match( "greaterThanEqual(" )



      @state.type = type
      @state.channel = channel
    ensure
      # -> uncomment the next line to manually enable rule tracing
      # trace_out( __method__, 11 )


    end

    # lexer rule t__22! (T__22)
    # (in Statement.g)
    def t__22!
      # -> uncomment the next line to manually enable rule tracing
      # trace_in( __method__, 12 )



      type = T__22
      channel = ANTLR3::DEFAULT_CHANNEL
    # - - - - label initialization - - - -


      # - - - - main rule block - - - -
      # at line 18:9: 'if'
      match( "if" )



      @state.type = type
      @state.channel = channel
    ensure
      # -> uncomment the next line to manually enable rule tracing
      # trace_out( __method__, 12 )


    end

    # lexer rule t__23! (T__23)
    # (in Statement.g)
    def t__23!
      # -> uncomment the next line to manually enable rule tracing
      # trace_in( __method__, 13 )



      type = T__23
      channel = ANTLR3::DEFAULT_CHANNEL
    # - - - - label initialization - - - -


      # - - - - main rule block - - - -
      # at line 19:9: 'in('
      match( "in(" )



      @state.type = type
      @state.channel = channel
    ensure
      # -> uncomment the next line to manually enable rule tracing
      # trace_out( __method__, 13 )


    end

    # lexer rule t__24! (T__24)
    # (in Statement.g)
    def t__24!
      # -> uncomment the next line to manually enable rule tracing
      # trace_in( __method__, 14 )



      type = T__24
      channel = ANTLR3::DEFAULT_CHANNEL
    # - - - - label initialization - - - -


      # - - - - main rule block - - - -
      # at line 20:9: 'lessThan('
      match( "lessThan(" )



      @state.type = type
      @state.channel = channel
    ensure
      # -> uncomment the next line to manually enable rule tracing
      # trace_out( __method__, 14 )


    end

    # lexer rule t__25! (T__25)
    # (in Statement.g)
    def t__25!
      # -> uncomment the next line to manually enable rule tracing
      # trace_in( __method__, 15 )



      type = T__25
      channel = ANTLR3::DEFAULT_CHANNEL
    # - - - - label initialization - - - -


      # - - - - main rule block - - - -
      # at line 21:9: 'lessThanEqual('
      match( "lessThanEqual(" )



      @state.type = type
      @state.channel = channel
    ensure
      # -> uncomment the next line to manually enable rule tracing
      # trace_out( __method__, 15 )


    end

    # lexer rule t__26! (T__26)
    # (in Statement.g)
    def t__26!
      # -> uncomment the next line to manually enable rule tracing
      # trace_in( __method__, 16 )



      type = T__26
      channel = ANTLR3::DEFAULT_CHANNEL
    # - - - - label initialization - - - -


      # - - - - main rule block - - - -
      # at line 22:9: 'not('
      match( "not(" )



      @state.type = type
      @state.channel = channel
    ensure
      # -> uncomment the next line to manually enable rule tracing
      # trace_out( __method__, 16 )


    end

    # lexer rule t__27! (T__27)
    # (in Statement.g)
    def t__27!
      # -> uncomment the next line to manually enable rule tracing
      # trace_in( __method__, 17 )



      type = T__27
      channel = ANTLR3::DEFAULT_CHANNEL
    # - - - - label initialization - - - -


      # - - - - main rule block - - - -
      # at line 23:9: 'or('
      match( "or(" )



      @state.type = type
      @state.channel = channel
    ensure
      # -> uncomment the next line to manually enable rule tracing
      # trace_out( __method__, 17 )


    end

    # lexer rule t__28! (T__28)
    # (in Statement.g)
    def t__28!
      # -> uncomment the next line to manually enable rule tracing
      # trace_in( __method__, 18 )



      type = T__28
      channel = ANTLR3::DEFAULT_CHANNEL
    # - - - - label initialization - - - -


      # - - - - main rule block - - - -
      # at line 24:9: 'then'
      match( "then" )



      @state.type = type
      @state.channel = channel
    ensure
      # -> uncomment the next line to manually enable rule tracing
      # trace_out( __method__, 18 )


    end

    # lexer rule newline! (NEWLINE)
    # (in Statement.g)
    def newline!
      # -> uncomment the next line to manually enable rule tracing
      # trace_in( __method__, 19 )



      type = NEWLINE
      channel = ANTLR3::DEFAULT_CHANNEL
    # - - - - label initialization - - - -


      # - - - - main rule block - - - -
      # at line 90:15: '\\n'
      match( 0xa )

      # --> action
       channel = HIDDEN 
      # <-- action



      @state.type = type
      @state.channel = channel
    ensure
      # -> uncomment the next line to manually enable rule tracing
      # trace_out( __method__, 19 )


    end

    # lexer rule space! (SPACE)
    # (in Statement.g)
    def space!
      # -> uncomment the next line to manually enable rule tracing
      # trace_in( __method__, 20 )



      type = SPACE
      channel = ANTLR3::DEFAULT_CHANNEL
    # - - - - label initialization - - - -


      # - - - - main rule block - - - -
      # at line 91:15: ( ' ' )+
      # at file 91:15: ( ' ' )+
      match_count_1 = 0
      while true
        alt_1 = 2
        look_1_0 = @input.peek( 1 )

        if ( look_1_0 == 0x20 )
          alt_1 = 1

        end
        case alt_1
        when 1
          # at line 91:15: ' '
          match( 0x20 )

        else
          match_count_1 > 0 and break
          eee = EarlyExit(1)


          raise eee
        end
        match_count_1 += 1
      end



      # --> action
       channel = HIDDEN 
      # <-- action



      @state.type = type
      @state.channel = channel
    ensure
      # -> uncomment the next line to manually enable rule tracing
      # trace_out( __method__, 20 )


    end

    # lexer rule string! (STRING)
    # (in Statement.g)
    def string!
      # -> uncomment the next line to manually enable rule tracing
      # trace_in( __method__, 21 )



      type = STRING
      channel = ANTLR3::DEFAULT_CHANNEL
    # - - - - label initialization - - - -


      # - - - - main rule block - - - -
      # at line 92:13: ( '\\'' (~ ( '\\'' ) )* '\\'' | '\\\"' (~ ( '\\\"' ) )* '\\\"' )
      alt_4 = 2
      look_4_0 = @input.peek( 1 )

      if ( look_4_0 == 0x27 )
        alt_4 = 1
      elsif ( look_4_0 == 0x22 )
        alt_4 = 2
      else
        raise NoViableAlternative( "", 4, 0 )

      end
      case alt_4
      when 1
        # at line 92:15: '\\'' (~ ( '\\'' ) )* '\\''
        match( 0x27 )
        # at line 92:20: (~ ( '\\'' ) )*
        while true # decision 2
          alt_2 = 2
          look_2_0 = @input.peek( 1 )

          if ( look_2_0.between?( 0x0, 0x26 ) || look_2_0.between?( 0x28, 0xffff ) )
            alt_2 = 1

          end
          case alt_2
          when 1
            # at line 
            if @input.peek( 1 ).between?( 0x0, 0x26 ) || @input.peek( 1 ).between?( 0x28, 0xffff )
              @input.consume
            else
              mse = MismatchedSet( nil )
              recover mse
              raise mse

            end



          else
            break # out of loop for decision 2
          end
        end # loop for decision 2

        match( 0x27 )

      when 2
        # at line 93:15: '\\\"' (~ ( '\\\"' ) )* '\\\"'
        match( 0x22 )
        # at line 93:20: (~ ( '\\\"' ) )*
        while true # decision 3
          alt_3 = 2
          look_3_0 = @input.peek( 1 )

          if ( look_3_0.between?( 0x0, 0x21 ) || look_3_0.between?( 0x23, 0xffff ) )
            alt_3 = 1

          end
          case alt_3
          when 1
            # at line 
            if @input.peek( 1 ).between?( 0x0, 0x21 ) || @input.peek( 1 ).between?( 0x23, 0xffff )
              @input.consume
            else
              mse = MismatchedSet( nil )
              recover mse
              raise mse

            end



          else
            break # out of loop for decision 3
          end
        end # loop for decision 3

        match( 0x22 )

      end

      @state.type = type
      @state.channel = channel
    ensure
      # -> uncomment the next line to manually enable rule tracing
      # trace_out( __method__, 21 )


    end

    # lexer rule number! (NUMBER)
    # (in Statement.g)
    def number!
      # -> uncomment the next line to manually enable rule tracing
      # trace_in( __method__, 22 )



      type = NUMBER
      channel = ANTLR3::DEFAULT_CHANNEL
    # - - - - label initialization - - - -


      # - - - - main rule block - - - -
      # at line 95:15: ( '-' )? ( DIGIT )+ '.' ( DIGIT )+
      # at line 95:15: ( '-' )?
      alt_5 = 2
      look_5_0 = @input.peek( 1 )

      if ( look_5_0 == 0x2d )
        alt_5 = 1
      end
      case alt_5
      when 1
        # at line 95:15: '-'
        match( 0x2d )

      end
      # at file 95:20: ( DIGIT )+
      match_count_6 = 0
      while true
        alt_6 = 2
        look_6_0 = @input.peek( 1 )

        if ( look_6_0.between?( 0x30, 0x39 ) )
          alt_6 = 1

        end
        case alt_6
        when 1
          # at line 
          if @input.peek( 1 ).between?( 0x30, 0x39 )
            @input.consume
          else
            mse = MismatchedSet( nil )
            recover mse
            raise mse

          end



        else
          match_count_6 > 0 and break
          eee = EarlyExit(6)


          raise eee
        end
        match_count_6 += 1
      end


      match( 0x2e )
      # at file 95:31: ( DIGIT )+
      match_count_7 = 0
      while true
        alt_7 = 2
        look_7_0 = @input.peek( 1 )

        if ( look_7_0.between?( 0x30, 0x39 ) )
          alt_7 = 1

        end
        case alt_7
        when 1
          # at line 
          if @input.peek( 1 ).between?( 0x30, 0x39 )
            @input.consume
          else
            mse = MismatchedSet( nil )
            recover mse
            raise mse

          end



        else
          match_count_7 > 0 and break
          eee = EarlyExit(7)


          raise eee
        end
        match_count_7 += 1
      end




      @state.type = type
      @state.channel = channel
    ensure
      # -> uncomment the next line to manually enable rule tracing
      # trace_out( __method__, 22 )


    end

    # lexer rule int! (INT)
    # (in Statement.g)
    def int!
      # -> uncomment the next line to manually enable rule tracing
      # trace_in( __method__, 23 )



      type = INT
      channel = ANTLR3::DEFAULT_CHANNEL
    # - - - - label initialization - - - -


      # - - - - main rule block - - - -
      # at line 96:15: ( '-' )? ( DIGIT )+
      # at line 96:15: ( '-' )?
      alt_8 = 2
      look_8_0 = @input.peek( 1 )

      if ( look_8_0 == 0x2d )
        alt_8 = 1
      end
      case alt_8
      when 1
        # at line 96:15: '-'
        match( 0x2d )

      end
      # at file 96:20: ( DIGIT )+
      match_count_9 = 0
      while true
        alt_9 = 2
        look_9_0 = @input.peek( 1 )

        if ( look_9_0.between?( 0x30, 0x39 ) )
          alt_9 = 1

        end
        case alt_9
        when 1
          # at line 
          if @input.peek( 1 ).between?( 0x30, 0x39 )
            @input.consume
          else
            mse = MismatchedSet( nil )
            recover mse
            raise mse

          end



        else
          match_count_9 > 0 and break
          eee = EarlyExit(9)


          raise eee
        end
        match_count_9 += 1
      end




      @state.type = type
      @state.channel = channel
    ensure
      # -> uncomment the next line to manually enable rule tracing
      # trace_out( __method__, 23 )


    end

    # lexer rule variable! (VARIABLE)
    # (in Statement.g)
    def variable!
      # -> uncomment the next line to manually enable rule tracing
      # trace_in( __method__, 24 )



      type = VARIABLE
      channel = ANTLR3::DEFAULT_CHANNEL
    # - - - - label initialization - - - -


      # - - - - main rule block - - - -
      # at line 97:15: '$' ( DIGIT )+
      match( 0x24 )
      # at file 97:19: ( DIGIT )+
      match_count_10 = 0
      while true
        alt_10 = 2
        look_10_0 = @input.peek( 1 )

        if ( look_10_0.between?( 0x30, 0x39 ) )
          alt_10 = 1

        end
        case alt_10
        when 1
          # at line 
          if @input.peek( 1 ).between?( 0x30, 0x39 )
            @input.consume
          else
            mse = MismatchedSet( nil )
            recover mse
            raise mse

          end



        else
          match_count_10 > 0 and break
          eee = EarlyExit(10)


          raise eee
        end
        match_count_10 += 1
      end




      @state.type = type
      @state.channel = channel
    ensure
      # -> uncomment the next line to manually enable rule tracing
      # trace_out( __method__, 24 )


    end

    # lexer rule digit! (DIGIT)
    # (in Statement.g)
    def digit!
      # -> uncomment the next line to manually enable rule tracing
      # trace_in( __method__, 25 )


    # - - - - label initialization - - - -


      # - - - - main rule block - - - -
      # at line 
      if @input.peek( 1 ).between?( 0x30, 0x39 )
        @input.consume
      else
        mse = MismatchedSet( nil )
        recover mse
        raise mse

      end



    ensure
      # -> uncomment the next line to manually enable rule tracing
      # trace_out( __method__, 25 )


    end

    # main rule used to study the input at the current position,
    # and choose the proper lexer rule to call in order to
    # fetch the next token
    #
    # usually, you don't make direct calls to this method,
    # but instead use the next_token method, which will
    # build and emit the actual next token
    def token!
      # at line 1:8: ( T__11 | T__12 | T__13 | T__14 | T__15 | T__16 | T__17 | T__18 | T__19 | T__20 | T__21 | T__22 | T__23 | T__24 | T__25 | T__26 | T__27 | T__28 | NEWLINE | SPACE | STRING | NUMBER | INT | VARIABLE )
      alt_11 = 24
      alt_11 = @dfa11.predict( @input )
      case alt_11
      when 1
        # at line 1:10: T__11
        t__11!


      when 2
        # at line 1:16: T__12
        t__12!


      when 3
        # at line 1:22: T__13
        t__13!


      when 4
        # at line 1:28: T__14
        t__14!


      when 5
        # at line 1:34: T__15
        t__15!


      when 6
        # at line 1:40: T__16
        t__16!


      when 7
        # at line 1:46: T__17
        t__17!


      when 8
        # at line 1:52: T__18
        t__18!


      when 9
        # at line 1:58: T__19
        t__19!


      when 10
        # at line 1:64: T__20
        t__20!


      when 11
        # at line 1:70: T__21
        t__21!


      when 12
        # at line 1:76: T__22
        t__22!


      when 13
        # at line 1:82: T__23
        t__23!


      when 14
        # at line 1:88: T__24
        t__24!


      when 15
        # at line 1:94: T__25
        t__25!


      when 16
        # at line 1:100: T__26
        t__26!


      when 17
        # at line 1:106: T__27
        t__27!


      when 18
        # at line 1:112: T__28
        t__28!


      when 19
        # at line 1:118: NEWLINE
        newline!


      when 20
        # at line 1:126: SPACE
        space!


      when 21
        # at line 1:132: STRING
        string!


      when 22
        # at line 1:139: NUMBER
        number!


      when 23
        # at line 1:146: INT
        int!


      when 24
        # at line 1:150: VARIABLE
        variable!


      end
    end


    # - - - - - - - - - - DFA definitions - - - - - - - - - - -
    class DFA11 < ANTLR3::DFA
      EOT = unpack( 18, -1, 1, 27, 31, -1 )
      EOF = unpack( 50, -1 )
      MIN = unpack( 1, 10, 6, -1, 1, 108, 1, 114, 1, 102, 1, 101, 6, -1, 
                    1, 48, 1, 46, 1, -1, 1, 115, 1, -1, 1, 101, 2, -1, 1, 
                    115, 2, -1, 1, 101, 1, 97, 1, 115, 2, -1, 1, 116, 1, 
                    84, 1, 101, 1, 104, 1, 114, 1, 97, 1, 84, 1, 110, 1, 
                    104, 1, 40, 1, 97, 2, -1, 1, 110, 1, 40, 2, -1 )
      MAX = unpack( 1, 116, 6, -1, 1, 113, 1, 114, 1, 110, 1, 101, 6, -1, 
                    2, 57, 1, -1, 1, 115, 1, -1, 1, 101, 2, -1, 1, 115, 
                    2, -1, 1, 105, 1, 97, 1, 115, 2, -1, 1, 116, 1, 84, 
                    1, 101, 1, 104, 1, 114, 1, 97, 1, 84, 1, 110, 1, 104, 
                    1, 69, 1, 97, 2, -1, 1, 110, 1, 69, 2, -1 )
      ACCEPT = unpack( 1, -1, 1, 1, 1, 2, 1, 3, 1, 4, 1, 5, 1, 6, 4, -1, 
                       1, 16, 1, 17, 1, 18, 1, 19, 1, 20, 1, 21, 2, -1, 
                       1, 24, 1, -1, 1, 9, 1, -1, 1, 12, 1, 13, 1, -1, 1, 
                       22, 1, 23, 3, -1, 1, 7, 1, 8, 11, -1, 1, 14, 1, 15, 
                       2, -1, 1, 10, 1, 11 )
      SPECIAL = unpack( 50, -1 )
      TRANSITION = [
        unpack( 1, 14, 21, -1, 1, 15, 1, -1, 1, 16, 1, -1, 1, 19, 2, -1, 
                1, 16, 1, -1, 1, 1, 2, -1, 1, 2, 1, 17, 2, -1, 10, 18, 33, 
                -1, 1, 3, 1, -1, 1, 4, 3, -1, 1, 5, 1, 6, 2, -1, 1, 7, 1, 
                -1, 1, 8, 1, -1, 1, 9, 2, -1, 1, 10, 1, -1, 1, 11, 1, 12, 
                4, -1, 1, 13 ),
        unpack(  ),
        unpack(  ),
        unpack(  ),
        unpack(  ),
        unpack(  ),
        unpack(  ),
        unpack( 1, 20, 4, -1, 1, 21 ),
        unpack( 1, 22 ),
        unpack( 1, 23, 7, -1, 1, 24 ),
        unpack( 1, 25 ),
        unpack(  ),
        unpack(  ),
        unpack(  ),
        unpack(  ),
        unpack(  ),
        unpack(  ),
        unpack( 10, 18 ),
        unpack( 1, 26, 1, -1, 10, 18 ),
        unpack(  ),
        unpack( 1, 28 ),
        unpack(  ),
        unpack( 1, 29 ),
        unpack(  ),
        unpack(  ),
        unpack( 1, 30 ),
        unpack(  ),
        unpack(  ),
        unpack( 1, 31, 3, -1, 1, 32 ),
        unpack( 1, 33 ),
        unpack( 1, 34 ),
        unpack(  ),
        unpack(  ),
        unpack( 1, 35 ),
        unpack( 1, 36 ),
        unpack( 1, 37 ),
        unpack( 1, 38 ),
        unpack( 1, 39 ),
        unpack( 1, 40 ),
        unpack( 1, 41 ),
        unpack( 1, 42 ),
        unpack( 1, 43 ),
        unpack( 1, 44, 28, -1, 1, 45 ),
        unpack( 1, 46 ),
        unpack(  ),
        unpack(  ),
        unpack( 1, 47 ),
        unpack( 1, 48, 28, -1, 1, 49 ),
        unpack(  ),
        unpack(  )
      ].freeze

      ( 0 ... MIN.length ).zip( MIN, MAX ) do | i, a, z |
        if a > 0 and z < 0
          MAX[ i ] %= 0x10000
        end
      end

      @decision = 11


      def description
        <<-'__dfa_description__'.strip!
          1:1: Tokens : ( T__11 | T__12 | T__13 | T__14 | T__15 | T__16 | T__17 | T__18 | T__19 | T__20 | T__21 | T__22 | T__23 | T__24 | T__25 | T__26 | T__27 | T__28 | NEWLINE | SPACE | STRING | NUMBER | INT | VARIABLE );
        __dfa_description__
      end

    end


    private

    def initialize_dfas
      super rescue nil
      @dfa11 = DFA11.new( self, 11 )


    end

  end # class Lexer < ANTLR3::Lexer

  at_exit { Lexer.main( ARGV ) } if __FILE__ == $0

end
