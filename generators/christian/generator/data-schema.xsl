<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="xml" indent="yes" cdata-section-elements="formatString appendCharacterString"/>

  <xsl:variable name="doWarn"           select="not(/module/@suppressWarnings = 'true')" />
  <xsl:key name="kDropdownOpt" match="*[@t='dropdown']/opts/opt" use="concat(name(ancestor::*[last()-1]), name(ancestor::*[last()-2]), name(ancestor::*[last()-3]), text())"/>
  <xsl:key name="kPropertyName" match="*/*/*//*[
    not(ancestor-or-self::*[contains(@f, 'onlyui') or contains(@f, 'user')]) and
    not(name() = 'app') and
    not(name() = 'author') and
    not(name() = 'col') and
    not(name() = 'cols') and
    not(name() = 'desc') and
    not(name() = 'fmt') and
    not(name() = 'gps') and
    not(name() = 'opt') and
    not(name() = 'opts') and
    not(name() = 'pos') and
    not(name() = 'str') and
    not(name() = 'timestamp') and
    not(ancestor-or-self::rels) and
    not(normalize-space(@t) = 'button') and
    not(normalize-space(@t) = 'gpsdiag') and
    not(normalize-space(@t) = 'group') and
    not(normalize-space(@t) = 'map')
    ]"
    use="concat(name(ancestor::*[last()-1]), name(.))"/>

  <xsl:template match="/module">
    <dataSchema>
      <xsl:copy-of select="/module/rels/*" />
      <xsl:call-template name="arch-el" />
    </dataSchema>
  </xsl:template>

  <!-- ArchaeologicalElement -->
  <xsl:template name="arch-el">
    <xsl:for-each select="/module/*[not(contains(@f, 'onlyui')) and not(name() = 'rels') and (./*//*[not(ancestor-or-self::*[contains(@f, 'onlyui') or contains(@f, 'user')]) and not(name() = 'gps') and not(name() = 'author') and not(name() = 'timestamp') and not(name() = 'cols') and not(name() = 'col') and not(name() = 'desc') and not(name() = 'opt') and not(name() = 'opts') and not(ancestor-or-self::rels) and not(normalize-space(@t) = 'group') and not(normalize-space(@t) = 'gpsdiag') and not(normalize-space(@t) = 'map') and not(normalize-space(@t) = 'button')])]">
      <xsl:variable name="faims-archent-name">
        <xsl:call-template name="string-replace-all">
          <xsl:with-param name="text" select="name()" />
          <xsl:with-param name="replace" select="'_'" />
          <xsl:with-param name="by" select="' '" />
        </xsl:call-template>
      </xsl:variable>
      <ArchaeologicalElement name="{$faims-archent-name}">
        <xsl:if test="not(.//*[contains(@f, ' id') or contains(@f, 'id ') or normalize-space(@f) = 'id'])">
          <xsl:comment>ERROR: Identifier not given</xsl:comment>
        </xsl:if>
        <xsl:call-template name="desc" />

        <!-- Parse the properties -->
        <xsl:call-template name="properties"/>
      </ArchaeologicalElement>
    </xsl:for-each>
  </xsl:template>

  <!-- description -->
  <xsl:template match="desc">
    <xsl:value-of select="."/>
  </xsl:template>
  <xsl:template name="desc">
    <description>
      <!--<xsl:if test="$doWarn and not(desc)">-->
        <!--<xsl:comment>WARNING: &lt;desc&gt; tag not given</xsl:comment>-->
      <!--</xsl:if>-->
      <xsl:apply-templates select="desc"/>
    </description>
  </xsl:template>

  <!-- property -->
  <xsl:template name="properties">
    <xsl:for-each select="./*//*[not(ancestor-or-self::*[contains(@f, 'onlyui') or contains(@f, 'user')]) and not(name() = 'gps') and not(name() = 'author') and not(name() = 'timestamp') and not(name() = 'cols') and not(name() = 'col') and not(name() = 'desc') and not(name() = 'opt') and not(name() = 'opts') and not(ancestor-or-self::rels) and not(normalize-space(@t) = 'group') and not(normalize-space(@t) = 'gpsdiag') and not(normalize-space(@t) = 'map') and not(normalize-space(@t) = 'button') and not(name() = 'str') and not(name() = 'pos') and not(name() = 'fmt') and not(name() = 'app')]">
      <xsl:sort select="concat(str/pos/text(), substring('not-found', 1 div not(str/pos/text())))" />

      <xsl:variable name="faims-attribute-name">
        <xsl:call-template name="string-replace-all">
          <xsl:with-param name="text" select="name(.)" />
          <xsl:with-param name="replace" select="'_'" />
          <xsl:with-param name="by" select="' '" />
        </xsl:call-template>
      </xsl:variable>
      <property name="{$faims-attribute-name}">
        <xsl:if test="contains(@f, 'id ') or contains(@f, ' id') or normalize-space(@f) = 'id'">
          <xsl:attribute name="isIdentifier">true</xsl:attribute>
        </xsl:if>
        <xsl:if test="normalize-space(@t) = 'input'
          or not(@t)">
          <xsl:attribute name="type">measure</xsl:attribute>
        </xsl:if>
        <xsl:if test="normalize-space(@t) = 'camera'
          or normalize-space(@t) = 'audio'
          or normalize-space(@t) = 'video'
          or normalize-space(@t) = 'file'">
          <xsl:attribute name="type">file</xsl:attribute>
          <xsl:attribute name="file">true</xsl:attribute>
          <xsl:if test="not(contains(@f, 'nothumb'))">
            <xsl:attribute name="thumbnail">true</xsl:attribute>
          </xsl:if>
        </xsl:if>
        <xsl:if test="normalize-space(@t) = 'checkbox'
          or normalize-space(@t) = 'dropdown'
          or normalize-space(@t) = 'picture'
          or normalize-space(@t) = 'radio'
          or normalize-space(@t) = 'list'">
          <xsl:attribute name="type">vocab</xsl:attribute>
          <xsl:if test="$doWarn and not(.//opts)">
            <xsl:comment>WARNING: A set of &lt;opts&gt; tags are expected but not present</xsl:comment>
          </xsl:if>
        </xsl:if>
        <xsl:if test="generate-id() = generate-id(key('kPropertyName', concat(name(ancestor::*[last()-1]), name(.)))[2])">
          <xsl:comment>ERROR: This view's name is a duplicate of one or more other views' in this tab group</xsl:comment>
        </xsl:if>
        <xsl:call-template name="desc" />
        <xsl:call-template name="faims-strings" />
        <xsl:apply-templates select="opts"/>
      </property>
    </xsl:for-each>

    <xsl:if test="./*/gps">
      <property name="Latitude" type="measure">
        <xsl:if test="count(.//Latitude) &gt;= 1 or count(.//gps) &gt;= 2">
          <xsl:comment>ERROR: This view's name is a duplicate of one or more other views' in this tab group</xsl:comment>
        </xsl:if>
        <description/>
      </property>
      <property name="Longitude" type="measure">
        <xsl:if test="count(.//Longitude) &gt;= 1 or count(.//gps) &gt;= 2">
          <xsl:comment>ERROR: This view's name is a duplicate of one or more other views' in this tab group</xsl:comment>
        </xsl:if>
        <description/>
      </property>
      <property name="Northing" type="measure">
        <xsl:if test="count(.//Northing) &gt;= 1 or count(.//gps) &gt;= 2">
          <xsl:comment>ERROR: This view's name is a duplicate of one or more other views' in this tab group</xsl:comment>
        </xsl:if>
        <description/>
      </property>
      <property name="Easting" type="measure">
        <xsl:if test="count(.//Easting) &gt;= 1 or count(.//gps) &gt;= 2">
          <xsl:comment>ERROR: This view's name is a duplicate of one or more other views' in this tab group</xsl:comment>
        </xsl:if>
        <description/>
      </property>
    </xsl:if>
  </xsl:template>

  <xsl:template name="faims-strings">
    <xsl:if test=".//str and not(normalize-space(@f) = 'id') and not(contains(@f, ' id')) and not(contains(@f, 'id '))">
      <xsl:comment>WARNING: Property has &lt;str&gt; tags but is not flagged as an identifier</xsl:comment>
    </xsl:if>
    <xsl:if test=".//fmt">
      <formatString><xsl:value-of select=".//fmt/text()"/></formatString>
    </xsl:if>
    <xsl:if test=".//app">
      <appendCharacterString><xsl:value-of select=".//app/text()"/></appendCharacterString>
    </xsl:if>
  </xsl:template>

  <!-- dropdown/radio button/picture gallery options -->
  <xsl:template match="opts">
    <lookup>
      <xsl:for-each select="opt">
        <xsl:call-template name="opt"/>
      </xsl:for-each>
    </lookup>
  </xsl:template>
  <xsl:template name="opt">
    <term>
      <xsl:if test="@p">
        <xsl:attribute name="pictureURL"><xsl:value-of select="normalize-space(@p)"/></xsl:attribute>
      </xsl:if>
      <xsl:if test="normalize-space(text()) = ''">
        <xsl:comment>ERROR: Option is missing a name</xsl:comment>
      </xsl:if>
      <xsl:if test="$doWarn and generate-id() = generate-id(key('kDropdownOpt', concat(name(ancestor::*[last()-1]), name(ancestor::*[last()-2]), name(ancestor::*[last()-3]), text()))[2])">
        <xsl:comment>WARNING: Option is duplicated in this menu</xsl:comment>
        <!-- TODO: Make this warning work correctly for hierarchical dropdowns -->
      </xsl:if>
      <xsl:text>{</xsl:text>
      <xsl:call-template name="string-to-arch16n-line">
        <xsl:with-param name="string" select="normalize-space(text())" />
      </xsl:call-template>
      <xsl:text>}</xsl:text>
<xsl:text>
</xsl:text>
      <xsl:call-template name="desc" />
      <xsl:for-each select="opt">
        <xsl:call-template name="opt"/>
      </xsl:for-each>
    </term>
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
