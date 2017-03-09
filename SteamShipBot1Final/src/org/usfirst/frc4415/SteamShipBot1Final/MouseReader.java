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
	private String xFieldString = "";
	private String yFieldString = "";
	private int m_nRestarts = 0;
	private int m_nReports = 0;
	
	public MouseReader(String hostName, int portNumber, AHRS navX){
		this.hostName = hostName;
		this.portNumber = portNumber;
		this.navX = navX;
		this.setName("Mouse Thread");
	}
	
	private void sleep(int ms) {
		try{
			Thread.sleep(ms);
		} catch (InterruptedException e){
			threadMessage("Mouse Reader.  Sleep was interrupted: " + e.getMessage());
		}
	}
	
	public int getNumRestarts() {
		return m_nRestarts;
	}
	
	public int getNumReports() {
		return m_nReports;
	}
	
	public void run(){			
		while(true){
			restart:
			while(true){
				m_nRestarts++;
				threadMessage(String.format("Mouse Reader: Number of full restarts = %d", m_nRestarts));
				try (
					Socket clientSocket = new Socket(hostName, portNumber);
					PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);
				    BufferedReader in = new BufferedReader(
				    		new InputStreamReader(clientSocket.getInputStream()));
				    BufferedReader stdIn = new BufferedReader(
				                    new InputStreamReader(System.in))
				){
					clientSocket.setSoTimeout(1000);
					out.println("Requesting field_coordinates");  // Dont change this.  This is an actual command for the Jetson.
					try{
						String response = in.readLine();
						threadMessage("Mouse Reader: Response to request of field_coordinates: " + response);
					} catch (SocketException e){
						System.out.println("Mouse Reader: Socket Timed Out at request recv'd Read Operation.  Reconnecting.");
						sleep(200);
						break restart;
					}
					while(true){
						try{
							String gyroAngle = "-999999";
							if (navX != null) {
								gyroAngle = new Double(navX.getAngle()).toString();
							}
							out.println(gyroAngle);
						//	out.println(new Double(ahrs.getAngle()).toString());
						} catch (RuntimeException e){
							threadMessage("Mouse Reader: Gyro Read Fail: " + e.getMessage());
						}
						try{
							xFieldString = in.readLine();					// KEEPS READING UNTIL LINE BREAK "\n"
							if(xFieldString==null){
								threadMessage("Mouse Reader: xField is null. Reconnecting.");
								sleep(200);
								break restart;
							}
						} catch (SocketException e){
							threadMessage("Mouse Reader: Socket Timed Out at xFieldString Read Operation.  Reconnecting." + e.getMessage());
							sleep(200);
							break restart;
						}
						
						out.println("xFieldString Recieved!");  // This is an actual command to the Jetson!
						try{
							yFieldString = in.readLine();					// KEEPS READING UNTIL LINE BREAK "\n"
							if(yFieldString==null){
								threadMessage("Mouse Reader: yField is null. Reconnecting.");
								sleep(200);
								break restart;
							}
						} catch (SocketException e){
							threadMessage("Mouse Reader: Socket Timed Out at yFieldString)Read Operation. Reconnecting. " + e.getMessage());
							sleep(200);
							break restart;
						}
						
						m_nReports++;
						if(m_nReports % 250 == 0) {
							threadMessage(String.format("Mouse Reader:  Number of reports received: %d",  m_nReports));
						}
						//threadMessage("Mouse Reader: Field Location:   X = " + xFieldString + "   Y = " + yFieldString);
						
						//SmartDashboard.putString("xField", xFieldString);
						//SmartDashboard.putString("yField", yFieldString);
						
						sleep(20);
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
					threadMessage("Mouse Reader: Don't know about host " + hostName + ".  Exiting -- NO MOUSE READER WILL BE ACTIVE!");
		            return;
		        } catch (IOException e) {
		            threadMessage("Mouse Reader: Couldn't get IO connection to " + hostName + ". Reconnecting.");
		        } 	
				sleep(100);
			}
		}
	}
	
	public static void threadMessage(String message){
		
		// this method displays the name of the thread, followed by the message
		
		String threadName = Thread.currentThread().getName();
		System.out.format("%s: %s%n", threadName, message);
	}
	
	public double getXField(){
		double xField = -999999;
		try{
			xField = Double.parseDouble(xFieldString);
		} catch(NumberFormatException e){
			//threadMessage("xField string does not contain a parsable double.");
			//throw e;
		} catch(NullPointerException e){
			//threadMessage("xField string is null");
			//throw e;
		}
		return xField;
	}
	
	public double getYField(){
		double yField = -999999;
		try{
			yField = Double.parseDouble(yFieldString);
		} catch(NumberFormatException e){
			//threadMessage("yField string does not contain a parsable double.");
			//throw e;
		} catch(NullPointerException e){
			//threadMessage("yField string is null");
			//throw e;
		}
		return yField;
	}
}

