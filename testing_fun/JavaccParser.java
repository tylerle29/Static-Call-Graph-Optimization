import java.io.StringReader;
import java.nio.file.Files;
import java.nio.file.Path;
import com.code_intelligence.jazzer.api.FuzzedDataProvider;
import com.code_intelligence.jazzer.api.BugDetectors;
import com.code_intelligence.jazzer.api.FuzzerSecurityIssueLow;

public class JavaccParser {
    public static void fuzzerTestOneInput(FuzzedDataProvider data) {
    System.out.println("Entered fuzzerTestOneInput");

    try {
      BugDetectors.allowNetworkConnections();

      // Get the input string
      String input = data.consumeRemainingAsString();
      System.out.println("=== Fuzz input ===");
      System.out.println(input);
      // Write input to a temp file to simulate a corpus file path

      // Call entrypoint
      Entrypoint.entrypoint(input);

    } catch (Exception e) {
      System.err.println("Caught exception: " + e);
    } catch (Throwable t) {
                // Crash = bug? Only escalate non-expected errors
                throw new FuzzerSecurityIssueLow("Unhandled exception: " + t);
    }

  }
}
