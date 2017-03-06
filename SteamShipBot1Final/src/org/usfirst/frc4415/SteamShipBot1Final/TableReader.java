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
import java.util.concurrent.locks.*;
import java.net.*;
import java.util.ArrayList;

public class TableReader extends Thread{
	
	private String hostName;
	private int portNumber;
	private static ArrayList<String> keyList;                  // DLB: why static?  and others not?
	private static ArrayList<Double> valueList;
	private static String newLine = "";
	private boolean ready = false;							   // Shoudn't this be static too?
	private static Lock datalock = new ReentrantLock();
	
	public TableReader(String hostName, int portNumber){
		this.hostName = hostName;
		this.portNumber = portNumber;
		this.setName("Table Reader");
		keyList = new ArrayList<String>();
		valueList = new ArrayList<Double>();
	}
	
// Required to overrun the run() method defined in Thread
	// run() is called by TableReader.start() in main thread
	public void run(){
		while(true){
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
								if(newLine == null){
									threadMessage("Recieved null timestamp.  Reconnecting.");
									break restart;
								}
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
		            	// DLB: what should be done here?  I suggest break restart.
		        }	catch (IOException e) {
		            	System.err.println("Couldn't get I/O for the connection to " +
		            			hostName);
		            	// DLB: what should be done here?  I suggest break restart.
		        }
	// if failing to make a connection, sleep 100ms and try again
				try{
					Thread.sleep(100);
				} 	catch (InterruptedException e){
					threadMessage("Thread interrupted at connection attempt.");
					return;  // DLB: How does this "try again"
				}
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
		datalock.lock();
		if (keyList.contains(newKey)){
			valueList.set(keyList.indexOf(newKey), newValue);
		} else {
			keyList.add(newKey);
			valueList.add(newValue);
		}
		datalock.unlock();
	}
	
	@SuppressWarnings("unchecked")
	public static void printTable(){
		ArrayList<String> tempkeys;
		ArrayList<Double> tempvals;
		datalock.lock();
		tempkeys =  (ArrayList<String>) keyList.clone();     // DLB: Not sure these casts work.. 
		tempvals = (ArrayList<Double>) valueList.clone();
		datalock.unlock();
		
		for(int i = 0; i < tempkeys.size(); i++){
			threadMessage(tempkeys.get(i) + ": " + tempvals.get(i));
		}
		System.out.println();
	}
	
	public static void threadMessage(String message){
		
		// this method displays the name of the thread, followed by the message
		
		String threadName = Thread.currentThread().getName();
		System.out.format("%s: %s%n", threadName, message);
	}
	
	public double get(String key, double deFault){
		datalock.lock();  // Prevents changes while user is accessing table.
		double v = deFault;
		if (ready){	
			int indx = keyList.indexOf(key);
			if (indx >= 0 && indx < valueList.size()) {
				v = valueList.get(indx);
			}
		} else {
			System.out.println("Table not available");
		}
		datalock.unlock();  // Release other parts of the program to continue...
		return v;
	}
	
	public boolean isReady(){
		return ready;
	}
	
}