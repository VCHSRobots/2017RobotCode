package org.usfirst.frc4415.SteamShipBot1Final;

/********************************************************************************************
*																							*
*	TableReader - 	a program that reads a key-value table in from a host every 100ms and	*
*					offers access to its values.  The process occurs on a seperate thread.	*
* 																							*
*	02/06/2017 KJF Created.																	*
*																							*
********************************************************************************************/

import java.io.*;
import java.net.*;
import java.util.ArrayList;

public class TableReader extends Thread{
	
	private String hostName;
	private int portNumber;
	private static ArrayList<String> keyList;
	private static ArrayList<Double> valueList;
	private static String newLine = "";
	private boolean ready = false;
	
	public TableReader(String hostName, int portNumber){
		this.hostName = hostName;
		this.portNumber = portNumber;
		keyList = new ArrayList<String>();
		valueList = new ArrayList<Double>();
		this.setName("Table Thread");
	}
	
	// Required to overrun the run() method defined in Thread
	// run() is called by TableReader.start() in main thread
	public void run(){
		restart:
		while(true){
			threadMessage("New thread running.");
			// open a client socket with host
			try (
		            Socket clientSocket = new Socket(hostName, portNumber);
		            PrintWriter out =
		                new PrintWriter(clientSocket.getOutputStream(), true);
		            BufferedReader in =
		                new BufferedReader(
		                    new InputStreamReader(clientSocket.getInputStream()));
		            BufferedReader stdIn =
		                new BufferedReader(
		                    new InputStreamReader(System.in))
		        ) {
// RIO-Server Communication Initialization
				clientSocket.setSoTimeout(1000);
				out.println("Requesting rio_pi_communication");	
				try {
					Thread.sleep(100);
				} catch (InterruptedException e1) {
					e1.printStackTrace();
				}
				newLine = in.readLine();
				threadMessage(newLine);
				if(!newLine.equals("Request granted")){
					threadMessage("Request denied");
					break restart;
				}
// Request Table
				while(true){
					try {
						Thread.sleep(100);
					} catch (InterruptedException e1) {
						// TODO Auto-generated catch block
						e1.printStackTrace();
					}
					out.println("Requesting table");
					do{
						try{
							newLine = in.readLine();					// getting a null here instead of the first line of the table
						} catch (SocketException e){
							System.out.println("Server connection timed out.");
							break restart;
						}
						if(!newLine.equals("End of file")){	
							try{
								String newKey = extractKey(newLine);
								Double newValue = extractValue(newLine);
								updateTable(newKey, newValue);	
							} 	catch(NullPointerException e){
								threadMessage("Null Pointer Exception caught");
							}
						}
					}	while(!newLine.equals("End of file"));
// Check the incoming table for a time stamp
					if(!keyList.contains("timestamp")){
						threadMessage("No timestamp included, exiting thread");
						return;
					}
					ready = true;
					printTable();
					threadMessage("End of file received.");
					while(true){
// sleep for 100ms
						try{
							Thread.sleep(100);
						}	catch(InterruptedException e){
							threadMessage("TableReader thread interrupted.");
							return;
						}
// check if timestamp changed					
						out.println("Requesting timestamp");
						try{
							newLine = in.readLine();
						} catch (SocketException e){
							System.out.println("Server connection timed out.");
							break restart;
						}
// if timestamp changed, update table
						if (Double.parseDouble(newLine) != valueList.get(keyList.indexOf("timestamp"))){
							break;
						}
					}
				}						
			}	catch (UnknownHostException e) {
	            	System.err.println("Don't know about host " + hostName);
	        }	catch (IOException e) {
	        		threadMessage("Couldn't get IO connection to " + hostName);
	        }
// if failing to make a connection, sleep 100ms and try again
			try{
				Thread.sleep(100);
			} 	catch (InterruptedException e){
				threadMessage("Thread interrupted at connection attempt.");
				return;
			}
		}
	}
	
	public static String extractKey(String newLine) throws NullPointerException{
		String newKey = newLine.substring(0, newLine.indexOf("=")).toLowerCase().trim();
		return newKey;
	}
	
	public static Double extractValue(String newLine)throws NullPointerException{
		Double newValue = Double.parseDouble(newLine.substring(newLine.indexOf("=")+1));
		return newValue;
	}
	
	public static void updateTable(String newKey, Double newValue){
		if (keyList.contains(newKey)){
			valueList.set(keyList.indexOf(newKey), newValue);
		} else {
			keyList.add(newKey);
			valueList.add(newValue);
		}
	}
	
	public static void printTable(){
		for(int i = 0; i < keyList.size(); i++){
			threadMessage(keyList.get(i) + ": " + valueList.get(i));
		}
		System.out.println();
	}
	
	public static void threadMessage(String message){
		
		// this method displays the name of the thread, followed by the message
		
		String threadName = Thread.currentThread().getName();
		System.out.format("%s: %s%n", threadName, message);
	}
	
	public double get(String key, double deFault){
		if (ready){	
			return valueList.get(keyList.indexOf(key));
		} else {
			return deFault;
		}
	}
	
	public boolean isReady(){
		return ready;
	}
	
}