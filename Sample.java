import com.github.javaparser.JavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;

import java.io.FileInputStream;
import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class MethodCallExtractor {

    public static void main(String[] args) throws IOException {
        // Parse the Java file
        FileInputStream in = new FileInputStream("path/to/your/BankAccountService.java");
        CompilationUnit cu = JavaParser.parse(in);

        // Extract method calls
        MethodCallCollector collector = new MethodCallCollector();
        collector.visit(cu, null);

        // Print the results
        Map<String, List<String>> methodCalls = collector.getMethodCalls();
        for (Map.Entry<String, List<String>> entry : methodCalls.entrySet()) {
            System.out.println("Method: " + entry.getKey());
            for (String call : entry.getValue()) {
                System.out.println("  Call: " + call);
            }
        }
    }

    private static class MethodCallCollector extends VoidVisitorAdapter<Void> {
        private final Map<String, List<String>> methodCalls = new HashMap<>();

        @Override
        public void visit(MethodDeclaration md, Void arg) {
            super.visit(md, arg);
            MethodCallVisitor methodCallVisitor = new MethodCallVisitor();
            methodCallVisitor.visit(md, null);
            methodCalls.put(md.getNameAsString(), methodCallVisitor.getCalls());
        }

        public Map<String, List<String>> getMethodCalls() {
            return methodCalls;
        }
    }

    private static class MethodCallVisitor extends VoidVisitorAdapter<Void> {
        private final List<String> calls = new ArrayList<>();

        @Override
        public void visit(MethodCallExpr mc, Void arg) {
            super.visit(mc, arg);
            calls.add(mc.getNameAsString());
        }

        public List<String> getCalls() {
            return calls;
        }
    }
}

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class ExpressionEvaluator {
    public static void main(String[] args) {
        String expression = "abc.get().newthing(Abc.class,\"12\").find(abc.find(),\"re\")";
        parseExpression(expression);
    }

    public static void parseExpression(String expression) {
        // Define regex patterns to match method calls and arguments
        Pattern pattern = Pattern.compile("(\\w+)\\.(\\w+)\\(([^)]*)\\)|" +  // Method calls with arguments
                                           "(\\w+)\\.(\\w+)\\(|" +          // Method calls without arguments
                                           "(\\w+)\\(([^)]*)\\)");         // Method calls inside arguments
        
        Matcher matcher = pattern.matcher(expression);

        while (matcher.find()) {
            // Group 1 & 2: Method call with arguments
            String object = matcher.group(1);
            String method = matcher.group(2);
            String arguments = matcher.group(3);
            
            if (method != null) {
                System.out.println("Method - " + method + "()");
                if (arguments != null && !arguments.isEmpty()) {
                    List<String> argsList = parseArguments(arguments);
                    System.out.println("Argument - " + String.join(", ", argsList));
                }
            }

            // Group 4 & 5: Method call without arguments
            String methodWithoutArgs = matcher.group(5);
            if (methodWithoutArgs != null) {
                System.out.println("Method - " + methodWithoutArgs + "()");
            }

            // Group 6 & 7: Method call within arguments
            String innerMethod = matcher.group(6);
            String innerArguments = matcher.group(7);
            if (innerMethod != null) {
                System.out.println("Method - " + innerMethod + "()");
                if (innerArguments != null && !innerArguments.isEmpty()) {
                    List<String> innerArgsList = parseArguments(innerArguments);
                    System.out.println("Argument - Method - " + String.join(", ", innerArgsList));
                }
            }
        }
    }

    // Method to parse and extract arguments
    private static List<String> parseArguments(String argsString) {
        List<String> arguments = new ArrayList<>();
        StringBuilder argBuilder = new StringBuilder();
        boolean insideQuotes = false;

        for (char c : argsString.toCharArray()) {
            if (c == '"' && (argBuilder.length() == 0 || argBuilder.charAt(argBuilder.length() - 1) != '\\')) {
                insideQuotes = !insideQuotes;
                argBuilder.append(c);
            } else if (c == ',' && !insideQuotes) {
                arguments.add(argBuilder.toString().trim());
                argBuilder.setLength(0);
            } else {
                argBuilder.append(c);
            }
        }

        if (argBuilder.length() > 0) {
            arguments.add(argBuilder.toString().trim());
        }

        return arguments;
    }
}

