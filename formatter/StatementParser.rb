#!/usr/bin/env ruby
#
# Statement.g
# --
# Generated using ANTLR version: 3.5
# Ruby runtime library version: 1.10.0
# Input grammar file: Statement.g
# Generated at: 2014-10-07 12:11:49
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


    # register the proper human-readable name or literal value
    # for each token type
    #
    # this is necessary because anonymous tokens, which are
    # created from literal values in the grammar, do not
    # have descriptive names
    register_names( "DIGIT", "INT", "NEWLINE", "NUMBER", "SPACE", "STRING", 
                    "VARIABLE", "')'", "','", "'['", "']'", "'and('", "'between('", 
                    "'else'", "'elsif'", "'equal('", "'greaterThan('", "'greaterThanEqual('", 
                    "'if'", "'in('", "'lessThan('", "'lessThanEqual('", 
                    "'not('", "'or('", "'then'" )


    # - - - - - - begin action @token::members - - - - - -
    # Statement.g


        def value
            return nil if text == 'null'
            return text.to_f unless text =~ /^(\'|\")/
            text[1..-2]
        end

    # - - - - - - end action @token::members - - - - - - -


  end


  class Parser < ANTLR3::Parser
    @grammar_home = Statement
    include ANTLR3::ASTBuilder

    RULE_METHODS = [ :program, :statement, :next_statement, :multi_expression, 
                     :single_expression, :list, :literals, :literal ].freeze

    include TokenData

    begin
      generated_using( "Statement.g", "3.5", "1.10.0" )
    rescue NoMethodError => error
      # ignore
    end

    def initialize( input, options = {} )
      super( input, options )
    end
    # - - - - - - - - - - - - Rules - - - - - - - - - - - - -
    ProgramReturnValue = define_return_scope :value

    #
    # parser rule program
    #
    # (in Statement.g)
    # 16:1: program returns [value] : s= statement ;
    #
    def program
      # -> uncomment the next line to manually enable rule tracing
      # trace_in( __method__, 1 )


      return_value = ProgramReturnValue.new

      # $rule.start = the first token seen before matching
      return_value.start = @input.look


      root_0 = nil

      s = nil



      begin
      root_0 = @adaptor.create_flat_list


      # at line 17:7: s= statement
      @state.following.push( TOKENS_FOLLOWING_statement_IN_program_56 )
      s = statement
      @state.following.pop
      @adaptor.add_child( root_0, s.tree )


      # --> action
       return_value.value = ( s.nil? ? nil : s.value ) 
      # <-- action


      # - - - - - - - rule clean up - - - - - - - -
      return_value.stop = @input.look( -1 )


      return_value.tree = @adaptor.rule_post_processing( root_0 )
      @adaptor.set_token_boundaries( return_value.tree, return_value.start, return_value.stop )


      rescue ANTLR3::Error::RecognitionError => re
        report_error(re)
        recover(re)
        return_value.tree = @adaptor.create_error_node( @input, return_value.start, @input.look(-1), re )


      ensure
        # -> uncomment the next line to manually enable rule tracing
        # trace_out( __method__, 1 )


      end

      return return_value
    end

    StatementReturnValue = define_return_scope :value

    #
    # parser rule statement
    #
    # (in Statement.g)
    # 20:1: statement returns [value] : 'if' e= multi_expression 'then' v= literal (s= next_statement )? ;
    #
    def statement
      # -> uncomment the next line to manually enable rule tracing
      # trace_in( __method__, 2 )


      return_value = StatementReturnValue.new

      # $rule.start = the first token seen before matching
      return_value.start = @input.look


      root_0 = nil

      string_literal1 = nil
      string_literal2 = nil
      e = nil
      v = nil
      s = nil


      tree_for_string_literal1 = nil
      tree_for_string_literal2 = nil

      begin
      root_0 = @adaptor.create_flat_list


      # at line 21:7: 'if' e= multi_expression 'then' v= literal (s= next_statement )?
      string_literal1 = match( T__22, TOKENS_FOLLOWING_T__22_IN_statement_79 )
      tree_for_string_literal1 = @adaptor.create_with_payload( string_literal1 )
      @adaptor.add_child( root_0, tree_for_string_literal1 )


      @state.following.push( TOKENS_FOLLOWING_multi_expression_IN_statement_83 )
      e = multi_expression
      @state.following.pop
      @adaptor.add_child( root_0, e.tree )

      string_literal2 = match( T__28, TOKENS_FOLLOWING_T__28_IN_statement_85 )
      tree_for_string_literal2 = @adaptor.create_with_payload( string_literal2 )
      @adaptor.add_child( root_0, tree_for_string_literal2 )


      @state.following.push( TOKENS_FOLLOWING_literal_IN_statement_89 )
      v = literal
      @state.following.pop
      @adaptor.add_child( root_0, v.tree )

      # at line 21:49: (s= next_statement )?
      alt_1 = 2
      look_1_0 = @input.peek( 1 )

      if ( look_1_0.between?( T__17, T__18 ) )
        alt_1 = 1
      end
      case alt_1
      when 1
        # at line 21:49: s= next_statement
        @state.following.push( TOKENS_FOLLOWING_next_statement_IN_statement_93 )
        s = next_statement
        @state.following.pop
        @adaptor.add_child( root_0, s.tree )


      end

      # --> action
       
                  if ( e.nil? ? nil : e.value ) 
                      return_value.value = ( v.nil? ? nil : v.value )
                  else
                      return_value.value = ( s.nil? ? nil : s.value )
                  end
              
      # <-- action


      # - - - - - - - rule clean up - - - - - - - -
      return_value.stop = @input.look( -1 )


      return_value.tree = @adaptor.rule_post_processing( root_0 )
      @adaptor.set_token_boundaries( return_value.tree, return_value.start, return_value.stop )


      rescue ANTLR3::Error::RecognitionError => re
        report_error(re)
        recover(re)
        return_value.tree = @adaptor.create_error_node( @input, return_value.start, @input.look(-1), re )


      ensure
        # -> uncomment the next line to manually enable rule tracing
        # trace_out( __method__, 2 )


      end

      return return_value
    end

    NextStatementReturnValue = define_return_scope :value

    #
    # parser rule next_statement
    #
    # (in Statement.g)
    # 31:1: next_statement returns [value] : ( 'elsif' e= multi_expression 'then' v= literal (s= next_statement )? | 'else' v= literal );
    #
    def next_statement
      # -> uncomment the next line to manually enable rule tracing
      # trace_in( __method__, 3 )


      return_value = NextStatementReturnValue.new

      # $rule.start = the first token seen before matching
      return_value.start = @input.look


      root_0 = nil

      string_literal3 = nil
      string_literal4 = nil
      string_literal5 = nil
      e = nil
      v = nil
      s = nil


      tree_for_string_literal3 = nil
      tree_for_string_literal4 = nil
      tree_for_string_literal5 = nil

      begin
      # at line 32:5: ( 'elsif' e= multi_expression 'then' v= literal (s= next_statement )? | 'else' v= literal )
      alt_3 = 2
      look_3_0 = @input.peek( 1 )

      if ( look_3_0 == T__18 )
        alt_3 = 1
      elsif ( look_3_0 == T__17 )
        alt_3 = 2
      else
        raise NoViableAlternative( "", 3, 0 )

      end
      case alt_3
      when 1
        root_0 = @adaptor.create_flat_list


        # at line 32:7: 'elsif' e= multi_expression 'then' v= literal (s= next_statement )?
        string_literal3 = match( T__18, TOKENS_FOLLOWING_T__18_IN_next_statement_126 )
        tree_for_string_literal3 = @adaptor.create_with_payload( string_literal3 )
        @adaptor.add_child( root_0, tree_for_string_literal3 )


        @state.following.push( TOKENS_FOLLOWING_multi_expression_IN_next_statement_130 )
        e = multi_expression
        @state.following.pop
        @adaptor.add_child( root_0, e.tree )

        string_literal4 = match( T__28, TOKENS_FOLLOWING_T__28_IN_next_statement_132 )
        tree_for_string_literal4 = @adaptor.create_with_payload( string_literal4 )
        @adaptor.add_child( root_0, tree_for_string_literal4 )


        @state.following.push( TOKENS_FOLLOWING_literal_IN_next_statement_136 )
        v = literal
        @state.following.pop
        @adaptor.add_child( root_0, v.tree )

        # at line 32:52: (s= next_statement )?
        alt_2 = 2
        look_2_0 = @input.peek( 1 )

        if ( look_2_0.between?( T__17, T__18 ) )
          alt_2 = 1
        end
        case alt_2
        when 1
          # at line 32:52: s= next_statement
          @state.following.push( TOKENS_FOLLOWING_next_statement_IN_next_statement_140 )
          s = next_statement
          @state.following.pop
          @adaptor.add_child( root_0, s.tree )


        end

        # --> action
         
                    if ( e.nil? ? nil : e.value ) 
                        return_value.value = ( v.nil? ? nil : v.value )
                    else
                        return_value.value = ( s.nil? ? nil : s.value )
                    end
                
        # <-- action


      when 2
        root_0 = @adaptor.create_flat_list


        # at line 40:7: 'else' v= literal
        string_literal5 = match( T__17, TOKENS_FOLLOWING_T__17_IN_next_statement_159 )
        tree_for_string_literal5 = @adaptor.create_with_payload( string_literal5 )
        @adaptor.add_child( root_0, tree_for_string_literal5 )


        @state.following.push( TOKENS_FOLLOWING_literal_IN_next_statement_163 )
        v = literal
        @state.following.pop
        @adaptor.add_child( root_0, v.tree )


        # --> action
         
                    return_value.value = ( v.nil? ? nil : v.value )
                
        # <-- action


      end
      # - - - - - - - rule clean up - - - - - - - -
      return_value.stop = @input.look( -1 )


      return_value.tree = @adaptor.rule_post_processing( root_0 )
      @adaptor.set_token_boundaries( return_value.tree, return_value.start, return_value.stop )


      rescue ANTLR3::Error::RecognitionError => re
        report_error(re)
        recover(re)
        return_value.tree = @adaptor.create_error_node( @input, return_value.start, @input.look(-1), re )


      ensure
        # -> uncomment the next line to manually enable rule tracing
        # trace_out( __method__, 3 )


      end

      return return_value
    end

    MultiExpressionReturnValue = define_return_scope :value

    #
    # parser rule multi_expression
    #
    # (in Statement.g)
    # 46:1: multi_expression returns [value] : ( 'and(' l= single_expression ',' r= multi_expression ')' | 'or(' l= single_expression ',' r= multi_expression ')' |e= single_expression );
    #
    def multi_expression
      # -> uncomment the next line to manually enable rule tracing
      # trace_in( __method__, 4 )


      return_value = MultiExpressionReturnValue.new

      # $rule.start = the first token seen before matching
      return_value.start = @input.look


      root_0 = nil

      string_literal6 = nil
      char_literal7 = nil
      char_literal8 = nil
      string_literal9 = nil
      char_literal10 = nil
      char_literal11 = nil
      l = nil
      r = nil
      e = nil


      tree_for_string_literal6 = nil
      tree_for_char_literal7 = nil
      tree_for_char_literal8 = nil
      tree_for_string_literal9 = nil
      tree_for_char_literal10 = nil
      tree_for_char_literal11 = nil

      begin
      # at line 47:5: ( 'and(' l= single_expression ',' r= multi_expression ')' | 'or(' l= single_expression ',' r= multi_expression ')' |e= single_expression )
      alt_4 = 3
      case look_4 = @input.peek( 1 )
      when T__15 then alt_4 = 1
      when T__27 then alt_4 = 2
      when INT, NUMBER, STRING, VARIABLE, T__16, T__19, T__20, T__21, T__23, T__24, T__25, T__26 then alt_4 = 3
      else
        raise NoViableAlternative( "", 4, 0 )

      end
      case alt_4
      when 1
        root_0 = @adaptor.create_flat_list


        # at line 47:7: 'and(' l= single_expression ',' r= multi_expression ')'
        string_literal6 = match( T__15, TOKENS_FOLLOWING_T__15_IN_multi_expression_194 )
        tree_for_string_literal6 = @adaptor.create_with_payload( string_literal6 )
        @adaptor.add_child( root_0, tree_for_string_literal6 )


        @state.following.push( TOKENS_FOLLOWING_single_expression_IN_multi_expression_198 )
        l = single_expression
        @state.following.pop
        @adaptor.add_child( root_0, l.tree )

        char_literal7 = match( T__12, TOKENS_FOLLOWING_T__12_IN_multi_expression_200 )
        tree_for_char_literal7 = @adaptor.create_with_payload( char_literal7 )
        @adaptor.add_child( root_0, tree_for_char_literal7 )


        @state.following.push( TOKENS_FOLLOWING_multi_expression_IN_multi_expression_204 )
        r = multi_expression
        @state.following.pop
        @adaptor.add_child( root_0, r.tree )

        char_literal8 = match( T__11, TOKENS_FOLLOWING_T__11_IN_multi_expression_206 )
        tree_for_char_literal8 = @adaptor.create_with_payload( char_literal8 )
        @adaptor.add_child( root_0, tree_for_char_literal8 )



        # --> action
         return_value.value = ( l.nil? ? nil : l.value ) && ( r.nil? ? nil : r.value ) 
        # <-- action


      when 2
        root_0 = @adaptor.create_flat_list


        # at line 48:7: 'or(' l= single_expression ',' r= multi_expression ')'
        string_literal9 = match( T__27, TOKENS_FOLLOWING_T__27_IN_multi_expression_216 )
        tree_for_string_literal9 = @adaptor.create_with_payload( string_literal9 )
        @adaptor.add_child( root_0, tree_for_string_literal9 )


        @state.following.push( TOKENS_FOLLOWING_single_expression_IN_multi_expression_220 )
        l = single_expression
        @state.following.pop
        @adaptor.add_child( root_0, l.tree )

        char_literal10 = match( T__12, TOKENS_FOLLOWING_T__12_IN_multi_expression_222 )
        tree_for_char_literal10 = @adaptor.create_with_payload( char_literal10 )
        @adaptor.add_child( root_0, tree_for_char_literal10 )


        @state.following.push( TOKENS_FOLLOWING_multi_expression_IN_multi_expression_226 )
        r = multi_expression
        @state.following.pop
        @adaptor.add_child( root_0, r.tree )

        char_literal11 = match( T__11, TOKENS_FOLLOWING_T__11_IN_multi_expression_228 )
        tree_for_char_literal11 = @adaptor.create_with_payload( char_literal11 )
        @adaptor.add_child( root_0, tree_for_char_literal11 )



        # --> action
         return_value.value = ( l.nil? ? nil : l.value ) || ( r.nil? ? nil : r.value ) 
        # <-- action


      when 3
        root_0 = @adaptor.create_flat_list


        # at line 49:7: e= single_expression
        @state.following.push( TOKENS_FOLLOWING_single_expression_IN_multi_expression_240 )
        e = single_expression
        @state.following.pop
        @adaptor.add_child( root_0, e.tree )


        # --> action
         return_value.value = ( e.nil? ? nil : e.value ) 
        # <-- action


      end
      # - - - - - - - rule clean up - - - - - - - -
      return_value.stop = @input.look( -1 )


      return_value.tree = @adaptor.rule_post_processing( root_0 )
      @adaptor.set_token_boundaries( return_value.tree, return_value.start, return_value.stop )


      rescue ANTLR3::Error::RecognitionError => re
        report_error(re)
        recover(re)
        return_value.tree = @adaptor.create_error_node( @input, return_value.start, @input.look(-1), re )


      ensure
        # -> uncomment the next line to manually enable rule tracing
        # trace_out( __method__, 4 )


      end

      return return_value
    end

    SingleExpressionReturnValue = define_return_scope :value

    #
    # parser rule single_expression
    #
    # (in Statement.g)
    # 52:1: single_expression returns [value] : ( 'equal(' l= literal ',' r= literal ')' | 'greaterThan(' l= literal ',' r= literal ')' | 'greaterThanEqual(' l= literal ',' r= literal ')' | 'lessThan(' l= literal ',' r= literal ')' | 'lessThanEqual(' l= literal ',' r= literal ')' | 'between(' l= literal ',' min= literal ',' max= literal ')' | 'not(' e= single_expression ')' | 'in(' v= literal ',' l= list ')' |e= literal );
    #
    def single_expression
      # -> uncomment the next line to manually enable rule tracing
      # trace_in( __method__, 5 )


      return_value = SingleExpressionReturnValue.new

      # $rule.start = the first token seen before matching
      return_value.start = @input.look


      root_0 = nil

      string_literal12 = nil
      char_literal13 = nil
      char_literal14 = nil
      string_literal15 = nil
      char_literal16 = nil
      char_literal17 = nil
      string_literal18 = nil
      char_literal19 = nil
      char_literal20 = nil
      string_literal21 = nil
      char_literal22 = nil
      char_literal23 = nil
      string_literal24 = nil
      char_literal25 = nil
      char_literal26 = nil
      string_literal27 = nil
      char_literal28 = nil
      char_literal29 = nil
      char_literal30 = nil
      string_literal31 = nil
      char_literal32 = nil
      string_literal33 = nil
      char_literal34 = nil
      char_literal35 = nil
      l = nil
      r = nil
      min = nil
      max = nil
      e = nil
      v = nil


      tree_for_string_literal12 = nil
      tree_for_char_literal13 = nil
      tree_for_char_literal14 = nil
      tree_for_string_literal15 = nil
      tree_for_char_literal16 = nil
      tree_for_char_literal17 = nil
      tree_for_string_literal18 = nil
      tree_for_char_literal19 = nil
      tree_for_char_literal20 = nil
      tree_for_string_literal21 = nil
      tree_for_char_literal22 = nil
      tree_for_char_literal23 = nil
      tree_for_string_literal24 = nil
      tree_for_char_literal25 = nil
      tree_for_char_literal26 = nil
      tree_for_string_literal27 = nil
      tree_for_char_literal28 = nil
      tree_for_char_literal29 = nil
      tree_for_char_literal30 = nil
      tree_for_string_literal31 = nil
      tree_for_char_literal32 = nil
      tree_for_string_literal33 = nil
      tree_for_char_literal34 = nil
      tree_for_char_literal35 = nil

      begin
      # at line 53:5: ( 'equal(' l= literal ',' r= literal ')' | 'greaterThan(' l= literal ',' r= literal ')' | 'greaterThanEqual(' l= literal ',' r= literal ')' | 'lessThan(' l= literal ',' r= literal ')' | 'lessThanEqual(' l= literal ',' r= literal ')' | 'between(' l= literal ',' min= literal ',' max= literal ')' | 'not(' e= single_expression ')' | 'in(' v= literal ',' l= list ')' |e= literal )
      alt_5 = 9
      case look_5 = @input.peek( 1 )
      when T__19 then alt_5 = 1
      when T__20 then alt_5 = 2
      when T__21 then alt_5 = 3
      when T__24 then alt_5 = 4
      when T__25 then alt_5 = 5
      when T__16 then alt_5 = 6
      when T__26 then alt_5 = 7
      when T__23 then alt_5 = 8
      when INT, NUMBER, STRING, VARIABLE then alt_5 = 9
      else
        raise NoViableAlternative( "", 5, 0 )

      end
      case alt_5
      when 1
        root_0 = @adaptor.create_flat_list


        # at line 53:7: 'equal(' l= literal ',' r= literal ')'
        string_literal12 = match( T__19, TOKENS_FOLLOWING_T__19_IN_single_expression_263 )
        tree_for_string_literal12 = @adaptor.create_with_payload( string_literal12 )
        @adaptor.add_child( root_0, tree_for_string_literal12 )


        @state.following.push( TOKENS_FOLLOWING_literal_IN_single_expression_267 )
        l = literal
        @state.following.pop
        @adaptor.add_child( root_0, l.tree )

        char_literal13 = match( T__12, TOKENS_FOLLOWING_T__12_IN_single_expression_269 )
        tree_for_char_literal13 = @adaptor.create_with_payload( char_literal13 )
        @adaptor.add_child( root_0, tree_for_char_literal13 )


        @state.following.push( TOKENS_FOLLOWING_literal_IN_single_expression_273 )
        r = literal
        @state.following.pop
        @adaptor.add_child( root_0, r.tree )

        char_literal14 = match( T__11, TOKENS_FOLLOWING_T__11_IN_single_expression_275 )
        tree_for_char_literal14 = @adaptor.create_with_payload( char_literal14 )
        @adaptor.add_child( root_0, tree_for_char_literal14 )



        # --> action
         return_value.value = ( l.nil? ? nil : l.value ) == ( r.nil? ? nil : r.value ) 
        # <-- action


      when 2
        root_0 = @adaptor.create_flat_list


        # at line 54:7: 'greaterThan(' l= literal ',' r= literal ')'
        string_literal15 = match( T__20, TOKENS_FOLLOWING_T__20_IN_single_expression_285 )
        tree_for_string_literal15 = @adaptor.create_with_payload( string_literal15 )
        @adaptor.add_child( root_0, tree_for_string_literal15 )


        @state.following.push( TOKENS_FOLLOWING_literal_IN_single_expression_289 )
        l = literal
        @state.following.pop
        @adaptor.add_child( root_0, l.tree )

        char_literal16 = match( T__12, TOKENS_FOLLOWING_T__12_IN_single_expression_291 )
        tree_for_char_literal16 = @adaptor.create_with_payload( char_literal16 )
        @adaptor.add_child( root_0, tree_for_char_literal16 )


        @state.following.push( TOKENS_FOLLOWING_literal_IN_single_expression_295 )
        r = literal
        @state.following.pop
        @adaptor.add_child( root_0, r.tree )

        char_literal17 = match( T__11, TOKENS_FOLLOWING_T__11_IN_single_expression_297 )
        tree_for_char_literal17 = @adaptor.create_with_payload( char_literal17 )
        @adaptor.add_child( root_0, tree_for_char_literal17 )



        # --> action
         return_value.value = ( l.nil? ? nil : l.value ).nil? == false && ( r.nil? ? nil : r.value ).nil? == false && ( l.nil? ? nil : l.value ).to_f > ( r.nil? ? nil : r.value ).to_f 
        # <-- action


      when 3
        root_0 = @adaptor.create_flat_list


        # at line 55:7: 'greaterThanEqual(' l= literal ',' r= literal ')'
        string_literal18 = match( T__21, TOKENS_FOLLOWING_T__21_IN_single_expression_307 )
        tree_for_string_literal18 = @adaptor.create_with_payload( string_literal18 )
        @adaptor.add_child( root_0, tree_for_string_literal18 )


        @state.following.push( TOKENS_FOLLOWING_literal_IN_single_expression_310 )
        l = literal
        @state.following.pop
        @adaptor.add_child( root_0, l.tree )

        char_literal19 = match( T__12, TOKENS_FOLLOWING_T__12_IN_single_expression_312 )
        tree_for_char_literal19 = @adaptor.create_with_payload( char_literal19 )
        @adaptor.add_child( root_0, tree_for_char_literal19 )


        @state.following.push( TOKENS_FOLLOWING_literal_IN_single_expression_316 )
        r = literal
        @state.following.pop
        @adaptor.add_child( root_0, r.tree )

        char_literal20 = match( T__11, TOKENS_FOLLOWING_T__11_IN_single_expression_318 )
        tree_for_char_literal20 = @adaptor.create_with_payload( char_literal20 )
        @adaptor.add_child( root_0, tree_for_char_literal20 )



        # --> action
         return_value.value = ( l.nil? ? nil : l.value ).nil? == false && ( r.nil? ? nil : r.value ).nil? == false && ( l.nil? ? nil : l.value ).to_f >= ( r.nil? ? nil : r.value ).to_f 
        # <-- action


      when 4
        root_0 = @adaptor.create_flat_list


        # at line 56:7: 'lessThan(' l= literal ',' r= literal ')'
        string_literal21 = match( T__24, TOKENS_FOLLOWING_T__24_IN_single_expression_328 )
        tree_for_string_literal21 = @adaptor.create_with_payload( string_literal21 )
        @adaptor.add_child( root_0, tree_for_string_literal21 )


        @state.following.push( TOKENS_FOLLOWING_literal_IN_single_expression_332 )
        l = literal
        @state.following.pop
        @adaptor.add_child( root_0, l.tree )

        char_literal22 = match( T__12, TOKENS_FOLLOWING_T__12_IN_single_expression_334 )
        tree_for_char_literal22 = @adaptor.create_with_payload( char_literal22 )
        @adaptor.add_child( root_0, tree_for_char_literal22 )


        @state.following.push( TOKENS_FOLLOWING_literal_IN_single_expression_338 )
        r = literal
        @state.following.pop
        @adaptor.add_child( root_0, r.tree )

        char_literal23 = match( T__11, TOKENS_FOLLOWING_T__11_IN_single_expression_340 )
        tree_for_char_literal23 = @adaptor.create_with_payload( char_literal23 )
        @adaptor.add_child( root_0, tree_for_char_literal23 )



        # --> action
         return_value.value = ( l.nil? ? nil : l.value ).nil? == false && ( r.nil? ? nil : r.value ).nil? == false && ( l.nil? ? nil : l.value ).to_f < ( r.nil? ? nil : r.value ).to_f 
        # <-- action


      when 5
        root_0 = @adaptor.create_flat_list


        # at line 57:7: 'lessThanEqual(' l= literal ',' r= literal ')'
        string_literal24 = match( T__25, TOKENS_FOLLOWING_T__25_IN_single_expression_350 )
        tree_for_string_literal24 = @adaptor.create_with_payload( string_literal24 )
        @adaptor.add_child( root_0, tree_for_string_literal24 )


        @state.following.push( TOKENS_FOLLOWING_literal_IN_single_expression_354 )
        l = literal
        @state.following.pop
        @adaptor.add_child( root_0, l.tree )

        char_literal25 = match( T__12, TOKENS_FOLLOWING_T__12_IN_single_expression_356 )
        tree_for_char_literal25 = @adaptor.create_with_payload( char_literal25 )
        @adaptor.add_child( root_0, tree_for_char_literal25 )


        @state.following.push( TOKENS_FOLLOWING_literal_IN_single_expression_360 )
        r = literal
        @state.following.pop
        @adaptor.add_child( root_0, r.tree )

        char_literal26 = match( T__11, TOKENS_FOLLOWING_T__11_IN_single_expression_362 )
        tree_for_char_literal26 = @adaptor.create_with_payload( char_literal26 )
        @adaptor.add_child( root_0, tree_for_char_literal26 )



        # --> action
         return_value.value = ( l.nil? ? nil : l.value ).nil? == false && ( r.nil? ? nil : r.value ).nil? == false && ( l.nil? ? nil : l.value ).to_f <= ( r.nil? ? nil : r.value ).to_f 
        # <-- action


      when 6
        root_0 = @adaptor.create_flat_list


        # at line 58:7: 'between(' l= literal ',' min= literal ',' max= literal ')'
        string_literal27 = match( T__16, TOKENS_FOLLOWING_T__16_IN_single_expression_372 )
        tree_for_string_literal27 = @adaptor.create_with_payload( string_literal27 )
        @adaptor.add_child( root_0, tree_for_string_literal27 )


        @state.following.push( TOKENS_FOLLOWING_literal_IN_single_expression_376 )
        l = literal
        @state.following.pop
        @adaptor.add_child( root_0, l.tree )

        char_literal28 = match( T__12, TOKENS_FOLLOWING_T__12_IN_single_expression_378 )
        tree_for_char_literal28 = @adaptor.create_with_payload( char_literal28 )
        @adaptor.add_child( root_0, tree_for_char_literal28 )


        @state.following.push( TOKENS_FOLLOWING_literal_IN_single_expression_382 )
        min = literal
        @state.following.pop
        @adaptor.add_child( root_0, min.tree )

        char_literal29 = match( T__12, TOKENS_FOLLOWING_T__12_IN_single_expression_384 )
        tree_for_char_literal29 = @adaptor.create_with_payload( char_literal29 )
        @adaptor.add_child( root_0, tree_for_char_literal29 )


        @state.following.push( TOKENS_FOLLOWING_literal_IN_single_expression_388 )
        max = literal
        @state.following.pop
        @adaptor.add_child( root_0, max.tree )

        char_literal30 = match( T__11, TOKENS_FOLLOWING_T__11_IN_single_expression_390 )
        tree_for_char_literal30 = @adaptor.create_with_payload( char_literal30 )
        @adaptor.add_child( root_0, tree_for_char_literal30 )



        # --> action
         return_value.value = ( l.nil? ? nil : l.value ).nil? == false && ( min.nil? ? nil : min.value ).nil? == false && ( max.nil? ? nil : max.value ).nil? == false && ( l.nil? ? nil : l.value ).to_f >= ( min.nil? ? nil : min.value ).to_f && ( l.nil? ? nil : l.value ).to_f <= ( max.nil? ? nil : max.value ).to_f 
        # <-- action


      when 7
        root_0 = @adaptor.create_flat_list


        # at line 59:7: 'not(' e= single_expression ')'
        string_literal31 = match( T__26, TOKENS_FOLLOWING_T__26_IN_single_expression_400 )
        tree_for_string_literal31 = @adaptor.create_with_payload( string_literal31 )
        @adaptor.add_child( root_0, tree_for_string_literal31 )


        @state.following.push( TOKENS_FOLLOWING_single_expression_IN_single_expression_404 )
        e = single_expression
        @state.following.pop
        @adaptor.add_child( root_0, e.tree )

        char_literal32 = match( T__11, TOKENS_FOLLOWING_T__11_IN_single_expression_406 )
        tree_for_char_literal32 = @adaptor.create_with_payload( char_literal32 )
        @adaptor.add_child( root_0, tree_for_char_literal32 )



        # --> action
         
                    if ( e.nil? ? nil : e.value )
                        return_value.value = false
                    else
                        return_value.value = true
                    end  
                
        # <-- action


      when 8
        root_0 = @adaptor.create_flat_list


        # at line 67:7: 'in(' v= literal ',' l= list ')'
        string_literal33 = match( T__23, TOKENS_FOLLOWING_T__23_IN_single_expression_425 )
        tree_for_string_literal33 = @adaptor.create_with_payload( string_literal33 )
        @adaptor.add_child( root_0, tree_for_string_literal33 )


        @state.following.push( TOKENS_FOLLOWING_literal_IN_single_expression_429 )
        v = literal
        @state.following.pop
        @adaptor.add_child( root_0, v.tree )

        char_literal34 = match( T__12, TOKENS_FOLLOWING_T__12_IN_single_expression_431 )
        tree_for_char_literal34 = @adaptor.create_with_payload( char_literal34 )
        @adaptor.add_child( root_0, tree_for_char_literal34 )


        @state.following.push( TOKENS_FOLLOWING_list_IN_single_expression_435 )
        l = list
        @state.following.pop
        @adaptor.add_child( root_0, l.tree )

        char_literal35 = match( T__11, TOKENS_FOLLOWING_T__11_IN_single_expression_437 )
        tree_for_char_literal35 = @adaptor.create_with_payload( char_literal35 )
        @adaptor.add_child( root_0, tree_for_char_literal35 )



        # --> action

                    return_value.value = ( l.nil? ? nil : l.value ).include?(( v.nil? ? nil : v.value ))
                
        # <-- action


      when 9
        root_0 = @adaptor.create_flat_list


        # at line 71:7: e= literal
        @state.following.push( TOKENS_FOLLOWING_literal_IN_single_expression_459 )
        e = literal
        @state.following.pop
        @adaptor.add_child( root_0, e.tree )


        # --> action
         return_value.value = ( e.nil? ? nil : e.value ) 
        # <-- action


      end
      # - - - - - - - rule clean up - - - - - - - -
      return_value.stop = @input.look( -1 )


      return_value.tree = @adaptor.rule_post_processing( root_0 )
      @adaptor.set_token_boundaries( return_value.tree, return_value.start, return_value.stop )


      rescue ANTLR3::Error::RecognitionError => re
        report_error(re)
        recover(re)
        return_value.tree = @adaptor.create_error_node( @input, return_value.start, @input.look(-1), re )


      ensure
        # -> uncomment the next line to manually enable rule tracing
        # trace_out( __method__, 5 )


      end

      return return_value
    end

    ListReturnValue = define_return_scope :value

    #
    # parser rule list
    #
    # (in Statement.g)
    # 74:1: list returns [value] : '[' l= literals ']' ;
    #
    def list
      # -> uncomment the next line to manually enable rule tracing
      # trace_in( __method__, 6 )


      return_value = ListReturnValue.new

      # $rule.start = the first token seen before matching
      return_value.start = @input.look


      root_0 = nil

      char_literal36 = nil
      char_literal37 = nil
      l = nil


      tree_for_char_literal36 = nil
      tree_for_char_literal37 = nil

      begin
      root_0 = @adaptor.create_flat_list


      # at line 75:7: '[' l= literals ']'
      char_literal36 = match( T__13, TOKENS_FOLLOWING_T__13_IN_list_482 )
      tree_for_char_literal36 = @adaptor.create_with_payload( char_literal36 )
      @adaptor.add_child( root_0, tree_for_char_literal36 )


      @state.following.push( TOKENS_FOLLOWING_literals_IN_list_486 )
      l = literals
      @state.following.pop
      @adaptor.add_child( root_0, l.tree )

      char_literal37 = match( T__14, TOKENS_FOLLOWING_T__14_IN_list_487 )
      tree_for_char_literal37 = @adaptor.create_with_payload( char_literal37 )
      @adaptor.add_child( root_0, tree_for_char_literal37 )



      # --> action
       return_value.value = ( l.nil? ? nil : l.value ) 
      # <-- action


      # - - - - - - - rule clean up - - - - - - - -
      return_value.stop = @input.look( -1 )


      return_value.tree = @adaptor.rule_post_processing( root_0 )
      @adaptor.set_token_boundaries( return_value.tree, return_value.start, return_value.stop )


      rescue ANTLR3::Error::RecognitionError => re
        report_error(re)
        recover(re)
        return_value.tree = @adaptor.create_error_node( @input, return_value.start, @input.look(-1), re )


      ensure
        # -> uncomment the next line to manually enable rule tracing
        # trace_out( __method__, 6 )


      end

      return return_value
    end

    LiteralsReturnValue = define_return_scope :value

    #
    # parser rule literals
    #
    # (in Statement.g)
    # 78:1: literals returns [value] : (l= literal ',' rest= literals |l= literal );
    #
    def literals
      # -> uncomment the next line to manually enable rule tracing
      # trace_in( __method__, 7 )


      return_value = LiteralsReturnValue.new

      # $rule.start = the first token seen before matching
      return_value.start = @input.look


      root_0 = nil

      char_literal38 = nil
      l = nil
      rest = nil


      tree_for_char_literal38 = nil

      begin
      # at line 79:5: (l= literal ',' rest= literals |l= literal )
      alt_6 = 2
      case look_6 = @input.peek( 1 )
      when STRING then look_6_1 = @input.peek( 2 )

      if ( look_6_1 == T__12 )
        alt_6 = 1
      elsif ( look_6_1 == T__14 )
        alt_6 = 2
      else
        raise NoViableAlternative( "", 6, 1 )

      end
      when VARIABLE then look_6_2 = @input.peek( 2 )

      if ( look_6_2 == T__12 )
        alt_6 = 1
      elsif ( look_6_2 == T__14 )
        alt_6 = 2
      else
        raise NoViableAlternative( "", 6, 2 )

      end
      when NUMBER then look_6_3 = @input.peek( 2 )

      if ( look_6_3 == T__12 )
        alt_6 = 1
      elsif ( look_6_3 == T__14 )
        alt_6 = 2
      else
        raise NoViableAlternative( "", 6, 3 )

      end
      when INT then look_6_4 = @input.peek( 2 )

      if ( look_6_4 == T__12 )
        alt_6 = 1
      elsif ( look_6_4 == T__14 )
        alt_6 = 2
      else
        raise NoViableAlternative( "", 6, 4 )

      end
      else
        raise NoViableAlternative( "", 6, 0 )

      end
      case alt_6
      when 1
        root_0 = @adaptor.create_flat_list


        # at line 79:7: l= literal ',' rest= literals
        @state.following.push( TOKENS_FOLLOWING_literal_IN_literals_512 )
        l = literal
        @state.following.pop
        @adaptor.add_child( root_0, l.tree )

        char_literal38 = match( T__12, TOKENS_FOLLOWING_T__12_IN_literals_514 )
        tree_for_char_literal38 = @adaptor.create_with_payload( char_literal38 )
        @adaptor.add_child( root_0, tree_for_char_literal38 )


        @state.following.push( TOKENS_FOLLOWING_literals_IN_literals_518 )
        rest = literals
        @state.following.pop
        @adaptor.add_child( root_0, rest.tree )


        # --> action
         return_value.value = ( rest.nil? ? nil : rest.value ).push(( l.nil? ? nil : l.value )) 
        # <-- action


      when 2
        root_0 = @adaptor.create_flat_list


        # at line 80:7: l= literal
        @state.following.push( TOKENS_FOLLOWING_literal_IN_literals_530 )
        l = literal
        @state.following.pop
        @adaptor.add_child( root_0, l.tree )


        # --> action
         return_value.value = [( l.nil? ? nil : l.value )] 
        # <-- action


      end
      # - - - - - - - rule clean up - - - - - - - -
      return_value.stop = @input.look( -1 )


      return_value.tree = @adaptor.rule_post_processing( root_0 )
      @adaptor.set_token_boundaries( return_value.tree, return_value.start, return_value.stop )


      rescue ANTLR3::Error::RecognitionError => re
        report_error(re)
        recover(re)
        return_value.tree = @adaptor.create_error_node( @input, return_value.start, @input.look(-1), re )


      ensure
        # -> uncomment the next line to manually enable rule tracing
        # trace_out( __method__, 7 )


      end

      return return_value
    end

    LiteralReturnValue = define_return_scope :value

    #
    # parser rule literal
    #
    # (in Statement.g)
    # 83:1: literal returns [value] : (s= STRING |v= VARIABLE |n= NUMBER |i= INT );
    #
    def literal
      # -> uncomment the next line to manually enable rule tracing
      # trace_in( __method__, 8 )


      return_value = LiteralReturnValue.new

      # $rule.start = the first token seen before matching
      return_value.start = @input.look


      root_0 = nil

      s = nil
      v = nil
      n = nil
      i = nil


      tree_for_s = nil
      tree_for_v = nil
      tree_for_n = nil
      tree_for_i = nil

      begin
      # at line 84:5: (s= STRING |v= VARIABLE |n= NUMBER |i= INT )
      alt_7 = 4
      case look_7 = @input.peek( 1 )
      when STRING then alt_7 = 1
      when VARIABLE then alt_7 = 2
      when NUMBER then alt_7 = 3
      when INT then alt_7 = 4
      else
        raise NoViableAlternative( "", 7, 0 )

      end
      case alt_7
      when 1
        root_0 = @adaptor.create_flat_list


        # at line 84:7: s= STRING
        s = match( STRING, TOKENS_FOLLOWING_STRING_IN_literal_555 )
        tree_for_s = @adaptor.create_with_payload( s )
        @adaptor.add_child( root_0, tree_for_s )



        # --> action
         return_value.value = s.value 
        # <-- action


      when 2
        root_0 = @adaptor.create_flat_list


        # at line 85:7: v= VARIABLE
        v = match( VARIABLE, TOKENS_FOLLOWING_VARIABLE_IN_literal_567 )
        tree_for_v = @adaptor.create_with_payload( v )
        @adaptor.add_child( root_0, tree_for_v )



        # --> action
         return_value.value = $argument_mapper.get_value(v.text) 
        # <-- action


      when 3
        root_0 = @adaptor.create_flat_list


        # at line 86:7: n= NUMBER
        n = match( NUMBER, TOKENS_FOLLOWING_NUMBER_IN_literal_579 )
        tree_for_n = @adaptor.create_with_payload( n )
        @adaptor.add_child( root_0, tree_for_n )



        # --> action
         return_value.value = n.value 
        # <-- action


      when 4
        root_0 = @adaptor.create_flat_list


        # at line 87:7: i= INT
        i = match( INT, TOKENS_FOLLOWING_INT_IN_literal_591 )
        tree_for_i = @adaptor.create_with_payload( i )
        @adaptor.add_child( root_0, tree_for_i )



        # --> action
         return_value.value = i.value 
        # <-- action


      end
      # - - - - - - - rule clean up - - - - - - - -
      return_value.stop = @input.look( -1 )


      return_value.tree = @adaptor.rule_post_processing( root_0 )
      @adaptor.set_token_boundaries( return_value.tree, return_value.start, return_value.stop )


      rescue ANTLR3::Error::RecognitionError => re
        report_error(re)
        recover(re)
        return_value.tree = @adaptor.create_error_node( @input, return_value.start, @input.look(-1), re )


      ensure
        # -> uncomment the next line to manually enable rule tracing
        # trace_out( __method__, 8 )


      end

      return return_value
    end



    TOKENS_FOLLOWING_statement_IN_program_56 = Set[ 1 ]
    TOKENS_FOLLOWING_T__22_IN_statement_79 = Set[ 5, 7, 9, 10, 15, 16, 19, 20, 21, 23, 24, 25, 26, 27 ]
    TOKENS_FOLLOWING_multi_expression_IN_statement_83 = Set[ 28 ]
    TOKENS_FOLLOWING_T__28_IN_statement_85 = Set[ 5, 7, 9, 10 ]
    TOKENS_FOLLOWING_literal_IN_statement_89 = Set[ 1, 17, 18 ]
    TOKENS_FOLLOWING_next_statement_IN_statement_93 = Set[ 1 ]
    TOKENS_FOLLOWING_T__18_IN_next_statement_126 = Set[ 5, 7, 9, 10, 15, 16, 19, 20, 21, 23, 24, 25, 26, 27 ]
    TOKENS_FOLLOWING_multi_expression_IN_next_statement_130 = Set[ 28 ]
    TOKENS_FOLLOWING_T__28_IN_next_statement_132 = Set[ 5, 7, 9, 10 ]
    TOKENS_FOLLOWING_literal_IN_next_statement_136 = Set[ 1, 17, 18 ]
    TOKENS_FOLLOWING_next_statement_IN_next_statement_140 = Set[ 1 ]
    TOKENS_FOLLOWING_T__17_IN_next_statement_159 = Set[ 5, 7, 9, 10 ]
    TOKENS_FOLLOWING_literal_IN_next_statement_163 = Set[ 1 ]
    TOKENS_FOLLOWING_T__15_IN_multi_expression_194 = Set[ 5, 7, 9, 10, 16, 19, 20, 21, 23, 24, 25, 26 ]
    TOKENS_FOLLOWING_single_expression_IN_multi_expression_198 = Set[ 12 ]
    TOKENS_FOLLOWING_T__12_IN_multi_expression_200 = Set[ 5, 7, 9, 10, 15, 16, 19, 20, 21, 23, 24, 25, 26, 27 ]
    TOKENS_FOLLOWING_multi_expression_IN_multi_expression_204 = Set[ 11 ]
    TOKENS_FOLLOWING_T__11_IN_multi_expression_206 = Set[ 1 ]
    TOKENS_FOLLOWING_T__27_IN_multi_expression_216 = Set[ 5, 7, 9, 10, 16, 19, 20, 21, 23, 24, 25, 26 ]
    TOKENS_FOLLOWING_single_expression_IN_multi_expression_220 = Set[ 12 ]
    TOKENS_FOLLOWING_T__12_IN_multi_expression_222 = Set[ 5, 7, 9, 10, 15, 16, 19, 20, 21, 23, 24, 25, 26, 27 ]
    TOKENS_FOLLOWING_multi_expression_IN_multi_expression_226 = Set[ 11 ]
    TOKENS_FOLLOWING_T__11_IN_multi_expression_228 = Set[ 1 ]
    TOKENS_FOLLOWING_single_expression_IN_multi_expression_240 = Set[ 1 ]
    TOKENS_FOLLOWING_T__19_IN_single_expression_263 = Set[ 5, 7, 9, 10 ]
    TOKENS_FOLLOWING_literal_IN_single_expression_267 = Set[ 12 ]
    TOKENS_FOLLOWING_T__12_IN_single_expression_269 = Set[ 5, 7, 9, 10 ]
    TOKENS_FOLLOWING_literal_IN_single_expression_273 = Set[ 11 ]
    TOKENS_FOLLOWING_T__11_IN_single_expression_275 = Set[ 1 ]
    TOKENS_FOLLOWING_T__20_IN_single_expression_285 = Set[ 5, 7, 9, 10 ]
    TOKENS_FOLLOWING_literal_IN_single_expression_289 = Set[ 12 ]
    TOKENS_FOLLOWING_T__12_IN_single_expression_291 = Set[ 5, 7, 9, 10 ]
    TOKENS_FOLLOWING_literal_IN_single_expression_295 = Set[ 11 ]
    TOKENS_FOLLOWING_T__11_IN_single_expression_297 = Set[ 1 ]
    TOKENS_FOLLOWING_T__21_IN_single_expression_307 = Set[ 5, 7, 9, 10 ]
    TOKENS_FOLLOWING_literal_IN_single_expression_310 = Set[ 12 ]
    TOKENS_FOLLOWING_T__12_IN_single_expression_312 = Set[ 5, 7, 9, 10 ]
    TOKENS_FOLLOWING_literal_IN_single_expression_316 = Set[ 11 ]
    TOKENS_FOLLOWING_T__11_IN_single_expression_318 = Set[ 1 ]
    TOKENS_FOLLOWING_T__24_IN_single_expression_328 = Set[ 5, 7, 9, 10 ]
    TOKENS_FOLLOWING_literal_IN_single_expression_332 = Set[ 12 ]
    TOKENS_FOLLOWING_T__12_IN_single_expression_334 = Set[ 5, 7, 9, 10 ]
    TOKENS_FOLLOWING_literal_IN_single_expression_338 = Set[ 11 ]
    TOKENS_FOLLOWING_T__11_IN_single_expression_340 = Set[ 1 ]
    TOKENS_FOLLOWING_T__25_IN_single_expression_350 = Set[ 5, 7, 9, 10 ]
    TOKENS_FOLLOWING_literal_IN_single_expression_354 = Set[ 12 ]
    TOKENS_FOLLOWING_T__12_IN_single_expression_356 = Set[ 5, 7, 9, 10 ]
    TOKENS_FOLLOWING_literal_IN_single_expression_360 = Set[ 11 ]
    TOKENS_FOLLOWING_T__11_IN_single_expression_362 = Set[ 1 ]
    TOKENS_FOLLOWING_T__16_IN_single_expression_372 = Set[ 5, 7, 9, 10 ]
    TOKENS_FOLLOWING_literal_IN_single_expression_376 = Set[ 12 ]
    TOKENS_FOLLOWING_T__12_IN_single_expression_378 = Set[ 5, 7, 9, 10 ]
    TOKENS_FOLLOWING_literal_IN_single_expression_382 = Set[ 12 ]
    TOKENS_FOLLOWING_T__12_IN_single_expression_384 = Set[ 5, 7, 9, 10 ]
    TOKENS_FOLLOWING_literal_IN_single_expression_388 = Set[ 11 ]
    TOKENS_FOLLOWING_T__11_IN_single_expression_390 = Set[ 1 ]
    TOKENS_FOLLOWING_T__26_IN_single_expression_400 = Set[ 5, 7, 9, 10, 16, 19, 20, 21, 23, 24, 25, 26 ]
    TOKENS_FOLLOWING_single_expression_IN_single_expression_404 = Set[ 11 ]
    TOKENS_FOLLOWING_T__11_IN_single_expression_406 = Set[ 1 ]
    TOKENS_FOLLOWING_T__23_IN_single_expression_425 = Set[ 5, 7, 9, 10 ]
    TOKENS_FOLLOWING_literal_IN_single_expression_429 = Set[ 12 ]
    TOKENS_FOLLOWING_T__12_IN_single_expression_431 = Set[ 13 ]
    TOKENS_FOLLOWING_list_IN_single_expression_435 = Set[ 11 ]
    TOKENS_FOLLOWING_T__11_IN_single_expression_437 = Set[ 1 ]
    TOKENS_FOLLOWING_literal_IN_single_expression_459 = Set[ 1 ]
    TOKENS_FOLLOWING_T__13_IN_list_482 = Set[ 5, 7, 9, 10 ]
    TOKENS_FOLLOWING_literals_IN_list_486 = Set[ 14 ]
    TOKENS_FOLLOWING_T__14_IN_list_487 = Set[ 1 ]
    TOKENS_FOLLOWING_literal_IN_literals_512 = Set[ 12 ]
    TOKENS_FOLLOWING_T__12_IN_literals_514 = Set[ 5, 7, 9, 10 ]
    TOKENS_FOLLOWING_literals_IN_literals_518 = Set[ 1 ]
    TOKENS_FOLLOWING_literal_IN_literals_530 = Set[ 1 ]
    TOKENS_FOLLOWING_STRING_IN_literal_555 = Set[ 1 ]
    TOKENS_FOLLOWING_VARIABLE_IN_literal_567 = Set[ 1 ]
    TOKENS_FOLLOWING_NUMBER_IN_literal_579 = Set[ 1 ]
    TOKENS_FOLLOWING_INT_IN_literal_591 = Set[ 1 ]

  end # class Parser < ANTLR3::Parser

  at_exit { Parser.main( ARGV ) } if __FILE__ == $0

end
