<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="text" indent="no"/>

  <xsl:variable name="newline" >
<xsl:text>
</xsl:text>
  </xsl:variable>

  <xsl:template match="/">

<xsl:text>import android.util.Log;

Object dialog;

setFileSyncEnabled(true);
setSyncDelay(5.0f);
setSyncEnabled(true);
setSyncMaxInterval(600.0f);
setSyncMinInterval(5.0f);


makeLocalID(){
  fetchOne("CREATE TABLE IF NOT EXISTS localSettings (key text primary key, value text);", null);
  fetchOne("DROP VIEW IF EXISTS parentchild;", null);
}
makeLocalID();

newTab(String tab, Boolean resolveTabGroups) {
  if (!resolveTabGroups) {
    return newTab(tab);
  }

  tab = tab.replaceAll("/$", "");
  tab = tab.replaceAll("^/", "");
  if (tab.matches("/")) {
    newTab(tab);
  } else {
    newTabGroup(tab);
  }
}

/******************************************************************************/
/*                                 ACTION BAR                                 */
/******************************************************************************/
addActionBarItem("clean_synced_files", new ActionButtonCallback() {
  actionOnLabel() {
    "{Clean_Synced_Files}";
  }
  actionOn() {
    cleanSyncedFiles();
  }
});

addActionBarItem("sync", new ToggleActionButtonCallback() {
  actionOnLabel() {
    "{Disable_Sync}";
  }
  actionOn() {
    setSyncEnabled(false);
    setFileSyncEnabled(false);
    showToast("{Sync_Disabled}");
  }
  isActionOff() {
    isSyncEnabled();
  }
  actionOffLabel() {
    "{Enable_Sync}";
  }
  actionOff() {
    setSyncEnabled(true);
    setFileSyncEnabled(true);
    showToast("{Sync_Enabled}");
  }
});

addActionBarItem("internal_gps", new ToggleActionButtonCallback() {
  actionOnLabel() {
    "{Disable_Internal_GPS}";
  }
  actionOn() {
    stopGPS();
    showToast("{Internal_GPS_Disabled}");
    updateGPSDiagnostics();
  }
  isActionOff() {
    isInternalGPSOn();
  }
  actionOffLabel() {
    "{Enable_Internal_GPS}";
  }
  actionOff() {
    if(isExternalGPSOn()) {
      stopGPS();
    }
    startInternalGPS();
    showToast("{Internal_GPS_Enabled}");
    updateGPSDiagnostics();
  }
});

addActionBarItem("external_gps", new ToggleActionButtonCallback() {
  actionOnLabel() {
    "{Disable_External_GPS}";
  }
  actionOn() {
    stopGPS();
    if (isBluetoothConnected()) {
      showToast("{External_GPS_Disabled}");
    } else {
      showToast("{Please_Enable_Bluetooth}");
    }
    updateGPSDiagnostics();
  }
  isActionOff() {
    isExternalGPSOn();
  }
  actionOffLabel() {
    "{Enable_External_GPS}";
  }
  actionOff() {
    if(isInternalGPSOn()) {
      stopGPS();
    }
    startExternalGPS();
    if(isBluetoothConnected()) {
      showToast("{External_GPS_Enabled}");
    } else {
      showToast("{Please_Enable_Bluetooth}");
      this.actionOn();
    }
    updateGPSDiagnostics();
  }
});

</xsl:text>

    <!-- GPS -->
<xsl:text>
/******************************************************************************/
/*                                    GPS                                     */
/******************************************************************************/
updateGPSDiagnostics() {
  String diagnosticsRef = "</xsl:text>
  <xsl:call-template name="gps-diag-ref" />
  <xsl:text>";</xsl:text>
  <xsl:text>
  if (diagnosticsRef.equals("")) {
    return;
  }

  String status         = "";
  String previousStatus = getFieldValue(diagnosticsRef);
  String notInitialised = "{GPS_is_not_initialised}";

  // Check if GPS is initialised or was previously initialised.
  if (!isExternalGPSOn() &amp;&amp; !isInternalGPSOn()) {
    if (!isNull(previousStatus) &amp;&amp; !previousStatus.equals(notInitialised)) { // previous gps status is some last valid coordinate.
      // This is hackish. Arch16n substitution happens only at display-time, but the following if clause requires substitution to have happened at run-time
      String error = "";
      error = "{GPS_is_no_longer_initialised}. {Previous_status}:";
      setFieldValue(diagnosticsRef, error);   // Arch16n entry is substituted after this
      error = getFieldValue(diagnosticsRef);

      // check that error message wasn't previously appended to the previous status message.
      if (previousStatus.length()    >= error.length() &amp;&amp;
          previousStatus.subSequence(0, error.length()).equals(error)) {
        status = previousStatus;
      } else {
        status = error + "\n" + previousStatus;
      }
    } else {
      status = notInitialised;
    }
  } else {
    status += "{Internal_GPS}: ";
    if (isInternalGPSOn())
    {
      status += "{on}";
    } else {
      status += "{off}";
    }
    status += "\nExternal GPS: ";
    if (isExternalGPSOn())
    {
      if (isBluetoothConnected()) {
        status += "{on_and_bluetooth_connected}";
      } else {
        status += "{on_and_bluetooth_disconnected}";
      }
    } else {
      status += "{off}";
    }
    Object position = getGPSPosition();
    if (position != null) {
      Object projPosition = getGPSPositionProjected();
      status += "\n{Latitude}: " + position.getLatitude();
      status += "   {Longitude}: " + position.getLongitude();
      status += "\n{Northing}: " + projPosition.getLatitude();
      status += "   {Easting}: " + projPosition.getLongitude();
      status += "\n{Accuracy}: " + getGPSEstimatedAccuracy();
    } else {
      status += "\n{Position}: {no_GPS_position_could_be_found}";
    }
  }
  setFieldValue(diagnosticsRef, status);
}
</xsl:text>


    <!-- User login stuff -->
<xsl:text>
/******************************************************************************/
/*                                 USER LOGIN                                 */
/******************************************************************************/
</xsl:text>
    <xsl:choose>
      <xsl:when test="count(//*[contains(@f, 'user')]) = 0">
<xsl:text>
// WARNING: This module is missing a login menu
String userId    = "1";
String nameFirst = "";
String nameLast  = "";
String email     = "";
User   user      = new User(userId, nameFirst, nameLast, email);
setUser(user);
</xsl:text>
      </xsl:when>
      <xsl:when test="count(//*[contains(@f, 'user')]) = 1">
        <xsl:call-template name="users"/>
      </xsl:when>
      <xsl:when test="count(//*[contains(@f, 'user')]) &gt; 1">
        <xsl:text>//WARNING: This module has more than one login menu</xsl:text>
        <xsl:value-of select="$newline" />
        <xsl:call-template name="users"/>
      </xsl:when>
    </xsl:choose>
    <xsl:value-of select="$newline" />

    <!-- makeVocab stuff -->
<xsl:text>
/******************************************************************************/
/*                              MENU POPULATION                               */
/******************************************************************************/
/** Wrapper for to make a vocab without an exlusion list **/
makeVocab(String type, String path, String attrib) {
  makeVocab(type, path, attrib, null);
}

/** Vocab Population **/
/* Populates the path specified vocabulary from the database based on the given attribute name, where type 
is the type of the vocab to populate (PictureGallery, HierarchicalPictureGallery, CheckBoxGroup, DropDown, HierarchicalDropDown, RadioGroup or List). */
makeVocab(String type, String path, String attrib, List vocabExclusions) {
    makeVocab(type, path, attrib, vocabExclusions, null);
}

/* Populates the path specified vocabulary from the database based on the given attribute name, where type 
is the type of the vocab to populate (PictureGallery, HierarchicalPictureGallery, CheckBoxGroup, DropDown, HierarchicalDropDown, RadioGroup or List). */
makeVocab(String type, String path, String attrib, List vocabExclusions, String callbackFunction){
  if (isNull(type) || isNull(path) || isNull(attrib)) {
    Log.e("makeVocab()", "Can't make populate a vocab when the given type, path or attribute is Null");
    return;
  }

  if (type.equals("PictureGallery")) {
    String pictureGalleryQuery = "SELECT vocabid, vocabname, pictureurl "+
                                 "  FROM vocabulary "+
                                 "  LEFT OUTER JOIN attributekey USING (attributeid) "+
                                 " WHERE attributename = '" + attrib + "' "+
                                 " ORDER BY  vocabcountorder;";
    fetchAll(pictureGalleryQuery, new FetchCallback() {
      onFetch(pictures) {
        populatePictureGallery(path, pictures);
        if (callbackFunction != null &amp;&amp; !isNull(callbackFunction)) {
          execute(callbackFunction);
        }
      }
    });
    return;
  }

  if (type.equals("HierarchicalPictureGallery")) {
    populateHierarchicalPictureGallery(path, attrib);
    if (callbackFunction != null &amp;&amp; !isNull(callbackFunction)) {
      execute(callbackFunction);
    }
    return;
  }

  if (type.equals("HierarchicalDropDown")) {
    // populateHierarchicalDropDown(path, attrib);
    populateHierarchicalDropDown(path, attrib, true);
    if (callbackFunction != null &amp;&amp; !isNull(callbackFunction)) {
      execute(callbackFunction);
    }
    return;
  }

  String getAttributeVocabQuery = "SELECT vocabid, vocabname "+
                                  "  FROM vocabulary "+
                                  "  JOIN attributekey USING (attributeid) "+
                                  " WHERE attributename = '" + attrib + "' "+
                                  " ORDER BY vocabcountorder;";
  fetchAll(getAttributeVocabQuery,
    new FetchCallback() {
      onFetch(result) {
        // print("makeVocab() result: " + result);
        if (result!=null &amp;&amp; result.size()>0 &amp;&amp; vocabExclusions!=null &amp;&amp; vocabExclusions.size()>0) {
          List filteredVocab = new ArrayList();
          for(item : result) {
            if (vocabExclusions.contains(item.get(1))) {
              Log.d("makeVocab()", "removing vocab exclusion: " + item.get(1));
            } else {
              filteredVocab.add(item);
            }
          }
          result=filteredVocab;
        }
        // print("makeVocab() filtered result: " + result);
        if(type.equals("CheckBoxGroup")) {
          populateCheckBoxGroup(path, result);
        } else if(type.equals("DropDown")) {
          // populateDropDown(path, result);
          populateDropDown(path, result, true);
        } else if(type.equals("RadioGroup")) {
          populateRadioGroup(path, result);
        } else if(type.equals("List")) {
          populateList(path, result);
        }
        if (callbackFunction != null &amp;&amp; !isNull(callbackFunction)) {
          execute(callbackFunction);
        }
      }
    });
}
</xsl:text>
    <xsl:for-each select="//*[@t and not(ancestor-or-self::*[contains(@f, 'onlyui') or contains(@f, 'onlydata')]) and not(contains(@f, 'user'))]">
      <xsl:variable name="is-hierarchical">
        <xsl:call-template name="is-hierarchical"/>
      </xsl:variable>
      <xsl:choose>
        <xsl:when test="normalize-space(@t) = 'checkbox'">
          <xsl:text>makeVocab("CheckBoxGroup", "</xsl:text>
          <xsl:call-template name="complete-makevocab" />
        </xsl:when>
        <xsl:when test="normalize-space(@t) = 'dropdown'">
          <xsl:choose>
            <xsl:when test="$is-hierarchical = '1'">
              <xsl:text>makeVocab("HierarchicalDropDown", "</xsl:text>
              <xsl:call-template name="complete-makevocab" />
            </xsl:when>
            <xsl:otherwise>
              <xsl:text>makeVocab("DropDown", "</xsl:text>
              <xsl:call-template name="complete-makevocab" />
            </xsl:otherwise>
          </xsl:choose>
        </xsl:when>
        <xsl:when test="normalize-space(@t) = 'list'">
          <xsl:text>makeVocab("List", "</xsl:text>
          <xsl:call-template name="complete-makevocab" />
        </xsl:when>
        <xsl:when test="normalize-space(@t) = 'picture'">
          <xsl:choose>
            <xsl:when test="$is-hierarchical = '1'">
              <xsl:text>makeVocab("HierarchicalPictureGallery", "</xsl:text>
              <xsl:call-template name="complete-makevocab" />
            </xsl:when>
            <xsl:otherwise>
              <xsl:text>makeVocab("PictureGallery", "</xsl:text>
              <xsl:call-template name="complete-makevocab" />
            </xsl:otherwise>
          </xsl:choose>
        </xsl:when>
        <xsl:when test="normalize-space(@t) = 'radio'">
          <xsl:text>makeVocab("RadioGroup", "</xsl:text>
          <xsl:call-template name="complete-makevocab" />
        </xsl:when>
      </xsl:choose>
    </xsl:for-each>

    <xsl:value-of select="$newline" />

    <!-- Validation -->
<xsl:text>
/******************************************************************************/
/*                                 VALIDATION                                 */
/******************************************************************************/
/* `ref`  is a reference/path to a field
 * `name` is a human-readable name for that field
 * `cond` is a String containing a boolean expression that evaluates to true if
 *        and only if the the field pair returned by this function should be
 *        validated.
 *
 *  Returns a field pair (really just an ArrayList).
 */
fieldPair(String ref, String name, String cond) {
  List fp = new ArrayList();
  fp.add(ref);
  fp.add(name);
  fp.add(cond);
  return fp;
}

fieldPair(String ref, String name) {
  String t = "true";
  return fieldPair(ref, name, t);
}

/* Returns true if field specified by `ref` is valid. False otherwise.
 */
isValidField(String ref) {
  return !isNull(getFieldValue(ref));
}
/* `format` can either be HTML or PLAINTEXT
 */
validateFields(List fields, String format) {
  Integer numInvalid = 0;

  /* Build validation message string (and count how many invalid fields exist) */
  String out = "Please fill out the following fields:\n";
  for(f : fields) {
    String ref  = f.get(0); // Reference to field
    String name = f.get(1); // Human-readable name
    String cond = f.get(2); // Validation condition

    // Only validate a field whose validation condition evaluates to `true`
    Boolean doValidateField = (Boolean) eval(cond);
    if (!doValidateField)
      continue;

    // Add any invalid fields to the output and tally them
    if (!isValidField(ref)) {
      out += "- " + name + "\n";
      numInvalid++;
    }
  }
  // All the fields are valid; just overwrite `out` with a cheery message
  if (numInvalid == 0)
    out = "All fields contain valid data!";

  /* Format the output as dictated by `format` */
  if (format == "HTML") {
    out = out.replace("\n", "&lt;br&gt;");
  } else if (format == "PLAINTEXT") {
    ;
  }

  return out;
}

</xsl:text>
    <xsl:for-each select="/module/*[.//*[contains(@f, 'notnull')]]">
      <xsl:text>validate</xsl:text>
      <xsl:call-template name="string-replace-all">
        <xsl:with-param name="text" select="name()" />
        <xsl:with-param name="replace" select="'_'" />
        <xsl:with-param name="by" select="''" />
      </xsl:call-template>
      <xsl:text>() {</xsl:text>
      <xsl:value-of select="$newline" />
      <xsl:text>  List f = new ArrayList(); // Fields to be validated</xsl:text>
      <xsl:value-of select="$newline" />
      <xsl:value-of select="$newline" />
      <xsl:for-each select=".//*[contains(@f, 'notnull')]">
        <xsl:text>  f.add(fieldPair("</xsl:text>
        <xsl:call-template name="ref" />
        <xsl:text>", "</xsl:text>
        <xsl:call-template name="label" />
        <xsl:text>"));</xsl:text>
        <xsl:value-of select="$newline" />
      </xsl:for-each>
      <xsl:value-of select="$newline" />
      <xsl:text>  String validationMessage = validateFields(f, "PLAINTEXT");</xsl:text>
      <xsl:value-of select="$newline" />
      <xsl:text>  showWarning("Validation Results", validationMessage);</xsl:text>
      <xsl:value-of select="$newline" />
      <xsl:text>}</xsl:text>
    </xsl:for-each>

    <xsl:value-of select="$newline" />

    <!-- Autosaving -->
<xsl:text>
/******************************************************************************/
/*                                 AUTOSAVING                                 */
/******************************************************************************/
Map tabgroupToUuid = new HashMap();

getUuid(String tabgroup) {
  tabgroupToUuid.get(tabgroup);
}

setUuid(String tabgroup, String uuid) {
  tabgroupToUuid.put(tabgroup, uuid);
}

saveTabGroup(String tabgroup) {
  saveTabGroup(tabgroup, "");
}

saveTabGroup(String tabgroup, String callback) {
  Boolean enableAutosave = true;
  String  id             = getUuid(tabgroup);
  List    geometry       = null;
  List    attributes     = null;
  SaveCallback saveCallback  = new SaveCallback() {
    onSave(uuid, newRecord) {
      setUuid(tabgroup, uuid);
      populateAuthorAndTimestamp(tabgroup);
      execute(callback);
    }
    onError(message) {
      showToast(message);
    }
  };

  populateAuthorAndTimestamp(tabgroup);
  saveTabGroup(tabgroup, id, geometry, attributes, saveCallback, enableAutosave);
}

populateAuthorAndTimestamp(String tabgroup) {
  Map tabgroupToAuthor    = new HashMap();
  Map tabgroupToTimestamp = new HashMap();

</xsl:text>
    <xsl:call-template name="populate-author" />
    <xsl:call-template name="populate-timestamp" />
<xsl:text>
  String authorPath    = tabgroupToAuthor.get(tabgroup);
  String timestampPath = tabgroupToTimestamp.get(tabgroup);
  String uuid = getUuid(tabgroup);
  if (isNull(uuid)) {
    if (!isNull(authorPath))
      setFieldValue(authorPath,    "Entity not yet saved");
    if (!isNull(timestampPath))
      setFieldValue(timestampPath, "Entity not yet saved");
    return;
  }

  String q = "SELECT createdat, createdby " +
             "  FROM createdmodifiedatby " +
             " WHERE uuid = '" + uuid + "'";
  FetchCallback callback = new FetchCallback() {
    onFetch(result) {
      setFieldValue(timestampPath, result.get(0));
      setFieldValue(authorPath,    result.get(1));
    }
  };

  fetchOne(q, callback);
}

</xsl:text>
    <xsl:for-each select="/module/*[not(ancestor-or-self::*[contains(@f, 'onlyui') or contains(@f, 'onlydata')])]">
      <xsl:text>onShow</xsl:text>
      <xsl:call-template name="string-replace-all">
        <xsl:with-param name="text" select="name()" />
        <xsl:with-param name="replace" select="'_'" />
        <xsl:with-param name="by" select="''" />
      </xsl:call-template>
<xsl:text> () {
  // TODO: Add some things which should happen when this tab group is shown
  saveTabGroup("</xsl:text>
      <xsl:value-of select="name()" />
<xsl:text>");
}</xsl:text>
      <xsl:value-of select="$newline" />
    </xsl:for-each>
    <xsl:value-of select="$newline" />
    <xsl:for-each select="/module/*[not(ancestor-or-self::*[contains(@f, 'onlyui') or contains(@f, 'onlydata')])]">
      <xsl:text>onEvent("</xsl:text>
      <xsl:value-of select="name()"/>
      <xsl:text>", "show", "onShow</xsl:text>
      <xsl:call-template name="string-replace-all">
        <xsl:with-param name="text" select="name()" />
        <xsl:with-param name="replace" select="'_'" />
        <xsl:with-param name="by" select="''" />
      </xsl:call-template>
      <xsl:text>()");</xsl:text>
      <xsl:value-of select="$newline" />
    </xsl:for-each>

    <xsl:value-of select="$newline" />

    <!-- Triggers/buttons which link to a tab or tabgroup -->
    <xsl:for-each select="//*[@l]">
      <xsl:text>onClick</xsl:text>
        <xsl:call-template name="string-replace-all">
          <xsl:with-param name="text" select="name(ancestor::*[last()-1])" />
          <xsl:with-param name="replace" select="'_'" />
          <xsl:with-param name="by" select="''" />
        </xsl:call-template>
      <xsl:call-template name="string-replace-all">
        <xsl:with-param name="text" select="name()" />
        <xsl:with-param name="replace" select="'_'" />
        <xsl:with-param name="by" select="''" />
      </xsl:call-template>
<xsl:text> () {
  // TODO: Add some things which should happen when this element is clicked
</xsl:text>
      <xsl:variable name="link" select="@l"/>
      <xsl:choose>
        <xsl:when test="
          not(contains($link, '/')) and
          not(/module/*[name() = $link and
            (contains(@f, 'onlydata') or
             contains(@f, 'onlyui'))
          ])">
          <xsl:text>  new</xsl:text>
          <xsl:call-template name="string-replace-all">
            <xsl:with-param name="text" select="$link" />
            <xsl:with-param name="replace" select="'_'" />
            <xsl:with-param name="by" select="''" />
          </xsl:call-template>
          <xsl:text>();</xsl:text>
        </xsl:when>
        <xsl:otherwise>
          <xsl:text>  newTab("</xsl:text>
          <xsl:value-of select="@l"/>
          <xsl:text>", true);</xsl:text>
        </xsl:otherwise>
      </xsl:choose>
      <xsl:value-of select="$newline" />
      <xsl:text>}</xsl:text>
      <xsl:value-of select="$newline" />
    </xsl:for-each>
    <xsl:value-of select="$newline" />

    <xsl:for-each select="//*[@l]">
      <xsl:variable name="show-tab-string">
        <xsl:text>"onClick</xsl:text>
        <xsl:call-template name="string-replace-all">
          <xsl:with-param name="text" select="name(ancestor::*[last()-1])" />
          <xsl:with-param name="replace" select="'_'" />
          <xsl:with-param name="by" select="''" />
        </xsl:call-template>
        <xsl:call-template name="string-replace-all">
          <xsl:with-param name="text" select="name()" />
          <xsl:with-param name="replace" select="'_'" />
          <xsl:with-param name="by" select="''" />
        </xsl:call-template>
        <xsl:text>()"</xsl:text>
      </xsl:variable>

      <xsl:variable name="button-path">
        <xsl:value-of select="name(ancestor::*[last()-1])"/>
        <xsl:text>/</xsl:text>
        <xsl:value-of select="name(ancestor::*[last()-2])"/>
        <xsl:text>/</xsl:text>
        <xsl:value-of select="name()"/>
      </xsl:variable>

      <xsl:text>onEvent("</xsl:text>
      <xsl:value-of select="$button-path"/>
      <xsl:text>", "click", </xsl:text>
      <xsl:value-of select="$show-tab-string"/>
      <xsl:text>);</xsl:text>
      <xsl:value-of select="$newline" />
    </xsl:for-each>
    <xsl:value-of select="$newline" />

    <!-- onEvent calls for audio, camera, file and video GUI elements -->
<xsl:text>
/******************************************************************************/
/*                   AUDIO, CAMERA, FILE AND VIDEO BINDINGS                   */
/******************************************************************************/
</xsl:text>
    <xsl:for-each select="//*[normalize-space(@t) = 'audio']">
      <xsl:text>onEvent("</xsl:text>
      <xsl:value-of select="name(ancestor::*[last()-1])"/>
      <xsl:text>/</xsl:text>
      <xsl:value-of select="name(ancestor::*[last()-2])"/>
      <xsl:text>/Button_</xsl:text>
      <xsl:value-of select="name()"/>
      <xsl:text>", "click", "attachAudioTo(\"</xsl:text>
      <xsl:call-template name="ref" />
      <xsl:text>\")");</xsl:text>
      <xsl:value-of select="$newline" />
    </xsl:for-each>
    <xsl:for-each select="//*[normalize-space(@t) = 'camera']">
      <xsl:text>onEvent("</xsl:text>
      <xsl:value-of select="name(ancestor::*[last()-1])"/>
      <xsl:text>/</xsl:text>
      <xsl:value-of select="name(ancestor::*[last()-2])"/>
      <xsl:text>/Button_</xsl:text>
      <xsl:value-of select="name()"/>
      <xsl:text>", "click", "attachPictureTo(\"</xsl:text>
      <xsl:call-template name="ref" />
      <xsl:text>\")");</xsl:text>
      <xsl:value-of select="$newline" />
    </xsl:for-each>
    <xsl:for-each select="//*[normalize-space(@t) = 'file']">
      <xsl:text>onEvent("</xsl:text>
      <xsl:value-of select="name(ancestor::*[last()-1])"/>
      <xsl:text>/</xsl:text>
      <xsl:value-of select="name(ancestor::*[last()-2])"/>
      <xsl:text>/Button_</xsl:text>
      <xsl:value-of select="name()"/>
      <xsl:text>", "click", "attachFileTo(\"</xsl:text>
      <xsl:call-template name="ref" />
      <xsl:text>\")");</xsl:text>
      <xsl:value-of select="$newline" />
    </xsl:for-each>
    <xsl:for-each select="//*[normalize-space(@t) = 'video']">
      <xsl:text>onEvent("</xsl:text>
      <xsl:value-of select="name(ancestor::*[last()-1])"/>
      <xsl:text>/</xsl:text>
      <xsl:value-of select="name(ancestor::*[last()-2])"/>
      <xsl:text>/Button_</xsl:text>
      <xsl:value-of select="name()"/>
      <xsl:text>", "click", "attachVideoTo(\"</xsl:text>
      <xsl:call-template name="ref" />
      <xsl:text>\")");</xsl:text>
      <xsl:value-of select="$newline" />
    </xsl:for-each>

    <!-- Navigation Drawer -->
<xsl:text>
/******************************************************************************/
/*                             NAVIGATION DRAWER                              */
/******************************************************************************/
removeNavigationButtons() {
  removeNavigationButton("new");
  removeNavigationButton("duplicate");
  removeNavigationButton("delete");
  removeNavigationButton("validate");
}

addNavigationButtons(String tabgroup) {
  removeNavigationButtons();

  addNavigationButton("new", new ActionButtonCallback() {
    actionOnLabel() {
      "{New}";
    }
    actionOn() {
      if(!isNull(getUuid(tabgroup))) {
          newRecord(tabgroup);
          showToast("{New_record_created}");
      } else {
          showAlert("{Warning}", "{Any_unsaved_changes_will_be_lost}", "newRecord(\""+tabgroup+"\")", "");
      }
    }
  }, "success");
  addNavigationButton("duplicate", new ActionButtonCallback() {
    actionOnLabel() {
      "{Duplicate}";
    }
    actionOn() {
      if(!isNull(getUuid(tabgroup))) {
          duplicateRecord(tabgroup);
      } else {
          showWarning("{Warning}", "{This_record_is_unsaved_and_cannot_be_duplicated}");
      }
    }
  }, "primary");
  addNavigationButton("delete", new ActionButtonCallback() {
    actionOnLabel() {
      "{Delete}";
    }
    actionOn() {
      deleteRecord(tabgroup);
    }
  }, "danger");
  addNavigationButton("validate", new ActionButtonCallback() {
    actionOnLabel() {
      "{Validate}";
    }
    actionOn() {
      String validationFunction = "validate" + tabgroup.replaceAll("_", "") + "()";
      eval(validationFunction);
    }
  }, "default");
}

// Makes a new record of the given tabgroup
newRecord(String tabgroup) {
  cancelTabGroup(tabgroup, false);

  String newTabGroupFunction = "new" + tabgroup.replaceAll("_", "") + "()"; // Typical value: "newTabgroup()"
  eval(newTabGroupFunction);

  Log.d("newRecord", tabgroup);
}

// Deletes the current record of the given tabgroup
deleteRecord(String tabgroup) {
  String deleteTabGroupFunction = "delete" + tabgroup.replaceAll("_", "") + "()"; // Typical value: "deleteTabgroup()"
  eval(deleteTabGroupFunction);

  Log.d("deleteRecord", tabgroup);
}

// Duplicates the current record of the given tabgroup
duplicateRecord(String tabgroup) {
  dialog = showBusy("Duplicating", "Please wait...");

  String duplicateTabGroupFunction = "duplicate" + tabgroup.replaceAll("_", "") + "()"; // Typical value: "duplicateTabgroup()"
  eval(duplicateTabGroupFunction);

  Log.d("duplicateRecord", tabgroup);
}

// generic fetch saved attributes query
getDuplicateAttributeQuery(String originalRecordID, String attributesToDupe) {
  if (attributesToDupe.equals("")) {
    attributesToDupe = "''";
  }
  String duplicateQuery = "SELECT attributename, freetext, vocabid, measure, certainty " +
                          "  FROM latestnondeletedaentvalue JOIN attributekey USING (attributeid) " +
                          " WHERE attributename IN ('', "+attributesToDupe+") " +
                          "   AND uuid = '"+originalRecordID+"'; ";
  return duplicateQuery;
}

// generic get extra attributes
getExtraAttributes(fetchedAttributes) {
  List extraAttributes = createAttributeList();
  Log.d("Module", "Duplicating fetched attributes: " + fetchedAttributes.toString());
  for (savedAttribute : fetchedAttributes) {
    extraAttributes.add(
      createEntityAttribute(
        savedAttribute.get(0),
        savedAttribute.get(1),
        savedAttribute.get(2),
        savedAttribute.get(3),
        savedAttribute.get(4)
      )
    );
  }
  return extraAttributes;
}

</xsl:text>
    <xsl:for-each select="/module/*[not(ancestor-or-self::*[contains(@f, 'onlyui') or contains(@f, 'onlydata')])]">
      <xsl:call-template name="tabgroup-new" />
      <xsl:call-template name="tabgroup-duplicate" />
      <xsl:call-template name="tabgroup-delete" />
      <xsl:call-template name="tabgroup-really-delete" />
    </xsl:for-each>
<xsl:text>
doNotDelete(){
  showToast("{Delete_Cancelled}");
}
</xsl:text>
    <xsl:for-each select="/module/*[ancestor-or-self::*[contains(@f, 'onlyui') or contains(@f, 'onlydata')]]">
      <xsl:text>onEvent("</xsl:text>
      <xsl:value-of select="name()"/>
      <xsl:text>", "show", "removeNavigationButtons()");</xsl:text>
      <xsl:value-of select="$newline"/>
    </xsl:for-each>
    <xsl:for-each select="/module/*[not(ancestor-or-self::*[contains(@f, 'onlyui') or contains(@f, 'onlydata')])]">
      <xsl:text>onEvent("</xsl:text>
      <xsl:value-of select="name()"/>
      <xsl:text>", "show", "addNavigationButtons(\"</xsl:text>
      <xsl:value-of select="name()"/>
      <xsl:text>\")");</xsl:text>
      <xsl:value-of select="$newline"/>
    </xsl:for-each>

    <!-- Search -->
    <xsl:if test="/module/*/search">
      <xsl:if test="count(/module/*/search) &gt; 1">
        <xsl:text>// WARNING: More than one search tab found. Settting bindings for only the first.</xsl:text>
      </xsl:if>
      <xsl:text>
/******************************************************************************/
/*                                   SEARCH                                   */
/******************************************************************************/
onEvent("</xsl:text><xsl:value-of select="name(/module/*[./search])"/><xsl:text>/Search"               , "show"  , "search();");
onEvent("</xsl:text><xsl:value-of select="name(/module/*[./search])"/><xsl:text>/Search/Entity_List"   , "click" , "loadEntity();");
onEvent("</xsl:text><xsl:value-of select="name(/module/*[./search])"/><xsl:text>/Search/Search_Button" , "click" , "search()");
onEvent("</xsl:text><xsl:value-of select="name(/module/*[./search])"/><xsl:text>/Search/Search_Term"   , "click" , "clearSearch()");
</xsl:text>
      <xsl:call-template name="search-entities" />
      <xsl:text>
clearSearch(){
  setFieldValue("</xsl:text><xsl:value-of select="name(/module/*[./search])"/><xsl:text>/Search/Search_Term","");
}

search(){
  String tabgroup = "</xsl:text><xsl:value-of select="name(/module/*[./search])"/><xsl:text>";
  String refEntityList  = tabgroup + "/Search/Entity_List";
  String refSearchTerm  = tabgroup + "/Search/Search_Term";
  String refEntityTypes = tabgroup + "/Search/Entity_Types";

</xsl:text>
<xsl:if test="count(/module/*[not(contains(@f, 'onlyui')) and not(name() = 'rels') and (./*//*[not(ancestor-or-self::*[contains(@f, 'onlyui') or contains(@f, 'user')]) and not(name() = 'cols') and not(name() = 'col') and not(name() = 'desc') and not(name() = 'opt') and not(name() = 'opts') and not(ancestor-or-self::rels) and not(normalize-space(@t) = 'group') and not(normalize-space(@t) = 'gpsdiag') and not(normalize-space(@t) = 'map') and not(normalize-space(@t) = 'button')])]) &lt; 2">
  <xsl:text>  String type = "All";</xsl:text>
</xsl:if>
<xsl:if test="count(/module/*[not(contains(@f, 'onlyui')) and not(name() = 'rels') and (./*//*[not(ancestor-or-self::*[contains(@f, 'onlyui') or contains(@f, 'user')]) and not(name() = 'cols') and not(name() = 'col') and not(name() = 'desc') and not(name() = 'opt') and not(name() = 'opts') and not(ancestor-or-self::rels) and not(normalize-space(@t) = 'group') and not(normalize-space(@t) = 'gpsdiag') and not(normalize-space(@t) = 'map') and not(normalize-space(@t) = 'button')])]) &gt;= 2">
  <xsl:text>  String type = getFieldValue(refEntityTypes);</xsl:text>
</xsl:if>
<xsl:text>
  String term = getFieldValue(refSearchTerm);
  String searchQuery = "SELECT uuid, response "+
                       "  FROM latestNonDeletedArchEntFormattedIdentifiers  "+
                       " WHERE uuid in (SELECT uuid "+
                       "                  FROM latestNonDeletedArchEntIdentifiers "+
                       "                 WHERE attributename != 'Site Code' "+
                       "                   AND measure LIKE '"+term+"'||'%'  "+
                       "                   AND ( aenttypename LIKE '"+type+"' OR 'All' = '"+type+"' ) "+
                       "                )  "+
                       " ORDER BY response "+
                       " LIMIT ? "+
                       "OFFSET ? ";

  populateCursorList(refEntityList, searchQuery, 25);
  refreshTabgroupCSS(tabgroup);

  Log.d("Boncuklu Module", "Search query: " + searchQuery);
}

loadEntity() {
  loadEntityFrom(getListItemValue());
}

loadEntityFrom(String entityID) {
  if (isNull(entityID)) {
    Log.e("Module", "Cannot load an entity with a null ID.");
    return;
  }

  String getEntTypeNameQ = "SELECT aenttypename " +
                           "  FROM latestnondeletedarchent " +
                           "  JOIN aenttype " +
                           " USING (aenttypeid) " +
                           " WHERE uuid = '" + entityID + "'";
  fetchAll(getEntTypeNameQ, new FetchCallback() {
    onFetch(result) {
      String archEntName = result.get(0).get(0);
      String loadFunction = "load" + archEntName.replaceAll(" ", "") + "From(entityID)"; // Typical value: loadContextFrom(entityID)
      eval(loadFunction);
    }
  });
}
</xsl:text>
      <xsl:value-of select="$newline"/>
      <xsl:call-template name="load-entity-functions" />
    </xsl:if>

    <!-- Take From GPS Button -->
    <xsl:if test="/module/*/*/gps">
      <xsl:text>
/******************************************************************************/
/*                          TAKE FROM GPS BUTTON(S)                           */
/******************************************************************************/
</xsl:text>
<xsl:call-template name="take-from-gps-bindings"/>
<xsl:text>
/* Takes the current point using gps. */
takePoint(String tabgroup) {
  String archEntType = tabgroup.replaceAll("_", " ");
  String currentUuid = getUuid(tabgroup);
  if (isNull(currentUuid)){
    showToast("Please enter data first and let a save occur.");
  }

  Object position = getGPSPosition();
  if (position == null) {
    showToast("{GPS_Not_Initialised}");
    return;
  }

  Object projPosition = getGPSPositionProjected();
  Double latitude     = position.getLatitude();
  Double longitude    = position.getLongitude();
  Double northing     = projPosition.getLatitude();
  Double easting      = projPosition.getLongitude();

  samplePoint = new Point(new MapPos(easting, northing), null, (PointStyle) null, null);
  ArrayList geolist = new ArrayList();
  geolist.add(samplePoint);

  attributes = createAttributeList();
  attributes.add(createEntityAttribute("Latitude", "Accuracy: "+getGPSEstimatedAccuracy(), null, null, null));

  saveArchEnt(currentUuid, archEntType, geolist, attributes, new SaveCallback() {
    onSave(uuid, newRecord) {
      print("[takePoint()] Added geometry: " + geolist);
      fillInGPS(tabgroup);
    }
  });
}

/* Sets the value of GPS views for the given tab path. */
fillInGPS(String tabgroup) {
</xsl:text>
    <xsl:call-template name="take-from-gps-mappings"/>
<xsl:text>
  String currentUuid = getUuid(tabgroup);
  if (isNull(currentUuid)) {
    return;
  }

  String query = "SELECT x(transform(geospatialcolumn,                4326)) as longtiude, " +
                 "       y(transform(geospatialcolumn,                4326)) as latitude, " +
                 "       x(transform(geospatialcolumn, "+getModuleSrid()+")) as easting, " +
                 "       y(transform(geospatialcolumn, "+getModuleSrid()+")) as northing " +
                 "  FROM latestnondeletedarchent, vocabulary " +
                 " WHERE uuid = '" + currentUuid + "';";

  fetchOne(query, new FetchCallback() {
    onFetch(result) {
      print("[fillInGPS()] Fetched DB transformed geometry: " + result);
      setFieldValue(tabgroupToTabRef.get(tabgroup) + "Latitude"  , result.get(0));
      setFieldValue(tabgroupToTabRef.get(tabgroup) + "Longitude" , result.get(1));
      setFieldValue(tabgroupToTabRef.get(tabgroup) + "Northing"  , result.get(2));
      setFieldValue(tabgroupToTabRef.get(tabgroup) + "Easting"   , result.get(3));
    }
  });
}
</xsl:text>
    </xsl:if>

    <xsl:if test="//autonum">
<xsl:text>
/******************************************************************************/
/*                       AUTONUMBERING HELPER FUNCTIONS                       */
/******************************************************************************/
insertIntoLocalSettings(String key, String val) {
    fetchOne("REPLACE INTO localSettings(key, value) VALUES('" + key + "', '" + val + "');");
}

insertIntoLocalSettings(String key, Integer val) {
    insertIntoLocalSettings(key, Integer.toString(val));
}

/*
 * If value of field specified by `ref` is null, sets the field to `defaultVal`,
 * otherwise increments its value.
 *
 * Returns the value the field was updated to.
 */
incField(String ref, Integer defaultVal) {
  String val = getFieldValue(ref);

  if (isNull(val)) {
    setFieldValue(ref, defaultVal);
    return defaultVal;
  }

  Integer inc = Integer.parseInt(val) + 1;
  setFieldValue(ref, inc);
  insertIntoLocalSettings(ref, inc.toString());

  return inc;
}

/* Increments the field at `ref` or returns null if it does not contain a
 * number.
 */
incField(String ref) {
  return incField(ref, 1);
}

onEvent("Control", "load", "onLoadControl()");

/* This function should only be called once since it creates event handlers,
 * otherwise multiple copies of the same handler will trigger with the event.
 */
onLoadControl() {
  List l = new ArrayList();
</xsl:text>
      <xsl:call-template name="control-starting-id-paths"/>
<xsl:text>

  for (ref : l) {
    loadStartingId(ref);
  }
  for (ref : l) {
    onFocus(ref, null,  "insertIntoLocalSettings(\"" + ref + "\", getFieldValue(\"" + ref + "\"));");
  }
}

loadStartingId(String ref) {
  String idQ = "SELECT value FROM localSettings WHERE key = '" + ref + "';";
  fetchOne(idQ, new FetchCallback() {
    onFetch(result) {
      if (!isNull(result)) {
        setFieldValue(ref, result.get(0));
      } else {
        setFieldValue(ref, "1");
      }
    }
  });
}

</xsl:text>
      <xsl:call-template name="incautonum"/>
    </xsl:if>

  </xsl:template>

  <xsl:template name="populate-author">
    <xsl:for-each select="//author">
      <xsl:text>  tabgroupToAuthor.put("</xsl:text>
      <xsl:value-of select="name(ancestor::*[last()-1])" />
      <xsl:text>", "</xsl:text>
      <xsl:value-of select="name(ancestor::*[last()-1])" />
      <xsl:text>/</xsl:text>
      <xsl:value-of select="name(ancestor::*[last()-2])" />
      <xsl:text>/Author</xsl:text>
      <xsl:text>");</xsl:text>
      <xsl:value-of select="$newline"/>
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="populate-timestamp">
    <xsl:for-each select="//timestamp">
      <xsl:text>  tabgroupToTimestamp.put("</xsl:text>
      <xsl:value-of select="name(ancestor::*[last()-1])" />
      <xsl:text>", "</xsl:text>
      <xsl:value-of select="name(ancestor::*[last()-1])" />
      <xsl:text>/</xsl:text>
      <xsl:value-of select="name(ancestor::*[last()-2])" />
      <xsl:text>/Timestamp</xsl:text>
      <xsl:text>");</xsl:text>
      <xsl:value-of select="$newline"/>
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="incautonum">
    <xsl:text>incAutoNum(String destPath) {</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>  Map destToSource = new HashMap();</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:call-template name="incautonum-map"/>
    <xsl:text></xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>  String sourcePath = destToSource.get(destPath);</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>  String destVal    = getFieldValue(sourcePath);</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>  setFieldValue(destPath, destVal);</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>  incField(sourcePath);</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>}</xsl:text>
    <xsl:value-of select="$newline"/>
  </xsl:template>
  <xsl:template name="incautonum-map">
    <xsl:for-each select="//*[contains(@f, 'autonum')]">
      <xsl:text>  destToSource.put("</xsl:text>
      <xsl:call-template name="ref" />
      <xsl:text>", "</xsl:text>
      <xsl:value-of select="name(//autonum/ancestor::*[last()-1])" />
      <xsl:text>/</xsl:text>
      <xsl:value-of select="name(//autonum/ancestor::*[last()-2])" />
      <xsl:text>/Next_</xsl:text>
      <xsl:value-of select="name()"/>
      <xsl:text>");</xsl:text>
      <xsl:value-of select="$newline"/>
    </xsl:for-each>
  </xsl:template>
  <xsl:template name="control-starting-id-paths">
    <xsl:for-each select="//*[contains(@f, 'autonum')]">
      <xsl:text>  l.add("</xsl:text>
      <xsl:value-of select="name(//autonum/ancestor::*[last()-1])" />
      <xsl:text>/</xsl:text>
      <xsl:value-of select="name(//autonum/ancestor::*[last()-2])" />
      <xsl:text>/Next_</xsl:text>
      <xsl:value-of select="name()"/>
      <xsl:text>");</xsl:text>
      <xsl:value-of select="$newline"/>
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="take-from-gps-bindings">
    <xsl:for-each select="/module//gps">
      <xsl:text>onEvent("</xsl:text>
      <xsl:value-of select="name(ancestor::*[last()-1])"/>
      <xsl:text>/</xsl:text>
      <xsl:value-of select="name(ancestor::*[last()-2])"/>
      <xsl:text>/Take_From_GPS</xsl:text>
      <xsl:text>", "click", "takePoint(\"</xsl:text>
      <xsl:value-of select="name(ancestor::*[last()-1])"/>
      <xsl:text>\")");</xsl:text>
      <xsl:value-of select="$newline"/>
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="take-from-gps-mappings">
    <xsl:text>  Map tabgroupToTabRef = new HashMap();</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:for-each select="/module//gps">
      <xsl:text>  tabgroupToTabRef.put("</xsl:text>
      <xsl:value-of select="name(ancestor::*[last()-1])"/>
      <xsl:text>", "</xsl:text>
      <xsl:value-of select="name(ancestor::*[last()-1])"/>
      <xsl:text>/</xsl:text>
      <xsl:value-of select="name(ancestor::*[last()-2])"/>
      <xsl:text>/");</xsl:text>
      <xsl:value-of select="$newline"/>
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="load-entity-functions">
    <xsl:for-each select="/module/*[not(contains(@f, 'onlyui'))]">
      <xsl:text>load</xsl:text>
      <xsl:call-template name="string-replace-all">
        <xsl:with-param name="text" select="name()" />
        <xsl:with-param name="replace" select="'_'" />
        <xsl:with-param name="by" select="''" />
      </xsl:call-template>
      <xsl:text>From(String uuid) {
  String tabgroup = "</xsl:text><xsl:value-of select="name()"/><xsl:text>";
  setUuid(tabgroup, uuid);
  if (isNull(uuid)) return;

  showTabGroup(tabgroup, uuid);
}</xsl:text>
      <xsl:value-of select="$newline"/>
      <xsl:value-of select="$newline"/>
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="tabgroup-new">
    <xsl:variable name="camelcase-tabgroup">
      <xsl:call-template name="string-replace-all">
        <xsl:with-param name="text" select="name()" />
        <xsl:with-param name="replace" select="'_'" />
        <xsl:with-param name="by" select="''" />
      </xsl:call-template>
    </xsl:variable>

    <xsl:text>new</xsl:text>
    <xsl:value-of select="$camelcase-tabgroup"/>
    <xsl:text>(){</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>  String tabgroup = "</xsl:text>
    <xsl:value-of select="name()"/>
    <xsl:text>";</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:value-of select="$newline"/>
    <xsl:call-template name="tabgroup-new-no-id"/>
<xsl:text>
  setUuid(tabgroup, null);
  newTabGroup(tabgroup);

</xsl:text>
    <xsl:call-template name="tabgroup-new-incautonum"/>
    <xsl:text>}</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:value-of select="$newline"/>
  </xsl:template>

  <xsl:template name="tabgroup-new-no-id">
    <xsl:if test=".//*[contains(@f, 'autonum')]">
      <xsl:text>  String autoNumSource = "";</xsl:text>
      <xsl:value-of select="$newline"/>
    </xsl:if>
    <xsl:for-each select=".//*[contains(@f, 'autonum')]">
      <xsl:text>  autoNumSource = getFieldValue("</xsl:text>
      <xsl:value-of select="name(//autonum/ancestor::*[last()-1])" />
      <xsl:text>/</xsl:text>
      <xsl:value-of select="name(//autonum/ancestor::*[last()-2])" />
      <xsl:text>/Next_</xsl:text>
      <xsl:value-of select="name()"/>
      <xsl:text>");</xsl:text>
      <xsl:value-of select="$newline"/>
      <xsl:text>  if (isNull(autoNumSource)) {</xsl:text>
      <xsl:value-of select="$newline"/>
      <xsl:text>    showWarning("{Alert}","{A_next_ID_has_not_been_entered_please_provide_one}");</xsl:text>
      <xsl:value-of select="$newline"/>
      <xsl:text>    return;</xsl:text>
      <xsl:value-of select="$newline"/>
      <xsl:text>  }</xsl:text>
      <xsl:value-of select="$newline"/>
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="tabgroup-new-incautonum">
    <xsl:if test=".//*[contains(@f, 'autonum')]">
      <xsl:text>  String autoNumDest = "";</xsl:text>
      <xsl:value-of select="$newline"/>
    </xsl:if>
    <xsl:for-each select=".//*[contains(@f, 'autonum')]">
      <xsl:text>  autoNumDest = "</xsl:text>
      <xsl:call-template name="ref" />
      <xsl:text>";</xsl:text>
      <xsl:value-of select="$newline"/>
      <xsl:text>  incAutoNum(autoNumDest);</xsl:text>
      <xsl:value-of select="$newline"/>
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="tabgroup-duplicate-incautonum">
    <xsl:call-template name="tabgroup-new-incautonum"/>
  </xsl:template>

  <xsl:template name="tabgroup-duplicate">
    <xsl:variable name="camelcase-tabgroup">
      <xsl:call-template name="string-replace-all">
        <xsl:with-param name="text" select="name()" />
        <xsl:with-param name="replace" select="'_'" />
        <xsl:with-param name="by" select="''" />
      </xsl:call-template>
    </xsl:variable>

    <xsl:text>duplicate</xsl:text>
    <xsl:value-of select="$camelcase-tabgroup"/>
    <xsl:text>(){</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>  String tabgroup = "</xsl:text>
    <xsl:value-of select="name()"/>
    <xsl:text>";</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:value-of select="$newline"/>
    <xsl:text>  disableAutoSave(tabgroup);</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:value-of select="$newline"/>
    <xsl:call-template name="tabgroup-duplicate-incautonum"/>
    <xsl:value-of select="$newline"/>
    <xsl:call-template name="tabgroup-duplicate-exclusions-1" />
<xsl:text>

  saveCallback = new SaveCallback() {
    onSave(uuid, newRecord) {
      setUuid(tabgroup, uuid);
      populateAuthorAndTimestamp(tabgroup);

      Boolean enable_autosave = true;
      showToast("{Duplicated_record}");
      dialog.dismiss();
      saveTabGroup(tabgroup, getUuid(tabgroup), null, null, new SaveCallback(){
        onSave(autosaveUuid, autosaveNewRecord) {
          setUuid(tabgroup, autosaveUuid);
        }
      }, enable_autosave);
    }
  };

  String extraDupeAttributes = "";
  fetchAll(getDuplicateAttributeQuery(getUuid(tabgroup), extraDupeAttributes), new FetchCallback(){
    onFetch(result) {
      excludeAttributes = new ArrayList();
</xsl:text>
    <xsl:call-template name="tabgroup-duplicate-exclusions-2" />
<xsl:text>
      duplicateTabGroup(tabgroup, null, getExtraAttributes(result), excludeAttributes, saveCallback);
    }
  });
}
</xsl:text>
    <xsl:value-of select="$newline"/>
  </xsl:template>

  <xsl:template name="tabgroup-duplicate-exclusions-1">
    <xsl:for-each select=".//*[@t and not(ancestor-or-self::*[contains(@f, 'onlyui') or contains(@f, 'onlydata')]) and not(contains(@f, 'user'))]">
      <xsl:choose>
        <xsl:when test="normalize-space(@t) = 'audio'">
          <xsl:text>  populateFileList("</xsl:text>
          <xsl:call-template name="ref" />
          <xsl:text>", new ArrayList());</xsl:text>
          <xsl:value-of select="$newline" />
        </xsl:when>
        <xsl:when test="normalize-space(@t) = 'camera'">
          <xsl:text>  populateCameraPictureGallery("</xsl:text>
          <xsl:call-template name="ref" />
          <xsl:text>", new ArrayList());</xsl:text>
          <xsl:value-of select="$newline" />
        </xsl:when>
        <xsl:when test="normalize-space(@t) = 'file'">
          <xsl:text>  populateFileList("</xsl:text>
          <xsl:call-template name="ref" />
          <xsl:text>", new ArrayList());</xsl:text>
          <xsl:value-of select="$newline" />
        </xsl:when>
        <xsl:when test="normalize-space(@t) = 'video'">
          <xsl:text>  populateVideoGallery("</xsl:text>
          <xsl:call-template name="ref" />
          <xsl:text>", new ArrayList());</xsl:text>
          <xsl:value-of select="$newline" />
        </xsl:when>
      </xsl:choose>
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="tabgroup-duplicate-exclusions-2">
    <xsl:for-each select=".//*[
      (
        normalize-space(@t) = 'audio' or
        normalize-space(@t) = 'camera' or
        normalize-space(@t) = 'file' or
        normalize-space(@t) = 'video'
      ) and
      not(ancestor-or-self::*[contains(@f, 'onlyui') or contains(@f, 'onlydata')]) and not(contains(@f, 'user'))]">

      <xsl:text>      excludeAttributes.add("</xsl:text>
      <xsl:call-template name="string-replace-all">
        <xsl:with-param name="text" select="name(.)" />
        <xsl:with-param name="replace" select="'_'" />
        <xsl:with-param name="by" select="' '" />
      </xsl:call-template>
      <xsl:text>");</xsl:text>
      <xsl:value-of select="$newline" />
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="tabgroup-delete">
    <xsl:variable name="camelcase-tabgroup">
      <xsl:call-template name="string-replace-all">
        <xsl:with-param name="text" select="name()" />
        <xsl:with-param name="replace" select="'_'" />
        <xsl:with-param name="by" select="''" />
      </xsl:call-template>
    </xsl:variable>

    <xsl:text>delete</xsl:text>
    <xsl:value-of select="$camelcase-tabgroup" />
    <xsl:text>(){</xsl:text>
    <xsl:value-of select="$newline" />
    <xsl:text>  String tabgroup = "</xsl:text>
    <xsl:value-of select="name()"/>
    <xsl:text>";</xsl:text>
    <xsl:value-of select="$newline"/>
<xsl:text>
  if (isNull(getUuid(tabgroup))) {
    cancelTabGroup(tabgroup, true);
  } else {
    showAlert("{Confirm_Deletion}", "{Press_OK_to_Delete_this_Record}", "reallyDelete</xsl:text>
    <xsl:value-of select="$camelcase-tabgroup" />
    <xsl:text>()", "doNotDelete()");
  }
}
</xsl:text>
    <xsl:value-of select="$newline"/>
  </xsl:template>

  <xsl:template name="tabgroup-really-delete">
    <xsl:variable name="camelcase-tabgroup">
      <xsl:call-template name="string-replace-all">
        <xsl:with-param name="text" select="name()" />
        <xsl:with-param name="replace" select="'_'" />
        <xsl:with-param name="by" select="''" />
      </xsl:call-template>
    </xsl:variable>

    <xsl:text>reallyDelete</xsl:text>
    <xsl:value-of select="$camelcase-tabgroup" />
    <xsl:text>(){</xsl:text>
    <xsl:value-of select="$newline" />
    <xsl:text>  String tabgroup = "</xsl:text>
    <xsl:value-of select="name()"/>
    <xsl:text>";</xsl:text>
<xsl:text>
  deleteArchEnt(getUuid(tabgroup));
  cancelTabGroup(tabgroup, false);
}
</xsl:text>
    <xsl:value-of select="$newline"/>
  </xsl:template>

  <xsl:template name="is-hierarchical">
    <xsl:if test=".//opt/opt">
      <xsl:text>1</xsl:text>
    </xsl:if>
  </xsl:template>

  <xsl:template name="ref">
    <xsl:value-of select="name(ancestor::*[last()-1])"/>
    <xsl:text>/</xsl:text>
    <xsl:value-of select="name(ancestor::*[last()-2])"/>
    <xsl:text>/</xsl:text>
    <xsl:value-of select="name()"/>
  </xsl:template>

  <xsl:template name="complete-makevocab">
    <xsl:variable name="faims-attribute-name">
      <xsl:call-template name="string-replace-all">
        <xsl:with-param name="text" select="name(.)" />
        <xsl:with-param name="replace" select="'_'" />
        <xsl:with-param name="by" select="' '" />
      </xsl:call-template>
    </xsl:variable>

    <xsl:call-template name="ref" />
    <xsl:text>", "</xsl:text>
    <xsl:value-of select="$faims-attribute-name" />
    <xsl:text>");</xsl:text>
    <xsl:value-of select="$newline" />
  </xsl:template>

  <xsl:template name="users">
    <xsl:for-each select="//*[contains(@f, 'user')][1]">
<xsl:text>
String userMenuPath = "</xsl:text><xsl:call-template name="ref" /><xsl:text>";

populateListForUsers(){
  String getNonDeletedUsersQuery = "SELECT userid, fname || ' ' || lname "+
                                   "  FROM user "+
                                   " WHERE userdeleted is null;";

  fetchAll(getNonDeletedUsersQuery, new FetchCallback() {
    onFetch(result) {
      populateDropDown(userMenuPath, result, true);
    }
  });
}

String username = "";

selectUser () {
  String userVocabId  = getFieldValue(userMenuPath);
  String userQ        = "SELECT userid,fname,lname,email FROM user " +
                        "WHERE  userid='" + userVocabId + "';";
  FetchCallback callback = new FetchCallback() {
    onFetch(result) {
      user = new User(
            result.get(0),
            result.get(1),
            result.get(2),
            result.get(3)
      );
      setUser(user);
      username = result.get(1) + " " + result.get(2);
    }
  };

  fetchOne(userQ, callback);
}

onEvent(userMenuPath, "show",  "populateListForUsers()");
onEvent(userMenuPath, "select", "selectUser()");
</xsl:text>
    </xsl:for-each>
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

  <xsl:template name="label">
    <xsl:choose>
      <xsl:when test="normalize-space(text())">
        <xsl:text>{</xsl:text>
        <xsl:call-template name="string-to-arch16n-key">
          <xsl:with-param name="string" select="normalize-space(text())" />
        </xsl:call-template>
        <xsl:text>}</xsl:text>
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>{</xsl:text>
        <xsl:call-template name="string-to-arch16n-key">
          <xsl:with-param name="string" select="name()" />
        </xsl:call-template>
        <xsl:text>}</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template name="search-entities">
    <xsl:if test="count(/module/*[not(contains(@f, 'onlyui')) and not(name() = 'rels') and (./*//*[not(ancestor-or-self::*[contains(@f, 'onlyui') or contains(@f, 'user')]) and not(name() = 'cols') and not(name() = 'col') and not(name() = 'desc') and not(name() = 'opt') and not(name() = 'opts') and not(ancestor-or-self::rels) and not(normalize-space(@t) = 'group') and not(normalize-space(@t) = 'gpsdiag') and not(normalize-space(@t) = 'map') and not(normalize-space(@t) = 'button')])]) &gt;= 2">
      <xsl:text>onEvent("</xsl:text><xsl:value-of select="name(/module/*[./search])"/><xsl:text>/Search/Entity_Types"  , "click" , "search()");</xsl:text>
      <xsl:value-of select="$newline" />
      <xsl:value-of select="$newline" />
      <xsl:text>entityTypes = new ArrayList();</xsl:text>
      <xsl:value-of select="$newline" />
      <xsl:text>entityTypes.add(new NameValuePair("{All}", "All"));</xsl:text>
      <xsl:value-of select="$newline" />
      <xsl:for-each select="/module/*[not(contains(@f, 'onlyui'))]">
        <xsl:text>entityTypes.add(new NameValuePair("{</xsl:text>
        <xsl:value-of select="name()"/>
        <xsl:text>}", "</xsl:text>
        <xsl:call-template name="string-replace-all">
          <xsl:with-param name="text" select="name()" />
          <xsl:with-param name="replace" select="'_'" />
          <xsl:with-param name="by" select="' '" />
        </xsl:call-template>
        <xsl:text>"));</xsl:text>
        <xsl:value-of select="$newline" />
      </xsl:for-each>
      <xsl:text>populateDropDown("</xsl:text><xsl:value-of select="name(/module/*[./search])"/><xsl:text>/Search/Entity_Types", entityTypes);</xsl:text>
      <xsl:value-of select="$newline" />
    </xsl:if>
  </xsl:template>

  <xsl:template name="gps-diag-ref">
    <xsl:for-each select="//*[normalize-space(@t) = 'gpsdiag'][1]">
      <xsl:call-template name="ref" />
    </xsl:for-each>
  </xsl:template>

</xsl:stylesheet>
