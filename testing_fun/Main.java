import java.io.StringReader;

public class Main {
    public static void main(String[] args) {
        String input = "your test input here"; // <-- Replace with valid input for your grammar

        try {
            MyParser parser = new MyParser(new StringReader(input));
            parser.Start(); // Assumes "Start" is your entry point
            System.out.println("Parsing completed successfully.");
        } catch (ParseException e) {
            System.out.println("Parsing failed: " + e.getMessage());
        } catch (Exception e) {
            System.out.println("Unexpected error: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
