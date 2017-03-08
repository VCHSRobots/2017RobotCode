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
	private int m_nTableUpdates = 0;
	private int m_nTableRestarts = 0;
	private int m_nTableTimeStamps = 0;
	
	public TableReader(String hostName, int portNumber){
		this.hostName = hostName;
		this.portNumber = portNumber;
		this.setName("Table Reader");
		keyList = new ArrayList<String>();
		valueList = new ArrayList<Double>();
	}
	
	private void sleep(int ms){
		try{
			Thread.sleep(ms);
		} 	catch (InterruptedException e){
			threadMessage("Table Reader: Thread interrupted at connection attempt.");
		}
	}
	
	// Required to overrun the run() method defined in Thread
	// run() is called by TableReader.start() in main thread
	public void run(){
		while(true){
			restart:
			while(true){
				m_nTableRestarts++;
				threadMessage(String.format("Table Reader: New thread running.  Number Restarts = %d", m_nTableRestarts));
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
					out.println("Requesting rio_pi_communication");	   // Do not Change this!!! This is actual command being sent to Jetson!
					sleep(100);
					newLine = in.readLine();
					if (newLine == null ) {
						threadMessage("Table Reader: Null received on initial request.  Restarting after small wait.");
						sleep(400);
						break restart;
					}
					threadMessage(newLine);
					if(!newLine.equals("Request granted")){
						threadMessage("Table Reader: Request denied");
						break restart;
					}
					threadMessage("Table Reader: Request granted");
					// Request Table
					while(true){
						sleep(100);
						out.println("Requesting table");	// Do not goof this up: This is an actual command being sent to Jetson!
						do{
							try{
								newLine = in.readLine();					// getting a null here instead of the first line of the table
							} catch (SocketException e){
								System.out.println("Server connection timed out.");
								break restart;
							}
							if (newLine == null) {
								threadMessage("Table Reader: Illegal response from Jetson.  Null recevied after requesting the table.  Restarting.");
								break restart;
							}
							if(!newLine.equals("End of file")){	
								try{
									String newKey = extractKey(newLine);
									Double newValue = extractValue(newLine);
									updateTable(newKey, newValue);	
								} 	catch(NullPointerException e){
									threadMessage("Table Reader: Null Pointer Exception caught.  Key/Value not updated.");
								}	catch(java.lang.StringIndexOutOfBoundsException ee) {
									threadMessage("Table Reader: Something wrong with a line in the table (" + newLine + ")"); 
								}
							}
						}	while(!newLine.equals("End of file"));
						m_nTableUpdates++;
						threadMessage(String.format("Table Reader: New table update.  Number of updates = %d", m_nTableUpdates));
						// Check the incoming table for a time stamp
						if(!keyList.contains("timestamp")){
							threadMessage("Table Reader: No timestamp included, exiting thread.  NO TABLE READER WILL BE ACTIVE FROM THIS POINT FORWARD.");
							return;
						}
						ready = true;
						threadMessage("Table Reader: End of file received.");
						printTable();
						while(true){
							sleep(100);
							// check if timestamp changed					
							out.println("Requesting timestamp");  // Do not change this!  Actual command to Jetson being sent!
							try{
								newLine = in.readLine();
								int iDoNullAgain = 0;
								while (newLine == null && iDoNullAgain < 20) {
									newLine = in.readLine();
									iDoNullAgain++;
									sleep(10);
								}
								if(newLine == null){
									threadMessage("Table Reader: Recieved null timestamp Many Times.  Reconnecting.");
									break restart;
								}
							} catch (SocketException e){
								threadMessage("Table Reader: Server connection timed out. Reconnecting");
								break restart;
							}
							m_nTableTimeStamps++;
							if (m_nTableTimeStamps % 100 == 0) {
								threadMessage(String.format("Table Reader: Number of Timestamps received = %d", m_nTableTimeStamps));
							}
							// if timestamp changed, update table
							if (Double.parseDouble(newLine) != valueList.get(keyList.indexOf("timestamp"))){
								break;
							}
						}
					}						
				}	catch (UnknownHostException e) {
					threadMessage("Table Reader: Don't know about host " + hostName);
					// At this point, we will fall through, wait 100 ms (below), and start a new connection.
		        }	catch (IOException e) {
		        	threadMessage("Table Reader: Couldn't get I/O for the connection to " + hostName);
		        	// At this point, we will fall through, wait 100 ms (below), and start a new connection.
		        }
				// if failing to make a connection, sleep 100ms and try again
				sleep(100);
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