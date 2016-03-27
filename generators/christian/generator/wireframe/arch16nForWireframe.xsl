<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="xml" indent="yes"/>

  <xsl:template match="/">
    <xsl:for-each select="//*[not(name() = 'desc') and not(name() = 'opts') and not (name() = 'module') and not(name() = 'rels') and not(name() = 'col') and not(name() = 'cols') and not(name() = 'module') and not(name() = 'rels') and not(contains(@f, 'nolabel'))]">
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
    <!-- These are some entries mentioned in the staticly (as opposed to
         dynamically) generated portion of the UI schema -->
<xsl:text>Accuracy=Accuracy
Any_unsaved_changes_will_be_lost=Any unsaved changes will be lost
Clean_Synced_Files=Clean synced files
Confirm_Deletion=Confirm Deletion
Delete_Cancelled=Delete cancelled
Delete=Delete
Disable_External_GPS=Disable External GPS
Disable_Internal_GPS=Disable Internal GPS
Disable_Sync=Disable Sync
Duplicated_record=Duplicated record
Duplicate=Duplicate
Easting=Easting
Enable_External_GPS=Enable External GPS
Enable_Internal_GPS=Enable Internal GPS
Enable_Sync=Enable Sync
External_GPS_Disabled=External GPS disabled
External_GPS_Enabled=External GPS enabled
GPS_is_no_longer_initialised=GPS is no longer initialised
GPS_is_not_initialised=GPS is not initialised
Internal_GPS_Disabled=Internal GPS disabled
Internal_GPS_Enabled=Internal GPS enabled
Internal_GPS=Internal GPS
Latitude=Latitude
Longitude=Longitude
New=New
New_record_created=New record created
Northing=Northing
Please_Enable_Bluetooth=Please enable bluetooth
no_GPS_position_could_be_found=no GPS position could be found
off=off
on=on
on_and_bluetooth_connected=on and bluetooth connected
on_and_bluetooth_disconnected=on and bluetooth disconnected
Position=Position
Press_OK_to_Delete_this_Record=Press OK to delete this record
Previous_status=Previous status
Sync_Disabled=Sync disabled
Sync_Enabled=Sync enabled
This_record_is_unsaved_and_cannot_be_duplicated=This record is unsaved and cannot be duplicated
Validate=Validate
Warning=Warning</xsl:text>
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
