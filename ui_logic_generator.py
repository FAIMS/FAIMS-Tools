#!/usr/bin/python

# Written by Vincent Tran

# NEEDS A COMPLETE REWRITE
import fileinput, sys

archents = []
# Write to stderr this line won't appear when you pipe out from stdout.
sys.stderr.write("Do you need to specify an area code or something similar when you log in? [Y/n]\n")
line = raw_input()
listLogin = False
if line == "n" or line == "N":
    listLogin = True

sys.stderr.write("Enter archent names using capitals and spaces, ie Bucket, Tower Pole. Press Enter for each new archent.\n")

print """/*** 'Editable' - you can edit the code below based on the needs ***/
import java.util.concurrent.Callable;
User user; // don't touch
String userid;

/*setSyncEnabled(true);
setFileSyncEnabled(true);*/

makeLocalID(){
    fetchOne("CREATE TABLE IF NOT EXISTS localSettings (key text primary key, value text);");
    fetchOne("drop view if exists identifierAsSpreadsheet;");
    fetchOne("create view identifierAsSpreadsheet as select uuid, group_concat(coalesce(measure || ' ' || vocabname || '(' ||freetext||')',  measure || ' (' || freetext ||')',  vocabname || ' (' || freetext ||')',  measure || ' ' || vocabname ,  vocabname || ' (' || freetext || ')',  measure || ' (' || freetext || ')',  measure,  vocabname,  freetext,  measure,  vocabname,  freetext), ' ') as response from (select * from latestNonDeletedArchentIdentifiers order by attributename) group by uuid;");
}

makeLocalID();

/*** CONTROL ***/
// Put your control tab things here
onEvent("control", "show", "refreshBuildings();removeNavigationButtons();");

removeNavigationButtons() {
    removeNavigationButton("save");
    removeNavigationButton("save_and_new");
    removeNavigationButton("delete");
}

"""

for line in fileinput.input():
    archents.append(line)

for archent in archents:
    archent = archent.rstrip()
    archent_id = archent.lower().replace(" ", "_") + "_id"
    archent_ui = archent.replace(" ", "_")
    archent_method = archent.replace(" ", "")
    print "/*** " + archent.upper() + """***/

onEvent(\"""" + archent_ui + """\", "show", "add""" + archent_method + """Navigation();");
/* Only necessary when you can return to this tab group from a child tab group
onEvent(\"""" + archent_ui + """\", "show", "add""" + archent_method + """Navigation();autoSave""" + archent_method + """();");
*/
/* Only necessary when autosaving should be activated when a specific field is filled in
onFocus("Path/To/Required_Filed", null, "activateAutoSave""" + archent_method + """();");
*/

String """ + archent_id + """ = null;

new""" + archent_method + """() {
    newTabGroup(\"""" + archent_ui + """\");
    """ + archent_id + """ = null;
}

load""" + archent_method + """() {
    """ + archent_id + """ = getListItemValue();
    load""" + archent_method + """From(""" + archent_id + """);
}

load""" + archent_method + """From(archentid) {
    if (isNull(archentid)) {
        showToast("No {""" + archent + """} selected");
        return;
    }

    showTabGroup(\"""" + archent_ui + """\", archentid, new FetchCallback() {
        onFetch(result) {
            """ + archent_id + """ = archentid;
            saveTabGroup(\"""" + archent_ui + "\", " + archent_id + """, null, null, new SaveCallback() {
                onSave(uuid, newRecord) {
                    """ + archent_id + """ = uuid;
                }
            }, true);
        }
    });
}

save""" + archent_method + """(Callable callback) {
    /* Add required fields
    if (isNull()) {
        showWarning("Validation Error", "Cannot save {""" + archent + """} without required fields");
        return;
    }
    */
    saveTabGroup(\"""" + archent_ui + """\", """ + archent_id + """, null, null, new SaveCallback() {
        onSave(uuid, newRecord) {
            """ + archent_id + """ = uuid;
            if(callback != null) callback.call();
        }
    });
}

/* Only necessary when autosaving should be activated when a specific field is filled in
activateAutoSave""" + archent_method + """() {
    if(!isNull(""" + archent_id + """)) return;
    /* Add required fields
    if (isNull()) return;
    */
    saveTabGroup(""" + archent_method + """, """ + archent_id + """, null, null, new SaveCallback() {
        onSave(uuid, newRecord) {
            """ + archent_id + """ = uuid;
            saveTabGroup(""" + archent_method + """, """ + archent_id + """, null, null, new SaveCallback() {
                onSave(uuid, newRecord) {
                    """ + archent_id + """ = uuid;
                }
            }, true);
        }
    });
}
*/

/* Only necessary when you can return to this tab group from a child tab group
autosave""" + archent_method + """() {
    if(isNull(""" + archent_id + """)) return;
    saveTabGroup("""" + archent_method + """", """ + archent_id + """, null, null, new SaveCallback() {
        onSave(uuid, newRecord) {
            """ + archent_id + """ = uuid;
        }
    }, true);
}
*/

delete""" + archent_method + """() {
    if (!isNull(""" + archent_id + """)) {
        showAlert("Confirm Deletion", "Press OK to Delete this {""" + archent + """}!", "reallyDelete""" + archent_method + """()", "doNotDelete()");
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
    archent_method = archent.replace(" ", "").rstrip()
    print "\nload" + archent_method + """Attributes();

add""" + archent_method + """Navigation();() {
    removeNavigationButton("save");
    removeNavigationButton("save_and_new");
    removeNavigationButton("delete");   

    addNavigationButton("save", new ActionButtonCallback() {
        actionOnLabel() {
            "Save {""" + archent_method + """}";
        }
        actionOn() {
            save""" + archent_method + """(null);
        }
    }, "success");

    addNavigationButton("save_and_new", new ActionButtonCallback() {
        actionOnLabel() {
            "Save and New {""" + archent_method + """}";
        }
        actionOn() {
            save""" + archent_method + """(new Callable() {
                call() {
                    new""" + archent_method + """();
                }
            });
        }
    }, "success");

    addNavigationButton("delete", new ActionButtonCallback() {
        actionOnLabel() {
            "Delete {""" + archent_method + """}";
        }
        actionOn() {
            delete""" + archent_method + """();
        }
    }, "danger");
}

"""

print """/*** MISC ***/

saveEntitiesToRel(String type, String entity1, String entity2) {
    if (isNull(entity1) || isNull(entity2)) return;
    saveRel(null, type, null, null, new SaveCallback() {
        onSave(rel_id, newRecord) {
            addReln(entity1, rel_id, null);
            addReln(entity2, rel_id, null);
        }
    });
}

saveEntitiesToRel(String type, String entity1, String entity2, Callable callback) {
    if (isNull(entity1) || isNull(entity2)) return;
    saveRel(null, type, null, null, new SaveCallback() {
        onSave(rel_id, newRecord) {
            addReln(entity1, rel_id, null);
            addReln(entity2, rel_id, null);
            if(callback != null) callback.call();
        }
    });
}

saveEntitiesToHierRel(String type, String entity1, String entity2, String e1verb, String e2verb) {
    if (isNull(entity1) || isNull(entity2)) return;
    saveRel(null, type, null, null, new SaveCallback() {
        onSave(rel_id, newRecord) {
            addReln(entity1, rel_id, e1verb);
            addReln(entity2, rel_id, e2verb);
        }
    });
}

makeVocab(String type, String path, String attrib){
    fetchAll("select vocabid, vocabname from vocabulary join attributekey using (attributeid) where attributename = '"+attrib+"' order by vocabcountorder",
        new FetchCallback() {
            onFetch(result) {
                if(type.equals("CheckBoxGroup")) {
                    populateCheckBoxGroup(path, result);
                } else if(type.equals("DropDown")) {
                    populateDropDown(path, result);
                } else if(type.equals("RadioGroup")) {
                    populateRadioGroup(path, result);
                } else if(type.equals("List")) {
                    populateList(path, result);
                }
            }
        });
}

makePictureGallery(String path, String attrib) {
    fetchAll("select vocabid, vocabname, pictureurl from vocabulary left join attributekey using (attributeid) where attributename = '" + attrib + "' order by vocabcountorder;",
        new FetchCallback() {
            onFetch(result) {
                populatePictureGallery(path, result);
            }
        });
}

doNotDelete() {
    showToast("Delete Cancelled.");
}

fillInGPS(String path) {
    Object position = getGPSPosition();
    Object projPosition = getGPSPositionProjected();
    if (position != null) {
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
/*** USER ***/
"""
if listLogin:
    print """loadUsers() {
    fetchAll("select userid, fname || ' ' || lname from user", new FetchCallback() {
        onFetch(result) {
            populateList("user/usertab/users", result);
        }
    });
}

loadUsers();

String username = "";

login() {
    fetchOne("select userid,fname,lname,email from user where userid='" + getListItemValue() + "';", new FetchCallback() {
        onFetch(result) {
            user = new User(result.get(0),result.get(1),result.get(2),result.get(3));
            setUser(user);
            username = result.get(1) + " " + result.get(2);
            showTabGroup("control");
        }
    });
}

"""
else:
    print """populateListForUsers() {
    fetchAll("select userid, fname ||' ' || lname from user", new FetchCallback() {
        onFetch(result) {
            populateDropDown("user/usertab/users", result);
            fetchOne("select value from localSettings where key = 'User';", new FetchCallback() {
                onFetch(result) {
                    if (!isNull(result)){
                        setFieldValue("user/usertab/users", result.get(0));
                    }
                }
            });  
        }
    });

    fetchOne("select value from localSettings where key = 'Area';", new FetchCallback() {
        onFetch(result) {
            if (!isNull(result)){
                setFieldValue("user/usertab/area", result.get(0));
            }
        }
    });
}

populateListForUsers();

String username = "";
String areaCode = "";

login(){
    if(isNull(getFieldValue("user/usertab/area")) || isNull(getFieldValue("user/usertab/users"))){
        showWarning("Warning", "Please select a User and enter an Area before logging in.");
    } else {
        fetchOne("select userid,fname,lname,email from user where userid='" + getFieldValue("user/usertab/users") + "';",
            new FetchCallback() {
                onFetch(result) {
                    User user = new User(result.get(0),result.get(1),result.get(2),result.get(3));
                    userid = result.get(0);
                    setUser(user);
                    username = result.get(1) + " " + result.get(2);
                    showTabGroup("control");

                    fetchOne("REPLACE INTO localSettings(key, value) VALUES('User', '"+userid+"');", null);
                    fetchOne("REPLACE INTO localSettings(key, value) VALUES('Area', '"+getFieldValue("user/usertab/area")+"');", null);
                    areaCode = getFieldValue("user/usertab/area");
                }
            });
    }
}

"""
print """onEvent("user/usertab/login", "click", "login()");

/*** SYNC ***/
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

addActionBarItem("sync", new ToggleActionButtonCallback() {
    actionOnLabel() {
        "Sync enabled";
    }
    actionOn() {
        setSyncEnabled(false);
        setFileSyncEnabled(false);
        showToast("Sync disabled.");
    }
    isActionOff() {
        isSyncEnabled();
    }
    actionOffLabel() {
        "Sync disabled";
    }
    actionOff() {
        setSyncEnabled(true);
        setFileSyncEnabled(true);
        showToast("Sync enabled.");
    }
});

addActionBarItem("internal_gps", new ToggleActionButtonCallback() {
    actionOnLabel() {
        "Internal GPS enabled";
    }
    actionOn() {
        stopGPS();
        showToast("GPS disabled.");
    }
    isActionOff() {
        isInternalGPSOn();
    }
    actionOffLabel() {
        "Internal GPS disabled";
    }
    actionOff() {
        if(isExternalGPSOn()) {
            stopGPS();
        }
        startInternalGPS();
        showToast("GPS enabled.");
    }
});

addActionBarItem("external_gps", new ToggleActionButtonCallback() {
    actionOnLabel() {
        "External GPS enabled";
    }
    actionOn() {
        stopGPS();
        showToast("GPS disabled.");

    }
    isActionOff() {
        isExternalGPSOn();
    }
    actionOffLabel() {
        "External GPS disabled";
    }
    actionOff() {
        if(isInternalGPSOn()) {
            stopGPS();
        }
        startExternalGPS();
        if(isBluetoothConnected()) {
            showToast("GPS enabled.");
        } else {
            showToast("Please enable bluetooth.");
            this.isActionOff();
        }
    }
});
"""