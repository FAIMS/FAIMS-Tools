<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns    ="http://www.w3.org/2002/xforms"
                xmlns:ev ="http://www.w3.org/2001/xml-events"
                xmlns:h  ="http://www.w3.org/1999/xhtml"
                xmlns:jr ="http://openrosa.org/javarosa"
                xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                xmlns:fn="http://www.w3.org/2005/xpath-functions"                
                version="2.0">
  <xsl:output method="xml" indent="yes" omit-xml-declaration="yes"/>






<xsl:template match="/">
<xsl:text>#!/bin/bash</xsl:text>
<xsl:text>&#xa;&#xa;</xsl:text>
<xsl:for-each select="//*[@ref]">
<xsl:variable name="label">
<xsl:for-each select="child::*">
<xsl:if test="name() = 'label'">
  <xsl:value-of select="text()"/>
</xsl:if>
</xsl:for-each>
</xsl:variable>


<xsl:variable name="arch16n">
  <xsl:choose>
    <xsl:when test="contains($label, '{')">
      <xsl:value-of select="document('arch16n.xml')/arch16ns/arch16n[@k=$label]"/>
    </xsl:when>
    <xsl:otherwise>
      <xsl:value-of select="$label"/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:variable>

<xsl:variable name="cols">
  <xsl:choose>
    <xsl:when test="normalize-space(../../../../@ref)"><xsl:value-of select="count(../preceding-sibling::*) + count(../following-sibling::*)"/></xsl:when>
    <xsl:otherwise>1</xsl:otherwise>
  </xsl:choose>
</xsl:variable>

<xsl:variable name="elementType">
  <xsl:choose>
    <xsl:when test="name() = 'input'">
      <xsl:choose>
        <xsl:when test="@faims_map='true'">map</xsl:when>
        <xsl:when test="@faims_table='true'">table</xsl:when>
        <xsl:when test="@faims_web='true'">webview</xsl:when>
        <xsl:otherwise>input</xsl:otherwise>
      </xsl:choose>
    </xsl:when>
    <xsl:when test="name() = 'select'">
      <xsl:choose>
        <xsl:when test="@type='camera'">file</xsl:when>
        <xsl:when test="@type='video'">file</xsl:when>
        <xsl:when test="@type='file'">file</xsl:when>
        <xsl:otherwise>checkbox</xsl:otherwise>
      </xsl:choose>
    </xsl:when>
    <xsl:when test="name() = 'trigger'">button</xsl:when>

    <xsl:when test="name() = 'select1'">
      <xsl:choose>
        <xsl:when test="@type='image'">pictureGallery</xsl:when>
        <xsl:when test="@appearance='full'">radio</xsl:when>
        <xsl:when test="@appearance='compact'">list</xsl:when>
        <xsl:otherwise>dropdown</xsl:otherwise>
      </xsl:choose>
    </xsl:when>
    <xsl:otherwise>uncaught</xsl:otherwise>
  </xsl:choose>
</xsl:variable>

<xsl:variable name="annotation">
  <xsl:if test="@faims_annotation='true'">true</xsl:if>
  <xsl:if test="@faims_annotation='false' or count(@faims_annotation)=0">false</xsl:if>
</xsl:variable>
<xsl:variable name="certainty">
  <xsl:if test="@faims_certainty='true'">true</xsl:if>
  <xsl:if test="@faims_certainty='false' or count(@faims_certainty)=0">false</xsl:if>
</xsl:variable>
<xsl:variable name="info">
  <xsl:if test="count(@faims_attribute_name)=1">true</xsl:if>
  <xsl:if test="count(@faims_attribute_name)=0">false</xsl:if>
</xsl:variable>
<xsl:variable name="required">
  <xsl:choose><xsl:when test="contains(@faims_style_class, 'required')">true</xsl:when>
  <xsl:otherwise>false</xsl:otherwise>
  </xsl:choose>
</xsl:variable>
<xsl:variable name="readonly">
  <xsl:choose><xsl:when test="@faims_read_only='true'">true</xsl:when>
  <xsl:otherwise>false</xsl:otherwise>
  </xsl:choose>
</xsl:variable>

  <xsl:variable name="elementName"><xsl:if test="normalize-space(../../../../@ref)"><xsl:value-of select="normalize-space(../../../../@ref)"/>_<xsl:value-of select="normalize-space(../../../@ref)"/>_<xsl:value-of select="normalize-space(@ref)"/></xsl:if><xsl:if test="normalize-space(../../../../@ref) = ''"><xsl:value-of select="normalize-space(../../@ref)"/>_<xsl:value-of select="normalize-space(../@ref)"/>_<xsl:value-of select="normalize-space(@ref)"/></xsl:if></xsl:variable>


  <xsl:if test="name() = 'input' or name() = 'select1' or name() = 'select' or name() = 'trigger' ">
    <xsl:text>./makeElement.sh </xsl:text>
    <xsl:value-of select="$elementName"/>
    <xsl:text> "</xsl:text>
    <xsl:value-of select="$arch16n" />
    <xsl:text>" </xsl:text>
    <xsl:value-of select="$elementType"/>
    <xsl:text> </xsl:text>
    <xsl:value-of select="$cols"/>
    <xsl:text> </xsl:text>
    <xsl:value-of select="$annotation"/>
    <xsl:text> </xsl:text>
    <xsl:value-of select="$certainty"/>
    <xsl:text> </xsl:text>
    <xsl:value-of select="$info"/>
    <xsl:text> </xsl:text>
    <xsl:value-of select="$required"/>
    <xsl:text> </xsl:text>
    <xsl:value-of select="$readonly"/>
    <xsl:text> .</xsl:text>
    <xsl:text>&#xa;</xsl:text>
  </xsl:if>




</xsl:for-each>
</xsl:template>



</xsl:stylesheet>
