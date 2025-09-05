import java.io.File;
import java.nio.file.Files;
import java.io.IOException;

import java.io.ByteArrayInputStream;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;

import org.w3c.dom.DOMImplementation;
import org.w3c.dom.Document;
import org.xml.sax.ErrorHandler;
import org.xml.sax.SAXParseException;
import org.apache.xalan.xslt.Process;

//import com.code_intelligence.jazzer.api.FuzzedDataProvider;
import javax.xml.transform.*;
import javax.xml.transform.stream.StreamResult;
import javax.xml.transform.stream.StreamSource;
import java.io.*;
import java.nio.file.*;

import javax.xml.transform.*;
import javax.xml.transform.stream.*;
import java.io.*;
import java.nio.file.*;

public class Checker {
    public static void main(String[] args) throws IOException, TransformerException {
        if (args.length < 2) {
            System.out.println("Usage: java Checker <xml-file> <xsl-file>");
            return;
        }

        // Read XML and XSL contents from file paths
        String xml = Files.readString(Paths.get(args[0]));
        String xsl = Files.readString(Paths.get(args[1]));

        // Create transformer
        TransformerFactory factory = TransformerFactory.newInstance();
        Transformer transformer = factory.newTransformer(new StreamSource(new StringReader(xsl)));

        // Output result to string
        StringWriter output = new StringWriter();
        transformer.transform(
            new StreamSource(new StringReader(xml)),
            new StreamResult(output)
        );

        // Print output
        System.out.println("Transformation Result:");
        System.out.println(output.toString());
    }
}
