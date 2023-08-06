
import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintStream;
import java.io.PrintWriter;
import java.io.StringReader;
import java.io.Writer;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.regex.Matcher;
import java.util.stream.Stream;

import javax.naming.spi.ObjectFactoryBuilder;
import javax.print.DocFlavor.READER;
import javax.print.DocFlavor.URL;
import javax.tools.JavaCompiler;

import com.fasterxml.jackson.core.JsonFactory;
import com.fasterxml.jackson.core.JsonFactoryBuilder;
import com.fasterxml.jackson.core.JsonGenerator;
import com.fasterxml.jackson.core.JsonLocation;
import com.fasterxml.jackson.core.JsonParseException;
import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.ObjectCodec;
import com.fasterxml.jackson.core.StreamReadFeature;
import com.fasterxml.jackson.core.StreamWriteFeature;
import com.fasterxml.jackson.core.TreeNode;
import com.fasterxml.jackson.core.Version;
import com.fasterxml.jackson.core.JsonFactory.Feature;
import com.fasterxml.jackson.core.json.JsonReadFeature;
import com.fasterxml.jackson.core.json.JsonWriteFeature;
import com.fasterxml.jackson.core.type.ResolvedType;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.*;

public class Test {
    public static void main(String[] args) throws IOException {
        File file = new File("filer.json");
        Map<String, String> map = parseJson(file, "teams");
        File csv = toCSV(map);
    }


    public static Map<String, String> parseJson(File json, String key) throws JsonParseException, IOException {
        try {
            PrintWriter writer = new PrintWriter(json);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        JsonFactory factory = JsonFactory.builder().configure(Feature.USE_THREAD_LOCAL_FOR_BUFFER_RECYCLING, true)
                .configure(JsonWriteFeature.ESCAPE_NON_ASCII, true)
                .configure(JsonReadFeature.ALLOW_UNESCAPED_CONTROL_CHARS, true)
                .configure(StreamReadFeature.USE_FAST_DOUBLE_PARSER, true)
                .configure(StreamWriteFeature.AUTO_CLOSE_CONTENT, true).build();

        JsonParser parser = factory.createParser(json);
        Map<String, String> map = new HashMap<>();
        parser.overrideCurrentName(key);
        TypeReference<List<String>> ref = new TypeReference<List<String>>() {
        };
        parser.setCodec(new Team());
        Iterator<String> iterator = parser.readValueAs(ref);
        TreeNode node = parser.getCodec().readTree(parser);
        Iterator<String> iteratorr = node.get(key).fieldNames();
        int i = 0;
        while (iteratorr.hasNext()) {
            i++;
            map.put("team" + Integer.toString(i), iteratorr.toString());
        }

        return map;
    }

    public static File toCSV(Map<String, String> data) throws IOException {
        File csvFile = new File("teams.csv");
        csvFile.createNewFile();
        PrintWriter writer = new PrintWriter(csvFile);
        for (Entry<String, String> indivData : data.entrySet()) {
            writer.write(indivData.toString() + "\n");
        }
        writer.close();

        return csvFile;
    }

    public File toFile(ArrayList<String[]> dataStream, File file) {
        try (FileWriter writerr = new FileWriter(file)) {
            for (String[] data : dataStream) {
                StringBuilder line = new StringBuilder();
                for (int i = 0; i < data.length; i++) {
                    line.append(data[i]);
                    if (i < data.length - 1) {
                        line.append(",");
                    }
                }
                writerr.write(line.toString() + "\n");
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        return file;
    }

    public static class Team extends ObjectCodec {
 

        @Override

        public Version version() {
            // TODO Auto-generated method stub
            return null;
        }

        @Override
        public <T> T readValue(JsonParser p, Class<T> valueType) throws IOException {
            return null;
        }

        @Override
        public <T> T readValue(JsonParser p, TypeReference<T> valueTypeRef) throws IOException {
            // TODO Auto-generated method stub
            return null;
        }

        @Override
        public <T> T readValue(JsonParser p, ResolvedType valueType) throws IOException {
            // TODO Auto-generated method stub
            return null;
        }

        @Override
        public <T> Iterator<T> readValues(JsonParser p, Class<T> valueType) throws IOException {
            // TODO Auto-generated method stub
            return null;
        }

        @Override
        public <T> Iterator<T> readValues(JsonParser p, TypeReference<T> valueTypeRef) throws IOException {
            // TODO Auto-generated method stub
            return null;
        }

        @Override
        public <T> Iterator<T> readValues(JsonParser p, ResolvedType valueType) throws IOException {
            // TODO Auto-generated method stub
            return null;
        }

        @Override
        public void writeValue(JsonGenerator gen, Object value) throws IOException {
            // TODO Auto-generated method stub

        }

        @Override
        public <T extends TreeNode> T readTree(JsonParser p) throws IOException {
            // TODO Auto-generated method stub
            return null;
        }

        @Override
        public void writeTree(JsonGenerator gen, TreeNode tree) throws IOException {
            // TODO Auto-generated method stub

        }

        @Override
        public TreeNode createObjectNode() {
            // TODO Auto-generated method stub
            return null;
        }

        @Override
        public TreeNode createArrayNode() {
            // TODO Auto-generated method stub
            return null;
        }

        @Override
        public JsonParser treeAsTokens(TreeNode n) {
            // TODO Auto-generated method stub
            return null;
        }

        @Override
        public <T> T treeToValue(TreeNode n, Class<T> valueType) throws JsonProcessingException {
            // TODO Auto-generated method stub
            return null;
        }


    }
}
