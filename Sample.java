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
