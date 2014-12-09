import ciranda.*;
import ciranda.features.*;
import ciranda.utils.*;
import ciranda.classify.*;
import java.io.File;
import java.nio.file.Path;
import java.io.BufferedReader;
import java.io.*;

public class LabelEnronDataset {

private static final String DIRECTORY = "../enron_mail_20110402/maildir/";
private static final String OUT_FILE = "../message_class.labels";   // filename, request, deliver, commit, propose, meet, delivereddata
private static final String BODY_START_TOKEN = "X-FileName";

private static PrintWriter pw;

private static SpeechAct sa = new SpeechAct();

public static void main(String[] args){
        try {
                pw = new PrintWriter(OUT_FILE, "UTF-8");
                processDirectory(DIRECTORY);
                pw.close();
        } catch (FileNotFoundException e) {
                System.err.println("Failed to open " + OUT_FILE);
        } catch (UnsupportedEncodingException e) {
                System.err.println("Failed to open " + OUT_FILE);
        }
}

private static void processDirectory(String directory) {
        File [] subdirs = new File(directory).listFiles();
        System.out.println(directory + " has " + subdirs.length + " files to process.");
        for (File subdir : subdirs) {
                processSubDir(subdir);
        }
}

// subdir is a dir for allen-p, for example
private static void processSubDir(File subdir) {
        if (subdir == null) return;
        Path path = subdir.toPath();
        Path sentPath = path.resolve("sent");
        File [] sentPathDir = sentPath.toFile().listFiles();
        if (sentPathDir == null) return;
        System.out.println(subdir + " has " + sentPathDir.length + " files to process.");
        for (File sentEmail : sentPathDir) {
                processFile(sentEmail);
        }
        System.out.println(subdir + ": done!");
}

private static void processFile(File file) {

        String msg = getMsg(file);

        sa.loadMessage(msg);

        int request = sa.hasRequest() ? 1 : 0;
        int deliver = sa.hasDeliver() ? 1 : 0;
        int commit = sa.hasCommit() ? 1 : 0;
        int propose = sa.hasPropose() ? 1 : 0;
        int meet = sa.hasMeet() ? 1 : 0;
        int ddata = sa.hasDdata() ? 1 : 0;

        String result = file + " " + request + " " + deliver + " " + commit + " " + propose + " " + meet + " " + ddata;
        pw.println(result);
}

private static String getMsg(File file) {
        boolean write = false; // Wait for BODY_START_TOKEN
        try {
                BufferedReader br = new BufferedReader(new FileReader(file));
                StringBuilder sb = new StringBuilder();
                String line = br.readLine();

                while (line != null) {

                        if (write) {
                                sb.append(line);
                                sb.append(" ");
                        }

                        if (line.contains(BODY_START_TOKEN)) {
                                write = true;
                        }

                        line = br.readLine();
                }

                return sb.toString();
        } catch (FileNotFoundException e) {
                return null;
        } catch (IOException e) {
                return null;
        }
}
}
