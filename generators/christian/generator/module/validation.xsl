<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="xml" indent="yes"/>

  <xsl:variable name="doWarn"           select="not(/module/@suppressWarnings = 'true')" />
  <xsl:key name="kDropdownOpt" match="*[@t='dropdown']/opts/opt" use="concat(name(ancestor::*[last()-1]), name(ancestor::*[last()-2]), name(ancestor::*[last()-3]), text())"/>

  <xsl:template match="/module">
    <ValidationSchema>
      <xsl:call-template name="arch-el" />
    </ValidationSchema>
  </xsl:template>

  <!-- ArchaeologicalElement -->
  <xsl:template name="arch-el">
    <xsl:for-each select="/module/*[not(contains(@f, 'nodata')) and not(contains(@f, 'noui')) and not(name() = 'rels') and not(name() = 'logic') and (./*//*[not(ancestor-or-self::*[contains(@f, 'nodata') or contains(@f, 'noui') or contains(@f, 'user')]) and not(name() = 'cols') and not(name() = 'col') and not(name() = 'desc') and not(name() = 'opt') and not(name() = 'opts') and not(ancestor-or-self::rels) and not(normalize-space(@t) = 'group') and not(normalize-space(@t) = 'table') and not(normalize-space(@t) = 'map') and not(normalize-space(@t) = 'button')])]">
      <ArchaeologicalElement name="{name(.)}">
        <xsl:call-template name="properties"/>
      </ArchaeologicalElement>
    </xsl:for-each>
  </xsl:template>

  <!-- property -->
  <xsl:template name="properties">
    <xsl:for-each select="./*//*[contains(@f, 'notnull') and not(ancestor-or-self::*[contains(@f, 'nodata') or contains(@f, 'noui') or contains(@f, 'user')]) and not(name() = 'cols') and not(name() = 'col') and not(name() = 'desc') and not(name() = 'opt') and not(name() = 'opts') and not(ancestor-or-self::rels)  and not(ancestor-or-self::logic) and not(normalize-space(@t) = 'group') and not(normalize-space(@t) = 'table') and not(normalize-space(@t) = 'map') and not(normalize-space(@t) = 'button') and not(name() = 'str') and not(name() = 'pos') and not(name() = 'fmt') and not(name() = 'app')]">
      <xsl:variable name="faims-attribute-name">
        <xsl:call-template name="string-replace-all">
          <xsl:with-param name="text" select="name(.)" />
          <xsl:with-param name="replace" select="'_'" />
          <xsl:with-param name="by" select="' '" />
        </xsl:call-template>
      </xsl:variable>
      <property name="{$faims-attribute-name}">
        <validator type="blankchecker">
          <param>
            <xsl:if test="normalize-space(@t) = 'input' or not(@t)">
              <xsl:attribute name="value">measure</xsl:attribute>
            </xsl:if>
            <xsl:if test="normalize-space(@t) = 'checkbox'
              or normalize-space(@t) = 'dropdown'
              or normalize-space(@t) = 'picture'
              or normalize-space(@t) = 'radio'
              or normalize-space(@t) = 'list'">
              <xsl:attribute name="value">vocab</xsl:attribute>
            </xsl:if>
            <xsl:attribute name="type">field</xsl:attribute>
          </param>
        </validator>
      </property>
    </xsl:for-each>
  </xsl:template>

  <!-- dropdown/radio button/picture gallery options -->

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
