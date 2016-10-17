<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="text" indent="no"/>

  <xsl:variable name="newline" >
<xsl:text>
</xsl:text>
  </xsl:variable>

  <xsl:template match="/">

<xsl:text>import android.util.Log;

Object dialog;          // Used to help coordinate the display of a "busy..." dialog
String parentTabgroup;  // Used to allow entities to be saved as children
String parentTabgroup__;// Used to allow entities to be saved as children
String redirectTab;     // makes newTab work as expected
String username = "";
String userid   = "";

setFileSyncEnabled(true);
setSyncDelay(5.0f);
setSyncEnabled(true);
setSyncMaxInterval(600.0f);
setSyncMinInterval(5.0f);

/*********************** REGEX-FREE STRING REPLACEMENT ************************/
String replaceFirst(String haystack, String needle, String replacement) {
  i = haystack.indexOf(needle);
  if (i == -1)           return haystack;
  if (needle.equals("")) return haystack;
  pre  = haystack.substring(0, i                                   );
  post = haystack.substring(   i+needle.length(), haystack.length());
  return pre + replacement + post;
}

String replaceFirst(String haystack, String replacement) {
  return replaceFirst(haystack, "%s", replacement);
}

/******************************* LOCALSETTINGS ********************************/
void makeLocalID(){
  fetchOne("CREATE TABLE IF NOT EXISTS localSettings (key text primary key, value text);", null);
  fetchOne("DROP VIEW IF EXISTS parentchild;", null);
  fetchOne("CREATE VIEW parentchild AS "+
           "SELECT parent.uuid as parentuuid, child.uuid as childuuid, parent.participatesverb as parentparticipatesverb, parent.relationshipid, parent.aenttypename as parentaenttypename, child.participatesverb as childparticipatesverb, child.aenttypename as childaenttypename "+
           "  FROM (SELECT uuid, participatesverb, aenttypename, relationshipid"+
           "          FROM latestnondeletedaentreln "+
           "          JOIN relationship USING (relationshipid) "+
           "          JOIN latestnondeletedarchent USING (uuid) "+
           "          JOIN aenttype USING (aenttypeid)) parent "+
           "  JOIN (SELECT uuid, relationshipid, participatesverb, aenttypename "+
           "          FROM latestnondeletedaentreln "+
           "          JOIN relationship USING (relationshipid) "+
           "          JOIN latestnondeletedarchent USING (uuid) "+
           "          JOIN aenttype USING (aenttypeid)) child "+
           "    ON (parent.relationshipid = child.relationshipid AND parent.uuid != child.uuid);", null);
}
makeLocalID();

void insertIntoLocalSettings(String ref) {
  String val = getFieldValue(ref);
  insertIntoLocalSettings(ref, val);
}

void insertIntoLocalSettings(String key, String val) {
  fetchOne("REPLACE INTO localSettings(key, value) VALUES('" + key + "', '" + val + "');");
}

void insertIntoLocalSettings(String key, Integer val) {
  insertIntoLocalSettings(key, Integer.toString(val));
}

void insertIntoLocalSettingsOnChange(String ref) {
  String val = getFieldValue(ref);

  String insertCallback  = "";
  insertCallback += "insertIntoLocalSettings(\"{key}\")";
  insertCallback  = replaceFirst(insertCallback, "{key}", ref);

  addOnEvent(ref, "blur",  insertCallback);
  addOnEvent(ref, "click", insertCallback);
}

void setFieldValueFromLocalSettings(String key, String ref, boolean doOverwrite) {
  String val = getFieldValue(ref);
  if (!isNull(val) &amp;&amp; !doOverwrite) {
    return;
  }

  String q = "SELECT value FROM localSettings WHERE key = '" + key + "';";
  fetchOne(q, new FetchCallback() {
    onFetch(result) {
      if (!isNull(result)) {
        setFieldValue(ref, result.get(0));
      }
    }
  });
}

void setFieldValueFromLocalSettings(String ref, boolean doOverwrite) {
  setFieldValueFromLocalSettings(ref, ref, doOverwrite);
}

void setFieldValueFromLocalSettings(String ref) {
  setFieldValueFromLocalSettings(ref, false);
}

void setFieldValueFromLocalSettingsOnShow(String ref, boolean doOverwrite) {
  String cb = "setFieldValueFromLocalSettings(\"%s\", %s)";
  cb = replaceFirst(cb, ref);
  cb = replaceFirst(cb, doOverwrite + "");

  addOnEvent(ref, "show", cb);
}

void setFieldValueFromLocalSettingsOnShow(String ref) {
  boolean doOverwrite = false;
  setFieldValueFromLocalSettingsOnShow(ref, doOverwrite);
}

/* Causes the value of the field given by `ref` to be saved each time it is
 * modified (on blur). The value of the field is restored when the tab group
 * containing the field is displayed.
 *
 * This function depends on `addOnEvent`. Therefore this function must be called
 * after `addOnEvent` is defined, but before `bindOnEvents` is called. This will
 * be so if the call is made in the autogenerator's `logic` tags.
 */
void persistOverSessions(String ref) {
  setFieldValueFromLocalSettingsOnShow(ref);
  insertIntoLocalSettingsOnChange     (ref);
}

/*************************** FIELD COPYING HELPERS ****************************/
/* Provides an easy way to copy field values, even between vocabs.            */
/******************************************************************************/
void copyFieldValue(String src, String dst) {
  Boolean doFindVocabId = true;
  copyFieldValue(src, dst, doFindVocabId);
}

/* `src`           The ref of the source field.
 * `dst`           The ref of the destination field.
 * `doFindVocabId` If this is true, and the properties/attributes of `src` and
 *                 `dst` are different, `copyFieldValue` treats `src` and `dst`
 *                 as if they were menus. Therefore, to copy the value seen by
 *                 the user (i.e. the vocabName of `src`), a database query is
 *                 performed. The query determines the which vocabId of `dst`
 *                 will make it display the same vocabName as `src`.
 *
 *                 If `doFindVocabId` is false, the value returned by
 *                 `getFieldValue` is copied, without any database accesses.
 */
void copyFieldValue(String src, String dst, Boolean doFindVocabId) {
  String vocabIdSrc   = getFieldValue(src);
  String vocabNameSrc = getFieldValue(src, true);

  String attrNameSrc = getAttributeName(src);
  String attrNameDst = getAttributeName(dst);

  if (attrNameSrc.equals(attrNameDst) || !doFindVocabId) {
    setFieldValue(dst, vocabIdSrc);
    return;
  }

  String q = "";
  q += "    SELECT vocabid";
  q += "      FROM vocabulary";
  q += " LEFT JOIN attributekey";
  q += "     USING (attributeid)";
  q += "     WHERE attributename = '{attrNameDst}'";
  q += "       AND vocabname     = '{vocabNameSrc}'";
  q  = replaceFirst(q, "{attrNameDst}",  attrNameDst);
  q  = replaceFirst(q, "{vocabNameSrc}", vocabNameSrc);


  FetchCallback populate = new FetchCallback() {
    onFetch(result) {
      if (result == null) {
        // Fall back to dumb field copying
        copyFieldValue(src, dst, false);
      }

      String vocabIdDst = result.get(0);
      setFieldValue(dst, vocabIdDst);
    }
  };

  fetchOne(q, populate);
}

void inheritFieldValue(String src, String dst, boolean doFindVocabId) {
  String fun = "";
  fun = "copyFieldValue(\"{src}\", \"{dst}\", false)";
  fun = replaceFirst(fun, "{src}", src);
  fun = replaceFirst(fun, "{dst}", dst);

  addOnEvent(getTabGroupRef(dst), "create", fun);
}

void inheritFieldValue(String src, String dst) {
  inheritFieldValue(src, dst, false);
}

newTab(String tab, Boolean resolveTabGroups) {
  if (!resolveTabGroups) {
    return newTab(tab);
  }

  tab = tab.replaceAll("/$", "");
  tab = tab.replaceAll("^/", "");

  path = tab.split("/");
  switch (path.length) {
    case 0:
      break;
    case 1:
      newTabGroup(path[0]);
      break;
    case 2:
      String tabgroupString = path[0];
      String tabString      = path[0] + "/" + path[1];

      redirectTab = tabString;
      String onShowTabgroup = "if (!isNull(redirectTab)) { newTab(redirectTab); redirectTab = \"\"; }";
      addOnEvent(tabgroupString, "show", onShowTabgroup);

      newTabGroup(tabgroupString);
      newTab(tabString);
      break;
    default:
  }
}

/******************************************************************************/
/*                           DOCUMENT OBJECT MODEL                            */
/******************************************************************************/
String PREVIOUSLY_DISPLAYED_TAB_GROUP = "";
String CURRENTLY_DISPLAYED_TAB_GROUP  = "";

List getTabGroups() {
  List tabGroups = new ArrayList();
</xsl:text>
  <xsl:for-each select="/module/*[
    not(name() = 'logic') and
    not(name() = 'rels') and
    not(ancestor-or-self::*[contains(@f, 'noui')])
    ]">
    <xsl:text>  tabGroups.add("</xsl:text>
    <xsl:value-of select="name()" />
    <xsl:text>");</xsl:text>
    <xsl:value-of select="$newline" />
  </xsl:for-each>
  <xsl:text>
  return tabGroups;
}

void updateDisplayedTabGroup(String tabGroup) {
  PREVIOUSLY_DISPLAYED_TAB_GROUP = CURRENTLY_DISPLAYED_TAB_GROUP;
  CURRENTLY_DISPLAYED_TAB_GROUP  = tabGroup;
}

String getPreviousTabGroup() {
  return getPreviouslyDisplayedTabGroup();
}

String getPreviouslyDisplayedTabGroup() {
  return PREVIOUSLY_DISPLAYED_TAB_GROUP;
}

String getDisplayedTabGroup() {
  return CURRENTLY_DISPLAYED_TAB_GROUP;
}

boolean isDisplayed(String ref) {
  return getDisplayedTabGroup().equals(ref);
}

String getTabGroupRef(String fullRef) {
  Boolean lastPartOnly = false;
  return getTabGroupRef(fullRef, lastPartOnly);
}

String getTabGroupRef(String fullRef, Boolean lastPartOnly) {
  if (isNull(fullRef)) {
    return null;
  }

  String[] parts = fullRef.split("/");

  if (parts.length &lt; 1) return null;
  return parts[0];
}

String getTabRef(String fullRef) {
  Boolean lastPartOnly = false;
  return getTabRef(fullRef, lastPartOnly);
}

String getTabRef(String fullRef, Boolean lastPartOnly) {
  if (isNull(fullRef)) {
    return null;
  }

  String[] parts = fullRef.split("/");

  if (parts.length &lt; 2) return null;
  if (lastPartOnly) return                  parts[1];
  else              return parts[0] + "/" + parts[1];
}

String getLastRefPart(String fullRef) {
  if (isNull(fullRef)) {
    return null;
  }

  String[] parts = fullRef.split("/");
  return parts[parts.length-1];
}

String getGuiElementRef(String fullRef) {
  Boolean lastPartOnly = true;
  return getGuiElementRef(fullRef, lastPartOnly);
}

String getGuiElementRef(String fullRef, Boolean lastPartOnly) {
  if (isNull(fullRef)) {
    return null;
  }

  String[] parts = fullRef.split("/");

  if (parts.length &lt; 3) return null;
  if (lastPartOnly) return parts[2];
  else              return fullRef;
}

String getArch16nKey(String ref) {
  String lastRefPart = getLastRefPart(ref);

  if (isNull(lastRefPart)) return null;
  else                     return "{" + lastRefPart + "}";
}

String guessArch16nVal(String ref) {
  String arch16nKey = getArch16nKey(ref);

  if (isNull(arch16nKey)) return "";
  arch16nKey = arch16nKey.replaceAll("_", " ");
  arch16nKey = arch16nKey.replaceAll("^\\{", "");
  arch16nKey = arch16nKey.replaceAll("\\}$", "");
  return arch16nKey;
}

String getAttributeName(String ref) {
  String guiElementRef = getGuiElementRef(ref);
  if (isNull(guiElementRef)) {
    return null;
  }

  String attributeName = guiElementRef.replaceAll("_", " ");
  return attributeName;
}

String getArchEntType(String ref) {
  String tabGroupRef = getTabGroupRef(ref);
  if (isNull(tabGroupRef)) {
    return null;
  }

  String archEntType = tabGroupRef.replaceAll("_", " ");
  return archEntType;
}

String getArchEntTypePascalCased(String ref) {
  String archEntType = getArchEntType(ref);
  if (archEntType == null) {
    return archEntType;
  }

  return archEntType.replaceAll(" ", "");
}

/******************************************************************************/
/*                            BINDING ACCUMULATOR                             */
/*                                                                            */
/* The binding accumulator allows onEvent bindings for the same element to    */
/* accumulate over multiple onEvent calls instead of having later calls       */
/* override earlier ones.                                                     */
/*                                                                            */
/* It also adds support for a several additional events:                      */
/*   - "blur" --- This is merely an interface to make code for adding "blur"  */
/*         events more consistent.                                            */
/*   - "copy" --- Triggered as a record is duplicated, immediately before it  */
/*         is first saved.                                                    */
/*   - "create" --- Triggered after a record is first created.                */
/*   - "delete" --- Triggered after a record is deleted.                      */
/*   - "fetch" --- Triggered after a record is fetched and displayed in a     */
/*         given tab group.                                                   */
/*   - "focus" --- This is merely an interface to make code for adding        */
/*         "focus" events more consistent.                                    */
/*   - "leave" --- Triggered after a given tab group is navigated away        */
/*         from. Note that this event cannot be triggered when the FAIMS app  */
/*         is exited.                                                         */
/*   - "save" --- Triggered each time a tab group is saved. This includes the */
/*         first time the tab group is saved as well as subsequent            */
/*         onSave(String, Boolean) calls.                                     */
/*                                                                            */
/* A single call to `bindOnEvents` must occur after all the `addOnEvent` and  */
/* `delOnEvents` calls. Calling `bindOnEvents` is what actually establishes   */
/* the bindings once they have been added to the accumulator.                 */
/******************************************************************************/
String SEP = Character.toString ((char) 0); // Beanshell won't let me write "\0"
Map    EVENTS        = new HashMap(); // (ref, event type) -> callback statement
Set    CUSTOM_EVENTS = new HashSet(); // Events not handled by `onEvent`
CUSTOM_EVENTS.add("blur");
CUSTOM_EVENTS.add("copy");
CUSTOM_EVENTS.add("create");
CUSTOM_EVENTS.add("delete");
CUSTOM_EVENTS.add("fetch");
CUSTOM_EVENTS.add("focus");
CUSTOM_EVENTS.add("leave");
CUSTOM_EVENTS.add("save");

String getKey(String ref, String event) {
  return ref + SEP + event;
}

/* Returns the set of statements bound to an element at `ref` and occuring on
 * `event`.
 */
ArrayList getStatements(String ref, String event) {
  String    key = getKey(ref, event);
  ArrayList val = (ArrayList) EVENTS.get(key);

  if (val == null) return new ArrayList();
  else             return val;
}

void addStatement(String ref, String event, String statement) {
  // In the case that a statement already exists for a given (`ref`, `event`)
  // pair, writing `val.add(statement);` will be enough to add the extra
  // statement. This is because `getStatements` returns a reference to a list.
  // In the case just described, the list is stored in the `EVENTS` map.
  // However, sometimes `getStatements` returns empty lists which are not stored
  // in that map. In this case, calling `EVENTS.put` is required.

  String    key = getKey(ref, event);
  ArrayList val = getStatements(ref, event);
  val.add(statement);
  EVENTS.put(key, val);
}

String getStatementsString(String ref, String event) {
  ArrayList stmts = getStatements(ref, event);
  String stmtsStr = "";
  for (String s : stmts) {
    stmtsStr += s;
    stmtsStr += "; ";
  }
  return stmtsStr;
}

void delOnEvent(String ref, String event, String statement) {
  while(getStatements(ref, event).remove(statement));
}

void addOnEvent(String ref, String event, String statement) {
  // Calling `delOnEvent()` first ensures statement occurs once in the list, at
  // the end.
  delOnEvent  (ref, event, statement);
  addStatement(ref, event, statement);
}

void bindOnEvent(String ref, String event) {
  String stmtsStr     = getStatementsString(ref, event);
  String focusStmtStr = getStatementsString(ref, "focus");
  String blurStmtStr  = getStatementsString(ref, "blur" );

  if (!CUSTOM_EVENTS.contains(event)) {
    onEvent(ref, event, stmtsStr);
  } else if (event.equals("focus")) {
    onFocus(ref, focusStmtStr, blurStmtStr);
  } else if (event.equals("blur" )) {
    onFocus(ref, focusStmtStr, blurStmtStr);
  } else {
    ; // Other events are implemented using auto-generated callback functions
  }
}

void bindOnEvents() {
  for (String key : EVENTS.keySet()) {
    refevent = key.split(SEP);
    ref   = refevent[0];
    event = refevent[1];
    bindOnEvent(ref, event);
  }
}

void onLeaveTabGroup() {
  onLeaveTabGroup(getPreviouslyDisplayedTabGroup());
}

/* Execute the "leave" event for the tab group at `ref` if a callback for it
 * exists.
 */
void onLeaveTabGroup(String ref) {
  String event    = "leave";
  String stmtsStr = getStatementsString(ref, event);
  execute(stmtsStr);
}

/* Establishes `onEvent` bindings necessary to make the "leave" event work. The
 * "leave" event is really triggered upon "show" of another tab.
 */
for (tg : getTabGroups()) {
  String ref      = tg;
  String event    = "show";
  String callback;

  // Update (previously) displayed tab group
  callback = "updateDisplayedTabGroup(\"%s\")";
  callback = replaceFirst(callback, tg);
  addOnEvent(tg, event, callback);

  // Trigger on leave tab group event
  callback = "onLeaveTabGroup()";
  addOnEvent(tg, event, callback);
}

/******************************************************************************/
/*                           DROPDOWN VALUE GETTER                            */
/*                                                                            */
/* For consistency with `getListItemValue()`.                                 */
/******************************************************************************/
String DROPDOWN_ITEM_VALUE = null;

String getDropdownItemValue() {
  return DROPDOWN_ITEM_VALUE;
}

</xsl:text>
    <xsl:for-each select="//*[
        (
          normalize-space(@t) = 'dropdown' or
          not(@t) and
          ./opts  and not(.//@p)
        ) and
        not(ancestor-or-self::*[contains(@f, 'noui')])
      ]">
      <xsl:text>addOnEvent("</xsl:text>
      <xsl:call-template name="ref" />
      <xsl:text>", "click", "DROPDOWN_ITEM_VALUE = getFieldValue(\"</xsl:text>
      <xsl:call-template name="ref" />
      <xsl:text>\")");</xsl:text>
      <xsl:value-of select="$newline" />
    </xsl:for-each>
<xsl:text>
/******************************************************************************/
/*                             MENU VALUE GETTER                              */
/*                                                                            */
/* Provides simple ways of getting a menu's vocabname as opposed to the       */
/* default, which is the vocabid.                                             */
/******************************************************************************/
// Map from vocabid to vocabname. Populated by `fetchMenuValues()`.
Map MENU_VALUES = null;

/*
 * Initialises `MENU_VALUES` with the (vocabid -> vocabname) mapping of every
 * menu.
 */
void fetchMenuValues() {
  MENU_VALUES = new HashMap();

  String q = "";
  q += " SELECT vocabid, vocabname";
  q += " FROM   vocabulary";

  populateHashMap = new FetchCallback() {
    onFetch(result) {
      for (row : result) {
        vocabId   = row.get(0);
        vocabName = row.get(1);
        MENU_VALUES.put(vocabId, vocabName);
      }
    }
  };

  fetchAll(q, populateHashMap);
}

fetchMenuValues();

/* Returns a menu's vocabname, instead of the (counter-intuitive) vocabid.
 */
String getFieldValue(String ref, Boolean doConvertVocabIds) {
  if (!doConvertVocabIds) {
    return getFieldValue(ref);
  }

  String val       = getFieldValue(ref);
  String vocabName = MENU_VALUES.get(val);

  if (val       == null) return "";
  if (vocabName == null) return "";
  return vocabName;
}

/* Shorthand for writing getFieldValue(ref, true). This function's use is
 * discouraged in favour of writing `getFieldValue(ref, true)`.
 */
String getMenuValue(String ref) {
  return getFieldValue(ref, true);
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
</xsl:text>
<xsl:call-template name="gps-diag-update" />
<xsl:text>
void updateGPSDiagnostics() {
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
      if (previousStatus.length()    &gt;= error.length() &amp;&amp;
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
/** Fetches the contents of a specifed vocabulary and stores it in the given list. **/
void fetchVocab(String vocabName, List storageList) {
  fetchVocab(vocabName, storageList, null);
}
void fetchVocab(String vocabName, List storageList, String callbackFunction) {
  fetchAll("select vocabid, vocabname from vocabulary left join attributekey using (attributeid) where attributename = '" + vocabName + "';", new FetchCallback() {
    onFetch(result) {
      storageList.addAll(result);
      Log.d("fetchVocab()", "Fetched vocabulary \"" + vocabname + "\" contents: " + result.toString());
      if (callbackFunction != null &amp;&amp; !isNull(callbackFunction)) {
        execute(callbackFunction);
      }
    }
  });
}

/** Wrapper for to make a vocab without an exlusion list **/
void makeVocab(String type, String path, String attrib) {
  makeVocab(type, path, attrib, null);
}

/** Vocab Population **/
/* Populates the path specified vocabulary from the database based on the given attribute name, where type 
is the type of the vocab to populate (PictureGallery, HierarchicalPictureGallery, CheckBoxGroup, DropDown, HierarchicalDropDown, RadioGroup or List). */
void makeVocab(String type, String path, String attrib, List vocabExclusions) {
    makeVocab(type, path, attrib, vocabExclusions, null);
}

/* Populates the path specified vocabulary from the database based on the given attribute name, where type 
is the type of the vocab to populate (PictureGallery, HierarchicalPictureGallery, CheckBoxGroup, DropDown, HierarchicalDropDown, RadioGroup or List). */
void makeVocab(String type, String path, String attrib, List vocabExclusions, String callbackFunction){
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
        Boolean hasNull =
                vocabExclusions == null
            || !vocabExclusions.contains("")
            &amp;&amp; !vocabExclusions.contains(null);
        // print("makeVocab() filtered result: " + result);
        if(type.equals("CheckBoxGroup")) {
          populateCheckBoxGroup(path, result);
        } else if(type.equals("DropDown")) {
          // populateDropDown(path, result);
          populateDropDown(path, result, hasNull);
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
    <xsl:for-each select="//*[(@t or ./opts) and not(ancestor-or-self::*[contains(@f, 'nodata') or contains(@f, 'noui')]) and not(contains(@f, 'user')) and not(@e) and not(@ec)]">
      <xsl:variable name="is-hierarchical">
        <xsl:call-template name="is-hierarchical"/>
      </xsl:variable>
      <xsl:choose>
        <xsl:when test="normalize-space(@t) = 'checkbox'">
          <xsl:text>makeVocab("CheckBoxGroup", "</xsl:text>
          <xsl:call-template name="complete-makevocab" />
        </xsl:when>
        <xsl:when test="normalize-space(@t) = 'dropdown' or
          (not(@t) and ./opts and not(.//@p))">
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
        <xsl:when test="normalize-space(@t) = 'picture' or
          (not(@t) and .//@p)">
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
List fieldPair(String ref, String name, String cond) {
  List fp = new ArrayList();
  fp.add(ref);
  fp.add(name);
  fp.add(cond);
  return fp;
}

List fieldPair(String ref, String name) {
  String t = "true";
  return fieldPair(ref, name, t);
}

/* Returns true if field specified by `ref` is valid. False otherwise.
 */
boolean isValidField(String ref) {
  return !isNull(getFieldValue(ref));
}
/* `format` can either be HTML or PLAINTEXT
 */
String validateFields(List fields, String format) {
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
      <xsl:text>void validate</xsl:text>
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
      <xsl:value-of select="$newline" />
      <xsl:value-of select="$newline" />
    </xsl:for-each>

    <xsl:value-of select="$newline" />

    <!-- Autosaving -->
<xsl:text>
/******************************************************************************/
/*                                 AUTOSAVING                                 */
/******************************************************************************/
Map tabgroupToUuid = Collections.synchronizedMap(new HashMap());

String getUuid(String tabgroup) {
  return tabgroupToUuid.get(tabgroup);
}

void setUuid(String tabgroup, String uuid) {
  tabgroupToUuid.put(tabgroup, uuid);
}

void saveTabGroup(String tabgroup) {
  saveTabGroup(tabgroup, "");
}

void saveTabGroup(String tabgroup, String callback) {
  Boolean enableAutosave      = true;
  String  id                  = getUuid(tabgroup);
  List    geometry            = null;
  List    attributes          = null;
  String  parentTabgroup_     = parentTabgroup;
  String  parentTabgroupUuid_ = getUuid(parentTabgroup_);
  Boolean userWasSet          = !username.equals("");

  callback += "; onSave" + getArchEntTypePascalCased(tabgroup) + "__()";

  parentTabgroup = null;

  SaveCallback saveCallback  = new SaveCallback() {
    onSave(uuid, newRecord) {
      setUuid(tabgroup, uuid);
      // Make a child-parent relationship if need be.
      if (
          newRecord &amp;&amp;
          !isNull(parentTabgroup_) &amp;&amp;
          !isNull(parentTabgroupUuid_)
      ) {
        String rel = "";
        rel += parentTabgroup_.replaceAll("_", " ");
        rel += " - ";
        rel += tabgroup.replaceAll("_", " ");
        saveEntitiesToHierRel(
          rel,
          parentTabgroupUuid_,
          uuid,
          "Parent Of",
          "Child Of",
          callback
        );
      } else {
        execute(callback);
      }

      // This fixes an interesting bug. Without this, if a user was not set
      // (by calling `setUser`) at the time `saveTabGroup` was first called, but
      // set by the time `onSave` was called, the tab group is saved correctly
      // the first time only.
      //
      // Adding this allows subsequent saves to succeed. Presumably it plays
      // some role in helping FAIMS associate the correct user with a record.
      if (!userWasSet) {
        saveTabGroup(tabgroup, callback);
      }

    }
    onError(message) {
      showToast(message);
    }
  };

  saveTabGroup(tabgroup, id, geometry, attributes, saveCallback, enableAutosave);
}

void setToTimestampNow(String ref) {
  String now = getTimestampNow();
  setFieldValue(ref, now);
}

String getTimestampNow() {
  String fmt = "yyyy-MM-dd HH:mm:ssZ";
  return getTimestampNow(fmt);
}

String getTimestampNow(String fmt) {
  date    = new Date();
  dateFmt = new java.text.SimpleDateFormat(fmt);
  dateStr = dateFmt.format(date);

  // Insert colon into timezone (e.g. +1000 -> +10:00)
  String left; String right;

  left    = dateStr.substring(0, dateStr.length() - 2);
  right   = dateStr.substring(   dateStr.length() - 2);
  dateStr = left + ":" + right;

  return dateStr;
}

void populateAuthorAndTimestamp(String tabgroup) {
  Map tabgroupToAuthor    = new HashMap();
  Map tabgroupToTimestamp = new HashMap();
</xsl:text>
    <xsl:call-template name="populate-author" />
    <xsl:call-template name="populate-timestamp" />
<xsl:text>
  String authorPath    = tabgroupToAuthor.get(tabgroup);
  String timestampPath = tabgroupToTimestamp.get(tabgroup);

  String authorVal    = username;
  String timestampVal = getTimestampNow();

  if (!isNull(authorPath))    setFieldValue(authorPath,    authorVal);
  if (!isNull(timestampPath)) setFieldValue(timestampPath, timestampVal);
}

</xsl:text>
    <xsl:for-each select="/module/*[
      not(name() = 'logic') and
      not(name() = 'rels') and
      not(ancestor-or-self::*[contains(@f, 'nodata') or contains(@f, 'noui')])
      ]">
      <xsl:variable name="camelcase-tabgroup">
        <xsl:call-template name="string-replace-all">
          <xsl:with-param name="text" select="name()" />
          <xsl:with-param name="replace" select="'_'" />
          <xsl:with-param name="by" select="''" />
        </xsl:call-template>
      </xsl:variable>
      <xsl:text>void onShow</xsl:text>
      <xsl:value-of select="$camelcase-tabgroup"/>
<xsl:text> () {
  // TODO: Add some things which should happen when this tabgroup is shown
  saveTabGroup("</xsl:text>
      <xsl:value-of select="name()" />
      <xsl:text>");</xsl:text>
      <xsl:value-of select="$newline" />
      <xsl:text>}</xsl:text>
      <xsl:value-of select="$newline" />
    </xsl:for-each>
    <xsl:value-of select="$newline" />
    <xsl:for-each select="/module/*[
      not(name() = 'logic') and
      not(name() = 'rels') and
      not(ancestor-or-self::*[contains(@f, 'nodata') or contains(@f, 'noui')])
      ]">
      <xsl:text>addOnEvent("</xsl:text>
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

    <!-- Generate some errors if need be -->
    <xsl:for-each select="//*[@l and @lc]">
      <xsl:text>// ERROR: "l" and "lc" tags cannot be present simultaneously; found on "</xsl:text>
      <xsl:call-template name="ref" />
      <xsl:text>"</xsl:text>
      <xsl:value-of select="$newline" />
    </xsl:for-each>
    <!-- Triggers/buttons which link to a tab or tabgroup -->
    <xsl:for-each select="//*[@l]">
      <xsl:text>void onClick</xsl:text>
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
            (contains(@f, 'noui') or
             contains(@f, 'nodata'))
          ])">
          <xsl:text>  parentTabgroup__ = "</xsl:text>
          <xsl:value-of select="name(ancestor::*[last()-1])"/>
          <xsl:text>";</xsl:text>
          <xsl:value-of select="$newline" />
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
          <xsl:call-template name="string-replace-all">
            <xsl:with-param name="text" select="@l" />
            <xsl:with-param name="replace" select="'/search'" />
            <xsl:with-param name="by" select="'/Search'" />
          </xsl:call-template>
          <xsl:text>", true);</xsl:text>
        </xsl:otherwise>
      </xsl:choose>
      <xsl:value-of select="$newline" />
      <xsl:text>}</xsl:text>
      <xsl:value-of select="$newline" />
    </xsl:for-each>
    <xsl:for-each select="//*[@lc]">
      <xsl:text>void onClick</xsl:text>
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
      <xsl:variable name="link" select="@lc"/>
      <xsl:choose>
        <xsl:when test="
          not(contains($link, '/')) and
          not(/module/*[name() = $link and
            (contains(@f, 'noui') or
             contains(@f, 'nodata'))
          ])">
          <xsl:text>  String tabgroup = "</xsl:text>
          <xsl:value-of select="name(ancestor::*[last()-1])"/>
          <xsl:text>";</xsl:text>
          <xsl:value-of select="$newline" />
          <xsl:text>  if (isNull(getUuid(tabgroup))){</xsl:text>
          <xsl:value-of select="$newline" />
          <xsl:text>    showToast("{You_must_save_this_tabgroup_first}");</xsl:text>
          <xsl:value-of select="$newline" />
          <xsl:text>    return;</xsl:text>
          <xsl:value-of select="$newline" />
          <xsl:text>  }</xsl:text>
          <xsl:value-of select="$newline" />
          <xsl:text>  parentTabgroup   = tabgroup;</xsl:text>
          <xsl:value-of select="$newline" />
          <xsl:text>  parentTabgroup__ = tabgroup;</xsl:text>
          <xsl:value-of select="$newline" />
          <xsl:text>  new</xsl:text>
          <xsl:call-template name="string-replace-all">
            <xsl:with-param name="text" select="$link" />
            <xsl:with-param name="replace" select="'_'" />
            <xsl:with-param name="by" select="''" />
          </xsl:call-template>
          <xsl:text>();</xsl:text>
        </xsl:when>
        <xsl:otherwise>
          <xsl:text>  // ERROR: "lc" attribute cannot belong to element flagged with "noui" or "nodata"</xsl:text>
          <xsl:value-of select="$newline" />
        </xsl:otherwise>
      </xsl:choose>
      <xsl:value-of select="$newline" />
      <xsl:text>}</xsl:text>
      <xsl:value-of select="$newline" />
    </xsl:for-each>
    <xsl:value-of select="$newline" />

    <xsl:for-each select="//*[@l or @lc]">
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

      <xsl:text>addOnEvent("</xsl:text>
      <xsl:value-of select="$button-path"/>
      <xsl:text>", "click", </xsl:text>
      <xsl:value-of select="$show-tab-string"/>
      <xsl:text>);</xsl:text>
      <xsl:value-of select="$newline" />
    </xsl:for-each>
    <xsl:value-of select="$newline" />

    <!-- addOnEvent calls for audio, camera, file and video GUI elements -->
    <xsl:if test="//*[
      normalize-space(@t) = 'audio' or
      normalize-space(@t) = 'camera' or
      normalize-space(@t) = 'file' or
      normalize-space(@t) = 'video'
      ]">
<xsl:text>
/******************************************************************************/
/*                   AUDIO, CAMERA, FILE AND VIDEO BINDINGS                   */
/******************************************************************************/
</xsl:text>
    </xsl:if>
    <xsl:for-each select="//*[normalize-space(@t) = 'audio']">
      <xsl:text>addOnEvent("</xsl:text>
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
      <xsl:text>addOnEvent("</xsl:text>
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
      <xsl:text>addOnEvent("</xsl:text>
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
      <xsl:text>addOnEvent("</xsl:text>
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
    <xsl:if test="//*[normalize-space(@t) = 'viewfiles']">
<xsl:text>
/******************************************************************************/
/*                 BINDINGS FOR 'VIEW ATTACHED FILES' BUTTONS                 */
/******************************************************************************/
</xsl:text>
    </xsl:if>
    <xsl:for-each select="//*[normalize-space(@t) = 'viewfiles']">
      <xsl:text>addOnEvent("</xsl:text>
      <xsl:value-of select="name(ancestor::*[last()-1])"/>
      <xsl:text>/</xsl:text>
      <xsl:value-of select="name(ancestor::*[last()-2])"/>
      <xsl:text>/</xsl:text>
      <xsl:value-of select="name()"/>
      <xsl:text>", "click", "viewArchEntAttachedFiles(getUuid(\"</xsl:text>
      <xsl:value-of select="name(ancestor::*[last()-1])"/>
      <xsl:text>\"))");</xsl:text>
      <xsl:value-of select="$newline" />
    </xsl:for-each>

    <!-- Navigation Drawer -->
<xsl:text>
/******************************************************************************/
/*                             NAVIGATION DRAWER                              */
/******************************************************************************/
void removeNavigationButtons() {
  removeNavigationButton("new");
  removeNavigationButton("duplicate");
  removeNavigationButton("delete");
  removeNavigationButton("validate");
}

void addNavigationButtons(String tabgroup) {
  removeNavigationButtons();
  List tabgroupsToValidate = new ArrayList();
</xsl:text>
    <xsl:call-template name="tabgroups-to-validate"/>
    <xsl:text>
  addNavigationButton("new", new ActionButtonCallback() {
    actionOnLabel() {
      "{New}";
    }
    actionOn() {
      if(isNull(getUuid(tabgroup))) {
          newRecord(tabgroup, true);
          showToast("{New_record_created}");
      } else {
          showAlert("{Warning}", "{Any_unsaved_changes_will_be_lost}", "newRecord(\""+tabgroup+"\", true)", "");
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
  if (tabgroupsToValidate.contains(tabgroup)) {
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
}

/******************************************************************************/
/*        ENTITY AND RELATIONSHIP SAVING AND LOADING HELPER FUNCTIONS         */
/******************************************************************************/
/** Saves two entity id's as a relation. **/
void saveEntitiesToRel(String type, String entity1, String entity2) {
  String callback = null;
  saveEntitiesToRel(type, entity1, entity2, callback);
}

/** Saves two entity id's as a relation with some callback executed. **/
void saveEntitiesToRel(String type, String entity1, String entity2, String callback) {
  String e1verb = null;
  String e2verb = null;
  saveEntitiesToHierRel(type, entity1, entity2, e1verb, e2verb, callback);
}

/** Saves two entity id's as a hierachical relation with some callback executed. **/
void saveEntitiesToHierRel(String type, String entity1, String entity2, String e1verb, String e2verb, String callback) {
  if (isNull(entity1) || isNull(entity2)) return;
  saveRel(null, type, null, null, new SaveCallback() {
    onSave(rel_id, newRecord) {
      addReln(entity1, rel_id, e1verb);
      addReln(entity2, rel_id, e2verb);
      if(!isNull(callback)) {
         execute(callback);
      }
    }
    onError(message) {
      Log.e("saveEntitiesToHierRel", message);
      showToast(message);
    }
  });
}

// Makes a new record of the given tabgroup
void newRecord(String tabgroup) {
  boolean doUpdateRelVars = false;
  newRecord(tabgroup, doUpdateRelVars);
}

void newRecord(String tabgroup, boolean doUpdateRelVars) {
  if (doUpdateRelVars) {
    String uuidOld = getUuid(getDisplayedTabGroup());
    String q       = getDuplicateRelnQuery(uuidOld); // We're not duplicating
                                                     // anything, just getting
                                                     // the parent's UUID.

    cancelTabGroup(tabgroup, false);

    FetchCallback updateRelVars = new FetchCallback() {
      onFetch(result) {
        if (result != null &amp;&amp; result.size() &gt;= 1) {
          parentTabgroup   = result.get(0).get(4);
          parentTabgroup   = parentTabgroup.replaceAll(" ", "_");
          parentTabgroup__ = parentTabgroup;
        }

        newRecord(tabgroup, false);
      }
    };
    fetchAll(q, updateRelVars);
    return;
  }

  String newTabGroupFunction = "new" + tabgroup.replaceAll("_", "") + "()"; // Typical value: "newTabgroup()"
  eval(newTabGroupFunction);

  Log.d("newRecord", tabgroup);
}

// Deletes the current record of the given tabgroup
void deleteRecord(String tabgroup) {
  String deleteTabGroupFunction = "delete" + tabgroup.replaceAll("_", "") + "()"; // Typical value: "deleteTabgroup()"
  eval(deleteTabGroupFunction);

  Log.d("deleteRecord", tabgroup);
}

// Duplicates the current record of the given tabgroup
void duplicateRecord(String tabgroup) {
  dialog = showBusy("Duplicating", "Please wait...");

  String duplicateTabGroupFunction = "duplicate" + tabgroup.replaceAll("_", "") + "()"; // Typical value: "duplicateTabgroup()"
  eval(duplicateTabGroupFunction);

  Log.d("duplicateRecord", tabgroup);
}

// generic fetch saved attributes query
String getDuplicateAttributeQuery(String originalRecordID, String attributesToDupe) {
  if (attributesToDupe.equals("")) {
    attributesToDupe = "''";
  }
  String duplicateQuery = "SELECT attributename, freetext, vocabid, measure, certainty " +
                          "  FROM latestnondeletedaentvalue JOIN attributekey USING (attributeid) " +
                          " WHERE attributename IN ('', "+attributesToDupe+") " +
                          "   AND uuid = '"+originalRecordID+"'; ";
  return duplicateQuery;
}

String getDuplicateRelnQuery(String originalRecordID) {
  String dupeRelnQuery = "SELECT relntypename, parentparticipatesverb, childparticipatesverb, parentuuid, parentaenttypename, childaenttypename"+
                         "  FROM parentchild join relationship using (relationshipid) "+
                         "  JOIN relntype using (relntypeid) "+
                         " WHERE childuuid = '"+originalRecordID+"' " +
                         "   AND parentparticipatesverb = 'Parent Of' ";
  return dupeRelnQuery;
}

void makeDuplicateRelationships(fetchedAttributes, String newUuid){
  Log.e("Module", "makeDuplicateRelationships");
  for (savedAttribute : fetchedAttributes){
    String relntypename           = savedAttribute.get(0);
    String parentparticipatesverb = savedAttribute.get(1);
    String childparticipatesverb  = savedAttribute.get(2);
    String parentUuid             = savedAttribute.get(3);
    String childArchEntType       = savedAttribute.get(5);

    String onSaveRel              = "onSave" + childArchEntType.replaceAll(" ", "") + "__()";

    saveEntitiesToHierRel(
        relntypename,
        parentUuid,
        newUuid,
        parentparticipatesverb,
        childparticipatesverb,
        onSaveRel
    );
  }
}

// generic get extra attributes
List getExtraAttributes(fetchedAttributes) {
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

void loadEntity() {
  loadEntity(false);
}
void loadEntity(Boolean isDropdown) {
  if (isDropdown) {
    loadEntityFrom(getDropdownItemValue());
  } else {
    loadEntityFrom(getListItemValue());
  }
}

void loadEntityFrom(String entityID) {
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
<xsl:for-each select="/module/*[
  not(name() = 'logic') and
  not(name() = 'rels') and
  not(ancestor-or-self::*[contains(@f, 'nodata') or contains(@f, 'noui')])
  ]">
      <xsl:call-template name="tabgroup-new" />
      <xsl:call-template name="tabgroup-oncreate" />
      <xsl:call-template name="tabgroup-onfetch" />
      <xsl:call-template name="tabgroup-onsave" />
      <xsl:call-template name="tabgroup-oncopy" />
      <xsl:call-template name="tabgroup-ondelete" />
      <xsl:call-template name="tabgroup-duplicate" />
      <xsl:call-template name="tabgroup-delete" />
      <xsl:call-template name="tabgroup-really-delete" />
    </xsl:for-each>
<xsl:text>
void doNotDelete(){
  showToast("{Delete_Cancelled}");
}
</xsl:text>
<xsl:for-each select="/module/*[
  ancestor-or-self::*[contains(@f, 'nodata') or contains(@f, 'noui')]
  ]">
      <xsl:text>addOnEvent("</xsl:text>
      <xsl:value-of select="name()"/>
      <xsl:text>", "show", "removeNavigationButtons()");</xsl:text>
      <xsl:value-of select="$newline"/>
    </xsl:for-each>
    <xsl:for-each select="/module/*[
      not(name() = 'logic') and
      not(name() = 'rels') and
      not(ancestor-or-self::*[contains(@f, 'nodata') or contains(@f, 'noui')])
      ]">
      <xsl:text>addOnEvent("</xsl:text>
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
addOnEvent("</xsl:text><xsl:value-of select="name(/module/*[./search])"/><xsl:text>/Search"               , "show"  , "search();");
addOnEvent("</xsl:text><xsl:value-of select="name(/module/*[./search])"/><xsl:text>/Search/Entity_List"   , "click" , "loadEntity();");
addOnEvent("</xsl:text><xsl:value-of select="name(/module/*[./search])"/><xsl:text>/Search/Search_Button" , "click" , "search()");
addOnEvent("</xsl:text><xsl:value-of select="name(/module/*[./search])"/><xsl:text>/Search/Search_Term"   , "click" , "clearSearch()");
</xsl:text>
      <xsl:call-template name="search-entities" />
      <xsl:text>
void clearSearch(){
  setFieldValue("</xsl:text><xsl:value-of select="name(/module/*[./search])"/><xsl:text>/Search/Search_Term","");
}

void search(){
  String tabgroup = "</xsl:text><xsl:value-of select="name(/module/*[./search])"/><xsl:text>";
  String refEntityList  = tabgroup + "/Search/Entity_List";
  String refSearchTerm  = tabgroup + "/Search/Search_Term";
  String refEntityTypes = tabgroup + "/Search/Entity_Types";

</xsl:text>
<xsl:if test="count(/module/*[not(contains(@f, 'nodata')) and not(name() = 'rels') and not(name() = 'logic') and (./*//*[not(ancestor-or-self::*[contains(@f, 'nodata') or contains(@f, 'user')]) and not(name() = 'cols') and not(name() = 'col') and not(name() = 'desc') and not(name() = 'opt') and not(name() = 'opts') and not(ancestor-or-self::rels) and not(normalize-space(@t) = 'group') and not(normalize-space(@t) = 'table') and not(normalize-space(@t) = 'gpsdiag') and not(normalize-space(@t) = 'map') and not(normalize-space(@t) = 'button')])]) &lt; 2">
  <xsl:text>  String type = "";</xsl:text>
</xsl:if>
<xsl:if test="count(/module/*[not(contains(@f, 'nodata')) and not(name() = 'rels') and not(name() = 'logic') and (./*//*[not(ancestor-or-self::*[contains(@f, 'nodata') or contains(@f, 'user')]) and not(name() = 'cols') and not(name() = 'col') and not(name() = 'desc') and not(name() = 'opt') and not(name() = 'opts') and not(ancestor-or-self::rels) and not(normalize-space(@t) = 'group') and not(normalize-space(@t) = 'table') and not(normalize-space(@t) = 'gpsdiag') and not(normalize-space(@t) = 'map') and not(normalize-space(@t) = 'button')])]) &gt;= 2">
  <xsl:text>  String type = getFieldValue(refEntityTypes);</xsl:text>
</xsl:if>
<xsl:text>
  String term = getFieldValue(refSearchTerm);
  String searchQuery = "SELECT uuid, response "+
                       "  FROM latestNonDeletedArchEntFormattedIdentifiers  "+
                       " WHERE uuid in (SELECT uuid "+
                       "                  FROM latestNonDeletedArchEntIdentifiers "+
                       "                 WHERE measure LIKE '"+term+"'||'%'  "+
                       "                   AND ( aenttypename LIKE '"+type+"' OR '' = '"+type+"' ) "+
                       "                )  "+
                       " ORDER BY response "+
                       " LIMIT ? "+
                       "OFFSET ? ";

  populateCursorList(refEntityList, searchQuery, 25);
  refreshTabgroupCSS(tabgroup);

  Log.d("Module", "Search query: " + searchQuery);
}
</xsl:text>
    </xsl:if>
    <xsl:if test="(/module/*/search) or (//@e) or (//@ec)">
      <xsl:value-of select="$newline"/>
      <xsl:call-template name="load-entity-functions" />
    </xsl:if>

    <!-- Take From GPS Button -->
      <xsl:text>
/******************************************************************************/
/*                          TAKE FROM GPS BUTTON(S)                           */
/******************************************************************************/
</xsl:text>
    <xsl:if test="/module/*/*/gps">
<xsl:call-template name="take-from-gps-bindings"/>
<xsl:text>
/* Takes the current point using gps. */
void takePoint(String tabgroup) {
</xsl:text>
    <xsl:call-template name="take-from-gps-mappings"/>
<xsl:text>
  String archEntType = tabgroup.replaceAll("_", " ");
  String currentUuid = getUuid(tabgroup);
  if (isNull(currentUuid)){
    showToast("Please enter data first and let a save occur.");
    return;
  }

  boolean isInternalGPSOff = !isInternalGPSOn();
  boolean isExternalGPSOff = !isExternalGPSOn();
  Object  position = getGPSPosition();
  if (position == null || isInternalGPSOff &amp;&amp; isExternalGPSOff) {
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

  String accuracy = "" + getGPSEstimatedAccuracy();
  setFieldValue(tabgroupToTabRef.get(tabgroup) + "Accuracy", accuracy);

  saveArchEnt(currentUuid, archEntType, geolist, null, new SaveCallback() {
    onSave(uuid, newRecord) {
      print("[takePoint()] Added geometry: " + geolist);
      fillInGPS(tabgroup);
    }
  });
}

/* Sets the value of GPS views for the given tab path. */
void fillInGPS(String tabgroup) {
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
      setFieldValue(tabgroupToTabRef.get(tabgroup) + "Longitude" , result.get(0));
      setFieldValue(tabgroupToTabRef.get(tabgroup) + "Latitude"  , result.get(1));
      setFieldValue(tabgroupToTabRef.get(tabgroup) + "Easting"   , result.get(2));
      setFieldValue(tabgroupToTabRef.get(tabgroup) + "Northing"  , result.get(3));
    }
  });
}
</xsl:text>
    </xsl:if>
<xsl:text>
void clearGpsInTabGroup(String tabgroup) {
</xsl:text>
    <xsl:call-template name="take-from-gps-mappings"/>
<xsl:text>

  String tabRef = tabgroupToTabRef.get(tabgroup);
  if (isNull(tabRef)) return;

  clearGpsInTab(tabRef);
}

void clearGpsInTab(String tabRef) {
  setFieldValue(tabRef + "Accuracy"  , "");
  setFieldValue(tabRef + "Latitude"  , "");
  setFieldValue(tabRef + "Longitude" , "");
  setFieldValue(tabRef + "Easting"   , "");
  setFieldValue(tabRef + "Northing"  , "");
}
</xsl:text>

    <xsl:if test="//*[contains(@f, 'autonum')] and not(//autonum)">
      <xsl:text>// ERROR: field(s) flagged with 'autonum' but no autonum tag exists</xsl:text>
    </xsl:if>
    <xsl:if test="//autonum">
<xsl:text>
/******************************************************************************/
/*                       AUTONUMBERING HELPER FUNCTIONS                       */
/******************************************************************************/
/*
 * If value of field specified by `ref` is null, sets the field to `defaultVal`,
 * otherwise increments its value.
 *
 * Returns the value the field was updated to.
 */
Integer incField(String ref, Integer defaultVal) {
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
Integer incField(String ref) {
  return incField(ref, 1);
}

List getStartingIdPaths() {
  List l = new ArrayList();
</xsl:text>
      <xsl:call-template name="control-starting-id-paths"/>
<xsl:text>
  return l;
}

void loadStartingId(String ref) {
  // If there's already a value in the field, we don't need to load one.
  String val = getFieldValue(ref);
  if (!isNull(val)) {
    return;
  }

  // Load a value into the field. Set it to 1 if no value has been previously
  // saved.
  String idQ = "SELECT value FROM localSettings WHERE key = '" + ref + "';";
  fetchOne(idQ, new FetchCallback() {
    onFetch(result) {
      if (isNull(result)) setFieldValue(ref, "1"          );
      else                setFieldValue(ref, result.get(0));
    }
  });
}

loadStartingIds() {
  List l = getStartingIdPaths();

  for (ref : l) {
    loadStartingId(ref);
  }
}

addOnEvent("</xsl:text><xsl:call-template name="autonum-parent"/><xsl:text>", "show", "loadStartingIds()");

/*
 * Sets bindings to save autonum'd fields whenever they're blurred.
 */
for (ref : getStartingIdPaths()) {
  onFocus(ref, null, "insertIntoLocalSettings(\"" + ref + "\", getFieldValue(\"" + ref + "\"));");
}

</xsl:text>
      <xsl:call-template name="incautonum"/>
    </xsl:if>

  <xsl:text>
/******************************************************************************/
/*                POPULATION OF ENTITY AND CHILD ENTITY LISTS                 */
/******************************************************************************/
/*
 * `viewType`   the type of GUI element to be populated. It can either equal
 *              "DropDown" or "List".
 * `path`       the reference of the GUI element to be populated.
 * `parentUuid` the parent in the relationship denoted by `relType`.
 * `entType`    the type of the entities the menu will be populated with.
 * `relType`    the name of the relationship the children are to be in with the
 *              entity denoted by `parentUuid`.
 */
void populateMenuWithEntities (
  String viewType,
  String path,
  String parentUuid,
  String entType,
  String relType
) {
  String getChildEntitiesQ = "" +
    "SELECT childuuid, response "+
    "  FROM parentchild JOIN latestNonDeletedArchEntFormattedIdentifiers ON (childuuid = uuid) " +
    "  JOIN createdmodifiedatby USING (uuid) " +
    " WHERE relationshipid IN (SELECT relationshipid  " +
    "                            FROM latestnondeletedrelationship JOIN relntype USING (relntypeid) " +
    "                           WHERE relntypename = '"+relType+"') " +
    "   AND parentuuid = " + parentUuid + " " +
    "   AND (childaenttypename = '"+entType+"' OR '"+entType+"' = '') " +
    " ORDER BY createdat DESC ";

  String getEntitiesQ = "" +
    "SELECT uuid, response "+
    "  FROM latestNonDeletedArchEntFormattedIdentifiers  "+
    " WHERE uuid in (SELECT uuid "+
    "                  FROM latestNonDeletedArchEntIdentifiers "+
    "                 WHERE aenttypename = '"+entType+"' OR '"+entType+"' = '' " +
    "               )  "+
    " ORDER BY response ";

  String q = null;
  if (relType.equals("")) {
    q = getEntitiesQ;
  } else {
    q = getChildEntitiesQ;
  }

  FetchCallback cbPopulateDropDown = new FetchCallback() {
    onFetch(result) {
      populateDropDown(path, result, true);
    }
  };

  switch (viewType) {
    case "DropDown":
      fetchAll(q, cbPopulateDropDown);
      break;
    case "List":
      q += " LIMIT ? OFFSET ? ";
      populateCursorList(path, q, 25);
      break;
    default:
      Log.e("populateMenuWithEntities ", "Unexpected type '" + viewType + "'");
  }
}

void populateEntityListsInTabGroup(String tabGroup) {
  if (isNull(tabGroup)) {
    return;
  }

  for (m : ENTITY_MENUS) {
    String path         = m[1];
    String menuTabGroup = getTabGroupRef(path);
    String functionCall = getEntityMenuPopulationFunction(m);

    if (menuTabGroup.equals(tabGroup))
      execute(functionCall);
  }
}

/* Populates each list containing records whose archent type is the same as that
 * of `tabGroup`.
 */
void populateEntityListsOfArchEnt(String tabGroup) {
  if (isNull(tabGroup)) {
    return;
  }

  String archEntTypeToPopulate = getArchEntType(tabGroup);

  for (m : ENTITY_MENUS) {
    String archEntType  = m[3];
    String functionCall = getEntityMenuPopulationFunction(m);

    if (archEntType.equals(archEntTypeToPopulate))
      execute(functionCall);
  }
}

String getEntityMenuPopulationFunction(String[] menuDescriptor) {
  String viewType       = menuDescriptor[0];
  String path           = menuDescriptor[1];
  String parentUuidCall = menuDescriptor[2];
  String entType        = menuDescriptor[3];
  String relType        = menuDescriptor[4];

  String functionCall = "";
  functionCall += "populateMenuWithEntities(";
  functionCall += "\"" + viewType       + "\"";
  functionCall += ", ";
  functionCall += "\"" + path           + "\"";
  functionCall += ", ";
  functionCall +=        parentUuidCall       ;
  functionCall += ", ";
  functionCall += "\"" + entType        + "\"";
  functionCall += ", ";
  functionCall += "\"" + relType        + "\"";
  functionCall += ")";

  return functionCall;
}

ENTITY_MENUS = new ArrayList();
</xsl:text>
      <xsl:call-template name="entity-menu" />
      <xsl:call-template name="entity-child-menu" />
<xsl:text>for (m : ENTITY_MENUS) {
  String path         = m[1];
  String functionCall = getEntityMenuPopulationFunction(m);

  execute(functionCall);
}
</xsl:text>
      <xsl:call-template name="entity-loading" />

    <xsl:if test="/module/logic">
      <xsl:text>
/******************************************************************************/
/*                             HANDWRITTEN LOGIC                              */
/******************************************************************************/
</xsl:text>
      <xsl:value-of select="/module/logic/text()"/>
    </xsl:if>

    <xsl:text>
/******************************************************************************/
/*                                    INIT                                    */
/*                                                                            */
/* Stuff which needs to be done last.                                         */
/******************************************************************************/
bindOnEvents();
</xsl:text>

  </xsl:template>

  <xsl:template name="tabgroups-to-validate">
    <xsl:for-each select="/module/*[.//*[contains(@f, 'notnull')]]">
      <xsl:text>  tabgroupsToValidate.add("</xsl:text>
      <xsl:value-of select="name()" />
      <xsl:text>");</xsl:text>
      <xsl:value-of select="$newline"/>
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="populate-author">
    <xsl:for-each select="//author">
      <xsl:text>  tabgroupToAuthor.put("</xsl:text>
      <xsl:value-of select="name(ancestor::*[last()-1])" />
      <xsl:text>", "</xsl:text>
      <xsl:value-of select="name(ancestor::*[last()-1])" />
      <xsl:text>/</xsl:text>
      <xsl:value-of select="name(ancestor::*[last()-2])" />
      <xsl:text>/author</xsl:text>
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
      <xsl:text>/timestamp</xsl:text>
      <xsl:text>");</xsl:text>
      <xsl:value-of select="$newline"/>
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="incautonum">
    <xsl:text>void incAutoNum(String destPath) {</xsl:text>
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
      <xsl:text>addOnEvent("</xsl:text>
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
    <xsl:for-each select="/module/*[
      not(name() = 'logic') and
      not(name() = 'rels') and
      not(contains(@f, 'nodata'))
      ]">
      <xsl:variable name="camelcase-tabgroup">
        <xsl:call-template name="string-replace-all">
          <xsl:with-param name="text" select="name()" />
          <xsl:with-param name="replace" select="'_'" />
          <xsl:with-param name="by" select="''" />
        </xsl:call-template>
      </xsl:variable>
      <xsl:text>void load</xsl:text>
      <xsl:value-of select="$camelcase-tabgroup"/>
      <xsl:text>From(String uuid) {
  String tabgroup = "</xsl:text><xsl:value-of select="name()"/><xsl:text>";
  setUuid(tabgroup, uuid);
  if (isNull(uuid)) return;

  FetchCallback cb = new FetchCallback() {
    onFetch(result) {
      populateEntityListsInTabGroup(tabgroup);
      // WARNING: The default behaviour of calling `onFetch</xsl:text>
      <xsl:value-of select="$camelcase-tabgroup"/>
      <xsl:text>()` upon fetching an entity is deprecated in this version of FAIMS Tools. If you never implemented this function, this warning can safely be ignored.
      onFetch</xsl:text><xsl:value-of select="$camelcase-tabgroup"/><xsl:text>__();
    }
  };

  showTabGroup(tabgroup, uuid, cb);
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

    <xsl:text>void new</xsl:text>
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
  populateAuthorAndTimestamp(tabgroup);
  populateEntityListsInTabGroup(tabgroup);
</xsl:text>

    <xsl:call-template name="tabgroup-new-incautonum"/>
    <xsl:text>  onCreate</xsl:text>
    <xsl:value-of select="$camelcase-tabgroup"/>
    <xsl:text>__();</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:value-of select="$newline"/>
    <xsl:text>  // WARNING: The default behaviour of calling `</xsl:text>
    <xsl:text>onCreate</xsl:text>
    <xsl:value-of select="$camelcase-tabgroup"/>
    <xsl:text>()` upon entity creation is deprecated in this version of FAIMS Tools. If you never implemented this function, this warning can safely be ignored.</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>}</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:value-of select="$newline"/>
  </xsl:template>

  <xsl:template name="tabgroup-oncreate">
    <xsl:variable name="camelcase-tabgroup">
      <xsl:call-template name="string-replace-all">
        <xsl:with-param name="text" select="name()" />
        <xsl:with-param name="replace" select="'_'" />
        <xsl:with-param name="by" select="''" />
      </xsl:call-template>
    </xsl:variable>
    <xsl:value-of select="$newline"/>
    <xsl:text>void onCreate</xsl:text>
    <xsl:value-of select="$camelcase-tabgroup"/>
    <xsl:text>__(){</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>  String ref      = "</xsl:text>
    <xsl:value-of select="name()"/>
    <xsl:text>";</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>  String event    = "create";</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>  String stmtsStr = getStatementsString(ref, event);</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>  execute(stmtsStr);</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>}</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:value-of select="$newline"/>
  </xsl:template>

  <xsl:template name="tabgroup-onfetch">
    <xsl:variable name="camelcase-tabgroup">
      <xsl:call-template name="string-replace-all">
        <xsl:with-param name="text" select="name()" />
        <xsl:with-param name="replace" select="'_'" />
        <xsl:with-param name="by" select="''" />
      </xsl:call-template>
    </xsl:variable>
    <xsl:value-of select="$newline"/>
    <xsl:text>// Triggered after an existing record is loaded.</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>void onFetch</xsl:text>
    <xsl:value-of select="$camelcase-tabgroup"/>
    <xsl:text>__(){</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>  String ref      = "</xsl:text>
    <xsl:value-of select="name()"/>
    <xsl:text>";</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>  String event    = "fetch";</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>  String stmtsStr = getStatementsString(ref, event);</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>  execute(stmtsStr);</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>}</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:value-of select="$newline"/>
  </xsl:template>

  <xsl:template name="tabgroup-onsave">
    <xsl:variable name="camelcase-tabgroup">
      <xsl:call-template name="string-replace-all">
        <xsl:with-param name="text" select="name()" />
        <xsl:with-param name="replace" select="'_'" />
        <xsl:with-param name="by" select="''" />
      </xsl:call-template>
    </xsl:variable>
    <xsl:value-of select="$newline"/>
    <xsl:text>// Triggered after an existing record is saved.</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>void onSave</xsl:text>
    <xsl:value-of select="$camelcase-tabgroup"/>
    <xsl:text>__(){</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>  String ref      = "</xsl:text>
    <xsl:value-of select="name()"/>
    <xsl:text>";</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>  String event    = "save";</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>  String stmtsStr = getStatementsString(ref, event);</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>  execute(stmtsStr);</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>}</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:value-of select="$newline"/>

    <xsl:text>addOnEvent("</xsl:text>
    <xsl:value-of select="name()"/>
    <xsl:text>", "save", "</xsl:text>
    <xsl:text>populateEntityListsOfArchEnt(\"</xsl:text>
    <xsl:value-of select="name()"/>
    <xsl:text>\")");</xsl:text>
    <xsl:value-of select="$newline"/>
  </xsl:template>

  <xsl:template name="tabgroup-oncopy">
    <xsl:variable name="camelcase-tabgroup">
      <xsl:call-template name="string-replace-all">
        <xsl:with-param name="text" select="name()" />
        <xsl:with-param name="replace" select="'_'" />
        <xsl:with-param name="by" select="''" />
      </xsl:call-template>
    </xsl:variable>
    <xsl:value-of select="$newline"/>
    <xsl:text>// Triggered as a record is duplicated but before it's saved.</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>void onCopy</xsl:text>
    <xsl:value-of select="$camelcase-tabgroup"/>
    <xsl:text>__(){</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>  String ref      = "</xsl:text>
    <xsl:value-of select="name()"/>
    <xsl:text>";</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>  String event    = "copy";</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>  String stmtsStr = getStatementsString(ref, event);</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>  execute(stmtsStr);</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>}</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:value-of select="$newline"/>
  </xsl:template>

  <xsl:template name="tabgroup-ondelete">
    <xsl:variable name="camelcase-tabgroup">
      <xsl:call-template name="string-replace-all">
        <xsl:with-param name="text" select="name()" />
        <xsl:with-param name="replace" select="'_'" />
        <xsl:with-param name="by" select="''" />
      </xsl:call-template>
    </xsl:variable>
    <xsl:value-of select="$newline"/>
    <xsl:text>void onDelete</xsl:text>
    <xsl:value-of select="$camelcase-tabgroup"/>
    <xsl:text>__(){</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>  String ref      = "</xsl:text>
    <xsl:value-of select="name()"/>
    <xsl:text>";</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>  String event    = "delete";</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>  String stmtsStr = getStatementsString(ref, event);</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>  execute(stmtsStr);</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>}</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:value-of select="$newline"/>
  </xsl:template>

  <xsl:template name="autonum-parent">
    <xsl:value-of select="name(//autonum/ancestor::*[last()-1])" />
    <!--<xsl:text>/</xsl:text>-->
    <!--<xsl:value-of select="name(//autonum/ancestor::*[last()-2])" />-->
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

    <xsl:text>void duplicate</xsl:text>
    <xsl:value-of select="$camelcase-tabgroup"/>
    <xsl:text>(){</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>  String tabgroup = "</xsl:text>
    <xsl:value-of select="name()"/>
    <xsl:text>";</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>  String uuidOld = getUuid(tabgroup);</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>  setUuid(tabgroup, "");</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:value-of select="$newline"/>
    <xsl:text>  disableAutoSave(tabgroup);</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:call-template name="tabgroup-duplicate-incautonum"/>
    <xsl:value-of select="$newline"/>
    <xsl:text>  clearGpsInTabGroup(tabgroup);</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>  populateAuthorAndTimestamp(tabgroup);</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>  populateEntityListsInTabGroup(tabgroup);</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:call-template name="tabgroup-duplicate-exclusions-1" />
    <xsl:value-of select="$newline"/>
    <xsl:text>  onCopy</xsl:text>
    <xsl:value-of select="$camelcase-tabgroup" />
    <xsl:text>__();</xsl:text>
<xsl:text>

  saveCallback = new SaveCallback() {
    onSave(uuid, newRecord) {
      setUuid(tabgroup, uuid);

      fetchAll(getDuplicateRelnQuery(uuidOld), new FetchCallback(){
        onFetch(result) {
          Log.e("Module", result.toString());

          if (result != null &amp;&amp; result.size() &gt;= 1) {
            parentTabgroup__ = result.get(0).get(4);
            parentTabgroup__ = parentTabgroup__.replaceAll(" ", "_");
          }

          makeDuplicateRelationships(result, getUuid(tabgroup));

          showToast("{Duplicated_record}");
          dialog.dismiss();
        }
      });

      saveTabGroup(tabgroup);
    }
  };

  String extraDupeAttributes = "";
  fetchAll(getDuplicateAttributeQuery(uuidOld, extraDupeAttributes), new FetchCallback(){
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
    <xsl:for-each select=".//*[@t and not(ancestor-or-self::*[contains(@f, 'nodata') or contains(@f, 'noui')]) and not(contains(@f, 'user'))]">
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
      not(ancestor-or-self::*[contains(@f, 'nodata') or contains(@f, 'noui')]) and not(contains(@f, 'user'))]">

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

    <xsl:text>void delete</xsl:text>
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

    <xsl:text>void reallyDelete</xsl:text>
    <xsl:value-of select="$camelcase-tabgroup" />
    <xsl:text>(){</xsl:text>
    <xsl:value-of select="$newline" />
    <xsl:text>  String tabgroup = "</xsl:text>
    <xsl:value-of select="name()"/>
    <xsl:text>";</xsl:text>
<xsl:text>
  deleteArchEnt(getUuid(tabgroup));
  cancelTabGroup(tabgroup, false);
  populateEntityListsOfArchEnt(tabgroup);
  onDelete</xsl:text><xsl:value-of select="$camelcase-tabgroup" /><xsl:text>__();
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
    <xsl:if test="name(ancestor::*[last()-1])">
      <xsl:text>/</xsl:text>
    </xsl:if>
    <xsl:value-of select="name(ancestor::*[last()-2])"/>
    <xsl:if test="name(ancestor::*[last()-2])">
      <xsl:text>/</xsl:text>
    </xsl:if>
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

  <xsl:template name="entity-menu">
    <xsl:for-each select="//*[@e]">
      <xsl:text>ENTITY_MENUS.add(new String[] {</xsl:text>
      <xsl:value-of select="$newline" />
      <xsl:choose>
        <xsl:when test="normalize-space(@t) = 'dropdown'">
          <xsl:text>  "DropDown",</xsl:text>
        </xsl:when>
        <xsl:otherwise>
          <xsl:text>  "List",</xsl:text>
        </xsl:otherwise>
      </xsl:choose>
      <xsl:value-of select="$newline" />
      <xsl:text>  "</xsl:text><xsl:call-template name="ref" /><xsl:text>",</xsl:text>
      <xsl:value-of select="$newline" />
      <xsl:text>  "getUuid(\"</xsl:text><xsl:value-of select="name(ancestor::*[last()-1])"/><xsl:text>\")",</xsl:text>
      <xsl:value-of select="$newline" />
      <xsl:text>  "</xsl:text>
      <xsl:call-template name="string-replace-all">
        <xsl:with-param name="text" select="@e" />
        <xsl:with-param name="replace" select="'_'" />
        <xsl:with-param name="by" select="' '" />
      </xsl:call-template>
      <xsl:text>",</xsl:text>
      <xsl:value-of select="$newline" />
      <xsl:text>  ""</xsl:text>
      <xsl:value-of select="$newline" />
      <xsl:text>});</xsl:text>
      <xsl:value-of select="$newline" />
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="entity-child-menu">
    <xsl:for-each select="//*[@ec]">
      <xsl:text>ENTITY_MENUS.add(new String[] {</xsl:text>
      <xsl:value-of select="$newline" />
      <xsl:choose>
        <xsl:when test="normalize-space(@t) = 'dropdown'">
          <xsl:text>  "DropDown",</xsl:text>
        </xsl:when>
        <xsl:otherwise>
          <xsl:text>  "List",</xsl:text>
        </xsl:otherwise>
      </xsl:choose>
      <xsl:value-of select="$newline" />
      <xsl:text>  "</xsl:text><xsl:call-template name="ref" /><xsl:text>",</xsl:text>
      <xsl:value-of select="$newline" />
      <xsl:text>  "getUuid(\"</xsl:text><xsl:value-of select="name(ancestor::*[last()-1])"/><xsl:text>\")",</xsl:text>
      <xsl:value-of select="$newline" />
      <xsl:text>  "</xsl:text>
      <xsl:call-template name="string-replace-all">
        <xsl:with-param name="text" select="@ec" />
        <xsl:with-param name="replace" select="'_'" />
        <xsl:with-param name="by" select="' '" />
      </xsl:call-template>
      <xsl:text>",</xsl:text>
      <xsl:value-of select="$newline" />
      <xsl:text>  "</xsl:text>
      <xsl:call-template name="string-replace-all">
        <xsl:with-param name="text" select="name(ancestor::*[last()-1])" />
        <xsl:with-param name="replace" select="'_'" />
        <xsl:with-param name="by" select="' '" />
      </xsl:call-template>
      <xsl:text> - </xsl:text>
      <xsl:call-template name="string-replace-all">
        <xsl:with-param name="text" select="@ec" />
        <xsl:with-param name="replace" select="'_'" />
        <xsl:with-param name="by" select="' '" />
      </xsl:call-template>
      <xsl:text>",</xsl:text>
      <xsl:value-of select="$newline" />
      <xsl:text>});</xsl:text>
      <xsl:value-of select="$newline" />
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="entity-loading">
    <xsl:for-each select="//*[(normalize-space(@t) = 'list' or normalize-space(@t) = '' or normalize-space(@t) = 'dropdown') and (@e or @ec)]">
      <xsl:text>addOnEvent("</xsl:text>
      <xsl:call-template name="ref" />
      <xsl:choose>
        <xsl:when test="normalize-space(@t) = 'dropdown'">
          <xsl:text>", "click", "loadEntity(true)");</xsl:text>
        </xsl:when>
        <xsl:otherwise>
          <xsl:text>", "click", "loadEntity()");</xsl:text>
        </xsl:otherwise>
      </xsl:choose>
      <xsl:value-of select="$newline" />
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="users">
    <xsl:for-each select="//*[contains(@f, 'user')][1]">
<xsl:text>
String userMenuPath = "</xsl:text><xsl:call-template name="ref" /><xsl:text>";

void populateListForUsers(){
  String getNonDeletedUsersQuery = "SELECT userid, fname || ' ' || lname "+
                                   "  FROM user "+
                                   " WHERE userdeleted is null;";

  fetchAll(getNonDeletedUsersQuery, new FetchCallback() {
    onFetch(result) {
</xsl:text>
    <xsl:call-template name="users-populate-call" />
<xsl:text>
    }
  });
}

void selectUser() {
</xsl:text>
    <xsl:call-template name="users-vocabid"/>
<xsl:text>
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
      userid   = result.get(0);
    }
  };

  fetchOne(userQ, callback);
}

addOnEvent(userMenuPath, "show",  "populateListForUsers()");
addOnEvent(userMenuPath, "click", "selectUser()");
</xsl:text>
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="users-populate-call">
    <xsl:choose>
      <xsl:when test="normalize-space(@t) = 'list' or normalize-space(@t) = ''">
        <xsl:text>      populateList(userMenuPath, result);</xsl:text>
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>      populateDropDown(userMenuPath, result, true);</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template name="users-vocabid">
    <xsl:choose>
      <xsl:when test="normalize-space(@t) = 'list' or normalize-space(@t) = ''">
        <xsl:text>  String userVocabId  = getListItemValue();</xsl:text>
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>  String userVocabId  = getFieldValue(userMenuPath);</xsl:text>
        <xsl:value-of select="$newline" />
        <xsl:text>  if (isNull(userVocabId)) {</xsl:text>
        <xsl:value-of select="$newline" />
        <xsl:text>    username = "";</xsl:text>
        <xsl:value-of select="$newline" />
        <xsl:text>    userid = "";</xsl:text>
        <xsl:value-of select="$newline" />
        <xsl:text>    return;</xsl:text>
        <xsl:value-of select="$newline" />
        <xsl:text>  }</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
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
    <xsl:if test="count(/module/*[not(contains(@f, 'nodata')) and not(name() = 'rels') and not(name() = 'logic') and (./*//*[not(ancestor-or-self::*[contains(@f, 'nodata') or contains(@f, 'user')]) and not(name() = 'cols') and not(name() = 'col') and not(name() = 'desc') and not(name() = 'opt') and not(name() = 'opts') and not(ancestor-or-self::rels) and not(normalize-space(@t) = 'group') and not(normalize-space(@t) = 'table') and not(normalize-space(@t) = 'gpsdiag') and not(normalize-space(@t) = 'map') and not(normalize-space(@t) = 'button')])]) &gt;= 2">
      <xsl:text>addOnEvent("</xsl:text><xsl:value-of select="name(/module/*[./search])"/><xsl:text>/Search/Entity_Types"  , "click" , "search()");</xsl:text>
      <xsl:value-of select="$newline" />
      <xsl:value-of select="$newline" />
      <xsl:text>entityTypes = new ArrayList();</xsl:text>
      <xsl:value-of select="$newline" />
      <xsl:text>entityTypes.add(new NameValuePair("{All}", ""));</xsl:text>
      <xsl:value-of select="$newline" />
      <xsl:for-each select="/module/*[
        not(name() = 'logic') and
        not(name() = 'rels') and
        not(contains(@f, 'nodata'))
        ]">
        <xsl:text>entityTypes.add(new NameValuePair("</xsl:text>
        <xsl:call-template name="label" />
        <xsl:text>", "</xsl:text>
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

  <xsl:template name="gps-diag-update">
    <xsl:for-each select="//*[normalize-space(@t) = 'gpsdiag'][1]">
      <xsl:text>addOnEvent("</xsl:text>
      <xsl:value-of select="name(ancestor::*[last()-1])"/>
      <xsl:text>/</xsl:text>
      <xsl:value-of select="name(ancestor::*[last()-2])"/>
      <xsl:text>", "show", "updateGPSDiagnostics()");</xsl:text>
      <xsl:value-of select="$newline" />
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="gps-diag-ref">
    <xsl:for-each select="//*[normalize-space(@t) = 'gpsdiag'][1]">
      <xsl:call-template name="ref" />
    </xsl:for-each>
  </xsl:template>

</xsl:stylesheet>
