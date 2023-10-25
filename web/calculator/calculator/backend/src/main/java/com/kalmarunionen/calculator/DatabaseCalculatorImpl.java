package com.kalmarunionen.calculator;

import java.sql.*;

public class DatabaseCalculatorImpl implements CalculatorService, AutoCloseable
{
    private Connection conn;

    public DatabaseCalculatorImpl() throws Exception
    {
        connect();
    }

    public String calculate(String expression) throws Exception
    {
        String escapedSql = String.format("SELECT %s as result", expression);
        try
        {
            return runQuery(escapedSql, true);
        } catch(SQLException e){
            return "SQLException: " + e.getMessage();
        } catch(Exception e){
            System.out.println("Exception: " + e.getMessage());
            return "Exception: " + e.getMessage();
        }
    }

    private void connect() throws Exception
    {
        conn = DriverManager.getConnection(
            System.getenv("DATABASE_URI"), 
            System.getenv("DATABASE_USER"), 
            System.getenv("DATABASE_PASSWORD"));
    }

    private String runQuery(String sql, boolean retry) throws Exception, SQLException
    {
        try (PreparedStatement statement = conn.prepareStatement(sql))
        {
            ResultSet resultSet = statement.executeQuery();
            return (resultSet.next() ? resultSet.getString(1) : "Failed to calculate");
        } catch(SQLException e){
            if(retry && (e.getMessage().contains("Connection is closed") || e.getMessage().contains("Socket error"))){
                System.out.println("Retry due to SQL exception: " + e.getMessage());
                connect();
                return runQuery(sql, false);
            }
            throw e;
        }
    }

    @Override
    public void close() throws Exception {
        conn.close();
    }
}