<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="text" indent="no"/>

  <xsl:variable name="newline" >
<xsl:text>
</xsl:text>
  </xsl:variable>

  <xsl:template match="/">

<xsl:text>
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

validateContext() {
  List f= new ArrayList(); // Fields to be validated

  String validationMessage = validateFields(f, "PLAINTEXT");
  showWarning("Validation Results", validationMessage);
}

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

saveTabGroup(String tabGroup) {
  String uuidVar = "uuid" + tabGroup.replaceAll("_", "");
  saveTabGroup(tabGroup, uuidVar);
}

saveTabGroup(String tabGroup, String uuidVar) {
  saveTabGroup(tabGroup, uuidVar, "");
}

saveTabGroup(String tabGroup, String uuidVar, String callback) {
  Boolean enableAutosave = true;
  String  id             = eval(uuidVar);
  List    geometry       = null;
  List    attributes     = null;
  SaveCallback saveCallback  = new SaveCallback() {
    onSave(uuid, newRecord) {
      eval(uuidVar + " = uuid;");
      execute(callback);
    }
    onError(message) {
      showToast(message);
    }
  };

  saveTabGroup(tabGroup, id, geometry, attributes, saveCallback, enableAutosave);
}

</xsl:text>

    <!-- User login stuff -->
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
    <xsl:for-each select="//*[@t and not(ancestor-or-self::*[contains(@f, 'onlyui')]) and not(contains(@f, 'user'))]">
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
    <xsl:for-each select="/module/*[.//*[contains(@f, 'notnull')]]">
      <xsl:text>validate</xsl:text>
      <xsl:call-template name="string-replace-all">
        <xsl:with-param name="text" select="name()" />
        <xsl:with-param name="replace" select="'_'" />
        <xsl:with-param name="by" select="''" />
      </xsl:call-template>
      <xsl:text>() {</xsl:text>
      <xsl:value-of select="$newline" />
      <xsl:text>  List fields = new ArrayList(); // Fields to be validated</xsl:text>
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
      <xsl:text>  String validationMessage = validateFields(fields, "PLAINTEXT");</xsl:text>
      <xsl:value-of select="$newline" />
      <xsl:text>  showWarning("Validation Results", validationMessage);</xsl:text>
      <xsl:value-of select="$newline" />
      <xsl:text>}</xsl:text>
    </xsl:for-each>

    <xsl:value-of select="$newline" />

    <!-- Autosaving -->
    <xsl:for-each select="/module/*[not(ancestor-or-self::*[contains(@f, 'onlyui')])]">
      <xsl:text>uuid</xsl:text>
      <xsl:call-template name="string-replace-all">
        <xsl:with-param name="text" select="name()" />
        <xsl:with-param name="replace" select="'_'" />
        <xsl:with-param name="by" select="''" />
      </xsl:call-template>
      <xsl:text> = null;</xsl:text>
      <xsl:value-of select="$newline" />
    </xsl:for-each>
    <xsl:value-of select="$newline" />
    <xsl:for-each select="/module/*[not(ancestor-or-self::*[contains(@f, 'onlyui')])]">
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
    <xsl:for-each select="/module/*[not(ancestor-or-self::*[contains(@f, 'onlyui')])]">
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
      <xsl:text>  newTab("</xsl:text>
      <xsl:value-of select="@l"/>
      <xsl:text>", true);</xsl:text>
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
onEvent(userMenuPath, "click", "selectUser()");
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

</xsl:stylesheet>
