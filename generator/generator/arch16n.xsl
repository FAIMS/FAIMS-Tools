<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="text" indent="yes"/>

  <xsl:template match="/">
    <xsl:for-each select="//*[not(name() = 'desc') and not(name() = 'opts') and not (name() = 'module') and not(name() = 'rels') and not(name() = 'col') and not(name() = 'cols') and not(name() = 'module') and not(name() = 'rels') and not(contains(@f, 'nolabel'))]">
      <xsl:sort select="normalize-space(text())" />


        <xsl:variable name="arch16n-key">
          <xsl:choose>
            <xsl:when test="normalize-space(text())">
              <xsl:call-template name="string-to-arch16n-key">
                <xsl:with-param name="string" select="normalize-space(text())" />
              </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
              <xsl:value-of select="name()" />
            </xsl:otherwise>
          </xsl:choose>
        </xsl:variable>

        <xsl:variable name="arch16n-val">
          <xsl:choose>
            <xsl:when test="normalize-space(text())">
              <xsl:value-of select="normalize-space(text())" />
            </xsl:when>
            <xsl:otherwise>
              <xsl:call-template name="string-replace-all">
                <xsl:with-param name="text" select="name()" />
                <xsl:with-param name="replace" select="'_'" />
                <xsl:with-param name="by" select="' '" />
              </xsl:call-template>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:variable>

        <xsl:value-of select="$arch16n-key" />
        <xsl:text>=</xsl:text>
        <xsl:value-of select="$arch16n-val" />
<xsl:text>
</xsl:text>

        <!-- Some types t add buttons not explicitly mentioned in the module's
             xml file. -->
        <xsl:if test="contains(normalize-space(@t), 'audio')">
          <xsl:text>Button_</xsl:text>
          <xsl:value-of select="$arch16n-key" />
          <xsl:text>=Attach Audio</xsl:text>
<xsl:text>
</xsl:text>
        </xsl:if>
        <xsl:if test="contains(normalize-space(@t), 'camera')">
          <xsl:text>Button_</xsl:text>
          <xsl:value-of select="$arch16n-key" />
          <xsl:text>=Attach Photograph</xsl:text>
<xsl:text>
</xsl:text>
        </xsl:if>
        <xsl:if test="contains(normalize-space(@t), 'file')">
          <xsl:text>Button_</xsl:text>
          <xsl:value-of select="$arch16n-key" />
          <xsl:text>=Attach File</xsl:text>
<xsl:text>
</xsl:text>
        </xsl:if>
        <xsl:if test="contains(normalize-space(@t), 'video')">
          <xsl:text>Button_</xsl:text>
          <xsl:value-of select="$arch16n-key" />
          <xsl:text>=Attach Video</xsl:text>
<xsl:text>
</xsl:text>
        </xsl:if>

    </xsl:for-each>
  </xsl:template>

  <!-- WARNING:  This template assumes $string contains at most 80
       non-alphanumeric characters
  -->
  <xsl:template name="string-to-arch16n-key">
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

</xsl:stylesheet>
