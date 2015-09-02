<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns    ="http://www.w3.org/2002/xforms"
                xmlns:ev ="http://www.w3.org/2001/xml-events"
                xmlns:h  ="http://www.w3.org/1999/xhtml"
                xmlns:jr ="http://openrosa.org/javarosa"
                xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                version="1.0">
  <xsl:output method="xml" indent="yes"/>

  <xsl:variable name="valid-in-label" select="'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789- '" />
  <xsl:variable name="smallcase"      select="'abcdefghijklmnopqrstuvwxyz'" />
  <xsl:variable name="uppercase"      select="'ABCDEFGHIJKLMNOPQRSTUVWXYZ'" />
  <xsl:variable name="doWarn"         select="not(/module/@suppressWarnings = 'true')" />

  <xsl:template match="/">
    <h:html>
      <h:head>
        <h:title>Fill This In</h:title>
        <model>
          <instance>
            <faims id="Fill_This_In">
              <style>
                <orientation>
                  <orientation/>
                </orientation>
                <even>
                  <layout_weight/>
                </even>
                <large>
                  <layout_weight/>
                </large>
              </style>
              <xsl:call-template name="model"/>
            </faims>
          </instance>
          <xsl:call-template name="bindings"/>
        </model>
      </h:head>
      <h:body>
        <group ref="style">
          <label/>
          <group ref="orientation">
            <label/>
            <input ref="orientation">
              <label>horizontal</label>
            </input>
          </group>
          <group ref="even">
            <label/>
            <input ref="layout_weight">
              <label>1</label>
            </input>
          </group>
          <group ref="large">
            <label/>
            <input ref="layout_weight">
              <label>3</label>
            </input>
          </group>
        </group>
        <xsl:call-template name="body"/>
      </h:body>
    </h:html>
  </xsl:template>

  <xsl:template name="model">
    <xsl:for-each select="/module/*">                                  <!-- Iterate over tab group nodes -->
      <xsl:element name="{name()}">
        <xsl:for-each select="*">                                      <!-- Iterate over tab nodes -->
          <xsl:if test="not(translate(name(), $smallcase, '') = '')"> <!-- Skip nodes with "reserved" names (i.e. all lower case letters -->
            <xsl:if test="
              contains(translate(name(), $uppercase, $smallcase), 'search') or
              contains(translate(name(), $uppercase, $smallcase), 'records')">
              <xsl:comment>WARNING:  __                                                        </xsl:comment>
              <xsl:comment>WARNING: /  \        _____________________________________________  </xsl:comment>
              <xsl:comment>WARNING: |  |       /                                             \ </xsl:comment>
              <xsl:comment>WARNING: @  @       | It looks like you are implementing a search | </xsl:comment>
              <xsl:comment>WARNING: || ||   ___| feature. Would you like help? (You can use  | </xsl:comment>
              <xsl:comment>WARNING: || ||  /   | the built-in "search" tag here to add a tab | </xsl:comment>
              <xsl:comment>WARNING: |\_/|      | which searches all arch-ents.)              | </xsl:comment>
              <xsl:comment>WARNING: \___/      \_____________________________________________/ </xsl:comment>
            </xsl:if>
            <xsl:element name="{name()}">
              <xsl:for-each select="*">                         <!-- Iterate over GUI elements -->
                <xsl:call-template name="model-expand-reserved-or-view"/>
              </xsl:for-each>
            </xsl:element>
          </xsl:if>
          <xsl:if test="name() = 'search'">
            <Search>
              <Colgroup_0>
                <Col_0>
                  <Search_Term/>
                </Col_0>
                <Col_1>
                  <Search_Button/>
                </Col_1>
              </Colgroup_0>
              <xsl:if test="count(/module/*[not(contains(@f, 'nodata')) and not(name() = 'rels') and (./*//*[not(ancestor-or-self::*[contains(@f, 'nodata') or contains(@f, 'user')]) and not(name() = 'cols') and not(name() = 'col') and not(name() = 'desc') and not(name() = 'opt') and not(name() = 'opts') and not(ancestor-or-self::rels) and not(normalize-space(@t) = 'group') and not(normalize-space(@t) = 'gpsdiag') and not(normalize-space(@t) = 'map') and not(normalize-space(@t) = 'button')])]) &gt;= 2">
                <Entity_Types/>
              </xsl:if>
              <Entity_List/>
            </Search>
          </xsl:if>
        </xsl:for-each>
      </xsl:element>
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="bindings">
    <xsl:for-each select="/module/*">                                <!-- Iterate over tab group nodes -->
      <xsl:for-each select="*">                                      <!-- Iterate over tab nodes -->
        <xsl:if test="not(translate(name(), $smallcase, '') = '')"> <!-- Skip nodes with "reserved" names (i.e. all lower case letters -->
          <xsl:for-each select="*">                                  <!-- Iterate over GUI elements -->
            <xsl:call-template name="bind-expand-reserved-or-view"/>
          </xsl:for-each>
        </xsl:if>
      </xsl:for-each>
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="body">
    <xsl:for-each select="/module/*">                                <!-- Iterate over tab group nodes -->
      <xsl:element name="group">
        <xsl:attribute name="ref">
          <xsl:value-of select="name()"/>
        </xsl:attribute>
        <xsl:if test="not(ancestor-or-self::*[contains(@f, 'nodata')])">
          <xsl:attribute name="faims_archent_type">
            <xsl:call-template name="string-replace-all">
              <xsl:with-param name="text" select="name()" />
              <xsl:with-param name="replace" select="'_'" />
              <xsl:with-param name="by" select="' '" />
            </xsl:call-template>
          </xsl:attribute>
        </xsl:if>
        <xsl:call-template name="label" />
        <xsl:for-each select="*">                                      <!-- Iterate over tab nodes -->
          <xsl:if test="not(translate(name(), $smallcase, '') = '')"> <!-- Skip nodes with "reserved" names (i.e. all lower case letters -->
            <xsl:element name="group">
              <xsl:attribute name="ref"><xsl:value-of select="name()"/></xsl:attribute>
              <xsl:if test=".//*[normalize-space(@t) = 'map']">
                <xsl:attribute name="faims_scrollable">false</xsl:attribute>
              </xsl:if>
              <xsl:call-template name="parse-flags">
                <xsl:with-param name="flags" select="@f" />
              </xsl:call-template>
              <xsl:call-template name="label" />
              <xsl:for-each select="*[not(contains(@f, 'noui'))]"> <!-- Iterate over GUI elements -->
                <xsl:call-template name="body-expand-reserved-or-view"/>
              </xsl:for-each>
            </xsl:element>
          </xsl:if>
          <xsl:if test="name() = 'search'">
            <group ref="Search" faims_scrollable="false">
              <xsl:if test="../Search">
                <xsl:comment>ERROR: View name is duplicated such that this UI schema is invalid</xsl:comment>
              </xsl:if>
              <xsl:if test="count(//search) &gt; 1">
                <xsl:comment>ERROR: View name is duplicated such that this UI schema is invalid</xsl:comment>
              </xsl:if>
              <xsl:call-template name="label"/>
              <group faims_style="orientation" ref="Colgroup_0">
                <label/>
                <group faims_style="even" ref="Col_0">
                  <label/>
                  <input ref="Search_Term">
                    <label>{Search_Term}</label>
                  </input>
                </group>
                <group faims_style="large" ref="Col_1">
                  <label/>
                  <trigger ref="Search_Button">
                    <label>{Search}</label>
                  </trigger>
                </group>
              </group>
              <xsl:if test="count(/module/*[not(contains(@f, 'nodata')) and not(name() = 'rels') and (./*//*[not(ancestor-or-self::*[contains(@f, 'nodata') or contains(@f, 'user')]) and not(name() = 'cols') and not(name() = 'col') and not(name() = 'desc') and not(name() = 'opt') and not(name() = 'opts') and not(ancestor-or-self::rels) and not(normalize-space(@t) = 'group') and not(normalize-space(@t) = 'gpsdiag') and not(normalize-space(@t) = 'map') and not(normalize-space(@t) = 'button')])]) &gt;= 2">
                <select1 ref="Entity_Types">
                  <label>{Entity_Types}</label>
                  <item>
                    <label>Options not loaded</label>
                    <value>Options not loaded</value>
                  </item>
                </select1>
              </xsl:if>
              <select1 appearance="compact" ref="Entity_List">
                <label>{Entity_List}</label>
                <item>
                  <label>Options not loaded</label>
                  <value>Options not loaded</value>
                </item>
              </select1>
            </group>
          </xsl:if>
        </xsl:for-each>
      </xsl:element>
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="model-expand-reserved-or-view">
    <xsl:choose>
      <xsl:when test="name() = 'author'">
        <xsl:call-template name="model-expand-author" />
      </xsl:when>
      <xsl:when test="name() = 'autonum'">
        <xsl:call-template name="model-expand-autonum" />
      </xsl:when>
      <xsl:when test="name() = 'cols'">
        <xsl:call-template name="model-expand-cols" />
      </xsl:when>
      <xsl:when test="name() = 'gps'">
        <xsl:call-template name="model-expand-gps" />
      </xsl:when>
      <xsl:when test="name() = 'timestamp'">
        <xsl:call-template name="model-expand-timestamp" />
      </xsl:when>
      <xsl:otherwise>
        <xsl:call-template name="model-expand-view" />
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template name="model-expand-author">
    <Author/>
  </xsl:template>

  <xsl:template name="model-expand-timestamp">
    <Timestamp/>
  </xsl:template>

  <xsl:template name="model-expand-autonum">
    <xsl:for-each select="//*[contains(@f, 'autonum')]">
      <xsl:element name="Next_{name()}"/>
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="model-expand-view">
    <xsl:element name="{name()}"/>
    <xsl:if test="normalize-space(@t) = 'audio'
      or normalize-space(@t) = 'camera'
      or normalize-space(@t) = 'file'
      or normalize-space(@t) = 'video'">
      <xsl:element name="Button_{name()}"/>
    </xsl:if>
  </xsl:template>

  <xsl:template name="model-expand-gps">
    <Colgroup_GPS>
      <Col_0>
        <Latitude/>
        <Northing/>
      </Col_0>
      <Col_1>
        <Longitude/>
        <Easting/>
      </Col_1>
    </Colgroup_GPS>
    <Take_From_GPS/>
  </xsl:template>

  <xsl:template name="model-expand-cols">
    <xsl:element name="Colgroup_{count(./preceding-sibling::cols)}">
      <xsl:for-each select="*">
        <xsl:element name="Col_{count(./preceding-sibling::*)}">
          <xsl:choose>
            <xsl:when test="name() = 'col'">
                <xsl:for-each select="*">
                  <xsl:element name="{name(.)}"/>
                </xsl:for-each>
            </xsl:when>
            <xsl:otherwise>
                <xsl:element name="{name(.)}"/>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:element>
      </xsl:for-each>
    </xsl:element>
  </xsl:template>

  <xsl:template name="bind-expand-reserved-or-view">
    <xsl:choose>
      <xsl:when test="name(.) = 'autonum'">
        <xsl:call-template name="bind-expand-autonum" />
      </xsl:when>
      <xsl:when test="name(.) = 'cols'">
        <xsl:call-template name="bind-expand-cols" />
      </xsl:when>
      <xsl:otherwise>
        <xsl:call-template name="bind-expand-view" />
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template name="bind-expand-autonum">
    <xsl:for-each select="//*[contains(@f, 'autonum')]">
      <xsl:element name="bind">
        <xsl:attribute name="type">decimal</xsl:attribute>
        <xsl:attribute name="nodeset">
          <xsl:text>/faims/</xsl:text>
          <xsl:value-of select="name(//autonum/ancestor::*[last()-1])"/>
          <xsl:text>/</xsl:text>
          <xsl:value-of select="name(//autonum/ancestor::*[last()-2])"/>
          <xsl:text>/Next_</xsl:text>
          <xsl:value-of select="name()"/>
        </xsl:attribute>
      </xsl:element>
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="bind-expand-cols">
    <xsl:for-each select=".//*[@b or contains(@f, 'autonum')]">
      <xsl:if test="$doWarn and @b and contains(@f, 'autonum')">
        <xsl:comment>WARNING: Binding in b attribute ignored; use of "autonum" flag forces decimal binding</xsl:comment>
      </xsl:if>
      <xsl:element name="bind">
        <xsl:attribute name="type">
          <xsl:choose>
            <xsl:when test="contains(@f, 'autonum')">
              <xsl:text>decimal</xsl:text>
            </xsl:when>
            <xsl:otherwise>
              <xsl:value-of select="normalize-space(@b)"/>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:attribute>
        <xsl:choose>
          <xsl:when test="./ancestor::col">
            <xsl:attribute name="nodeset">
              <xsl:text>/faims/</xsl:text>
              <xsl:value-of select="name(ancestor::*[last()-1])"/>
              <xsl:text>/</xsl:text>
              <xsl:value-of select="name(ancestor::*[last()-2])"/>
              <xsl:text>/Colgroup_</xsl:text>
              <xsl:value-of select="count(./ancestor::cols[1]/preceding-sibling::cols)"/>
              <xsl:text>/Col_</xsl:text>
              <xsl:value-of select="count(./ancestor::col[1]/preceding-sibling::*)"/>
              <xsl:text>/</xsl:text>
              <xsl:value-of select="name()"/>
            </xsl:attribute>
          </xsl:when>
          <xsl:otherwise>
            <xsl:attribute name="nodeset">
              <xsl:text>/faims/</xsl:text>
              <xsl:value-of select="name(ancestor::*[last()-1])"/>
              <xsl:text>/</xsl:text>
              <xsl:value-of select="name(ancestor::*[last()-2])"/>
              <xsl:text>/Colgroup_</xsl:text>
              <xsl:value-of select="count(./ancestor::cols[1]/preceding-sibling::cols)"/>
              <xsl:text>/Col_</xsl:text>
              <xsl:value-of select="count(./preceding-sibling::*)"/>
              <xsl:text>/</xsl:text>
              <xsl:value-of select="name()"/>
            </xsl:attribute>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:element>
      <xsl:if test="$doWarn and
            normalize-space(@b) != 'date' and
            normalize-space(@b) != 'decimal' and
            normalize-space(@b) != 'string' and
            normalize-space(@b) != 'time'
            ">
        <xsl:comment>WARNING: Unexpected binding "<xsl:value-of select="@b"/>"</xsl:comment>
      </xsl:if>
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="bind-expand-view">
    <xsl:if test="@b">
      <xsl:element name="bind">
        <xsl:attribute name="type">
          <xsl:value-of select="normalize-space(@b)"/>
        </xsl:attribute>
        <xsl:attribute name="nodeset">/faims/<xsl:value-of select="name(ancestor::*[last()-1])"/>/<xsl:value-of select="name(ancestor::*[last()-2])"/>/<xsl:value-of select="name()"/></xsl:attribute>
      </xsl:element>
      <xsl:if test="$doWarn and @b and contains(@f, 'autonum')">
        <xsl:comment>WARNING: Binding in b attribute ignored; use of "autonum" flag forces decimal binding</xsl:comment>
      </xsl:if>
      <xsl:if test="$doWarn and
        normalize-space(@b) != 'date' and
        normalize-space(@b) != 'decimal' and
        normalize-space(@b) != 'string' and
        normalize-space(@b) != 'time'
        ">
        <xsl:comment>WARNING: Unexpected binding "<xsl:value-of select="@b"/>"</xsl:comment>
      </xsl:if>
    </xsl:if>
    <xsl:if test="contains(@f, 'autonum')">
      <xsl:element name="bind">
        <xsl:attribute name="type">decimal</xsl:attribute>
        <xsl:attribute name="nodeset">
          <xsl:text>/faims/</xsl:text>
          <xsl:value-of select="name(ancestor::*[last()-1])"/>
          <xsl:text>/</xsl:text>
          <xsl:value-of select="name(ancestor::*[last()-2])"/>
          <xsl:text>/</xsl:text>
          <xsl:value-of select="name()"/>
        </xsl:attribute>
      </xsl:element>
    </xsl:if>
  </xsl:template>

  <xsl:template name="body-expand-reserved-or-view">
    <xsl:choose>
      <xsl:when test="name(.) = 'author'">
        <xsl:call-template name="body-expand-author" />
      </xsl:when>
      <xsl:when test="name(.) = 'autonum'">
        <xsl:call-template name="body-expand-autonum" />
      </xsl:when>
      <xsl:when test="name(.) = 'gps'">
        <xsl:call-template name="body-expand-gps" />
      </xsl:when>
      <xsl:when test="name(.) = 'cols'">
        <xsl:call-template name="body-expand-cols" />
      </xsl:when>
      <xsl:when test="name(.) = 'timestamp'">
        <xsl:call-template name="body-expand-timestamp" />
      </xsl:when>
      <xsl:otherwise>
        <xsl:call-template name="body-expand-view" />
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template name="body-expand-author">
    <input ref="Author" faims_read_only="true" faims_annotation="false" faims_certainty="false">
      <xsl:call-template name="label" />
      <xsl:call-template name="warn-unexpected-attr" />
    </input>
  </xsl:template>

  <xsl:template name="body-expand-timestamp">
    <input ref="Timestamp" faims_read_only="true" faims_annotation="false" faims_certainty="false">
      <xsl:call-template name="label" />
      <xsl:call-template name="warn-unexpected-attr" />
    </input>
  </xsl:template>

  <xsl:template name="body-expand-autonum">
    <xsl:for-each select="//*[contains(@f, 'autonum')]">
      <xsl:element name="input">
        <xsl:attribute name="ref">
          <xsl:text>Next_</xsl:text>
          <xsl:value-of select="name()"/>
        </xsl:attribute>
        <xsl:attribute name="faims_style_class">
          <xsl:text>required</xsl:text>
        </xsl:attribute>
        <xsl:element name="label">
          <xsl:text>{Next_</xsl:text>
          <xsl:value-of select="name()"/>
          <xsl:text>}</xsl:text>
        </xsl:element>
      </xsl:element>
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="body-expand-gps">
    <group ref="Colgroup_GPS" faims_style="orientation">
      <xsl:call-template name="warn-unexpected-attr" />
      <label/>
      <group ref="Col_0" faims_style="even">
        <label/>
        <input ref="Latitude" faims_attribute_name="Latitude" faims_attribute_type="measure" faims_read_only="true">
          <xsl:if test="count(..//Latitude) &gt;= 1 or count(..//gps) &gt;= 2">
            <xsl:comment>ERROR: View name is duplicated such that this UI schema is invalid.</xsl:comment>
          </xsl:if>
          <label>{Latitude}</label>
        </input>
        <input ref="Northing" faims_attribute_name="Northing" faims_attribute_type="measure" faims_read_only="true">
          <xsl:if test="count(..//Northing) &gt;= 1 or count(..//gps) &gt;= 2">
            <xsl:comment>ERROR: View name is duplicated such that this UI schema is invalid.</xsl:comment>
          </xsl:if>
          <label>{Northing}</label>
        </input>
      </group>
      <group ref="Col_1" faims_style="even">
        <label/>
        <input ref="Longitude" faims_attribute_name="Longitude" faims_attribute_type="measure" faims_read_only="true">
          <xsl:if test="count(..//Longitude) &gt;= 1 or count(..//gps) &gt;= 2">
            <xsl:comment>ERROR: View name is duplicated such that this UI schema is invalid.</xsl:comment>
          </xsl:if>
          <label>{Longitude}</label>
        </input>
        <input ref="Easting" faims_attribute_name="Easting" faims_attribute_type="measure" faims_read_only="true">
          <xsl:if test="count(..//Easting) &gt;= 1 or count(..//gps) &gt;= 2">
            <xsl:comment>ERROR: View name is duplicated such that this UI schema is invalid.</xsl:comment>
          </xsl:if>
          <label>{Easting}</label>
        </input>
      </group>
    </group>
    <trigger ref="Take_From_GPS">
      <label>{Take_From_GPS}</label>
    </trigger>
  </xsl:template>

  <xsl:template name="body-expand-cols">
    <xsl:element name="group">
      <xsl:attribute name="ref">Colgroup_<xsl:value-of select="count(./preceding-sibling::cols)"/></xsl:attribute>
      <xsl:attribute name="faims_style">orientation</xsl:attribute>
      <xsl:call-template name="warn-unexpected-attr" />
      <label/>
      <xsl:for-each select="*">
        <xsl:element name="group">
          <xsl:attribute name="ref">Col_<xsl:value-of select="count(./preceding-sibling::*)"/></xsl:attribute>
          <xsl:attribute name="faims_style">even</xsl:attribute>
          <label/>
          <xsl:choose>
            <xsl:when test="name() = 'col'">
                <xsl:for-each select="*">
                  <xsl:call-template name="body-expand-view" />
                </xsl:for-each>
            </xsl:when>
            <xsl:otherwise>
              <xsl:call-template name="body-expand-view" />
            </xsl:otherwise>
          </xsl:choose>
        </xsl:element>
      </xsl:for-each>
    </xsl:element>
  </xsl:template>

  <xsl:template name="body-expand-view">
    <xsl:choose>
      <xsl:when test="normalize-space(@t)='audio'">
        <xsl:element name="select">
          <xsl:attribute name="type">file</xsl:attribute>
          <xsl:if test="not(ancestor-or-self::*[contains(@f, 'nodata')])">
            <xsl:attribute name="faims_attribute_type">measure</xsl:attribute>
          </xsl:if>
          <xsl:if test="not(ancestor-or-self::*[contains(@f, 'nosync')])">
            <xsl:attribute name="faims_sync">true</xsl:attribute>
          </xsl:if>
          <xsl:call-template name="body-expand-view-standard-nodes" />
          <item>
            <label>Options not loaded</label>
            <value>0</value>
          </item>
        </xsl:element>
        <trigger ref="Button_{name()}">
          <xsl:variable name="nodeName">Button_<xsl:value-of select="name()"/></xsl:variable>
          <xsl:if test="../*[name() = $nodeName]">
            <xsl:comment>ERROR: View name is duplicated such that this UI schema is invalid.</xsl:comment>
          </xsl:if>
          <label>{Button_<xsl:value-of select="name()"/>}</label>
        </trigger>
      </xsl:when>
      <xsl:when test="normalize-space(@t)='button'">
        <xsl:element name="trigger">
          <xsl:call-template name="body-expand-view-standard-nodes" />
        </xsl:element>
      </xsl:when>
      <xsl:when test="normalize-space(@t)='camera'">
        <xsl:element name="select">
          <xsl:attribute name="type">camera</xsl:attribute>
          <xsl:if test="not(ancestor-or-self::*[contains(@f, 'nodata')])">
            <xsl:attribute name="faims_attribute_type">measure</xsl:attribute>
          </xsl:if>
          <xsl:if test="not(ancestor-or-self::*[contains(@f, 'nosync')])">
            <xsl:attribute name="faims_sync">true</xsl:attribute>
          </xsl:if>
          <xsl:call-template name="body-expand-view-standard-nodes" />
          <item>
            <label>Options not loaded</label>
            <value>0</value>
          </item>
        </xsl:element>
        <trigger ref="Button_{name()}">
          <xsl:variable name="nodeName">Button_<xsl:value-of select="name()"/></xsl:variable>
          <xsl:if test="../*[name() = $nodeName]">
            <xsl:comment>ERROR: View name is duplicated such that this UI schema is invalid.</xsl:comment>
          </xsl:if>
          <label>{Button_<xsl:value-of select="name()"/>}</label>
        </trigger>
      </xsl:when>
      <xsl:when test="normalize-space(@t)='checkbox'">
        <xsl:element name="select">
          <xsl:if test="not(ancestor-or-self::*[contains(@f, 'nodata')])">
            <xsl:attribute name="faims_attribute_type">vocab</xsl:attribute>
          </xsl:if>
          <xsl:call-template name="body-expand-view-standard-nodes" />
          <item>
            <label>Options not loaded</label>
            <value>0</value>
          </item>
        </xsl:element>
      </xsl:when>
      <xsl:when test="normalize-space(@t)='dropdown' or (not(@t) and ./opts)">
        <xsl:element name="select1">
          <xsl:if test="not(ancestor-or-self::*[contains(@f, 'nodata')]) and not(@e) and not(@ec)">
            <xsl:attribute name="faims_attribute_type">vocab</xsl:attribute>
          </xsl:if>
          <xsl:call-template name="body-expand-view-standard-nodes" />
          <xsl:if test="$doWarn and not(@t)">
            <xsl:comment>WARNING: No type t was given for this view; assuming it is a dropdown</xsl:comment>
          </xsl:if>
          <item>
            <label>Options not loaded</label>
            <value>0</value>
          </item>
        </xsl:element>
      </xsl:when>
      <xsl:when test="normalize-space(@t)='file'">
        <xsl:element name="select">
          <xsl:attribute name="type">file</xsl:attribute>
          <xsl:if test="not(ancestor-or-self::*[contains(@f, 'nodata')])">
            <xsl:attribute name="faims_attribute_type">measure</xsl:attribute>
          </xsl:if>
          <xsl:if test="not(ancestor-or-self::*[contains(@f, 'nosync')])">
            <xsl:attribute name="faims_sync">true</xsl:attribute>
          </xsl:if>
          <xsl:call-template name="body-expand-view-standard-nodes" />
          <item>
            <label>Options not loaded</label>
            <value>0</value>
          </item>
        </xsl:element>
        <trigger ref="Button_{name()}">
          <xsl:variable name="nodeName">Button_<xsl:value-of select="name()"/></xsl:variable>
          <xsl:if test="../*[name() = $nodeName]">
            <xsl:comment>ERROR: View name is duplicated such that this UI schema is invalid.</xsl:comment>
          </xsl:if>
          <label>{Button_<xsl:value-of select="name()"/>}</label>
        </trigger>
      </xsl:when>
      <xsl:when test="normalize-space(@t)='gpsdiag'">
        <xsl:element name="input">
          <xsl:attribute name="faims_read_only">true</xsl:attribute>
          <xsl:call-template name="body-expand-view-standard-nodes" />
        </xsl:element>
      </xsl:when>
      <xsl:when test="normalize-space(@t)='group'">
        <xsl:element name="{normalize-space(@t)}">
          <xsl:call-template name="body-expand-view-standard-nodes" />
        </xsl:element>
      </xsl:when>
      <xsl:when test="normalize-space(@t)='input'">
        <xsl:element name="{normalize-space(@t)}">
          <xsl:if test="not(ancestor-or-self::*[contains(@f, 'nodata')])">
            <xsl:attribute name="faims_attribute_type">measure</xsl:attribute>
          </xsl:if>
          <xsl:call-template name="body-expand-view-standard-nodes" />
        </xsl:element>
      </xsl:when>
      <xsl:when test="normalize-space(@t)='list' or
        not(@t) and @e or
        not(@t) and @ec or
        not(@t) and contains(@f, 'user')">
        <xsl:element name="select1">
          <xsl:attribute name="appearance">compact</xsl:attribute>
          <xsl:call-template name="body-expand-view-standard-nodes" />
          <xsl:if test="$doWarn and not(@t)">
            <xsl:comment>WARNING: No type t was given for this view; assuming it is a list</xsl:comment>
          </xsl:if>
          <item>
            <label>Options not loaded</label>
            <value>0</value>
          </item>
        </xsl:element>
      </xsl:when>
      <xsl:when test="normalize-space(@t)='map'">
        <xsl:element name="input">
          <xsl:attribute name="faims_map">true</xsl:attribute>
          <xsl:call-template name="body-expand-view-standard-nodes" />
        </xsl:element>
      </xsl:when>
      <xsl:when test="normalize-space(@t)='picture'">
        <xsl:element name="select1">
          <xsl:attribute name="type">image</xsl:attribute>
          <xsl:if test="not(ancestor-or-self::*[contains(@f, 'nodata')])">
            <xsl:attribute name="faims_attribute_type">vocab</xsl:attribute>
          </xsl:if>
          <xsl:call-template name="body-expand-view-standard-nodes" />
          <item>
            <label>Options not loaded</label>
            <value>0</value>
          </item>
        </xsl:element>
      </xsl:when>
      <xsl:when test="normalize-space(@t)='radio'">
        <xsl:element name="select1">
          <xsl:attribute name="appearance">full</xsl:attribute>
          <xsl:if test="not(ancestor-or-self::*[contains(@f, 'nodata')])">
            <xsl:attribute name="faims_attribute_type">vocab</xsl:attribute>
          </xsl:if>
          <xsl:call-template name="body-expand-view-standard-nodes" />
          <item>
            <label>Options not loaded</label>
            <value>0</value>
          </item>
        </xsl:element>
      </xsl:when>
      <xsl:when test="normalize-space(@t)='video'">
        <xsl:element name="select">
          <xsl:attribute name="type">video</xsl:attribute>
          <xsl:if test="not(ancestor-or-self::*[contains(@f, 'nodata')])">
            <xsl:attribute name="faims_attribute_type">measure</xsl:attribute>
          </xsl:if>
          <xsl:if test="not(ancestor-or-self::*[contains(@f, 'nosync')])">
            <xsl:attribute name="faims_sync">true</xsl:attribute>
          </xsl:if>
          <xsl:call-template name="body-expand-view-standard-nodes" />
          <item>
            <label>Options not loaded</label>
            <value>0</value>
          </item>
        </xsl:element>
        <trigger ref="Button_{name()}">
          <xsl:variable name="nodeName">Button_<xsl:value-of select="name()"/></xsl:variable>
          <xsl:if test="../*[name() = $nodeName]">
            <xsl:comment>ERROR: View name is duplicated such that this UI schema is invalid.</xsl:comment>
          </xsl:if>
          <label>{Button_<xsl:value-of select="name()"/>}</label>
        </trigger>
      </xsl:when>
      <xsl:when test="normalize-space(@t) = 'webview' or normalize-space(@t) = 'web'">
        <xsl:element name="input">
          <xsl:attribute name="faims_web">true</xsl:attribute>
          <xsl:call-template name="body-expand-view-standard-nodes" />
        </xsl:element>
      </xsl:when>
      <xsl:when test="normalize-space(@t) = ''">
        <xsl:element name="input">
          <xsl:if test="not(ancestor-or-self::*[contains(@f, 'nodata')])">
            <xsl:attribute name="faims_attribute_type">measure</xsl:attribute>
          </xsl:if>
          <xsl:call-template name="body-expand-view-standard-nodes" />
          <xsl:if test="$doWarn">
            <xsl:comment>WARNING: No type t was given for this view; assuming it is an input</xsl:comment>
          </xsl:if>
        </xsl:element>
      </xsl:when>
      <xsl:otherwise>
        <xsl:element name="{normalize-space(@t)}">
          <xsl:call-template name="body-expand-view-standard-nodes" />
          <xsl:if test="$doWarn">
            <xsl:comment>WARNING: This view was created from an element whose t attribute's value is unexpected</xsl:comment>
          </xsl:if>
        </xsl:element>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template name="body-expand-view-standard-nodes">
    <xsl:attribute name="ref">
      <xsl:value-of select="name()"/>
    </xsl:attribute>
    <xsl:if test="@c and not(contains(@f, 'notnull')) and not(contains(@f, 'autonum'))">
      <xsl:attribute name="faims_style_class">
        <xsl:value-of select="@c"/>
      </xsl:attribute>
    </xsl:if>
    <xsl:if test="normalize-space(@t) != 'group' and
      normalize-space(@t) != 'button' and
      normalize-space(@t) != 'map' and
      normalize-space(@t) != 'web' and
      normalize-space(@t) != 'webview' and
      normalize-space(@t) != 'gpsdiag' and
      not(@e) and
      not(@ec) and
      not(ancestor-or-self::*[contains(@f, 'nodata')])">
      <xsl:attribute name="faims_attribute_name">
        <xsl:call-template name="string-replace-all">
          <xsl:with-param name="text" select="name()" />
          <xsl:with-param name="replace" select="'_'" />
          <xsl:with-param name="by" select="' '" />
        </xsl:call-template>
      </xsl:attribute>
    </xsl:if>
    <xsl:if test="@e or @ec">
      <xsl:attribute name="faims_annotation">false</xsl:attribute>
      <xsl:attribute name="faims_certainty" >false</xsl:attribute>
    </xsl:if>
    <xsl:call-template name="parse-flags">
      <xsl:with-param name="flags" select="@f" />
    </xsl:call-template>
    <xsl:if test="$doWarn and @c and contains(@f, 'notnull')">
      <xsl:comment>WARNING: Style in c attribute not applied; styling conflict exists due to "notnull" flag</xsl:comment>
    </xsl:if>
    <xsl:if test="$doWarn and @c and contains(@f, 'autonum')">
      <xsl:comment>WARNING: Style in c attribute not applied; styling conflict exists due to "autonum" flag</xsl:comment>
    </xsl:if>
    <xsl:call-template name="label" />
    <xsl:call-template name="warn-unexpected-attr" />
  </xsl:template>

  <xsl:template name="label">
    <xsl:element name="label">
      <xsl:if test="not(contains(@f, 'nolabel')) and not(contains(@f, 'noui'))">
        <xsl:choose>
          <xsl:when test="normalize-space(text())">
            <xsl:if test="
              $doWarn and
              not(name() = 'author') and
              not(name() = 'search') and
              not(name() = 'timestamp') and
              not(translate(normalize-space(text()), $valid-in-label, ''))">
              <xsl:comment>WARNING: For this element, a label was explicitly given. It may have been able to be represented more succinctly by allowing it to be inferred from its element's tag</xsl:comment>
            </xsl:if>
            <xsl:text>{</xsl:text>
            <xsl:call-template name="string-to-arch16n-line">
              <xsl:with-param name="string" select="normalize-space(text())" />
            </xsl:call-template>
            <xsl:text>}</xsl:text>
          </xsl:when>
          <xsl:otherwise>
            <xsl:text>{</xsl:text>
            <xsl:value-of select="name()" />
            <xsl:text>}</xsl:text>
            <!--<xsl:if test="$doWarn">-->
              <!--<xsl:comment>WARNING: Label not given; automatically generated from element name</xsl:comment>-->
            <!--</xsl:if>-->
          </xsl:otherwise>
        </xsl:choose>
      </xsl:if>
    </xsl:element>
  </xsl:template>

<!--
  Function string-replace-all taken from:
    http://geekswithblogs.net/Erik/archive/2008/04/01/120915.aspx
  Invoked as:

    <xsl:variable name="newtext">
      <xsl:call-template name="string-replace-all">
        <xsl:with-param name="text" select="$text" />
        <xsl:with-param name="replace" select="a" />
        <xsl:with-param name="by" select="b" />
      </xsl:call-template>
    </xsl:variable>
-->
  <xsl:template name="string-replace-all">
    <xsl:param name="text" />
    <xsl:param name="replace" />
    <xsl:param name="by" />
    <xsl:choose>
      <xsl:when test="contains($text, $replace)">
        <xsl:value-of select="substring-before($text,$replace)" />
        <xsl:value-of select="$by" />
        <xsl:call-template name="string-replace-all">
          <xsl:with-param name="text"
          select="substring-after($text,$replace)" />
          <xsl:with-param name="replace" select="$replace" />
          <xsl:with-param name="by" select="$by" />
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="$text" />
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template name="parse-flags">
    <xsl:param name="flags" />
    <xsl:variable name="v1">
      <xsl:call-template name="string-replace-all">
        <xsl:with-param name="text"    select="$flags" />
        <xsl:with-param name="replace" select="'noscroll'" />
        <xsl:with-param name="by"      select="''" />
      </xsl:call-template>
    </xsl:variable>
    <xsl:if test="string-length($v1) &lt; string-length($flags)">
      <xsl:attribute name="faims_scrollable">false</xsl:attribute>
    </xsl:if>
    <xsl:variable name="v2">
      <xsl:call-template name="string-replace-all">
        <xsl:with-param name="text"    select="$v1" />
        <xsl:with-param name="replace" select="'readonly'" />
        <xsl:with-param name="by"      select="''" />
      </xsl:call-template>
    </xsl:variable>
    <xsl:if test="string-length($v2) &lt; string-length($v1)">
      <xsl:attribute name="faims_read_only">true</xsl:attribute>
    </xsl:if>
    <xsl:variable name="v3">
      <xsl:call-template name="string-replace-all">
        <xsl:with-param name="text"    select="$v2" />
        <xsl:with-param name="replace" select="'nocertainty'" />
        <xsl:with-param name="by"      select="''" />
      </xsl:call-template>
    </xsl:variable>
    <xsl:if test="string-length($v3) &lt; string-length($v2)">
      <xsl:attribute name="faims_certainty">false</xsl:attribute>
    </xsl:if>
    <xsl:variable name="v4">
      <xsl:call-template name="string-replace-all">
        <xsl:with-param name="text"    select="$v3" />
        <xsl:with-param name="replace" select="'noannotation'" />
        <xsl:with-param name="by"      select="''" />
      </xsl:call-template>
    </xsl:variable>
    <xsl:if test="string-length($v4) &lt; string-length($v3)">
      <xsl:attribute name="faims_annotation">false</xsl:attribute>
    </xsl:if>
    <xsl:variable name="v5">
      <xsl:call-template name="string-replace-all">
        <xsl:with-param name="text"    select="$v4" />
        <xsl:with-param name="replace" select="'hidden'" />
        <xsl:with-param name="by"      select="''" />
      </xsl:call-template>
    </xsl:variable>
    <xsl:if test="string-length($v5) &lt; string-length($v4)">
      <xsl:attribute name="faims_hidden">true</xsl:attribute>
    </xsl:if>
    <xsl:variable name="v6">
      <xsl:call-template name="string-replace-all">
        <xsl:with-param name="text"    select="$v5" />
        <xsl:with-param name="replace" select="'id'" />
        <xsl:with-param name="by"      select="''" />
      </xsl:call-template>
    </xsl:variable>
    <xsl:variable name="v7">
      <xsl:call-template name="string-replace-all">
        <xsl:with-param name="text"    select="$v6" />
        <xsl:with-param name="replace" select="'nodata'" />
        <xsl:with-param name="by"      select="''" />
      </xsl:call-template>
    </xsl:variable>
    <xsl:if test="string-length($v7) &lt; string-length($v6)">
      <xsl:attribute name="faims_certainty">false</xsl:attribute>
      <xsl:attribute name="faims_annotation">false</xsl:attribute>
    </xsl:if>
    <xsl:variable name="v8">
      <xsl:call-template name="string-replace-all">
        <xsl:with-param name="text"    select="$v7" />
        <xsl:with-param name="replace" select="'noui'" />
        <xsl:with-param name="by"      select="''" />
      </xsl:call-template>
    </xsl:variable>
    <xsl:variable name="v9">
      <xsl:call-template name="string-replace-all">
        <xsl:with-param name="text"    select="$v8" />
        <xsl:with-param name="replace" select="'nosync'" />
        <xsl:with-param name="by"      select="''" />
      </xsl:call-template>
    </xsl:variable>
    <xsl:variable name="v10">
      <xsl:call-template name="string-replace-all">
        <xsl:with-param name="text"    select="$v9" />
        <xsl:with-param name="replace" select="'nothumbnail'" />
        <xsl:with-param name="by"      select="''" />
      </xsl:call-template>
    </xsl:variable>
    <xsl:variable name="v11">
      <xsl:call-template name="string-replace-all">
        <xsl:with-param name="text"    select="$v10" />
        <xsl:with-param name="replace" select="'nothumb'" />
        <xsl:with-param name="by"      select="''" />
      </xsl:call-template>
    </xsl:variable>
    <xsl:variable name="v12">
      <xsl:call-template name="string-replace-all">
        <xsl:with-param name="text"    select="$v11" />
        <xsl:with-param name="replace" select="'user'" />
        <xsl:with-param name="by"      select="''" />
      </xsl:call-template>
    </xsl:variable>
    <xsl:variable name="v13">
      <xsl:call-template name="string-replace-all">
        <xsl:with-param name="text"    select="$v12" />
        <xsl:with-param name="replace" select="'notnull'" />
        <xsl:with-param name="by"      select="''" />
      </xsl:call-template>
    </xsl:variable>
    <xsl:if test="string-length($v13) &lt; string-length($v12)">
      <xsl:attribute name="faims_style_class">required</xsl:attribute>
    </xsl:if>
    <xsl:variable name="v14">
      <xsl:call-template name="string-replace-all">
        <xsl:with-param name="text"    select="$v13" />
        <xsl:with-param name="replace" select="'autonum'" />
        <xsl:with-param name="by"      select="''" />
      </xsl:call-template>
    </xsl:variable>
    <xsl:variable name="v15">
      <xsl:call-template name="string-replace-all">
        <xsl:with-param name="text"    select="$v14" />
        <xsl:with-param name="replace" select="'nolabel'" />
        <xsl:with-param name="by"      select="''" />
      </xsl:call-template>
    </xsl:variable>
    <xsl:variable name="v16">
      <xsl:value-of select="normalize-space($v15)" />
    </xsl:variable>
    <xsl:if test="$doWarn and $v16 != ''">
      <xsl:comment>WARNING: Unexpected flag(s) "<xsl:value-of select="$v16" />"</xsl:comment>
    </xsl:if>
  </xsl:template>

  <xsl:template name="warn-unexpected-attr">
    <xsl:for-each select="@*">
      <xsl:if test="
        name() != 'b' and
        name() != 'c' and
        name() != 'e' and
        name() != 'ec' and
        name() != 'f' and
        name() != 'l' and
        name() != 'lc' and
        name() != 'p' and
        name() != 't'
        ">
        <xsl:comment>
          <xsl:text>WARNING: Unexpected attribute "</xsl:text>
          <xsl:value-of select="name()"/>
          <xsl:text>" ignored</xsl:text>
        </xsl:comment>
      </xsl:if>
    </xsl:for-each>
  </xsl:template>

  <!-- WARNING:  This template assumes $string contains at most 80
       non-alphanumeric characters
  -->
  <xsl:template name="string-to-arch16n-line">
    <xsl:param name="string" />
    <xsl:value-of select="
      translate(
        $string,
        translate(
          $string,
          'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
          ''
        ),
        '________________________________________________________________________________'
      )
    " />
  </xsl:template>

</xsl:stylesheet>
