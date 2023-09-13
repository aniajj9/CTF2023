package com.kalmarunionen.calculator;

import static spark.Spark.delete;
import static spark.Spark.get;
import static spark.Spark.options;
import static spark.Spark.post;
import static spark.Spark.put;
import static spark.Spark.*;
import java.util.regex.*;

public class MainController 
{
    public static void main(String[] args) throws Exception 
    {
        final CalculatorService calculator = new DatabaseCalculatorImpl();

        get("/status", (request, response) -> {
            System.out.println("Endpoint /status called");
            response.type("text/plain");
            return "HEALTHY";
        });

        post("/calculate", (request, response) -> {
            String expression = request.queryParams("expression");

            if(expression == null || !isValidExpression(expression)){
                return "Invalid expression, try again!";
            }
            
            return calculator.calculate(expression);
        });
    }

    private static boolean isValidExpression(String expression) 
    {
        Pattern pattern = Pattern.compile("^[0-9 )(.+-]+$", Pattern.MULTILINE);
        Matcher matcher = pattern.matcher(expression);
        return matcher.find();
    }
}