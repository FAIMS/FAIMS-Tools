import formatter.StringFormatter;
import java.io.File;
import java.io.FileNotFoundException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import org.sqlite.Function;

public class Fetch {
    public static Connection conn = null;

    public static void verifyPathToFile(String pathToDb) throws FileNotFoundException {
        File newDbFile = new File(pathToDb);
        File newDbDir  = newDbFile.getParentFile();

        boolean exists = newDbDir.isDirectory();
        if (!exists)
            throw new FileNotFoundException(newDbDir.toString());
    }

    public static void useDatabase(String pathToDb) throws FileNotFoundException, SQLException {
        if (!"".equals(pathToDb))
            verifyPathToFile(pathToDb);

        // BEGIN ESTABLISHING THE NEW CONNECTION
        // 1. Disconnect previous db, if it exists
        if (conn != null) {
            try { conn.close(); } catch (SQLException e) { }
        }

        // 2. Connect new db
        String path = "jdbc:sqlite:" + pathToDb;
        conn = DriverManager.getConnection(path);

        Function.create(conn, "format",  new Function() {
            // Appropriated from the FAIMS app's code. Source:
            // https://github.com/FAIMS/faims-android/blob/437a0969723a2103a48dd47c06f5f4d0ad2dc73b/faimsandroidapp/src/main/java/au/org/intersect/faims/android/database/Database.java#L185
            public void xFunc() throws SQLException {
              // Copy xFunc's (i.e. format's) arguments into `argsToSub`. Not all
              // arguments get copied. Just the ones we want to substitute into a
              // format string expression
              int lenArgsToSub = Math.max(0, args() - 1);
              String[] argsToSub = new String[lenArgsToSub];
              for (int i = 0; i < args() - 1; i++)
                  argsToSub[i] = value_text(i+1);

              try {
                  if (args() < 1) {
                      result((String) null);
                  } else {
                      if (value_text(0) == null) {
                          String value = "";
                          for (int i = 1 ; i < args(); i++) {
                              if (value_text(i) != null) {
                                  if (!"".equals(value)) {
                                      value += ", ";
                                  }
                                  value += value_text(i);
                              }
                          }
                          result(value);
                      } else {
                          result(new StringFormatter(value_text(0)).preCompute().evaluate(argsToSub));
                      }
                  }
              } catch (Exception e) {
                  e.printStackTrace();

                  String eMsg = "Error trying to run formatter with arguments " + Arrays.toString(argsToSub) + ": " + e.getMessage();
                  System.out.println(eMsg);
                  error(eMsg);
              }
            }

            public void xStep() { }

            public void xFinal() { }
        });

        Function.create(conn, "AddGeometryColumn",  new Function() {
            public void xFunc() throws SQLException {
                System.err.println("Spatialite function `AddGeometryColumn` not implemented");
            }

            public void xStep() { }

            public void xFinal() { }
        });

        Function.create(conn, "CreateSpatialIndex",  new Function() {
            public void xFunc() throws SQLException {
                System.err.println("Spatialite function `CreateSpatialIndex` not implemented");
            }

            public void xStep() { }

            public void xFinal() { }
        });
    }

    public static void importFromDatabase(String path) throws Exception {
        verifyPathToFile(path);
        String query = "restore from " + path;

        if (conn == null)
            useDatabase("");
        Statement stmt = conn.createStatement();
        ResultSet rs = null;
        stmt.executeUpdate(query);

        try { if (rs   != null) rs  .close(); } catch (Exception e) {};
        try { if (stmt != null) stmt.close(); } catch (Exception e) {};
    }

    public static ArrayList<List<String>> fetchAll(String query) throws Exception {
        if (conn == null)
            useDatabase("");

        Statement stmt = conn.createStatement();
        ResultSet rs = null;
        try {
            rs = stmt.executeQuery(query);
        } catch (SQLException e) {
            if (!"query does not return ResultSet".equals(e.getMessage()))
              throw e;
        }

        ArrayList<List<String>> output = null;
        if (rs != null) {
            output = new ArrayList<List<String>>();

            // Get the number of columns
            ResultSetMetaData rsmd = rs.getMetaData();
            int numCols = rsmd.getColumnCount();

            // Load result set into array lists
            while(rs.next()) {
                // Unwrap the result set into a list
                List<String> row = new ArrayList<String>();
                for (int i = 1; i <= numCols; i++)
                    row.add(rs.getString(i));
                output.add(row);
            }
        }

        try { if (rs   != null) rs  .close(); } catch (Exception e) {};
        try { if (stmt != null) stmt.close(); } catch (Exception e) {};
        return output;
    }

    public static ArrayList<String> fetchOne(String query) throws Exception {
      ArrayList<List<String>> l = fetchAll(query);

      if (l        == null) return (ArrayList<String>) null;
      if (l.size() == 0   ) return (ArrayList<String>) new ArrayList<String>();

      return (ArrayList<String>) l.get(0);
    }
}
