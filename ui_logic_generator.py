#!/usr/bin/python
# Yes, this is disgusting. Don't judge.
import fileinput, sys

archents = []
# Write to stderr this line won't appear when you pipe out from stdout.
sys.stderr.write("Enter archent names using capitals and spaces, ie Bucket, Tower Pole. Press Enter for each new archent.\n")

print """/*** 'Editable' - you can edit the code below based on the needs ***/
User user; // don't touch
String userid;

/*setSyncEnabled(true);
setFileSyncEnabled(true);*/

makeLocalID(){
    fetchOne("CREATE TABLE IF NOT EXISTS localSettings (key text primary key, value text);");
    fetchOne("drop view if exists identifierAsSpreadsheet;");
    fetchOne("create view identifierAsSpreadsheet as select uuid, group_concat(coalesce(measure || ' ' || vocabname || '(' ||freetext||')',  measure || ' (' || freetext ||')',  vocabname || ' (' || freetext ||')',  measure || ' ' || vocabname ,  vocabname || ' (' || freetext || ')',  measure || ' (' || freetext || ')',  measure,  vocabname,  freetext,  measure,  vocabname,  freetext), ' ') as response from (select * from latestNonDeletedArchentIdentifiers order by attributename) group by uuid;");
}

makeLocalID();"""

for line in fileinput.input():
    archents.append(line)

for archent in archents:
    archent = archent.rstrip()
    archent_id = archent.lower().replace(" ", "_") + "_id"
    archent_ui = archent.replace(" ", "_")
    archent_method = archent.replace(" ", "")
    print "String " + archent_id + """ = null;

new""" + archent_method + """() {
    """ + archent_id + """ = null;
    newTabGroup(\"""" + archent_ui + """\");
}

load""" + archent_method + """() {
    """ + archent_id + """ = getListItemValue();
    load""" + archent_method + """From(""" + archent_id + """);
}

load""" + archent_method + """From(archentid) {
    """ + archent_id + """ = archentid;
    if (isNull(""" + archent_id + """)) {
        showToast("No """ + archent + """ selected");
        return;
    }

    showTabGroup(\"""" + archent_ui + """\", """ + archent_id + """);
}

save""" + archent_method + """(String callback) {
    /* Add identifiers
    if (isNull()) {
        showWarning("Validation Error", "Cannot save """ + archent + """ without identifiers");
        return;
    }
    */
    if (!isNull(""" + archent_id + """)) {
        entity = fetchArchEnt(""" + archent_id + """);
    }
    saveTabGroup(\"""" + archent_ui + """\", """ + archent_id + """, null, null, \"""" + archent_id + """ = getLastSavedRecordId();" + callback);
}

delete""" + archent_method + """() {
    if (!isNull(""" + archent_id + """)) {
        showAlert("Confirm Deletion", "Press OK to Delete this """ + archent + """!", "reallyDelete""" + archent_method + """()", "doNotDelete()");
    } else {
        cancelTabGroup(\"""" + archent_ui + """\", true);
    }
}

reallyDelete""" + archent_method + """() {
    deleteArchEnt(""" + archent_id + """);
    cancelTabGroup(\"""" + archent_ui + """\", false);
}

load""" + archent_method + """Attributes() {
}
"""
print """/*** MISC ***/

saveEntitiesToRel(type, entity1, entity2) {
    if (isNull(entity1) || isNull(entity2)) return;
    
    rel_id = saveRel(null, type, null, null);
    addReln(entity1, rel_id, null);
    addReln(entity2, rel_id, null);
}

saveEntitiesToHierRel(type, entity1, entity2, e1verb, e2verb) {
    if (isNull(entity1) || isNull(entity2)) return;
    
    rel_id = saveRel(null, type, null, null);
    addReln(entity1, rel_id, e1verb);
    addReln(entity2, rel_id, e2verb);
}

makeVocab(String attrib) {
    Object a = fetchAll("select vocabid, vocabname from vocabulary join attributekey using (attributeid) where attributename = '"+attrib+"' ");
    return a;
}

getVocabName(String vocabid) {
    Object a = fetchOne("select vocabName from vocabulary where vocabid = '"+ vocabid +"';");
    return a.get(0);
}

makePictureGallery(String attrib) {
    fetchAll("select vocabid, vocabname, pictureurl from vocabulary left join attributekey using (attributeid) where attributename = '" + attrib + "' order by vocabname;");
}

doNotDelete() {
    showToast("Delete Cancelled.");
}

fillInGPS(String path) {
    Object position = getGPSPosition();    
    Object projPosition = getGPSPositionProjected();
    if (projPosition != null ){
        Double latitude = position.getLatitude();
        Double longitude = position.getLongitude();
        Double northing = projPosition.getLatitude();
        Double easting = projPosition.getLongitude();
        setFieldValue(path+"Latitude", latitude);
        setFieldValue(path+"Longitude", longitude);
        setFieldValue(path+"Northing", northing);
        setFieldValue(path+"Easting", easting);
    } else {
        showToast("GPS Not initialized");
    }
}

/*** 'Uneditable' - you can edit the code below with extreme precaution ***/

DATA_ENTRY_LAYER = "Data Entry Layer";
DATA_ENTRY_LAYER_ID = 0;

initMap() {
    setMapZoom("Context/map/map", 15.0f);

    showBaseMap("Context/map/map", "Base Layer", "files/data/maps/OraraSmall.tif");
    createCanvasLayer("Context/map/map", "Non-saved sketch layer");

    DATA_ENTRY_LAYER_ID = createCanvasLayer("Context/map/map", DATA_ENTRY_LAYER);

    isEntity = true;
    queryName = "All entities";
    querySQL = "SELECT uuid, aenttimestamp FROM latestNonDeletedArchEntIdentifiers";
        
    addDatabaseLayerQuery("Context/map/map", queryName, querySQL);

    addTrackLogLayerQuery("Context/map/map", "track log entities", 
        "SELECT uuid, max(aenttimestamp) as aenttimestamp " + 
        " FROM archentity join aenttype using (aenttypeid) " +
        " where archentity.deleted is null " + 
        "   and lower(aenttypename) = lower('gps_track') " + 
        " group by uuid " + 
        " having max(aenttimestamp)");
        
    addSelectQueryBuilder("Context/map/map", "Select entity by type", createQueryBuilder(
        "select uuid " + 
        "  from latestNonDeletedArchent " + 
        "  JOIN latestNonDeletedAentValue using (uuid) " + 
        "  join aenttype using (aenttypeid) " + 
        "  LEFT OUTER JOIN vocabulary using (vocabid, attributeid) " + 
        "  where lower(aenttypename) = lower(?) " + 
        "   group by uuid").addParameter("Type", "RemoteSensingContext"));
        
    //addLegacySelectQueryBuilder("Context/map/map", "Select geometry by id", "files/data/maps/sydney.sqlite", "Geology100_Sydney", 
    //    createLegacyQueryBuilder("Select PK_UID from Geology100_Sydney where PK_UID = ?").addParameter("ID", null));
                    
    // define database layer styles for points, lines, polygons and text
    ps = createPointStyle(10, Color.BLUE, 0.2f, 0.5f);
    ls = createLineStyle(10, Color.GREEN, 0.05f, 0.3f, null);
    pos = createPolygonStyle(10, Color.parseColor("#440000FF"), createLineStyle(10, Color.parseColor("#AA000000"), 0.01f, 0.3f, null));
    ts = createTextStyle(10, Color.WHITE, 40, Typeface.SANS_SERIF);

    showDatabaseLayer("Context/map/map", "Saved Data Layer", isEntity, queryName, querySQL, ps, ls, pos, ts);
}

//initMap();


/*** TRACKLOG ***/
/*
setGPSUpdateInterval(4);

onEvent("control/gps/startTimeLog", "click", "startTrackingGPS(\\"time\\", 10, \\"saveTimeGPSTrack()\\")");
onEvent("control/gps/startDistanceLog", "click", "startTrackingGPS(\\"distance\\", 10, \\"saveDistanceGPSTrack()\\")");
onEvent("control/gps/stopTrackLog", "click", "stopTrackingGPS()");

saveTimeGPSTrack() {
    List attributes = createAttributeList();
    attributes.add(createEntityAttribute("gps_type", "time", null, null, null));
    saveGPSTrack(attributes);
}

saveDistanceGPSTrack() {
    List attributes = createAttributeList();
    attributes.add(createEntityAttribute("gps_type", "distance", null, null, null));
    saveGPSTrack(attributes);
}

saveGPSTrack(List attributes) {
    position = getGPSPosition();
    if (position == null) return;

    //attributes.add(createEntityAttribute("gps_user", "" + user.getUserId(), null, null, null));
    attributes.add(createEntityAttribute("gps_timestamp", "" + getCurrentTime(), null, null, null));
    attributes.add(createEntityAttribute("gps_longitude", "" + position.getLongitude(), null, null, null));
    attributes.add(createEntityAttribute("gps_latitude", "" + position.getLatitude(), null, null, null));
    //attributes.add(createEntityAttribute("gps_heading", "" + getGPSHeading(), null, null, null));
    attributes.add(createEntityAttribute("gps_accuracy", "" + getGPSEstimatedAccuracy(), null, null, null));
    
    positionProj = getGPSPositionProjected();
    Point p = new Point(new MapPos(positionProj.getLongitude(), positionProj.getLatitude()), null, (PointStyle) null, null);
    ArrayList l = new ArrayList();
    l.add(p);
    
    saveArchEnt(null, "gps_track", l, attributes);
}
*/
/*** USER ***/

getDefaultUsersList() {
    users = fetchAll("select userid, fname ||' ' || lname from user");
    return users;
}

populateListForUsers(){
    populateDropDown("user/usertab/users", getDefaultUsersList());
    populateRadioGroup("user/usertab/Area_Code", makeVocab("AreaCode"));

    Object localArea = fetchOne("select value from localSettings where key = 'Area';");
    Object localUser = fetchOne("select value from localSettings where key = 'User';");

    if (!isNull(localArea)){
        setFieldValue("user/usertab/Area_Code", localArea.get(0));
    }

    if (!isNull(localUser)){
        setFieldValue("user/usertab/users", localUser.get(0));
    }

}

populateListForUsers();

String username = "";
String device = "";
String areaCode = "";

login(){
    if(isNull(getFieldValue("user/usertab/Area_Code")) || isNull(getFieldValue("user/usertab/users"))){
        showWarning("Warning", "Please select a User and an Area Code before logging in.");
    } else {
        Object userResult = fetchOne("select userid,fname,lname,email from user where userid='" + getFieldValue("user/usertab/users") + "';");
        User user = new User(userResult.get(0),userResult.get(1),userResult.get(2),userResult.get(3));
        userid = userResult.get(0);
        setUser(user);
        username = userResult.get(1) + " " + userResult.get(2);
        showTabGroup("control");

        fetchOne("REPLACE INTO localSettings(key, value) VALUES('User', '"+userid+"');");
        fetchOne("REPLACE INTO localSettings(key, value) VALUES('Area', '"+getFieldValue("user/usertab/Area_Code")+"');");

        areaCode = fetchOne("select vocabid, vocabname from vocabulary join localSettings on (value=vocabid) where key = 'Area' ").get(1);
    }

}

onEvent("user/usertab/login", "click", "login()");
onEvent("user/usertab/guide", "click", "showTab(\\"user/help\\")");

/*** SYNC ***/

onEvent("control/gps/startsync", "click", "startSync()");
onEvent("control/gps/stopsync", "click", "stopSync()");

setSyncMinInterval(10.0f);
setSyncMaxInterval(20.0f);
setSyncDelay(5.0f);

startSync() {
    setSyncEnabled(true);
    setFileSyncEnabled(true);
}

stopSync() {
    setSyncEnabled(false);
    setFileSyncEnabled(false);
}
"""

for archent in archents:
    archent_method = archent.replace(" ", "").rstrip()
    print "load" + archent_method + "Attributes();"