package org.usfirst.frc4415.SteamShipBot1Final;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.SocketException;
import java.net.UnknownHostException;

import com.kauailabs.navx.frc.AHRS;

import edu.wpi.first.wpilibj.smartdashboard.SmartDashboard;

public class MouseReader extends Thread {
	
	private String hostName;
	private int portNumber;
	private AHRS navX;
	private static String xFieldString = "";
	private static String yFieldString = "";
	private static double xField = 0;
	private static double yField = 0;
	
	public MouseReader(String hostName, int portNumber, AHRS navX){
		this.hostName = hostName;
		this.portNumber = portNumber;
		this.navX = navX;
		this.setName("Mouse Thread");
	}
	
	public void run(){			

		while(true){
			try (
				Socket clientSocket = new Socket(hostName, portNumber);
				PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);
			    BufferedReader in = new BufferedReader(
			    		new InputStreamReader(clientSocket.getInputStream()));
			    BufferedReader stdIn = new BufferedReader(
			                    new InputStreamReader(System.in))
			){
				clientSocket.setSoTimeout(1000);
				out.println("Requesting field_coordinates");
				try{
					threadMessage(in.readLine());
				} catch (SocketException e){
					System.out.println("Socket Timed Out at request recv'd Read Operation");
					return;
				}
				while(true){
					try{
						String gyroAngle = new Double(navX.getAngle()).toString();
						//String gyroAngle = "45.0";
						out.println(gyroAngle);
					//	out.println(new Double(ahrs.getAngle()).toString());
					} catch (RuntimeException e){
						System.out.println("Gyro Read Fail: " + e.getMessage());
					}
					try{
						xFieldString = in.readLine();					// KEEPS READING UNTIL LINE BREAK "\n"
					} catch (SocketException e){
						System.out.println("Socket Timed Out at xFieldString Read Operation" + e.getMessage());
					}
					
					
					//threadMessage("xField: " + xFieldString);
					out.println("xFieldString Recieved!");
					try{
						yFieldString = in.readLine();					// KEEPS READING UNTIL LINE BREAK "\n"
					} catch (SocketException e){
						System.out.println("Socket Timed Out at yFieldString)Read Operation" + e.getMessage());
					}
					
					//threadMessage("Field Location:   X = " + xFieldString + "   Y = " + yFieldString);
					
					SmartDashboard.putString("xField", xFieldString);
					SmartDashboard.putString("yField", yFieldString);
					try{
						Thread.sleep(20);
					} catch (InterruptedException e){
						threadMessage(e.getMessage());
						break;
					}
	/*					try{
							Thread.sleep(50);
						} catch (InterruptedException e){
							threadMessage("Interrupted exception caught at sleep method. " + e.getMessage());
							break;		// if you do a return here: out, in and stdIn never get closed,
										// and therefore you get a resource leak
						}
	*/
				}
				
			} catch (UnknownHostException e) {
	            System.err.println("Don't know about host " + hostName);
	            return;
	        } catch (IOException e) {
	            threadMessage("Couldn't get IO connection to " + hostName);
	        } 	
			try{
				Thread.sleep(100);
			} catch (InterruptedException e){
				threadMessage("Interrupted exception caught at sleep during reconnect");
			}
		}
	}
	
	public static void threadMessage(String message){
		
		// this method displays the name of the thread, followed by the message
		
		String threadName = Thread.currentThread().getName();
		System.out.format("%s: %s%n", threadName, message);
	}
	
	public double getXField(){
		xField = Double.parseDouble(xFieldString);
		return xField;
	}
	
	public double getYField(){
		yField = Double.parseDouble(yFieldString);
		return yField;
	}
}

